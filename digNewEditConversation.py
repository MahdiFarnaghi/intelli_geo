import os

from qgis.PyQt import QtGui, QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal

from qgis.PyQt.QtCore import QEvent, Qt

# Import customized widgets for message
from . import messageEdit

# Load the UI file
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'dlgNewEditConversation.ui'))


class NewEditConversationDialog(QtWidgets.QDialog, FORM_CLASS):
    closed = pyqtSignal()
    titleEnterPressed = pyqtSignal(str)

    def __init__(self, title=None, description=None, parent=None):
        """Constructor."""
        super(NewEditConversationDialog, self).__init__(parent)
        # Set up the user interface from Designer.

        self.setupUi(self)
        if title is not None:
            self.ptName.setText(title)
        if description is not None:
            self.ptDescription.setPlainText(description)

        self.pbOkay.clicked.connect(self.handleOkay)
        self.pbCancel.clicked.connect(self.close)

        # flag of update
        self.isUpdate = False

        # install the event filter to self.ptName
        self.ptName.installEventFilter(self)

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()

    def onUpdateMetadata(self):
        name = self.ptName.text()
        description = self.ptDescription.toPlainText()
        LLM = self.cbLLM.currentText()

        return name, description, LLM

    def handleOkay(self):
        # Call onUpdateMetadata and process output
        name, description, LLM = self.onUpdateMetadata()
        self.accept()  # Close the dialog

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and obj is self.ptName:
            if event.key() == Qt.Key_Return and self.ptName.hasFocus():
                self.ptDescription.setFocus()
                return True
        return super().eventFilter(obj, event)
