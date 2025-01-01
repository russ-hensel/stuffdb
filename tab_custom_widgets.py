#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 12:41:16 2024

"""
"""

KEY_WORDS:      some stuff rsh custom for stuffdb edit and criteria
CLASS_NAME:     CustomWidgetTab
WIDGETS:        CQLineEdit CQDateEdit CQLineEditCriteria CQDateCriteria
STATUS:         works 5/10
TAB_TITLE:      RSHCustomWidgets

         self.help_file_name     =  "find_this_file.txt"

"""
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main_qt
    #main.main()
# --------------------


# ---- tof
# # --------------------
# if __name__ == "__main__":
#     #----- run the full app
#     import qt_fitz_book
#     qt_fitz_book.main()
# # --------------------


import glob
import inspect
import json
import math
import os
import subprocess
import sys
import time
from collections import namedtuple
from datetime import datetime
from functools import partial
from random import randint
from subprocess import PIPE, STDOUT, Popen, run

import pyqtgraph as pg  # import PyQtGraph after PyQt5
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

# ---- end imports

print_func_header   = uft.print_func_header


# --------------------------------
def set_groupbox_style( groupbox ):
    """ """
    groupbox.setStyleSheet("""
        QGroupBox {
            border: 2px solid blue;
            border-radius: 10px;
            margin-top: 15px;
        }

        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 3px;
            background-color: white;
        }
    """)

#  --------
class CustomWidgetTab( QWidget ) :
    def __init__(self):
        """

        """
        super().__init__()
        self.help_file_name     =  uft.to_help_file_name( __name__ )

        self._build_gui()

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

        groupbox_criteria   = QGroupBox( "Criteria" )
        set_groupbox_style( groupbox_criteria )

        groupbox_edits      = QGroupBox( "Edits" )
        set_groupbox_style( groupbox_edits )

        button_layout       = QHBoxLayout( )

        layout.addWidget( groupbox_edits )
        g_layout            = QVBoxLayout( groupbox_edits  )

        # # ---- edits --------------------------------
        # layout.addWidget( groupbox_edits )
        # g_layout            = QVBoxLayout( groupbox_edits  )
        self._build_gui_in_gb_edit( g_layout )

        # ---- criteria --------------------------------
        layout.addWidget( groupbox_criteria )
        g_layout            = QVBoxLayout( groupbox_criteria  )
        self._build_gui_in_gb_criteria( g_layout )

        # ---- buttons
        layout.addLayout( button_layout )

        label       = "mutate_1\n"
        widget      = QPushButton( label )
        widget.clicked.connect( self.mutate_1 )
        button_layout.addWidget( widget )

        label       = "mutate_2\n"
        widget      = QPushButton( label )
        widget.clicked.connect( self.mutate_2 )
        button_layout.addWidget( widget )

        # ---- raise_except
        widget = QPushButton("raise\n_except")
        # widget.clicked.connect(lambda: self.print_message(widget.text()))
        a_widget        = widget
        widget.clicked.connect( lambda: self.raise_except( ) )
        button_layout.addWidget( widget )

        label       = "default\n"
        widget      = QPushButton( label )
        widget.clicked.connect( self.default )
        button_layout.addWidget( widget )

        label       = "examine_0\n"
        widget      = QPushButton( label )
        widget.clicked.connect( self.examine_0 )
        button_layout.addWidget( widget )

        # ---- PB inspect
        widget              = QPushButton("inspect\n")
        connect_to        = self.inspect
        widget.clicked.connect( connect_to )
        button_layout.addWidget( widget )

        # ---- PB breakpoint
        widget              = QPushButton("breakpoint\n ")
        connect_to          = self.breakpoint
        widget.clicked.connect( connect_to )
        button_layout.addWidget( widget )

    # ------------------------
    def _build_gui_in_gb_edit(self, layout  ):
        """
        build some of the gui in a groupbox
        """
        lbl_stretch         = self.lbl_stretch
        widget_stretch      = self.widget_stretch

        # ---- CQLineEdit
        b_layout        = QHBoxLayout( )
        layout.addLayout( b_layout )

        widget            = QLabel( "CQLineEdit_1")
        b_layout.addWidget( widget,  stretch = lbl_stretch )

        widget            = custom_widgets.CQLineEdit(  self, field_name   = "CQLineEdit_1",
                                                        display_type       = "string",
                                                        db_type            = "string" )
        self.line_edit_1_widget = widget
        b_layout.addWidget( widget,  stretch = widget_stretch )

        # ---- CQLineEdit_2
        b_layout        = QHBoxLayout( )
        layout.addLayout( b_layout )

        widget            = QLabel( "CQLineEdit_2")
        b_layout.addWidget( widget,  stretch = lbl_stretch )

        widget            = custom_widgets.CQLineEdit(  self, field_name    = "CQLineEdit_2", )
        self.line_edit_2_widget = widget
        b_layout.addWidget( widget,  stretch = widget_stretch )

        # ---- CQDateEdit_1
        b_layout        = QHBoxLayout( )
        layout.addLayout( b_layout )

        widget            = QLabel( "CQDateEdit_1")
        b_layout.addWidget( widget,  stretch = lbl_stretch )

        widget              = custom_widgets.CQDateEdit(  self, field_name    = "a field name", )
        self.date_edit_1_widget = widget
        b_layout.addWidget( widget,  stretch = widget_stretch )

        # ---- CQDateEdit_n
        b_layout        = QHBoxLayout( )
        layout.addLayout( b_layout )

        widget            = QLabel( "CQDateEdit_n:")
        b_layout.addWidget( widget,  stretch = lbl_stretch )

        widget            = custom_widgets.CQDateEdit(  self, field_name    = "a field name", )
        self.date_edit_2_widget = widget
        b_layout.addWidget( widget,  stretch = self.widget_stretch )


    def _build_gui_in_gb_criteria(self, layout  ):
        """
        build some of the gui in a groupbox
        """
        lbl_stretch        = self.lbl_stretch
        widget_stretch     = self.widget_stretch

        # ---- CQLineEditCriteria_1
        b_layout        = QHBoxLayout( )
        layout.addLayout( b_layout )

        widget            = QLabel( "CQLineEditCriteria_1 :")
        b_layout.addWidget( widget,  stretch = lbl_stretch )

        widget            = custom_widgets.CQLineEditCriteria(  self,   )
        self.line_edit_criteria_1_widget = widget
        b_layout.addWidget( widget,  stretch = widget_stretch )

        # ---- CQDateCriteria_1
        b_layout        = QHBoxLayout( )
        layout.addLayout( b_layout )

        widget            = QLabel( "CQDateCriteria_1:")
        b_layout.addWidget( widget,  stretch = self.lbl_stretch )

        widget            = custom_widgets.CQDateCriteria(    )
        self.date_critera_1_widget = widget
        # widget           = widget.container
        b_layout.addWidget( widget,  stretch = self.widget_stretch )

        widget            = QLabel( "CQDateCriteria_2:")
        b_layout.addWidget( widget,  stretch = self.lbl_stretch )

        widget            = custom_widgets.CQDateCriteria(    )
        self.date_critera_2_widget = widget
        # widget           = widget.container
        b_layout.addWidget( widget,  stretch = self.widget_stretch )

    # --------------------------
    def examine_0( self, arg  ):
        """
        set_data_to_default( self, from_prior_value = False ):
            # ------------------------------------
            def clear_data( self, to_prior ):

                def get_raw_data( self, ):
    #-----------------------------
    def validate( self ):
    #-----------------------------
    def set_data_to_default( self, from_prior_value = False ):
        """
        print_func_header( "examine_0" )


        widget        = self.line_edit_1_widget
        print( f"for line_edit_1_widget { str(widget)}")

        value     = "a_string_value"
        widget.set_data( value,  in_type = "string" )


        print( f"for line_edit_1_widget { str(widget)}")

        widget.set_data_to_default( to_prior = False )

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

            # Execute the message box and wait for a response
            msg_box.exec_()

    # ------------------------
    def inspect(self):
        """
        the usual
        """
        print_func_header( "inspect" )

        # make some locals for inspection
        my_tab_widget = self
        parent_window = self.parent( ).parent( ).parent().parent()

        self_line_edit_1_widget   = self.line_edit_1_widget
        self_line_edit_1_widget = self.line_edit_1_widget
        self_date_edit_1_widget = self.date_edit_1_widget
        self_date_edit_2_widget = self.date_edit_2_widget
        self_line_edit_criteria_1_widget = self.line_edit_criteria_1_widget

        wat_inspector.go(
             msg            = "inspect !! more locals would be nice ",
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