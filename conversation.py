import os

from qgis.PyQt.QtCore import pyqtSignal, QObject

from langchain_cohere import ChatCohere
from langchain_openai import OpenAIEmbeddings
from langchain_cohere.embeddings import CohereEmbeddings
from langchain_openai import ChatOpenAI

from .utils import getCurrentTimeStamp, getVersion, pack, show_variable_popup
from .processor import Processor
from .workflowManager import WorkflowManager


class Conversation(QObject):
    llmResponse = pyqtSignal(str, str, str)
    llmReflection = pyqtSignal(str, str, str)
    llmInterrupted = pyqtSignal(str)

    def __init__(self, ID: str, dataloader, retrivalDatabase):
        """
        >>> metaInfo.keys()
        ... ["ID", "llmID", "title", "description", "created", "modified", "messageCount", "workflowCount", "userID"]
        """
        super().__init__()  # Call the QObject constructor

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

        self.modified = getCurrentTimeStamp()

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
            # Await the asynchronous updateLLMResponse method
            return self.updateLLMResponse(message, responseType)
        else:
            pass

    def updateLLMResponse(self, message, responseType):
        self.LLMFinished = False
        self.Processor.responseReady.connect(self.onResponseReady)
        self.Processor.errorSignal.connect(self.onResponseInterrupted)
        self.Processor.asyncResponse(message, responseType)

    def onResponseReady(self, message, responseType, response, workflow):
        self.Processor.responseReady.disconnect(self.onResponseReady)

        if workflow != "empty":
            modelPath = self.workflowManager.saveWorkflow(response, workflow, self.title, self.workflowCount)
            self.workflowCount += 1
        else:
            modelPath = None

        self.LLMFinished = True
        self.messageCount += 1
        self.modified = getCurrentTimeStamp()
        self.llmResponse.emit(response, workflow, modelPath)
        # return response, workflow, modelPath

    def onResponseInterrupted(self, error):
        self.Processor.responseReady.disconnect(self.onResponseReady)
        self.Processor.errorSignal.disconnect(self.onResponseInterrupted)
        self.llmInterrupted.emit(error)
        self.LLMFinished = True

    def fetch(self) -> list[tuple]:
        """
        Get entire conversation history from local database
        """
        log = ""
        interactionHistory = self.dataloader.selectInteraction(self.ID)

        return interactionHistory

    def fetchTail(self):
        latestInteraction = self.dataloader.selectLatestInteraction(self.ID, self.Processor.latestInteractionID)
        messageDict = pack(latestInteraction, "interaction")

        return messageDict

    def getMetadata(self):
        metadata = (f"Created: {self.created} | LLM: {self.llmName} | Messages: {str(self.messageCount)} | "
                    f"Workflow: {str(self.workflowCount)} ")

        return metadata

    def clear(self):
        """
        remove every record related to an ID in the dataloader
        """
        self.dataloader.cleartable(self.ID)
        self.messageCount = 0
        self.workflowCount = 0

    def delete(self):
        self.dataloader.deleteConversation(self.ID)

    def updateReflection(self,
                         logMessage: str,
                         executedCode: str,
                         responseType: str = "code") -> None:
        """
        When reflection loop is triggered, go to processor for a bug-fix
        """
        if self.LLMFinished:
            self.messageCount += 1
            self.LLMFinished = False

            self.Processor.reflectionReady.connect(self.onReflectionReady)
            self.Processor.asyncReflect(logMessage, executedCode, responseType)

    def onReflectionReady(self, logMessage, responseType, response, workflow):
        show_variable_popup("Conversation.onReflectionReady")
        self.LLMFinished = True
        if workflow != "empty":
            modelPath = self.workflowManager.saveWorkflow(response, workflow, self.title, self.workflowCount)
            self.workflowCount += 1
        else:
            modelPath = None

        self.LLMFinished = True
        self.messageCount += 1
        self.modified = getCurrentTimeStamp()

        self.llmReflection.emit(response, workflow, modelPath)
