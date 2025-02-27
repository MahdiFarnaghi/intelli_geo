from qgis.PyQt.QtWidgets import QComboBox, QListView
from qgis.PyQt.QtCore import QModelIndex, pyqtSignal
from .utils import show_variable_popup

class HoverComboBox(QComboBox):
    hovered = pyqtSignal(str)  # Custom signal emitted when an item is hovered

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setView(QListView())  # Use a QListView for better control
        self.view().entered.connect(self.on_item_hovered)

        self.last_hovered_item = None  # To track the last hovered item

    def on_item_hovered(self, index: QModelIndex):
        """
        Emit the 'hovered' signal only when the mouse moves to a new item.
        """
        if index.isValid():
            item_text = index.data()
            if item_text != self.last_hovered_item:  # Check if the hovered item has changed
                self.last_hovered_item = item_text
                self.hovered.emit(item_text)  # Emit the signal with the new item

    def add_item_with_action(self, item_text, hoverAction):
        """
        Add an item to the combo box and connect it to a hover action.
        """
        self.addItem(item_text)  # Add the new item
        self.hovered.connect(hoverAction)  # Connect the hover signal to the action

    def clear_hover_state(self):
        """
        Reset the last hovered state when the popup is hidden.
        """
        self.last_hovered_item = None

    def showPopup(self):
        """
        Override showPopup to reset the hover state when the popup is shown.
        """
        self.clear_hover_state()
        super().showPopup()
