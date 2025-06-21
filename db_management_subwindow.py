#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 07:26:39 2025

@author: russ
"""


# ---- tof



# --------------------
if __name__ == "__main__":
    import main
    main.main()
# --------------------

# ---- imports
import functools
import inspect
import logging
import pprint
import subprocess
#from functools import partial
from pathlib import Path


from PyQt5.QtCore   import QDate, QModelIndex, Qt, QTimer, pyqtSlot
from PyQt5.QtCore   import Qt, QDateTime
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtGui import (QFont,
                         QIntValidator,
                         QStandardItem,
                         QStandardItemModel,
                         QTextCursor)

from PyQt5.QtSql import (QSqlDatabase,
                         QSqlQuery,
                         QSqlQueryModel,
                         QSqlRelation,
                         QSqlRelationalDelegate,
                         QSqlRelationalTableModel,
                         QSqlTableModel)
from PyQt5.QtWidgets import (QAction,
                             QActionGroup,
                             QApplication,
                             QButtonGroup,
                             QCheckBox,
                             QComboBox,
                             QDialog,
                             QDateEdit,
                             QDockWidget,
                             QFileDialog,
                             QFrame,
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



import parameters
import data_dict
import check_fix

#import gui_qt_ext
import info_about
#import key_words
import string_util
import text_edit_ext
#import table_model
import wat_inspector
from app_global     import AppGlobal
import qsql_utils

#import ex_qt
#import exec_qt
#import mdi_management


# ---- import end

FIF             = info_about.INFO_ABOUT.find_info_for

EXEC_RUNNER     = None  # setup below
# MARKER              = ">snip"



# ---- end imports
# PERHAPS IN DATA DICT
ALL_TABLES  = [
                         'help_info', "help_text",  "help_key_word",
                         'stuff', "stuff_text",
                         'plant', "plant_text",
                         'people' "people_text",
                            ]

TABLE_DICT  = {
                         'help_info': "help_text",
                         'stuff': "stuff_text",
                         'plant': "plant_text",
                         'people': "people_text",
                            }

KW_TABLE_DICT  = {
                         'help_info': "help_key_word",
                         'stuff': "stuff_key_word",
                         'plant': "plant_key_word",
                         'people': "people_key_word",
                            }

IKW_TABLE_DICT = {value: key for key, value in KW_TABLE_DICT.items()}

# ----------------------------------------
class DbManagementSubWindow( QMdiSubWindow ):
    """
    db_management_subwindow.DbManagementSubWindow( )
    """
    def __init__(self, instance_ix = 0 ):
        """
        This is the parent for the document
        It holds our tabs
        when a document is created it registers itself with what mdi...?
        """
        super().__init__()

        self.subwindow_name     = "Database Management"

        self.instance_ix        = instance_ix

        mdi_area                = AppGlobal.main_window.mdi_area
            #we could return the subwindow for parent to add
        #sub_window              = self
            # sub_window.setWindowTitle( "this title may be replaced " )
        self.db                 = AppGlobal.qsql_db_access.db

        self.prior_tab          = 0
        self.current_tab        = 0

        # self.record_state
        self.current_tab_index      = 0       # assumed to be criteria

        self.tab_folder             = QTabWidget() # create for descendants

        # may want to keep at end of this init
        AppGlobal.mdi_management.register_document(  self )



        self.detail_table_name      = "xxx"  # need for framework do not delete
        # self.key_word_table_name    = "stuff_key_word"
        # self.text_table_name        = "stuff_text"  # text tables always id and text_data
            # used in text tab base
        self.help_filename          = "stuff_doc.txt"
        self.subwindow_name         = "Database Management"

        self._build_gui()
        self.__init_2__()

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says
        """
        # Main notebook with  tabs
        main_notebook           = self.tab_folder   # create in parent
        self.main_notebook      = main_notebook

        sub_window              = self
        mdi_area                = AppGlobal.main_window.mdi_area
        # main_notebook.currentChanged.connect( self.on_tab_changed )

        # ix                        = -1

        # ix                       += 1
        # self.criteria_tab_index   = ix
        self.first_tab         = BasicsTab( self  )
        main_notebook.addTab(       self.first_tab, "BasicsTab" )

        self.first_tab         = KeyWordTab( self  )
        main_notebook.addTab( self.first_tab, "Key Words" )

        self.first_tab         = RecordMatchTab( self  )
        main_notebook.addTab( self.first_tab, "RecordMatchTab" )

        tab                 = OutputTab( self  )
        self.output_tab     = tab
        main_notebook.addTab( tab, "Output" )

        self.output_edit    = tab.output_edit   # self.output_edit

        sub_window.setWidget( main_notebook )
        mdi_area.addSubWindow( sub_window )
        #      # perhaps add to register_document in midi_management

        sub_window.show()

    # --------------------------------
    def __init_2__( self ):
        """call at end of child __init__ """
        # !! perhaps in ancestor to a post innit
        title       = self.subwindow_name
        if self.instance_ix !=0:
            title  += f" {self.instance_ix}"

        self.setWindowTitle( title )
        AppGlobal.mdi_management.update_menu_item( self )
        self.set_size_pos()

    # --------------------------------
    def set_size_pos( self ):
        """
        run after tab is added??
        """
        debug_msg = ( "set_size_pos--------------------------------------  " )
        logging.debug( debug_msg )

        # # --- works but window is hidden
        # self.showMaximized()
        # self.show()

        # ---- next partly works
        # this is a bit crude a kluge for now
        my_parameters       = AppGlobal.parameters
        qt_xpos             = my_parameters.doc_qt_xpos
        qt_ypos             = my_parameters.doc_qt_ypos
        qt_width            = my_parameters.doc_qt_width
        qt_height           = my_parameters.doc_qt_height

        self.setGeometry(  qt_xpos,
                           qt_ypos,
                           qt_width,
                           qt_height  )

    # --------------------------------
    def activate_output_tab( self,    ):
        """


        self.parent_window.activate_output_tab()
        """
        self.main_notebook.setCurrentWidget( self.output_tab  )

    # --------------------------------
    def output_msg( self, msg, clear = False  ):
        """
        dup with line_out
        """
        self.append_msg( msg, clear = clear  )

    #----------------------------
    def append_msg( self, msg, clear = False ):
        """
        read it --
            and print to console
        msg is just the name of the function
        """
        #msg     = f"----==== {msg} ====----"
        # if clear:
        #     self.clear_msg(  )
        if clear:
            self.output_edit.clear()
        self.output_edit.append( msg )

    # --------------------------------
    def closeEvent(self, event):
        """
        may not be complete -- for example pending updates
        """
        AppGlobal.mdi_management.forget_document(  self )
        self.on_close()
        event.accept()

    # --------------------------------
    @pyqtSlot()
    def on_close( self ):
        """
        just debug for now
        """
        debug_msg  = (f"{self.windowTitle()} has been closed")
        logging.debug( debug_msg )

    # ------------------------------------------
    def system_rpt( self, ):
        """

        """



    # ------------------------------------------
    def doc_wat_inspect( self, ):
        """
        links to main menu bar for debug
        """
        debug_msg    = ( f"doc_inspect may want to add to  {self}")
        logging.debug( debug_msg )
        # make some locals for inspection
        self_detail_tab         = self.detail_tab
        self_text_tab           = self.text_tab
        self_detail_table_name  = self.detail_table_name
        # parent_window = self.parent( ).parent( ).parent().parent()

        todo = """
           """

        wat_inspector.go(
             msg            = "inspect !! more locals would be nice ",
             # inspect_me     = self.people_model,
             a_locals       = locals(),
             a_globals      = globals(), )

    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = "\n>>>>>>>>>>* DB Manatement   *<<<<<<<<<<<<"


        # a_str   = string_util.to_columns( a_str, ["criteria_tab_index",
        #                                    f"{self.criteria_tab_index}" ] )
        # a_str   = string_util.to_columns( a_str, ["current_id",
        #                                    f"{self.current_id}" ] )
        # a_str   = string_util.to_columns( a_str, ["current_tab_index",
        #                                    f"{self.current_tab_index}" ] )

        # a_str   = string_util.to_columns( a_str, ["detail_table_id",
        #                                    f"{self.detail_table_id}" ] )
        # a_str   = string_util.to_columns( a_str, ["detail_table_name",
        #                                    f"{self.detail_table_name}" ] )
        # a_str   = string_util.to_columns( a_str, ["history_tab",
        #                                    f"{self.history_tab}" ] )
        # a_str   = string_util.to_columns( a_str, ["list_tab",
        #                                    f"{self.list_tab}" ] )
        # # a_str   = string_util.to_columns( a_str, ["mapper",
        # #                                    f"{self.mapper}" ] )
        # a_str   = string_util.to_columns( a_str, ["menu_action_id",
        #                                    f"{self.menu_action_id}" ] )
        # a_str   = string_util.to_columns( a_str, ["picture_tab",
        #                                    f"{self.picture_tab}" ] )
        # a_str   = string_util.to_columns( a_str, ["subwindow_name",
        #                                    f"{self.subwindow_name}" ] )
        # a_str   = string_util.to_columns( a_str, ["tab_folder",
        #                                    f"{self.tab_folder}" ] )
        a_str   = string_util.to_columns( a_str, ["text_tab",
                                            f"{self.text_tab}" ] )

        # b_str   = self.super().__str__( self )
        # a_str   = a_str + "\n" + b_str

        return a_str


