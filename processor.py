# Temporary imports
import json
import os

from PyQt5.QtCore import QResource

from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage, ToolMessage

from .utils import show_variable_popup
from .tools import readEnvironment
from .environment import QgisEnvironment


class Processor():
    def __init__(self, llm, llmProvider):
        self.llm = llm
        self.llmProvider = llmProvider
        self.outputParser = StrOutputParser()
        currentFilePath = os.path.abspath(__file__)
        currentFolder = os.path.dirname(currentFilePath)
        promptPath = os.path.join(currentFolder, 'resources', 'prompt.json')
        self.promptPath = (promptPath)
        self.promptDict = self.loadPrompt()

    def loadPrompt(self):
        """
        Load pre-defined prompt
        """
        with open(self.promptPath, 'r') as file:
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

    def reactionRouter(self, userInput):
        decision = self.classifier(userInput)
        show_variable_popup(decision)

        if "no" in decision.lower():
            generalChatResponse = self.generalChat(userInput)

            return generalChatResponse

        elif "yes" in decision.lower():
            modelProducerResponse = self.modelProducer(userInput)

            return modelProducerResponse

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
        humanMessage = HumanMessage(template.format(input=userInput))
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

    def response(self, userInput):
        response = self.reactionRouter(userInput)

        return response
