#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""


"""
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    main.main()
# --------------------

# ---- version
__version__   = "Ver 68: 2025 03 25.01"

import datetime
import inspect
import logging
import os
import random
import sys
import time

# ---- imports
import traceback

import app_logging
import data_dict
#import   stuffdb_def
import dict_main
import text_edit_ext
import wat_inspector
from app_global import AppGlobal
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import (PYQT_VERSION_STR,
                          QT_VERSION_STR,
                          QFile,
                          QFileInfo,
                          QSettings,
                          Qt,
                          QTimer,
                          QVariant)
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import (QIcon,
                         QImage,
                         QImageReader,
                         QImageWriter,
                         QKeySequence,
                         QPainter,
                         QPixmap)
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
# ---- QtSql
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt5.QtWidgets import (QAction,
                             QActionGroup,
                             QApplication,
                             QDockWidget,
                             QFileDialog,
                             QFrame,
                             QInputDialog,
                             QLabel,
                             QListWidget,
                             QMainWindow,
                             QMdiArea,
                             QMdiSubWindow,
                             QMenu,
                             QMessageBox,
                             QPushButton,
                             QSpinBox,
                             QTextEdit,
                             QVBoxLayout,
                             QWidget)

import key_gen
#import   mdi_management
import main_window
import parameters
import qsql_db_access
import sql_util

# ---- end imports

# or put in app_global ? "That is a No Go",

# ---------------
# from stuff_main_window import MainWindow

# -----------------------------
def delete_file( file_name ):
    """
    will delete any file, but intended for db file
    """
    exists    = str( os.path.isfile( file_name ) )
    # print( f"{file_name} exists {exists}" )

    if exists:
        try:
            os.remove( file_name )   # error if file not found
            print(f"delete_file removed {file_name} "  )

        except OSError as error:
            print( error )
            print( f"delete_file os.remove threw error on file {file_name} file probably does not exist this should be ok?")

    # else:
    #     print( f"file already gone  {file_name}                ")


# ============================================
class App( ):
    """
    this class is the "main" or controller for the whole app
    to run see end of this file
    it is the controller of an mvc app
    """
    def __init__( self,    ):
        """
        usual init for main app
        splash not working as desired, disabled
        splash screen which is of not help unless we sleep the init
        """
        self.version           = __version__
        self.app_name          = f"Stuff DB in QT {__version__}"
        #self.app_version       = self.version   # get rid of dupe at some point... app_version in gui_ext
        self.app_url           = "www.where"
        # clean out dead
        AppGlobal.controller   = self
        text_edit_ext.STUFF_DB = self
        self.gui               = None

        # ---- wat inspector

        self.restart( )

    # ----------------------------------
    def restart( self ):
        """
        use to restart the app without ending it
        this process can be very quick -- much quicker than a cold start
        this code is also an extension of __init__
        """
        print( "========= StuffDb restart =================" )

        self.q_app              = QApplication( []  )
        AppGlobal.q_app         = self.q_app

        self.parameters         = parameters.Parameters( )
        AppGlobal.parameters    = self.parameters

        app_logging.init()

        a_qsql_db_access        = qsql_db_access.QsqlDbAccess( )

        AppGlobal.qsql_db_access  = a_qsql_db_access

        self.sql_runner         = sql_util.SqlRunner( self.parameters.db_file_name )
        AppGlobal.sql_runner    = self.sql_runner

        a_key_gen               = key_gen.KeyGenerator( a_qsql_db_access.db  )  #  AppGlobal.qsql_db_access.db
        AppGlobal.key_gen       = a_key_gen

        data_dict.build_it( "stuffdb" )    # access as data_dict.DATA_DICT

        table_name_list  = data_dict.DATA_DICT.get_table_name_list()
        if len( table_name_list ) < 10:
            msg     = f"we seem to be short on data_dict items {len( table_name_list )}"
            logging.error( msg )
            for i_table in table_name_list:
                print( f"{i_table}")
            ValueError()

        self.main_window        = main_window.StuffdbMainWindow()
        AppGlobal.main_window   = self.main_window
        self.main_window.show()

        #rint( f"{AppGlobal.logger = }")

        self.prog_info()
        #rint( f"{AppGlobal.logger = }")
        AppGlobal.logger.debug( "self.q_app.exec_() next" )
        a_wat_inspector  = wat_inspector.WatInspector( self.q_app )
        # dialog       = wat_inspector.DisplayWat( self.q_app )
        self.q_app.exec_()   # perhaps move to run method

    # --------------------------------------------
    def prog_info( self,  ):
        """
        record info about the program to the log file
        """
        #logger_level( "until_foo.prog_info"  )
        fll         = AppGlobal.force_log_level
        logger      = logging.getLogger( )
        # logger      = self.logger
        logger.log( fll, "" )
        logger.log( fll, "============================" )
        logger.log( fll, "" )
        title       =   ( f"Application: {self.app_name} in mode {AppGlobal.parameters.mode}"
                          f"and version  {self.version}" )
        logger.log( fll, title )
        logger.log( fll, "" )

        if len( sys.argv ) == 0:
            logger.info( "no command line arg " )
        else:
            for ix_arg, i_arg in enumerate( sys.argv ):
                msg = f"command line arg + {str( ix_arg ) }  =  { i_arg })"
                logger.log( AppGlobal.force_log_level, msg )

        msg          = f"current directory {os.getcwd()}"
        logger.log( fll, msg  )

        start_ts     = time.time()
        dt_obj       = datetime.datetime.utcfromtimestamp( start_ts )
        string_rep   = dt_obj.strftime('%Y-%m-%d %H:%M:%S')
        msg          = f"Time now: {string_rep}"
        logger.log( fll, msg )
        # logger_level( "Parameters say log to: " + self.parameters.pylogging_fn )
                         # parameters and controller not available can get fro logger_level

    # ----------------------------------------------
    def os_open_help( self,  ):
        """
        what it says, read ... see menu may not be used

        """
        AppGlobal.os_open_help_file( AppGlobal.parameters.help_file )

    # ----------------------------------------------
    def os_open_log( self,  ):
        """
        have function since want flush

        """
        my_logging   = app_logging.APP_LOGGING
        my_logging.os_open_log_file
        return

    # ----------------------------------------------
    def os_open_parmfile( self,  ):
        """
        used as callback from gui button
        """
        # a_filename = self.starting_dir  + os.path.sep + "parameters.py"
        AppGlobal.os_open_txt_file( "parameters.py" )

    # ----------------------------------------------
    def os_open_gui_log( self,  ):
        """
        gui log logs what is sent to the gui message area
        used as callback from gui button
        """
        # a_filename = self.starting_dir  + os.path.sep + "parameters.py"
        AppGlobal.os_open_txt_file(  self.parameters.gui_text_log_fn )

def main():
    app         = App(   )
    # mainWin     = stuff_db_main_window.StuffDbMainWindow()
    # mainWin.show()
    sys.exit( 99 )
#  # app         = QApplication( sys.argv )
#  # mainWin     = stuff_db_main_window.StuffDbMainWindow()
#  # mainWin.show()
#  # sys.e


# ---- eof