# ----------------------------------------
class BasicsTab( QWidget ):
    """
    what it says
    """
    def __init__(self, parent_window ):
        """

        """
        super().__init__()

        # self.criteria_dict          = {}
        # self.critera_widget_list    = []
        # self.critera_is_changed     = True
        self.parent_window          = parent_window
        self.key_words_widget       = None      # set to value in gui if used

        self.tab_name               = "DbMaint"
        self.build_gui()

    # -----------------------------
    def build_gui( self,   ):
        """

        """
        vlayout              = QVBoxLayout( self )

        layout              = QHBoxLayout( self )
        vlayout.addLayout( layout )

        # ---- table combobox
        widget              = QComboBox()

        self.table_widget   = widget

        a_list              = ALL_TABLES

        widget.addItems( a_list )
        widget.setCurrentIndex( 0 )
        layout.addWidget( widget )


        widget              = QPushButton( "create sql" )
        self.q_pbutton_1    = widget
        connect_to          = self.create_sql
        widget.clicked.connect(  connect_to   )
        layout.addWidget( widget )

        widget              = QPushButton( "record count" )
        connect_to          = self.record_count_rpt
        widget.clicked.connect( connect_to  )
        layout.addWidget( widget )

        # ---- new row
        layout              = QHBoxLayout( self )
        vlayout.addLayout( layout )

        widget              = QPushButton( "Systems and SubSystes" )
        connect_to          = self.system_sub_count_rpt
        widget.clicked.connect( connect_to  )
        layout.addWidget( widget )

    # -------------------------------
    def _build_top_widgets_placer_delete( self, placer ):
        """
        what it says read, std for all criteria tabs
        lets add a Hbox
        """
        placer.new_row()
        button_layout    = QHBoxLayout()
        placer.layout.addLayout( button_layout, placer.ix_col, placer.ix_row, 0, 5  )
        #row: int, column: int, rowSpan: int, columnSpan: int, alignment: Union[Qt.Alignment, Qt.AlignmentFlag] = Qt.Alignment()):
        placer.new_row()
        # ---- buttons
        a_widget        = QPushButton( "Clear" )
        a_widget.clicked.connect(  self.clear_criteria )
        button_layout.addWidget( a_widget )

        a_widget        = QPushButton( "Go -->" )
        a_widget.clicked.connect(  self.parent_window.criteria_select )
        button_layout.addWidget( a_widget )

        a_widget        = QPushButton( "Paste/Go -->" )
        a_widget.clicked.connect(  self.paste_go )
        button_layout.addWidget( a_widget )

        a_widget        = QPushButton( "Clear/Paste/Go -->" )
        a_widget.clicked.connect(  self.clear_go )
        button_layout.addWidget( a_widget )


    # -------------------------
    # ---- reports
    def record_count_rpt( self,   ):
        """
        What it says, read

        """
        table_name     = self.table_widget.currentText()


        msg    = ( f"record_count_rpt for table {table_name = }" )
        self.parent_window.output_msg(  msg, clear = True )


        db                  = AppGlobal.qsql_db_access.db
        check_fix.line_out  = self.parent_window.output_msg
        check_fix.print_record_count( db, table_name )

        #self.parent_window.output_msg(  msg )
        self.parent_window.activate_output_tab()

    # ---- reports
    def system_sub_count_rpt( self,   ):
        """
        What it says, read

        """
        table_name     = "stuff"

        db             = AppGlobal.qsql_db_access.db

        msg      = ("System_sub_count_rpt:")
        self.parent_window.output_msg( msg, clear = True )

        sql     = """
            SELECT system, sub_system, COUNT(*) as sub_system_count
            FROM help_info
            WHERE system IS NOT NULL AND sub_system IS NOT NULL
            GROUP BY system, sub_system
            ORDER BY system, sub_system;
            """

        query      = QSqlQuery( db )

        query_ok   =  qsql_utils.query_exec_error_check( query = query, sql = sql, raise_except = True )

        # self.parent_window.output_msg( sql )

        while query.next():
            # a_id        = query.value(0)
            # value_1        = query.value(1)
            # value_2   = query.value(2)

            msg      = (f" : {query.value(0) = }  { query.value(1) = }  { query.value(2) = }  ")

            self.parent_window.output_msg(  msg )

        self.parent_window.activate_output_tab()

    #-------------------------
    def create_sql( self,   ):
        """
        What it says, read

        """
        table_name     = self.table_widget.currentText()
        self.parent_window.output_msg(   f"for table {table_name = }", clear = True )

        a_table    = data_dict.DATA_DICT.get_table( table_name )

        sql        = a_table.to_sql_create()
        msg    = f"{sql} "
        self.parent_window.output_msg(  msg )
        self.parent_window.activate_output_tab()


