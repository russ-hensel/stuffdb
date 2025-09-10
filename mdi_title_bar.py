import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMdiArea, QMdiSubWindow,
                            QTextEdit, QVBoxLayout, QWidget, QPushButton, QHBoxLayout,
                            QLabel, QCheckBox, QSpinBox, QComboBox)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QEvent
from PyQt5.QtGui import QMouseEvent


class CustomMdiSubWindow(QMdiSubWindow):
    """Custom QMdiSubWindow with enhanced title bar behavior control."""

    # Custom signals
    titleDoubleClicked = pyqtSignal()
    titleSingleClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Behavior control flags
        self.double_click_maximizes = True
        self.custom_behavior_enabled = False
        self.click_timer = QTimer()
        self.click_timer.setSingleShot(True)
        self.click_timer.timeout.connect(self.handleSingleClick)
        self.click_count = 0

        # Connect our custom signals
        self.titleDoubleClicked.connect(self.onTitleDoubleClick)
        self.titleSingleClicked.connect(self.onTitleSingleClick)

    def setDoubleClickBehavior(self, maximize=True, custom_enabled=False):
        """Control double-click behavior on title bar."""
        self.double_click_maximizes = maximize
        self.custom_behavior_enabled = custom_enabled

        if not maximize:
            # Disable the built-in maximize behavior
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

    def mouseDoubleClickEvent(self, event):
        """Handle double-click events on the window."""
        if event.button() == Qt.LeftButton:
            # Check if the double-click is on the title bar area
            if self.isInTitleBar(event.pos()):
                if self.custom_behavior_enabled:
                    self.titleDoubleClicked.emit()
                    event.accept()
                    return
                elif not self.double_click_maximizes:
                    # Prevent default maximize behavior
                    event.accept()
                    return

        # Default behavior for other cases
        super().mouseDoubleClickEvent(event)

    def mousePressEvent(self, event):
        """Handle single click detection with timer."""
        if event.button() == Qt.LeftButton and self.isInTitleBar(event.pos()):
            self.click_count += 1
            if self.click_count == 1:
                # Start timer for single click detection
                self.click_timer.start(QApplication.doubleClickInterval())

        super().mousePressEvent(event)

    def handleSingleClick(self):
        """Handle single click after timer expires."""
        if self.click_count == 1:
            self.titleSingleClicked.emit()
        self.click_count = 0

    def isInTitleBar(self, pos):
        """Check if position is within the title bar area."""
        # This is an approximation - the title bar is typically at the top
        title_height = self.style().pixelMetric(self.style().PM_TitleBarHeight)
        return pos.y() <= title_height and pos.x() >= 0 and pos.x() <= self.width()

    def onTitleDoubleClick(self):
        """Custom double-click handler."""
        print(f"Custom double-click on '{self.windowTitle()}'")

        # Example custom behaviors
        if hasattr(self, 'custom_action'):
            if self.custom_action == "minimize":
                self.showMinimized()
            elif self.custom_action == "close":
                self.close()
            elif self.custom_action == "resize":
                current_size = self.size()
                if current_size.width() < 600:
                    self.resize(800, 600)
                else:
                    self.resize(400, 300)
            elif self.custom_action == "toggle_maximize":
                if self.isMaximized():
                    self.showNormal()
                else:
                    self.showMaximized()

    def onTitleSingleClick(self):
        """Custom single-click handler."""
        print(f"Single click on '{self.windowTitle()}'")


