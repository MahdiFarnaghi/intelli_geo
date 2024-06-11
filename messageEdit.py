from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import pyqtSignal, Qt

class MessageEdit(QTextEdit):
    enterPressed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.enterPressed.emit()
        else:
            super().keyPressEvent(event)