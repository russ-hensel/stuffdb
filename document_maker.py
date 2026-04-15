#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 11:33:31 2024

@author: russ
"""


# --------------------
if __name__ == "__main__":
    import main
    main.main()
# --------------------


# ---- imports



# ---- begin pyqt from import_qt.py

# ---- QtCore

# ----QtWidgets






# ----QtWidgets Boxs, Dialogs

# ---- QtSql


# ---- imports more

#import sqlite3
#from PyQt5.QtGui import QIntValidator



#from   functools import partial
#import collections
#import functools

# ---- imports local

from   app_global import AppGlobal

import help_sub_window
import stuff_sub_window
import photo_sub_window
import photoshow_sub_window

# import sys
# import sqlite3
# from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
#                              QTabWidget, QLabel, QMessageBox)
# from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlRecord
# from PyQt5.QtGui import QIntValidator
#import  qt_sql_query
#import  channel_sub_window

# ----------------------------------------
class DocumentMaker(   ):

    def __init__(self,  ):
        # super().__init__()
        # self.setWindowTitle(title)
        self.counter   = 0

    # -------------------------
    def add_subwindow_is_it_used( self,  window_type ):
        """
        from chat_subwindow.py
        full of errors is it used
        """
        msg              = f"add_subwindow for window_type {window_type }"
        # mdi_area       = self.main_window.mdi_area

        # AppGlobal.main_window
        mdi_area       = AppGlobal.main_window.mdi_area
        self.counter   += 1

        if  window_type == "2tabs":
            sub_window      = TwoTabSubWindow()


        # elif  window_type == "channel":
        #     sub_window      = channel_sub_window.ChannelSubWindow()

        elif  window_type == "help":
            sub_window      = help_sub_window.HelpSubWindow()

        elif  window_type == "photo":
            sub_window      = photo_sub_window.PhotoSubWindow()

        elif  window_type == "photoshow":
            sub_window      = photoshow_sub_window.PhotoshowSubWindow()

        elif  window_type == "stuff":
            sub_window      = stuff_sub_window.StuffSubWindow()

        elif  window_type == "criteria":
            sub_window      = CriteriaSubWindow()

        elif  window_type == "tab_in_tab":
            sub_window      = TabInTabSubWindow()

        elif  window_type == "chat_criterria":
            sub_window      = ChatCriteriaSubWindow()

        else:
            1/0
            #sub_window      = CriteriaSubWind


# ---- eof



