#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 11:51:07 2024

@author: russ


from   chat_top_mdi_window.py

some local variables need to be promoted to instance for later reference


"""

# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    main.main()
# --------------------

# ---- imports


"""
my reference list of qt imports comes from import_qt.py

"""
# ---- begin pyqt from import_qt.py
# ---- QtGui
from PyQt5.QtGui import (
    QStandardItemModel,
    QStandardItem,
    QIcon,
           )
# ---- QtCore
from PyQt5.QtCore  import  (
    QDate,
    QModelIndex,
    QTimer,
    Qt,
    pyqtSlot,
    )

# ----QtWidgets
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QAction,
    QDateEdit,
    QMenu,
    QAction,
    QLineEdit,
    QActionGroup,
    QApplication,
    QDockWidget,
    QTabWidget,
    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QSpinBox,
    QMdiSubWindow,
    QTextEdit,
    QButtonGroup,
    )


# ----QtWidgets big
from PyQt5.QtWidgets import (
    QAction,
    QMenu,
    QApplication,
    QMainWindow,
    QToolBar,
    QTableView,
    QFrame,
    QMainWindow,
    QMdiArea,
    QMdiSubWindow,
    QMdiArea,
    QMdiSubWindow,
    )

# ----QtWidgets layouts
from PyQt5.QtWidgets import (
    QGridLayout,
    QVBoxLayout
    )

# ----QtWidgets Boxes, Dialogs
from PyQt5.QtWidgets import (
    QAction,
    QActionGroup,
    QDockWidget,
    QFileDialog,
    QInputDialog,

    QLabel,
    QListWidget,
    QMenu,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QCheckBox,
    QComboBox,
    )

from PyQt5.QtGui import (
    QIntValidator,
    )

# ---- QtSql
from PyQt5.QtSql import (
    QSqlDatabase,
    QSqlTableModel,
    QSqlQuery
    )


# ---- imports more

#import random
import collections
import functools
import traceback


# ------- local
import    gui_qt_ext
import    document_maker
#import    help_sub_window
import   db_create
from     app_global import AppGlobal
import   mdi_management

# ------------------------------------------
class StuffdbMainWindow( QMainWindow ):
    """
    see __init__
    """
    def __init__(self):
        """
        main window for db type windows, holds mdi stuff
        Returns:
            None.

        """
        # super( QMainWindow, self).__init__()
        super().__init__()
        AppGlobal.main_window       = self
        parameters                  = AppGlobal.parameters
        self.show()

        self.setWindowTitle( "StuffdbMainWindow" )
        self.setGeometry( parameters.qt_xpos,
                          parameters.qt_ypos ,
                          parameters.qt_width,
                          parameters.qt_height  )

        self.build_gui( )

    # -------------------------
    def build_gui( self,  ):
        """
        what it says read:

        """
        # Create MDI Area set as central widget
        self.mdi_area = QMdiArea()
        self.setCentralWidget(self.mdi_area)

        # need a_mdi_management to exist to call from menu,
        # but it needs a reference to the menu, so this.... hot mess
        a_mdi_management                = mdi_management.MidManagement( self  )
        self.mdi_management             = a_mdi_management
        AppGlobal.mdi_management        = a_mdi_management

        self.build_menu()
        a_mdi_management.window_menu    = self.window_menu

        self.build_toolbar()

        self.document_maker             = document_maker.DocumentMaker()
        AppGlobal.document_maker        = self.document_maker

    #-----------------------------------
    def build_toolbar( self,  ):
        """
        what it says read:

        """
        toolbar = QToolBar("My Toolbar")
        self.addToolBar(toolbar)

        # Create actions with icons
        action1 = QAction( QIcon.fromTheme("document-new"), "Choice 1", self )
        action1.triggered.connect(self.show_message1)
        toolbar.addAction(action1)

        # Standard Icon Names
        # https://specifications.freedesktop.org/icon-naming-spec/latest/ar01s04.html

        # action = QAction( QIcon.fromTheme( "printer" ), "Choice 1", self )
        # action.triggered.connect( self.show_message1 )
        # toolbar.addAction(action)

        # ---- stuff items
        #action          = QAction( QIcon.fromTheme( "go-next" ), "Next", self )
        action          = QAction(  "Add", self )
        connect_to      = functools.partial(  self.go_active_sub_window_func,
                                              "new_record"     )
        action.triggered.connect( connect_to )
        toolbar.addAction(action)

        action          = QAction(  "Add/Copy", self )
        connect_to      = functools.partial(  self.go_active_sub_window_func,
                                              "copy_prior_row"     )
        action.triggered.connect( connect_to )
        toolbar.addAction( action )

        action          = QAction(  "Save", self )
        connect_to      = functools.partial(  self.go_active_sub_window_func,
                                              "save"     )
        action.triggered.connect( connect_to )
        toolbar.addAction( action )

        #action          = QAction( QIcon.fromTheme( "go-next" ), "Next", self )
        action          = QAction(  "Delete", self )
        connect_to      = functools.partial(  self.go_active_sub_window_func,
                                              "delete_record"     )
        action.triggered.connect( connect_to )
        toolbar.addAction( action )

        # ---- list nav
        action          = QAction( QIcon.fromTheme( "go-next" ), "Next", self )
        a_function      = functools.partial(  self.go_active_sub_window_func,
                                              "next_list_to_detail"     )
        action.triggered.connect( a_function )
        toolbar.addAction(action)

        # # Create actions with icons
        # action          = QAction( QIcon.fromTheme( "go-previous" ), "test calling", self )
        # # a_function      = functools.partial(  self.go_active_sub_window_func,
        # #              help_sub_window.HelpSubWindow.prior_list_to_detail     )

        # a_function      = functools.partial(  self.go_active_sub_window_func,
        #                                       help_sub_window.HelpSubWindow.classmethod_foo     )
        action          = QAction( QIcon.fromTheme( "go-previous" ), "Previous", self )
        a_function      = functools.partial(  self.go_active_sub_window_func,
                                              "prior_list_to_detail"     )
        action.triggered.connect( a_function )
        toolbar.addAction(action)

        # ---- history nav
        action  = QAction( "<List | History >", self)
        #action .triggered.connect( self.criteria_select )
        toolbar.addAction(action )

        action          = QAction( QIcon.fromTheme( "go-next" ), "Next", self )
        a_function      = functools.partial(  self.go_active_sub_window_func,
                                              "next_history_to_detail"     )
        action.triggered.connect( a_function )
        toolbar.addAction(action)

        action          = QAction( QIcon.fromTheme( "go-previous" ), "Previous", self )
        a_function      = functools.partial(  self.go_active_sub_window_func,
                                              "prior_history_to_detail"     )
        action.triggered.connect( a_function )
        toolbar.addAction(action)

        action          = QAction(   "Test Next Key", self )
        a_function      = functools.partial(  AppGlobal.key_gen.get_next_key,
                                              "channel"     )
        action.triggered.connect( a_function )
        toolbar.addAction(action)

        # action          = QAction(   "new_default", self )
        # a_function      = functools.partial(  self.go_active_sub_window_func,
        #                                       "default_new_row"     )
        # action.triggered.connect( a_function )
        # toolbar.addAction(action)

        # action          = QAction(   "copy prior", self )
        # a_function      = functools.partial(  self.go_active_sub_window_func,
        #                                       "copy_prior_row"     )
        # action.triggered.connect( a_function )
        # toolbar.addAction(action)
        # ---- tests
        action          = QAction(   "fetch id test", self )
        a_function      = functools.partial(  self.go_active_sub_window_func,
                                              "fetch_id_test"     )
        action.triggered.connect( a_function )
        toolbar.addAction(action)

        action          = QAction(   "i_am_hsw", self )
        a_function      = functools.partial(  self.go_active_sub_window_func,
                                            "i_am_hsw"     )
        action.triggered.connect( a_function )
        toolbar.addAction(action)

    # ------------------------------------
    def build_menu( self,  ):
        """
        what it says read:

        """
        # Add actions to submenus, one of which links to an about box
        about_action1 = QAction( "About...", self )
        about_action1.triggered.connect( self.show_about_box )

        # Create menu bar with two menus and submenus
        menubar         = self.menuBar()
        self.menubar    = menubar

        # ---- File  current template
        a_menu          = menubar.addMenu( "File" )

        action     = QAction( "Save", self )
        # connect_to      = functools.partial( AppGlobal.os_open_txt_file,
        #                                      AppGlobal.parameters.pylogging_fn  )
        action.triggered.connect( self.not_implemented )
        a_menu.addAction( action )

        #---------------
        action          = QAction( "Save All", self )
        connect_to      = functools.partial( AppGlobal.os_open_txt_file,
                                             AppGlobal.parameters.pylogging_fn  )
        action.triggered.connect( connect_to )
        a_menu.addAction( action )

        # # ---- menu 1 with subs, a bit of a mess
        # menu1           = menubar.addMenu("Menu 1")

        # submenu1        = QMenu("SubMenu 1.1", self)
        # self.menuMenuA  = submenu1
        # menu1.addMenu(submenu1)

        # submenu2        = QMenu("SubMenu 1.2", self)
        # menu1.addMenu(submenu2)
        # submenu2.addAction( about_action1 )

        # ---- Stuff
        menu            = menubar.addMenu("DocOps")
        self.menu_open  = menu # do we need ref, may want to change the name

        action          = QAction( "Add", self )
        # connect_to      = functools.partial( self.add_subwindow, window_type = "help" )
        connect_to      = functools.partial(  self.go_active_sub_window_func,
                                              "default_new_row"     )
        action.triggered.connect( connect_to )
        menu.addAction( action )

        action          = QAction( "Add/Copy", self )
        #connect_to      = functools.partial( self.add_subwindow, window_type = "stuff" )
        connect_to      = functools.partial(  self.go_active_sub_window_func,
                                              "copy_prior_row"     )
        action.triggered.connect( connect_to )
        menu.addAction( action )

        action          = QAction( "Save", self )
        connect_to      = functools.partial(  self.go_active_sub_window_func,
                                              "save"     )
        action.triggered.connect( connect_to )
        menu.addAction( action )

        action          = QAction( "Delete", self )
        connect_to      = functools.partial( self.add_subwindow, window_type = "channel" )
        action.triggered.connect( self.not_implemented )
        menu.addAction( action )

        menu.addSeparator()

        # ---- open
        menu_open       = menubar.addMenu("Open")
        self.menu_open  = menu_open

        action          = QAction( "Help (really)", self )
        connect_to      = functools.partial( self.add_subwindow, window_type = "help" )
        action.triggered.connect( connect_to )
        menu_open.addAction( action )

        action          = QAction( "Photo", self )
        connect_to      = functools.partial( self.add_subwindow, window_type = "photo" )
        action.triggered.connect( connect_to )
        menu_open.addAction( action )

        action          = QAction( "Photo Show", self )
        connect_to      = functools.partial( self.add_subwindow, window_type = "photoshow" )
        action.triggered.connect( connect_to )
        menu_open.addAction( action )

        action          = QAction( "Stuff", self )
        connect_to      = functools.partial( self.add_subwindow, window_type = "stuff" )
        action.triggered.connect( connect_to )
        menu_open.addAction( action )

        menu_open.addSeparator()

        action          = QAction( "Channels", self )
        connect_to      = functools.partial( self.add_subwindow, window_type = "channel" )
        action.triggered.connect( connect_to )
        menu_open.addAction( action )

        menu_open.addSeparator()

        open_action     = QAction( "Open 2 tabs", self )
        connect_to      = functools.partial( self.add_subwindow, window_type = "2tabs" )
        open_action.triggered.connect( connect_to )
        menu_open.addAction( open_action )

        #---------------
        open_action     = QAction( "Open Criteria", self )
        connect_to      = functools.partial( self.add_subwindow, window_type = "criteria" )
        open_action.triggered.connect( connect_to )
        menu_open.addAction( open_action )

        #---------------
        open_action     = QAction( "Tab in Tab", self )
        connect_to      = functools.partial( self.add_subwindow, window_type = "tab_in_tab" )
        open_action.triggered.connect( connect_to )
        menu_open.addAction( open_action )

        #---------------
        open_action     = QAction( "chat_criteria", self )
        connect_to      = functools.partial( self.add_subwindow, window_type = "chat_criteria" )
        open_action.triggered.connect( connect_to )
        menu_open.addAction( open_action )

        # ---- Configuration
        a_menu          = menubar.addMenu("Configuration")

        open_action     = QAction( "Open Log", self )
        connect_to      = functools.partial( AppGlobal.os_open_txt_file,
                                             AppGlobal.parameters.pylogging_fn  )
        open_action.triggered.connect( connect_to )
        a_menu.addAction( open_action )

        #---------------
        open_action     = QAction( "Open Parameters", self )
        connect_to      = AppGlobal.controller.os_open_parmfile
        open_action.triggered.connect( connect_to )
        a_menu.addAction( open_action )

        a_menu.addSeparator()

        # # -------- help
        # open_action     = QAction( "Define table help_info", self )
        # connect_to      = functools.partial( AppGlobal.stuff_db_db.define_table_help_info,
        #                                      allow_drop = False    )
        # open_action.triggered.connect( connect_to )
        # a_menu.addAction( open_action )

        # #---------------
        # open_action     = QAction( "Addto table help_info", self )
        # connect_to      = AppGlobal.stuff_db_db.addto_table_help_info
        # # connect_to      = functools.partial( AppGlobal.stuff_db_db.addto_table_help_info,
        # #                                      allow_drop = False    )
        # open_action.triggered.connect( connect_to )
        # a_menu.addAction( open_action )

        a_menu.addSeparator()

        # # -------- key gen
        # open_action     = QAction( "Define table key_gen", self )
        # connect_to      = functools.partial( AppGlobal.stuff_db_db.define_table_key_gen,
        #                                      allow_drop = False    )
        # open_action.triggered.connect( connect_to )
        # a_menu.addAction( open_action )

        #---------------
        action          = QAction( "Create Table Stuff", self )
        connect_to      = functools.partial( db_create.create_table_stuff,
                                             db = AppGlobal.qsql_db_access.db   )
        action.triggered.connect( connect_to )
        a_menu.addAction( action )

        #---------------
        action          = QAction( "Create Table Stuff Text", self )
        connect_to      = functools.partial( db_create.create_table_stuff_text,
                                             db = AppGlobal.qsql_db_access.db   )
        action.triggered.connect( connect_to )
        a_menu.addAction( action )

        # #---------------
        # open_action     = QAction( "Addto table key_gen", self )
        # connect_to      = AppGlobal.stuff_db_db.addto_table_key_gen
        # # connect_to      = functools.partial( AppGlobal.stuff_db_db.addto_table_help_info,
        # #                                      allow_drop = False    )
        # open_action.triggered.connect( connect_to )
        # a_menu.addAction( open_action )

        #---------------
        open_action     = QAction( "test next key", self )
        connect_to      = self.test_create_next_key
        open_action.triggered.connect( connect_to )
        a_menu.addAction( open_action )

        a_menu.addSeparator()

        # #---------------
        # open_action     = QAction( "Define table channel", self )
        # connect_to      = functools.partial( AppGlobal.stuff_db_db.define_table_channel,
        #                                      allow_drop = False    )
        # open_action.triggered.connect( connect_to )
        # a_menu.addAction( open_action )

        # #---------------
        # open_action     = QAction( "Define table channel text", self )
        # connect_to      = functools.partial( AppGlobal.stuff_db_db.define_table_channel_text,
        #                                      allow_drop = False    )
        # open_action.triggered.connect( connect_to )
        # a_menu.addAction( open_action )

        # ---- window menu
        window_menu        = menubar.addMenu( "Windows" )
        self.window_menu   = window_menu

        action             = QAction( "Cascade", self )
        action.triggered.connect( self.mdi_management.cascade_sub_windows )
        window_menu.addAction( action )

        action             = QAction( "Tile", self )
        action.triggered.connect( self.mdi_management.tile_sub_windows )
        window_menu.addAction( action )

        # action             = QAction( "Tile", self )
        # action.triggered.connect( self.show_about_box )
        # window_menu.addAction( action )

        action             = QAction( "Layer", self )
        action.triggered.connect( self.mdi_management.layer_sub_windows)
        window_menu.addAction( action )

        action             = QAction( "Split Left", self )
        action.triggered.connect( self.show_about_box )
        window_menu.addAction( action )

        # tile horizontal
        # tile vertical
        # split right

        window_menu.addSeparator()

        # ---- Help
        menu_help       = menubar.addMenu( "Help" )

        action          = QAction( "Help...", self )
        connect_to      = functools.partial( AppGlobal.os_open_txt_file,
                                             AppGlobal.parameters.help_fn  )
        action.triggered.connect( connect_to )
        menu_help.addAction( action )

        about_action1 = QAction( "About...", self )
        about_action1.triggered.connect( self.show_about_box )
        menu_help.addAction( about_action1 )   # action is added directly to menu

        #menu_widget     = QMenu( "About", self)   # this implies another level of sub menus
        #menu_help.addMenu( menu_widget )

    #----------------------------
    def not_implemented( self,   ):
        """
        what it says read:
        """
        QMessageBox.information(self, "Not Implemented", "Working on this...")

    # ------- info
    def get_active_subwindow( self,   ):
        """
        what it says read:

        """
        asw        = self.mdi_area.activeSubWindow()   # method of the QMdiArea class. This method
        #rint( "get_active_subwindow {asw = } " )
        return asw

    # ---------------------
    def open_new_subwindow( self, open_new_subwindow ):
        """
        what it says read:

        """
        print( "stub function to be overridden do not delete " )

    # ----------------------------
    def create_tab_content_test(self, text):
        """
        Args:
            text (TYPE): DESCRIPTION.

        """
        tab         = QWidget()
        layout      = QVBoxLayout(tab)
        label       = QLabel( text )
        layout.addWidget( label )
        return tab
    # ---- Subwindow actions ----------------------
    # most done thru go to active sub window function
    # -----------------------
    def show_about_box(self):
        """
        what it says, but !! more info

        """
        QMessageBox.about(self, "About", "This is an about box.\n Second Line?")

    # ---------------------------------------
    def add_subwindow( self, window_type = None ):
        """
        indirect because of order of creation
        might otherwise be circular

        """
        self.document_maker.add_subwindow( window_type = window_type )

    # ---------------------------------------
    def go_active_sub_window_func( self, a_function_name  ):
        """
        allows calling sub window functions by name in a string

        a_function_name should exist in active subwindow
        use name as string not function
        function should not take args ( remove this restriction later ?? )
        this should go to the subwindow not the tab

        """
        active_window   = self.get_active_subwindow()
        a_function      = getattr( active_window, a_function_name, None )
        #rint( f"{a_function_name = } {a_function = }")
        ## add a test for none
        try:
            a_function( )

        except Exception as an_except:   #  or( E1, E2 )

            msg     = f"a_except         >>{an_except}<<  type  >>{type( an_except)}<<"
            print( msg )

            msg     = f"an_except.args   >>{an_except.args}<<"
            print( msg )

            s_trace = traceback.format_exc()
            msg     = f"format-exc       >>{s_trace}<<"
            print( msg )
            AppGlobal.logger.error( msg )   #    AppGlobal.logger.debug( msg )

            msg     = f"looking for function     >>{a_function_name = }<< in {active_window = }"
            print( msg )


        #     #raise  # to reraise same
        # finally:
        #     msg     = f"in finally  {1}"
        #     print( msg )

    # ---- test actions ----------------------
    # -----------------------------
    def test_create_next_key(self):
        """
        what it says
            this is for a new row on the window

        """
        next_key    = AppGlobal.key_gen.get_next_key(  "channel"  )
        print( f"{ next_key = }")

    # -----------------------------
    def show_message1(self):
        """
        what it says

        """
        msg      = "You selected Choice 1"
        QMessageBox.information(self, "Message",  msg )


# ---- eof
