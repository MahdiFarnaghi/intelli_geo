import os

from langchain_cohere import ChatCohere
from langchain_openai import OpenAIEmbeddings
from langchain_cohere.embeddings import CohereEmbeddings
from langchain_openai import ChatOpenAI

from .utils import getCurrentTimeStamp, getVersion, pack
from .processor import Processor
from .workflowManager import WorkflowManager


class Conversation:
    def __init__(self, ID: str, dataloader, retrivalDatabase):
        """
        >>> metaInfo.keys()
        ... ["ID", "llmID", "title", "description", "created", "modified", "messageCount", "workflowCount", "userID"]
        """
        metaInfo = dataloader.selectConversationInfo(ID)
        self.metaInfo = metaInfo

        self.dataloader = dataloader
        self.LLMFinished = True
        # self.messageCount, self.workflowCount = 0, 0

        # TODO: model chooser logic
        self.llmProvider, self.llmName = self.dataloader.getLLMInfo(self.llmID)
        # ONWORKING: model chooser logic

        self.Processor = Processor(self.llmID, self.ID, retrivalDatabase, self.dataloader)
        self.workflowManager = WorkflowManager()

    def __getattr__(self, name):
        # available variables: "ID", "llmID", "title", "description", "created", "modified", "messageCount",
        # "workflowCount", "userID"
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
            modelPath = self.workflowManager.saveWorkflow(response, workflow, self.title, self.workflowCount)
            self.workflowCount += 1
        else:
            modelPath = None

        self.LLMFinished = True
        self.messageCount += 1
        self.modified = getCurrentTimeStamp()

        return response, workflow, modelPath

    def fetch(self) -> str:
        """
        Get entire conversation history from local database
        """
        log = ""
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
                log += f"LLM: {messageDict['responseText']} \t {messageDict['responseTime']}\n\n"

        return log

    def fetchTail(self):
        logTail = ""

    def getMetadata(self):
        metadata = (f"Created: {self.created} | LLM: {self.llmName} | Messages: {str(self.messageCount)} | "
                    f"Workflow: {str(self.workflowCount)} ")

        return metadata

    def clear(self):
        self.dataloader.cleartable(self.ID)
        self.messageCount = 0
        self.workflowCount = 0

    def delete(self):
        self.dataloader.deleteConversation(self.ID)
