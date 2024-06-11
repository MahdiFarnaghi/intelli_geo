from langchain_cohere import ChatCohere
from .utils import getCurrentTimeStamp
from .processor import Processor

class Conversation:
    def __init__(self, ID, dataloader, LLMName=None):
        metaInfo = dataloader.selectMetaInfo(ID)[0]
        self.metaInfo = metaInfo

        self.dataloader = dataloader
        self.LLMFinished = True
        if self.LLMName is "Cohere":
            self.LLM = ChatCohere(cohere_api_key="nLWE6IlAgzdxuNELOSZq1WYFl5kuvUL3CIVqtZkl")
        else:
            self.LLM = ChatCohere(cohere_api_key="nLWE6IlAgzdxuNELOSZq1WYFl5kuvUL3CIVqtZkl")

        self.Processor = Processor(self.LLM, 'Cohere')


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

    def updateUserPrompt(self, message):
        if self.LLMFinished:
            self.dataloader.insertData(self.ID, sender="user", message=message)
            self.updateLLMResponse(message)
            self.messageCount += 1
        else:
            pass

    def updateLLMResponse(self, message):
        self.LLMFinished = False

        response = self.Processor.response(message)
        self.dataloader.insertData(self.ID, sender="LLM", message=response)
        self.LLMFinished = True
        self.messageCount += 1
        self.lastEdit = getCurrentTimeStamp()

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








