import os
from typing import Tuple

from qgis.PyQt import QtGui, QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal

from qgis.PyQt.QtCore import QEvent, Qt

# Import customized widgets for message
from . import messageEdit
from .utils import nestedDict2list, show_variable_popup

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
        show_variable_popup(self.llmFullList)
        for llmIDItem in self.llmFullList:
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
        endpoint, apiKey = self.configfullList[currentIndex][-2:]
        self.leAPIEndpoint.setText(endpoint)
        self.leAPIEndpoint.setReadOnly(True)
        self.leAPIKey.setText(apiKey)

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
        endpoint, apiKey = self.configfullList[index][-2:]
        self.leAPIEndpoint.setText(endpoint)
        self.leAPIKey.setText(apiKey)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and obj is self.ptName:
            if event.key() == Qt.Key_Return and self.ptName.hasFocus():
                self.ptDescription.setFocus()
                return True
        return super().eventFilter(obj, event)
