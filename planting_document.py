#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 09:56:07 2024

@author: russ
"""
# ---- tof
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main

# --------------------

import functools
import sqlite3
import time
from   datetime import datetime






#from   functools import partial
#import collections

from qt_compat import QApplication, QAction, exec_app, qt_version
from PyQt.QtWidgets import QMainWindow, QToolBar, QMessageBox
from qt_compat import Qt, DisplayRole, EditRole, CheckStateRole
from qt_compat import TextAlignmentRole
from qt_compat import QSizePolicy_Expanding, QSizePolicy_Minimum, QSizePolicy_Fixed, QSizePolicy_Preferred
from qt_compat import OnManualSubmit, OnRowChange, OnFieldChange
from qt_compat import NoEditTriggers
from qt_compat import SelectRows, SelectItems,ExtendedSelection



from PyQt.QtCore import(   QModelIndex,
                            QRectF,
                            QDate,
                            QModelIndex,
                            Qt,
                            QTimer,
                            pyqtSlot, )


from PyQt.QtGui import (QIntValidator,
                         QPainter,
                         QPixmap,
                         QStandardItem,
                         QStandardItemModel,
                     )

# from PyQt.QtSql import QSqlDatabase, QSqlQuery, QSql_Model
from PyQt.QtSql import (QSqlDatabase,
                         QSqlQuery,
                         QSqlQueryModel,
                         QSqlRelation,
                         QSqlRelationalDelegate,
                         QSqlRelationalTableModel,
                         QSqlTableModel)

#from PyQt.QtGui import ( QAction, QActionGroup, )

from PyQt.QtWidgets import (QAbstractItemView,

                        QApplication,
                        QButtonGroup,
                        QCheckBox,
                        QComboBox,
                        QDateEdit,
                        QDialog,
                        QDockWidget,
                        QFileDialog,
                        QFrame,
                        QGraphicsPixmapItem,
                        QGraphicsScene,
                        QGraphicsView,
                        QGridLayout,
                        QHBoxLayout,
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
                        QSizePolicy,
                        QSpacerItem,
                        QSpinBox,
                        QTabWidget,
                        QTableView,
                        QTableWidget,
                        QTableWidgetItem,
                        QTextEdit,
                        QVBoxLayout,
                        QWidget,
                        )

# ---- imports local
import base_document_tabs
import custom_widgets as cw
import key_words
import mdi_management
import planting_document_edit
import qt_sql_query
import qt_with_logging
import logging
import combo_dict_ext
import data_dict

import gui_qt_ext
import string_utils as string_util
import string_utils
from   app_global import AppGlobal
import people_document
import people_document_edit
import import_utils


#from pubsub import pub

logger              = logging.getLogger( )
LOG_LEVEL           = 20 # level form much debug
           #  higher is more debugging    logging.log( LOG_LEVEL,  debug_msg, )

EVENT_FIELD_DICT        = None  # created later?


IX_EVENT_ID             = 0 # many are magic convert to this
IX_EVENT_ID_OLD         = 1
IX_EVENT_PLANT_ID       = 2
IX_EVENT_PLANT_ID_OLD   = 3
IX_EVENT_DATE           = 4
IX_EVENT_DLR            = 5
IX_EVENT_CMNT           = 6
IX_EVENT_TYPE           = 7


# ---- end parms

# ----------------------------------------
class PlantingDocument( base_document_tabs.DocumentBase ):
    """
    for the planting table....
    """
    def __init__(self, instance_ix = 0 ):
        """
        the usual
        """
        super().__init__( instance_ix )

        self.detail_table_name  = "planting"
        self.text_table_name    = "planting_text"  # text tables always id and text_data
        self.subwindow_name     = "PlantingSubWindow"

        self._build_gui()
        self.__init_2__()
    # --------------------------------
    @property
    def topic( self ):
        """
        of the detail record
        """
        topic     = "planting topic "
        if self.record_state:
            topic    = f"{topic} {self.record_state = }"
        topic    = f"{topic} {self.detail_tab.name_field.text()}"

        return   topic

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says
            pretty much build the tabs in the usual way
            from criteira to history
        """
        main_notebook           = self.tab_folder   # create in parent
        # main_notebook           = QTabWidget()
        self.main_notebook      = main_notebook   # phase out for tab_folder !!

        sub_window              = self
        mdi_area                = AppGlobal.main_window.mdi_area
        # main_notebook.currentChanged.connect( self.on_tab_changed )

        ix                        = -1

        ix                       += 1
        self.criteria_tab_index   = ix
        self.criteria_tab         = PlantingCriteriaTab( self )
        main_notebook.addTab(       self.criteria_tab, "Criteria" )

        ix                       += 1
        self.list_tab_index      = ix
        self.list_tab            = PlantingListTab( self  )
        main_notebook.addTab(  self.list_tab, "List"    )

        ix                       += 1
        self.detail_tab_index     = ix
        self.detail_tab           = PlantingDetailTab( self )
        main_notebook.addTab( self.detail_tab, "Detail"     )

        ix                       += 1
        self.picture_tab_index     = ix
        self.picture_tab           = base_document_tabs.StuffdbPictureTab( self )
        main_notebook.addTab( self.picture_tab, "Picture"     )

        ix                         += 1
        self.text_tab_index         = ix
        self.text_tab               = PlantingTextTab( self )
        main_notebook.addTab( self.text_tab, "Text"     )

        ix                        += 1
        self.history_tab_index     = ix
        self.history_tab           = PlantingHistorylTab( self )
        main_notebook.addTab( self.history_tab, "History"    )

        sub_window.setWidget( main_notebook )
        mdi_area.addSubWindow( sub_window )

        sub_window.show()

    # -------------------------------------
    def i_am_hsw(self):
        """
        make sure call is to here for testing
        """
        print( "planting sub window, i_am_hsw")

    # -------------------------------------
    def default_new_row( self ):
        """
        defaults values for a new row in the detail and the
        text tabs

        Changes state of detail and related tabs

        """
        next_key      = AppGlobal.key_gen.get_next_key(
            self.detail_table_name )
        self.detail_tab.default_new_row( next_key )
        self.text_tab.default_new_row(   next_key )

    # -------------------------------------
    def copy_prior_row( self ):
        """tail_tab.default_new_row( next_key )
        default values with copy for a new row in the detail and the
               text tabs
        probably can promote, may need different func name on text so tabs can be the same?
        Returns:
            None.
            """
        next_key      = AppGlobal.key_gen.get_next_key(
            self.detail_table_name )
        self.detail_tab.copy_prior_row( next_key )
        self.text_tab.copy_prior_row(  next_key )

    # ---- capture events ----------------------------
    # ------------------------------------------

    # ------------------------------------------
    def on_list_double_clicked( self, index: QModelIndex ):
        """
        !! not currently used so promote? -- or delete
        what it says, read

        Args:
            index (QModelIndex):  where clicked

        """
        row                 = index.row()
        column              = index.column()
        # " value: {value}" )
        print( f"Clicked on_list_double_clicked on row {row}, column {column}, value tbd" )

    # --------------------------
    def on_tab_changed_promoted_in_part_maybe( self, event ):
        """
        not currently use, but may trigger a save or other action
        in the future
        """
        # old_prior               = self.prior_tab
        self.prior_tab          = self.current_tab  # because not updated yet
        self.current_tab        = self.main_notebook.currentIndex()
        current_text            = self.main_notebook.tabText(
            self.current_tab )
        # rint( f"on_tab_changed {self.prior_tab = } {self.current_tab = }   {current_text = }" )

        # # could be done at any time
        # self.tap_page_Planting_fn   = self.a_notebook.tab( self.a_notebook.select(), 'text' ) + ".txt"
        # rint( f"tap_page_Planting_fn  >>{self.tap_page_Planting_fn}<< "
        #        "for tabpage on_changed need to remove spaces" )
        # #rint( f"on_changed  {event} for tabpage" )
        # #rint( self.get_info() )

    # ---- sub window interactions ---------------------------------------
    # ------------------------------------------

    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = ">>>>>>>>>>* plantingSubWindow  *<<<<<<<<<<<<"

        return a_str

