#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 17 14:20:54 2025

@author: russ
"""


# ---- tof

# ---- imports

# ---- end imports


#-------------------------------

# I am working in python with qt5.  I would like a widget
# that lets the user enter a line of text and after the entry
# that line is saved so that the text can appear in a pop up
# list at a later time.

# I should be a subclass of QComboBox with text editing enabled.
# I am just interested in the sub class code, i do not need
# the whole context to run it.  Can you write this code?

# -------------- grock
# good so far, can you make sure it does not allow duplicate lines, and
# set a limit after which the oldest line ( at the bottom of the list )
# is deleted on each add

class EditableComboBox(QComboBox):
    def __init__(self, parent=None, max_items=10):
        super().__init__(parent)
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.InsertAtTop)
        self.max_items = max_items
        self.lineEdit().returnPressed.connect(self.addCurrentText)

    def addCurrentText(self):
        text = self.lineEdit().text().strip()
        if text and text not in [self.itemText(i) for i in range(self.count())]:
            self.insertItem(0, text)
            self.setCurrentText(text)
            if self.count() > self.max_items:
                self.removeItem(self.count() - 1)



# ----------------- claud   --- claud would seem to win


from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import Qt, pyqtSignal

from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import Qt, pyqtSignal

from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import Qt, pyqtSignal

class HistoryComboBox(QComboBox):
    """
    A QComboBox subclass that allows text entry and maintains a history of entered text.
    The history is presented as dropdown options when the user clicks the dropdown arrow.
    """

    textSubmitted = pyqtSignal(str)  # Signal emitted when text is submitted

    def __init__(self, parent=None, max_history=10):
        """
        Initialize the HistoryComboBox.

        Args:
            parent: Parent widget
            max_history: Maximum number of history items to store
        """
        super().__init__(parent)

        # Enable editing
        self.setEditable(True)

        # Set insert policy to not add duplicates automatically
        self.setInsertPolicy(QComboBox.NoInsert)

        # Store maximum history size
        self.max_history = max_history

        # Connect signals
        self.lineEdit().returnPressed.connect(self.add_current_text_to_history)

    def add_current_text_to_history(self):
        """Add the current text to the history if not empty and not a duplicate."""
        text = self.currentText().strip()

        if not text:
            return

        # Check if the text is already in the history
        index = self.findText(text)

        if index >= 0:
            # If it exists, remove it so we can add it to the top
            self.removeItem(index)

        # Insert at the beginning
        self.insertItem(0, text)

        # If we've exceeded the maximum history size, remove the oldest item
        if self.count() > self.max_history:
            self.removeItem(self.count() - 1)

        # Keep the current text instead of clearing it
        # Set the current index to -1 to ensure the text remains visible
        self.setCurrentIndex(-1)
        self.setCurrentText(text)

        # Emit signal with the submitted text
        self.textSubmitted.emit(text)

    def keyPressEvent(self, event):
        """
        Handle key press events to add text to history when Enter is pressed.
        """
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.add_current_text_to_history()

        # Pass the event to the parent class
        super().keyPressEvent(event)

    def get_history(self):
        """Get the current history as a list of strings."""
        return [self.itemText(i) for i in range(self.count())]

    def set_history(self, history_list):
        """Set the history from a list of strings."""
        self.clear()
        for item in reversed(history_list):
            if item.strip():
                self.addItem(item)

    def clear_history(self):
        """Clear the history."""
        self.clear()

    def get_text(self):
        """Get the current text in the edit field."""
        return self.currentText()

    def set_text(self, text, add_to_history=True):
        """
        Set the text in the edit field.

        Args:
            text: Text to set
            add_to_history: If True, also adds the text to history
        """
        if add_to_history and text.strip():
            # Temporarily store the text
            stored_text = text.strip()

            # Check if the text is already in the history
            index = self.findText(stored_text)

            if index >= 0:
                # If it exists, remove it so we can add it to the top
                self.removeItem(index)

            # Insert at the beginning
            self.insertItem(0, stored_text)

            # If we've exceeded the maximum history size, remove the oldest item
            if self.count() > self.max_history:
                self.removeItem(self.count() - 1)

            # Set the current index to -1 to show the text in the edit field
            # without selecting an item from the dropdown
            self.setCurrentIndex(-1)

            # Make sure the text is set correctly
            self.setCurrentText(stored_text)
        else:
            # Just set the text without adding to history
            self.setCurrentText(text)