import os
from typing import Tuple

from qgis.PyQt import QtGui, QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal

from qgis.PyQt.QtCore import QEvent, Qt
from qgis.PyQt.QtWidgets import QLineEdit

# Import customized widgets for message
from . import messageEdit
from .utils import nestedDict2list, show_variable_popup


class PasswordLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setEchoMode(QLineEdit.Password)  # Start in password mode

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.setEchoMode(QLineEdit.Normal)  # Show text in normal mode when focused

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.setEchoMode(QLineEdit.Password)  # Hide text in password mode when not focused


# Load the UI file
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'dlgNewEditConversation.ui'))


class NewEditConversationDialog(QtWidgets.QDialog, FORM_CLASS):
    closed = pyqtSignal()
    titleEnterPressed = pyqtSignal(str)

    def __init__(self, llmFullDict, configfullList, title=None, description=None, llmID=None, parent=None):
        """Constructor."""
        super(NewEditConversationDialog, self).__init__(parent)
        self.configfullList = configfullList

        # Set up the user interface from Designer.
        self.setupUi(self)

        self.llmFullList = nestedDict2list(llmFullDict)
        for llmIDItem in self.llmFullList:
            if llmIDItem in ["default::default", "DeepSeek::deepseek-chat", "DeepSeek::deepseek-reasoner",
                             "OpenAI::o1"]:
                continue
            self.cbLLM.addItem(llmIDItem)

        if title is not None:
            self.ptName.setText(title)
        if description is not None:
            self.ptDescription.setPlainText(description)
        if llmID is not None:
            index = self.cbLLM.findText(llmID)
            self.cbLLM.setCurrentIndex(index)
            self.cbLLM.setEditable(False)
            self.cbLLM.setEnabled(False)

        currentIndex = self.cbLLM.currentIndex()
        currentLLMID = self.cbLLM.itemText(currentIndex)
        show_variable_popup(self.configfullList)
        for llmInfo in self.configfullList:
            if currentLLMID == llmInfo[0]:
                endpoint, apiKey = llmInfo[-2:]

                # endpoint, apiKey = self.configfullList[currentIndex][-2:]
                self.leAPIEndpoint.setText(endpoint)
                self.leAPIEndpoint.setReadOnly(True)

                # API key input lineEdit
                self.leAPIKey.setText(apiKey)
                self.leAPIKey.setEchoMode(QLineEdit.Password)
                break

        self.pbOkay.clicked.connect(self.handleOkay)
        self.pbCancel.clicked.connect(self.close)
        self.cbLLM.currentIndexChanged.connect(self.onIndexChanged)

        # flag of update
        self.isUpdate = False

        # install the event filter to self.ptName
        self.ptName.installEventFilter(self)

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()

    def onUpdateMetadata(self) -> Tuple[str, str, str, str, str]:
        name = self.ptName.text()
        description = self.ptDescription.toPlainText()
        llmID = self.cbLLM.currentText()
        endpoint = self.leAPIEndpoint.text()
        apiKey = self.leAPIKey.text()

        return name, description, llmID, endpoint, apiKey

    def handleOkay(self):
        # Call onUpdateMetadata and process output
        name, description, LLM, endpoint, apiKey = self.onUpdateMetadata()
        self.accept()  # Close the dialog

    def onIndexChanged(self, index):
        currentLLMID = self.cbLLM.itemText(index)
        for llmInfo in self.configfullList:
            if currentLLMID == llmInfo[0]:
                endpoint, apiKey = llmInfo[-2:]

                self.leAPIEndpoint.setText(endpoint)
                self.leAPIEndpoint.setReadOnly(True)

                # API key input lineEdit
                self.leAPIKey.setText(apiKey)
                self.leAPIKey.setEchoMode(QLineEdit.Password)
                break

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and obj is self.ptName:
            if event.key() == Qt.Key_Return and self.ptName.hasFocus():
                self.ptDescription.setFocus()
                return True
        return super().eventFilter(obj, event)
