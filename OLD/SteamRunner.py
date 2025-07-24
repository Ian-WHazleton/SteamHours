from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QGridLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys
import openpyxl  # Add this import statement
from SteamAPI_Caller import get_total_games_and_hours, get_average_playtime, update_spreadsheet

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Steam Game Stats")

        # Set the main window background color
        self.setStyleSheet("background-color: #202020;")

        # Make the window cover the entire screen but remain windowed
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        self.setGeometry(screen_geometry)

        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a vertical layout for the main layout
        main_layout = QVBoxLayout()

        # Create the Excel workbook and load the 'Hours' sheet
        self.workbook = openpyxl.load_workbook(r'D:\SteamHours\Steam Game V2.xlsx')
        if 'Hours' in self.workbook.sheetnames:
            self.sheet = self.workbook['Hours']
        else:
            raise Exception("Sheet 'Hours' does not exist in the workbook.")

        # Get total games and hours from the sheet
        self.total_games, self.total_hours = get_total_games_and_hours(self.sheet)
        self.average_playtime = get_average_playtime(self.sheet)

        # Create the boxes layout for displaying stats
        boxes_layout = QHBoxLayout()
        boxes_layout.setSpacing(40)

        # Create the boxes with stats
        self.add_number_box(boxes_layout, str(self.total_games), "Total Games", "#FFCCCB")
        self.add_number_box(boxes_layout, str(self.total_hours), "Total Hours", "#ADD8E6")
        self.add_number_box(boxes_layout, str(round(self.average_playtime, 2)), "Avg Playtime (hrs)", "#90EE90")

        # Add the boxes layout to the main layout
        main_layout.addLayout(boxes_layout)

        # Create a grid layout for buttons
        button_grid = QGridLayout()
        button_count = 1
        for row in range(4):
            for col in range(3):
                button = QPushButton(f"Button {button_count}")
                button.setMinimumWidth(400)
                button.setMaximumWidth(400)
                button.setMinimumHeight(100)
                button.setMaximumHeight(100)
                button.setStyleSheet("background-color: #D3D3D3;")
                button_grid.addWidget(button, row, col)
                button_count += 1

        # Add the button grid to the main layout
        main_layout.addLayout(button_grid)

        # Set the layout for the central widget
        central_widget.setLayout(main_layout)

    def add_number_box(self, layout, number, caption, color):
        """Helper function to add a number box to the layout."""
        box_layout = QVBoxLayout()

        number_label = QLabel(number, self)
        number_label.setFont(QFont("Arial", 24))
        number_label.setAlignment(Qt.AlignCenter)

        caption_label = QLabel(caption, self)
        caption_label.setFont(QFont("Arial", 12))
        caption_label.setAlignment(Qt.AlignCenter)

        box_layout.addWidget(number_label)
        box_layout.addWidget(caption_label)

        box_widget = QWidget(self)
        box_widget.setLayout(box_layout)
        box_widget.setStyleSheet(f"background-color: {color}; padding: 10px; border-radius: 5px;")
        box_widget.setMinimumWidth(300)
        box_widget.setMaximumWidth(300)
        box_widget.setMinimumHeight(300)
        box_widget.setMaximumHeight(300)

        layout.addWidget(box_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
