#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 12:41:16 2024

"""
"""

KEY_WORDS:      some stuff rsh custom  edit with sql model for forms and fields zz
CLASS_NAME:     CustomEditWidgetTab
WIDGETS:        CQLineEdit CQDateEdit QSqlTableModel
STATUS:         dev 2/10
TAB_TITLE:      RSHCustom_EditWidgets

         self.help_file_name     =  "find_this_file.txt"

"""
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main_qt
    #main.main()
# --------------------


# ---- tof


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

FIF       = info_about.INFO_ABOUT.find_info_for



# ---- end imports


RECORD_NULL         = 0
RECORD_FETCHED      = 1
RECORD_NEW          = 2
RECORD_DELETE       = 3

INDENT              = uft.INDENT
print_func_header   = uft.print_func_header

new_keys     = [ 5001, 5002, 5003, 5004,5005, 5006, 5007 ]

def key_gen( ix ):
    """this is junk and will only work a few times
    """
    return new_keys[ ix ]


#  --------
class CustomEditWidgetTab( QWidget ) :
    def __init__(self):
        """

        """
        super().__init__()
        self.help_file_name     =  uft.to_help_file_name( __name__ )

        self.current_id        = -1       # invalid but prir next should fix
        self.id_list           = [ 1000, 1001, 1002, 1003, 1004, 3 ]
        self.ix_id_list        = 0    # where we are in self.id_list
        self.field_list        = []
        self.new_key_ix        = 0
        self._build_model()
        self._build_gui()
        self.current_record_type = RECORD_NULL

    # ------------------------------
    def _build_gui(self,   ):
        """
        all build on a local QWidget
        count : const int
        currentData : const QVariant
        currentIndex : int

        edits

        criteria

        """
        tab_page        = self
        lbl_stretch     = 0
        widget_stretch  = 3

        self.lbl_stretch     = lbl_stretch
        self.widget_stretch  = widget_stretch

        layout              = QVBoxLayout( tab_page )

        self._build_gui_form( layout )

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

    # ------------------------------
    def _build_model( self,   ):
        """
        build model and views if used here

        """
        sql     = """
            CREATE TABLE people (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                name            TEXT NOT NULL,
                age             INTEGER,
                family_relation TEXT
            )
        """

        # ---- people
        model                  = QSqlTableModel( self, global_vars.EX_DB   )
        self.model             = model
        model.setTable( 'people' )

        model.setEditStrategy( QSqlTableModel.OnManualSubmit )

        print( "make a second model to see if any interaction ")

        model                  = QSqlTableModel( self, global_vars.EX_DB   )
        self.model_2           = model
        model.setTable( 'people' )

        model.setFilter( f"" )
        model.select()
        #ia_qt.q_sql_query_model( model, "select_record 2" )


        print( FIF( self.model,   msg = "_build_model self.mode    post filter and select  " ) )
        print( FIF( self.model_2, msg = "_build_model self.model_2 post filter and select  " ) )


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
    def _build_gui_form(self, layout  ):
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
        edit_field.set_data_to_default    = edit_field.set_data_to_pass

        self.id_field         = edit_field
        self.field_list.append( edit_field )
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
        edit_field.set_data_to_default      = edit_field.do_data_to_self_default
            # should already be set

        edit_field.default_value            = "custom default for name"

        a_partial                           = partial( edit_field.do_data_to_default_value, "**" )
        edit_field.set_data_to_default      = a_partial

        if not name_in_text_edit:
            self.name_field      = edit_field

        # self.field_list.append( edit_field )
        # row_layout.addWidget( edit_field )

        # ----  age
        edit_field           = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "age",
                                                db_type        = "integer",
                                                display_type   = "string" )

        self.age_field         = edit_field

        # ---- ....one of next two
        #a_partial                         = partial( edit_field.validate_max_length, max_len = 5 )
        edit_field.validate               = edit_field.validate_is_int

        a_partial                         = partial( edit_field.validate_max_int, max_int = 99 )
        edit_field.validate               = a_partial

        self.field_list.append( edit_field )
        row_layout.addWidget( edit_field )


        # ----  family_relation
        edit_field           = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "family_relation",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.relation_field         = edit_field

        self.field_list.append( edit_field )
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
        if name_in_text_edit:
            self.name_field      = edit_field

        self.field_list.append( edit_field )
        row_layout.addWidget( edit_field )


    # --------------------------
    def examine( self, arg  ):
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
        print_func_header( "examine" )

        a_timestamp    = self.date_edit_2_widget.get_data_as_timestamp()

        #rint( f"inspect date_edit_2_widget.get_data_as_timestamp() { a_timestamp = }",   )


        print( "line edit ---------------")
        widget    = self.line_edit_1_widget
        msg       = f"{widget.data_value = }"
        print( msg )

        widget.data   = "changed data with @property.setter"

        widget    = self.line_edit_1_widget
        msg       = f"{widget.data_value = }"
        print( msg )

        # ---- edits
        msg       = "\nFor the edit widgets:"
        msg       = f"{self.date_edit_1_widget.data_value = }"
        print( msg )
        msg       = f"{self.date_edit_2_widget = }"
        print( msg )
        msg       = f"{ self.line_edit_1_widget = }"
        print( msg )
        msg       = f"{self.line_edit_2_widget = }"
        print( msg )

        print( f"inspect end { '' } --------",  )

    # --------------------------
    def default( self, arg  ):
        """
        !!What it says
        """
        print_func_header( "default" )

        print( f"\n\n\ndefaultt { '' }  --------",   )

        print( "self.line_edit_1_widget" )
        widget       =   self.line_edit_1_widget
        widget.set_data_default()

        widget       =   self.line_edit_2_widget
        widget.set_data_default()

        print( "self.line_edit_1_widget" )
        print( "self.line_edit_1_widget" )
        widget       =    self.date_edit_1_widget
        widget.set_data_default()


        print( "self.line_edit_2_widget" )
        widget       =    self.date_edit_2_widget
        widget.set_data_default()


        print( "self.date_criteria_1_widget" )
        widget       =   self.date_critera_1_widget
        widget.set_date_default()

    # # --------------------------
    # def set_to_edits_1( self, arg  ):
    #     """
    #     first set to edits
    #     """
    #     widget        = self.line_edit_1_widget
    #     print_func_header( "set_to_edits_1" )
    #     widget.clear_data(  )
    #     set_data( data, widget.db_type, )


    # ------------------------
    def record_to_field(self, record ):
        """
        What it says
        taken from stuff and simplifed
        move data from fetched record into the correct fields
        """
        print_func_header( f"record_to_field {record = }" )

        # ---- code_gen: detail_tab -- _record_to_field -- begin code
        for i_field in  self.field_list:
            i_field.set_data_from_record( record )

        #msg    = "but we do not have text data so lets kluge something together "

    # ------------------------
    def new_fields(self, a_type ):
        """
        What it says
        taken from stuff and simplifed
        move data from fetched record into the correct fields
        """
        print_func_header( f"new_fields {a_type = }" )

        # ---- code_gen: detail_tab -- _record_to_field -- begin code
        for i_field in  self.field_list:
            pass
            #i_field.set_data_from_record( record )


    # -------------------------------------
    def new_record( self, next_key, a_type ):
        """
        from stuff simplified, not finished
        looks a bit like default new row
        promoted  --  ok ??
        """
        print_func_header( f"new_record {next_key = } {a_type = }" )

        self.id_field.set_data( next_key, "integer" )

        self.current_id             = next_key
        self.current_record_type    = RECORD_NEW

        if  a_type == "copy":
            print( "not done yet ")
            self.field_list
            for i_field in  self.field_list:
                i_field.set_data_to_prior()

        elif a_type == "default":
            print( "not done yet ")
            self.field_list
            for i_field in  self.field_list:
                i_field.set_data_to_default()

        elif a_type == "clear":
            print( "not done yet ")
            self.field_list
            for i_field in  self.field_list:
                i_field.set_data_to_default()


        return


        self.new_fields( to_prior = False )


        #self.record_state       = RECORD_NEW

        # think we need to use custon_widget
        #self.id_field.setText( str( next_key ) )
        self.id_field.set_data( next_key, "integer" )

        self.current_id         = next_key

    # --------------------------
    def select_by_id( self, a_id   ):
        """
        What it says
        taken from stuff and simplifed
        """
        print_func_header( f"select_by_id {a_id = }" )

        record   = None
        model    = self.model

        # assumes success
        self.current_id             = a_id
        self.current_record_type    = RECORD_FETCHED

        #ia_qt.q_sql_query_model( model, "select_record 1" )
        model.setFilter( f"id = {a_id}" )
        model.select()
        #ia_qt.q_sql_query_model( model, "select_record 2" )

        print( f"{INDENT}select_by_id{model.rowCount() = }  ")

        print(  FIF( model, msg = "select_by_id post filter and select " ) )

        if model.rowCount() > 0:
            record                  = model.record(0)
            self.id_field.setText( str(record.value("id")) )
            self.record_to_field( record )
            #self.textField.setText(record.value("text_data"))
            #self.record_state       = RECORD_FETCHED
            self.current_id         = a_id

        else:
            msg    = f"Record not found! {a_id = }"
            print( msg )
            #AppGlobal.logger.error( msg )
            #QMessageBox.warning(self, "Select",  msg )
        #ia_qt.q_sql_query_model( model, "select_record 3 ancestor " )
        # model.setFilter("")  # why what happens if we leave alone
              # comment out here seems to fix history should be ok across all tabs
        #ia_qt.q_sql_query_model( model, "select_record 4  ancestor" )

    # may be more like events plantings....  remove Picture soon ? or keep as special

        # if record:
        #     #rint( "in DetailTabBase, now dowing history probably only place should be done on select look for other calls  ")
        #     self.parent_window.record_to_history_table( record )

        # if self.pictures_tab:
        #     self.pictures_tab.select_by_id( id_value )


    # --------------------------
    def prior_next( self, delta  ):
        """
        What it says
        delta may be positive or negative
        """
        print_func_header( f"prior_next {delta = }" )

        ix                     = self.ix_id_list
        our_list               = self.id_list
        max                    = len( our_list )

        new_ix                 = ix + delta

        if   new_ix < 0:
            print( "wrap to max ix")
            new_ix  = max - 1

        elif new_ix >= max:
            print( "wrap to ix = 0")
            new_ix  = 0

        self.ix_id_list   = new_ix
        #return new_ix

        self.select_by_id( our_list[ new_ix ]  )

    # -------------------------------------
    def insert_default( self,   ):
        """
        what it says
        test edits for default behaviour
        """
        print_func_header( "insert_default" )
        self.record_state = RECORD_NEW

        self.new_key_ix    = self.new_key_ix  + 1
        new_key            = key_gen( self.new_key_ix )
        self.new_record(  next_key = new_key, a_type = "default"    )

    # --------------------------
    def insert_copy( self,    ):
        """
        What it says
        """
        print_func_header( "insert_copy or prior " )
        self.new_key_ix    = self.new_key_ix  + 1
        new_key            = key_gen( self.new_key_ix )
        self.new_record(  next_key = new_key, a_type = "copy"  )
        # self.date_critera_widget.set_date_default()
        # self.date_edit_widget.set_data_default()


    # --------------------------
    def mutate_1( self, arg  ):
        """
        !!What it says
        """
        print_func_header( "mutate_1" )

        self.date_critera_widget.set_date_default()
        self.date_edit_widget.set_data_default()

    # --------------------------
    def mutate_2( self, arg  ):
        """
        !!What it says
        """
        print_func_header( "mutate_2" )
        what    = "add_record -- tbd"
        #print( f"{BEGIN_MARK_1}{what}{BEGIN_MARK_2}")
        print( f"\n\n\ninspect { '' }  --------",   )
        self.date_critera_widget.set_date_default()
        self.date_edit_widget.set_data_default()


    # --------------------------
    def validate( self,   ):
        """
        validate all the fieds
        """
        print_func_header( f"validate" )

        try:

            for i_field in  self.field_list:
                i_field.validate()

        except Exception as an_except:   #  or( E1, E2 )

            msg     = f"a_except         >>{an_except}<<  type  >>{type( an_except)}<<"
            print( msg )

            s_trace = traceback.format_exc()
            msg     = f"format-exc       >>{s_trace}<<"
            print( msg )

            #raise  # to reraise same
        # finally:
        #     msg     = f"in finally  {1}"
        #     print( msg )


    # --------------------------
    def raise_except( self,   ):
        """

        """
        try:
            raise custom_widgets.ValidationIssue( "why o why", self )

        except custom_widgets.ValidationIssue  as an_except:
            #an_except.why, an_except.this_control
            # msg     = f"a_except         >>{an_except}<<  type  >>{type( an_except)}<<"
            # print( msg )

            # msg     = f"an_except.args   >>{an_except.args}<<"
            # print( msg )

            # s_trace = traceback.format_exc()
            # msg     = f"format-exc       >>{s_trace}<<"
            # print( msg )
            # AppGlobal.logger.error( msg )   #    AppGlobal.logger.debug( msg )
            msg     = an_except.args[0]
            print( f"{msg = }" )
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Input Issue")
            msg_box.setText( msg )

            # Adding buttons
            choice_a = msg_box.addButton( "Ok", QMessageBox.ActionRole)
            # choice_b = msg_box.addButton( "Choice B", QMessageBox.ActionRole)

            # Set the dialog to be modal (blocks interaction with other windows)
            msg_box.setModal( True )

            msg_box.exec_()


    # -----------------------------------------
    def update_db( self, ):
        """
        from russ crud was in phototexttab, probably universal
        looks like can promote to ancestor
        """

        print_func_header( f"update_db {self.current_record_type = }  " )


        record_state   = self.current_record_type
        if   record_state   == RECORD_NULL:
            print( "update_db record null no action, return ")
            return
            # if self.key_word_table_name:
            #     self.key_word_obj.string_to_new(( self.get_kw_string()) )

        elif  record_state   == RECORD_NEW:
            self.update_new_record()
            # if self.key_word_table_name:
            #     self.key_word_obj.string_to_new(( self.get_kw_string()) )

        elif  record_state   == RECORD_FETCHED:
            1/0
            self.update_record_fetched()
            # if self.key_word_table_name:
            #     self.key_word_obj.string_to_new(( self.get_kw_string()) )

        elif  record_state   == RECORD_DELETE:
            1/0
            # self.delete_record_update()
            # if self.key_word_table_name:
            #     self.key_word_obj.string_to_new( "" )

        else:
            print( f"update_db wtf  {self.record_state = } ")
        # if self.key_word_table_name:
        #     self.key_word_obj.compute_add_delete( self.current_id  )
        #rint( f"update_db record state now:  {self.record_state = } ")
        #rint( "what about other tabs and subtabs")

    # ---------------------------
    def update_new_record( self ):
        """
        from russ crud worked   --- from photo_text -- worked
        photo-detal ng need edit trying worked --- move to ancestor

        """
        print( f"DetailTabBase update_new_record  {self.record_state  = }")
        model   = self.tab_model     # QSqlTableModel(
        if not self.record_state  == RECORD_NEW:
            msg       = ( f"save_new_record bad state, return  {self.record_state  = }")
            print( msg )
            return

        record  = model.record()

        self.field_to_record( record )

        model.insertRecord( model.rowCount(), record )

        #model.submitAll()
        if self.mapper:
            self.mapper.submit()
        else:
            record = model.record(0)
            self.field_to_record(  record )
            model.setRecord(0, record)

        ok   = model_submit_all( model, f"DetailTabBase.update_new_record { self.current_id = } ")

        self.record_state    = RECORD_FETCHED
        # msg      =  f"New record saved! { self.current_id = } "
        # rint( msg )
        #QMessageBox.information(self, "Save New", msg )




    # ------------------------
    def inspect(self):
        """
        the usual
        """
        print_func_header( "inspect tbd" )

        # make some locals for inspection
        my_tab_widget = self
        #parent_window = self.parent( ).parent( ).parent().parent()
        self_id_field           = self.id_field
        self_name_field         = self.name_field
        self_age_field          = self.age_field
        self_relation_field     = self.relation_field
        self.current_record_type       = self.current_record_type
        self_model              = self.model
        self_field_list         = self.field_list


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

    # ------------------------
    def breakpoint(self):
        """
        keep this in each object so user breaks into that object
        """
        print_func_header( "breakpoint" )
        breakpoint()


# ---- eof