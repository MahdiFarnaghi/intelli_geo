# Temporary imports
import json
import os

from PyQt5.QtCore import QResource

from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_community.vectorstores import FAISS

from .utils import show_variable_popup, getVersion
from .tools import readEnvironment
from .environment import QgisEnvironment


class Processor:
    def __init__(self, llm, llmProvider, retrievalVectorbase):
        self.llm = llm
        self.llmProvider = llmProvider
        self.retrivalDatabase = retrievalVectorbase
        self.outputParser = StrOutputParser()
        currentFilePath = os.path.abspath(__file__)
        currentFolder = os.path.dirname(currentFilePath)
        promptPath = os.path.join(currentFolder, 'resources', 'prompt_v0.1.json')
        self.promptDict = self.loadPrompt(promptPath)

        self.version = getVersion()

    def loadPrompt(self, promptPath):
        """
        Load pre-defined prompt
        """
        with open(promptPath, 'r') as file:
            promptDict = json.load(file)
        # resource = QResource(self.promptPath)
        # data = resource.data()
        # if not resource.isValid():
        #     show_variable_popup(resource)
        # show_variable_popup(data)
        #
        # jsonStr = data.data().decode('utf-8')
        #
        # promptDict = json.loads(jsonStr)

        return promptDict

    def promptMaker(self, promptDict):
        template = ''
        for key, value in promptDict.items():
            template += key + "\n\n" + value + "\n\n"

        promptTemplate = ChatPromptTemplate.from_template(template)

        return promptTemplate

    def classifier(self, userInput):
        classifierPrompt = self.promptMaker(self.promptDict["classifier"]["default"])

        classifierChain = classifierPrompt | self.llm | self.outputParser
        decision = classifierChain.invoke(userInput)

        return decision

    def reactionRouter(self, userInput, responseType):
        decision = self.classifier(userInput)
        show_variable_popup(decision)

        if "no" in decision.lower():
            generalChatResponse = self.generalChat(userInput)

            return generalChatResponse, False, False

        elif "yes" in decision.lower():
            if responseType == "Visual mode":
                modelProducerResponse = self.modelProducer(userInput)
                return modelProducerResponse, True, False
            else:
                codeProducerResponse = self.codeProducer(userInput)
                return codeProducerResponse, False, True


        else:
            confirmChain = self.confirmChain()

    def generalChat(self, userInput):
        template = self.promptMaker(self.promptDict["generalChat"]["default"])
        humanMessage = HumanMessage(template.format(input=userInput))
        messages = [humanMessage]

        tools = [readEnvironment]
        llmWithTools = self.llm.bind_tools(tools)
        llmMessage = llmWithTools.invoke(messages)
        messages.append(llmMessage)

        if len(llmMessage.tool_calls) == 0:
            return self.outputParser.invoke(llmMessage)

        for toolcall in llmMessage.tool_calls:
            selectedTool = {"readenvironment": readEnvironment}[toolcall["name"].lower()]
            toolOutput = selectedTool.invoke(toolcall["args"])
            messages.append(ToolMessage(toolOutput, tool_call_id=toolcall["id"]))

        chatChain = llmWithTools | self.outputParser
        return chatChain.invoke(messages)

    def modelProducer(self, userInput):
        template = self.promptMaker(self.promptDict["modelProducer"]["default"])

        # get example
        retrievedExample = self.retrivalDatabase.retrieveExample(userInput, exampleType="Model")[0]
        exampleStr = ""
        for example in retrievedExample:
            exampleStr += "\n\n" + example

        show_variable_popup(exampleStr)

        humanMessage = HumanMessage(template.format(input=userInput, example=exampleStr))
        messages = [humanMessage]

        tools = [readEnvironment]
        llmWithTools = self.llm.bind_tools(tools)
        llmMessage = llmWithTools.invoke(messages)
        messages.append(llmMessage)

        for toolcall in llmMessage.tool_calls:
            selectedTool = {"readenvironment": readEnvironment}[toolcall["name"].lower()]
            toolOutput = selectedTool.invoke(toolcall["args"])
            messages.append(ToolMessage(toolOutput, tool_call_id=toolcall["id"]))

        modelProducerChain = llmWithTools | self.outputParser
        return modelProducerChain.invoke(messages)

    def codeProducer(self, userInput):
        template = self.promptMaker(self.promptDict["codeProducer"]["default"])

        # get documentation
        retrievedDoc = self.retrivalDatabase.retrieveDocument(userInput)[0]
        docStr = ""
        for doc in retrievedDoc:
            docStr += "\n\n" + doc

        show_variable_popup(docStr)

        # get example
        retrievedExample = self.retrivalDatabase.retrieveExample(userInput, exampleType="Script")[0]
        exampleStr = ""
        for example in retrievedExample:
            exampleStr += "\n\n" + example

        show_variable_popup(exampleStr)

        humanMessage = HumanMessage(template.format(input=userInput, doc=docStr, example=exampleStr))
        messages = [humanMessage]

        tools = [readEnvironment]
        llmWithTools = self.llm.bind_tools(tools)
        llmMessage = llmWithTools.invoke(messages)
        messages.append(llmMessage)

        for toolcall in llmMessage.tool_calls:
            selectedTool = {"readenvironment": readEnvironment}[toolcall["name"].lower()]
            toolOutput = selectedTool.invoke(toolcall["args"])
            messages.append(ToolMessage(toolOutput, tool_call_id=toolcall["id"]))

        modelProducerChain = llmWithTools | self.outputParser
        return modelProducerChain.invoke(messages)

    def confirmChain(self):
        return RunnableLambda(lambda x: "Are you sure?")

    def response(self, userInput, responseType):
        response, withModel, withCode = self.reactionRouter(userInput, responseType)

        return response, withModel, withCode
