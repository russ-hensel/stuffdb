#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 19 08:48:24 2025

from grok works --- move to qt examples
"""


# ---- tof

# ---- imports

# ---- end imports


#-------------------------------






# ---- eof

from PyQt5 import QtCore, QtWidgets, QtSql
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget, QMenu
from PyQt5.QtCore   import Qt
import sys


# -------------------------------
def table_widget_no_edit( table_widget ):
    """
    think makes all of a table widget non editable
    from chat
    take a table widget Q..... what  maybe descendants of abstract
    and make it non editable
    .... put this in examples
    """
    table = table_widget
    for row in range(table.rowCount()):
        for column in range(table.columnCount()):
            item = table.item(row, column)
            if item is not None:
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)







class DatabaseCopyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.src_db = "file_src.db"
        self.dest_db = "file_dest.db"
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Database Table Copy")
        self.setFixedSize(400, 300)  # Adjusted for table visibility

        # Create layout
        layout = QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)

        # Create table
        columns = ["id", "id_old", "type", "sub_system", "system"]  # Example columns from help_info
        self.history_table = QTableWidget(0, len(columns), self)
        self.history_table.setHorizontalHeaderLabels(columns)
        self.history_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.history_table.customContextMenuRequested.connect(self.show_context_menu)

        # ---- will this stop the context menu? no it does not no they are fine
        widget     = self.history_table
        table_widget_no_edit( widget )
        widget.setSelectionBehavior( QTableWidget.SelectRows )  # Select entire rows

        # Add widgets to layout
        self.copy_button = QPushButton("Copy Table Data")
        self.status_label = QLabel("Click the button to copy data")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.history_table)
        layout.addWidget(self.copy_button)
        layout.addWidget(self.status_label)

        # Connect button
        self.copy_button.clicked.connect(self.copy_table_data)

        # Set layout
        self.setLayout(layout)

        # Optional: Populate table for testing
        self.populate_table()

    def populate_table(self):
        # Add sample data to make table interactive
        self.history_table.setRowCount(2)
        for row in range(2):
            for col in range(self.history_table.columnCount()):
                item = QtWidgets.QTableWidgetItem(f"Row {row}, Col {col}")
                self.history_table.setItem(row, col, item)
        self.history_table.resizeColumnsToContents()

    def show_context_menu(self, pos):
        """
        Show context menu for history_table
        """
        menu = QMenu(self.history_table)
        action = menu.addAction("Test Action")
        action.setEnabled(True)
        action.triggered.connect(lambda: self.status_label.setText("Test Action Triggered"))
        menu.addSeparator()
        menu.addAction("Clear Table", lambda: self.history_table.setRowCount(0))
        menu.exec_(self.history_table.mapToGlobal(pos))

    def copy_table_data(self):
        self.status_label.setText("Copying... (implement QSqlQuery logic here)")

def main():
    app = QApplication(sys.argv)
    window = DatabaseCopyApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()