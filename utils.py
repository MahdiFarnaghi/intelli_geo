from datetime import datetime
from functools import wraps
from bs4 import BeautifulSoup
from typing import Literal
import uuid
import re
import requests

from qgis.core import Qgis
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QLabel, QDialog, QScrollArea, QVBoxLayout, QWidget
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


def unpack(rowDict: dict, table: Literal["conversation", "interaction", "prompt"]) -> list:
    if table not in ["conversation", "interaction", "prompt"]:
        raise ValueError("Must specify the table type for function 'unpack'")

    # make pycharm happy
    colnameList = []

    if table == "conversation":
        colnameList = ["ID", "llmID", "title", "description", "created", "modified", "messageCount", "modelCount", "userID"]
    elif table == "interaction":
        colnameList = ["ID", "conversationID", "promptID", "requestText", "contextText", "requestTime", "typeMessage",
                       "responseText", "responseTime", "workflow", "executionLog"]
    elif table == "prompt":
        colnameList = ["ID", "llmID", "version", "template", "promptType"]

    rowList = []
    for name in colnameList:
        rowList.append(rowDict[name])

    return rowList


def pack(rowTuple: tuple, table: Literal["conversation", "interaction", "prompt"]) -> dict:
    """
    Converts a tuple of row data into a dictionary with column names as keys.
    Raise valueError: If the table type is not "conversation" or "interaction".
    """
    if table not in ["conversation", "interaction", "prompt"]:
        raise ValueError("Must specify the table type for function 'pack'.")

    # make pycharm happy
    colnameList = []

    if table == "conversation":
        colnameList = ["ID", "llmID", "title", "description", "created", "modified", "messageCount", "modelCount", "userID"]
    elif table == "interaction":
        colnameList = ["ID", "conversationID", "promptID", "requestText", "contextText", "requestTime", "typeMessage",
                       "responseText", "responseTime", "workflow", "executionLog"]
    elif table == "prompt":
        colnameList = ["ID", "llmID", "version", "template", "promptType"]

    rowDict = {}
    for i, name in enumerate(colnameList):
        rowDict[name] = rowTuple[i]

    return rowDict


def getVersion():
    fullVersion = Qgis.QGIS_VERSION
    return ".".join(fullVersion.split('.')[:2])


def tuple2Dict(allRowList: list[tuple], table: Literal["conversation", "interaction", "prompt"]) -> list[dict]:
    result = []
    for rowTuple in allRowList:
        result.append(pack(rowTuple, table))

    return result


def nestedDict2list(fullDict: dict[list]) -> list:
    ans = []
    for key, subList in fullDict.items():
        for item in subList:
            ans.append(f"{key}::{item}")

    return ans


def extractCode(response: str) -> str:
    pattern = r'```python(.*?)```'
    match = re.search(pattern, response, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return ""


def extractXml(response: str) -> str:
    pattern = r'```xml(.*?)```'
    match = re.search(pattern, response, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        startMarker = '```xml'
        endMarker = '>'
        substring = None

        startIndex = response.rfind(startMarker)
        if startIndex != -1:
            startIndex += len(startMarker)
            endIndex = response.rfind(endMarker, startIndex)
            if endIndex != -1:
                substring = response[startIndex:(endIndex + len(endMarker))]

        if substring:
            return substring
        else:
            return ""


def readURL(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    soup = BeautifulSoup(response.content, 'html.parser')
    pageText = soup.get_text()

    return pageText


def splitAtPattern(inputStr, pattern=r'13.*?\n'):
    # Find all matches of the pattern in the input string
    matches = re.finditer(pattern, inputStr)

    # Initialize the start position
    start = 0
    parts = []

    for match in matches:
        # Get the position of the match
        matchStart, matchEnd = match.span()

        # Append the part before the match
        parts.append(inputStr[start:matchStart])

        # Update the start position to the end of the match
        start = matchStart

    # Append the remaining part of the string
    parts.append(inputStr[start:])

    return parts


def show_variable_popup(variable):
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

    # Create the dialog
    dialog = QDialog()
    dialog.setWindowTitle('String and Variable Name')

    # Create the scroll area
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)

    # Create a widget to hold the contents
    content_widget = QWidget()
    content_layout = QVBoxLayout(content_widget)

    # Add content to the layout
    message = f'Variable Name: {variable_name}\nString Value: {variable}'
    label = QLabel(message)
    content_layout.addWidget(label)

    # Set the content widget to the scroll area
    scroll_area.setWidget(content_widget)

    # Create the main layout and add the scroll area to it
    main_layout = QVBoxLayout(dialog)
    main_layout.addWidget(scroll_area)

    # Set the dialog layout
    dialog.setLayout(main_layout)

    # Show the dialog
    dialog.exec_()

    if not QApplication.instance():
        app.exec_()  # Start the application loop if not already running
