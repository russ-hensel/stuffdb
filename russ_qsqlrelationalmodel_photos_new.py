#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 09:12:11 2024



    no working add issues a update with wrong columns

        ** reduce the join to one column
                slight error in column allignment but still update
        !! trace thru code does it seem to be update
                fields_to_model  is going thru update part
                !! compare to chat version
                data       =  self.photo_photo_fn_field.text() removed because not updatable
      still issues but too much clutter my index numbers are messed up

      save backup    bak_4

"""





# ---- imports

import sys
# sys.path.append( r"D:\Russ\0000\python00\python3\_projects\rshlib"  )
# sys.path.append( "../")
sys.path.insert( 1, "../rshlib" )
sys.path.insert( 1, "./ex_qt" )
sys.path.insert( 1, ".//mnt/WIN_D/Russ/0000/python00/python3/_examples/" )
sys.path.insert( 1, ".//mnt/WIN_D/Russ/0000/python00/python3/_examples/qt" )

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget, QPushButton, QLineEdit, QFormLayout, QDialog, QMessageBox, QComboBox
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlRelationalTableModel, QSqlRelation, QSqlRelationalDelegate
from PyQt5.QtCore import Qt

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget, QPushButton, QLineEdit, QFormLayout, QDialog, QMessageBox, QComboBox, QLabel
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlRelationalTableModel, QSqlRelation, QSqlRelationalDelegate, QSqlQuery, QSqlDriver, QSqlRecord



# ---- local imports
import  tracked_qsql_relational_table_model


from    app_global import AppGlobal
# ---- end imports


# ---- a few parameters
app_title   = "russ_qsqlrelationalmodel_photos.py"

db_file     = "texs_x.db"
db_file     = ':memory:'
db_file     = '/mnt/WIN_D/Russ/0000/python00/python3/_projects/stuffdb/data/appdb.db'

create_db   = False

style       = "photo"  # or seq >



def create_connection_and_db():
    """
    uses key gen later but this is jus static

    """

    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName( db_file )
    if not db.open():
        print("Unable to establish a database connection.")
        return False

    if not create_db:
        print( f"hope your db { db_file = } works")
        return True

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


class KeyGen():
    """
    a debug, tweak for short term valid
    """
    def __init__( self ):
        self.keys     = list( range( 3055, 5000 ))
        self.ix_keys  = -1


    def get_next_key( self, table_name ):
        """


        Args:
            table_name (TYPE): DESCRIPTION.

        Returns:
            new_key (TYPE): DESCRIPTION.

        """
        self.ix_keys  += 1
        new_key        = self.keys[ self.ix_keys ]
        print( f"key_gen for {table_name} {self.ix_keys = } {new_key = }" )
        return new_key



class EditDialog( QDialog ):
    """
    what it says, read?
    seems to be used to edit and add
    it tells edit from add based on having an
    index -- index to model or an id think index

    """
    # ------------------------------------------
    def __init__(self, model, keygen, index = None, parent = None):
        """


        Args:
            model (TYPE): DESCRIPTION.
            keygen (TYPE): DESCRIPTION.
            index (TYPE, optional): DESCRIPTION. Defaults to None.
            parent (TYPE, optional): DESCRIPTION. Defaults to None.

        Returns:
            None.

        """
        super().__init__( parent )
        self.parent         = parent
            # we will get some importand data from the parent
            # watch for it
        self.model          = model
        self.keygen         = keygen
        self.index          = index
        self.setWindowTitle( "Edit Data" )

        self._build_gui()

        if index:    # no index means new record, but may need defaults
            #self.load_data()  # at least some of gui has to be built
            self.model_to_fields()

        #self.populate_departments()

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says, read?
        """
        #self._build_seq_gui()

        if   style  == "photo":
            self._build_gui_photo()
        elif style  == "photox":
            1/0
        else:
            100/0

        # ---- buttons
        self.setLayout( self.layout )

        self.buttons            = QWidget()
        self.button_layout      = QVBoxLayout()

        a_widget                = QPushButton("Save")
        self.save_button        = a_widget
        a_widget.clicked.connect(self.update_db)
        self.button_layout.addWidget( a_widget )

        #----
        a_widget                = QPushButton("Cancel")
        self.cancel_button        = a_widget
        a_widget.clicked.connect(  self.reject )
        self.button_layout.addWidget( a_widget )

        self.buttons.setLayout(self.button_layout)

        self.layout.addRow(self.buttons)

    # ------------------------------------------

    # ------------------------------------------
    def _build_gui_photo( self, ):
        """
        what it says, read?

                self.name_ix          # useful later


        """
        self.layout                     = QFormLayout()

        # a_widget                        = QLineEdit()
        # self.seq_no_field               = a_widget
        # self.layout.addRow( "seq_no",         a_widget )

        # ----
        a_widget                        = QLineEdit()
        self.id_field                   = a_widget
        self.id_ix                      = 0
        self.layout.addRow( "id",         a_widget )

        a_widget                            = QLineEdit()
        self.photoshow_id_field             = a_widget
        self.photoshow_id_ix                  = 1
        self.layout.addRow( "photoshow_id",         a_widget )


        # a_widget                            = QLineEdit()
        # self.photo_name_field               = a_widget
        # self.photo_name_ix                  = 2
        # self.layout.addRow( "photo_name**",         a_widget )


        a_widget                        = QLineEdit()
        self.photo_photo_fn_field       = a_widget
        self.photo_photo_fn_ix          = 3
        self.layout.addRow( "photo_fn**",         a_widget )

        a_widget                        = QLineEdit()
        self.seq_no_field               = a_widget
        self.seq_no_ix                  = 4
        self.layout.addRow( "seq_no",         a_widget )


    # ------------------------------------------
    def populate_departments(self):
        """
        what it says, read?
        """

        return

        query = QSqlDatabase.database().exec("SELECT id, name FROM department")
        while query.next():
            self.department_combo.addItem(query.value(1), query.value(0))

    # ------------------------------------------
    def model_to_fields( self ):
        """
        what it says, read?
        rename to model_to_fields
        """
        #self.model_to_fields_seq()

        if   style  == "photo":
            self.model_to_fields_photo()
        elif style  == "seq":
            self.model_to_fields_seq()
        else:
            100/0


    # ------------------------------------------
    def model_to_fields_photo( self ):
        """
        what it says, read?
        rename to model_to_fields
        """
        model               = self.model




        ix_col              = -1

        # ix_col              += 1
        # data                = model.data( model.index(self.index.row(), ix_col) )
        # self.photo_photo_fn_field.setText( data )

        # ix_col              += 1
        # data                = model.data( model.index(self.index.row(), ix_col) )
        # self.seq_no_field.setText( str( data ) )

        ix_col              += 1
        data                = model.data( model.index( self.index.row(), ix_col) )
        self.id_field.setText( str( data ) )

        ix_col              += 1
        data                = model.data( model.index( self.index.row(), ix_col) )
        self.photoshow_id_field.setText( str( data ) )

        # # ---- photo_name
        # ix_col              += 1
        # #data                = model.data( model.index(self.index.row(), ix_col) )
        # data                = "read_only"
        # self.photo_name_field.setText( str( data ) )

        ix_col              += 1
        field               = "photo_photo_fn_ix"
        data                = model.data( model.index(self.index.row(), ix_col) )
        print( f"get {field} from index {ix_col}  {self.photo_photo_fn_ix = }  {data = }" )
        #data                = "read_only"
        self.photo_photo_fn_field.setText( str( data ) )


        ix_col              += 1
        field               = "seq_no"
        data                = model.data( model.index(self.index.row(), ix_col) )
        print( f"get {field} from index {ix_col}  {self.seq_no_ix = }  {data = }" )
        self.seq_no_field.setText( str( data ) )

        # ix_col              += 1
        # data                = model.data( model.index(self.index.row(), ix_col) )
        # self.no_06_field.setText( str( data ) )



    # ------------------------------------------
    def load_data_bakxxxxxx( self ):
        """
        what it says, read?
        rename to model_to_field
        """
        model               = self.model

        name                = self.model.data( self.model.index(self.index.row(), 1) )
        department_id       = self.model.data(self.model.index(self.index.row(), 2))
        self.name_field.setText(name)
        department_index    = self.department_combo.findData(department_id)
        if department_index != -1:
            self.department_combo.setCurrentIndex(department_index)

    # ------------------------------------------
    def update_db(self):
        """
        what it says, read?
        we are only updating one at a time
        so this is ok for now
        does not do the delete case
        logic:
            get data from fields ( make sub ?)
            apply to model

            update and add now
        """

        # self.save_data_like_chat()
        # return


        if   style  == "photo":
            self.update_photo()
        elif style  == "except":
            1/0
        else:
            100/0

    # ------------------------------------------
    def save_data_like_chat_works_modelonthis(self):
        print( "save_data_like_chat"    )

        # name            = self.name_edit.text()
        # department_id   = self.department_combo.currentData()

        # if not name:
        #     QMessageBox.warning(self, "Input Error", "Employee name cannot be empty.")
        #     return

        if self.index:
            print( "if update true use update??" )

            data        = int ( self.photoshow_id_field.text() )
            self.model.setData(self.model.index(self.index.row(), 1), data)

            data        = int ( self.photoshow_id_field.text() )
            self.model.setData(self.model.index(self.index.row(), 2), data )


        else:
            print( "if update insert?? this will change the row count" )

            self.model.insertRow(self.model.rowCount())

            key = self.keygen.get_next_key( self.parent.table_name  )
            self.model.setData(self.model.index(self.model.rowCount() - 1, 0), key)

            data        = int ( self.photoshow_id_field.text() )
            self.model.setData(self.model.index(self.model.rowCount() - 1, 1), data)

            data       =  int( self.seq_no_field.text() )
            self.model.setData(self.model.index(self.model.rowCount() - 1, 2), data)



        self.model.submitAll()  # Submit changes to the database
        self.accept()

    # ------------------------------------------
    def update_photo(self):
        """
        what it says, read?
        _org   = original version
        mutates
            self.model
        """
        self.fields_to_model(   )


        self.model.submitAll()
        self.accept()   # QDialog method ?


    # ------------------------------------------
    def fields_to_model(self, ):
        """
        what it says - read
            this is photo version
            I am finally going to just reason it out

        logic:
            may not move back data that cannot be updated

            photoshow_id should be on auto
            seq no should be on auto
            need field name, field_id and conversion
            use code gen or some clever programming

            can we build attributes at runtime from a name -- without evel
        """
        print( ".................... using field to model")
        model                = self.model
        table_name           = self.parent.table_name


        if not self.index:   # new row  self.index and index not the same
            print( ">>>>>>>>>>>>new row")
            key             = self.keygen.get_next_key( table_name )
            # row count here becomes rowcount - 1 later
            model.insertRow( model.rowCount() )
            ix_row               = model.rowCount() - 1   # model row that get the data here new row
            # model.index makes an index row col for the data
            model.setData( model.index( ix_row, 0), key )

            # index           = index_add
            # index_row       = index_add

        else: # old and new rows
            print( ">>>>>>>>>>>>>>.update")
            ix_row               = self.index.row()   # row index wher edit data come from
            # index_update   = self.index
            # index          = index_update
            # index_row      = self.index.row()

        # ---- photoshow_id
        data       =  int( self.photoshow_id_field.text() )
        print( f"fields_to_model photoshow_id { data } {self.photoshow_id_ix = }" )
        model.setData( model.index(  ix_row, self.photoshow_id_ix ), data )

        # ---- seq_no
        data       =  int( self.seq_no_field.text() )
        print( f"fields_to_model seq_no { data } {self.seq_no_ix = }" )
        model.setData( model.index(  ix_row, self.seq_no_ix ), data )  # save ok save may be ok else  ??


    # ------------------------------------------
    def fields_to_model_close_nc(self, ):
        """
        what it says - read
            this is photo version

        logic:
            may not move back data that cannot be updated

            photoshow_id should be on auto
            seq no should be on auto
            need field name, field_id and conversion
            use code gen or some clever programming

            can we build attributes at runtime from a name -- without evel
        """
        print( ".................... using field to model")
        model                = self.model
        table_name           = self.parent.table_name
        row_count_minus_1    = model.rowCount() - 1

        if not self.index:   # new row  self.index and index not the same
            print( ">>>>>>>>>>>>new row")
            key             = self.keygen.get_next_key( table_name )
            # row count here becomes rowcount - 1 later
            model.insertRow( model.rowCount() )
            row_count_minus_1    = model.rowCount() - 1
            model.setData( model.index( row_count_minus_1, 0), key )

            # index           = index_add
            # index_row       = index_add

        else: # old and new rows
            print( ">>>>>>>>>>>>>>.update")
            index_update   = self.index
            index          = index_update
            index_row      = self.index.row()

        # ---- photoshow_id
        data       =  int( self.photoshow_id_field.text() )
        print( f"fields_to_model photoshow_id { data } {self.photoshow_id_ix = }" )
        model.setData( model.index(  row_count_minus_1, self.photoshow_id_ix ), data )

        # ---- seq_no
        data       =  int( self.seq_no_field.text() )
        print( f"fields_to_model seq_no { data } {self.seq_no_ix = }" )
        model.setData( model.index(  row_count_minus_1, self.seq_no_ix ), data )  # save ok save may be ok else  ??



    # ------------------------------------------
    def update_db_org(self):
        """
        what it says, read?
        _org   = original version
        """
        name              = self.name_field.text()
        department_id     = self.department_combo.currentData()

        if not name:
            QMessageBox.warning(self, "Input Error", "Employee name cannot be empty.")
            return

        if self.index:   # old fetched row
            self.model.setData(self.model.index(self.index.row(), 1), name)
            self.model.setData(self.model.index(self.index.row(), 2), department_id)
        else:             # new row
            key     = self.keygen.get_next_key()
            self.model.insertRow(self.model.rowCount())
            self.model.setData(self.model.index(self.model.rowCount() - 1, 0), key)
            self.model.setData(self.model.index(self.model.rowCount() - 1, 1), name)
            self.model.setData(self.model.index(self.model.rowCount() - 1, 2), department_id)

        self.model.submitAll()  # Submit changes to the database
        self.accept()




