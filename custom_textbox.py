from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtGui import QFont

class CustomTextBox(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Arial", 12))
        self.setStyleSheet("background-color: #404040; color: white; border: 1px solid #666; padding: 5px;")
        # Add any shared logic or methods here
