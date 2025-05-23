#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""

KEY_WORDS:      custom picture viewer plus rsh    stagetwo
CLASS_NAME:      PictureViewerPlusTab
WIDGETS:         PictureViewerPlus
STATUS:         runs_correctly_0_10      demo_complete_2_10   !! review_key_words   !! review_help_0_10
TAB_TITLE:     PictureViewerPlus

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
import tab_base

# ---- end imports


#  --------
class PictureViewerPlusTab( tab_base.TabBase ) :
    def __init__(self):
        """

        """
        super().__init__()
        self.help_file_name     =  "find_this_file.txt"


        self.ix_file_list      = -1
        self.file_list         = [
                                    "/mnt/WIN_D/PhotoDB/08/dsc00700.jpg",
                                        "/mnt/WIN_D/PhotoDB/08/dsc00701.jpg",
                                            "/mnt/WIN_D/PhotoDB/08/dsc00702.jpg",
                                            "/mnt/WIN_D/PhotoDB/08/dsc00703.jpg",

                                    ]

        self.mutate_dict[0]    = self.mutate_0
        self.mutate_dict[1]    = self.mutate_1
        # self.mutate_dict[2]    = self.mutate_2
        # self.mutate_dict[3]    = self.mutate_3
        # self.mutate_dict[4]    = self.mutate_4




        self._build_gui()


    def _build_guixxx(self,   ):
        """
        all build on a local QWidget
        count : const int
        currentData : const QVariant
        currentIndex : int
        """
        tab_page      = self

        layout        = QVBoxLayout( tab_page )

    def _build_gui_widgets(self, main_layout  ):
        """
        the usual, build the gui with the widgets of interest
        and the buttons for examples
        """
        layout              = QVBoxLayout(   )

        main_layout.addLayout( layout )
        button_layout        = QHBoxLayout(   )

        button_layout = QHBoxLayout( )

        widget        = picture_viewer.PictureViewerPlus(   )
        self.viewer   = widget
        layout.addWidget( widget )

        # ---- buttons
        layout.addLayout ( button_layout )

        # label       = "add buttons "
        # widget      = QPushButton( label )
        # #widget.clicked.connect( self.combo_reload )
        # button_layout.addWidget( widget )

        label       = "mutate\n"
        widget      = QPushButton( label )
        widget.clicked.connect( self.mutate )
        button_layout.addWidget( widget )

        # ----
        label       = "inspect\n"
        widget      = QPushButton( label )
        widget.clicked.connect( self.inspect )
        button_layout.addWidget( widget )


        # ---- breakpoint
        label       = "breakpoint\n"
        widget      = QPushButton( label )
        widget.clicked.connect( self.breakpoint )
        button_layout.addWidget( widget )


    # --------------------------
    def mutatexxx( self, arg  ):
        """
        now wrap logic  --- make change picture
        """
        self.ix_file_list           += 1
        self.viewer.display_file( self.file_list[ self.ix_file_list ] )
        self.viewer.display_info()


    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_0" )

        msg    = "so far not implemented "
        self.append_msg( msg, clear = False )

    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_1" )

        msg    = "so far not implemented "
        self.append_msg( msg, clear = False )


    # ------------------------
    def inspect(self):
        """
        the usual
        """
        self.append_function_msg( "inspect" )

        # make some locals for inspection
        my_tab_widget = self
        parent_window = self.parent( ).parent( ).parent().parent()

        wat_inspector.go(
             msg            = "inspect !! add more locals ",
             # inspect_me     = self.people_model,
             a_locals       = locals(),
             a_globals      = globals(), )

    # ------------------------
    def breakpoint(self):
        """
        each tab gets its own function so we break in that
        tabs code
        """
        self.append_function_msg( "breakpoint" )

        breakpoint()