# ---------------------------------
class MainWindow( QMainWindow ):
    """
    tech:
        we have a model and a view, integrated
        and a dialog with fields that need to be moved
        in and out


    """
    def __init__(self):
        """
        what it says, read?
        """
        super().__init__()
        self.setWindowTitle( app_title )
        self.resize(800, 600)

        self.table_name   =  "photoshow_photo"
        self.keygen       = KeyGen()

        self._build_gui( )

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says, read?
        """
        #self._build_seq_gui()

        if   style  == "photo":
            self._build_gui_photo()
        elif style  == "seq":
            self._build_gui_seq()
        else:
            100/0

        # ---- buttons
        self.setLayout( self.layout )

        self.buttons            = QWidget()
        self.button_layout      = QVBoxLayout()


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
    def _build_gui_photo( self, ):
        """
        what it says, read?
        """
        # Set up the main layout
        main_layout = QVBoxLayout()

        # Create a table view
        self.view = QTableView()
        self.view.setSelectionBehavior(QTableView.SelectRows)
        main_layout.addWidget( self.view )

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

        self._build_model()

        # Set up the container widget
        container           = QWidget()
        container.setLayout( main_layout )
        self.setCentralWidget(container)


    # ------------------------------------------
    def _build_seq_gui( self, ):
        """
        what it says, read?
        """
        self.layout             = QFormLayout()

        a_widget                            = QLineEdit()
        self.no_00_field                    = a_widget
        self.layout.addRow( "no_00_field",         a_widget )

        a_widget                            = QLineEdit()
        self.no_01_field                    = a_widget
        self.layout.addRow( "no_01_field",         a_widget )

        a_widget                            = QLineEdit()
        self.no_02_field                    = a_widget
        self.layout.addRow( "no_02_field",         a_widget )

        a_widget                            = QLineEdit()
        self.no_03_field                    = a_widget
        self.layout.addRow( "no_03_field",         a_widget )

        a_widget                            = QLineEdit()
        self.no_04_field                    = a_widget
        self.layout.addRow( "no_04_field",         a_widget )

        a_widget                            = QLineEdit()
        self.no_05_field                    = a_widget
        self.layout.addRow( "no_05_field",         a_widget )

        a_widget                            = QLineEdit()
        self.no_06_field                    = a_widget
        self.layout.addRow( "no_06_field",         a_widget )

    # ------------------------------------------
    def _build_model( self, ):
        """
        what it says, read?
        """
        # ----
        # may not need both
        self.ids_new        = set( )
        self.ids_delete     = set()
        self.primay_table   = 'photoshow_photo'

        #self.model          = QSqlRelationalTableModel(self)
        #self.model          = TrackedQSqlRelationalTableModel( self )

        self.model          =  tracked_qsql_relational_table_model.TrackedQSqlRelationalTableModel( self )

        self.model.setTable( 'photoshow_photo' )
        self.model.setEditStrategy( QSqlTableModel.OnManualSubmit )

        ix_foreign_key        = 2         # key to photo position in table
        foreign_table         = "photo"
        foreign_table_key     = "id"      # key joining to photo

        # i can not seem to set more than one relation is thi right?
        # self.model.setRelation( ix_foreign_key, QSqlRelation( foreign_table, foreign_table_key, "photo_fn"  ))
        # self.model.setRelation( ix_foreign_key, QSqlRelation( foreign_table, foreign_table_key, "name"  ))
        # self.model.setRelation( ix_foreign_key, QSqlRelation( foreign_table, foreign_table_key, "name, photo_fn"  ))
        self.model.setRelation( ix_foreign_key, QSqlRelation( foreign_table, foreign_table_key, "id, photo_fn, name"  ))


        # ---- select here?
        self.model.select()

        # Set the model to the view -- view defined inn gui
        self.view.setModel( self.model )
        self.view.setItemDelegate( QSqlRelationalDelegate(self.view ) )


    # ------------------------------------------
    def add_record(self):
        """
        what it says, read?
        """
        dialog = EditDialog(self.model, self.keygen, parent = self )
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
            dialog = EditDialog( self.model, self.keygen, index, parent = self )
            if dialog.exec_() == QDialog.Accepted:
                self.model.select()



# # ============================================
# class App( ):
#     """
#     this class is the "main" or controller for the whole app
#     to run see end of this file
#     it is the controller of an mvc app
#     """
#     def __init__( self,    ):
#         """
#         usual init for main app
#         splash not working as desired, disabled
#         splash screen which is of not help unless we sleep the init
#         """
#         self.app_name          = "Stuff QT"
#         self.version           = __version__ # "Ver 08: 2024 11 03.01"
#         #self.app_version       = self.version   # get rid of dupe at some point... app_version in gui_ext
#         self.app_url           = "www.where"
#         # clean out dead
#         AppGlobal.controller   = self
#         self.gui               = None

