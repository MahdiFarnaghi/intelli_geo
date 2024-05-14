import sys
from PyQt5.QtWidgets import QApplication, QMessageBox

def printShow(title, message):
    '''
    display given text
    test function of communication logics
    '''
    app = QApplication(sys.argv)
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.setIcon(QMessageBox.Information)
    msg.exec_()
    sys.exit()