# ----------------------------------------
class KeyWordTab( QWidget ):
    """
    what it says

    maint and report on key word tables
    """
    def __init__(self, parent_window ):
        """

        """
        super().__init__()

        # self.criteria_dict          = {}
        # self.critera_widget_list    = []
        # self.critera_is_changed     = True
        self.parent_window          = parent_window
        self.key_words_widget       = None      # set to value in gui if used

        self.tab_name               = "DbMaint"
        self.build_gui()

    # -----------------------------
    def build_gui( self,   ):
        """

        """
        vlayout              = QVBoxLayout( self )

        # ---- new row
        layout              = QHBoxLayout( self )
        vlayout.addLayout( layout )

        # ---- table combobox
        widget              = QComboBox()

        self.table_widget   = widget

        a_list              = [
                         'help_key_word',
                         'stuff_key_word',
                         'plant_key_word',
                         'people_key_word' ]

        widget.addItems( a_list )
        widget.setCurrentIndex( 0 )
        layout.addWidget( widget )

        widget              = QPushButton( "key_word_dups" )
        self.q_pbutton_1    = widget
        connect_to          = self.key_word_dups
        widget.clicked.connect(  connect_to   )
        layout.addWidget( widget )

        widget              = QPushButton( "rebuild_key_words" )
        connect_to          = self.rebuild_key_word
        widget.clicked.connect( connect_to  )
        layout.addWidget( widget )

        # ---- new row
        layout              = QHBoxLayout( self )
        vlayout.addLayout( layout )

        widget              = QPushButton( "!!" )
        # connect_to          = self.system_sub_count_rpt
        # widget.clicked.connect( connect_to  )
        layout.addWidget( widget )


    # -------------------------
    # -------------------------
    def rebuild_key_word( self,   ):
        """
        What it says, read

        """
        db                  = AppGlobal.qsql_db_access.db

        IKW_TABLE_DICT
        kw_table_name       = self.table_widget.currentText()
        table_name          = IKW_TABLE_DICT[ kw_table_name ]


        check_fix.line_out  = self.parent_window.output_msg
        db_check            = check_fix.DbCheck( db )

        msg    = f"Rebuild {table_name = } for key words"
        self.parent_window.output_msg(  msg, clear = True )


        db_check.fix_key_word_index( base_table_name        = table_name,
                                     key_word_table_name    = kw_table_name )

        #check_fix.check_key_words_for_dups( db, table_name )

        # msg    = f"{sql} "
        # self.parent_window.output_msg(  msg )
        self.parent_window.activate_output_tab()



    # ---- reports
    # -------------------------
    def key_word_dups( self,   ):
        """
        What it says, read

        """
        db             = AppGlobal.qsql_db_access.db
        table_name     = self.table_widget.currentText()

        msg    = f"Check {table_name = } for key word duplicates"
        self.parent_window.output_msg(  msg, clear = True )

        check_fix.line_out    = self.parent_window.output_msg
        check_fix.check_key_words_for_dups( db, table_name )

        # msg    = f"{sql} "
        # self.parent_window.output_msg(  msg )
        self.parent_window.activate_output_tab()



    # -------------------------
    def system_sub_count_rpt( self,   ):
        """
        What it says, read

        """
        table_name     = "stuff"
        db             = AppGlobal.qsql_db_access.db

        msg    = f"Record Count for systems and subsudtems {table_name = }"
        self.parent_window.output_msg( msg, clear = True )

        sql     = """
            SELECT system, sub_system, COUNT(*) as sub_system_count
            FROM help_info
            WHERE system IS NOT NULL AND sub_system IS NOT NULL
            GROUP BY system, sub_system
            ORDER BY system, sub_system;
            """

        query      = QSqlQuery( db )

        query_ok   =  qsql_utils.query_exec_error_check( query = query, sql = sql, raise_except = True )

        msg      = ("system_sub_count_rpt:")
        self.parent_window.output_msg( msg, )

        self.parent_window.output_msg( sql, )

        while query.next():
            # a_id        = query.value(0)
            # value_1        = query.value(1)
            # value_2   = query.value(2)

            msg      = (f" : {query.value(0) = }  { query.value(1) = }  { query.value(2) = }  ")
            self.parent_window.output_msg( msg, )

        self.parent_window.activate_output_tab()

    #------------------------
    def create_sql( self,   ):
        """
        What it says, read

        """
        table_name     = self.table_widget.currentText()

        msg    = ( f"Create SQL for table {table_name = }" )
        self.parent_window.output_msg( msg, clear = True )

        a_table    = data_dict.DATA_DICT.get_table( table_name )

        sql        = a_table.to_sql_create()

        msg    = f"{sql} "
        self.parent_window.output_msg( msg, )

        self.parent_window.activate_output_tab()


