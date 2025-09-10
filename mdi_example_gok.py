

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QMdiSubWindow, QTextEdit
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MDI Application with Custom Colors")
        self.setGeometry(100, 100, 800, 600)

        # Create MDI Area
        self.mdi_area = QMdiArea()
        self.setCentralWidget(self.mdi_area)

        # Apply stylesheet to QMdiArea for background color
        self.mdi_area.setStyleSheet("""
            QMdiArea {
                background-color: #2E2E2E; /* Dark background for MDI area */
            }
        """)

        # Create and add multiple subwindows
        for i in range(3):
            subwindow = QMdiSubWindow()
            subwindow.setWidget(QTextEdit())
            subwindow.setWindowTitle(f"Subwindow {i+1}")
            self.mdi_area.addSubWindow(subwindow)

            # Ensure Qt handles styling to avoid window manager interference
            subwindow.setAttribute(Qt.WA_StyledBackground, True)

            # Apply stylesheet to QMdiSubWindow for title bar and frame
            subwindow.setStyleSheet("""
                QMdiSubWindow {
                    background-color: #333333; /* Subwindow background */
                    border: 1px solid #555555; /* Subwindow border */
                }
                QMdiSubWindow:title {
                    background-color: #2196F3; /* Active title bar color (blue) */
                    color: white; /* Title text color */
                    padding: 5px; /* Padding for title bar */
                }
                QMdiSubWindow:!focus:title {
                    background-color: #666666; /* Inactive title bar color (gray) */
                    color: white;
                }
            """)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Set Fusion style for consistent look on Linux Mint
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())