

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMdiArea, QMdiSubWindow, QTextEdit,
    QMenuBar, QMenu, QAction, QPushButton, QVBoxLayout, QWidget
)
from PyQt5.QtCore import Qt

class CustomSubWindow(QMdiSubWindow):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setAttribute(Qt.WA_StyledBackground, True)

        # Create widget and layout for subwindow content
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Add a text edit
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        # Add buttons to change title bar and background colors
        self.btn_change_title_color = QPushButton("Change Title Color")
        self.btn_change_title_color.clicked.connect(self.change_title_color)
        layout.addWidget(self.btn_change_title_color)

        self.btn_change_bg_color = QPushButton("Change Background Color")
        self.btn_change_bg_color.clicked.connect(self.change_background_color)
        layout.addWidget(self.btn_change_bg_color)

        self.setWidget(widget)

        # Set initial stylesheet
        self.update_stylesheet(title_color="#2196F3", bg_color="#333333")

    def update_stylesheet(self, title_color, bg_color):
        """Update the stylesheet with new title bar and background colors."""
        self.setStyleSheet(f"""
            QMdiSubWindow {{
                background-color: {bg_color};
                border: 1px solid #555555;
            }}
            QMdiSubWindow:title {{
                background-color: {title_color};
                color: white;
                padding: 5px;
            }}
            QMdiSubWindow:!focus:title {{
                background-color: #666666;
                color: white;
            }}
        """)

    def change_title_color(self):
        """Cycle through title bar colors."""
        colors = ["#2196F3", "#4CAF50", "#F44336", "#9C27B0"]  # Blue, Green, Red, Purple
        current_color = self.styleSheet().split("background-color: ")[2].split(";")[0]
        next_color = colors[(colors.index(current_color) + 1) % len(colors)] if current_color in colors else colors[0]
        self.update_stylesheet(title_color=next_color, bg_color=self.styleSheet().split("background-color: ")[1].split(";")[0])

    def change_background_color(self):
        """Cycle through background colors."""
        colors = ["#333333", "#2E2E2E", "#4A4A4A", "#1C2526"]  # Dark shades
        current_color = self.styleSheet().split("background-color: ")[1].split(";")[0]
        next_color = colors[(colors.index(current_color) + 1) % len(colors)] if current_color in colors else colors[0]
        self.update_stylesheet(title_color=self.styleSheet().split("background-color: ")[2].split(";")[0], bg_color=next_color)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MDI Application with Dynamic Colors")
        self.setGeometry(100, 100, 800, 600)

        # Create menu bar
        menubar = QMenuBar(self)
        self.setMenuBar(menubar)
        style_menu = QMenu("Style", self)
        menubar.addMenu(style_menu)

        # Add actions to change MDI area background
        self.action_blue = QAction("MDI Blue Background", self)
        self.action_blue.triggered.connect(lambda: self.change_mdi_background("#2196F3"))
        style_menu.addAction(self.action_blue)

        self.action_green = QAction("MDI Green Background", self)
        self.action_green.triggered.connect(lambda: self.change_mdi_background("#4CAF50"))
        style_menu.addAction(self.action_green)

        self.action_dark = QAction("MDI Dark Background", self)
        self.action_dark.triggered.connect(lambda: self.change_mdi_background("#2E2E2E"))
        style_menu.addAction(self.action_dark)

        # Create MDI Area
        self.mdi_area = QMdiArea()
        self.setCentralWidget(self.mdi_area)
        self.mdi_area.setStyleSheet("QMdiArea { background-color: #2E2E2E; }")

        # Add subwindows
        for i in range(3):
            subwindow = CustomSubWindow(f"Subwindow {i+1}")
            self.mdi_area.addSubWindow(subwindow)

    def change_mdi_background(self, color):
        """Change the MDI area background color."""
        self.mdi_area.setStyleSheet(f"QMdiArea {{ background-color: {color}; }}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Use Fusion style for consistent look on Linux Mint
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())