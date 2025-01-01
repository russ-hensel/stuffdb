#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""

KEY_WORDS:      custom picture viewer rsh
CLASS_NAME:      PictureViewerTab
WIDGETS:         PictureViewer
STATUS:         unknown
TAB_TITLE:     PictureViewer

         self.help_file_name     =  "find_this_file.txt"

"""
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main_qt
    #main.main()
# --------------------
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
import picture_viewer


# ---- end imports

print_func_header   = uft.print_func_header


#  --------
class PictureViewerTab( QWidget ) :
    def __init__(self):
        """

        """
        super().__init__()
        self.help_file_name     =  "find_this_file.txt"

        self._build_gui()

    # -----------------------------
    def _build_gui(self,   ):
        """
        all build on a local QWidget
        count : const int
        currentData : const QVariant
        currentIndex : int
        """

        tab_page      = self

        layout        = QVBoxLayout( tab_page )
        button_layout = QHBoxLayout( )

        widget        = picture_viewer.PictureViewer(   )
        self.viewer   = widget
        layout.addWidget( widget )
        # ---- QGroupBox
        #groupbox   = QGroupBox()
        # groupbox   = QGroupBox( "QGroupBox 1" )   # version with title
        # layout.addWidget( groupbox )
        # layout_b     = QHBoxLayout( groupbox  )
        # self.build_gui_in_groupbox( layout_b )

        # ---- buttons
        layout.addLayout ( button_layout )

        label       = "add buttons\n and actions"
        widget      = QPushButton( label )
        #widget.clicked.connect( self.combo_reload )
        button_layout.addWidget( widget )



        # # ----
        # label       = "inspect"
        # widget      = QPushButton( label )
        # widget.clicked.connect( self.inspect )
        # button_layout.addWidget( widget )

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


    # --------------------------
    def examine( self, arg  ):
        """
        count : const int
        currentData : const QVariant
        currentIndex : int
        currentText : QString
        duplicatesEnabled : bool
        editable : bool
        """
        print_func_header( "examine ...... think xxx " )
        print( f"Inspect picture_viewer  { '' }  --------",   )

        wat.short( self.viewer )
        wat_says   = wat.str( self.viewer )
        print( f"\n\n\n-----------------------------------\n{wat_says}")
        pass


    # ------------------------
    def inspect(self):
        """
        the usual
        """
        print_func_header( "inspect" )

        # make some locals for inspection
        my_tab_widget = self
        # combo_1       = self.combo_1
        # combo_2       = self.combo_2
        wat_inspector.go(
             msg            = "inspect -- need more locals ",
             a_locals       = locals(),
             a_globals      = globals(), )

    # ------------------------
    def breakpoint(self):
        """
        each tab gets its own function so we break in that
        tabs code
        """
        print_func_header( "breakpoint" )
        breakpoint()

