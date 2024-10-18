from qgis.PyQt.QtWidgets import QDialog, QLabel, QPushButton, QHBoxLayout, QVBoxLayout

class DebugDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Debug Mode")
        self.setModal(True)  # Make it a modal dialog (blocks other windows)

        # Create a label to ask the question
        self.label = QLabel("Do you want to enable debug mode? In this mode IntelliGeo will read "
                            "the error log and auto-fix.")

        # Create Yes and No buttons
        self.yes_button = QPushButton("Yes")
        self.no_button = QPushButton("No")

        # Connect buttons to their slots
        self.yes_button.clicked.connect(self.accept)  # Dialog will return True when accepted
        self.no_button.clicked.connect(self.reject)  # Dialog will return False when rejected

        # Layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.yes_button)
        button_layout.addWidget(self.no_button)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addLayout(button_layout)
        self.setLayout(layout)