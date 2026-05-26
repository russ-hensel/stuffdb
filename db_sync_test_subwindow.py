#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""
does not do full records so far just one in list
    >>find   get_list_columns
    >>find   data_dict


"""

# --------------------
if __name__ == "__main__":
    import main
    pass
# --------------------

# ---- imports
#from   functools import partial
#import inspect
import logging
#import os
#import time
#from pathlib import Path

#from qtpy          import QtCore, QtWidgets

from qtpy.QtCore   import ( QDate, QDateTime,
                               QModelIndex,
                               Qt,
                               Slot,
                               QObject, Signal )

from qtpy.QtWidgets import (
                             QFileDialog,
                             QComboBox,
                             QGroupBox,
                             QHBoxLayout,
                             QLabel,
                             QLineEdit,
                             QHeaderView,
                             QMdiSubWindow,
                             QMessageBox,
                             QPushButton,
                             QSpacerItem,
                             QSizePolicy,
                             QTabWidget,
                             QTextEdit,
                             QVBoxLayout,
                             QWidget,
                             QTableView,
                             QTableWidget,
                             QTableWidgetItem,
                             )

from qtpy.QtSql import ( QSqlQuery,
                         QSqlQueryModel,
                         QSqlRecord,
                         QSqlTableModel)

# ---- local imports
#import collections
import parameters
import data_dict_all
#import check_fix


import info_about
import string_utils
import wat_inspector
from   app_global     import AppGlobal
#import qsql_utils
#import gui_qt_ext
#import ex_qt
#import exec_qt
#import mdi_management
#import db_dup_files
#import run_with_dialog
#import file_utils
import base_document_tabs

# ---- import end

WIDTH_MULP      = 8  # for some column widths
LOG_LEVEL       = 10    # higher is more
FIF             = info_about.INFO_ABOUT.find_info_for

EXEC_RUNNER     = None  # setup below
# MARKER              = ">snip"


# ----------------------------------------
class DbSyncTestSubWindow( QMdiSubWindow ):
    """

    """
    def __init__(self, instance_ix = 0 ):
        """
        This is the parent for the document
        It holds our tabs
        when a document is created it registers itself with what mdi...?
        """
        super().__init__()

        self.subwindow_name     = "DbSyncTestSubWindow"

        self.instance_ix        = instance_ix

        mdi_area                = AppGlobal.main_window.mdi_area
            #we could return the subwindow for parent to add
        #sub_window              = self
            # sub_window.setWindowTitle( "this title may be replaced " )
        self.db                 = AppGlobal.qsql_db_access.db

        self.prior_tab          = 0
        self.current_tab        = 0
        self.detail_table_id    = None # for compatible with midi management

        # self.record_state
        self.current_tab_index      = 0       # assumed to be criteria

        self.tab_folder             = QTabWidget() # create for descendants

        # may want to keep at end of this init
        AppGlobal.mdi_management.register_document( self )

        self.detail_table_name      = "xxx"  # need for framework do not delete
        # self.key_word_table_name    = "stuff_key_word"
        # self.text_table_name        = "stuff_text"  # text tables always id and text_data
            # used in text tab base
        self.help_filename          = "tbd.txt"

        self.file_out               = None
        self._build_gui()

        self.__init_2__()

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says
            main notebook and tabs
        """
        main_notebook           = self.tab_folder   # create in parent
        self.main_notebook      = main_notebook

        sub_window              = self
        mdi_area                = AppGlobal.main_window.mdi_area
        # main_notebook.currentChanged.connect( self.on_tab_changed )

        a_tab       = HelpInfoTableTab( self )
        main_notebook.addTab( a_tab, "HelpInfoTableTab" )

        a_tab       = StuffInfoTableTab( self )
        main_notebook.addTab( a_tab, "StuffInfoTableTab" )

        a_tab               = OutputTab( self  )
        self.output_tab     = a_tab
        main_notebook.addTab( a_tab, "Output" )

        self.output_edit    = a_tab.output_edit

        sub_window.setWidget( main_notebook )
        mdi_area.addSubWindow( sub_window )
             # perhaps add to register_document in midi_management

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
    def get_topic( self ):
        """
        for compat with midi manager
         'DbManagementSubWindow' object has no attribute 'get_topic'
        """
        return None

    # --------------------------------
    def set_size_pos( self ):
        """
        run after tab is added??
        """
        # debug_msg = ( "set_size_pos--------------------------------------  " )
        # logging.debug( debug_msg )

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
        what it says
        """
        self.main_notebook.setCurrentWidget( self.output_tab  )

    # --------------------------------
    def output_msg( self, msg, clear = False  ):
        """
        dup with line_out
        """
        self.append_msg( msg, clear = clear  )

    # --------------------------------
    def output_to_file( self, msg ):
        """
        self.parent_window.output_to_file( msg )

        """
        self.file_out.write( msg + "\n" )
        print( msg )

    # --------------------------------
    def open_file_out( self, file_name = "data_management_out.txt" ):
        """

        """
        self.file_name_out   = parameters.PARAMETERS.output_dir + "/" + file_name
        self.file_out        = open( self.file_name_out,
                                    'w',
                                    encoding  = "utf8",
                                    errors    = 'ignore' )

        return self.file_name_out

    # --------------------------------
    def close_file_out( self,  ):
        """
        what it says, read
        """
        if self.file_out:
            self.file_out.close()
        self.file_out = None

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

    #----------------------------
    def to_top_of_msg( self,   ):
        """
        read it --

        """
        text_edit   = self.output_edit
        cursor      = text_edit.textCursor()
        cursor.movePosition( cursor.Start )
        text_edit.setTextCursor(cursor)
        text_edit.ensureCursorVisible()

    #----------------------------
    def get_output_edit( self, ):
        """
        read it --

        may not need
        """
        return self.output_edit

    # --------------------------------
    def closeEvent(self, event):
        """
        may not be complete -- for example pending updates
        """
        AppGlobal.mdi_management.forget_document(  self )
        self.on_close()
        event.accept()

    # --------------------------------
    @Slot()
    def on_close( self ):
        """
        just debug for now
        """
        debug_msg  = (f"{self.windowTitle()} has been closed")
        logging.debug( debug_msg )

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
        """universal __str__ """
        return string_utils.obj_to_str( self )

# ----------------------------------------
class BaseInfoTableTab( QWidget, QObject ):  # object because of signals and slots
    """
    what it says
    """
    def __init__(self, parent_window ):
        """

        """
        super().__init__()

        self.parent_window          = parent_window
        # self.key_words_widget       = None      # set to value in gui if used
        self.ix_seq                 = 0         # just a seqential counter for inserts, prehaps drop
        self.ix_col_id              = 0         # not sure alway 0 is this where the id is?
        self.table_name             = None
        self.tab_name               = None
        self.sync_table             = None  # build later
        #self.build_gui()           # in descendant
        sender_signal               = AppGlobal.mdi_management.update_sync_obj.update_sync_signals.update_sync_pre
        sender_signal.connect( self.update_sync_pre )

    # -----------------------------
    def build_gui( self,   ):
        """
        what it says, read
        """
        vlayout             = QVBoxLayout( self )

        layout              = QHBoxLayout(  )
        vlayout.addLayout( layout )

        # ---- clear
        widget              = QPushButton( "Clear" )
        # self.q_pbutton_1    = widget
        connect_to          = self.clear
        widget.clicked.connect(  connect_to   )
        layout.addWidget( widget )

        self.build_table( layout )

    # -------------------------------------
    def build_table( self, layout ):
        """
        what it says read
            but really the sync table
        Returns:
            none
        """
        columns             = data_dict_all.SCHEMA.get_list_columns( self.table_name )

        # ----  sync table
        table               = self.make_a_table( columns )
        self.sync_table     = table

        col_head_texts   = [ "seq" ]  # plus one for sequence
        self.col_names   = [ "seq" ]
        col_head_widths  = [ "10"  ]

        # this works with the wrong column headings, they may be defined elsewhere like in build gui
        # but this is at least better
        col_head_texts   = [  ]  # we were off so
        self.col_names   = [  ]
        col_head_widths  = [  ]

        for i_column in columns:  # why not comp
            self.col_names.append(   i_column.column_name  )
            col_head_texts.append(   i_column.col_head_text  )
            col_head_widths.append(  i_column.col_head_width  )

        #table.setContextMenuPolicy( QtCore.Qt.CustomContextMenu )

        # table.setContextMenuPolicy( CustomContextMenu )
        # table.customContextMenuRequested.connect( self.show_history_context_menu )

        # table.cellClicked.connect( self.on_cell_clicked )
        layout.addWidget( table )

    # ------------------------
    def make_a_table( self, columns ):
        """
        may refactor back in
        """
        table               = QTableWidget(
                                       0, len( columns ), self )  # row column  parent

        # ---- column header and width
        for ix_col, i_column in enumerate( columns ):
            #rint( f" {ix_col = } { i_width = }")
            table.setHorizontalHeaderItem( ix_col, QTableWidgetItem( i_column.col_head_text )  )
            table.setColumnWidth(          ix_col, i_column.col_head_width * WIDTH_MULP )

        table.setSelectionBehavior( QTableView.SelectRows )  # Select entire rows
        base_document_tabs.table_widget_no_edit( table )

        return table

    # -------------------------------
    @Slot( object, str, str, int, object, )
    def update_sync_pre( self,
                        sender,
                        type_of_change,      # select update add delete
                        table_name,
                        table_id,
                        record_or_dict,
                          ):
        """
        think makes all of a table widget non editable
        may want to refactor or put in utility
        """
        msg    = f"update_sync_pre {sender = } {type_of_change =} {table_name = } \n     {table_id = } {record_or_dict = } "
        logging.debug( msg )

        if table_name != self.table_name:
            return

        if isinstance( record_or_dict, dict ):
            return # so far only do dicts

        if   type_of_change in [ "select", "update", ]:
            self.record_to_table( record_or_dict )

        elif type_of_change in [ "delete", ]:
            self.delete_row_by_id( table_id )

    # -------------------------------------
    def record_to_table( self, record ):
        """
        what it says read

        """
        table           = self.sync_table  # QTableWidget

        a_id            = record.value( "id" )
        # str_id          = str( a_id )

        is_insert       = True
        ix_row          = self.find_id_in_table( a_id, table )

        if ix_row >= 0:
            debug_msg   = ( f"record_to_table found row {ix_row} in "
                             "future update maybe if it works ")
            logging.debug( debug_msg )
            # need update action, almost same as insert
            is_insert       = False

        # ---- insert
        if is_insert:
            self.ix_seq     += 1
            row_position    = table.rowCount()
            table.insertRow( row_position )
            ix_row          = row_position   # or off by 1

        else:
            pass

        ix_col          = -1

        ix_col          += 1

        if is_insert:
            item             = QTableWidgetItem( str( self.ix_seq  ) )
            table.setItem( ix_row, ix_col, item   )

        for i_col_name in self.col_names:
            item             = QTableWidgetItem( str( record.value( i_col_name ) ) )
            table.setItem( ix_row, ix_col, item )
            ix_col          += 1

        pass

    # ------------------------
    def find_id_in_table( self, a_id, table  ):
        """
        what it says read
        return ix_row or -1 if not found
        just a linear search
        """
        str_id              = str( a_id )
        # table               = self.history_table  # QTableWidget(

        ix_found            = -1

        for row in range( table.rowCount() ):
            item    = table.item( row, self.ix_col_id )

            if item is None:
                msg   = ( "find_id_in_table error !!")
                logging.error( msg )
                #breakpoint()     # pdb.set_trace()  # Start the debugger here
                return - 1

            #rint( f"find_id_in_table {item.text()}" )
            # if no item,no match
            if item and item.text() == str_id:
                ix_found = row

        #rint( f">>>>>>>>>>>>find_row_with_text {str_id = } {ix_found = }")
        return ix_found   # check the caller for -1

    # --------------------------------
    def delete_row_by_id( self, id_to_delete ):
        """
        !! refactor rewrite -- would only do one row
        Delete a row from QTableWidget where the value in column 0 matches id_to_delete.
        ?? use the find_id_in_table for less redundant code

        table    = self.sync_table
        ix_row          = self.find_id_in_table( id_to_delete, table )
        if ix_row >= 0:
            table.removeRow( ix_row )
            table.viewport().update() # if just one row

        """
        table    = self.sync_table

        # Iterate through rows from bottom to top to avoid index shifting
        for row in reversed(range( table.rowCount()) ):
            item = table.item( row, 0 )

            if item and item.text() == str(id_to_delete):
                debug_msg  = (f"SyncTable_delete_row_by_id Deleting row {row} with id = {id_to_delete}")
                logging.log( LOG_LEVEL,  debug_msg, )

                table.removeRow( row )
                table.viewport().update() # if just one row -- and this will stop
                return

        debug_msg  = (f"SyncTable delete_row_by_id No row found with id = {id_to_delete}")
        logging.log( LOG_LEVEL,  debug_msg, )

    #-------------------------------------
    def clear( self, ):
        """
        What it says, read
            get current id, then loop thru line
            delete all where id does not match
        """
        # current_id = self.parent_window.detail_table_id
        table      = self.sync_table

        # Iterate through rows from bottom to top to avoid index shifting
        for row in reversed( range( table.rowCount()) ):
            #item = table.item(row, 0)
            # if item and item.text() != str(current_id):
            #     # print(f"Deleting row {row} with   {item = }")
            table.removeRow(row)

# ----------------------------------------
class HelpInfoTableTab( BaseInfoTableTab ):
    """
    what it says
    """
    def __init__(self, parent_window ):
        """

        """
        super().__init__( parent_window )

        self.parent_window          = parent_window
        # self.key_words_widget       = None      # set to value in gui if used
        self.ix_seq                 = 0         # just a seqential counter for inserts, prehaps drop
        self.ix_col_id              = 0         # not sure alway 0 is this where the id is?
        self.table_name             = "help_info"
        self.tab_name               = "HelpInfoTableTab"
        self.sync_table             = None  # build later
        self.build_gui()
        sender_signal               = AppGlobal.mdi_management.update_sync_obj.update_sync_signals.update_sync_pre
        sender_signal.connect( self.update_sync_pre )

# ----------------------------------------
class StuffInfoTableTab( BaseInfoTableTab ):
    """
    what it says
    """
    def __init__(self, parent_window ):
        """

        """
        super().__init__( parent_window )

        self.parent_window          = parent_window
        # self.key_words_widget       = None      # set to value in gui if used
        self.ix_seq                 = 0         # just a seqential counter for inserts, prehaps drop
        self.ix_col_id              = 0         # not sure alway 0 is this where the id is?
        self.table_name             = "stuff"
        self.tab_name               = "StuffInfoTableTab"
        self.sync_table             = None  # build later
        self.build_gui()
        sender_signal               = AppGlobal.mdi_management.update_sync_obj.update_sync_signals.update_sync_pre
        sender_signal.connect( self.update_sync_pre )

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

    # -------------------------------
    def _build_gui_bot( self, layout  ):
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

    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = "\n>>>>>>>>>>* xxxxxx *<<<<<<<<<<<<"

        return a_str


# just for prelim test
# if __name__ == "__main__":
#     test_clean_path_part()

# ---- eof