# ----------------------------------------
class RecordMatchTab( QWidget ):
    """
    what it says

    maint and report on key word tables
    """
    def __init__(self, parent_window ):
        """

        """
        super().__init__()

        # self.criteria_dict          = {}
        # self.critera_widget_list    = []
        # self.critera_is_changed     = True
        self.parent_window          = parent_window
        self.key_words_widget       = None      # set to value in gui if used

        self.tab_name               = "RecordMatch"


        self.build_gui()

    # -----------------------------
    def build_gui( self,   ):
        """

        """
        vlayout              = QVBoxLayout( self )

        # ---- new row
        layout              = QHBoxLayout( self )
        vlayout.addLayout( layout )

        # ---- table combobox
        widget              = QComboBox()

        self.table_widget   = widget

        a_list              =  TABLE_DICT.keys()

        widget.addItems( a_list )
        widget.setCurrentIndex( 0 )
        layout.addWidget( widget )

        widget              = QPushButton( "Missing Text" )
        self.q_pbutton_1    = widget
        connect_to          = self.find_missing_text
        widget.clicked.connect(  connect_to   )
        layout.addWidget( widget )

        widget              = QPushButton( "Excess Text " )
        connect_to          = self.find_excess_text
        widget.clicked.connect( connect_to  )
        layout.addWidget( widget )

        # ---- new row
        layout              = QHBoxLayout( self )
        vlayout.addLayout( layout )

    # ---- reports
    # -------------------------
    def find_excess_text( self,   ):
        """
        What it says, read

        """
        db                  = AppGlobal.qsql_db_access.db
        table_name          = self.table_widget.currentText()
        text_table_name     = TABLE_DICT[table_name]

        msg    = f"Check find_excess_text {table_name = } {text_table_name = } "
        self.parent_window.output_msg(  msg, clear = True )

        check_fix.line_out    = self.parent_window.output_msg
        check_fix.find_excess_text( db, table_name, text_table_name )

        self.parent_window.activate_output_tab()

    # -------------------------
    def find_missing_text( self,   ):
        """
        What it says, read

        """
        db                  = AppGlobal.qsql_db_access.db
        table_name          = self.table_widget.currentText()
        text_table_name     = TABLE_DICT[table_name]

        msg    = f"Check find_missing_text {table_name = } {text_table_name = } "
        self.parent_window.output_msg(  msg, clear = True )

        check_fix.line_out    = self.parent_window.output_msg
        check_fix.find_missing_text( db, table_name, text_table_name )

        self.parent_window.activate_output_tab()


