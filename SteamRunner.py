import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QSpacerItem, QSizePolicy, QPushButton, QGridLayout, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
import sys
import openpyxl
from SteamAPI_Caller import update_spreadsheet, get_total_games_and_hours

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Steam Data Tracker")

        # Set the main window background color
        self.setStyleSheet("background-color: #202020;")  # Dark gray background

        # Make the window cover the entire screen but remain windowed
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        self.setGeometry(screen_geometry)  # Set the window geometry to the screen size

        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a vertical layout for the boxes
        main_layout = QVBoxLayout()

        # Create a horizontal layout for the boxes
        boxes_layout = QHBoxLayout()
        boxes_layout.setSpacing(40)  # Set the gap between boxes (in pixels)

        # Create the first box (number and caption)
        self.total_games_label = self.add_number_box(boxes_layout, "0", "Total Games", "#FFCCCB")  # Light red
        
        # Create the second box (number and caption)
        self.total_hours_label = self.add_number_box(boxes_layout, "0.00", "Total Hours", "#ADD8E6")  # Light blue
        
        # Create the third box (number and caption)
        self.average_playtime_label = self.add_number_box(boxes_layout, "0.00", "Average Playtime", "#90EE90")  # Light green

        # Add the boxes layout to the main layout
        main_layout.addLayout(boxes_layout)

        # Define button names in a dictionary
        self.button_names = {
            1: "Update Steam Info",
            2: "Random Game",
            3: "Button 3",
            4: "Button 4",
            5: "Button 5",
            6: "Button 6",
            7: "Button 7",
            8: "Button 8",
            9: "Button 9",
            10: "Button 10",
            11: "Button 11",
            12: "Button 12"
        }

        # Create a grid layout for buttons
        button_grid = QGridLayout()

        # Add buttons to the grid layout using the names from the dictionary
        for i in range(1, 13):  # 12 buttons
            button = QPushButton(self.button_names[i])
            
            # Set fixed width and height for the buttons
            button.setMinimumWidth(400)
            button.setMaximumWidth(400)
            button.setMinimumHeight(100)
            button.setMaximumHeight(100)

            # Set the button background color to light gray
            button.setStyleSheet("background-color: #D3D3D3;")  # Light gray background for buttons

            # Connect specific actions to specific buttons
            if i == 1:  # "Update Steam Info" button
                button.clicked.connect(self.update_steam_data)
            elif i == 2:  # "Random Game" button
                button.clicked.connect(self.select_random_game)

            # Add the button to the grid (3 columns layout)
            row = (i - 1) // 3
            col = (i - 1) % 3
            button_grid.addWidget(button, row, col)

        # Add the button grid to the main layout
        main_layout.addLayout(button_grid)

        # Set the layout for the central widget
        central_widget.setLayout(main_layout)

    def add_number_box(self, layout, number, caption, color):
        """Helper function to add a number box to the layout."""
        # Create a vertical layout for each box
        box_layout = QVBoxLayout()

        number_label = QLabel(number, self)
        number_label.setFont(QFont("Arial", 24))
        number_label.setAlignment(Qt.AlignCenter)

        caption_label = QLabel(caption, self)
        caption_label.setFont(QFont("Arial", 12))
        caption_label.setAlignment(Qt.AlignCenter)

        # Add the labels to the box layout
        box_layout.addWidget(number_label)
        box_layout.addWidget(caption_label)

        # Create a widget to hold the box layout and set its background color
        box_widget = QWidget(self)
        box_widget.setLayout(box_layout)
        box_widget.setStyleSheet(f"background-color: {color}; padding: 10px; border-radius: 5px;")

        # Set a fixed width for the box widget
        box_widget.setMinimumWidth(300)
        box_widget.setMaximumWidth(300)
        box_widget.setMinimumHeight(300)
        box_widget.setMaximumHeight(300)

        # Add the box widget to the horizontal layout
        layout.addWidget(box_widget)

        # Return the QLabel to update later
        return number_label

    def update_steam_data(self):
        """Update Steam data and show loading animation."""
        # Create a local update button
        self.update_button = QPushButton("Update")  # Assign to self

        # Disable the update button and show a throbber
        self.update_button.setText("Updating...")
        self.update_button.setEnabled(False)

        # Start the throbber
        self.start_throbber()

        # Update the spreadsheet in a separate thread
        QTimer.singleShot(100, self.perform_update)  # Simulate an async operation

    def perform_update(self):
        """Perform the update of Steam data."""
        update_spreadsheet()  # Call the function to update the spreadsheet

        # Load the spreadsheet to get the updated values
        spreadsheet_path = r'D:\SteamHours\Steam Game V2.xlsx'
        workbook = openpyxl.load_workbook(spreadsheet_path)

        if 'Hours' in workbook.sheetnames:
            sheet = workbook['Hours']
            total_games, total_hours = get_total_games_and_hours(sheet)
            average_playtime = total_hours / total_games if total_games > 0 else 0.0

            # Update the labels with the new data
            self.total_games_label.setText(str(total_games))
            self.total_hours_label.setText(f"{total_hours:.2f}")
            self.average_playtime_label.setText(f"{average_playtime:.2f}")

        # Restore button state
        self.update_button.setText("Update Steam Info")
        self.update_button.setEnabled(True)

        # Stop the throbber
        self.stop_throbber()

    def start_throbber(self):
        """Start a simple throbber animation."""
        self.throbber_timer = QTimer(self)
        self.throbber_timer.timeout.connect(self.update_throbber)
        self.throbber_counter = 0
        self.throbber_text = "Updating"  # Base text for the throbber
        self.throbber_timer.start(500)  # Update every 500ms

    def update_throbber(self):
        """Update the throbber text."""
        # Add a dot for the throbber effect
        self.throbber_counter = (self.throbber_counter + 1) % 4
        dots = "." * self.throbber_counter
        self.update_button.setText(self.throbber_text + dots)

    def stop_throbber(self):
        """Stop the throbber timer."""
        self.throbber_timer.stop()

    def select_random_game(self):
        """Select a random game from the spreadsheet and display its name."""
        spreadsheet_path = r'D:\SteamHours\Steam Game V2.xlsx'
        workbook = openpyxl.load_workbook(spreadsheet_path)

        if 'Hours' in workbook.sheetnames:
            sheet = workbook['Hours']
            games = []
            for row in sheet.iter_rows(min_row=2, values_only=True):
                app_id, game_name = row[0], row[1]
                if game_name:
                    games.append(game_name)

            if games:
                random_game = random.choice(games)
                # Display the selected game name in a pop-up
                self.show_random_game_popup(random_game)

    def show_random_game_popup(self, game_name):
        """Show a pop-up window with the selected random game."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Random Game Selected")
        msg_box.setText(f"You got: {game_name}")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
