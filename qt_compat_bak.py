"""
qt_compat.py — Seamless PyQt5 / PyQt6 compatibility layer.

Usage:
    from qt_compat import PyQt, QApplication, QWidget, QAction, QActionGroup, exec_app
    from PyQt.QtWidgets import QMainWindow, QToolBar, QMessageBox
"""

import sys

# --- Import PyQt6 if available, else PyQt5 ---
try:
    import PyQt6 as PyQt
    from PyQt6 import QtCore, QtGui, QtWidgets, QtSql, QtPrintSupport
    from PyQt6.QtWidgets import QApplication, QWidget
    from PyQt6.QtWidgets  import QComboBox
    qt_version = 6



except ImportError:
    import PyQt5 as PyQt
    from PyQt5 import QtCore, QtGui, QtWidgets, QtSql, QtPrintSupport
    from PyQt5.QtWidgets import QApplication, QWidget
    from PyQt5.QtWidgets import QComboBox
    qt_version = 5



# --- Inject PyQt namespaces into sys.modules for normal imports ---
sys.modules["PyQt"] = PyQt
sys.modules["PyQt.QtCore"] = QtCore
sys.modules["PyQt.QtGui"] = QtGui
sys.modules["PyQt.QtWidgets"] = QtWidgets
sys.modules["PyQt.QtSql"] = QtSql
sys.modules["PyQt.QtPrintSupport"] = QtPrintSupport

# --- Normalize exec/app differences ---
exec_app = QApplication.exec if qt_version == 6 else QApplication.exec_

# --- Unified Qt reference ---
Qt = QtCore.Qt

# --- Alignment flags ---
AlignCenter = Qt.AlignmentFlag.AlignCenter if qt_version == 6 else Qt.AlignCenter
AlignLeft   = Qt.AlignmentFlag.AlignLeft if qt_version == 6 else Qt.AlignLeft
AlignRight  = Qt.AlignmentFlag.AlignRight if qt_version == 6 else Qt.AlignRight
AlignTop    = Qt.AlignmentFlag.AlignTop if qt_version == 6 else Qt.AlignTop
AlignBottom = Qt.AlignmentFlag.AlignBottom if qt_version == 6 else Qt.AlignBottom

# --- Orientation ---
Horizontal          = Qt.Orientation.Horizontal if qt_version == 6 else Qt.Horizontal
Vertical            = Qt.Orientation.Vertical if qt_version == 6 else Qt.Vertical

# --- ItemDataRole / CheckStateRole ---
DisplayRole         = Qt.ItemDataRole.DisplayRole if qt_version == 6 else Qt.DisplayRole
EditRole            = Qt.ItemDataRole.EditRole if qt_version == 6 else Qt.EditRole
CheckStateRole      = Qt.ItemDataRole.CheckStateRole if qt_version == 6 else Qt.CheckStateRole
TextAlignmentRole   = Qt.ItemDataRole.TextAlignmentRole if qt_version == 6 else Qt.TextAlignmentRole
WindowMaximized     = Qt.WindowState.WindowMaximized if qt_version == 6 else Qt.WindowMaximized
NoInsert            = QComboBox.InsertPolicy.NoInsert if qt_version == 6 else QComboBox.NoInsert



Checked         = QtCore.Qt.CheckState.Checked if qt_version == 6 else Qt.Checked
Unchecked       = QtCore.Qt.CheckState.Unchecked if qt_version == 6 else Qt.Unchecked
PartiallyChecked= QtCore.Qt.CheckState.PartiallyChecked if qt_version == 6 else Qt.PartiallyChecked

# --- Helper for moved classes (QtGui ↔ QtWidgets) ---
def _compat_class(gui_cls, widgets_cls):
    """Return QtGui.class if available, else QtWidgets.class."""
    try:
        return getattr(QtGui, gui_cls)
    except AttributeError:
        return getattr(QtWidgets, widgets_cls)

QAction        = _compat_class("QAction", "QAction")
QActionGroup   = _compat_class("QActionGroup", "QActionGroup")
QShortcut      = _compat_class("QShortcut", "QShortcut")
QKeySequence   = _compat_class("QKeySequence", "QKeySequence")
QTextCursor    = _compat_class("QTextCursor", "QTextCursor")

# --- setIconVisibleInMenu workaround ---
def set_icon_visible_in_menu(action, visible=True):
    if qt_version == 5:
        action.setIconVisibleInMenu(visible)
    # PyQt6 removed it, so noop

# --- Convenience factory for QAction ---
def make_action(text, icon=None, parent=None, shortcut=None, triggered=None):
    act = QAction(text, parent)
    if icon:
        act.setIcon(icon)
    if shortcut:
        act.setShortcut(shortcut)
    if triggered:
        act.triggered.connect(triggered)
    set_icon_visible_in_menu(act, True)
    return act

# --- Exported names ---
__all__ = [
    "PyQt", "qt_version", "Qt",
    "QApplication", "QWidget",
    "QAction", "QActionGroup", "QShortcut", "QKeySequence", "QTextCursor",
    "exec_app", "AlignCenter", "AlignLeft", "AlignRight", "AlignTop", "AlignBottom",
    "Horizontal", "Vertical",
    "DisplayRole", "EditRole", "CheckStateRole",
    "Checked", "Unchecked", "PartiallyChecked",
    "set_icon_visible_in_menu", "make_action"
]