# ----------------------------------------
class PlantingCriteriaTab( base_document_tabs.CriteriaTabBase, ):
    """
    criteria for list selection
    """
    def __init__(self, parent_window ):
        """
        the usual

        """
        super().__init__( parent_window )
        self.tab_name            = "PlantingCriteriaTab"

    # ------------------------------------------
    def _build_tab( self, ):
        """
        what it says, read
        put page into the notebook
        """
        # debug_util.get_traceback_list()
        page             = self

        layout           = QHBoxLayout( page )
                # can we fold in to next

        grid_layout      = gui_qt_ext.CQGridLayout( col_max = 10 )
        layout.addLayout( grid_layout )

        self._build_top_widgets_grid( grid_layout )

        # ----key words
        widget                = QLabel( "Key Words" )
        grid_layout.new_row()
        grid_layout.addWidget( widget )

        widget                  = cw.CQLineEdit(
                                                 field_name = "key_words"   )
        self.critera_widget_list.append( widget )
        self.key_words_widget   = widget  # is needed for paste
        widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        grid_layout.addWidget( widget, columnspan = 3 )

        # ----id
        widget                = QLabel( "ID" )
        grid_layout.new_row()
        grid_layout.addWidget( widget )

        widget                  = cw.CQLineEdit(
                                             field_name = "table_id" )
        self.id_field           = widget
        self.critera_widget_list.append( widget )
        #widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        grid_layout.addWidget( widget, )    # columnspan = 3 )



        # ---- name like
        grid_layout.new_row()
        widget  = QLabel( "Name (like)" )
        grid_layout.addWidget( widget )

        widget                  = cw.CQLineEdit(
                                                 field_name = "name"   )
        self.name_widget        = widget
        self.critera_widget_list.append( widget )
        widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        grid_layout.addWidget( widget )



        # ---- Order by
        grid_layout.new_row()
        widget  = QLabel( "!!Order by" )
        grid_layout.addWidget( widget )

        widget                 = cw.CQComboBox(
                                                 field_name = "order_by"   )
        self.critera_widget_list.append( widget )

        widget.addItem('name')
        widget.addItem('lbl_name')
        widget.addItem('Title??')

        grid_layout.addWidget( widget )

        # ---- Order by Direction
        #placer.new_row()
        widget  = QLabel( "Direction" )
        grid_layout.addWidget( widget )

        widget                     = cw.CQComboBox(
                                         field_name  = "order_by_dir",  )
        self.critera_widget_list.append( widget )

        widget.addItem('Ascending')
        widget.addItem('Decending')


        print( "build_tab build criteria change put in as marker ")
        widget.currentIndexChanged.connect( lambda: self.criteria_changed(  True   ) )
        grid_layout.addWidget( widget )

        # ---- criteria changed should be in parent
        grid_layout.new_row()
        widget  = QLabel( "criteria_changed_widget" )
        self.criteria_changed_widget  = widget
        grid_layout.addWidget( widget )

        # # ---- push up on page still needs adjust
        # width    = 350
        # widget   = QSpacerItem( width, 310, QSizePolicy.Expanding, QSizePolicy.Minimum )
        # grid_layout.new_row()
        # # grid_layout.addWidget( widget )
        # grid_layout.addItem( widget, grid_layout.ix_row, grid_layout.ix_col )

        # # ---- function_on_return( self )
        # for i_widget in self.critera_widget_list:
        #     i_widget.function_on_return   = self.criteria_select
        # ---- function_on_return( self )
        for i_widget in self.critera_widget_list:
            # ---- new  only really changes some edits
            i_widget.on_value_changed       = lambda: self.criteria_changed( True )
            i_widget.on_return_pressed      = self.criteria_select

        QTimer.singleShot( 0, self.key_words_widget.setFocus )

    # -------------
    def criteria_select( self,     ):
        """
        do the selection specified by the criteria in the gui

        """
        #rint( "criteria_select  >>>>>>>>>>>>>>>>>>>>>> " )
        parent_document                 = self.parent_window

        model                           = parent_document.list_tab.list_model
        #rint( "begin channel_select for the list")
        query                           = QSqlQuery( AppGlobal.qsql_db_access.db )
        query_builder                   = qt_sql_query.QueryBuilder( query, print_it = False, )

        kw_table_name                   = "platning_key_word"
        column_list                     = [ "id", "id_old", "name", "add_kw", "bed_id",       ]

        a_key_word_processor            = key_words.KeyWords( kw_table_name,
                                             AppGlobal.qsql_db_access.db )
        query_builder.table_name        = parent_document.detail_table_name
        query_builder.column_list       = column_list

        # ---- add criteria
        criteria_dict                   = self.get_criteria()

        # ---- key words
        criteria_key_words              = criteria_dict[ "key_words" ]
        criteria_key_words              = a_key_word_processor.string_to_key_words( criteria_key_words )
        key_word_count                  = len(  criteria_key_words )

        criteria_key_words              = ", ".join( [ f'"{i_word}"' for i_word in criteria_key_words ] )
        criteria_key_words              = f'( {criteria_key_words} ) '    # ( "one", "two" )

        if key_word_count > 0:
            query_builder.group_by_c_list   = column_list
            query_builder.sql_inner_join    = " planting_key_word  ON planting.id = planting_key_word.id "
            query_builder.sql_having        = f" count(*) = {key_word_count} "

            query_builder.add_to_where( f" key_word IN {criteria_key_words}" , [] )

        # !! change to bind variables sql inject
        # ---- id  table_id
        table_id     = criteria_dict[ "table_id" ].strip().lower()
        if table_id:
            add_where       =  f' planting.id = {table_id} '
            query_builder.add_to_where( add_where, [ ])

        # ---- name like
        name                          = criteria_dict[ "name" ].strip().lower()
        if name:
            add_where       = "lower( name )  like :name"   # :is name of bind var below
            query_builder.add_to_where( add_where, [(  ":name",
                                                     f"%{name}%" ) ])

        # ---- order by
        order_by   = criteria_dict[ "order_by" ]

        if   order_by == "name":
            column_name = "name"
        elif order_by == "lbl_name":
            column_name = "lbl_name"
        else:   # !! might better handel this
            column_name = "name"

        query_builder.add_to_order_by(    column_name, "ASC",   )

        query_builder.prepare_and_bind()

        debug_msg      = f"{query_builder = }"
        logging.log( LOG_LEVEL,  debug_msg, )

        is_ok  = AppGlobal.qsql_db_access.query_exec_model( query,
                                                  model,
                                                  msg = "HelpSubWindow criteria_select" )

        debug_msg      = (  f"criteria_select {query.executedQuery()} "  )
        logging.log( LOG_LEVEL,  debug_msg, )

        parent_document.main_notebook.setCurrentIndex( parent_document.list_tab_index )
        self.critera_is_changed = False

