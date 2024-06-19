# from settings import *
import os
from .utils import extractXml, getCurrentTimeStamp

class ModelManager:
    def __init__(self, modelPath=None):
        if modelPath is None:
            self.modelPath = os.path.join(os.path.expanduser("~"), "Documents", "QGIS_IntelliGeo")
            os.makedirs(self.modelPath, exist_ok=True)

    def saveModel(self, response, conversationTitle, modelCount):
        createTime = getCurrentTimeStamp()
        fileName = f"model_{createTime}_{conversationTitle}_{str(modelCount)}.model3"
        filePath = os.path.join(self.modelPath, fileName)

        with open(filePath, "w") as file:
            file.write(extractXml(response))

        return filePath






