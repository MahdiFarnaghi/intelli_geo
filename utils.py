"""
`utils.py` contains tool functions that is useful but not n

Created: May 2024
Last modified by: Zehao Lu @com3dian
"""

from datetime import datetime
from functools import wraps
from bs4 import BeautifulSoup
from typing import Literal
import uuid
import re
import requests
import psutil

from qgis.core import Qgis
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QDialog, QScrollArea, QVBoxLayout,
                             QWidget, QMessageBox, QPushButton, QLineEdit)
import inspect


def generateUniqueID():
    ID = str(uuid.uuid4())
    return ID.replace("-", "_")


def getCurrentTimeStamp():
    currentTime = datetime.now()
    timeString = currentTime.strftime("%m %d %Y %H:%M:%S")

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
        colnameList = ["ID", "llmID", "title", "description",
                       "created", "modified", "messageCount", "workflowCount",
                       "userID"]
    elif table == "interaction":
        colnameList = ["ID", "conversationID", "promptID", "requestText", "contextText", "requestTime", "typeMessage",
                       "responseText", "responseTime", "workflow", "executionLog"]
    elif table == "prompt":
        colnameList = ["ID", "llmID", "version", "template", "promptType"]

    if set(rowDict.keys()) != set(colnameList):
        raise KeyError("Unknown key in input.")

    rowList = []
    for name in colnameList:
        rowList.append(rowDict[name])

    return rowList


def pack(rowTuple: tuple, table: Literal["conversation", "interaction", "prompt"]) -> dict:
    """
    Converts a tuple of row data into a dictionary with column names as keys.
    Raise valueError: If the table type is not "conversation", "interaction" or "prompt".
    """
    if table not in ["conversation", "interaction", "prompt"]:
        raise ValueError("Must specify the table type for function 'pack'.")

    # make pycharm happy
    colnameList = []

    if table == "conversation":
        colnameList = ["ID", "llmID", "title", "description",
                       "created", "modified", "messageCount", "workflowCount",
                       "userID"]
    elif table == "interaction":
        colnameList = ["ID", "conversationID", "promptID",
                       "requestText", "contextText", "requestTime", "typeMessage",
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


def getSystemInfo():
    macAddresses = []
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == psutil.AF_LINK:
                macAddresses.append(addr.address)
    interfaces = psutil.net_if_addrs()

    # Filter only Ethernet interfaces (assuming Ethernet uses AF_LINK)
    ethInterfaces = [iface for iface, addrs in interfaces.items() if
                      any(addr.family == psutil.AF_LINK for addr in addrs)]

    qgisVersion = getVersion()

    systemInfo = {
        "macID": macAddresses[0] if macAddresses else "N/A",
        "ethInterfaces": ', '.join(ethInterfaces),
        "qgisVersion": qgisVersion
    }

    return systemInfo


def captcha_popup(captcha_dict):
    """
    Creates a dialog to display a captcha question, with an input field for the answer and confirm/cancel buttons.
    If no button is clicked and the dialog is closed, the function does not return any value.

    :param captcha_dict: Dictionary containing the captcha question and values.
    :return: The user's answer if confirmed, None if canceled, and nothing if no button is clicked.
    """
    app = QApplication.instance() or QApplication([])  # Create a QApplication if it doesn't exist

    # Create a QDialog as the main window
    dialog = QDialog()
    dialog.setWindowTitle("Captcha Verification")

    # Create the layout
    layout = QVBoxLayout()

    # Create and add the label with the question
    question_label = QLabel(captcha_dict.get('question', ''))
    layout.addWidget(question_label)

    # Create and add the QLineEdit for user input
    answer_input = QLineEdit()
    layout.addWidget(answer_input)

    # Create the confirm and cancel buttons
    button_layout = QHBoxLayout()

    confirm_button = QPushButton("Confirm")
    cancel_button = QPushButton("Cancel")

    button_layout.addWidget(confirm_button)
    button_layout.addWidget(cancel_button)

    layout.addLayout(button_layout)

    # Set the layout for the dialog
    dialog.setLayout(layout)

    # Variable to store the user's answer
    user_answer = None
    button_clicked = False

    # Define a function to handle the confirm button click
    def on_confirm():
        nonlocal user_answer, button_clicked
        user_answer = answer_input.text()
        if user_answer:
            button_clicked = True
            dialog.accept()  # Close the dialog and accept the result

    # Define a function to handle the cancel button click
    def on_cancel():
        nonlocal user_answer, button_clicked
        user_answer = None  # Ensure user_answer is None when cancel is clicked
        button_clicked = True
        dialog.reject()  # Close the dialog and reject the result

    # Connect the buttons to their respective functions
    confirm_button.clicked.connect(on_confirm)
    cancel_button.clicked.connect(on_cancel)

    # Execute the dialog and wait for the user response
    result = dialog.exec_()

    # Return the input value or None depending on the user action, or nothing if no button was clicked
    if result == QDialog.Accepted and button_clicked:
        return user_answer
    return None



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
