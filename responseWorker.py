from qgis.PyQt.QtCore import QRunnable, pyqtSignal, QObject


class WorkerSignals(QObject):
    finished = pyqtSignal(object, object)  # Signal to emit when the task is finished


class ResponseWorker(QRunnable):
    def __init__(self, processor, userInput, responseType):
        super().__init__()
        self.processor = processor
        self.userInput = userInput
        self.responseType = responseType
        self.signals = WorkerSignals()

    def run(self):
        # Execute the long-running task
        self.processor.dataloader.connect()
        response, workflow = self.processor.response(self.userInput, self.responseType)
        # Emit the finished signal with the response and workflow
        self.signals.finished.emit(response, workflow)
        self.processor.dataloader.close()


class ReflectWorker(QRunnable):
    def __init__(self, processor, logMessage, responseType):
        super().__init__()
        self.processor = processor
        self.logMessage = logMessage
        self.responseType = responseType
        self.signals = WorkerSignals()

    def run(self):
        # Execute the long-running task
        self.processor.dataloader.connect()
        response, workflow = self.processor.reflect(self.logMessage, self.responseType)
        # Emit the finished signal with the response and workflow
        self.signals.finished.emit(response, workflow)
        self.processor.dataloader.close()
