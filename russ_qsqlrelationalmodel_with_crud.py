#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 09:12:11 2024

@author: russ
"""

"""

I am using python with pyqt5.  Could you give me a brief tutorial, based around a
crud datbase application using QSqlRelationalTableModel and any closely related
qt objects.  Please include the code to generate an in memory sample database.

could you please add a bit of code for update and data validation and regenerate the example?

updated on submit all

in the code please make a comment for every method/function or leave
a pair of triple quotes for a comment to be added later


could we do another rewrite?  Assume the tables do not
use AUTOINCREMENT but use this class

class KeyGen():
    def __init__( self ):
        self.keys     = list( range( 100, 300 ))
        self.ix_keys  = -1
    def get_next_key( self, ):
        self.ix_keys  += 1
        return self.keys[ self.ix_keys ]

and gets keys with the get_next_key() method.  And assume
that the keys are generated at the end of an EditDialog

Please regenerate everything.






chat_qsqlrelationalmodel_with_crud.py

re-write in my style as  russ_qsqlrelationalmodel_with_crud.py


see also  crud_table_model_chat.py

"""


# ---- a few parameters
app_title   = "russ_qsqlrelationalmodel_with_crud.py"
db_file     = "texs_x.db"
db_file     = ':memory:'


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget, QPushButton, QLineEdit, QFormLayout, QDialog, QMessageBox, QComboBox
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlRelationalTableModel, QSqlRelation, QSqlRelationalDelegate
from PyQt5.QtCore import Qt

def create_connection_and_db():
    """
    uses key gen later but this is jus static

    """

    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName( db_file )
    if not db.open():
        print("Unable to establish a database connection.")
        return False

    query = QSqlDatabase.database().exec()

    # Create tables
    query.exec_("""CREATE TABLE department (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(20) NOT NULL)""")

    query.exec_("""CREATE TABLE employee (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    department_id INTEGER,
                    FOREIGN KEY (department_id) REFERENCES department(id))""")

    # Insert sample data
    query.exec_("INSERT INTO department (id, name) VALUES (100, 'HR')")
    query.exec_("INSERT INTO department (id, name) VALUES (101, 'Finance')")


    query.exec_("INSERT INTO employee (id, name, department_id) VALUES (200, 'Alice', 100)")
    query.exec_("INSERT INTO employee (id, name, department_id) VALUES (201, 'Bob', 101)")

    return True

# ---- end imports

class KeyGen():
    def __init__( self ):
        self.keys     = list( range( 2000, 5000 ))
        self.ix_keys  = -1
    def get_next_key( self, ):
        self.ix_keys  += 1
        return self.keys[ self.ix_keys ]


class EditDialog(QDialog):
    """
    what it says, read?
    seems to be used to edit and add
    it tells edit from add based on having an
    index -- index to model or an id think index

    """
    # ------------------------------------------
    def __init__(self, model, keygen, index=None, parent=None):
        super().__init__(parent)
        self.model          = model
        self.keygen         = keygen
        self.index          = index
        self.setWindowTitle("Edit Employee")


        self._build_gui()

        if index:
            self.load_data()  # at least some of gui has to be built

        self.populate_departments()

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says, read?
        """
        self.layout             = QFormLayout()
        self.name_edit          = QLineEdit()
        self.department_combo   = QComboBox()

        self.layout.addRow("Name:",         self.name_edit)
        self.layout.addRow("Department:",   self.department_combo)

        self.setLayout(self.layout)

        self.buttons            = QWidget()
        self.button_layout      = QVBoxLayout()

        # ---- buttons
        a_widget                = QPushButton("Save")
        self.save_button        = a_widget
        a_widget.clicked.connect(self.update_db)
        self.button_layout.addWidget( a_widget )

        # ----
        a_widget                = QPushButton("Cancel")
        self.cancel_button        = a_widget
        a_widget.clicked.connect(  self.reject )
        self.button_layout.addWidget( a_widget )


        self.buttons.setLayout(self.button_layout)

        self.layout.addRow(self.buttons)

    # ------------------------------------------
    def populate_departments(self):
        """
        what it says, read?
        """
        query = QSqlDatabase.database().exec("SELECT id, name FROM department")
        while query.next():
            self.department_combo.addItem(query.value(1), query.value(0))


    # ------------------------------------------
    def load_data(self):
        """
        what it says, read?
        """
        name = self.model.data(self.model.index(self.index.row(), 1))
        department_id = self.model.data(self.model.index(self.index.row(), 2))
        self.name_edit.setText(name)
        department_index = self.department_combo.findData(department_id)
        if department_index != -1:
            self.department_combo.setCurrentIndex(department_index)


    # ------------------------------------------
    def update_db(self):
        """
        what it says, read?
        """
        name = self.name_edit.text()
        department_id = self.department_combo.currentData()

        if not name:
            QMessageBox.warning(self, "Input Error", "Employee name cannot be empty.")
            return

        if self.index:
            self.model.setData(self.model.index(self.index.row(), 1), name)
            self.model.setData(self.model.index(self.index.row(), 2), department_id)
        else:
            key = self.keygen.get_next_key()
            self.model.insertRow(self.model.rowCount())
            self.model.setData(self.model.index(self.model.rowCount() - 1, 0), key)
            self.model.setData(self.model.index(self.model.rowCount() - 1, 1), name)
            self.model.setData(self.model.index(self.model.rowCount() - 1, 2), department_id)

        self.model.submitAll()  # Submit changes to the database
        self.accept()