class TitleBarBehaviorDemo(QMainWindow):
    """Demo showing different title bar behaviors."""

    def __init__(self):
        super().__init__()
        self.setupUI()
        self.window_counter = 0

    def setupUI(self):
        self.setWindowTitle("MDI Title Bar Behavior Demo")
        self.setGeometry(100, 100, 1200, 800)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create MDI Area (replace the None placeholder)
        self.mdi_area = QMdiArea()

        # Now create control panel (which may reference self.mdi_area)
        control_panel = self.createControlPanel()
        layout.addWidget(control_panel)

        # Add MDI Area to layout
        layout.addWidget(self.mdi_area)

        # Create demo windows
        self.createDemoWindows()

    def createControlPanel(self):
        """Create the control panel for testing different behaviors."""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Title
        title_label = QLabel("Title Bar Double-Click Behavior Control")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; margin: 5px;")
        layout.addWidget(title_label)

        # Controls row 1
        row1 = QHBoxLayout()

        self.enable_default_cb = QCheckBox("Enable Default Maximize")
        self.enable_default_cb.setChecked(True)
        self.enable_default_cb.toggled.connect(self.updateBehavior)

        self.enable_custom_cb = QCheckBox("Enable Custom Behavior")
        self.enable_custom_cb.toggled.connect(self.updateBehavior)

        self.custom_action_combo = QComboBox()
        self.custom_action_combo.addItems([
            "toggle_maximize", "minimize", "close", "resize"
        ])
        self.custom_action_combo.currentTextChanged.connect(self.updateCustomAction)

        row1.addWidget(QLabel("Behavior:"))
        row1.addWidget(self.enable_default_cb)
        row1.addWidget(self.enable_custom_cb)
        row1.addWidget(QLabel("Custom Action:"))
        row1.addWidget(self.custom_action_combo)
        row1.addStretch()

        # Controls row 2
        row2 = QHBoxLayout()

        add_window_btn = QPushButton("Add Window")
        add_window_btn.clicked.connect(self.addWindow)

        cascade_btn = QPushButton("Cascade")
        cascade_btn.clicked.connect(self.mdi_area.cascadeSubWindows)

        tile_btn = QPushButton("Tile")
        tile_btn.clicked.connect(self.mdi_area.tileSubWindows)

        test_behavior_btn = QPushButton("Test Current Behavior")
        test_behavior_btn.clicked.connect(self.testBehavior)

        row2.addWidget(add_window_btn)
        row2.addWidget(cascade_btn)
        row2.addWidget(tile_btn)
        row2.addWidget(test_behavior_btn)
        row2.addStretch()

        layout.addLayout(row1)
        layout.addLayout(row2)

        # Info panel
        info_label = QLabel("""
<b>How MDI Title Bar Double-Click Works:</b><br>
• <b>Default Qt Behavior:</b> Double-click toggles between maximized and normal size<br>
• <b>Built-in Method:</b> QMdiSubWindow handles this automatically via mouseDoubleClickEvent<br>
• <b>Window States:</b> Uses showMaximized()/showNormal() internally<br>
• <b>Customization:</b> Override mouseDoubleClickEvent() to implement custom behavior<br>
• <b>Detection:</b> Must check if click is within title bar area<br><br>
<b>Try:</b> Create windows, change settings above, then double-click title bars to test!
        """)
        info_label.setStyleSheet("background-color: #f0f0f0; padding: 10px; border-radius: 5px;")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        return panel

    def createDemoWindows(self):
        """Create initial demo windows."""
        behaviors = [
            ("Default Behavior", True, False, "toggle_maximize"),
            ("Custom Resize", False, True, "resize"),
            ("Custom Minimize", False, True, "minimize")
        ]

        for title, default_max, custom_enabled, custom_action in behaviors:
            self.addWindow(title, default_max, custom_enabled, custom_action)

    def addWindow(self, title=None, default_maximize=None, custom_enabled=None, custom_action=None):
        """Add a new MDI sub window."""
        self.window_counter += 1

        if title is None:
            title = f"Document {self.window_counter}"

        if default_maximize is None:
            default_maximize = self.enable_default_cb.isChecked()

        if custom_enabled is None:
            custom_enabled = self.enable_custom_cb.isChecked()

        if custom_action is None:
            custom_action = self.custom_action_combo.currentText()

        # Create content
        text_edit = QTextEdit()
        text_edit.setPlainText(f"""Window: {title}
Counter: {self.window_counter}

Double-Click Behavior:
- Default Maximize: {default_maximize}
- Custom Enabled: {custom_enabled}
- Custom Action: {custom_action}

Current State: Normal
Size: {text_edit.size()}

Try double-clicking the title bar!

Technical Details:
- Qt handles title bar detection automatically
- mouseDoubleClickEvent() is called on double-click
- Window state changes via showMaximized()/showNormal()
- Custom behavior requires event interception
- Title bar area detection uses style metrics
""")

        # Create sub window
        sub_window = CustomMdiSubWindow()
        sub_window.setWidget(text_edit)
        sub_window.setWindowTitle(title)
        sub_window.resize(350, 250)

        # Configure behavior
        sub_window.setDoubleClickBehavior(default_maximize, custom_enabled)
        sub_window.custom_action = custom_action

        # Connect signals for demo
        sub_window.titleDoubleClicked.connect(
            lambda: self.logEvent(f"Custom double-click: {sub_window.windowTitle()}")
        )
        sub_window.titleSingleClicked.connect(
            lambda: self.logEvent(f"Single click: {sub_window.windowTitle()}")
        )

        # Add to MDI area
        self.mdi_area.addSubWindow(sub_window)
        sub_window.show()

        self.logEvent(f"Created window: {title} (Default: {default_maximize}, Custom: {custom_enabled})")

    def updateBehavior(self):
        """Update behavior for all existing windows."""
        for sub_window in self.mdi_area.subWindowList():
            if isinstance(sub_window, CustomMdiSubWindow):
                sub_window.setDoubleClickBehavior(
                    self.enable_default_cb.isChecked(),
                    self.enable_custom_cb.isChecked()
                )

        self.logEvent(f"Updated all windows - Default: {self.enable_default_cb.isChecked()}, Custom: {self.enable_custom_cb.isChecked()}")

    def updateCustomAction(self, action):
        """Update custom action for all windows."""
        for sub_window in self.mdi_area.subWindowList():
            if isinstance(sub_window, CustomMdiSubWindow):
                sub_window.custom_action = action

        self.logEvent(f"Updated custom action to: {action}")

    def testBehavior(self):
        """Simulate double-click on active window."""
        active_window = self.mdi_area.activeSubWindow()
        if active_window and isinstance(active_window, CustomMdiSubWindow):
            active_window.titleDoubleClicked.emit()
            self.logEvent(f"Simulated double-click on: {active_window.windowTitle()}")
        else:
            self.logEvent("No active window to test")

    def logEvent(self, message):
        """Log events to console and status."""
        print(f"[MDI Demo] {message}")
        self.statusBar().showMessage(message, 3000)


def main():
    app = QApplication(sys.argv)

    # Set double-click interval for testing
    app.setDoubleClickInterval(500)  # 500ms

    window = TitleBarBehaviorDemo()
    window.show()

    print("MDI Title Bar Behavior Demo")
    print("=" * 50)
    print("Default Qt Behavior:")
    print("- Double-click title bar toggles maximize/restore")
    print("- Handled automatically by QMdiSubWindow")
    print("- Uses mouseDoubleClickEvent() internally")
    print()
    print("Custom Behavior Options:")
    print("- Override mouseDoubleClickEvent()")
    print("- Check if click is in title bar area")
    print("- Implement custom actions")
    print()
    print("Try different settings and double-click title bars!")

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()