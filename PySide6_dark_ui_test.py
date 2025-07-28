from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PySide6.QtGui import QFont
import sys

app = QApplication(sys.argv)
window = QWidget()
window.setStyleSheet("""
    QWidget { background-color: #2b2b2b; }
    QLabel { color: white; font-family: Arial; }
    QTextEdit {
        background-color: #404040;
        color: white;
        border: 1px solid #666;
        padding: 10px;
        font-family: 'Courier New', monospace;
        border-radius: 10px;
    }
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 8px 16px;
        margin: 5px 2px;
        min-width: 80px;
        border-radius: 4px;
    }
    QPushButton:hover { background-color: #45a049; }
""")
layout = QVBoxLayout()
title = QLabel("Price Breakdown")
title.setFont(QFont("Arial", 14, QFont.Bold))
layout.addWidget(title)
summary = QLabel("Total Cost: $99.99 | Games: 5")
summary.setFont(QFont("Arial", 11))
layout.addWidget(summary)
box = QTextEdit()
box.setReadOnly(True)
box.setPlainText("Game Name                Bundle Cost   Steam Price   Bundle %\n"
                 "----------------------------------------------------------\n"
                 "Example Game 1           $10.00        $20.00        10.0%\n"
                 "Example Game 2           $20.00        $30.00        20.0%\n")
layout.addWidget(box)
btn = QPushButton("Proceed with These Prices")
layout.addWidget(btn)
window.setLayout(layout)
window.setWindowTitle("PySide6 Styled Box")
window.resize(600, 400)
window.show()
sys.exit(app.exec())