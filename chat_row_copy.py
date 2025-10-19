#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 19 09:22:22 2025

grok

if button works, do not know how but context menu ok



"""


# ---- tof




#-------------------------------





# ---- imports



from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget, QMenu
import sys

# ---- end imports


class DatabaseCopyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.src_db = "file_src.db"
        self.dest_db = "file_dest.db"
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Database Table Copy")
        self.setFixedSize(600, 400)  # Adjusted for two tables

        layout = QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)

        # Define columns (same for both tables, from help_info)
        columns = ["id", "id_old", "type", "sub_system", "system"]

        # Create first table
        self.table_one = QTableWidget(0, len(columns), self)
        self.table_one.setHorizontalHeaderLabels(columns)
        self.table_one.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_one.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.table_one.customContextMenuRequested.connect(self.show_context_menu_one)

        # Create second table
        self.table_two = QTableWidget(0, len(columns), self)
        self.table_two.setHorizontalHeaderLabels(columns)
        self.table_two.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        # Add widgets to layout
        self.copy_button = QPushButton("use context menu button seems not to work")
        self.status_label = QLabel("Select a row in Table 1 to copy")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(QLabel("Table 1 (Source)"))
        layout.addWidget(self.table_one)
        layout.addWidget(QLabel("Table 2 (Destination)"))
        layout.addWidget(self.table_two)
        layout.addWidget(self.copy_button)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

        # Populate tables for testing
        self.populate_tables()

    def populate_tables(self):
        # Populate table_one with sample data
        self.table_one.setRowCount(3)
        for row in range(3):
            for col in range(self.table_one.columnCount()):
                item = QtWidgets.QTableWidgetItem(f"Row {row}, Col {col}")
                self.table_one.setItem(row, col, item)
        self.table_one.resizeColumnsToContents()

        # Populate table_two with some rows
        self.table_two.setRowCount(2)
        for row in range(2):
            for col in range(self.table_two.columnCount()):
                item = QtWidgets.QTableWidgetItem(f"Dest Row {row}, Col {col}")
                self.table_two.setItem(row, col, item)
        self.table_two.resizeColumnsToContents()

    def copy_row(self, ix_table_one, ix_table_two):
        """
        Copy data from row ix_table_one in table_one to row ix_table_two in table_two
        """
        if ix_table_one < 0 or ix_table_one >= self.table_one.rowCount():
            self.status_label.setText(f"Invalid source row: {ix_table_one}")
            return
        if ix_table_two < 0 or ix_table_two >= self.table_two.rowCount():
            self.status_label.setText(f"Invalid destination row: {ix_table_two}")
            return

        # Copy each cell from source row to destination row
        for col in range(self.table_one.columnCount()):
            source_item = self.table_one.item(ix_table_one, col)
            text = source_item.text() if source_item else ""
            # Create or update item in table_two
            dest_item = self.table_two.item(ix_table_two, col)
            if not dest_item:
                dest_item = QtWidgets.QTableWidgetItem()
                self.table_two.setItem(ix_table_two, col, dest_item)
            dest_item.setText(text)

        self.status_label.setText(f"Copied row {ix_table_one} to row {ix_table_two}")

    def show_context_menu_one(self, pos):
        """
        Context menu for table_one to select row and copy to table_two
        """
        menu = QMenu(self.table_one)
        current_row = self.table_one.currentRow()

        if current_row >= 0:
            # Add actions to copy to specific rows in table_two
            for row in range(self.table_two.rowCount()):
                menu.addAction(f"Copy to Table 2, Row {row}",
                              lambda r=row: self.copy_row(current_row, r))
        else:
            action = menu.addAction("No row selected")
            action.setEnabled(False)

        menu.addSeparator()
        menu.addAction("Clear Table 1", lambda: self.table_one.setRowCount(0))
        menu.exec_(self.table_one.mapToGlobal(pos))

    def copy_table_data(self):
        self.status_label.setText("Copying... (implement QSqlQuery logic here)")

def main():
    app = QApplication(sys.argv)
    window = DatabaseCopyApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

# ---- eof