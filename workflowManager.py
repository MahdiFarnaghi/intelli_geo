# from settings import *
import os
from .utils import extractXml, extractCode, getCurrentTimeStamp


class WorkflowManager:
    def __init__(self, modelPath=None):
        if modelPath is None:
            self.modelPath = os.path.join(os.path.expanduser("~"), "Documents", "QGIS_IntelliGeo")
            os.makedirs(self.modelPath, exist_ok=True)

    def saveWorkflow(self, response, workflowType, conversationTitle, modelCount):
        if workflowType not in ["withModel", "withCode"]:
            raise ValueError(f"workflowType should be either 'withModel' or 'withCode', got '{str(workflowType)}'")

        if workflowType == "withModel":
            fileName = f"model_{conversationTitle}_{str(modelCount)}.model3"
            filePath = os.path.join(self.modelPath, fileName)
            with open(filePath, "w") as file:
                file.write(extractXml(response))
        else:
            fileName = f"model_{conversationTitle}_{str(modelCount)}.py"
            filePath = os.path.join(self.modelPath, fileName)
            with open(filePath, "w") as file:
                file.write(extractCode(response))

        return filePath
