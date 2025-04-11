#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
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


from PyQt5.QtCore import Qt
from PyQt5.QtSql import (QSqlDatabase,
                         QSqlDriver,
                         QSqlQuery,
                         QSqlRecord,
                         QSqlRelation,
                         QSqlRelationalDelegate,
                         QSqlRelationalTableModel,
                         QSqlTableModel)

from PyQt5.QtWidgets import (QApplication,
                             QComboBox,
                             QDateTimeEdit,
                             QDialog,
                             QDialogButtonBox,
                             QFormLayout,
                             QGridLayout,
                             QHBoxLayout,
                             QLabel,
                             QLineEdit,
                             QMainWindow,
                             QMessageBox,
                             QPushButton,
                             QSpinBox,
                             QTableView,
                             QVBoxLayout,
                             QWidget)

# ---- local imports

from   app_global import AppGlobal
import custom_widgets

# ---- end imports


#------------
class EditPeopleContact( QDialog ):
    """
    Dialog for adding or editing a record in detail tab sub tabs
    """

    def __init__(self, parent=None, edit_data = None ):
        """ """

        super().__init__(parent)
        self.setWindowTitle("Add New Contact Info" if edit_data is None else "Edit Contact Info")
        if parent is None:
            1/0 # need parent which is the tab where the model is
        # Create form layout and fields
        self.edit_data  = edit_data

        form_layout     = QFormLayout()

        # ---- lets add a DataDict code gen for this
        self._build_fields( form_layout, edit_data  )
        # If we're editing, populate the fields with the existing data
        if edit_data is None:
            edit_data       = {}
            self.edit_data  = edit_data

            for i_widget in self.widget_list:
                i_widget.set_default()

        else:
            for i_widget in self.widget_list:
                i_widget.dict_to_edit( edit_data )

        # Button box
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

        """
        widget_list         = []
        self.widget_list    = widget_list

        # ---- begin gen ---------------------------------------

        # ---- ID field
        widget              = custom_widgets.CQLineEdit(
                                        parent         = None,
                                        field_name     = "seq_id",
                                         )
        widget.dict_to_edit_cnv    =  widget.cnv_int_to_str
        widget.edit_to_dict_cnv    =  widget.cnv_str_to_int

        widget_list.append( widget )
        widget.setReadOnly( True )
        widget.setMaxLength( 10 )
        layout.addRow( "ID:", widget )

        # ---- people_id
        widget              = custom_widgets.CQLineEdit(
                                        parent         = None,
                                        field_name     = "people_id",
                                         )
        widget.dict_to_edit_cnv    =  widget.cnv_int_to_str
        widget.edit_to_dict_cnv    =  widget.cnv_str_to_int

        widget_list.append( widget )
        widget.setReadOnly( True )
        widget.setMaxLength( 10 )
        layout.addRow( "People ID:", widget )

        # ---- type
        widget                      = custom_widgets.CQLineEdit(
                                        parent         = None,
                                        field_name     = "type",
                                         )
        widget.dict_to_edit_cnv     =  widget.cnv_str_to_str
        widget.edit_to_dict_cnv     =  widget.cnv_str_to_str

        widget_list.append( widget )
        widget.setMaxLength( 10 )
        layout.addRow( "Type:", widget )

        # ---- phone old
        widget                      = custom_widgets.CQLineEdit(
                                        parent         = None,
                                        field_name     = "phone_old",
                                         )
        widget.dict_to_edit_cnv     =  widget.cnv_str_to_str
        widget.edit_to_dict_cnv     =  widget.cnv_str_to_str

        self.id_edit        = widget
        widget_list.append( widget )
        widget.setMaxLength( 10 )
        layout.addRow( "Phone Old:", widget )

        # ---- cmnt
        widget                      = custom_widgets.CQLineEdit(
                                        parent         = None,
                                        field_name     = "cmnt",
                                         )
        widget.dict_to_edit_cnv     =  widget.cnv_str_to_str
        widget.edit_to_dict_cnv     =  widget.cnv_str_to_str

        self.id_edit        = widget
        widget_list.append( widget )
        widget.setMaxLength( 10 )
        layout.addRow( "Comment:", widget )

        # ---- phone
        widget                      = custom_widgets.CQLineEdit(
                                        parent         = None,
                                        field_name     = "phone",
                                         )
        widget.dict_to_edit_cnv     =  widget.cnv_str_to_str
        widget.edit_to_dict_cnv     =  widget.cnv_str_to_str

        widget_list.append( widget )
        widget.setMaxLength( 10 )
        layout.addRow( "Phone:", widget )

        # ---- autodial
        widget              = custom_widgets.CQLineEdit(
                                        parent         = None,
                                        field_name     = "autodial",
                                         )
        widget.dict_to_edit_cnv    =  widget.cnv_int_to_str
        widget.edit_to_dict_cnv    =  widget.cnv_str_to_int

        widget_list.append( widget )
        widget.setMaxLength( 10 )
        layout.addRow( "Autodial:", widget )

    #-----------------------
    def get_form_data( self ):
        """
        Get the data from the form fields as a dictionary.
        """
        #edit_data     = self.edit_data
        for i_widget in self.widget_list:
            i_widget.edit_to_dict( self.edit_data )

        return self.edit_data

#-------------------------

class EditPeopleEvent( QDialog ):
    """
        Dialog for adding or editing a record in detail sub tabs.
        now with custom widgets cw
    """

    def __init__(self, parent=None, edit_data = None ):
        """
        the usual
        """
        super().__init__(parent)
        self.setWindowTitle("Add New Event Info" if edit_data is None else "Edit Event Info")
        if parent is None:
            1/0 # need parent which is the tab where the model is
        # Create form layout and fields
        self.edit_data  = edit_data

        form_layout     = QFormLayout()

        # ---- lets add a DataDict code gen for this
        self._build_fields( form_layout, edit_data  )
        # If we're editing, populate the fields with the existing data
        if edit_data is None:
            edit_data       = {}
            self.edit_data  = edit_data

            for i_widget in self.widget_list:
                i_widget.ct_default()

        else:
            for i_widget in self.widget_list:
                i_widget.dict_to_edit( edit_data )

        # Button box
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

        """
        widget_list         = []
        self.widget_list    = widget_list

        # ---- begin gen ---------------------------------------

        # ---- ID field
        widget              = custom_widgets.CQLineEdit(
                                        parent         = None,
                                        field_name     = "seq_id",
                                         )
        widget.dict_to_edit_cnv    =  widget.cnv_int_to_str
        widget.edit_to_dict_cnv    =  widget.cnv_str_to_int

        widget_list.append( widget )
        widget.setReadOnly( True )
        widget.setMaxLength( 10 )
        layout.addRow( "ID:", widget )

        # ---- people_id
        widget              = custom_widgets.CQLineEdit(
                                        parent         = None,
                                        field_name     = "people_id",
                                         )
        widget.dict_to_edit_cnv    =  widget.cnv_int_to_str
        widget.edit_to_dict_cnv    =  widget.cnv_str_to_int

        widget_list.append( widget )
        widget.setReadOnly( True )
        widget.setMaxLength( 10 )
        layout.addRow( "People ID:", widget )

        # ---- type
        widget                      = custom_widgets.CQLineEdit(
                                        parent         = None,
                                        field_name     = "type",
                                         )
        widget.dict_to_edit_cnv     =  widget.cnv_str_to_str
        widget.edit_to_dict_cnv     =  widget.cnv_str_to_str

        self.id_edit        = widget
        widget_list.append( widget )
        widget.setMaxLength( 10 )
        layout.addRow( "Type:", widget )


        # ---- phone old
        widget                      = custom_widgets.CQLineEdit(
                                        parent         = None,
                                        field_name     = "phone_old",
                                         )
        widget.dict_to_edit_cnv     =  widget.cnv_str_to_str
        widget.edit_to_dict_cnv     =  widget.cnv_str_to_str

        widget_list.append( widget )
        widget.setMaxLength( 10 )
        layout.addRow( "Phone Old:", widget )

        # ---- cmnt
        widget                      = custom_widgets.CQLineEdit(
                                        parent         = None,
                                        field_name     = "cmnt",
                                         )
        widget.dict_to_edit_cnv     =  widget.cnv_str_to_str
        widget.edit_to_dict_cnv     =  widget.cnv_str_to_str

        widget_list.append( widget )
        widget.setMaxLength( 10 )
        layout.addRow( "Comment:", widget )

        # ---- phone
        widget                      = custom_widgets.CQLineEdit(
                                        parent         = None,
                                        field_name     = "phone",
                                         )
        widget.dict_to_edit_cnv     =  widget.cnv_str_to_str
        widget.edit_to_dict_cnv     =  widget.cnv_str_to_str

        widget_list.append( widget )
        widget.setMaxLength( 10 )
        layout.addRow( "Phone:", widget )

        # ---- autodial
        widget              = custom_widgets.CQLineEdit(
                                        parent         = None,
                                        field_name     = "autodial",
                                         )
        widget.dict_to_edit_cnv    =  widget.cnv_int_to_str
        widget.edit_to_dict_cnv    =  widget.cnv_str_to_int

        widget_list.append( widget )
        widget.setMaxLength( 10 )
        layout.addRow( "Autodial:", widget )

    #-----------------------
    def get_form_data( self ):
        """
        Get the data from the form fields as a dictionary.
        """
        #edit_data     = self.edit_data
        for i_widget in self.widget_list:
            i_widget.edit_to_dict( self.edit_data )

        return self.edit_data

# ---- eof