# ----------------------------------------
class OutputTab( QWidget ):
    """
    what it says


    """
    def __init__(self, parent_window ):
        """

        """
        super().__init__()

        self.parent_window          = parent_window

        self.tab_name               = "Output"
        self.build_gui()

    # -----------------------------
    def build_gui( self,   ):
        """

        """
        vlayout              = QVBoxLayout( self )

        self._build_gui_bot( vlayout )

        # # ---- new row
        # layout              = QHBoxLayout( self )
        # vlayout.addLayout( layout )

        # # ---- table combobox
        # widget              = QComboBox()

        # self.table_widget   = widget

        # a_list              = [
        #                  'help_key_word',
        #                  'stuff_key_word',
        #                  'plant_key_word',
        #                  'people_key_word' ]

        # widget.addItems( a_list )
        # widget.setCurrentIndex( 0 )
        # layout.addWidget( widget )


        # widget              = QPushButton( "key_word_dups" )
        # self.q_pbutton_1    = widget
        # connect_to          = self.key_word_dups
        # widget.clicked.connect(  connect_to   )
        # layout.addWidget( widget )

        # widget              = QPushButton( "!!rebuild_key_words" )
        # # connect_to          = self.record_count_rpt
        # # widget.clicked.connect( connect_to  )
        # layout.addWidget( widget )

        # # ---- new row
        # layout              = QHBoxLayout( self )
        # vlayout.addLayout( layout )

        # widget              = QPushButton( "!!" )
        # # connect_to          = self.system_sub_count_rpt
        # # widget.clicked.connect( connect_to  )
        # layout.addWidget( widget )


    # -------------------------------
    def _build_gui_bot(self, layout  ):
        """
        make the bottom of the gui, mostly the large
        message widget
        layouts
            a vbox for main layout
        """
        # ---- new row
        row_layout      = QHBoxLayout(   )
        layout.addLayout( row_layout,  )

        # ----
        widget              = QTextEdit("load\nthis should be new row ")
        self.msg_widget     = widget
        #widget.clicked.connect( self.load    )
        row_layout.addWidget( widget,   )
        self.output_edit    = widget


    # -------------------------

    # ---- reports
    # -------------------------

    # -------------------------
    def system_sub_count_rpt( self,   ):
        """
        What it says, read

        """



    # ---- Actions none yet


    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = "\n>>>>>>>>>>* xxxxxx *<<<<<<<<<<<<"

        return a_str

# ---- eof