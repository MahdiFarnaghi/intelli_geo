import os

from langchain_cohere import ChatCohere
from langchain_openai import OpenAIEmbeddings
from langchain_cohere.embeddings import CohereEmbeddings
from langchain_openai import ChatOpenAI

from .utils import getCurrentTimeStamp, getVersion, show_variable_popup, pack
from .processor import Processor
from .workflowManager import WorkflowManager


class Conversation:
    def __init__(self, ID, dataloader, retrivalDatabase):
        """
        >>> metaInfo.keys()
        ... ["ID", "llmID", "title", "description", "created", "modified", "userID"]
        """
        metaInfo = dataloader.selectConversationInfo(ID)
        self.metaInfo = metaInfo

        self.dataloader = dataloader
        self.LLMFinished = True
        # self.messageCount, self.modelCount = 0, 0
        # TODO: model chooser logic
        self.llmProvider, self.llmName = self.dataloader.getLLMInfo(self.llmID)
        # ONWORKING: model chooser logic
        if self.llmProvider == "OpenAI":
            apiKey = os.getenv("OPENAI_API_KEY")
            self.llm = ChatOpenAI(model=self.llmName, openai_api_key=apiKey, temperature=0)
            self.embedding = OpenAIEmbeddings(openai_api_key=apiKey)
        elif self.llmProvider == "Cohere":
            apiKey = os.getenv("COHERE_API_KEY")
            self.llm = ChatCohere(model=self.llmName, cohere_api_key=apiKey, temperature=0)
            self.embedding = CohereEmbeddings(cohere_api_key=apiKey)
        else:
            apiKey = os.getenv("COHERE_API_KEY")
            self.llm = ChatCohere(model="command-r-plus", cohere_api_key=apiKey, temperature=0)
            self.embedding = CohereEmbeddings(cohere_api_key=apiKey)

        self.Processor = Processor(self.llm, self.llmID, self.ID, retrivalDatabase, self.dataloader)
        self.workflowManager = WorkflowManager()

    def __getattr__(self, name):
        # available variables: "ID", "llmID", "title", "description", "created", "modified", "userID"
        if name != 'metaInfo' and name in self.metaInfo:
            return self.metaInfo[name]
        else:
            super().__getattr__(name)

    def __setattr__(self, name, value):
        if name == 'dataloader':
            super().__setattr__(name, value)
        elif name != 'metaInfo' and name in self.metaInfo:
            self.metaInfo[name] = value
        else:
            super().__setattr__(name, value)

    def updateUserPrompt(self, message, responseType):
        # TODO: make a queue for LLM reaction & user input
        if self.LLMFinished:
            self.messageCount += 1
            return self.updateLLMResponse(message, responseType)
        else:
            pass

    def updateLLMResponse(self, message, responseType):
        self.LLMFinished = False

        response, workflow = self.Processor.response(message, responseType)

        if workflow != "empty":
            modelPath = self.workflowManager.saveWorkflow(response, workflow, self.title, self.modelCount)
            self.modelCount += 1

        else:
            modelPath = None
            # self.dataloader.insertInteraction(self.ID, sender="LLM", message=response)

        self.LLMFinished = True
        self.messageCount += 1
        self.modified = getCurrentTimeStamp()

        return response, workflow, modelPath


    def fetch(self):
        log = ''
        interactionHistory = self.dataloader.selectInteraction(self.ID)
        # TODO: fetch loops through the databse and takes everything, for larger database can be time wasting
        # TODO: should we have an alternative method 'dispaly' that simply take the current shown content and
        # TODO: attach responses to the tail?

        log += f"Displaying {str(len(interactionHistory))} messages.\n"
        for message in interactionHistory:
            messageDict = pack(message, "interaction")
            if messageDict["typeMessage"] == "input":
                log += f"User: {messageDict['requestText']} \t {messageDict['requestTime']}\n\n"
            elif messageDict["typeMessage"] == "return":
                log += f"User: {messageDict['responseText']} \t {messageDict['responseTime']}\n\n"

        return log

    def fetchTail(self):
        logTail = ''

    def getMetadata(self):
        metadata = (f"Created: {self.created} | LLM: {self.llmName} | Messages: {str(self.messageCount)} | "
                    f"Model: {str(self.modelCount)} ")

        return metadata

    def clear(self):
        self.dataloader.cleartable(self.ID)
        self.messageCount = 0
        self.modelCount = 0

    def delete(self):
        self.dataloader.deleteConversation(self.ID)
