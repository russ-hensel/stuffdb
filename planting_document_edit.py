#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 08:28:36 2024



"""
# ---- tof
# --------------------
if __name__ == "__main__":
    import main

# --------------------

# ---- imports
import sys

from app_global import AppGlobal

from qt_compat import QApplication, QAction, exec_app, qt_version
from PyQt.QtWidgets import QMainWindow, QToolBar, QMessageBox
from qt_compat import Qt, DisplayRole, EditRole, CheckStateRole
from qt_compat import TextAlignmentRole



from PyQt.QtCore import Qt
from PyQt.QtSql import (QSqlDatabase,
                         QSqlDriver,
                         QSqlQuery,
                         QSqlRecord,
                         QSqlRelation,
                         QSqlRelationalDelegate,
                         QSqlRelationalTableModel,
                         QSqlTableModel)

from PyQt.QtWidgets import (QApplication,
                             QComboBox,
                             QDialog,
                             QFormLayout,
                             QGridLayout,
                             QHBoxLayout,
                             QDialogButtonBox,
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
import custom_widgets as cw

# ---- end imports


ok_blow_on_error = False
print( f"using: {ok_blow_on_error = } ")


#----------------------
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

#--------------------------------
class EditPlantingEvent( QDialog ):
    """Dialog for adding or editing a record in the stuff_event table.
    my first tweak before custom edits
    """

    def __init__(self, parent=None, edit_data = None ):
        """
        """
        super().__init__(parent)
        self.setWindowTitle("Add New Event Info" if edit_data is None else "Edit Event Info")

        self.resize(400, 250)

        if parent is None:
            1/0 # need parent which is the tab where the model is
        # Create form layout and fields
        self.edit_data  = edit_data

        form_layout     = QFormLayout()

        # ---- lets add a datadict code gen for this
        self._build_fields( form_layout, edit_data  )
        # If we're editing, populate the fields with the existing data
        if edit_data is None:
            edit_data       = {}
            self.edit_data  = edit_data

            for i_widget in self.widget_list:
                i_widget.set_default()

        else:
            for i_widget in self.widget_list:
                # date here is comming as a fromatted string, why is this
                i_widget.dict_to_edit( edit_data )

        # ---- Button box
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(button_box)

        self.setLayout( main_layout )

    # -------------------------------------
    def _build_fields( self, layout, edit_data ):
        """
        place fields into layout, a sub layout is ok
        tweaks
            none yet
        !! can we use the field dict to automate this
            will do manually for now

CREATE TABLE  planting_event    (
     id  INTEGER,
     id_old  VARCHAR(15),
     planting_id_old  VARCHAR(15),
     planting_id  INTEGER,
     event_dt  INTEGER,
     dlr  INTEGER,
     cmnt  VARCHAR(250),
     type  VARCHAR(15),
     dt_mo  INTEGER,
     dt_day  INTEGER,
     day_of_year  INTEGER
    )

        """
        widget_list         = []
        self.widget_list    = widget_list

        # ---- begin gen ---------------------------------------

        # ---- ID field
        widget              = cw.CQLineEdit(
                                        parent         = None,
                                        field_name     = "id",
                                         )

        widget.dict_to_edit_cnv    =  widget.cnv_int_to_str
        widget.edit_to_dict_cnv    =  widget.cnv_str_to_int

        # widget.ct_default          = 1/0

        #self.id_edit        = widget
        widget_list.append( widget )
        widget.setReadOnly( True )
        widget.setMaxLength( 10 )
        layout.addRow( "ID:", widget )

        # ----  field_name     = "planting_id",
        widget              = cw.CQLineEdit(
                                        parent         = None,
                                        field_name     = "planting_id",
                                         )
        widget.dict_to_edit_cnv    =  widget.cnv_int_to_str
        widget.edit_to_dict_cnv    =  widget.cnv_str_to_int

        #self.id_edit        = widget
        widget_list.append( widget )
        widget.setReadOnly( True )
        widget.setMaxLength( 10 )
        layout.addRow( "Planting ID:", widget )

        # ---- cmnt
        widget                      = cw.CQLineEdit(
                                        parent         = None,
                                        field_name     = "cmnt",
                                         )
        widget.dict_to_edit_cnv     =  widget.cnv_str_to_str
        widget.edit_to_dict_cnv     =  widget.cnv_str_to_str

        self.id_edit        = widget
        widget_list.append( widget )
        widget.setMaxLength( 250 )
        layout.addRow( "Comment:", widget )

        # ---- event_dt
        # Event date/time field (stored as integer timestamp)
        # self.event_date_edit = QDateTimeEdit(QDateTime.currentDateTime())
        # form_layout.addRow( "Event Date:", self.event_date_edit )

        widget                      = cw.CQDateEdit(
                                        parent         = None,
                                        field_name     = "event_dt",
                                         )

        print( "planting_document_edit_fix_me" )
        #think this should be string to string later string to qdate and inverse
        widget.dict_to_edit_cnv     =  widget.cnv_str_to_qdate
        widget.edit_to_dict_cnv     =  widget.cnv_qdate_to_int

        widget_list.append( widget )
        # widget.setMaxLength( 20 ) not a method
        layout.addRow( "Event Date:", widget )

        # ---- cmnt
        widget                      = cw.CQLineEdit(
                                        parent         = None,
                                        field_name     = "dlr",
                                         )
        widget.dict_to_edit_cnv     =  widget.cnv_int_to_str
        widget.edit_to_dict_cnv     =  widget.cnv_str_to_int

        self.id_edit        = widget
        widget_list.append( widget )
        widget.setMaxLength( 50 )
        layout.addRow( "Dollars $", widget )


    #-----------------------
    def get_form_data( self ):
        """
        Get the data from the form fields as a dictionary.
        """
        # see stuff that has some fix up
        for i_widget in self.widget_list:
            i_widget.edit_to_dict( self.edit_data )

        return self.edit_data


#---- eof