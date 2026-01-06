#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 13 16:02:45 2025

@author: russ
"""

# ---- tof

# --------------------
if __name__ == "__main__":
    import main
# --------------------

# ---- imports
# import functools
# import inspect
#import logging
#import pprint
# import subprocess
# import os
import time

#from functools import partial
from pathlib import Path

from qt_compat import QApplication, QAction, exec_app, qt_version
from PyQt.QtWidgets import QMainWindow, QToolBar, QMessageBox
from qt_compat import Qt, DisplayRole, EditRole, CheckStateRole
from qt_compat import TextAlignmentRole
from qt_compat import QSizePolicy_Expanding, QSizePolicy_Minimum  # and look at qt_compat there may be more




from PyQt.QtCore   import ( QDate, QModelIndex, Qt, QTimer, pyqtSlot,  QThread, pyqtSignal )



from PyQt.QtCore   import Qt, QDateTime
from PyQt.QtWidgets import QStyledItemDelegate
from PyQt.QtGui import (QFont,
                         QIntValidator,
                         QStandardItem,
                         QStandardItemModel,
                         QTextCursor)

from PyQt.QtSql import (QSqlDatabase,
                         QSqlQuery,
                         QSqlQueryModel,
                         QSqlRelation,
                         QSqlRelationalDelegate,
                         QSqlRelationalTableModel,
                         QSqlTableModel)

#from PyQt.QtGui import ( QAction, QActionGroup, )

from PyQt.QtWidgets import (
                             QFileDialog,
                             QApplication,
                             QButtonGroup,
                             QCheckBox,
                             QComboBox,
                             QDialog,
                             QDateEdit,
                             QDockWidget,
                             QFileDialog,
                             QFrame,
                             QGroupBox,
                             QGridLayout,
                             QHBoxLayout,
                             QHeaderView,
                             QInputDialog,
                             QLabel,
                             QLineEdit,
                             QListWidget,
                             QMainWindow,
                             QMdiArea,
                             QMdiSubWindow,
                             QMenu,
                             QMessageBox,
                             QPushButton,
                             QSpacerItem,
                             QSpinBox,
                             QSizePolicy,
                             QTableView,
                             QTableWidget,
                             QTableWidgetItem,
                             QTabWidget,
                             QTextEdit,
                             QVBoxLayout,
                             QWidget)

# import collections
# import parameters
# import data_dict
# import check_fix

# #import gui_qt_ext
import info_about
#import key_words
#import string_util
#import text_edit_ext
#import table_model
# import wat_inspector
# from app_global     import AppGlobal
# import qsql_utils

#import ex_qt
#import exec_qt
#import mdi_management


# ---- import end


#--------------------------------------
class HelperThread( QThread ):
    update_signal       = pyqtSignal(str)
    finished_signal     = pyqtSignal()

    #-------------------------
    def __init__(self, task_function, task_function_arg ):
        super().__init__()
        self._running = True

        self.task_function     = task_function
        self.task_function_arg = task_function_arg


    #-------------------------
    def run(self):
        """



        """
        self._running = True

        if self.task_function is None:
            for ix in range(5):
                if not self._running:
                    break
                self.update_signal.emit( str(ix) )
                time.sleep(0.5)

        else:
            self.task_function( self, self.task_function_arg )
                # self =HelperThread, so we can send back messages

        self.cleanup()
        self.finished_signal.emit()

    #-------------------------
    def stop(self):
        """

        """
        self.cleanup()
        self._running = False

    #-------------------------
    def cleanup(self):
         """
         to allow a second run i hope
         did not work try in dialog
         """
         msg     = f"thread cleanup {1}"
         print( msg )

         self.task_function     = None
         self.task_function_arg = None


#-------------------------------------
class ProgressDialog( QDialog ):


    def __init__(self, parent=None, *, dialog_args = {}, task_function = None, task_function_arg = None ):

        super().__init__(parent)

        self.task_function      = task_function
        self.task_function_arg  = task_function_arg


        # ---- build gui
        title   = dialog_args.get( "title", None )
        if title is None:
            title  = "default_progress_dialog"

        self.setWindowTitle( title )
        self.resize(300, 200)

        # Layout
        main_layout         = QVBoxLayout(self)
        widget              = QTextEdit(self)
        self.text_area      = widget
        widget.setReadOnly(True)
        main_layout.addWidget( widget )

        button_layout = QHBoxLayout()

        widget              = QPushButton("Stop -- not implemented yet", self)
        self.stop_button    = widget
        # Connect stop button
        widget.clicked.connect( self.stop_thread )
        button_layout.addWidget( widget )
        main_layout.addLayout(button_layout)

        # Thread setup
        self.thread = HelperThread( task_function     = self.task_function,
                                    task_function_arg = self.task_function_arg )

        self.thread.update_signal.connect( self.update_text )

        self.thread.finished_signal.connect( self.close )

    #-------------------------
    def start_thread(self):
        """ """
        self.text_area.clear()
        if not self.thread.isRunning():
            self.thread.start()
        msg   = "dialog start_thread() end"
        print( msg )
        self.cleanup()

    #-------------------------
    def stop_thread(self):
        """ """
        msg     = "ProgressDialog.stop_thread()"
        print( msg )
        self.cleanup()
        if self.thread.isRunning():
            self.thread.stop()

    #-------------------------
    def update_text(self, text):
        self.text_area.append(text)


    #-------------------------
    def cleanup(self):
         """
         to allow a second run i hope

         """
         msg     = f"dialog cleanup {1}"
         print( msg )
         self.task_function     = None
         self.task_function_arg = None

# ---- eof