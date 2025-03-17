#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 16:00:27 2025

@author: russ
"""


# ---- tof

# ---- imports

# ---- end imports


#-------------------------------






# ---- eof

from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PyQt5.QtCore import Qt, QModelIndex
import sys

# Custom model to control editability and alignment
class CustomSqlTableModel(QSqlTableModel):
    def __init__(self, parent=None, db=QSqlDatabase()):
        super().__init__(parent, db)
        # Specify multiple columns to make non-editable (e.g., columns 1 and 2)
        self.non_editable_columns = {0, 1, 2}  # Columns ....

    def flags(self, index: QModelIndex):
        # Get default flags from the base class
        flags = super().flags(index)
        # Remove editable flag for the specified columns
        if index.column() in self.non_editable_columns:
            return flags & ~Qt.ItemIsEditable  # Make these columns non-editable
        return flags

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        # Handle text alignment for specific columns (optional)
        if role == Qt.TextAlignmentRole:
            if index.column() == 0:  # Left-align column 0
                return Qt.AlignLeft | Qt.AlignVCenter
            elif index.column() == 1:  # Center-align column 1
                return Qt.AlignCenter | Qt.AlignVCenter
            elif index.column() == 2:  # Right-align column 2
                return Qt.AlignRight | Qt.AlignVCenter
        # Default to base class implementation for other roles
        return super().data(index, role)

def setup_database():
    # Set up in-memory SQLite database
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(":memory:")
    if not db.open():
        print("Failed to open database")
        sys.exit(-1)

    # Create a sample table and populate it
    query = QSqlQuery()
    query.exec_("""
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            salary REAL,
            department TEXT
        )
    """)

    # Insert sample data
    query.exec_("INSERT INTO employees (name, salary, department) VALUES ('Alice', 50000, 'HR')")
    query.exec_("INSERT INTO employees (name, salary, department) VALUES ('Bob', 60000, 'Engineering')")
    query.exec_("INSERT INTO employees (name, salary, department) VALUES ('Charlie', 75000, 'Sales')")

    return db

def main():
    app = QApplication(sys.argv)

    # Set up the database
    db = setup_database()

    # Create and set up the custom model
    model = CustomSqlTableModel(None, db)
    model.setTable("employees")
    model.select()  # Populate the model with data

    # Create the table view
    view = QTableView()
    view.setModel(model)

    # Set column widths (optional)
    view.setColumnWidth(0, 100)  # id
    view.setColumnWidth(1, 150)  # name
    view.setColumnWidth(2, 200)  # salary
    view.setColumnWidth(3, 150)  # department

    # Show the view
    view.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
