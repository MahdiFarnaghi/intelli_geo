from datetime import datetime
from functools import wraps
import uuid

from qgis.PyQt.QtWidgets import QApplication, QMessageBox
import inspect


def generateUniqueID():
    ID = str(uuid.uuid4())
    return ID.replace("-", "_")


def getCurrentTimeStamp():
    currentTime = datetime.now()
    timeString = currentTime.strftime("%B %d %Y %H:%M:%S")

    return timeString


def handleNoneConversation(func):
    @wraps(func)
    def wrapper(self, conversation, *args, **kwargs):
        if conversation is None:
            # If conversation is None, do nothing
            return
        return func(self, conversation, *args, **kwargs)

    return wrapper


def formatDescription(description):
    return description + '\n'


def unpack(infoDict):
    colNames = ['title', 'description', 'created', 'lastEdit', 'LLMName', 'messageCount', 'modelCount', 'ID']
    infoList = []
    for name in colNames:
        infoList.append(infoDict[name])

    return infoList


def pack(infoList):
    colNames = ['title', 'description', 'created', 'lastEdit', 'LLMName', 'messageCount', 'modelCount', 'ID']
    infoDict = {}
    for i, name in enumerate(colNames):
        infoDict[name] = infoList[i]

    return infoDict


def show_variable_popup(variable):
    # TODO: stylish
    app = QApplication.instance()  # Get the existing QApplication instance
    if not app:
        app = QApplication([])  # Create a new instance if no instance exists

    # Get the name of the variable from the caller's local variables
    frame = inspect.currentframe().f_back
    variable_name = None
    for name, val in frame.f_locals.items():
        if val is variable:
            variable_name = name
            break

    if variable_name is None:
        variable_name = 'Unknown'

    # Create and display the popup
    message = f'Variable Name: {variable_name}\nString Value: {variable}'
    QMessageBox.information(None, 'String and Variable Name', message)

    if not QApplication.instance():
        app.exec_()  # Start the application loop if not already running
