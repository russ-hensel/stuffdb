#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main window container for the mdi

"""

# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    main.main()
# --------------------

# ---- imports

import functools
import logging
import os
import traceback

import app_logging
# ------- local
import gui_qt_ext
import psutil
import show_parameters
#import    document_maker
#import    help_sub_window
# import   db_create
from app_global import AppGlobal

from PyQt5.QtCore import QDate, QModelIndex, Qt, QTimer, pyqtSlot

from PyQt5.QtGui import QIcon, QIntValidator, QStandardItem, QStandardItemModel
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt5.QtWidgets import (QAction,
                             QActionGroup,
                             QApplication,
                             QButtonGroup,
                             QCheckBox,
                             QComboBox,
                             QDateEdit,
                             QDialog,
                             QDockWidget,
                             QFileDialog,
                             QFrame,
                             QGridLayout,
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
                             QSpinBox,
                             QTableView,
                             QTabWidget,
                             QTextEdit,
                             QToolBar,
                             QVBoxLayout,
                             QWidget)


# ---- local imports
import mdi_management
import stuffdb
import parameters

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
        a_mdi_management                = mdi_management.MdiManagement( self  )
        self.mdi_management             = a_mdi_management
        AppGlobal.mdi_management        = a_mdi_management

        self.build_menu()
        a_mdi_management.window_menu    = self.window_menu

        icon    = QIcon(  parameters.PARAMETERS.icon  )
        self.setWindowIcon(icon)

        self.build_toolbar()

    #-----------------------------------
    def build_toolbar( self,  ):
        """
        what it says read:
        """
        toolbar = QToolBar("My Toolbar")
        self.addToolBar(toolbar)

        # Create actions with icons
        action1 = QAction( QIcon.fromTheme("document-new"), "Choice 1", self )
        action1.triggered.connect( self.show_message1 )
        toolbar.addAction(action1)

        # Standard Icon Names
        # https://specifications.freedesktop.org/icon-naming-spec/latest/ar01s04.html

        # action = QAction( QIcon.fromTheme( "printer" ), "Choice 1", self )
        # action.triggered.connect( self.show_message1 )
        # toolbar.addAction(action)

        # ---- DB operations
        #action          = QAction( QIcon.fromTheme( "go-next" ), "Next", self )
        action          = QAction(  "Add", self )
        connect_to      = functools.partial(  self.go_active_sub_window_func,
                                              "add_default"     )
        action.triggered.connect( connect_to )
        toolbar.addAction(action)

        action          = QAction(  "Add/Copy", self )
        connect_to      = functools.partial(  self.go_active_sub_window_func,
                                              "add_copy"    )    # "copy_prior_row"     )
        action.triggered.connect( connect_to )
        toolbar.addAction( action )

        action          = QAction(  "Save", self )
        connect_to      = functools.partial(  self.go_active_sub_window_func,
                                              "update_db"     )
        action.triggered.connect( connect_to )
        toolbar.addAction( action )

        #action          = QAction( QIcon.fromTheme( "go-next" ), "Next", self )
        action          = QAction(  "Delete", self )
        connect_to      = functools.partial(  self.go_active_sub_window_func,
                                              "delete"     )
        action.triggered.connect( connect_to )
        toolbar.addAction( action )

        # ---- List nav
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
        #                                       help_sub_window.HelpSubWindow.class method_foo     )
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

        # ---- go-previous
        action          = QAction( QIcon.fromTheme( "go-previous" ), "Previous", self )
        a_function      = functools.partial(  self.go_active_sub_window_func,
                                              "prior_history_to_detail"     )
        action.triggered.connect( a_function )
        toolbar.addAction(action)

        # # ---- got_deail_updates
        # action          = QAction(  "have_updatable_edits", self )
        # a_function      = functools.partial(  self.go_active_sub_window_func,
        #                                       "have_updatable_edits"     )
        # action.triggered.connect( a_function )
        # toolbar.addAction(action)


        # action          = QAction(   "Test Next Key", self )
        # a_function      = functools.partial(  AppGlobal.key_gen.get_next_key,
        #                                       "channel"     )
        # action.triggered.connect( a_function )
        # toolbar.addAction(action)

        action          = QAction(   "break...", self )
        # a_function      = functools.partial(  AppGlobal.key_gen.get_next_key,
        #                                       "channel"     )
        action.triggered.connect( breakpoint )
        toolbar.addAction(action)

        # ---- "add_to_log"
        action          = QAction( "add_to_log", self )
        connect_to      = app_logging.add_to_log
        action.triggered.connect( connect_to )
        toolbar.addAction( action )

        # ---- DocInspect
        action          = QAction( "doc_wat_inspect", self )
        connect_to      = functools.partial(  self.go_active_sub_window_func,
                                              "doc_wat_inspect"     )
        action.triggered.connect( connect_to )
        toolbar.addAction( action )

        # ---- "data_manager_inspect"
        action          = QAction( "data_manager_inspect", self )
        connect_to      = functools.partial(  self.go_active_sub_window_func,
                                              "data_manager_inspect"     )
        action.triggered.connect( connect_to )
        toolbar.addAction( action )

        # ---- doc -->str
        action          = QAction( "Doc->Str", self )
        connect_to      = functools.partial(  self.go_active_sub_window_func,
                                              "doc_str"     )
        action.triggered.connect( connect_to )
        toolbar.addAction( action )

        # ---- "Tab->Str"
        action          = QAction( "Tab->Str", self )
        connect_to      = functools.partial(  self.go_active_sub_window_func,
                                              "tab_str"     )
        action.triggered.connect( connect_to )
        toolbar.addAction( action )

        # # ---- tests
        # action          = QAction(   "fetch id test", self )
        # a_function      = functools.partial(  self.go_active_sub_window_func,
        #                                       "fetch_id_test"     )
        # action.triggered.connect( a_function )
        # toolbar.addAction(action)

        # action          = QAction(   "i_am_hsw", self )
        # a_function      = functools.partial(  self.go_active_sub_window_func,
        #                                     "i_am_hsw"     )
        # action.triggered.connect( a_function )
        # toolbar.addAction(action)

    # ------------------------------------
    def build_menu( self,  ):
        """
        what it says read:

        """
        menubar         = self.menuBar()
        self.menubar    = menubar

        # ---- File
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

        # ---- DocOps
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
                                              "add_copy"    )  #  "copy_prior_row"
        action.triggered.connect( connect_to )
        menu.addAction( action )

        action          = QAction( "Save", self )
        connect_to      = functools.partial(  self.go_active_sub_window_func,
                                              "update_db"     )
        action.triggered.connect( connect_to )
        menu.addAction( action )

        # ---- delete
        action          = QAction( "Delete", self )
        connect_to      = functools.partial(  self.go_active_sub_window_func,
                                              "delete"     )
        action.triggered.connect( connect_to )
        menu.addAction( action )

        # ----
        action          = QAction( "Doc->Str", self )
        connect_to      = functools.partial(  self.go_active_sub_window_func,
                                              "doc_str"     )
        action.triggered.connect( connect_to )
        menu.addAction( action )

        # ----
        action          = QAction( "Tab->Str", self )
        connect_to      = functools.partial(  self.go_active_sub_window_func,
                                              "tab_str"     )
        action.triggered.connect( connect_to )
        menu.addAction( action )

        # ---- "set size o"
        action          = QAction( "set size", self )
        #connect_to      = functools.partial( self.add_subwindow, window_type = "channel" )
        connect_to      = functools.partial(  self.go_active_sub_window_func,
                                              "set_size_pos"     )
        action.triggered.connect( connect_to )
        menu.addAction( action )

        # ---- "Mdi Info"
        action          = QAction( "Mdi Info", self )
        #connect_to      = functools.partial( self.add_subwindow, window_type = "channel" )
        connect_to      = AppGlobal.mdi_management.show_mdi_info
        action.triggered.connect( connect_to )
        menu.addAction( action )

        menu.addSeparator()

        # ---- Open
        menu_open       = menubar.addMenu( "Open" )
        self.menu_open  = menu_open

        action          = QAction( "Album", self )
        connect_to      = functools.partial( self.add_subwindow, window_type = "album" )
        action.triggered.connect( connect_to )
        menu_open.addAction( action )

        action          = QAction( "Help", self )
        connect_to      = functools.partial( self.add_subwindow, window_type = "help" )
        action.triggered.connect( connect_to )
        menu_open.addAction( action )

        action          = QAction( "People", self )
        connect_to      = functools.partial( self.add_subwindow, window_type = "people" )
        action.triggered.connect( connect_to )
        menu_open.addAction( action )

        action          = QAction( "Picture", self )
        connect_to      = functools.partial( self.add_subwindow, window_type = "picture" )
        action.triggered.connect( connect_to )
        menu_open.addAction( action )

        action          = QAction( "Plant", self )
        connect_to      = functools.partial( self.add_subwindow, window_type = "plant" )
        action.triggered.connect( connect_to )
        menu_open.addAction( action )

        action          = QAction( "Planting", self )
        connect_to      = functools.partial( self.add_subwindow, window_type = "planting" )
        action.triggered.connect( connect_to )
        menu_open.addAction( action )

        action          = QAction( "Stuff", self )
        connect_to      = functools.partial( self.add_subwindow, window_type = "stuff" )
        action.triggered.connect( connect_to )
        menu_open.addAction( action )

        menu_open.addSeparator()

        # ---- Configuration
        a_menu          = menubar.addMenu("Configuration")

        open_action     = QAction( "Open Log", self )
        connect_to      = functools.partial( AppGlobal.os_open_txt_file,
                                             AppGlobal.parameters.pylogging_fn  )
        open_action.triggered.connect( connect_to )
        a_menu.addAction( open_action )

        #---------------
        open_action     = QAction( "Show Parameters", self )
        connect_to      = self.show_parameters
        open_action.triggered.connect( connect_to )
        a_menu.addAction( open_action )
        #---------------
        open_action     = QAction( "Open Parameters", self )
        connect_to      = AppGlobal.controller.os_open_parmfile
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
        action.triggered.connect( self.mdi_management.cascade_documents )
        window_menu.addAction( action )

        action             = QAction( "Tile", self )
        action.triggered.connect( self.mdi_management.tile_documents )
        window_menu.addAction( action )

        # action             = QAction( "Tile", self )
        # action.triggered.connect( self.show_about_box )
        # window_menu.addAction( action )

        action             = QAction( "Layer", self )
        action.triggered.connect( self.mdi_management.layer_documents )
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

        action          = QAction( "Help on Text", self )
        doc_name        = f"{AppGlobal.parameters.help_path}/text_help.txt"
        connect_to      = functools.partial( AppGlobal.os_open_txt_file,
                                             doc_name          )
        action.triggered.connect( connect_to )
        menu_help.addAction( action )

        action          = QAction( "General Document Help...", self )

        connect_to      = self.open_general_document_help
        action.triggered.connect( connect_to )
        menu_help.addAction( action )

        action          = QAction( "Current Document Help...", self )
        connect_to      = self.open_document_help
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

    #-------
    def open_general_document_help( self,   ):
        """
        what it says read:
        """
        #print( str( AppGlobal.parameters) )
        doc_name        = f"{AppGlobal.parameters.help_path}/general_doc.txt"
        AppGlobal.os_open_txt_file( doc_name  )


    #-------
    def open_document_help( self,   ):
        """
        what it says read:
            still needs work
        """
        # document_help_dict = { "pictu": "picture_doc.txt",
        #                        "StuffSubWindow":  "stuff_doc.txt",
        #                        "plain":  "plant_doc.txt",
        #                        "album":  "album_doc.txt",
        #                        "HelpSubWindow":  "help_doc.txt",
        #                        }

        asw        = self.get_active_subwindow()
        if not asw:
            print( "document is none why not add a help here")
            return
        # asw        = self.mdi_area.activeSubWindow()
        # name       = asw.subwindow_name.lower()[0:5]
        # name       = asw.subwindow_name
        # msg        = f"want help for {name = }"
        # print( msg )
        #rint( f"open_document_help active document name {name = }]")
        #doc_name        = document_help_dict.get( name, "what_document.txt" )
        doc_name        = asw.help_filename
        doc_name        = f"{AppGlobal.parameters.help_path}/{doc_name}"
        #rint( f"open_document_help active document name {doc_name = }]")


        AppGlobal.os_open_txt_file( doc_name  )

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
        not sure why or what

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
        what it says, but !! more inf
        """
        mode        = AppGlobal.parameters.mode
        version     = f"Version = {stuffdb.__version__}"
        process_pid = psutil.Process(os.getpid())
        #print( f"process.memory_info().rss >>{process.memory_info().rss}<<")  # in bytes

        msg      =  "get the size this process thru its pid "
        memory   = process_pid.memory_info().rss/1_000_000
        memory   = f"Memory = {memory} Mbytes"
        repo     = " coming soom          "
        msg      = ( f"Stuff DB {version} {mode}"
                     f"\n{memory}"
                     f"\n{repo}"
                     )

        QMessageBox.about(self, "About", msg )


    # -----------------------
    def show_parameters(self):
        """
        what it says,
        """
        dialog     = show_parameters.DisplayParameters( parent = self )
        if dialog.exec_() == QDialog.Accepted:
            #self.model.submitAll()
            # ok     = stuffdb_tabbed_sub_window.model_submit_all(
            #            model,  f"StuffEventsSubTab.add_record " )
            # model.select()
            pass

    # ---------------------------------------
    def add_subwindow( self, window_type = None ):
        """
        indirect because of order of creation
        might otherwise be circular
        """
        AppGlobal.mdi_management.make_document( window_type = window_type )

    # ---------------------------------------
    def search_me( self, criteria = None ):
        """
        for now search comming from text widget
        """
        #AppGlobal.mdi_management.make_document( window_type = window_type )
        print( "here we are in search_me )))))))))))))))))))))))))))))))))))))))))))))))")
        asw     = self.get_active_subwindow(  )
        asw.search_me( criteria )



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
        if active_window is None:
            msg   = ( f"no active window for {a_function_name}")
            logging.error( msg )

            return

        a_function      = getattr( active_window, a_function_name, None )
        #rint( f"{a_function_name = } {a_function = }")
        ## add a test for none
        try:
            a_function( )

        except Exception as an_except:   #  or( E1, E2 )

            msg     = f"a_except         >>{an_except}<<  type  >>{type( an_except)}<<"
            logging.error( msg )

            msg     = f"an_except.args   >>{an_except.args}<<"
            logging.error( msg )

            s_trace = traceback.format_exc()
            msg     = f"format-exc       >>{s_trace}<<"
            logging.error( msg )

            msg     = f"looking for function     >>{a_function_name = }<< in {active_window = }"
            logging.error( msg )

        #     #raise  # to re raise same
        # finally:
        #     msg     = f"in finally  {1}"
        #     print( msg )

    # ---- test actions ----------------------
    # -----------------------------


    # -----------------------------
    def show_message1(self):
        """
        what it says

        """
        msg      = "You selected Choice 1"
        QMessageBox.information(self, "Message",  msg )

# ---- eof ------------------------------------------------
