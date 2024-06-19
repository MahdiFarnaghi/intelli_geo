from langchain.tools import tool
# from typing import *
import requests
from bs4 import BeautifulSoup

from qgis.utils import iface

from qgis.PyQt import QtWidgets, QtGui

from .environment import QgisEnvironment


@tool
def readEnvironment() -> str:
    """
    Use this tool to retrieve detailed information about the currently opened project in QGIS.

    The tool provides comprehensive data for all types of layers, including:
        - Layer Name
        - Layer Type
        - Coordinate Reference System (CRS)
        - Extent

    For vector layers, additional information is included:
        - Geometry Type

    For raster layers, additional information is included:
        - Resolution
        - Attributes (including Band Names and Data Types)
    """
    environment = QgisEnvironment()
    environment.refresh()
    return environment.getLayerAttributes()

def readVersion() -> str:
    environment = QgisEnvironment()
    return environment.version


def activateConsole(code: str, run: bool) -> None:
    iface.openPythonConsole()
    console = iface.pythonConsole()
    consoleWidget = console.findChild(QtWidgets.QPlainTextEdit)
    consoleWidget.insertPlainText(code)
    consoleWidget.setFocus()
    consoleWidget.moveCursor(QtGui.QTextCursor.End)
    consoleWidget.ensureCursorVisible()
    consoleWidget.setFocus()
    QtWidgets.QApplication.processEvents()

    if run:
        console.runCommand(consoleWidget.toPlainText())

    return None
