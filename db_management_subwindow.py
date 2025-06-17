#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 07:26:39 2025

@author: russ
"""


# ---- tof

# ---- imports

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

import data_dict
import gui_qt_ext
import info_about
#import key_words
import string_util
import text_edit_ext
#import table_model
import wat_inspector
from app_global     import AppGlobal
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
#import ex_qt
#import exec_qt
#import mdi_management


# ---- import end

FIF             = info_about.INFO_ABOUT.find_info_for

EXEC_RUNNER     = None  # setup below
# MARKER              = ">snip"





# ---- end imports


#-------------------------------

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


# !! may need fix
        #self.tab_folder.currentChanged.connect( self.on_tab_changed )

        #combo_dict_ext.build_it( AppGlobal.qsql_db_access.db )   # do not forget

        # self.detail_table_name      = "stuff"
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
        self.first_tab         = FirstTab( self  )
        main_notebook.addTab(       self.first_tab, "First Tab" )

        # ix                       += 1
        # self.list_tab_index      = ix
        # self.list_tab            = StuffListTab( self  )
        # main_notebook.addTab(  self.list_tab, "List"    )

        # ix                       += 1
        # self.detail_tab_index     = ix  #
        # self.detail_tab           = StuffDetailTab( self )
        # main_notebook.addTab( self.detail_tab, "Detail"     )

        # ix                       += 1
        # self.picture_tab_index     = ix
        # self.picture_tab           = base_document_tabs.StuffdbPictureTab( self )
        # main_notebook.addTab( self.picture_tab, "Picture"     )

        # ix                         += 1
        # self.detail_text_index      = ix  # phase out !!
        # self.text_tab_index         = ix
        # self.text_tab               = StuffTextTab( self )
        # main_notebook.addTab( self.text_tab, "Text"     )

        # ix                         += 1
        # self.history_tab_index     = ix
        # self.history_tab           = StuffHistoryTab( self )
        # main_notebook.addTab( self.history_tab, "History"    )

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
    def output_msg( self, msg  ):
        """

        """
        print( msg )

    # --------------------------------
    def get_topic( self ):
        """
        of the detail record -- implemented in stuff in people not working
        """
        return "DocumentBase need override for topic in descendant"




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
class FirstTab( QWidget ):
    """
    what it says
    """
    def __init__(self, parent_window ):
        """
        lots of variable may not be used .... clean up later
        """
        super().__init__()

        self.criteria_dict          = {}
        self.critera_widget_list    = []
        self.critera_is_changed     = True
        self.parent_window          = parent_window
        self.key_words_widget       = None      # set to value in gui if used

        self.tab_name               = "CriteriaTab set in child"
        self.build_gui()

    # -----------------------------
    def build_gui( self,   ):
        """

        """

        layout              = QHBoxLayout()

        widget              = QPushButton( "q_pbutton_1" )
        self.q_pbutton_1    = widget
        # connect_to          = self.pb_1_clicked
        # widget.clicked.connect(  connect_to   )
        layout.addWidget( widget )



    # -------------------------------
    def _build_top_widgets_grid( self, grid_layout ):
        """
        what it says read, std for all criteria tabs
        lets add a Hbox
        now on an hbox placed on the grid layout
        return
            mutates
            creates new row, uses creates another
        """
        grid_layout.new_row()
        button_layout    = QHBoxLayout()
        grid_layout.addLayout( button_layout, grid_layout.ix_col, grid_layout.ix_row, 1, 5  )
        #row: int, column: int, rowSpan: int, columnSpan:
            # int, alignment: Union[Qt.Alignment, Qt.AlignmentFlag] = Qt.Alignment()):
        grid_layout.new_row()

        # ---- may need a spacer where titles are in rest of page
        # width    = 35
        # widget   = QSpacerItem( width, 10, QSizePolicy.Expanding, QSizePolicy.Minimum )
        # #grid_layout.new_row()
        # # grid_layout.addWidget( widget )
        # grid_layout.addItem( widget, grid_layout.ix_row, grid_layout.ix_col    )  # row column
        # grid_layout.ix_col  += 1

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

        grid_layout.new_row()

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

    # -------------------------------
    def add_buttons( self, placer ):
        """
        debug
        this should be called add_debug_widgets
        """
        placer.new_row()
        widget  = QLabel( "unknown" )
        self.criteria_changed_widget = widget
        self.criteria_changed_widget.setText( "self.criteria_changed_widget" )
        placer.place( widget, columnspan = 2 )

        # ---- buttons
        a_widget        = QPushButton( "Clear Criteria change widget " )
        a_widget.clicked.connect(  self.clear_criteria )
        placer.new_row()
        placer.place( a_widget )

        a_widget        = QPushButton( "Run Select" )
        a_widget.clicked.connect(  self.parent_window.criteria_select )
        #placer.new_row()
        placer.place( a_widget )

        a_widget        = QPushButton( "show_criteria" )
        a_widget.clicked.connect( lambda: self.show_criteria(   ) )
        #placer.new_row()
        placer.place( a_widget )

        a_widget        = QPushButton( "Criteria Unchanged" )
        a_widget.clicked.connect( lambda: self.criteria_changed( False ) )
        #placer.new_row()
        placer.place( a_widget )

    # -------------------------
    def make_criteria_date_widget( self,   ):
        """
        THE WIDGETS HAVE CHANGED SINCE THIS WAS WRITTEN, FIX WHEN NEXT USED

        what it says, read
        make our standard date widgets

        return two widgets both same holdover from old code fix sometime ,
        starting and ending widget in a tuple
        """
        #widget                  = QDateEdit()
        widget                   = cw.CQDateCriteria()   # need types here perhaps !!
        widget.editingFinished.connect( lambda: self.criteria_changed( True ) )
        widget.userDateChanged.connect( lambda: self.criteria_changed( True ) )
        widget.setCalendarPopup( True )
        widget.setDisplayFormat( "dd/MM/yyyy" )
        widget.setDate( QDate( 2025, 1, 1 ))
        #widget_to_layout            = widget.container
        return ( widget, widget )
        # widget, widget_to_layout  =self.make_criteria_date_widget()

    # ---- Actions
    def criteria_select_if( self,   ):
        """
        What it says, read
            note: strip the strings
        """
        if self.critera_is_changed:
            self.criteria_select()
        else:
            pass
            # debug_msg  = ( "criteria_select_if no select !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            # logging.debug( debug_msg )
        # put in criteria_select  !! self.criteria_is_changed = False
        self.critera_is_changed = False


    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = "\n>>>>>>>>>>* CriteriaTabBase *<<<<<<<<<<<<"

        return a_str

# ---- eof