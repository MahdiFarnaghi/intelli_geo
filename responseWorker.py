import traceback

from qgis.PyQt.QtCore import QRunnable, pyqtSignal, QObject
from .utils import show_variable_popup

class WorkerSignals(QObject):
    finished = pyqtSignal(object, object)  # Signal to emit when the task is finished
    error = pyqtSignal(object)  # Signal to emit when error occurs

class ResponseWorker(QRunnable):
    def __init__(self, processor, userInput, responseType):
        super().__init__()
        self.processor = processor
        self.userInput = userInput
        self.responseType = responseType
        self.signals = WorkerSignals()

    def run(self):
        try:
            # Execute the long-running task
            self.processor.dataloader.connect()
            response, workflow = self.processor.response(self.userInput, self.responseType)
            # Emit the finished signal with the response and workflow
            self.signals.finished.emit(response, workflow)
            self.processor.dataloader.close()
        except Exception as e:
            errorStr = traceback.format_exc()
            self.signals.error.emit(errorStr)


class ReflectWorker(QRunnable):
    def __init__(self, processor, executedCode, logMessage, responseType):
        super().__init__()
        self.processor = processor
        self.logMessage = logMessage
        self.executedCode = executedCode
        self.responseType = responseType
        self.signals = WorkerSignals()

    def run(self):
        try:
            # Execute the long-running task
            self.processor.dataloader.connect()
            response, workflow = self.processor.reflect(self.logMessage, self.executedCode, self.responseType)
            # Emit the finished signal with the response and workflow
            self.signals.finished.emit(response, workflow)
            self.processor.dataloader.close()
        except Exception as e:
            errorStr = traceback.format_exc()
            self.signals.error.emit(errorStr)
