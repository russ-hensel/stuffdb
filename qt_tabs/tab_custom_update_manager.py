#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""
Created on Sun Dec 15 12:41:16 2024

"""
"""

KEY_WORDS:      some stuff rsh custom widgets update maager with sql model for forms and fields   new tab stagetwo zzz
CLASS_NAME:     CustomUpdateManagerTab
WIDGETS:        CQLineEdit CQDateEdit QSqlTableModel DataManager
STATUS:         runs_correctly_1_10      demo_complete_2_10   !! review_key_words   !! review_help_0_10
TAB_TITLE:      RSHCustom_DataManager

         self.help_file_name     =  "find_this_file.txt"

Search
    key_word
    is_key_word = True )
    setPlaceholderText



"""
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main_qt
    #main.main()
# --------------------



import traceback
import glob
import inspect
import json
import math
import os
import subprocess # ("David",   40,   "Daughter2" ),
            # ("James",   28,   "Aunt"      ),
            #
import sys
import time
from collections import namedtuple
from datetime import datetime
from functools import partial
from random import randint
from subprocess import PIPE, STDOUT, Popen, run

import pyqtgraph as pg
import wat
from PyQt5 import QtGui
from PyQt5.QtCore import (QAbstractListModel,
                          QAbstractTableModel,
                          QDate,
                          QDateTime,
                          QModelIndex,
                          QSize,
                          Qt,
                          QTime,
                          QTimer)
from PyQt5.QtGui import QColor, QImage, QPalette, QTextCursor, QTextDocument
# sql
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt5.QtWidgets import (QAction,
                             QApplication,
                             QButtonGroup,
                             QCheckBox,
                             QComboBox,
                             QDateEdit,
                             QDateTimeEdit,
                             QDial,
                             QDoubleSpinBox,
                             QFontComboBox,
                             QGridLayout,
                             QGroupBox,
                             QHBoxLayout,
                             QLabel,
                             QLCDNumber,
                             QLineEdit,
                             QListView,
                             QListWidget,
                             QListWidgetItem,
                             QMainWindow,
                             QMenu,
                             QMessageBox,
                             QProgressBar,
                             QPushButton,
                             QRadioButton,
                             QSizePolicy,
                             QSlider,
                             QSpinBox,
                             QStyledItemDelegate,
                             QTableView,
                             QTableWidget,
                             QTableWidgetItem,
                             QTabWidget,
                             QTextEdit,
                             QTimeEdit,
                             QVBoxLayout,
                             QWidget)

import parameters

import utils_for_tabs as uft
import wat_inspector
import custom_widgets
import global_vars
import info_about
import data_manager
import tab_base



FIF       = info_about.INFO_ABOUT.find_info_for



# ---- end imports


RECORD_NULL         = 0
RECORD_FETCHED      = 1
RECORD_NEW          = 2
RECORD_DELETE       = 3

INDENT              = uft.INDENT
print_func_header   = uft.print_func_header

new_keys     = [ 5001, 5002, 5003, 5004,5005, 5006, 5007 ] # change to list( range ())

def key_genxxx( ix ):
    """this is junk and will only work a few times
    """
    return new_keys[ ix ]


#  --------
class CustomUpdateManagerTab( tab_base.TabBase  ) :
    def __init__(self):
        """

        """
        super().__init__()
        self.help_file_name    =  uft.to_help_file_name( __name__ )

        # self.mutate_dict[0]    = self.mutate_0
        # self.mutate_dict[1]    = self.mutate_1
        # self.mutate_dict[2]    = self.mutate_2
        # self.mutate_dict[3]    = self.mutate_3
        # self.mutate_dict[4]    = self.mutate_4

        self.current_id        = -1       # invalid but prir next should fix

        # ---- junk to simulate next key
        self.id_list           = [ 1000, 1001, 1002, 1003, 1004, 3 ]
        self.ix_id_list        = 0    # where we are in self.id_list
        #self.field_list        = []
        self.new_key_ix        = 0

        self._build_model()

        # ---- data maanager
        self.data_manager      = data_manager.DataManager( self.model )
        self.data_manager.next_key_function = self.key_gen     # some_function( table_name )
        self.data_manager.enable_key_words(  "persons_key_words"  )

        self.current_record_type = RECORD_NULL

        self._build_gui()




    def _build_gui_widgets(self, main_layout  ):
        """
        the usual, build the gui with the widgets of interest
        and the buttons for examples
        """
        layout              = QVBoxLayout(   )

        main_layout.addLayout( layout )
        button_layout        = QHBoxLayout(   )

        lbl_stretch     = 0
        widget_stretch  = 3

        self.lbl_stretch     = lbl_stretch
        self.widget_stretch  = widget_stretch

        #self._build_fields_old( layout )
        self._build_fields( layout )

        # groupbox_criteria   = QGroupBox( "Criteria" )
        # set_groupbox_style( groupbox_criteria )

        # groupbox_edits      = QGroupBox( "Edits" )
        # set_groupbox_style( groupbox_edits )

        row_layout          = QHBoxLayout( )

        # ---- buttons
        layout.addLayout( row_layout )

        # label       = "select\n"
        # widget      = QPushButton( label )
        # widget.clicked.connect( self.mutate_1 )
        # row_layout.addWidget( widget )

        label       = "<<prior\n"
        widget      = QPushButton( label )
        connect_to  = partial( self.prior_next, -1 )
        widget.clicked.connect( connect_to )
        row_layout.addWidget( widget )

        label       = "next>>\n"
        widget      = QPushButton( label )
        connect_to  = partial( self.prior_next, 1 )
        widget.clicked.connect( connect_to )
        row_layout.addWidget( widget )

        # new_record
        label       = "insert_default\n"
        widget      = QPushButton( label )
        widget.clicked.connect( self.insert_default )
        row_layout.addWidget( widget )

        label       = "insert_copy\n"
        widget      = QPushButton( label )
        widget.clicked.connect( self.insert_copy )
        row_layout.addWidget( widget )

        label       = "validate\n"
        widget      = QPushButton( label )
        widget.clicked.connect( self.validate )
        row_layout.addWidget( widget )

        label       = "update_db\n"
        widget      = QPushButton( label )
        widget.clicked.connect( self.update_db )
        row_layout.addWidget( widget )

        # # ---- raise_except
        # widget = QPushButton("raise\n_except")
        # # widget.clicked.connect(lambda: self.print_message(widget.text()))
        # a_widget        = widget
        # widget.clicked.connect( lambda: self.raise_except( ) )
        # row_layout.addWidget( widget )


        # label       = "examine_0\n"
        # widget      = QPushButton( label )
        # widget.clicked.connect( self.examine_0 )
        # row_layout.addWidget( widget )

        widget = QPushButton("mutate\n")
        self.button_ex_1         = widget
        widget.clicked.connect( lambda: self.mutate( ) )
        button_layout.addWidget( widget )

        # ---- PB inspect
        widget              = QPushButton("inspect\n")
        connect_to        = self.inspect
        widget.clicked.connect( connect_to )
        row_layout.addWidget( widget )

        # ---- PB breakpoint
        widget              = QPushButton("breakpoint\n ")
        connect_to          = self.breakpoint
        widget.clicked.connect( connect_to )
        row_layout.addWidget( widget )

    def _build_fields( self, layout  ):
        """
        build some of the gui for a form
        these are field or record edits
        this code from code generation with tweak

        tweaks
        """
        # ---- code_gen: detail_tab_build_gui use for _build_fields was_build_gui  -- begin table entries
        # ---- code_gen: detail_tab_build_gui use for _build_fields was_build_gui  -- begin table entries

        # ---- code_gen: detail_tab_build_gui use for _build_fields was_build_gui  -- begin table entries


        # ---- id
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "id",
                                                db_type        = "integer",
                                                display_type   = "error",
                                                 )
        self.id_field     = edit_field
        edit_field.setPlaceholderText( "id" )
        edit_field.edit_to_rec     = edit_field.edit_to_rec_str_to_int
        edit_field.rec_to_edit     = edit_field.rec_to_edit_int_to_str
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- age
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "age",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.age_field     = edit_field
        edit_field.setPlaceholderText( "age" )
        edit_field.edit_to_rec     = edit_field.edit_to_rec_str_to_int
        edit_field.rec_to_edit     = edit_field.rec_to_edit_int_to_str
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- add_kw
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "add_kw",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.add_kw_field     = edit_field
        edit_field.setPlaceholderText( "add_kw" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field )


        # ---- family_relation
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "family_relation",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.family_relation_field     = edit_field
        edit_field.setPlaceholderText( "family_relation" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- name
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "name",
                                                db_type        = "string",
                                                display_type   = "error",
                                                 )
        self.name_field     = edit_field
        edit_field.setPlaceholderText( "name" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )

    # ------------------------------
    def _build_model( self,   ):
        """
        build model and views if used here

        """
        xxxxsql     = """
            CREATE TABLE people (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                name            TEXT NOT NULL,
                age             INTEGER,
                family_relation TEXT
                .....
            )
        """
        # ---- people
        model                  = QSqlTableModel( self, global_vars.EX_DB   )
                # this is what is used in stuffdb detail tab
        self.model             = model
        model.setTable( "persons" )

        model.setEditStrategy( QSqlTableModel.OnManualSubmit )

        #self.append_msg( "make a second model to see if any interaction ")

        model                  = QSqlTableModel( self, global_vars.EX_DB   )
        self.model_2           = model
        model.setTable( 'persons' )

        model.setFilter( "" )
        model.select()
        #ia_qt.q_sql_query_model( model, "select_record 2" )

        # method not valid yet
        # self.append_msg( FIF( self.model,   msg = "_build_model self.mode    post filter and select  " ) )
        # self.append_msg( FIF( self.model_2, msg = "_build_model self.model_2 post filter and select  " ) )


            #  OnFieldChange , OnRowChange , and OnManualSubmit .

        # model.setHeaderData(2, Qt.Horizontal, "Age*" ) # QtHorizontal in c
        #model->setHeaderData(1, Qt::Horizontal, tr("Salary"));

       #  view                    = QTableView( )
       #  self.people_view        = view
       #  view.setModel( model  )
       #  view.hideColumn( 0 )       # hide is hear but header on model
       #  view.setSelectionBehavior( QTableView.SelectRows )
       #  view.clicked.connect( self._people_view_clicked  )

       #  # ---- people_phones
       #  model                  = QSqlTableModel( self, global_vars.EX_DB  )
       #  self.phone_model       = model
       #  model.setTable( 'people_phones' )

       #  model.setEditStrategy( QSqlTableModel.OnManualSubmit )
       #      #  OnFieldChange , OnRowChange , and OnManualSubmit .
       #  # model->select();
       #  #model->setHeaderData(1, Qt::Horizontal, tr("Salary"));

       #  view                    = QTableView( )
       #  self.phone_view         = view
       #  view.setModel( model  )
       #  view.hideColumn( 0 )       # hide is hear but header on model
       #  #view.setSelectionBehavior( QTableView.SelectRows )
       #  #view.clicked.connect( self._view_clicked  )

       #      #  OnFieldChange , OnRowChange , and OnManualSubmit .
       #  # model->select();
       # #  model.setHeaderData(2, Qt.Horizontal, "Age*" ) # QtHorizontal in c
       #  #model->setHeaderData(1, Qt::Horizontal, tr("Salary"));

    # ------------------------
    def _build_fields_old(self, layout  ):
        """
        build some of the gui for a form
        these are field or record edits
        """
        name_in_text_edit  = True


        lbl_stretch         = self.lbl_stretch
        widget_stretch      = self.widget_stretch

        # ---- new row
        row_layout        = QHBoxLayout( )
        layout.addLayout( row_layout )

        # ---- id
        edit_field           = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "id",
                                                db_type        = "integer",
                                                display_type   = "string" )

        edit_field.setPlaceholderText( "id placeholder" )
        edit_field.rec_to_edit      = edit_field.rec_to_edit_int_to_str
        edit_field.edit_to_rec      = edit_field.edit_to_rec_str_to_int

        edit_field.ct_default     = partial( edit_field.do_ct_value, -99 )
        edit_field.ct_prior       = edit_field.do_ct_prior   # may be default

        # edit_field_validate     = edit_field_vlaidate.....
        # self.id_field         = edit_field     # not sre names are ever used
        self.data_manager.add_field( edit_field )
                # add_field( self, edit_field, is_key_word = False  ):
        row_layout.addWidget( edit_field )

        # ----  name
        if name_in_text_edit:
            field_name    = "not_used"
        edit_field           = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = field_name,
                                                db_type        = "string",
                                                display_type   = "string" )

        a_partial                           = partial( edit_field.validate_max_length, max_len = 5 )
        edit_field.validate                 = a_partial

        edit_field.ct_default     = partial( edit_field.do_ct_value, "custom default" )
        edit_field.ct_prior       = edit_field.do_ct_prior   # may be default
            # should already be set


        if not name_in_text_edit:
            self.name_field      = edit_field
            self.data_manager.add_field( edit_field, is_key_word = True )
        # self.field_list.append( edit_field )
        # row_layout.addWidget( edit_field )

        # ----  age
        edit_field           = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "age",
                                                db_type        = "integer",
                                                display_type   = "string" )

        self.age_field              = edit_field

        edit_field.rec_to_edit      = edit_field.rec_to_edit_int_to_str
        edit_field.edit_to_rec      = edit_field.edit_to_rec_str_to_int
        # ---- assign functions
        #a_partial                         = partial( edit_field.validate_max_length, max_len = 5 )
        edit_field.validate               = edit_field.validate_is_int

        a_partial                         = partial( edit_field.validate_max_int, max_int = 99 )
        edit_field.validate               = a_partial

        self.data_manager.add_field( edit_field )
        row_layout.addWidget( edit_field )

        # ----  add_kw
        widget            = QLabel( "add_kw ->")
        row_layout.addWidget( widget, )  #  stretch = lbl_stretch )

        edit_field           = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "add_kw",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.add_kw         = edit_field
        edit_field.setPlaceholderText( "setPlaceholderText add_kw" )
        self.data_manager.add_field( edit_field, is_key_word = True )
        row_layout.addWidget( edit_field )

        # ----  family_relation
        edit_field           = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "family_relation",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.relation_field         = edit_field

        self.data_manager.add_field( edit_field )
        row_layout.addWidget( edit_field )

        # ---- new row
        row_layout        = QHBoxLayout( )
        layout.addLayout( row_layout )

        # ----  text edit
        if name_in_text_edit:
            field_name    = "name"

        edit_field           = custom_widgets.CQTextEdit(
                                                parent         = None,
                                                field_name     = field_name,
                                                db_type        = "string",
                                                display_type   = "string" )
        self.text_field      = edit_field

        a_partial                  = partial( edit_field.do_ct_value, "**" )
        edit_field.ct_default      = a_partial
        if name_in_text_edit:
            self.name_field      = edit_field
            self.data_manager.add_field( edit_field,   is_key_word = True )

        row_layout.addWidget( edit_field )

    # ------------------------
    def _build_fields_newer(self, layout  ):
        """
        build some of the gui for a form
        these are field or record edits
        """


        lbl_stretch         = self.lbl_stretch
        widget_stretch      = self.widget_stretch

        # ---- new row
        row_layout        = QHBoxLayout( )
        layout.addLayout( row_layout )


        # ---- id
        edit_field           = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "id",
                                                db_type        = "integer",
                                                display_type   = "string" )

        edit_field.setPlaceholderText( "id placeholder" )
        edit_field.rec_to_edit      = edit_field.rec_to_edit_int_to_str
        edit_field.edit_to_rec      = edit_field.edit_to_rec_str_to_int

        edit_field.ct_default     = partial( edit_field.do_ct_value, -99 )
        edit_field.ct_prior       = edit_field.do_ct_prior   # may be default

        # edit_field_validate     = edit_field_vlaidate.....
        # self.id_field         = edit_field     # not sre names are ever used
        self.data_manager.add_field( edit_field )
                # add_field( self, edit_field, is_key_word = False  ):
        row_layout.addWidget( edit_field )

        # # ----  name
        # if name_in_text_edit:
        #     field_name    = "not_used"
        # edit_field           = custom_widgets.CQLineEdit(
        #                                         parent         = None,
        #                                         field_name     = field_name,
        #                                         db_type        = "string",
        #                                         display_type   = "string" )

        # a_partial                           = partial( edit_field.validate_max_length, max_len = 5 )
        # edit_field.validate                 = a_partial

        # edit_field.ct_default     = partial( edit_field.do_ct_value, "custom default" )
        # edit_field.ct_prior       = edit_field.do_ct_prior   # may be default
        #     # should already be set


        # if not name_in_text_edit:
        #     self.name_field      = edit_field
        #     self.data_manager.add_field( edit_field, is_key_word = True )
        # # self.field_list.append( edit_field )
        # # row_layout.addWidget( edit_field )

        # ----  age
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "age",
                                                db_type        = "integer",
                                                display_type   = "string" )

        self.age_field              = edit_field

        edit_field.rec_to_edit      = edit_field.rec_to_edit_int_to_str
        edit_field.edit_to_rec      = edit_field.edit_to_rec_str_to_int
        # ---- assign functions
        #a_partial                         = partial( edit_field.validate_max_length, max_len = 5 )
        edit_field.validate               = edit_field.validate_is_int

        a_partial                         = partial( edit_field.validate_max_int, max_int = 99 )
        edit_field.validate               = a_partial

        self.data_manager.add_field( edit_field )
        row_layout.addWidget( edit_field )

        edit_field           = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "add_kw",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.add_kw         = edit_field
        edit_field.setPlaceholderText( "setPlaceholderText add_kw" )
        self.data_manager.add_field( edit_field, is_key_word = True )
        row_layout.addWidget( edit_field )

        # ----  family_relation
        edit_field           = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "family_relation",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.relation_field         = edit_field

        self.data_manager.add_field( edit_field )
        row_layout.addWidget( edit_field )

        # ---- new row
        row_layout        = QHBoxLayout( )
        layout.addLayout( row_layout )

        edit_field           = custom_widgets.CQTextEdit(
                                                parent         = None,
                                                field_name     = "name",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.text_field      = edit_field

        a_partial                  = partial( edit_field.do_ct_value, "**" )
        edit_field.ct_default      = a_partial
        if name_in_text_edit:
            self.name_field      = edit_field
            self.data_manager.add_field( edit_field,   is_key_word = True )

        row_layout.addWidget( edit_field )

    # --------------------------
    def examinexxxxx( self, arg  ):
        """
        count : const int
        currentData : const QVariant
        currentIndex : int
        currentText : QString
        duplicatesEnabled : bool
        editable : bool        widget                          = self.make_criteria_date_widget()
        """
        """
        !!What it says
        """
        self.append_function_msg( "examine" )

        a_timestamp    = self.date_edit_2_widget.get_data_as_timestamp()

        #rint( f"inspect date_edit_2_widget.get_data_as_timestamp() { a_timestamp = }",   )


        self.append_msg( "line edit ---------------")
        widget    = self.line_edit_1_widget
        msg       = f"{widget.data_value = }"
        self.append_msg( msg )

        widget.data   = "changed data with @property.setter"

        widget    = self.line_edit_1_widget
        msg       = f"{widget.data_value = }"
        self.append_msg( msg )

        # ---- edits
        msg       = "\nFor the edit widgets:"
        msg       = f"{self.date_edit_1_widget.data_value = }"
        self.append_msg( msg )
        msg       = f"{self.date_edit_2_widget = }"
        self.append_msg( msg )
        msg       = f"{ self.line_edit_1_widget = }"
        self.append_msg( msg )
        msg       = f"{self.line_edit_2_widget = }"
        self.append_msg( msg )

        self.append_msg( f"inspect end { '' } --------",  )

    def key_gen( self, table_name_ignored ):
        """
        this is junk and will only work a few times
        as big as its array
        """
        self.new_key_ix    = self.new_key_ix  + 1
        new_key            = new_keys[    self.new_key_ix  ]
        return new_key

    # ------------------------
    def new_fields(self, a_type ):
        """
        What it says
        taken from stuff and simplifed
        move data from fetched record into the correct fields
        """
        self.append_function_msg( f"new_fields {a_type = }" )

        # ---- code_gen: detail_tab -- _record_to_field -- begin code
        for i_field in  self.field_list:
            pass
            #i_field.set_data_from_record( record )

        self.append_msg( "<--- done" )

    # # -------------------------------------
    # def new_record( self, next_key, a_type ):
    #     """
    #     from stuff simplified, not finished
    #     looks a bit like default new row
    #     promoted  --  ok ??
    #     """
    #     print_func_header( f"new_record {next_key = } {a_type = }" )

    #     self.id_field.set_data( next_key, "integer" )

    #     self.current_id             = next_key
    #     self.current_record_type    = RECORD_NEW

    #     if  a_type == "copy":
    #         self.append_msg( "not done yet ")
    #         self.field_list
    #         for i_field in  self.field_list:
    #             i_field.set_data_to_prior()

    #     elif a_type == "default":
    #         self.append_msg( "not done yet ")
    #         self.field_list
    #         for i_field in  self.field_list:
    #             i_field.set_data_to_default()
        self.append_msg( "<--- done" )
    #     elif a_type == "clear":
    #         self.append_msg( "not done yet ")
    #         self.field_list
    #         for i_field in  self.field_list:
    #             i_field.set_data_to_default()


    #     return


    #     self.new_fields( to_prior = False )        self.append_msg( "<--- done" )


    #     #self.record_state       = RECORD_NEW

    #     # think we need to use custon_widget
    #     #self.id_field.setText( str( next_key ) )
    #     self.id_field.set_data( next_key, "integer" )

    #     self.current_id         = next_key

    # # --------------------------
    # def select_by_id( self, a_id   ):
    #     """
    #     What it says
    #     taken from stuff and simplifed
    #     """
    #     print_func_header( f"select_by_id {a_id = }" )

    #     record   = None
    #     model    = self.model

    #     # assumes success
    #     self.current_id             = a_id
    #     self.current_record_type    = RECORD_FETCHED

    #     #ia_qt.q_sql_query_model( model, "select_record 1" )
    #     model.setFilter( f"id = {a_id}" )
    #     model.select()
    #     #ia_qt.q_sql_query_model( model, "select_record 2" )

    #     print( f"{INDENT}select_by_id{model.rowCount() = }  ")

    #     print(  FIF( model, msg = "select_by_id post filter and sele        self.append_msg( "<--- done" )ct " ) )

    #     if model.rowCount() > 0:
    #         record                  = model.record(0)
    #         self.id_field.setText( str(record.value("id")) )
    #         self.record_to_field( record )
    #         #self.textField.setText(record.value("text_data"))
    #         #self.record_state       = RECORD_FETCHED
    #         self.current_id         = a_id

    #     else:
    #         msg    = f"Record not found! {a_id = }"
    #         self.append_msg( msg )
    #         #AppGlobal.logger.error( msg )
    #         #QMessageBox.warning(self, "Select",  msg )
    #     #ia_qt.q_sql_query_model( model, "select_record 3 ancestor " )
    #     # model.setFilter("")  # why what happens if we leave alone
    #           # comment out here seems to fix history should be ok across all tabs
    #     #ia_qt.q_sql_query_model( model, "select_record 4  ancestor" )

    # # may be more like events plantings....  remove Picture soon ? or keep as special

    #     # if record:
    #     #     #rint( "in DetailTabBase, now dowing history probably only place should be done on select look for other calls  ")
    #     #     self.parent_window.record_to_history_table( record )

    #     # if self.pictures_tab:
    #     #     self.pictures_tab.select_by_id( id_value )


    # --------------------------
    def prior_next( self, delta  ):
        """
        What it says
        delta may be positive or negative
        """
        self.append_function_msg( f"prior_next {delta = }" )

        ix                     = self.ix_id_list
        our_list               = self.id_list
        max                    = len( our_list )

        new_ix                 = ix + delta

        if   new_ix < 0:
            self.append_msg( "wrap to max ix")
            new_ix  = max - 1

        elif new_ix >= max:
            self.append_msg( "wrap to ix = 0")
            new_ix  = 0

        self.ix_id_list   = new_ix
        #return new_ix

        #self.select_by_id( our_list[ new_ix ]  )

        self.data_manager.select_record( our_list[ new_ix ]  )

        self.append_msg( "<--- done" )


    # -------------------------------------
    def insert_default( self,   ):
        """
        what it says
        test edits for default behaviour
        """
        self.append_function_msg( "insert_default" )

        self.data_manager.new_record( next_key = None, option = "default" )
        # self.record_state = RECORD_NEW

        # self.new_key_ix    = self.new_key_ix  + 1
        # new_key            = key_gen( self.new_key_ix )
        # self.new_record(  next_key = new_key, a_type = "default"    )
        # print( "need next" )
        # 1/0
        # #self.data_manager.select_record( our_list[ new_ix ]  )

        self.append_msg( "<--- done" )

    # --------------------------
    def insert_copy( self,    ):
        """
        What it says
        """
        self.append_function_msg( "insert_copy or prior " )

        self.data_manager.new_record( next_key = None, option = "copy" )

        # self.new_key_ix    = self.new_key_ix  + 1
        # new_key            = key_gen( self.new_key_ix )
        # self.new_record(  next_key = new_key, a_type = "copy"  )
        # self.date_critera_widget.set_date_default()
        # self.date_edit_widget.set_data_default()
        self.append_msg( "<--- done" )

    # --------------------------
    def mutate_tbd( self, arg  ):
        """
        !!What it says
        """
        self.append_function_msg( "mutate_tbd" )

        self.date_critera_widget.set_date_default()
        self.date_edit_widget.set_data_default()

        self.append_msg( "<--- done" )

    # --------------------------
    def mutate_2_tbd( self, arg  ):
        """
        !!What it says
        """
        self.append_function_msg( "mutate_2_tbd" )
        what    = "add_record -- tbd"
        #print( f"{BEGIN_MARK_1}{what}{BEGIN_MARK_2}")
        self.append_msg( f"\n\n\ninspect { '' }  --------",   )
        self.date_critera_widget.set_date_default()
        self.date_edit_widget.set_data_default()

        self.append_msg( "<--- done" )

    # --------------------------
    def validate( self,   ):
        """
        validate all the fieds
        """
        self.append_function_msg( f"validate" )

        try:
            self.data_manager.validate()

        except Exception as an_except:   #  or( E1, E2 )

            msg     = f"in validate a_except         >>{an_except}<<  type  >>{type( an_except)}<<"
            self.append_msg( msg )

            msg     = f"an_except.args   >>{an_except.args}<<"
            self.append_msg( msg )

            s_trace = traceback.format_exc()
            msg     = f"format-exc       >>{s_trace}<<"
            self.append_msg( msg )


        #     #raise  # to reraise same
        # finally:
        #     msg     = f"in finally  {1}"
        #     print( msg )
        self.append_msg( "<--- done" )

    # -----------------------------------------
    def update_db( self, ):
        """
        from russ crud was in phototexttab, probably universal
        looks like can promote to ancestor
        """

        self.append_function_msg( f"update_db" )

        self.data_manager.update_db()

        self.append_msg( "<--- done" )

    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_0" )

        msg    = "so far not implemented "
        self.append_msg( msg, clear = False )

        self.append_msg( "<--- done" )

    # ------------------------
    def inspect(self):
        """
        the usual
        """
        self.append_function_msg( "inspect" )

        # make some locals for inspection
        my_tab_widget = self
        #parent_window = self.parent( ).parent( ).parent().parent()
        #self_id_field           = self.id_field
        self_name_field         = self.name_field
        self_age_field          = self.age_field
        #self_relation_field     = self.relation_field
        self_current_record_type       = self.current_record_type
        self_model              = self.model
        #self_field_list         = self.field_list
        self_data_manager       = self.data_manager

        # self_line_edit_1_widget   = self.line_edit_1_widget
        # self_line_edit_1_widget = self.line_edit_1_widget
        # self_date_edit_1_widget = self.date_edit_1_widget
        # self_date_edit_2_widget = self.date_edit_2_widget
        # self_line_edit_criteria_1_widget = self.line_edit_criteria_1_widget

        wat_inspector.go(
             msg            = "inspect this tab",
             # inspect_me     = self.people_model,
             a_locals       = locals(),
             a_globals      = globals(), )

        self.append_msg( "<--- done" )

    # ------------------------
    def breakpoint(self):
        """
        keep this in each object so user breaks into that object
        """
        self.append_function_msg( "breakpoint" )

        breakpoint()

        self.append_msg( "<--- done" )

# ---- eof