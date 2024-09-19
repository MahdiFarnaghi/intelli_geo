# Temporary imports
import json
import os

from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_community.vectorstores import FAISS
from langchain_cohere import ChatCohere
from langchain_openai import ChatOpenAI

from .utils import show_variable_popup, getVersion, getCurrentTimeStamp
from .tools import readEnvironment
from .environment import QgisEnvironment


class Processor:
    def __init__(self, llmID, conversationID, retrievalVectorbase, dataloader):
        self.llmID = llmID
        self.dataloader = dataloader
        self.llmProvider, self.llmName = llmID.split("::")
        _, apiKey = dataloader.fetchAPIKey(self.llmID)
        if self.llmProvider == "OpenAI":
            self.llm = ChatOpenAI(model=self.llmName, openai_api_key=apiKey, temperature=0)
        elif self.llmProvider == "Cohere":
            self.llm = ChatCohere(model=self.llmName, cohere_api_key=apiKey, temperature=0)

        self.conversationID = conversationID
        self.retrivalDatabase = retrievalVectorbase
        self.outputParser = StrOutputParser()
        self.version = getVersion()

    # def loadPrompt(self, promptPath):
    #     """
    #     Load pre-defined prompt
    #     """
    #     with open(promptPath, 'r') as file:
    #         promptDict = json.load(file)
    #     # resource = QResource(self.promptPath)
    #     # data = resource.data()
    #     # if not resource.isValid():
    #     #     show_variable_popup(resource)
    #     # show_variable_popup(data)
    #     #
    #     # jsonStr = data.data().decode('utf-8')
    #     #
    #     # promptDict = json.loads(jsonStr)
    #
    #     return promptDict

    # def _promptMaker(self, promptDict):
    #     template = ''
    #     for key, value in promptDict.items():
    #         template += key + "\n\n" + value + "\n\n"
    #
    #     promptTemplate = ChatPromptTemplate.from_template(template)
    #
    #     return promptTemplate

    def classifier(self, userInput: str) -> str:
        """
        Base on the given `userInput`, decide if it is asking about producing workflow (model, code).
        Return "yes" or "no".
        """
        requestTime = getCurrentTimeStamp()
        classifierPromptRow = self.dataloader.fetchPrompt(self.llmID, promptType="classifier")
        classifierPrompt = ChatPromptTemplate.from_template(classifierPromptRow["template"])

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

        if "no" in decision.lower():
            generalChatResponse = self.generalChat(userInput)

            return generalChatResponse, "empty"

        elif "yes" in decision.lower():
            if responseType == "Visual mode":
                modelProducerResponse = self.modelProducer(userInput)
                return modelProducerResponse, "withModel"
            else:
                codeProducerResponse = self.codeProducer(userInput)
                return codeProducerResponse, "withCode"

        else:
            confirmChain = self.confirmChain()

    def generalChat(self, userInput: str) -> str:
        requestTime = getCurrentTimeStamp()

        generalChatPromptRow = self.dataloader.fetchPrompt(self.llmID, promptType="generalChat")
        template = generalChatPromptRow["template"]
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

        show_variable_popup(exampleStr)

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

    def codeProducer(self, userInput: str) -> str:
        requestTime = getCurrentTimeStamp()
        generalChatPromptRow = self.dataloader.fetchPrompt(self.llmID, promptType="codeProducer")
        template = generalChatPromptRow["template"]

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

        contextText = "-------------".join([message.content for message in messageList])

        # langchain inference
        codeProducerChain = llmWithTools | self.outputParser
        codeReturn = codeProducerChain.invoke(messageList)
        responseTime = getCurrentTimeStamp()

        # ["conversationID", "promptID",
        #  "requestText", "contextText", "requestTime", "typeMessage",
        #  "responseText", "responseTime", "workflow", "executionLog"]
        interactionRow = [self.conversationID, generalChatPromptRow["ID"],
                          userInput, contextText, requestTime, "return",
                          codeReturn, responseTime, "withModel", ""]
        self.dataloader.insertInteraction(interactionRow, self.conversationID)

        return codeReturn

    def confirmChain(self):
        return RunnableLambda(lambda x: "Are you sure?")

    def response(self, userInput, responseType):
        response, workflow = self.reactionRouter(userInput, responseType)

        return response, workflow
