#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""
the "true" main for the stuffdb, but launch from main

"""
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
# --------------------

# ---- version
__version__   = "Ver .085: 2026-02-10.01"

# ---- imports
import datetime
import inspect
import logging
import os
#import random
import sys
import time
import traceback

from qt_compat      import QApplication, QAction, QActionGroup, exec_app, qt_version
from PyQt.QtWidgets import QMainWindow, QToolBar, QMessageBox


from PyQt import QtWidgets, uic
from PyQt.QtCore import (PYQT_VERSION_STR,
                          QT_VERSION_STR,
                          QFile,
                          QFileInfo,
                          QSettings,
                          Qt,
                          QTimer,
                          QVariant)
from PyQt.QtCore import pyqtSignal as Signal
from PyQt.QtCore import pyqtSlot
from PyQt.QtGui import (QIcon,
                         QImage,
                         QImageReader,
                         QImageWriter,
                         QKeySequence,
                         QPainter,
                         QPixmap)
from PyQt.QtPrintSupport import QPrintDialog, QPrinter

from PyQt.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel

#from PyQt.QtGui import ( QAction, QActionGroup, )


from PyQt.QtWidgets import (
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

from   app_global import AppGlobal
# import app_logging
import data_dict
#import   stuffdb_def
#import dict_main
import text_edit_ext
import wat_inspector
import key_gen
#import   mdi_management
import main_window
import parameters
import qsql_db_access
import sql_util
#import parameter_check
# ---- end imports

STUFFDB_CONNECTION_NAME    = "stuffdb_main_connection_name"

# stuffdb.DB_CONNECTION_NAME
# from stuffdb import DB_CONNECTION_NAME

# -----------------------------
def delete_file( file_name ):
    """
    will delete any file, but intended for db file
    """
    exists    = str( os.path.isfile( file_name ) )

    if exists:
        try:
            os.remove( file_name )   # error if file not found
            debug_msg  = (f"delete_file removed {file_name} "  )
            logging.debug( debug_msg )

        except OSError as error:
            debug_msg  = ( f"delete_file os.remove threw error on file {file_name} file probably does not exist this should be ok? {error}")
            logging.debug( debug_msg )


# -----------------------
class StuffApplication( QtWidgets.QApplication ):
    """
    from gok then modified
    to let me manage the uncaught exeeptions

    not doing what I want for now
    """
    def notify(self, receiver, event):
        try:
            return super().notify(receiver, event)
        except Exception as e:
            # Log or print the exception
            print(f"\n================================== Exception in event handler: {e} ===========================\n")
            traceback.print_exc()
            # Optionally re-raise or handle
            raise  # Re-raise to stop execution or debug
            # return False  # Or return False to stop event propagation

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
        #self.q_app              = StuffApplication( []  )

        AppGlobal.q_app         = self.q_app
        self.app_global         = AppGlobal
        AppGlobal.fatal_error   = None
        #stuff_db_app_global.logger( )

        self.assign_icon( )

        self.parameters         = parameters.Parameters( )
        AppGlobal.parameters    = self.parameters

        # after parameters are set up
        import app_logging
        an_applogging    = app_logging.AppLogging( )
        # app_logging.init()

        # ---- DB CONNECT
        a_qsql_db_access        = qsql_db_access.QsqlDbAccess( STUFFDB_CONNECTION_NAME )

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

        self.prog_info()

        a_wat_inspector         = wat_inspector.WatInspector( self.q_app )

        QTimer.singleShot(0, self.parameters.startup_function  )
        #self.q_app.exec_()   # perhaps move to run method
        exec_app()

    # -------------------------
    def assign_icon( self,  ):
        """
        what it says read:
            use often to see if we can hold on to icon
            self.assign_icon()

            in mdi....   self.main_window.assign_icon()
        """
        self.q_app.setWindowIcon( QIcon( parameters.PARAMETERS.icon ) )

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

    # ---- autostart functions for parameters
    # ----------------------------------------------
    def welcome_msg( self,  ):

     #PARAMETERS   = parameters.PARAMETERS

        msg      = ( "{Hello")
        QMessageBox.information( AppGlobal.main_window,
                                     "welcome msg ", msg )

    def cleanup( self ):
        """
        Perform cleanup operations
        this is for closing down, signaled perhaps by main_window
        """
        # Stop any running threads
        # Close database connections
        # Save application state
        # Clean up temporary files
        # etc.
        AppGlobal.qsql_db_access.remove_lock_file(   )



def main():
    app         = App(   )
    # mainWin     = stuff_db_main_window.StuffDbMainWindow()
    # mainWin.show()
   # sys.exit( 99 )
#  # app         = QApplication( sys.argv )
#  # mainWin     = stuff_db_main_window.StuffDbMainWindow()
#  # mainWin.show()
#  # sys.e

# ---- eof