# ------------------------------------------
class EditDialogxxx( QDialog ):
    def __init__(self, model, index=None, parent=None):
        """
        what it says, read?
        seems to be used to edit and add
        it tells edit from add based on having an
        index -- index to model or an id think index



        """
        super().__init__(parent)
        self.model = model
        self.index = index

        self.setWindowTitle("Edit Employee")

        self._build_gui( )

        self.populate_departments()

        if index:
            self.load_data()

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says, read?
        """
        self.layout             = QFormLayout()
        self.name_edit          = QLineEdit()
        self.department_combo   = QComboBox()

        self.layout.addRow(    "Name:",       self.name_edit)
        self.layout.addRow(    "Department:", self.department_combo)

        self.setLayout( self.layout )

        self.buttons            = QWidget()
        self.button_layout      = QVBoxLayout()
        self.layout.addRow( self.buttons )
        self.buttons.setLayout( self.button_layout )

        widget                  = QPushButton("Save")
        self.save_button        = widget
        widget.clicked.connect( self.update_db )
        self.button_layout.addWidget( widget )

        widget                  = QPushButton("Cancel")
        self.cancel_button        = widget
        widget.clicked.connect( self.reject )
        self.button_layout.addWidget( widget )


    # --------------------------------------------
    def populate_departments(self):
        """
        what it says, read?
        """
        query = QSqlDatabase.database().exec("SELECT id, name FROM department")
        while query.next():
            self.department_combo.addItem(query.value(1), query.value(0))

    # --------------------------------------------
    def load_data(self):
        """
        what it says, read?
        """
        name                = self.model.data(self.model.index(self.index.row(), 1))
        department_id       = self.model.data(self.model.index(self.index.row(), 2))
        self.name_edit.setText(name)
        department_index     = self.department_combo.findData(department_id)
        if department_index != -1:
            self.department_combo.setCurrentIndex( department_index )


    # ------------------------
    def update_db(self):
        """
        what it says, read?
        """
        name            = self.name_edit.text()
        department_id   = self.department_combo.currentData()

        if not name:
            QMessageBox.warning(self, "Input Error", "Employee name cannot be empty.")
            return

        if self.index:
            self.model.setData(self.model.index(self.index.row(), 1), name)
            self.model.setData(self.model.index(self.index.row(), 2), department_id)

        else:
            self.model.insertRow(self.model.rowCount())
            self.model.setData(self.model.index(self.model.rowCount() - 1, 1), name)
            self.model.setData(self.model.index(self.model.rowCount() - 1, 2), department_id)

        self.model.submitAll()
        self.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        """
        what it says, read?
        """
        super().__init__()
        self.setWindowTitle( app_title )
        self.resize(800, 600)

        self.keygen = KeyGen()

        self._build_gui( )

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says, read?
        """
        # Set up the main layout
        main_layout = QVBoxLayout()

        # Create a table view
        self.view = QTableView()
        self.view.setSelectionBehavior(QTableView.SelectRows)
        main_layout.addWidget(self.view)

        # Create buttons for CRUD operations
        widget        = QPushButton('Add')
        #add_button    = widget
        widget.clicked.connect(self.add_record)
        main_layout.addWidget( widget )

        #
        widget        = QPushButton('Edit')
        #add_button    = widget
        widget.clicked.connect(self.edit_record)
        main_layout.addWidget( widget )

        #
        widget        = QPushButton('Delete')
        #add_button    = widget
        widget.clicked.connect(self.delete_record)
        main_layout.addWidget( widget )

        #
        widget        = QPushButton('More...')
        #add_button    = widget
        #widget.clicked.connect(self.delete_record)
        main_layout.addWidget( widget )

        # ---- model probrbly should be in _build_model
        # Set up the model
        self.model = QSqlRelationalTableModel(self)
        self.model.setTable('employee')
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.setRelation(2, QSqlRelation( 'department', 'id', 'name') )
        self.model.select()

        # Set the model to the view
        self.view.setModel(self.model)
        self.view.setItemDelegate(QSqlRelationalDelegate(self.view))

        # Set up the container widget
        container = QWidget()
        container.setLayout( main_layout )
        self.setCentralWidget(container)

    # ------------------------------------------
    def add_record(self):
        """
        what it says, read?
        """
        dialog = EditDialog(self.model, self.keygen)
        if dialog.exec_() == QDialog.Accepted:
            self.model.select()

    # ------------------------------------------
    def delete_record(self):
        """
        what it says, read?
        can we let this pend, need to experiment
        """
        index = self.view.currentIndex()
        if index.isValid():
            self.model.removeRow(index.row())
            self.model.submitAll() # Submit changes to the database
            self.model.select()

   # Submit changes to the database
    # ------------------------------------------
    def edit_record(self):
        """
        what it says, read?
        """
        index = self.view.currentIndex()
        if index.isValid():
            dialog = EditDialog(self.model, self.keygen, index)
            if dialog.exec_() == QDialog.Accepted:
                self.model.select()

# ------------------------------------------
if __name__ == '__main__':
    """
    what it says, read?
    """
    app = QApplication(sys.argv)

    if not create_connection_and_db():
        sys.exit(1)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


