import sys

from PyQt5.QtGui import QTextCursor, QTextDocument
from PyQt5.QtWidgets import (QApplication,
                             QHBoxLayout,
                             QLineEdit,
                             QPushButton,
                             QTextEdit,
                             QVBoxLayout,
                             QWidget)


class TextSearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text Search")
        self.setGeometry(300, 300, 400, 300)

        # Widgets
        self.text_edit = QTextEdit()
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Enter search text")

        # Buttons
        self.down_button = QPushButton("Down")
        self.down_button.clicked.connect(self.search_down)

        self.up_button = QPushButton("Up")
        self.up_button.clicked.connect(self.search_up)

        # Layouts
        self.layout = QVBoxLayout()
        self.controls_layout = QHBoxLayout()

        self.controls_layout.addWidget(self.line_edit)
        self.controls_layout.addWidget(self.up_button)
        self.controls_layout.addWidget(self.down_button)

        self.layout.addWidget(self.text_edit)
        self.layout.addLayout(self.controls_layout)
        self.setLayout(self.layout)

        # State variable to track search position
        self.last_position = 0

    def search_down(self):
        search_text = self.line_edit.text()
        if search_text:
            cursor = self.text_edit.textCursor()
            cursor.setPosition(self.last_position)
            found = self.text_edit.find(search_text)

            if found:
                self.last_position = self.text_edit.textCursor().position()
            else:
                # Reset position if end is reached and no match
                self.last_position = 0

    def search_up(self):
        search_text = self.line_edit.text()
        if search_text:
            cursor = self.text_edit.textCursor()
            cursor.setPosition(self.last_position)
            # Use QTextDocument.FindBackward for backward search
            found = self.text_edit.find(search_text, QTextDocument.FindBackward)

            if found:
                self.last_position = self.text_edit.textCursor().position()
            else:
                # Reset position if start is reached and no match
                self.last_position = self.text_edit.document().characterCount()

# Run the app
app = QApplication(sys.argv)
window = TextSearchApp()
window.show()
sys.exit(app.exec_())
