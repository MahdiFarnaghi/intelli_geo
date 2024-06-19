import os

from langchain_cohere import ChatCohere
from langchain_openai import OpenAIEmbeddings
from langchain_cohere.embeddings import CohereEmbeddings
from langchain_openai import ChatOpenAI

from .utils import getCurrentTimeStamp, getVersion, show_variable_popup
from .processor import Processor
from .modelManager import ModelManager


class Conversation:
    def __init__(self, ID, dataloader, llmProvider=None):
        metaInfo = dataloader.selectMetaInfo(ID)[0]
        self.metaInfo = metaInfo

        self.dataloader = dataloader
        self.LLMFinished = True
        self.llmProvider = llmProvider
        if self.llmProvider is 'openai':
            apiKey = os.getenv("OPENAI_API_KEY")
            self.LLM = ChatOpenAI(openai_api_key=apiKey, temperature=0)
            self.embedding = OpenAIEmbeddings(openai_api_key=apiKey)
        else:
            apiKey = os.getenv("COHERE_API_KEY")
            self.LLM = ChatCohere(cohere_api_key=apiKey, temperature=0)
            self.embedding = CohereEmbeddings(cohere_api_key=apiKey)

        self.Processor = Processor(self.LLM, 'Cohere', self.embedding)
        self.modelManager = ModelManager()

    def __getattr__(self, name):
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
            self.dataloader.insertData(self.ID, sender="user", message=message)
            self.messageCount += 1
            return self.updateLLMResponse(message, responseType)
        else:
            pass

    def updateLLMResponse(self, message, responseType):
        self.LLMFinished = False

        response, withModel, withCode = self.Processor.response(message, responseType)
        if withModel:
            modelPath = self.modelManager.saveModel(response, self.title, self.modelCount)

            self.dataloader.insertData(self.ID, sender="LLM", message=response, model=modelPath)
            # TODO: 'withcode' tag to be processed
        else:
            modelPath = None
            self.dataloader.insertData(self.ID, sender="LLM", message=response)

        self.LLMFinished = True
        self.messageCount += 1
        self.lastEdit = getCurrentTimeStamp()

        return response, withModel, withCode, modelPath


    def fetch(self):
        log = ''
        history = self.dataloader.selectData(self.ID)
        # TODO: fetch loops through the databse and takes everything, for larger database can be time wasting
        # TODO: should we have an alternative method 'dispaly' that simply take the current shown content and
        # TODO: attach responses to the tail?
        log += 'Displaying ' + str(len(history)) + ' messages.\n'
        for message in history:
            log += message[0] + ': ' + message[2] + '\t' + message[1] + '\n\n'

        return log

    def fetchTail(self):
        logTail = ''

    def getMetadata(self):
        metadata = ''
        metadata += 'Created: ' + self.created + ' | '
        metadata += 'LLM: ' + 'Cohere' + ' | '
        metadata += 'Messages: ' + str(self.messageCount) + ' | '
        metadata += 'Models: ' + '? '

        return metadata

    def clear(self):
        self.dataloader.cleartable(self.ID)
        self.messageCount = 0

    def delete(self):
        self.dataloader.dropTable(self.ID)
