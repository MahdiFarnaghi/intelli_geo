# Temporary imports
import json
import os
import asyncio

from qgis.PyQt.QtCore import QThreadPool, pyqtSignal, QObject

from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from langchain_community.vectorstores import FAISS
from langchain_cohere import ChatCohere
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek

from .utils import show_variable_popup, getVersion, getCurrentTimeStamp, pack
from .tools import readEnvironment
from .responseWorker import ResponseWorker, ReflectWorker
from .dataloader import Dataloader


class Processor(QObject):
    responseReady = pyqtSignal(str, str, str, str)
    reflectionReady = pyqtSignal(str, str, str, str)
    errorSignal = pyqtSignal(str)

    def __init__(self, llmID, conversationID, retrievalVectorbase, dataloader):
        super().__init__()
        self.latestInteractionID = None
        self.llmID = llmID
        self.dataloader = Dataloader("IntelliGeo.db")

        self.llmProvider, self.llmName = llmID.split("::")
        _, apiKey = dataloader.fetchAPIKey(self.llmID)
        if self.llmProvider == "OpenAI":
            self.llm = ChatOpenAI(model=self.llmName, openai_api_key=apiKey, temperature=0)
        elif self.llmProvider == "Cohere":
            self.llm = ChatCohere(model=self.llmName, cohere_api_key=apiKey, temperature=0)
        elif self.llmProvider == "DeepSeek":
            self.llm = ChatDeepSeek(model=self.llmName, api_key=apiKey, temperature=0)

        self.conversationID = conversationID
        self.retrivalDatabase = retrievalVectorbase
        self.outputParser = StrOutputParser()
        self.version = getVersion()

        self.threadpool = QThreadPool()  # Create a thread pool

    def classifier(self, userInput: str) -> str:
        """
        Base on the given `userInput`, decide if it is asking about producing workflow (model, code).
        Return "yes" or "no".
        """
        requestTime = getCurrentTimeStamp()
        classifierPromptRow = self.dataloader.fetchPrompt(self.llmID, promptType="classifier", testing=True)
        classifierPrompt = ChatPromptTemplate.from_template(classifierPromptRow["template"])

        show_variable_popup(classifierPrompt)

        classifierChain = classifierPrompt | self.llm | self.outputParser
        decision = classifierChain.invoke({"input": userInput})
        responseTime = getCurrentTimeStamp()

        # ["conversationID", "promptID",
        #  "requestText", "contextText", "requestTime", "typeMessage",
        #  "responseText", "responseTime", "workflow", "executionLog"]
        interactionRow = [self.conversationID, classifierPromptRow["ID"],
                          userInput, "", requestTime, "input",
                          decision, responseTime, "empty", ""]
        self.dataloader.insertInteraction(interactionRow, self.conversationID)

        return decision

    def reactionRouter(self, userInput, responseType):
        decision = self.classifier(userInput)
        show_variable_popup(decision)

        if decision.lower() in ["no", "yes, yes", "yes, no"]:
            if decision.lower() == "no":
                generalChatResponse = self.generalChat(userInput)

                return generalChatResponse, "empty"

            elif decision.lower() == "yes, no":
                if responseType == "Visual mode":
                    modelProducerResponse = self.modelProducer(userInput)
                    return modelProducerResponse, "withModel"
                elif responseType == "Code":
                    codeProducerResponse, interactionID = self.codeProducer(userInput)
                    return codeProducerResponse, "withCode"
                else:
                    codeProducerResponse, interactionID = self.toolBoxProducer(userInput)
                    return codeProducerResponse, "withToolbox"

            else:
                if responseType == "Visual mode":
                    modelProducerResponse = self.modelRefine(userInput)
                    return modelProducerResponse, "withModel"
                elif responseType == "Code":
                    codeProducerResponse, interactionID = self.codeRefine(userInput)
                    return codeProducerResponse, "withCode"
                else:
                    codeProducerResponse, interactionID = self.toolBoxRefine(userInput)
                    return codeProducerResponse, "withToolbox"

        elif "yes" in decision.lower():
            if responseType == "Visual mode":
                modelProducerResponse = self.modelProducer(userInput)
                return modelProducerResponse, "withModel"
            elif responseType == "Code":
                codeProducerResponse, interactionID = self.codeProducer(userInput)
                return codeProducerResponse, "withCode"
            else:
                codeProducerResponse, interactionID = self.toolBoxProducer(userInput)
                return codeProducerResponse, "withToolbox"

        else:
            confirmChain = self.confirmChain()

    def generalChat(self, userInput: str) -> str:
        requestTime = getCurrentTimeStamp()

        generalChatPromptRow = self.dataloader.fetchPrompt(self.llmID, promptType="generalChat")
        template = generalChatPromptRow["template"]
        show_variable_popup(template)
        humanMessage = HumanMessage(template.format(input=userInput))
        messageList = [humanMessage]

        tools = [readEnvironment]
        llmWithTools = self.llm.bind_tools(tools)
        llmMessage = llmWithTools.invoke(messageList)
        messageList.append(llmMessage)

        if len(llmMessage.tool_calls) == 0:
            contextText = ""
            chatReturn = self.outputParser.invoke(llmMessage)

        else:
            for toolcall in llmMessage.tool_calls:
                selectedTool = {"readenvironment": readEnvironment}[toolcall["name"].lower()]
                toolOutput = selectedTool.invoke(toolcall["args"])
                messageList.append(ToolMessage(toolOutput, tool_call_id=toolcall["id"]))

            contextText = "-------------".join([message.content for message in messageList])

            # langchain inference
            chatChain = llmWithTools | self.outputParser
            chatReturn = chatChain.invoke(messageList)
        show_variable_popup(chatReturn)
        responseTime = getCurrentTimeStamp()

        # ["conversationID", "promptID",
        #  "requestText", "contextText", "requestTime", "typeMessage",
        #  "responseText", "responseTime", "workflow", "executionLog"]
        interactionRow = [self.conversationID, generalChatPromptRow["ID"],
                          userInput, contextText, requestTime, "return",
                          chatReturn, responseTime, "empty", ""]
        self.dataloader.insertInteraction(interactionRow, self.conversationID)

        return chatReturn

    def modelProducer(self, userInput: str) -> str:
        requestTime = getCurrentTimeStamp()

        generalChatPromptRow = self.dataloader.fetchPrompt(self.llmID, promptType="modelProducer")
        template = generalChatPromptRow["template"]

        # get example
        retrievedExample = self.retrivalDatabase.retrieveExample(userInput, topK=2, exampleType="Model")[0]
        exampleStr = ""
        for example in retrievedExample:
            exampleStr += "\n\n" + example

        humanMessage = HumanMessage(template.format(input=userInput, example=exampleStr))
        messageList = [humanMessage]

        tools = [readEnvironment]
        llmWithTools = self.llm.bind_tools(tools)
        llmMessage = llmWithTools.invoke(messageList)
        messageList.append(llmMessage)

        for toolcall in llmMessage.tool_calls:
            selectedTool = {"readenvironment": readEnvironment}[toolcall["name"].lower()]
            toolOutput = selectedTool.invoke(toolcall["args"])
            messageList.append(ToolMessage(toolOutput, tool_call_id=toolcall["id"]))

        contextText = "\n-------------\n".join([message.content for message in messageList])

        # langchain inference
        modelProducerChain = llmWithTools | self.outputParser
        modelReturn = modelProducerChain.invoke(messageList)
        responseTime = getCurrentTimeStamp()

        # ["conversationID", "promptID",
        #  "requestText", "contextText", "requestTime", "typeMessage",
        #  "responseText", "responseTime", "workflow", "executionLog"]
        interactionRow = [self.conversationID, generalChatPromptRow["ID"],
                          userInput, contextText, requestTime, "return",
                          modelReturn, responseTime, "withModel", ""]
        self.dataloader.insertInteraction(interactionRow, self.conversationID)

        return modelReturn

    def codeProducer(self, userInput: str) -> tuple[str, str]:
        requestTime = getCurrentTimeStamp()
        codeProducerPromptRow = self.dataloader.fetchPrompt(self.llmID, promptType="codeProducer")
        template = codeProducerPromptRow["template"]

        # get documentation
        retrievedDoc = self.retrivalDatabase.retrieveDocument(userInput)[0]
        docStr = ""
        for doc in retrievedDoc:
            docStr += "\n\n" + doc

        # get few-shot examples
        retrievedExample = self.retrivalDatabase.retrieveExample(userInput, topK=2, exampleType="Script")[0]
        exampleStr = ""
        """
        for example in retrievedExample:
            exampleStr += "\n\n" + example
        """
        humanMessage = HumanMessage(template.format(input=userInput, doc=docStr, example=exampleStr))
        messageList = [humanMessage]

        tools = [readEnvironment]
        toolDict = {"readenvironment": readEnvironment}
        llmWithTools = self.llm.bind_tools(tools)
        llmMessage = llmWithTools.invoke(messageList)
        messageList.append(llmMessage)

        for toolcall in llmMessage.tool_calls:
            selectedTool = toolDict[toolcall["name"].lower()]
            toolOutput = selectedTool.invoke(toolcall["args"])
            messageList.append(ToolMessage(toolOutput, tool_call_id=toolcall["id"]))

        contextText = "-------------\n".join([message.content for message in messageList])
        # langchain inference
        codeProducerChain = llmWithTools | self.outputParser
        codeReturn = codeProducerChain.invoke(messageList)
        responseTime = getCurrentTimeStamp()

        # ["conversationID", "promptID",
        #  "requestText", "contextText", "requestTime", "typeMessage",
        #  "responseText", "responseTime", "workflow", "executionLog"]
        interactionRow = [self.conversationID, codeProducerPromptRow["ID"],
                          userInput, contextText, requestTime, "return",
                          codeReturn, responseTime, "withCode", ""]
        interactionID = self.dataloader.insertInteraction(interactionRow, self.conversationID)
        self.latestInteractionID = interactionID

        return codeReturn, interactionID

    def toolBoxProducer(self, userInput: str) -> tuple[str, str]:
        requestTime = getCurrentTimeStamp()
        codeProducerPromptRow = self.dataloader.fetchPrompt(self.llmID, promptType="codeProducer")
        template = """
                 Instructions:
                 
                 This LLM is a QGIS plugin named IntelliGEO.
                 This LLM is a Python expert with a deep understanding of PyQGIS. This LLM is specialized in generating PyQGIS code scripts based on user descriptions.
                 The user will provide specific requirements for a GIS task they need to accomplish, and goal of this LLM is to generate PyQGIS code for a custom algorithm to be added to the QGIS Processing Toolbox. Ensure to generate code for QGIS toolbox instead of scripts.
                 Generate the code base on these documents and relevant examples: {doc}{example}
                 
                 Inputs:
                 
                 {input}
                 
                 Outputs:
                 
                 PyQGIS script:
                 ```python
                 # Insert your generated python code here base on the user description.
                 ```
                 """

        # get documentation
        retrievedDoc = self.retrivalDatabase.retrieveDocument(userInput, topK=2)[0]
        docStr = ""
        for doc in retrievedDoc:
            docStr += "\n\n" + doc

        # get few-shot examples
        retrievedExample = self.retrivalDatabase.retrieveExample(userInput, topK=2, exampleType="Script")[0]
        exampleStr = ""

        for example in retrievedExample:
            exampleStr += "\n\n" + example

        humanMessage = HumanMessage(template.format(input=userInput, doc=docStr, example=exampleStr))
        messageList = [humanMessage]

        show_variable_popup(messageList)

        tools = [readEnvironment]
        toolDict = {"readenvironment": readEnvironment}
        llmWithTools = self.llm.bind_tools(tools)
        llmMessage = llmWithTools.invoke(messageList)
        messageList.append(llmMessage)

        for toolcall in llmMessage.tool_calls:
            selectedTool = toolDict[toolcall["name"].lower()]
            toolOutput = selectedTool.invoke(toolcall["args"])
            messageList.append(ToolMessage(toolOutput, tool_call_id=toolcall["id"]))

        contextText = "-------------".join([message.content for message in messageList])

        # langchain inference
        codeProducerChain = llmWithTools | self.outputParser
        codeReturn = codeProducerChain.invoke(messageList)
        responseTime = getCurrentTimeStamp()

        # ["conversationID", "promptID",
        #  "requestText", "contextText", "requestTime", "typeMessage",
        #  "responseText", "responseTime", "workflow", "executionLog"]
        interactionRow = [self.conversationID, codeProducerPromptRow["ID"],
                          userInput, contextText, requestTime, "return",
                          codeReturn, responseTime, "withCode", ""]
        interactionID = self.dataloader.insertInteraction(interactionRow, self.conversationID)
        self.latestInteractionID = interactionID

        return codeReturn, interactionID

    def confirmChain(self):
        return RunnableLambda(lambda x: "Are you sure?")

    # def response(self, userInput, responseType):
    #     response, workflow = self.reactionRouter(userInput, responseType)
    #
    #     return response, workflow

    def asyncResponse(self, userInput, responseType):
        worker = ResponseWorker(self, userInput, responseType)
        # Connect the signal to handle the response
        worker.signals.finished.connect(
            lambda response, workflow: self.handleResponse(userInput, responseType, response, workflow)
        )
        worker.signals.error.connect(self.errorHandling)
        self.threadpool.start(worker)  # Start the worker in the thread pool

    def handleResponse(self, userInput, responseType, response, workflow):
        # Handle the response from the worker
        self.responseReady.emit(userInput, responseType, response, workflow)

    def response(self, userInput, responseType):
        """
        Run the response method asynchronously.
        """
        # Run reactionRouter asynchronously to avoid blocking
        response, workflow = self.reactionRouter(userInput, responseType)
        return response, workflow

    def asyncReflect(self, logMessage, executedCode, responseType: str = "code"):
        worker = ReflectWorker(self, logMessage, executedCode, responseType)
        worker.signals.finished.connect(
            lambda response, workflow: self.handleReflect(logMessage,
                                                          responseType,
                                                          response,
                                                          workflow)
        )
        worker.signals.error.connect(self.errorHandling)
        self.threadpool.start(worker)

    def handleReflect(self, logMessage, responseType, response, workflow):
        # Handle the response from the worker
        self.reflectionReady.emit(logMessage,
                                  responseType,
                                  response,
                                  workflow)

    def reflect(self, logMessage, executedCode, responseType: str = "code"):
        try:
            requestTime = getCurrentTimeStamp()
            codeProducerPromptRow = self.dataloader.fetchPrompt(self.llmID, promptType="codeProducer")

            latestRow = self.dataloader.selectLatestInteraction(self.conversationID, self.latestInteractionID)
            latestInteraction = pack(latestRow, "interaction")

            userInput = latestInteraction["requestText"]  # get the user Input
            AIResponse = latestInteraction["responseText"]  # get the AI response

            prompt = f"""
                     Context:
                     
                     This LLM is a QGIS plugin named IntelliGEO. This LLM is a Python expert with a deep understanding of PyQGIS. This LLM is specialized in generating PyQGIS code scripts based on user descriptions.
                     Previously, you were requested to generate PyQGIS code, and the generate code produced an error when executed. This error might come from the generated code or user editions. Below you will find relevant data.
                     
                     Data:
                     Original user request: {userInput}
                     Generated code: {AIResponse}
                     Executed code: {executedCode}
                     Error message: {logMessage}
                     
                     Task: Use the following questions to generate your response:
                     1. Does the generated code align with the orignal request?
                     2. What are the differenes between the generated code and the executed code?
                     3. Are the changes needed to set parameters in the code?
                     4. Does the error message relates to the differences between generated code and executed code?
                     5. Does the error message suggests there is an import error?
                     
                     As output produce a brief description of a solution, but do not include answers to the questions, and only if needed generate an edited version of the code to implement the proposed solution.
                     """
            # userInput = latestInteraction["requestText"]  # get the user Input
            # AIResponse = latestInteraction["responseText"]  # get the AI response
            # errorMessage = f"The code you provide returns the following error: {logMessage}, please fix it."
            #
            # messageList = [HumanMessage(content=userInput),
            #                AIMessage(content=AIResponse),
            #                HumanMessage(content=errorMessage)]
            #
            # contextText = "-------------".join([message.content for message in messageList])

            codeDebuggerChain = self.llm | self.outputParser
            codeReturn = codeDebuggerChain.invoke(prompt)
            responseTime = getCurrentTimeStamp()
            interactionRow = [self.conversationID, codeProducerPromptRow["ID"],
                              userInput, prompt, requestTime, "return",
                              codeReturn, responseTime, "withModel", ""]

            interactionID = self.dataloader.insertInteraction(interactionRow, self.conversationID)
            self.latestInteractionID = interactionID

            workflow = "withCode"
            return codeReturn, workflow
        
        except Exception as e:
            # Define error file path
            documentsPath = os.path.join(os.path.expanduser("~"), "Documents", "QGIS_IntelliGeo")

            os.makedirs(documentsPath, exist_ok=True)  # Ensure the directory exists
            errorFilePath = os.path.join(documentsPath, "error_log.txt")  # Define the error file path

            # Write error message to file
            with open(errorFilePath, "w") as error_file:
                error_message = f"An error occurred at reflection:\n{str(e)}"
                error_file.write(error_message)

    def modelRefine(self, userInput: str):
        return ""

    def codeRefine(self, userInput: str) -> tuple[str, str]:
        requestTime = getCurrentTimeStamp()
        # codeRefinerPromptRow = self.dataloader.fetchPrompt(self.llmID, promptType="codeRefiner")
        # template = codeRefinerPromptRow["template"]

        template = """
        This LLM is a QGIS plugin named IntelliGEO.

        This LLM, IntelliGEO, is a QGIS plugin specializing in PyQGIS. It generates or refines PyQGIS scripts based on user requirements or feedback. Users can request new scripts or modifications to existing ones, and the LLM ensures the code is efficient, accurate, and well-documented with comments explaining each section. When updating code, it incorporates user feedback while preserving functionality and structure.
        
        Generate the code based on these documents and relevant examples: {doc}{example}
        
        Context:
        
        The LLM do not have information about the opened QGIS project, make sure to use the readEnvironment tool to get the information of the current opened project.
        
        Previous Conversation
        
        User's Request:
        {previousRequest}
        
        LLM's Answer:
        {previousResponse}
        
        New Input:
        {input}

        Outputs:
        
        PyQGIS script:
        ```python
        # Insert your generated python code here base on the user description.
        ```
        """

        # get documentation
        retrievedDoc = self.retrivalDatabase.retrieveDocument(userInput, topK=1)[0]
        docStr = ""
        for doc in retrievedDoc:
            docStr += "\n\n" + doc

        # get few-shot examples
        retrievedExample = self.retrivalDatabase.retrieveExample(userInput, topK=2, exampleType="Script")[0]
        exampleStr = ""
        """
        for example in retrievedExample:
            exampleStr += "\n\n" + example
        """
        # get last interaction
        latestInteractionRow = self.dataloader.selectLatestInteraction(self.conversationID,
                                                                       self.latestInteractionID)
        latestInteraction = pack(latestInteractionRow, "interaction")

        # get the AI response
        previousRequest, AIResponse = latestInteraction["requestText"], latestInteraction["responseText"]
        show_variable_popup(previousRequest)
        humanMessage = HumanMessage(template.format(input=userInput, previousRequest=previousRequest,
                                                    previousResponse=AIResponse, doc=docStr, example=exampleStr))
        show_variable_popup(humanMessage)
        messageList = [humanMessage]

        tools = [readEnvironment]
        toolDict = {"readenvironment": readEnvironment}
        llmWithTools = self.llm.bind_tools(tools)
        llmMessage = llmWithTools.invoke(messageList)
        messageList.append(llmMessage)

        for toolcall in llmMessage.tool_calls:
            selectedTool = toolDict[toolcall["name"].lower()]
            toolOutput = selectedTool.invoke(toolcall["args"])
            messageList.append(ToolMessage(toolOutput, tool_call_id=toolcall["id"]))

        contextText = "-------------\n".join([message.content for message in messageList])
        # langchain inference
        codeProducerChain = llmWithTools | self.outputParser
        codeReturn = codeProducerChain.invoke(messageList)
        responseTime = getCurrentTimeStamp()

        # ["conversationID", "promptID",
        #  "requestText", "contextText", "requestTime", "typeMessage",
        #  "responseText", "responseTime", "workflow", "executionLog"]
        interactionRow = [self.conversationID, "OpenAI::gpt-4::0::codeProducer",
                          userInput, contextText, requestTime, "return",
                          codeReturn, responseTime, "withCode", ""]
        interactionID = self.dataloader.insertInteraction(interactionRow, self.conversationID)
        self.latestInteractionID = interactionID

        return codeReturn, interactionID

    def errorHandling(self, error):
        self.errorSignal.emit(error)

