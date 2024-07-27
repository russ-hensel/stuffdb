#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 14:03:58 2024

@author: russ
"""
# ---- tof
"""


"""
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    main.main()
# --------------------

# ---- verson
__version__   = "Ver 19: 2024 07 26.01"

# ---- imports

import sys
import random

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt

# from MainWindow import Ui_MainWindow

from PyQt5.QtCore import (
    PYQT_VERSION_STR,
    QFile,
    QFileInfo,
    QSettings,
    QT_VERSION_STR,
    QTimer,
    QVariant,
    Qt,
          )

from PyQt5.QtCore import pyqtSignal as Signal

from PyQt5.QtWidgets import (
    QAction,
    QActionGroup,
    QApplication,
    QDockWidget,
    QFileDialog,
    QFrame,
    QInputDialog,
    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QSpinBox,
    QMdiSubWindow,
    QTextEdit,
    )

# ---- QtSql
from PyQt5.QtSql import (
    QSqlDatabase,
    QSqlTableModel,
    QSqlQuery
    )

from PyQt5.QtGui import (
    QIcon,
    QImage,
    QImageReader,
    QImageWriter,
    QKeySequence,
    QPainter,
    QPixmap,   )

from PyQt5.QtPrintSupport import   (
    QPrintDialog,
    QPrinter  )

from PyQt5.QtWidgets import   QMainWindow, QMenu, QAction, QMessageBox

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu, QAction,
    QMdiArea,
    QMdiSubWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    )

from PyQt5.QtCore import pyqtSlot


import   os
import   logging
import   datetime
import   time

# ------- local
from     app_global import AppGlobal
import   mdi_management
import   stuffdb_main_window
import   parameters
import   sql_util
#import   stuffdb_def
import   key_gen
import   qsql_db_access
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
        self.app_name          = "Stuff QT"
        self.version           = __version__ # "Ver 08: 2024 11 03.01"
        #self.app_version       = self.version   # get rid of dupe at some point... app_version in gui_ext
        self.app_url           = "www.where"
        # clean out dead
        AppGlobal.controller   = self
        self.gui               = None

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

        a_qsql_db_access        = qsql_db_access.QsqlDbAccess( )

        AppGlobal.qsql_db_access  = a_qsql_db_access

        self.sql_runner         = sql_util.SqlRunner( self.parameters.db_fn )
        AppGlobal.sql_runner    = self.sql_runner

        a_key_gen               = key_gen.KeyGenerator( a_qsql_db_access.db  )
        AppGlobal.key_gen       = a_key_gen


        self.main_window        = stuffdb_main_window.StuffdbMainWindow()
        AppGlobal.main_window   = self.main_window
        self.main_window.show()

        print( f"{AppGlobal.logger = }")
        self.config_logger()
        self.prog_info()
        print( f"{AppGlobal.logger = }")
        AppGlobal.logger.debug( "self.q_app.exec_() next" )

        self.q_app.exec_()   # perhaps move to run method

        # self.mdi_management         = mdi_management.MidManagement( self  )
        # AppGlobal.mdi_management    = self.mdi_management
        # AppGlobal.main_window       = self



        # if not self.gui is None:
        #     #self.gui.root.destroy()           # make gui.destroy()
        #     self.gui.root_destroy()
        #     importlib.reload( parameters )    # should work on python 3 but sometimes does not
        # else:
        #     #self.q_to_splash
        #     pass


             # open early as may effect other parts of code

        #if  self.parameters.set_default_path_here:    # Now change the directory to location of this file
#        if True:
#            py_path    = self.parameters.running_on.py_path
#
#            # retval = os.getcwd()
#            # print( f"Directory now            {retval}")
#
#            print( f"Directory now ( sw if not ''  {os.getcwd()} change to >>{py_path}<<")
#            if py_path != "":
#                os.chdir( py_path )


       # # could combine with above ??
       #  self.do_transforms      = do_transforms.DoTransforms( )
       #  self.do_commands             = do_commands.Commands()           # confusion around commands vs do_commands
       #  self.snipper            = snipper.Snipper()
       #  self.snippeter          = snipper.Snippeter()
       #  # move these to snipper when get around to it
       #  self.snippets           = None       # define later automatically, leave alone
       #  self.snip_files         = None       # define later automatically, leave alone

       #  # this builds a list in parameters that is used by gui to build
       #  #    self.snippets and self.snip_files
       #  self._read_list_of_snippets_(   self.parameters.snippets_fn  )
       #  self._read_list_of_snip_files_( self.parameters.snip_file_fn )

       #  self.sq_appnippets_dict       = {}          # predefined stuff for clipboard -- do before gui
       #  self.snip_files_dict     = {}          # predefined stuff for clipboard -- do before gui

       #  # gets gui ref so make before gui
       #  self.cmd_processor  = cmd_processor.CmdProcessor(  )   # commands processed here

       #  # !! make parm driven or ditch gui.  self.gui_module         = "gui_qt"
       #  if   self.parameters.gui_module  == "gui_with_tabs":
       #      import gui_tk
       #      self.a_clipper      = clipper.make_clipper( "pyperclip" )
       #      self.gui            = gui_tk.GUI()
       #      self.gui.build_gui( )

       #  elif self.parameters.gui_module  == "gui_qt":
       #      from   PyQt5.QtWidgets import QApplication,  QMainWindow
       #      import gui_qt

       #      self.qt_app         = QApplication( sys.argv )
       #      self.a_clipper      = clipper.make_clipper( "qt" ) # may need to call after  QApplication
       #      self.gui            = gui_qt.GUI(   )
       #      self.gui.gui_1()
       #      #rint( f"in clip_board.py {self.gui.db_maker.rb_dispatch_dict}" )
       #      #rint( "next self.gui.show")
       #      self.gui.show()

       #  elif self.parameters.gui_module  == "gui_with_tk":
       #      1/0   # not really maintaining any more
       #      self.a_clipper      = clipper.make_clipper( "pyperclip" )
       #      self.gui            = gui_with_tabs.GUI()

       #  else:
       #      1/0   # fix with proper except
       #      # for multiple gui configurations, this will be a complete rebuild

       #  self._finish_gui( )



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
        #rint( "configed logger", flush = True )
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
        #logger_level( "util_foo.prog_info"  )
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
                         # parameters and controller not available can ge fro logger_level

    # ----------------------------------------------
    def os_open_help( self,  ):
        """
        what it says, read
        used as callback from gui button !! change to use app_global
        """
        AppGlobal.os_open_help_file( AppGlobal.parameters.help_file )

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
        gui log loggs what is sent to the gui message area
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


# # if __name__ == "__main__":
# #     main()
# #     # app = QApplication(sys.argv)
# #     # mainWin = StuffMainWindow()
# #     # mainWin.show()
# #     # sys.exit(app.exec_())
