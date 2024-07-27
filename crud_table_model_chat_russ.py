#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 11:27:04 2024

@author: russ

code from chat that seems to work
but I want to rewrite/organize

not finished with delte
and check for save on fetch......

"""

db_fn               = "/mnt/WIN_D/Russ/0000/python00/python3/_projects/stuff_db_qt/data/appdb.db"
#db_fn               = ":memory:"

create_db           = False

win_title           = "crud_table_model_chat_russ.py"





import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QPushButton, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlRecord



# ---- end imports

class KeyGen():
    def __init__( self ):
        self.keys     = list( range( 100, 300 ))
        self.ix_keys  = -1
    def get_next_key( self, ):
        self.ix_keys  += 1
        return self.keys[ self.ix_keys ]


# ---------------------------
class PhotoTextApp(QWidget):
    def __init__(self):
        super().__init__()
        # Create the database connection
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(  db_fn  )  # Use an in-memory database for this example
        self.db.open()
        self.key_gen             = KeyGen()
        self.deleted_id          = None
        self.RECORD_NULL         = 0
        self.RECORD_FETCHED      = 1
        self.RECORD_NEW          = 2
        self.RECORD_DELETE       = 3




        # Setup the model
        self.model = QSqlTableModel()
        self.model.setTable( "photo_text" )
        self.model.select()

        self.build_gui()
        if create_db:
            self.insert_sample_data()
        self.record_state   = self.RECORD_NULL

    # ---------------------------
    def build_gui(self):
        """


        Returns:
            None.

        """
        hbox = QHBoxLayout()

        # Setup the UI components

        # ---------------------------

        # self.saveNewButton = QPushButton('Save New', self)
        # self.saveNewButton.clicked.connect(self.save_new_record)

        # Layout setup
        vbox = QVBoxLayout()

        # ---- fields
        widget              = QLineEdit(self)
        self.idField        = widget
        vbox.addWidget( widget)

        widget              = QTextEdit(self)
        self.textField      = widget
        vbox.addWidget( widget)

        # ---- buttons
        widget              = QPushButton('!!Clear', self)
        self.clearButton    = widget
        widget.clicked.connect(self.clear_fields)
        hbox.addWidget( widget )

        widget              = QPushButton('Select', self)
        self.selectButton   = widget
        widget .clicked.connect(self.select_record)
        hbox.addWidget( widget )

        widget              = QPushButton('!! Save\nNew', self)
        self.saveNewButton  = widget
        widget.clicked.connect( self.update_new_record)
        hbox.addWidget( widget )

        widget              = QPushButton('Delete', self)
        self.deleteButton   = widget
        widget .clicked.connect(self.delete_record)
        hbox.addWidget( widget )

        widget              = QPushButton('Insert', self)
        self.insertButton   = widget
        widget .clicked.connect(self.new_record)
        hbox.addWidget( widget )

        widget             = QPushButton('update_db', self)
        self.saveNewButton = widget            # probably do not need ref.
        widget.clicked.connect( self.update_db )
        hbox.addWidget( widget )

        # given hbox can i get a reference to the fields by name

        vbox.addLayout( hbox )
        self.setLayout(vbox)

        self.setWindowTitle( win_title )
        self.show()

    def insert_sample_data(self):

        # # Create the table
        # query = self.db.exec_("""CREATE TABLE photo_text (
        #     id INTEGER PRIMARY KEY UNIQUE NOT NULL,
        #     text_data TEXT
        # )""")



        sample_data = [
            (1, "Sample text 1"),
            (2, "Sample text 2"),
            (3, "Sample text 3")
        ]

        for i_id, text in sample_data:
            a_result = self.db.exec_(f"INSERT INTO photo_text (id, text_data) VALUES ({i_id}, '{text}')")


    # ---------------------------
    def clear_fields(self):
        self.idField.clear()
        self.textField.clear()

        print( "clear_fields" )

    # ---------------------------
    def select_record(self):
        """
        from russ crud  works

        """
        model    = self.model

        id_value = self.idField.text()   # normally passed in for stuff
        if id_value:
            model.setFilter(f"id = {id_value}")
            model.select()
            if model.rowCount() > 0:
                record = model.record(0)
                self.idField.setText(str(record.value("id")))  # Convert to string
                self.textField.setText(record.value("text_data"))
                self.record_state       = self.RECORD_FETCHED
            else:
                QMessageBox.warning(self, "Select", "Record not found!")
            model.setFilter("")

    # ---------------------------
    def update_record_fetched(self):
        """
        from russ crud

        """
        print( f"update_record_fetched  {self.record_state  = }")
        model    = self.model
        if not self.record_state  == self.RECORD_FETCHED:
            print( f"update_record_fetched bad state, return  {self.record_state  = }")
            return

        id_value = self.idField.text()
        if id_value:
            model.setFilter(f"id = {id_value}")
            model.select()
            if model.rowCount() > 0:
                record = model.record(0)
                record.setValue("id", int(id_value))
                record.setValue("text_data", self.textField.toPlainText())
                model.setRecord(0, record)
                model.submitAll()
                QMessageBox.information(self, "Save", "Record ( fetched ) saved!")
            model.setFilter("")

    # ---------------------
    def delete_record(self):
        """
        from russ crud

        """
        if  self.record_state  == self.RECORD_DELETE:
            print( f"delete_record already in state    {self.record_state  = } will return")
            return

        if  self.record_state  == self.RECORD_NEW:
            print( f"delete_record record is new   {self.record_state  = } clear fields")
            self.clear_fields()
            self.record_state  = self.RECORD_NULL
            return

        self.record_state       = self.RECORD_DELETE
        id_value = self.idField.text()
        self.deleted_id     = id_value
        self.clear_fields()

    # ---------------------
    def delete_record_update(self):
        """
        from russ crud

        """
        model    = self.model
        if not self.record_state  == self.RECORD_DELETE:
            print( f"delete_record_update bad state, return  {self.record_state  = }")
            return
        id_value    = self.deleted_id
        if id_value:
            model.setFilter(f"id = {id_value}")
            model.select()
            if model.rowCount() > 0:
                model.removeRow(0)
                model.submitAll()
                self.clear_fields()  # will fix record state
                self.record_state       = self.RECORD_NULL
                QMessageBox.information(self, "Delete", "Record deleted!")
            model.setFilter( "" )

    # ---------------------------
    def new_record(self):
        """
        from russ crud

        """
        print( f"new_record  {self.record_state  = } you may have pending updates")

        # if not self.record_state  == record_fetched:
        #     print( f"save_record_fetched bad state, return  {self.record_state  = }")
        #     return
        print( f"new_record  from {self.record_state  = }")
        self.clear_fields()
        new_id                  = self.key_gen.get_next_key()
        self.idField.setText( str( new_id ) )
        self.textField.setText( f"this is default text for {new_id}")

        self.record_state       = self.RECORD_NEW
        # self.idField.setText(str(new_id))  is ok??

    def update_new_record(self):
        """
        from russ crud

        """
        print( f"save_new_record  {self.record_state  = }")
        model    = self.model
        if not self.record_state  == self.RECORD_NEW:
            print( f"save_new_record bad state, return  {self.record_state  = }")
            return

        new_id     = self.idField.text()
        new_text   = self.textField.toPlainText()
        if new_id and new_text:
            record =  model.record()
            record.setValue("id", int(new_id))
            record.setValue("text_data", new_text)
            model.insertRecord( model.rowCount(), record )
            model.submitAll()
            self.record_state    = self.RECORD_FETCHED
            QMessageBox.information(self, "Save New", "New record saved!")
        else:
            print( f"do not seem to have new id and text {new_id = } { new_text = }")

    def update_db( self, ):
        """
        from russ crud

        """
        if   self.record_state   == self.RECORD_NULL:
            print( "update_db record null no action, return ")

        elif  self.record_state   == self.RECORD_NEW:
            self.update_new_record()

        elif  self.record_state   == self.RECORD_FETCHED:
            self.update_record_fetched()

        elif  self.record_state   == self.RECORD_DELETE:
            self.delete_record_update()

        else:
            print( f"update_db wtf  {self.record_state = } ")

        print( f"update_db record state now:  {self.record_state = } ")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PhotoTextApp()
    sys.exit(app.exec_())
