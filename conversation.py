from langchain_cohere import ChatCohere

class Conversation:
    def __init__(self, tablename, dataloader, LLM = None):
        self.created = None
        self.messagesCount = None
        # number of qgis model
        self.modelCount = None

        self.tablename = tablename
        self.dataloader = dataloader
        self.LLMFinished = True
        if LLM is None:
            self.LLM = ChatCohere(cohere_api_key="nLWE6IlAgzdxuNELOSZq1WYFl5kuvUL3CIVqtZkl")
        else:
            self.LLM = LLM

    def updateUserPrompt(self, message):
        if self.LLMFinished:
            self.dataloader.insertdata(self.tablename, sender="user", message=message)
            self.updateLLMResponse(message)
        else:
            pass

    def updateLLMResponse(self, message):
        self.LLMFinished = False
        response = self.LLM.invoke(message)
        self.dataloader.insertdata(self.tablename, sender="LLM", message=response.content)
        self.LLMFinished = True

    def fetch(self):
        log = ''
        history = self.dataloader.selectdata(self.tablename)
        # TODO: fetch loops through the databse and takes everything, for larger database can be time wasting
        # TODO: should we have an alternative method 'dispaly' that simply take the current shown content and
        # TODO: attach responses to the tail?
        log += 'Displaying ' + str(len(history)) + ' messages.\n'
        for message in history:
            log += message[0] + ': ' + message[2] + '\t' + message[1] + '\n\n'

        return log







