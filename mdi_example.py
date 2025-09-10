import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMdiArea, QMdiSubWindow,
                            QTextEdit, QVBoxLayout, QWidget, QPushButton, QHBoxLayout,
                            QLabel, QColorDialog, QComboBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPalette


class CustomMdiSubWindow(QMdiSubWindow):
    """Custom QMdiSubWindow with additional styling capabilities."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupWindow()

    def setupWindow(self):
        """Setup the window with custom styling."""
        # You can set individual window styles here if needed
        pass


class ColorCustomizer(QWidget):
    """Widget to customize MDI colors in real-time."""

    colorChanged = pyqtSignal()

    def __init__(self, mdi_area, parent=None):
        super().__init__(parent)
        self.mdi_area = mdi_area
        self.setupUI()

    def setupUI(self):
        layout = QHBoxLayout(self)

        # Preset themes
        theme_label = QLabel("Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems([
            "Default", "Dark Blue", "Dark Gray", "Green Theme",
            "Purple Theme", "Orange Theme", "Custom"
        ])
        self.theme_combo.currentTextChanged.connect(self.applyTheme)

        # Color customization buttons
        self.title_color_btn = QPushButton("Title Bar Color")
        self.title_color_btn.clicked.connect(self.chooseTitleColor)

        self.bg_color_btn = QPushButton("Background Color")
        self.bg_color_btn.clicked.connect(self.chooseBgColor)

        self.text_color_btn = QPushButton("Title Text Color")
        self.text_color_btn.clicked.connect(self.chooseTextColor)

        # Add widgets to layout
        layout.addWidget(theme_label)
        layout.addWidget(self.theme_combo)
        layout.addWidget(self.title_color_btn)
        layout.addWidget(self.bg_color_btn)
        layout.addWidget(self.text_color_btn)
        layout.addStretch()

        # Current colors
        self.title_color = "#4a90e2"
        self.bg_color = "#2c3e50"
        self.text_color = "#ffffff"

    def applyTheme(self, theme_name):
        """Apply predefined theme."""
        themes = {
            "Default": {
                "title": "#4a90e2",
                "background": "#ecf0f1",
                "text": "#2c3e50",
                "border": "#bdc3c7"
            },
            "Dark Blue": {
                "title": "#2c3e50",
                "background": "#34495e",
                "text": "#ecf0f1",
                "border": "#4a90e2"
            },
            "Dark Gray": {
                "title": "#555555",
                "background": "#333333",
                "text": "#ffffff",
                "border": "#777777"
            },
            "Green Theme": {
                "title": "#27ae60",
                "background": "#2ecc71",
                "text": "#ffffff",
                "border": "#16a085"
            },
            "Purple Theme": {
                "title": "#8e44ad",
                "background": "#9b59b6",
                "text": "#ffffff",
                "border": "#e74c3c"
            },
            "Orange Theme": {
                "title": "#e67e22",
                "background": "#f39c12",
                "text": "#ffffff",
                "border": "#d35400"
            }
        }

        if theme_name in themes:
            theme = themes[theme_name]
            self.title_color = theme["title"]
            self.bg_color = theme["background"]
            self.text_color = theme["text"]
            border_color = theme["border"]
            self.applyCustomStyles(border_color)

    def chooseTitleColor(self):
        color = QColorDialog.getColor(QColor(self.title_color), self)
        if color.isValid():
            self.title_color = color.name()
            self.applyCustomStyles()

    def chooseBgColor(self):
        color = QColorDialog.getColor(QColor(self.bg_color), self)
        if color.isValid():
            self.bg_color = color.name()
            self.applyCustomStyles()

    def chooseTextColor(self):
        color = QColorDialog.getColor(QColor(self.text_color), self)
        if color.isValid():
            self.text_color = color.name()
            self.applyCustomStyles()

    def applyCustomStyles(self, border_color=None):
        """Apply custom styles to the MDI area."""
        if border_color is None:
            border_color = self.title_color

        # Comprehensive MDI styling
        style = f"""
        QMdiArea {{
            background-color: {self.bg_color};
            border: 2px solid {border_color};
        }}

        QMdiArea QScrollBar:vertical {{
            background-color: {self.bg_color};
            width: 12px;
            border: 1px solid {border_color};
        }}

        QMdiArea QScrollBar::handle:vertical {{
            background-color: {self.title_color};
            border-radius: 6px;
            min-height: 20px;
        }}

        QMdiArea QScrollBar::handle:vertical:hover {{
            background-color: {self.text_color};
        }}

        QMdiSubWindow {{
            border: 2px solid {border_color};
            border-radius: 5px;
        }}

        QMdiSubWindow::title {{
            background-color: {self.title_color};
            color: {self.text_color};
            font-weight: bold;
            font-size: 12px;
            padding: 5px;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
        }}

        QMdiSubWindow::title:hover {{
            background-color: {self._lighten_color(self.title_color, 20)};
        }}

        QMdiSubWindow::title:selected {{
            background-color: {self._lighten_color(self.title_color, 10)};
        }}

        /* Window control buttons */
        QMdiSubWindow QAbstractButton {{
            background-color: transparent;
            color: {self.text_color};
            border: none;
            padding: 2px;
            margin: 1px;
        }}

        QMdiSubWindow QAbstractButton:hover {{
            background-color: {self._lighten_color(self.title_color, 30)};
            border-radius: 3px;
        }}

        QMdiSubWindow QAbstractButton:pressed {{
            background-color: {self._darken_color(self.title_color, 20)};
        }}

        /* Inactive window styling */
        QMdiSubWindow:!active {{
            opacity: 0.8;
        }}

        QMdiSubWindow:!active::title {{
            background-color: {self._darken_color(self.title_color, 30)};
            color: {self._darken_color(self.text_color, 30)};
        }}
        """

        self.mdi_area.setStyleSheet(style)
        self.colorChanged.emit()

    def _lighten_color(self, color_str, percentage):
        """Lighten a color by a percentage."""
        try:
            color = QColor(color_str)
            h, s, l, a = color.getHsl()
            l = min(255, int(l + (255 - l) * percentage / 100))
            color.setHsl(h, s, l, a)
            return color.name()
        except:
            return color_str

    def _darken_color(self, color_str, percentage):
        """Darken a color by a percentage."""
        try:
            color = QColor(color_str)
            h, s, l, a = color.getHsl()
            l = max(0, int(l - l * percentage / 100))
            color.setHsl(h, s, l, a)
            return color.name()
        except:
            return color_str


class MdiExample(QMainWindow):
    """Example application demonstrating MDI customization."""

    def __init__(self):
        super().__init__()
        self.window_counter = 0
        self.setupUI()


    def setupUI(self):
        self.setWindowTitle("Custom MDI Colors - Linux Mint Compatible")
        self.setGeometry(100, 100, 1000, 700)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create MDI Area
        self.mdi_area = QMdiArea()
        self.mdi_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdi_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Color customizer
        self.color_customizer = ColorCustomizer(self.mdi_area)
        layout.addWidget(self.color_customizer)

        # Control buttons
        button_layout = QHBoxLayout()

        add_window_btn = QPushButton("Add Window")
        add_window_btn.clicked.connect(self.addSubWindow)

        cascade_btn = QPushButton("Cascade")
        cascade_btn.clicked.connect(self.mdi_area.cascadeSubWindows)

        tile_btn = QPushButton("Tile")
        tile_btn.clicked.connect(self.mdi_area.tileSubWindows)

        close_all_btn = QPushButton("Close All")
        close_all_btn.clicked.connect(self.mdi_area.closeAllSubWindows)

        button_layout.addWidget(add_window_btn)
        button_layout.addWidget(cascade_btn)
        button_layout.addWidget(tile_btn)
        button_layout.addWidget(close_all_btn)
        button_layout.addStretch()

        layout.addLayout(button_layout)
        layout.addWidget(self.mdi_area)

        # Apply initial theme
        self.color_customizer.applyTheme("Dark Blue")

        # Add some initial windows
        for i in range(3):
            self.addSubWindow()

    def addSubWindow(self):
        """Add a new sub window to the MDI area."""
        self.window_counter += 1

        # Create content for the sub window
        text_edit = QTextEdit()
        text_edit.setPlainText(f"""This is Sub Window {self.window_counter}

You can:
- Change title bar colors using the controls above
- Resize and move windows
- Try different themes
- Customize individual colors

Linux Mint styling is fully supported!
""")

        # Create sub window
        sub_window = CustomMdiSubWindow()
        sub_window.setWidget(text_edit)
        sub_window.setWindowTitle(f"Document {self.window_counter}")
        sub_window.resize(300, 200)

        # Add to MDI area
        self.mdi_area.addSubWindow(sub_window)
        sub_window.show()


def main():
    app = QApplication(sys.argv)

    # Set application style for better Linux Mint compatibility
    app.setStyle('Fusion')  # Works well on Linux

    window = MdiExample()
    window.show()

    print("MDI Color Customization Demo")
    print("- Use the theme dropdown to apply predefined themes")
    print("- Click color buttons to customize individual colors")
    print("- Add/remove windows to test the styling")
    print("- Optimized for Linux Mint!")

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()