#         self.restart( )





# ---- main
# ------------------------------------------
if __name__ == '__main__':
    """
    what it says, read?
    """
    app = QApplication(sys.argv)




    if not create_connection_and_db():
        sys.exit(1)

    # next_key      = AppGlobal.key_gen.get_next_key( "dfdsf" )


    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


# ---- reference  info

"""
how can i track the sql issued by various pyqt sql objects, can you
give me a few code examples? ( particurlary involving QSqlRelationalTableModel )

Is there a way with   QSqlRelationalTableModel,   QSqlRelation, or other
Qt object to select more than one column in the foreign table thru a join.  If so can you give
the code  or just a code snippet?



CREATE TABLE photoshow_photo (
            id              INTEGER PRIMARY KEY  UNIQUE NOT NULL, 0
            photoshow_id    INTEGER,                              1
            photo_id        INTEGER,                              2
            seq_no          INTEGER,
            no_comma        INTEGER

        )


CREATE TABLE photo (
            id          INTEGER PRIMARY KEY  UNIQUE NOT NULL,
            add_kw      VARCHAR(50),
            name        VARCHAR(60),
            descr       VARCHAR(60),
            photo_fn    VARCHAR(60),
            photo_ts    INTEGER,
            url         VARCHAR(60),
            title       VARCHAR(60),
            camera      VARCHAR(40),
            add_ts      INTEGER,
            edit_ts     INTEGER,
            no_comma    INTEGER

        )



SELECT
             photoshow_photo.id,
             photo.id,
             photoshow_photo.photoshow_id,
             photoshow_photo.photo_id,
             photoshow_photo.seq_no,
             photo.name,
             photo.photo_fn


    from     photoshow_photo

    JOIN   photoshow
    ON     photoshow.id = photoshow_photo.photoshow_id

    JOIN   photo
    ON     photoshow_photo.photo_id = photo.id

    WHERE  photoshow.id = 29;

The setRelation() function calls establish a relationship between two tables.
The first call specifies that column 2 in table employee is a foreign key that maps with field id of table city ,
and that the view should present the city ‘s name field to the user. The second call does something similar with column 3.


model.setTable("employee")

ix_foreign_key        = 2
foreign_table         = "city"
foreign_table_key     = "id"

model.setRelation( ix_foreign_key, QSqlRelation( foreign_table, foreign_table_key, "name"))

aa

model.setRelation(3, QSqlRelation("country", "id", "name"))

model.setTable("employee")

model.setRelation(2, QSqlRelation("city", "id", "name"))
model.setRelation(3, QSqlRelation("country", "id", "name"))
"""
# ---- chat
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

    now adapt for my photos in a photo show


    a photoshod id   photoshow_id will be input, at firs tixed, later passed in


russ_qsqlrelationalmodel_photos.py



"""