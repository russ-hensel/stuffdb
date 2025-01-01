#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 08:28:36 2024

stuff_document_edit.EditStuffEvents( model, keygen, index = None, parent = None)



"""

# --------------------
if __name__ == "__main__":
    import main
    main.main()
# --------------------


import sys

from app_global import AppGlobal
from PyQt5.QtCore import Qt
from PyQt5.QtSql import (QSqlDatabase,
                         QSqlDriver,
                         QSqlQuery,
                         QSqlRecord,
                         QSqlRelation,
                         QSqlRelationalDelegate,
                         QSqlRelationalTableModel,
                         QSqlTableModel)
# ----QtWidgets layouts
from PyQt5.QtWidgets import (QApplication,
                             QComboBox,
                             QDialog,
                             QFormLayout,
                             QGridLayout,
                             QHBoxLayout,
                             QLabel,
                             QLineEdit,
                             QMainWindow,
                             QMessageBox,
                             QPushButton,
                             QTableView,
                             QVBoxLayout,
                             QWidget)

# ---- local imports
# import  tracked_qsql_relational_table_model


# ---- end imports

style       = "photo"  # or seq >
style       = "seq"  # or seq >

#------------
relation    = "none"    # one  two    # related columns
relation    = "one"    # one  two    # related columns
relation    = "two"    # one  two    # related columns


print( "\n\n")
print( f"using: {style = }   {relation =}")

ok_blow_on_error = False
print( f"using: {ok_blow_on_error = } ")

photoshow_id   = 29
print( f"using: {photoshow_id = } ")

def blow_on_error( ):
    if ok_blow_on_error:
        print( "blow on error yes yes.... ")
        1/0

#----------------------
def fix_none_int( obj ):
    """
    read it -- make smarter later
    """
    if isinstance( obj, str ):
        obj    = obj.strip()

    if obj == "":
        print( "empty string return 0")
        return 0

    try:
        obj   = int( obj )
        return obj

    except:
        pass


    if obj is None:
        ret_val  = -999
        print( f"fix_none_int object is none return {ret_val}")
        blow_on_error()
        return  ret_val

    elif isinstance( obj, str ):
        ret_val  = -111
        print( f"fix_none_int object is non int string {ret_val}")
        blow_on_error()
        return  ret_val
    else:
        333/0

def fix_none_str( obj ):
    """
    read it -- make smarter later
    """
    if obj is None:
        return "none"
    else:
        return str( obj )

class EditStuffEvents( QDialog ):
    """
    what it says, read?
    seems to be used to edit and add
    it tells edit from add based on having an
    index -- index to model or an id think index

    CREATE TABLE stuff_event (
            id              INTEGER PRIMARY KEY  UNIQUE NOT NULL,
            stuff_id        INTEGER,
            cmnt            VARCHAR(100),
            event_ts        INTEGER,
            dlr             INTEGER,
            type            VARCHAR(20),
            no_comma        INTEGER

        )


    """
    # ------------------------------------------
    def __init__(self, model, index,  parent = None):
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
        self.parent         = parent  # parent may be a function use parent_window
        self.parent_window  = parent
            # we will get some importand data from the parent
            # watch for it
        self.model          = model

        #self.keygen         = keygen
        self.index          = index

        if index:
            msg    = "Edit Event"
        else:
            msg    = "Add Event"

        self.setWindowTitle( msg  )

        self._build_gui()

        if  index:    #   index means edit record
            #self.load_data()  # at least some of gui has to be built
            self.model_to_fields()

        else:
            data  = self.parent_window.current_id
            print( f"get currient_id {data = }")
            self.stuff_id_field.setText( str( data ) )

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says, read?
        """
        #self._build_seq_gui()

        if   True:
            self._build_gui_2()
        elif style  == "seq":
            self._build_gui_1()
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
    def _build_gui_1( self, ):
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

        a_widget                        = QLineEdit()
        self.photoshow_id_field         = a_widget
        self.photoshow_id_ix            = 1
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
    def _build_gui_2( self, ):
        """
        what it says, read?
        """
        # ---- code_gen: edit_fields_for_form  -- begin table entries

        layout              = QFormLayout()
        self.layout         = layout
        ix_field            = -1

        ix_field                += 1
        a_widget                = QLineEdit()
        a_widget.setEnabled( False )
        self.id_field           = a_widget
        self.id_ix              = ix_field
        layout.addRow( "id",    a_widget )

        ix_field                            += 1
        a_widget                            = QLineEdit()
        a_widget.setEnabled( False )
        self.stuff_id_field                   = a_widget
        self.stuff_id_ix                      = ix_field
        layout.addRow( "stuff_id",    a_widget )

        ix_field                            += 1
        a_widget                            = QLineEdit()
        self.cmnt_field                   = a_widget
        self.cmnt_ix                      = ix_field
        layout.addRow( "cmnt",    a_widget )

        ix_field                            += 1
        a_widget                            = QLineEdit()
        a_widget.setEnabled( False )
        self.event_ts_field                   = a_widget
        self.event_ts_ix                      = ix_field
        layout.addRow( "event_ts",    a_widget )

        ix_field                            += 1
        a_widget                            = QLineEdit()
        self.dlr_field                   = a_widget
        self.dlr_ix                      = ix_field
        layout.addRow( "dlr",    a_widget )

        ix_field                            += 1
        a_widget                            = QLineEdit()
        self.type_field                   = a_widget
        self.type_ix                      = ix_field
        layout.addRow( "type",    a_widget )

        ix_field                            += 1
        a_widget                            = QLineEdit()
        a_widget.setEnabled( False )
        self.no_comma_field                   = a_widget
        self.no_comma_ix                      = ix_field
        layout.addRow( "no_comma",    a_widget )

        # ---- code_gen: edit_fields_for_form  -- end table entries

    # ---- model to fields var ------------------------------------------
    def model_to_fields( self ):
        """
        what it says, read?
        rename to model_to_fields
        """
        #self.model_to_fields_seq()
        self.model_to_fields_2()
        # if   style  == "photo":
        #     self.model_to_fields_photo()
        # elif style  == "seq":
        #     self.model_to_fields_seq()
        # else:
        #     100/0


    # ------------------------------------------
    def model_to_fields_1( self ):
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

    # ------------------------------------------
    def model_to_fields_2( self ):
        """
        what it says, read?

        """
        model               = self.model

        ix_col              = -1

        # ---- code_gen: model_to_fields  -- begin table entries

        # ---- id
        ix_col              += 1
        data                = model.data( model.index( self.index.row(), ix_col) )
        self.id_field.setText( str( data ) )

        # ---- stuff_id
        ix_col              += 1
        data                = model.data( model.index( self.index.row(), ix_col) )
        self.stuff_id_field.setText( str( data ) )

        # ---- cmnt
        ix_col              += 1
        data                = model.data( model.index( self.index.row(), ix_col) )
        self.cmnt_field.setText( str( data ) )

        # ---- event_ts
        ix_col              += 1
        data                = model.data( model.index( self.index.row(), ix_col) )
        self.event_ts_field.setText( str( data ) )

        # ---- dlr
        ix_col              += 1
        data                = model.data( model.index( self.index.row(), ix_col) )
        self.dlr_field.setText( str( data ) )

        # ---- type
        ix_col              += 1
        data                = model.data( model.index( self.index.row(), ix_col) )
        self.type_field.setText( str( data ) )

        # ---- no_comma
        ix_col              += 1
        data                = model.data( model.index( self.index.row(), ix_col) )
        self.no_comma_field.setText( str( data ) )

        # ---- code_gen: model_to_fields  -- end table entries

    # ------------------------------------------
    def update_db(self):
        """
        what it says, read?
        _org   = original version
        mutates
            self.model

                """
        """
                what it says, read?
                we are only updating one at a time
                so this is ok for now
                does not do the delete case
                logic:
                    get data from fields ( make sub ?)
                    apply to model

                    update and add now

        import   qt_with_logging.
        qt_with_logging.QSqlTableModelWithLogging(    )
        qt_with_logging.QSqlRelationalTableModelWithLogging()
                """
        self.fields_to_model(   )
        msg    = "EditStuffEvents, may be doing update change this"
        ia_qt.q_sql_table_model( self.model, msg = msg,    )
        self.model.submitAll()   # QSqlTableModel(
        self.accept()   # QDialog method ?

    # ---- fields_to_model and var ------------------------------------------
    def fields_to_model( self, ):
        """
        what it says, read?
        """
        #self._build_seq_gui()

        self.fields_to_model_1()

        ia_qt.q_sql_table_model( self.model, "post fields_to_model" )

    # ------------------------------------------
    def fields_to_model_1(self, ):
        """
        what it says - read


        logic:
            no update of primary key
            may not move back data that cannot be updated

            photoshow_id should be on auto
            seq no should be on auto
            need field name, field_id and conversion
            use code gen or some clever programming

            can we build attributes at runtime from a name -- without evel
        """
        print( ".................... fields_to_model_..")
        model                = self.model
        table_name           = self.parent.table_name


        if not self.index:   # new row  self.index and index not the same
            print( ">>>>>>>>>>>>new row AppGlobal.key_gen       = a_key_gen")
            key             = AppGlobal.key_gen.get_next_key( table_name )
            # row count here becomes rowcount - 1 later
            model.insertRow( model.rowCount() )
            ix_row               = model.rowCount() - 1   # model row that get the data here new row
            # model.index makes an index row col for the data
            model.setData( model.index( ix_row, 0), key )

            # index           = index_add
            # index_row       = index_add

        else:
            print( ">>>>>>>>>>>>>>.update")
            ix_row               = self.index.row()   # row index wher edit data come from
            # index_update   = self.index
            # index          = index_update
            # index_row      = self.index.row()

        #print( f"{self.no_01_field == self.no_02_field = }" )


        # ---- stuff_id
        data       =  fix_none_int( self.stuff_id_field.text() )
        print( f"fields_to_model stuff_id  {data} {self.stuff_id_ix = }")
        model.setData( model.index(  ix_row, self.stuff_id_ix ), data )

        # ---- cmnt
        data       =   ( self.cmnt_field.text() )
        print( f"fields_to_model cmnt  {data} {self.cmnt_ix = }")
        model.setData( model.index(  ix_row, self.cmnt_ix ), data )

        # # ---- event_ts
        # data       =  fix_none_int( self.event_ts_field.text() )
        # print( f"fields_to_model event_ts  {data} {self.event_ts_ix = }")
        # model.setData( model.index(  ix_row, self.event_ts_ix ), data )

        # ---- dlr
        data       =  fix_none_int( self.dlr_field.text() )
        print( f"fields_to_model dlr  {data} {self.dlr_ix = }")
        model.setData( model.index(  ix_row, self.dlr_ix ), data )

        # ---- type
        data       =   ( self.type_field.text() )
        print( f"fields_to_model type  {data} {self.type_ix = }")
        model.setData( model.index(  ix_row, self.type_ix ), data )

        # # ---- no_comma
        # data       =  fix_none_int( self.no_comma_field.text() )
        # print( f"fields_to_model no_comma  {data} {self.no_comma_ix = }")
        # model.setData( model.index(  ix_row, self.no_comma_ix ), data )
        # # ---- code_gen: fields_to_model  -- end table entries