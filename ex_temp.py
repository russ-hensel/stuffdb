#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# ---- what
"""
view and update a single table, as a table layout
       QSqlTableModel -> QTableView()

ex_qt_table_model.py

"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget, QMessageBox, QPushButton, QHBoxLayout
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlTableModel, QSqlQuery
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self._build_gui()

    def _build_gui(self):
        self.setWindowTitle('Photo Viewer and Editor')

        # Create a widget for the window contents
        self.widget = QWidget()
        self.setCentralWidget(self.widget)

        # Set up the layout
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)

        # Create and set up the table views

        self.edit_view  = QTableView()
        self.layout.addWidget(self.edit_view)

        # Set up the database connection
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName( '/mnt/WIN_D/Russ/0000/python00/python3/_projects/stuff_db_qt/data/appdb.db' )

        if not self.db.open():
            QMessageBox.critical(self, "Database Error", self.db.lastError().text())
            return



        # Set up the table model for editing
        self.edit_model = QSqlTableModel( self, self.db )
        self.edit_model.setTable("photoshow_photo")
        self.edit_model.setEditStrategy(QSqlTableModel.OnManualSubmit)


        self.edit_model.setFilter( "photoshow_id = 29 " )

        #model.setFilter(f'photoshow.id = {photoshow_id}')

        # Set the sort order
        column_to_sort_by   = 0  # Index of the column to sort by (e.g., 0 for the first column)
        sort_order          = Qt.AscendingOrder  # or Qt.DescendingOrder
        self.edit_model.setSort(column_to_sort_by, sort_order)

        msg       = f"{self.edit_model.selectStatement()}"
        print( msg )

        self.edit_model.select()

        # Set the model to the edit view
        self.edit_view.setModel( self.edit_model )

        # Create and set up the buttons for adding, deleting, and submitting changes
        self.add_button    = QPushButton("Add Entry")
        self.delete_button = QPushButton("Delete Entry")
        self.submit_button = QPushButton("Submit Changes")

        self.add_button.clicked.connect(self.add_entry)
        self.delete_button.clicked.connect(self.delete_entry)
        self.submit_button.clicked.connect(self.submit_changes)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.submit_button)


        button    = QPushButton("id = 29")
        button.clicked.connect( self.select_29 )
        button_layout.addWidget( button )

        button = QPushButton("id = 129")
        button.clicked.connect( self.select_129 )
        button_layout.addWidget( button )


        self.layout.addLayout(button_layout)

    def add_entry(self):
        self.edit_model.insertRow(self.edit_model.rowCount())

    def delete_entry(self):
        index = self.edit_view.currentIndex()
        if index.isValid():
            self.edit_model.removeRow(index.row())

    def submit_changes(self):
        if not self.edit_model.submitAll():
            QMessageBox.critical(self, "Submit Error", self.edit_model.lastError().text())
        else:
            self.edit_model.select()  # Refresh the model to show changes


    def select_29(self, ):
        """
        these should be partials in good code
        """
        self.select_by_id( 29 )

    def select_129(self, ):
        """
        """
        self.select_by_id( 129 )

    def select_by_id(self, id):
        """
        this will select with sql
        which will be modified
        seems to work
        """
        print( f"select_by_id  {id = }")

        self.edit_model.setFilter( f"photoshow_id = {id} " )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