# ----------------------------------------
class PlantingListTab( base_document_tabs.ListTabBase   ):

    def __init__(self, parent_window ):

        super().__init__( parent_window )

        self.list_ix            = 5  # should track selected an item in detail

        self.tab_name           = "PlantingListTab"

        self._build_gui()

# ----------------------------------------
class PlantingDetailTab( base_document_tabs.DetailTabBase  ):
    """
    """
    def __init__(self, parent_window  ):
        """
        Args:
            parent_window (TYPE): DESCRIPTION.

        """
        super().__init__( parent_window )


        self.tab_name                   = "PlantingDetailTab"
        self.key_word_table_name        = "planting_key_word"
        self.post_init()
        #self.enable_send_topic_update   = True

    # -------------------------------------
    def _build_gui( self ):
        """
        modeled on other documents
        """
        page            = self
        tabxxx             = self
        max_col         = 10
        self.max_col    = max_col
        box_layout_1    =  QVBoxLayout( page )

        # placer          = gui_qt_ext.PlaceInGrid(
        #                     central_widget  = box_layout_1,
        #                     a_max           = max_col,
        #                     by_rows         = False  )

        # tab_layout      = placer

        # !! change name
        placer          = gui_qt_ext.CQGridLayout( col_max = max_col )

        tab_layout      = placer
        box_layout_1.addLayout( placer )


        # ----fields
        self._build_fields( placer )

        # ---- tab area
        tab_folder   = QTabWidget()

        tab_folder.setMovable( True )
        tab_layout.new_row()
        tab_layout.addWidget( tab_folder, columnspan   = max_col )

        sub_tab      = PlantingEventSubTab( self )
        self.event_sub_tab   = sub_tab
        tab_folder.addTab( sub_tab, "Events" )

        sub_tab      = PlantingPictureSubTab( self )

        #self.pictures_tab       = sub_tab
        self.picture_sub_tab    = sub_tab
        self.sub_tab_list.append( sub_tab )
        tab_folder.addTab( sub_tab, "Pictures" )

        self.prior_tab          = 0
        self.current_tab        = 0

        # Main notebook
        detail_notebook           = QTabWidget()
        self.detail_notebook      = detail_notebook

        # ---- buttons
        button_layout = QHBoxLayout()

        # create_button = QPushButton("Create Default")
        # create_button.clicked.connect( self.create_default_row )
        # button_layout.addWidget(create_button)

        # button = QPushButton( "To History" )
        # rint( "need detail_to_history")
        # button.clicked.connect( self.parent_window.detail_to_history )
        # button_layout.addWidget(update_button)

        #tab_layout.addLayout( button_layout )

    #---------------------------------
    def _build_fields( self, layout ):
        """
        What it says, read
            this is generated code except
            tweaks
                for spacing
                plant_id   is done by hand
                    plant_id  by hand id_in_old ---------------

        """
        width  = 50
        for ix in range( self.max_col ):  # try to tweak size to make it work
            widget   = QSpacerItem( width,
                                   10,
                                   QSizePolicy_Expanding,
                                   QSizePolicy_Minimum )

            layout.addItem( widget, 0, ix  )  # row column

        # ---- code_gen: TableDict.to_build_form
            #2025_04_01 for planting -- begin table entries

        # ---- id
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "id", )
        self.id_field     = edit_field
        edit_field.rec_to_edit_cnv        = edit_field.cnv_int_to_str
        edit_field.dict_to_edit_cnv       = edit_field.cnv_int_to_str
        edit_field.edit_to_rec_cnv        = edit_field.cnv_str_to_int
        edit_field.edit_to_dict_cnv       = edit_field.cnv_str_to_int
        edit_field.setReadOnly( True )
        edit_field.setPlaceholderText( "id" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 1 )

        # ---- id_old
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "id_old", )
        self.id_old_field     = edit_field
        edit_field.setReadOnly( True )
        edit_field.setPlaceholderText( "id_old" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 1 )

        # ---- name
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "name", )
        self.name_field     = edit_field
        edit_field.is_keep_prior_enabled        = True
        edit_field.setPlaceholderText( "name" )
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 4 )

        # # ---- plant_id
        # edit_field                  = cw.CQLineEdit(
        #                                         parent         = None,
        #                                         field_name     = "plant_id", )
        # self.plant_id_field     = edit_field
        # edit_field.setPlaceholderText( "plant_id" )
        # self.data_manager.add_field( edit_field, is_key_word = False )
        # layout.addWidget( edit_field, columnspan = 2 )

        # ---- plant_id  by hand id_in_old ---------------
        edit_field                  = cw.CQDictComboBox(
                                                parent         = None,
                                                field_name     = "plant_id", )
        self.plant_id_field           = edit_field


        widget_ext                    = combo_dict_ext.PLANT_COMBO_DICT_EXT
        widget_ext.add_widget( edit_field )
        edit_field.setPlaceholderText( "plant_id" )
        #edit_field.set_dictionary     = self.parent_window.stuff_containers
        #edit_field.get_info_for_id    = get_info_for_id          # will self get passed

        #edit_field.set_dictionary( AppGlobal.mdi_management.plant_containers )

            # to get info given an id
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )

        layout.addWidget( edit_field, columnspan = 2 )


        # ---- bed_old
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "bed_old", )
        self.bed_old_field     = edit_field
        edit_field.setPlaceholderText( "bed_old" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- location
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "location", )
        self.location_field     = edit_field
        edit_field.setPlaceholderText( "location" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- add_kw
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "add_kw", )
        self.add_kw_field     = edit_field
        edit_field.is_keep_prior_enabled        = True
        edit_field.setPlaceholderText( "add_kw" )
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- descr
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "descr", )
        self.descr_field     = edit_field
        edit_field.setPlaceholderText( "descr" )
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- type
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "type", )
        self.type_field     = edit_field
        edit_field.setPlaceholderText( "type" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- cmnt
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "cmnt", )
        self.cmnt_field     = edit_field
        edit_field.setPlaceholderText( "cmnt" )
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- lbl
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "lbl", )
        self.lbl_field     = edit_field
        edit_field.setPlaceholderText( "lbl" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- bed !! does not exist needs a lookup and ddl  probably
        # edit_field                  = cw.CQLineEdit(
        #                                         parent         = None,
        #                                         field_name     = "bed", )
        # self.bed_field     = edit_field
        # edit_field.setPlaceholderText( "bed" )
        # self.data_manager.add_field( edit_field, is_key_word = False )
        # layout.addWidget( edit_field, columnspan = 2 )

        # ---- lbl_name
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "lbl_name", )
        self.lbl_name_field     = edit_field
        edit_field.setPlaceholderText( "lbl_name" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- itag1
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "itag1", )
        self.itag1_field     = edit_field
        edit_field.setPlaceholderText( "itag1" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- planting_status
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "planting_status", )
        self.planting_status_field     = edit_field
        edit_field.setPlaceholderText( "planting_status" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- need_stake
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "need_stake", )
        self.need_stake_field     = edit_field
        edit_field.setPlaceholderText( "need_stake" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- need_label
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "need_label", )
        self.need_label_field     = edit_field
        edit_field.setPlaceholderText( "need_label" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- need_work
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "need_work", )
        self.need_work_field     = edit_field
        edit_field.setPlaceholderText( "need_work" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

    # ----------------------------
    def fetch_detail_row( self, id = None ):
        """
        Args:
            id can be external or as chat has it fetched

        Returns:
            None.
        !! could be promoted ... most has been
        """
        id      = self.id_field.text()
        ##self.detail_table_id    = id
        print( f"PlantingDocumentDetaiTab fetch_row { id=}")
        self.fetch_detail_row_by_id( id )

    # -----------------------------
    def copy_prior_row( self, next_key ):
        """
        could use create default_new_row
        what it says
            this is for a new row on the window -- no save
            fill with default
        Returns:
            None.

        """
        # ---- capture needed fields
        descr      = self.descr_field.text()
        add_kw     = self.add_kw_field.text()
        # rint(  ia_qt.q_line_edit( self.name_field,
        #                   msg = "this is the name field",  ) # include_dir = True ) )
        # url      = self.url_field.text()
        # mypref   = self.mypref_field.text()
        # mygroup  = self.mygroup_field.text()
        # add_ts   = self.add_ts_field.text()
        edit_ts  = self.edit_ts_field.text()
        edit_ts  = "self.edit_ts_field.text()"   # !! test

        self.default_new_row(  next_key )

        # ---- set the defaults
        self.descr_field.setText( descr + "*" )
        # self.url_field.setText( url )

        # # ---- ??redef add_ts
        # a_ts   = str( time.time() ) + "sec"

        # self.add_ts_field.setText(  a_ts )
        # self.edit_ts_field.setText( a_ts )
        # self.id_field.setText( str( next_key ) )

    # -----------------------------
    def default_new_row(self, next_key ):
        """
        what it says
            this is for a new row on the window -- no save
        arg:
            next_key for table, just trow out if not used
        Returns:
            None.

        """

    # ------------------------
    def field_to_record( self, record ):
        """
        for Planting now from photo
        for the updates, get the gui data into the record
        assume for new add time and id are already there?? or in a self.xxx
        since not sure how works put in instance
        we still need more fields her and probably in record to field
        """
        if self.record_state    == base_document_tabs.RECORD_NEW:  # may be needed
            record.setValue("id", int( self.current_id ) )

        # record.setValue( "name",       self.name_field.text())
        #record.setValue( "add_kw", self.add_kw_field.text())
        record.setValue( "name", self.name_field.text())
        # record.setValue( "photo_fn",      self.photo_fn_field.text())
        # ---- timestamps
        # record.setValue( "add_ts",   self.add_ts_field.text()) # should have already been set
        #record.setValue( "edit_ts", self.edit_ts_field.text())

        self.parent_window.record_to_history_table( record )


    # ------------------------
    def clear_fields(self):
        """
        what it says, read
        what fields, need a bunch of rename here
        clear_fields  clear_fields  -- or is this default
        !! but should users be able to?? may need on add -- this may be defaults
        """
        self.id_field.clear()
        # self.descr_field.clear()
        # self.name_field.clear()

        self.name_field.clear()
        #self.add_kw_field.clear()
        # self.url_field.clear()
        # self.mypref_field.clear()

    # ------------------------
    def get_picture_file_name(self):
        """
        some promotable -- but picture is special only one file, rest
        work differently
        see picture document

        return file_name or None if no file name
        """
        print( "get_picture_file_name to be implemented" )
        return ""  # none will cause exception  , just need file name that does not exist

    # ------------------------------------------
    def plant_containers_update( self, just_warning ):
        """sent down from on high update the stuff_id in dict  """
        self.plant_idfind_name_in_old_field.update_dictionary( just_warning )



# ==================================
class PlantingTextTab( base_document_tabs.TextTabBase  ):
    """
    """
    #--------------------------------------
    def __init__(self, parent_window  ):
        """
        Args:
            parent_window (TYPE): DESCRIPTION.
        Returns:
            None.
        """
        # self.table_name          = "stuff"  not needed we get fro parent
        super().__init__( parent_window )
        self.tab_name            = "PlantingTextTab"

        self.table              = "planting_text"
        self.table_name         = self.table   # !! eliminate one or other

        self.post_init()

# ----------------------------------------
class PlantingHistorylTab( base_document_tabs.HistoryTabBase   ):
    """ """
    def __init__(self, parent_window ):
        """
        """
        super().__init__( parent_window )

        # self.parent_window   = parent_window
        self.tab_name            = "PlantingHistorylTab"

# ----------------------------------------
class PlantingEventSubTab( base_document_tabs.SubTabWithEditBase ):
    """

    """
    def __init__(self, parent_window ):
        """
        """
        super().__init__( parent_window )

        self.table_name      = "planting_event"

        global EVENT_FIELD_DICT   # where when is used ??
        if EVENT_FIELD_DICT is None:
            EVENT_FIELD_DICT   = data_dict.rpt_sub_tab_columns_order( self.table_name, verbose = False  )

        self.field_dict     = EVENT_FIELD_DICT  # order is ix  key is field_name then a dict

        self._build_model()
        self._build_gui()


    # ---------------------------------
    def _build_model( self, ):
        """
        put in some init do delay build = lazy
        """
        model              = EventSqlTableModel( self, self.db )
        self.model         = model

        model.setTable( self.table_name )
        model.setEditStrategy(  OnManualSubmit )

    # ------------------------------------------
    def _build_dialog( self, edit_data ):
        """
        what it says, read
        # Open dialog with the current data
        #dialog = StuffEventDialog(self, edit_data=data)
        """
        dialog   = planting_document_edit.EditPlantingEvent( self, edit_data )
        return   dialog

    # ------------------------------------------
    def fix_add_keys( self, form_data ):
        """ """
        # print( "SubTabBase still need to fix this perahps add_dict_adjust( form_data ) not clear how to paramaterize ")
        # ver 3  --- but some may be passed in ?
        a_id                        = AppGlobal.key_gen.get_next_key( self.table_name )
        form_data[ "id" ]           = a_id
        form_data[ "planting_id" ]  = self.current_id

    # ---------------------------------------
    def select_by_id( self, id ):
        """
        maybe make anscestor and promote
        could be paramaterized with key name ??
        but is it worth it for 4 lines
        """
        model               = self.model

        self.current_id     = id
        model.setFilter( f"planting_id = {id}" )
        # model_write.setFilter( f"pictureshow_id = {id} " )
        model.select()

    # ----------------------------------
    def edit_selected_event(self):
        """
        Open dialog to edit the currently selected event.
        """
        selected_data = self.get_selected_row_data()
        if selected_data is None:
            return

        row, data = selected_data

        # Open dialog with the current data
        #dialog = StuffEventDialog(self, edit_data=data)
        dialog = planting_document_edit.EditPlantingEvent( self, edit_data=data )
            # self the parent tab

        model     = self.model

        if dialog.exec_() == QDialog.Accepted:
            form_data = dialog.get_form_data()
            # 0 id 1 id_old 2 planting_id_old 3 planting_id 4
            # event_dt 5 dlr 6 cmnt 7 type 8 dt_mo INTEGER, 9 dt_day INTEGER, 10 day_of_year INTEGER
            # Update the row with the new data
            # model.setData( model.index(row, 0), form_data["id"])
            # model.setData( model.index(row, 2), form_data["stuff_id"])
            # model.setData( model.index(row, 4), form_data["event_dt"])
            # model.setData( model.index(row, 5), form_data["dlr"])
            # model.setData( model.index(row, 6), form_data["cmnt"])
            # model.setData( model.index(row, 7), form_data["type"])

            # zz EVENT_FIELD_DICT  EVENT_FIELD_DICT PEOPLE_CONTACT_COLUMN_DICT

            for field_name, field_ix in  EVENT_FIELD_DICT.items():
                model.setData( model.index( row, field_ix ), form_data[ field_name ] )

# ------------------------------------
class PlantingPictureSubTab( base_document_tabs.PictureListSubTabBase ):
    """
    almost all promoted even this may not be necessary
    """
    def __init__(self, parent_window ):
        super().__init__( parent_window )
        self.pictures_for_table  = "planting"
        # perhaps call first ??

# ------------------------------------
class EventSqlTableModel( QSqlTableModel ):
    def __init__(self, parent=None, db=QSqlDatabase()):
        """ """
        super().__init__(parent, db)
        # Specify multiple columns to make non-editable (e.g., columns 1 and 2)
        self.non_editable_columns = { 99 }
            # 99 not used Columns ..doe it have to be in init or is synamic ..


    def flags(self, index: QModelIndex):
        """
        from chat, not really used as for non edit
        """
        # Get default flags from the base class
        flags = super().flags(index)
        # Remove editable flag for the specified columns
        if index.column() in self.non_editable_columns:
            return flags & ~Qt.ItemIsEditable  # Make these columns non-editable
        return flags

    # -------------------------------
    def data(self, index: QModelIndex, role= DisplayRole):
        """
        for special formatting
        and alignment
        zz
        IX_EVENT_DLR
        """
        col = index.column()

        # Check role first
        if role == DisplayRole:
            # Handle display formatting for event_dt (column 2)
            # data_dict may have column ix from name
            if False:
                pass
            # if   col == 4:  # event_dt
            #     value = super().data(index, Qt.EditRole)
            #     if value not in [ None, "" ]:
            #         #return datetime.fromtimestamp(value).strftime("%Y-%m-%d")
            #         return import_utils.string_to_ts_tenths( value )
            #     return value  # Return raw value if None

            elif col == IX_EVENT_DATE:  # this a string should it be an int?
                value = super().data(index, EditRole)
                # better try except
                # if value is not None:
                #     return datetime.fromtimestamp(value).strftime("%Y-%m-%d")
                # return value  # Return raw value if None
                try:
                    #return datetime.fromtimestamp(value).strftime( cw.DATE_FORMAT ) # "%Y-%m-%d" )
                    return datetime.fromtimestamp(value).strftime(  cw.PY_DATE_FORMAT )  # "%Y-%m-%d"
                    # from duston_widgets import DATE_FORMAT
                except ( ValueError, TypeError ) as error:
                    # error_message = str(error)
                    # msg  = (f"Caught an error: {error_message}")
                    # print( msg )
                    return None   # is this ok

        elif role == EditRole:
            # Return raw value for editing/database for my dates an int
            if col == 4:
                debug    = super().data(index, EditRole)
                return super().data(index, EditRole)

        elif role == TextAlignmentRole:
            # Handle alignment for all columns
            if col == 0:  # id
                return Qt.AlignLeft | Qt.AlignVCenter
            elif col == 1:  # stuff_id
                return Qt.AlignCenter | Qt.AlignVCenter
            elif col == 2:  # event_dt
                return Qt.AlignRight | Qt.AlignVCenter

        # Default to base class for all other roles and columns
        return super().data(index, role)

# ---- eof ------------------------------
