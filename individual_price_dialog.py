from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QWidget, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class IndividualPriceDialog(QDialog):
    def __init__(self, bundle_games, total_cost, parent=None):
        super().__init__(parent)
        self.bundle_games = bundle_games
        self.total_cost = total_cost
        self.price_inputs = {}
        
        self.setWindowTitle('Enter Individual Game Prices')
        self.setMinimumSize(500, 400)
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: white;
            }
            QLabel {
                color: white;
            }
            QLineEdit {
                background-color: #404040;
                color: white;
                border: 1px solid #666;
                padding: 5px;
                margin: 2px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                margin: 5px 2px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QScrollArea {
                border: 1px solid #555;
                background-color: #2b2b2b;
            }
            QWidget {
                background-color: #2b2b2b;
            }
            QMessageBox {
                background-color: #2b2b2b;
                color: white;
            }
            QMessageBox QLabel {
                color: white;
            }
            QMessageBox QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                margin: 5px 2px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        # Create main layout
        layout = QVBoxLayout()
        
        # Add title
        title_label = QLabel('Multi Purchase - Enter Individual Prices')
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        # Add explanation
        explanation = QLabel(
            f"You chose 'Multi Purchase' for {len(bundle_games)} games.\n"
            f"Total bundle cost: ${total_cost:.2f}\n\n"
            "Please enter the individual price you paid for each game:"
        )
        explanation.setStyleSheet("margin: 10px; font-size: 12px;")
        layout.addWidget(explanation)
        
        # Create scrollable area for game inputs
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Add input fields for each game
        for i, game_name in enumerate(bundle_games):
            game_layout = QHBoxLayout()
            
            # Game name label
            game_label = QLabel(f"{i+1}. {game_name}:")
            game_label.setMinimumWidth(300)
            game_layout.addWidget(game_label)
            
            # Price input
            price_input = QLineEdit()
            price_input.setPlaceholderText("0.00")
            price_input.setMaximumWidth(100)
            self.price_inputs[game_name] = price_input
            game_layout.addWidget(price_input)
            
            # Dollar sign
            dollar_label = QLabel("$")
            game_layout.addWidget(dollar_label)
            
            game_layout.addStretch()
            scroll_layout.addLayout(game_layout)
        
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
        # Add total calculation label
        self.total_label = QLabel("Current total: $0.00")
        self.total_label.setStyleSheet("font-weight: bold; margin: 10px;")
        layout.addWidget(self.total_label)
        
        # Connect input changes to update total
        for price_input in self.price_inputs.values():
            price_input.textChanged.connect(self.update_total)
        
        # Add buttons
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton('OK')
        self.cancel_button = QPushButton('Cancel')
        
        self.ok_button.clicked.connect(self.validate_and_accept)
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        # Set focus on first input
        if self.price_inputs:
            first_input = list(self.price_inputs.values())[0]
            first_input.setFocus()
    
    def update_total(self):
        """Update the total as user types."""
        total = 0.0
        for price_input in self.price_inputs.values():
            try:
                value = float(price_input.text() or "0")
                total += value
            except ValueError:
                pass
        
        self.total_label.setText(f"Current total: ${total:.2f}")
        
        # Color code the total
        if abs(total - self.total_cost) < 0.01:  # Within 1 cent
            self.total_label.setStyleSheet("font-weight: bold; margin: 10px; color: #4CAF50;")
        elif total > self.total_cost:
            self.total_label.setStyleSheet("font-weight: bold; margin: 10px; color: #f44336;")
        else:
            self.total_label.setStyleSheet("font-weight: bold; margin: 10px; color: #ff9800;")
    
    def validate_and_accept(self):
        """Validate prices before accepting."""
        individual_prices = {}
        total_entered = 0.0
        
        # Collect and validate all prices
        for game_name, price_input in self.price_inputs.items():
            try:
                price = float(price_input.text() or "0")
                if price < 0:
                    msg_box = QMessageBox(self)
                    msg_box.setWindowTitle("Invalid Price")
                    msg_box.setText(f"Price for '{game_name}' cannot be negative.")
                    msg_box.setIcon(QMessageBox.Icon.Warning)
                    msg_box.setStyleSheet("""
                        QMessageBox {
                            background-color: #2b2b2b;
                            color: white;
                        }
                        QMessageBox QLabel {
                            color: white;
                        }
                        QPushButton {
                            background-color: #4CAF50;
                            color: white;
                            border: none;
                            padding: 8px 16px;
                            margin: 5px 2px;
                            min-width: 80px;
                        }
                        QPushButton:hover {
                            background-color: #45a049;
                        }
                    """)
                    msg_box.exec()
                    return
                individual_prices[game_name] = price
                total_entered += price
            except ValueError:
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("Invalid Price")
                msg_box.setText(f"Invalid price entered for '{game_name}'. Please enter a valid number.")
                msg_box.setIcon(QMessageBox.Icon.Warning)
                msg_box.setStyleSheet("""
                    QMessageBox {
                        background-color: #2b2b2b;
                        color: white;
                    }
                    QMessageBox QLabel {
                        color: white;
                    }
                    QPushButton {
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        padding: 8px 16px;
                        margin: 5px 2px;
                        min-width: 80px;
                    }
                    QPushButton:hover {
                        background-color: #45a049;
                    }
                """)
                msg_box.exec()
                return
        
        # Check if total matches (within reasonable tolerance)
        if abs(total_entered - self.total_cost) > 0.01:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Total Mismatch")
            msg_box.setIcon(QMessageBox.Icon.Question)
            msg_box.setText(
                f"Individual prices total: ${total_entered:.2f}\n"
                f"Bundle cost: ${self.total_cost:.2f}\n"
                f"Difference: ${abs(total_entered - self.total_cost):.2f}\n\n"
                "Do you want to continue anyway?"
            )
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #2b2b2b;
                    color: white;
                }
                QMessageBox QLabel {
                    color: white;
                }
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    margin: 5px 2px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            
            reply = msg_box.exec()
            if reply != QMessageBox.StandardButton.Yes:
                return
        
        self.individual_prices = individual_prices
        self.accept()
    
    def get_individual_prices(self):
        """Return the individual prices entered by user."""
        return getattr(self, 'individual_prices', {})
