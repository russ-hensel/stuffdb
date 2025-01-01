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
__version__   = "Ver 55: 2024 12 22.01"

# ---- imports

import datetime
import logging
import os
import random
import sys
import time


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

#import   stuffdb_def
import key_gen
#import   mdi_management
import main_window
import parameters
import qsql_db_access
import sql_util
import wat_inspector
from app_global import AppGlobal



# ---------------
# from stuff_main_window import MainWindow


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
        print( "========= restart =================" )

        self.q_app              = QApplication( []  )
        AppGlobal.q_app         = self.q_app

        self.parameters         = parameters.Parameters( )
        AppGlobal.parameters    = self.parameters

        #dialog                  = wat_inspector.DisplayWat( self.q_app )

        a_qsql_db_access        = qsql_db_access.QsqlDbAccess( )

        AppGlobal.qsql_db_access  = a_qsql_db_access

        self.sql_runner         = sql_util.SqlRunner( self.parameters.db_fn )
        AppGlobal.sql_runner    = self.sql_runner

        a_key_gen               = key_gen.KeyGenerator( a_qsql_db_access.db  )  #  AppGlobal.qsql_db_access.db
        AppGlobal.key_gen       = a_key_gen

        self.main_window        = main_window.StuffdbMainWindow()
        AppGlobal.main_window   = self.main_window
        self.main_window.show()

        print( f"{AppGlobal.logger = }")
        self.config_logger()
        self.prog_info()
        print( f"{AppGlobal.logger = }")
        AppGlobal.logger.debug( "self.q_app.exec_() next" )
        a_wat_inspector  = wat_inspector.WatInspector( self.q_app )
        # dialog       = wat_inspector.DisplayWat( self.q_app )
        self.q_app.exec_()   # perhaps move to run method

    # ------------------------------------------
    def config_logger( self, ):
        """
        configure the python logger
        return change of state
        !! consider putting in app global, include close
        """
        AppGlobal.logger_id     = "App"
        logger                  = logging.getLogger( AppGlobal.logger_id )
        logger.handlers         = []  # get stuff to close from here

        logger.setLevel( self.parameters.logging_level )

        # create the logging file handler
        file_handler = logging.FileHandler( self.parameters.pylogging_fn )

        formatter    = logging.Formatter( '%(asctime)s - %(name)s - %(levelname)s - %(message)s' )
        file_handler.setFormatter( formatter )

        # add handler to logger object -- want only one add may be a problem
        logger.addHandler( file_handler )
        msg  = "pre logger debug -- did it work"
        AppGlobal.logger.debug( msg )

        logger.info( "Done config_logger .. next AppGlobal msg" )
        #rint( "configured logger", flush = True )
        self.logger      = logger   # for access in rest of class?
        AppGlobal.set_logger( logger )

        msg  = ( f"Message from AppGlobal.print_debug >> logger level in App = "
                 f"{self.logger.level} will show at level 10"
                )
        AppGlobal.print_debug( msg )

    # ------------------------------------------
    def close_logger( self, ):
        """
        configure the python logger
        return change of state
        !! consider putting in app global, include close
        """
        logger  = AppGlobal.logger
        for a_handler in logger.handlers:
            a_handler.close()

    # --------------------------------------------
    def prog_info( self,  ):
        """
        record info about the program to the log file
        """
        #logger_level( "until_foo.prog_info"  )
        fll         = AppGlobal.force_log_level
        logger      = self.logger
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

    # # ----------------------------------------------
    # def os_open_document_help( self,  ):
    #     """
    #     what it says, read  --- in main windows
    #     determines document with focus and gives help on it.
    #     """
    #     #document    = AppGlobal.mdi_management.get_active_document()
    #     document    = AppGlobal.main_window.get_active_subwindow()
    #     name        = document.subwindow_name
    #     print( f"os_open_document_help active document name {name = }]")
    #     #AppGlobal.os_open_help_file( AppGlobal.parameters.help_file )

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
    pass
    app         = App(   )
    # mainWin     = stuff_db_main_window.StuffDbMainWindow()
    # mainWin.show()
    sys.exit( 99 )
#  # app         = QApplication( sys.argv )
#  # mainWin     = stuff_db_main_window.StuffDbMainWindow()
#  # mainWin.show()
#  # sys.e


# ---- eof