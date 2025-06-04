#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""

album_document


"""

# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main

    #main.main()
# --------------------

import functools
import logging
#import sqlite3
import time
import traceback
import subprocess

import data_dict
import gui_qt_ext
import string_util
import wat_inspector
from app_global import AppGlobal
from PyQt5.QtCore import QDate, QModelIndex, QRectF, Qt, QTimer, pyqtSlot
from PyQt5.QtGui import (QIcon,
                         QIntValidator,
                         QPainter,
                         QPixmap,
                         QStandardItem,
                         QStandardItemModel)
from PyQt5.QtSql import (QSqlDatabase,
                         QSqlDriver,
                         QSqlError,
                         QSqlField,
                         QSqlQuery,
                         QSqlQueryModel,
                         QSqlRecord,
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
                             QDateEdit,
                             QDockWidget,
                             QFileDialog,
                             QFrame,
                             QGraphicsPixmapItem,
                             QGraphicsScene,
                             QGraphicsView,
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
                             QSizePolicy,
                             QSpacerItem,
                             QSpinBox,
                             QTableView,
                             QTableWidget,
                             QTableWidgetItem,
                             QTabWidget,
                             QTextEdit,
                             QToolBar,
                             QVBoxLayout,
                             QWidget)

# ---- local imports
import base_document_tabs
import custom_widgets as cw
import key_words
import picture_viewer
import qt_sql_query
import app_exceptions
import data_manager
# ---- end imports
LOG_LEVEL  = 10


# ----------------------------------------
class AlbumDocument( base_document_tabs.DocumentBase ):
    """
    for the photoshow table....
    """
    # --------------------------------------
    def __init__(self, instance_ix = 0 ):
        """
        the usual
        """
        super().__init__( instance_ix )

        self.detail_table_name  = "photoshow"
        # text tables always id and text_data
        self.text_table_name    = "photoshow_text"
        self.help_filename      = "album_doc.txt"
        self.subwindow_name     = "Album Document"

        # !! perhaps in ancestor to a post innit
        title       = self.subwindow_name
        if instance_ix !=0:
            title  += f" {instance_ix}"

        self.setWindowTitle( title )
        AppGlobal.mdi_management.update_menu_item( self )

        self._build_gui()

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says
            code seems a bit unclear, works, not ready to clean up
        """
        mdi_area                = AppGlobal.main_window.mdi_area
        # we could return the sub window for parent to add
        sub_window              = self

        # # Main notebook with  tabs
        main_notebook           = self.tab_folder   # create in parent
        self.main_notebook      = main_notebook

        # ---- tab building
        ix                        = -1

        ix                       += 1
        self.criteria_tab_index   = ix
        self.criteria_tab         = self._build_tab_criteria( self )
            # !! dump the function and pull back to here
        main_notebook.addTab(       self.criteria_tab, "Criteria" )

        ix                         += 1
        self.list_tab_index         = ix
        self.list_tab               = self._build_tab_list(  self  )
        main_notebook.addTab(      self.list_tab, "List of Albums"    )

        # ix                         += 1
        # self.detail_text_index      = ix
        # self.text_tab               = self._build_tab_text( self )
        # main_notebook.addTab( self.text_tab,    "Text"     )

        # for reasons have to do out of order

        self.detail_tab           = AlbumDetailTab(  self  )
        self.picture_tab          = self._build_tab_picture( self )
        #self.picture_tab.

        ix                       += 1
        self.detail_tab_index     = ix
        main_notebook.addTab( self.detail_tab, "Detail"     )

        ix                         += 1
        self.picture_tab_index     = ix
        self.photo_index           = ix
        main_notebook.addTab( self.picture_tab, "Picture"     )

        # ix                         += 1
        # self.photo_index           = ix
        # # rint( f"__init__  {self = }")
        # self.picture_tab             = self._build_tab_picture( self )
        # # rint( f">>>>> SubWindow _build_tab_photo __init__  {self.picture_tab = }")
        # main_notebook.addTab( self.picture_tab, "Picture"     )

        ix                        += 1
        self.history_tab_index     = ix
        self.history_tab           = self._build_tab_history( self )
        main_notebook.addTab( self.history_tab, "History"    )

        sub_window.setWidget( main_notebook )
        mdi_area.addSubWindow( sub_window )

        sub_window.show()

    # ------------------------------------------
    def _build_tab_list( self, parent_window   ):
        """
        what it says, read
        """
        return AlbumListTab( parent_window )

    # ------------------------------------------
    def _build_tab_criteria( self, parent_window ):
        """
        what it says, read
            put page into the notebook
        """
        return AlbumCriteriaTab( parent_window  )

    # -------------------------------------
    def _build_tab_picture( self, parent_window ):
        """
        '_build_tab_picture'
        """
        # debug_msg    =( f"_build_tab_picture  {parent_window=}")
        # logging.log( LOG_LEVEL,  debug_msg, )

        return base_document_tabs.StuffdbPictureTab( parent_window )

    # -----------------------------
    def _build_tab_history( self, parent_window ):
        """
        what it says, read
        """
        return AlbumHistoryTab( parent_window )

    # ---- capture events ----------------------------
    # ------------------------------------------
    def on_history_clickedxxx( self, index: QModelIndex ):
        """
        !! finish me
        Args:
            index (QModelIndex): DESCRIPTION.

        !! promote the whole thing?? need key to be id col 0 seems ok
        might be functioalize if we use an argument for self.list.tab
        """
        debug_msg    = ( "on_history_clicked  save first if necessary")
        logging.log( LOG_LEVEL,  debug_msg, )

        row                     = index.row()
        column                  = index.column()

        self.list_tab.list_ix   = row

        id_index                = self.history_tab.history_model.index(
            index.row( ), 0 )
        db_key                  = self.history_tab.history_model.data(
            id_index, Qt.DisplayRole )
        debug_msg = ( f"on_history_clicked Clicked on list row {row}, column "
                      "{column}, {db_key=}" )  # " value: {value}" )
        logging.debug( debug_msg )

        self.fetch_row_by_id( db_key )

        # set tab
        self.main_notebook.setCurrentIndex( self.detail_tab_index )
        self.detail_tab.id_field.setText( str( db_key )  )

    # ------------------------------------------
    def on_list_double_clickedxxxxx( self, index: QModelIndex ):
        """
        !! not currently used so promote? -- or delete
        what it says, read

        Args:
            index (QModelIndex):  where clicked

        """
        row                 = index.row()
        column              = index.column()
        # " value: {value}" )
        debug_msg = ( f"Clicked on row {row}, column {column}, value tbd" )
        logging.debug( debug_msg )

    # ---- sub window interactions ---------------------------------------
    # -------------------------------------
    def default_new_rowxxxxxx( self ):
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

    # ---------------------------------------
    def display_photo( self, file_name  ):
        """
        what it says, mostly focused on the detail tab
        should not be in Album
        """
        debug_msg   = ( f"<<<<<< display_photo  {self.picture_tab=}")
        logging.log( LOG_LEVEL,  debug_msg, )
        # logger.log( fll, "" )
        self.picture_tab.display_file( file_name )

    # ---- pictures
    # -------------------------------------
    def add_photo_to_show( self, photo_dict ):
        """
        may except on no show selected
        """
        debug_msg  = ( "AlbumDocument  add_photo_to_show  ")
        logging.debug( debug_msg )
        self.detail_tab.add_photo_to_show( photo_dict )

    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = ">>>>>>>>>>* AlbumDocument  *<<<<<<<<<<<<"

        return a_str

# ----------------------------------------
class AlbumCriteriaTab( base_document_tabs.CriteriaTabBase, ):
    """
    criteria for list selection
    """
    def __init__(self, parent_window ):
        """
        the usual
        """
        super().__init__( parent_window )
        self.tab_name            = "AlbumCriteriaTab"

    # ------------------------------------------
    def _build_tab( self, ):
        """
        what it says, read
        put page into the notebook
        """
        page            = self
        layout          = QHBoxLayout( page )
                # can we fold in to next

        grid_layout      = gui_qt_ext.CQGridLayout( col_max = 10 )
        layout.addLayout( grid_layout )

        self._build_top_widgets_grid( grid_layout )

        # ----id
        widget                = QLabel( "ID" )
        grid_layout.new_row()
        grid_layout.addWidget( widget )

        #widget                  = QLineEdit()
        widget                  = cw.CQLineEdit(
                                     field_name = "table_id" )
        self.critera_widget_list.append( widget )
        widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        grid_layout.addWidget( widget, )    # columnspan = 3 )

        # ----id_old
        widget                = QLabel( "ID Old" )
        grid_layout.new_row()
        grid_layout.addWidget( widget )

        widget                  = cw.CQLineEdit(
                                     field_name = "id_old" )
        self.critera_widget_list.append( widget )
        widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        grid_layout.addWidget( widget, )    # columnspan = 3 )

        # ----key words
        widget                = QLabel( "Key Words" )
        grid_layout.new_row()
        grid_layout.addWidget( widget )

        widget                  = cw.CQLineEdit(
                                     field_name = "key_words" )
        self.key_words_widget   = widget
        self.critera_widget_list.append( widget )
        widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        grid_layout.addWidget( widget, columnspan = 3 )

        # ----name
        widget                = QLabel( "name" )
        grid_layout.new_row()
        grid_layout.addWidget( widget )

        widget                  = cw.CQLineEdit(
                                     field_name = "name" )
        self.critera_widget_list.append( widget )
        widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        grid_layout.addWidget( widget, columnspan = 3 )

        # ---- Order by
        grid_layout.new_row()
        widget  = QLabel( "Order by" )
        grid_layout.addWidget( widget )

        widget                 = cw.CQComboBox(
                                     field_name = "order_by" )
        self.critera_widget_list.append( widget )

        widget.addItem('name')
        widget.addItem("name - ignore case")
        widget.addItem('descr')
        widget.addItem('id')
        widget.addItem('id_old')
        widget.addItem('start_date')

        grid_layout.addWidget( widget )

        # ---- Order by Direction
        #grid_layout.new_row()
        widget  = QLabel( "Direction" )
        grid_layout.addWidget( widget )

        widget                 = cw.CQComboBox(
                                     field_name = "order_by_dir" )
        self.critera_widget_list.append( widget )

        widget.addItem('Ascending')
        widget.addItem('Decending')

        debug_msg = ( "build_tab build criteria change put in as marker ")
        logging.debug( debug_msg )

        widget.currentIndexChanged.connect( lambda: self.criteria_changed( True ) )
        grid_layout.addWidget( widget )

        # ---- debug criteria changed should be in parent
        grid_layout.new_row()
        widget  = QLabel( "criteria_changed_widget" )
        self.criteria_changed_widget  = widget
        grid_layout.addWidget( widget )

        # ---- function_on_return( self )
        for i_widget in self.critera_widget_list:
            i_widget.function_on_return   = self.criteria_select


    # -------------
    def criteria_select( self,     ):
        """
        from help   mod in process -- at least some works

        """
        debug_msg = ( "criteria_select   trying to add key words " )
        logging.debug( debug_msg )

        parent_document                 = self.parent_window

        model                           = parent_document.list_tab.list_model
        #rint( "begin channel_select for the list")
        query                           = QSqlQuery()
        query_builder                   = qt_sql_query.QueryBuilder( query, print_it = False, )

        kw_table_name                   = "photoshow_key_words"
        #column_list                     = [ "id", "id_old", "name",  "add_kw",         ]

        # !! next is too much
        columns    = data_dict.DATA_DICT.get_list_columns( self.parent_window.detail_table_name )
        #col_head_texts   = [ "seq" ]  # plus one for sequence
        col_names        = [   ]
        #col_head_widths  = [ "10"  ]
        for i_column in columns:
            col_names.append(        i_column.column_name  )
            #col_head_texts.append(   i_column.col_head_text  )
            #col_head_widths.append(  i_column.col_head_width  )
        column_list                     = col_names

        a_key_word_processor            = key_words.KeyWords( kw_table_name, AppGlobal.qsql_db_access.db )
        query_builder.table_name        = parent_document.detail_table_name
        query_builder.column_list       = column_list

        # ---- add criteria
        criteria_dict                   = self.get_criteria()

        # !! change to bind variables sql inject
        # ---- id  table_id
        table_id     = criteria_dict[ "table_id" ].strip().lower()
        if table_id:
            add_where       =  f' id = {table_id} '
            query_builder.add_to_where( add_where, [ ])

        # ---- id_old
        id_old     = criteria_dict[ "id_old" ].strip().lower()
        if id_old:
            add_where       =  f' id_old = "{id_old}" '
            query_builder.add_to_where( add_where, [ ])

        # ---- key words
        criteria_key_words              = criteria_dict[ "key_words" ]
        criteria_key_words              = a_key_word_processor.string_to_key_words( criteria_key_words )
        key_word_count                  = len(  criteria_key_words )

        criteria_key_words              = ", ".join( [ f'"{i_word}"' for i_word in criteria_key_words ] )
        criteria_key_words              = f'( {criteria_key_words} ) '    # ( "one", "two" )

        if key_word_count > 0:
            query_builder.group_by_c_list   = column_list
            query_builder.sql_inner_join    = " photoshow_key_word  ON photoshow.id = photoshow_key_word.id "
            query_builder.sql_having        = f" count(*) = {key_word_count} "

            query_builder.add_to_where( f" key_word IN {criteria_key_words}" , [] )

        # ---- name like
        name                          = criteria_dict[ "name" ].strip().lower()
        if name:
            add_where       = "lower( name )  like :name"   # :is name of bind var below
            query_builder.add_to_where( add_where, [(  ":name",
                                                     f"%{name}%" ) ])

        # # ---- name like
        # latin_name                          = criteria_dict[ "latin_name" ].strip().lower()
        # if name:
        #     add_where       = "lower( latin_name )  like :latin_name"   # :is name of bind var below
        #     query_builder.add_to_where( add_where, [(  ":latin_name",
        #                                              f"%{latin_name}%" ) ])

        # ---- order by
        order_by   = criteria_dict[ "order_by" ]

        # no harm if too many -- switch to a dict?
        if   order_by == "name":
            column_name = "name"
        elif order_by == "latin_name":
            column_name = "latin_name"
        elif order_by == "start_date":
            column_name = "start_date"
        elif   order_by == "cmnt":
            column_name = "cmnt"
        elif order_by == "name":
            column_name = "name"
        elif order_by == "name - ignore case":
            column_name = "lower(name)"
        elif order_by == "id":
            column_name = "id"
        elif order_by == "id_old":
            column_name = "id_old"
        else:   # !! might better handel this
            column_name = "name"

        order_by_dir   = criteria_dict[ "order_by_dir" ].lower( )

        # debug_msg    = f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{column_name = }  {order_by_dir = }"
        # logging.debug( debug_msg )

        if "asc" in order_by_dir:
            literal   = "ASC"
        else:
            literal   = "DESC"

        query_builder.add_to_order_by(    column_name, literal,   )

        query_builder.prepare_and_bind()

        msg      = f"{query_builder = }"
        AppGlobal.logger.debug( msg )

        is_ok  = AppGlobal.qsql_db_access.query_exec_model( query,
                                                  model,
                                                  msg = "HelpSubWindow criteria_select" )

# ------------
#         help_document.main_notebook.setCurrentIndex( help_document.list_tab_index )
#         self.critera_is_changed = False
# -----------

        debug_msg      = (  query.executedQuery()   )
        logging.debug( debug_msg )

        parent_document.main_notebook.setCurrentIndex( parent_document.list_tab_index )
        self.critera_is_changed = False

# ----------------------------------------
class AlbumListTab( base_document_tabs.ListTabBase  ):
    """
    """
    def __init__(self, parent_window ):
        """
        the usual
        """
        super().__init__( parent_window )

        self.tab_name        = "AlbumListTab"

        self._build_gui()

# ----------------------------------------
class AlbumDetailTab( base_document_tabs.DetailTabBase  ):
    """
    """
    # ----------------------------------------
    def __init__(self, parent_window  ):
        """
        Args:
            parent_window (TYPE): DESCRIPTION.

        """
        super().__init__( parent_window )

        self.tab_name               = "AlbumDetailTab"

        self.key_word_table_name    = "photoshow_key_word"
        self.post_init()

    # -------------------------------------
    def _build_gui( self ):
        """
        what it says read
        Returns:
            none
        """
        page            = self

        max_col         = 12
        self.max_col    = max_col

        box_layout_1    =  QVBoxLayout( page )

        placer          = gui_qt_ext.CQGridLayout( col_max = max_col )

        tab_layout      = placer
        box_layout_1.addLayout( placer )

        # ----fields
        self._build_fields( placer )

        # ---- tab area
        tab_layout.new_row( )

        tab_folder   = QTabWidget()
        # tab_folder.setTabPosition(QTabWidget.West)
        tab_folder.setMovable(True)
        tab_layout.addWidget( tab_folder, columnspan = max_col )

        # sub_tab          = PhotoshowDetailListTab( self )
        #sub_tab          = self._build_tab_pictures( self )
        sub_tab                =  AlbumPictureSubTab( self )
        self.picture_sub_tab   = sub_tab   # phase out
        self.sub_tab_list.append( sub_tab )
        tab_folder.addTab( sub_tab, "Pictures" )

        # sub_tab      = TestDetaiSubTab( self )
        # tab_folder.addTab( sub_tab, "a test" )

        self.prior_tab          = 0
        self.current_tab        = 0

        # Main notebook with 3 tabs
        detail_notebook           = QTabWidget()
        self.detail_notebook      = detail_notebook

        # main_notebook.currentChanged.connect( self.on_tab_changed )

        # ix                        = -1

        # ix                       += 1
        # self.criteria_tab_index   = ix
        # self.criteria_tab         = self._build_tab_criteria( self )
        # detail_notebook.addTab(   self.criteria_tab,  "Criteria"  )

        # # ---- buttons
        # button_layout = QHBoxLayout()

        # update_button = QPushButton("Update")
        # update_button.clicked.connect(self.update_detail_row )
        # button_layout.addWidget(update_button)

        # tab_layout.addLayout( button_layout )

        # # a second sub layout
        # button_layout = QHBoxLayout()
        # tab_layout.addLayout( button_layout )

    #---------------------------------
    def _build_fields( self, layout ):
        """
        What it says, read
            this is generated code, then tweaked.
            tweaks are:
                ---  spacers
        """
        width    = 10
        for ix in range( self.max_col ):  # try to tweak size to make it work
            widget   = QSpacerItem( width, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
            layout.addItem( widget, 0, ix  )  # row column

        # ---- code_gen: TableDict.to_build_form 2025_04_01 for photoshow -- begin table entries -----------------------

        # ---- id
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "id", )
        self.id_field     = edit_field
        edit_field.setReadOnly( True )
        edit_field.setPlaceholderText( "id" )
        edit_field.rec_to_edit_cnv        = edit_field.cnv_int_to_str
        edit_field.dict_to_edit_cnv       = edit_field.cnv_int_to_str
        edit_field.edit_to_rec_cnv        = edit_field.cnv_str_to_int
        edit_field.edit_to_dict_cnv       = edit_field.cnv_str_to_int
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
        edit_field.setPlaceholderText( "name" )
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 4 )

        # ---- cmnt
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "cmnt", )
        self.cmnt_field     = edit_field
        edit_field.setPlaceholderText( "cmnt" )
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 4 )

        # ---- add_kw
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "add_kw", )
        self.add_kw_field     = edit_field
        edit_field.setPlaceholderText( "add_kw" )
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 4 )

        # ---- type
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "type", )
        self.type_field     = edit_field
        edit_field.setPlaceholderText( "type" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- web_site_dir
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "web_site_dir", )
        self.web_site_dir_field     = edit_field
        edit_field.setPlaceholderText( "web_site_dir" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- create_date
        edit_field                  = cw.CQDateEdit(
                                                parent         = None,
                                                field_name     = "create_date", )
        self.create_date_field     = edit_field
        edit_field.setPlaceholderText( "create_date" )
        edit_field.rec_to_edit_cnv        = edit_field.cnv_int_to_qdate
        edit_field.dict_to_edit_cnv       = edit_field.cnv_int_to_qdate
        edit_field.edit_to_rec_cnv        = edit_field.cnv_qdate_to_int
        edit_field.edit_to_dict_cnv       = edit_field.cnv_qdate_to_int
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- start_date
        edit_field                  = cw.CQDateEdit(
                                                parent         = None,
                                                field_name     = "start_date", )
        self.start_date_field     = edit_field
        edit_field.setPlaceholderText( "start_date" )
        edit_field.rec_to_edit_cnv        = edit_field.cnv_int_to_qdate
        edit_field.dict_to_edit_cnv       = edit_field.cnv_int_to_qdate
        edit_field.edit_to_rec_cnv        = edit_field.cnv_qdate_to_int
        edit_field.edit_to_dict_cnv       = edit_field.cnv_qdate_to_int
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- end_date
        edit_field                  = cw.CQDateEdit(
                                                parent         = None,
                                                field_name     = "end_date", )
        self.end_date_field     = edit_field
        edit_field.setPlaceholderText( "end_date" )
        edit_field.rec_to_edit_cnv        = edit_field.cnv_int_to_qdate
        edit_field.dict_to_edit_cnv       = edit_field.cnv_int_to_qdate
        edit_field.edit_to_rec_cnv        = edit_field.cnv_qdate_to_int
        edit_field.edit_to_dict_cnv       = edit_field.cnv_qdate_to_int
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

    # ----------------------------
    def fetch_detail_row( self, id=None ):
        """
        Args:
            id can be external or as chat has it fetched

        Returns:
            None.
        !! could be promoted
        """
        id         = self.id_field.text()
        debug_msg  = ( f"fetch_row { id=}")
        logging.debug( debug_msg )

        self.fetch_detail_row_by_id( id )

    # -----------------------------
    def delete_detail_row(self):
        """
        looks like could be promoted -- dbkey needs to stay id
              but need to delete detail_children as well
              but need to delete key words as well
        what it says read
         delete_detail_row delete_detail_row
        Returns:
            None.

        """
        model       = self.tab_model
        id          = self.id_field.text()
        if id:
            model.setFilter( f"id = {id}" )
            model.select()
            if model.rowCount() > 0:
                model.removeRow(0)
                model.submitAll()
                QMessageBox.information(self, "Delete Success",
                                        f"Record deleted successfully.{self.this_subwindow=}")
                self.clear_detail_fields()
            else:
                msg   = ( f"Delete Error: No record found with the given ID."
                        f"{self.this_subwindow = } { id = } " )
                QMessageBox.warning(self, "Error", msg )
                logging.error( msg )
                AppGlobal.logger.error( msg )
        else:
            msg  = f"Please enter a valid ID. {self.this_subwindow = } { id = }"
            QMessageBox.warning(self, "Input Error", msg )
            AppGlobal.logger.error( msg )

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
        # descr      = self.descr_field.text()
        name       = self.name_field.text()
        # add_kw     = self.add_kw_field.text()
        # print(  ia_qt.q_line_edit( self.name_field,
        #                   msg = "this is the name field",  ) # include_dir = True ) )
        # url      = self.url_field.text()

        edit_ts  = self.edit_ts_field.text()
        edit_ts  = "self.edit_ts_field.text()"   # !! test

        self.default_new_row(  next_key )

        # ---- set the defaults

        # self.descr_field.setText( descr + "*" )
        self.name_field.setText( name + "*" )

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
        # model    = self.tab_model

        # yt_id    = self.yt_id_field.text()
        # name     = self.name_field.text()
        # #print(  ia_qt.q_line_edit( self.name_field,
        # #                   msg = "this is the name field",  ) # include_dir = True ) )
        # url      = self.url_field.text()
        # mypref   = self.mypref_field.text()


        self.clear_detail_fields()

        # ---- ??redef add_ts
        a_ts   = str( time.time() ) + "sec"
        # record.setValue( "add_ts",  a_ts    )
        self.add_ts_field.setText(  a_ts )
        self.edit_ts_field.setText( a_ts )

        self.id_field.setText( str( next_key ) )

    # -------------------------
    def update_detail_row( self ):
        """
        what it says, read
        row is the model   detail.model ??
        !! change to update_detail_row
        Returns:
            None.
        update_detail_row update_detail_row
        """
        model       = self.tab_model
        id          = self.id_field.text()
        if id:
            model.setFilter(f"id = {id}")
            model.select()
            if model.rowCount() > 0:
                record = model.record(0)

                # ---- special for this table
                record.setValue("name", self.name_field.text())
                # record.setValue("add_kw",     self.add_kw_field.text())


                # ---- timestamps
                record.setValue("add_ts", self.add_ts_field.text())
                record.setValue("edit_ts", self.edit_ts_field.text())

                if model.setRecord(0, record):
                    model.submitAll()
                    msg    = "Record updated successfully. { self.this_subwindow = }"
                    AppGlobal.logger.debug( msg )
                    QMessageBox.information(self, "Update Success", msg )
                else:
                    msg    = f"Update Error Failed to update record. {self.this_subwindow = } {id = }"
                    AppGlobal.logger.error( msg )
                    QMessageBox.warning(self, "Error", msg )
            else:
                msg    = f"No record found with the given ID.{self.this_subwindow = } {id = } "
                AppGlobal.logger.error( msg )
                QMessageBox.warning(self, "Update Error", msg )
        else:
            msg    = f"Input Error", "Please enter a valid ID. { self.this_subwindow = } {id = } "
            AppGlobal.logger.debug( msg )
            QMessageBox.warning(self, "Input Error", msg )

    # ------------------------
    def get_picture_file_name(self):
        """
        some promotable -- but picture is special only one file, rest
        work differently
        see picture document

        return file_name or None if no file name
        """
        msg     = ( "get_picture_file_name to be implemented" )
        logging.debug(   msg )

        return ""  # none will cause exception  , just need file name that does not exist

    # ------------------------
    def field_to_record( self, record ):
        """
        for the updates, get the gui data into the record
        assume for new add time and id are already there?? or in a self.xxx
        since not sure how works put in instance
        we still need more fields her and probably in record to field
        """
        if self.record_state    == base_document_tabs.RECORD_NEW:  # may be needed
            record.setValue("id", int( self.current_id ) )

        record.setValue( "name", self.name_field.text())
        # record.setValue( "add_kw",     self.add_kw_field.text())
        # record.setValue( "descr",      self.descr_field.text())
        # record.setValue( "photo_fn",      self.photo_fn_field.text())
        # ---- timestamps
        # record.setValue( "add_ts",   self.add_ts_field.text()) # should have already been set
        # record.setValue( "edit_ts",  self.edit_ts_field.text())
        self.parent_window.record_to_history_table( record )

    # -------------------------------------
    def add_photo_to_show( self, photo_dict ):
        """
        may except on no show selected
         self.detail_tab
        picture_sub_tab

        """
        debug_msg = ( "Album_detail_tab  add_photo_to_show probably comes from a picture_document  ")
        logging.debug( debug_msg )

        # 'add_photo_to_show'
        self.picture_sub_tab.add_photo_to_show( photo_dict )

# ----------------------------------------
class TestDetaiSubTab( base_document_tabs.DetailTabBase, ):

    def __init__(self, parent_window ):
        """
        the usual

        """
        super().__init__( parent_window )

        self._build_gui()

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says, read
        put page into the notebook

        """
        page            = self


        placer          = gui_qt_ext.PlaceInGrid(
            central_widget=page,
            a_max=0,
            by_rows=False  )

        # a_widget        = QPushButton( "Get Criteria test" )
        # a_widget.clicked.connect(  self.get_criteria )
        # placer.place( a_widget )

        # ---- Channel Like
        a_widget  = QLabel( "xxx:" )
        placer.new_row()
        placer.place( a_widget )

        a_widget    = QLineEdit()

        placer.place( a_widget )
        self.channel_like_widget    = a_widget

        # ---- MyPref
        a_widget  = QLabel( "rrr" )
        placer.place( a_widget )

        a_widget    = QComboBox()
        values      = [ "Ignore", "Item 1", "Item 2", "Item 3"]
        a_widget.addItems( values )
        placer.place( a_widget )
        self.channel_pref_widget    = a_widget

        # self.channel_pref_widget.setCurrentText("Ignore")
        # text = self.channel_pref_widget.currentText()

        # ----Ch MyGroup
        a_widget  = QLabel( "ccc" )
        # placer.new_row()
        placer.place( a_widget )

        a_widget    = QComboBox()
        values      = ( "Ignore", 'Group1'  )
        a_widget.addItems( values )
        # a_widget.setCurrentText("Ignore")
        placer.place( a_widget )
        self.channel_group_widget  = a_widget

        # ----"Order By:"
        a_widget    = QLabel( "Order By:" )
        placer.new_row()
        placer.place( a_widget )

        a_widget    = QComboBox()
        values      = ( "Ignore", "title", 'pub_date', 'watched',
                        'view_count', )
        a_widget.addItems( values )
        placer.place( a_widget )
        self.channel_order_by_widget  = a_widget

        # ---- buttons
        a_widget        = QPushButton( "Do Nothing" )
        # a_widget.clicked.connect(  self.clear_criteria )
        placer.new_row()
        placer.place( a_widget )

    # -------------------------------------
    def __build_gui( self ):
        """
        what it says read
        Returns:
            none
        """
        tab                 = self
        tab_layout          = QVBoxLayout(tab)

        self.id_field       = QLineEdit()
        self.id_field.setValidator( QIntValidator() )
        self.id_field.setPlaceholderText("Enter ID")
        tab_layout.addWidget(self.id_field)

        entry_widget         = QTextEdit()
        self.text_data_field = entry_widget
        entry_widget.setPlaceholderText( "Some Long \n text on a new line " )
        tab_layout.addWidget( entry_widget  )

        # self.name_field = QLineEdit()
        # self.name_field.setPlaceholderText("Name")
        # tab_layout.addWidget(self.name_field)


        # self.mypref_field = QLineEdit()
        # self.mypref_field.setValidator(QIntValidator())
        # self.mypref_field.setPlaceholderText("Preference")
        # tab_layout.addWidget(self.mypref_field)

        button_layout = QHBoxLayout()

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
        # capture needed fields
        # yt_id    = self.yt_id_field.text()
        text_data       = self.text_data_field.text()

        self.default_new_row(  next_key )

        self.text_data_field.setTtext( f"{text_data} \n ------ \n {text_data}")

    # -----------------------------
    def default_new_row(self, next_key ):
        """
        what it says
            this is for a new row on the window -- no save
            needs key but timestamp photo from detail not text
        arg:
            next_key for table, just trow out if not used
        Returns:
            None.

        """
        self.clear_detail_fields()

        self.text_data_field.setText(
            f"this is the default text for id { next_key=}" )

        # # ---- ??redef add_ts
        # a_ts   = str( time.time() ) + "sec"
        # # record.setValue( "add_ts",  a_ts    )
        # self.add_ts_field.setText(  a_ts )
        # self.edit_ts_field.setText( a_ts )

        self.id_field.setText( str( next_key ) )

    # ----------------------------
    def fetch_detail_row( self, id=None ):
        """
        Args:
            id can be external or as chat has it fetched

        Returns:
            None.
        !! could be promoted
        """
        id      = self.id_field.text()

        debug_msg   = ( f"Album text tab fetch_detail_row { id= }")
        logging.log( LOG_LEVEL,  debug_msg, )

        self.fetch_detail_row_by_id( id )

    # -----------------------------
    def fetch_text_row_by_id( self, id   ):
        """
        what it says, read
        or is is not a fetch, a copy over, not what I want
        !! need to fix -- updates may no         t work
        also need to check for more id errors, perhaps
        Args:
            id (TYPE): DESCRIPTION.

        """
        model     = self.detail_text_model
        model.setFilter( (f"id = {id}") )
        model.select()
        if model.rowCount() > 0:
            record = model.record(0)
            self.text_data_field.setText(  record.value(    "text_data"     ))
            # self.name_field.setText(   record.value(    "name"      ))
            # self.url_field.setText(    record.value(     "url"       ))

        else:

            msg     = f"Fetch Error: No record tor text_data found with the given ID. {id = }"
            QMessageBox.warning(self, "Error", msg )
            AppGlobal.logger.error( msg )

        # else:
        #     QMessageBox.warning(self, "Input Error", f"Please enter a valid ID. { id = }")

    # -----------------------------
    def delete_detail_row(self):
        """
        looks like could be promoted -- dbkey needs to stay id
              but need to delete detail_children as well
              but need to delete key words as well
        what it says read
         delete_detail_row delete_detail_row
        Returns:
            None.

        """
        model       = self.detail_text_model
        id          = self.id_field.text()
        if id:
            model.setFilter( f"id = {id}" )
            model.select()
            if model.rowCount() > 0:
                model.removeRow(0)
                model.submitAll()
                QMessageBox.information(
                    self, "Delete Success", "detail_text_model Record deleted successfully.")
                self.clear_detail_fields()
            else:
                msg   = "Delete Error: No record found with the given ID. { id = } "
                QMessageBox.warning(self, "Error", msg )
                AppGlobal.logger.error( msg )
        else:
            msg  = f"Please enter a valid ID. { id = }"
            QMessageBox.warning(self, "Input Error",
                                "Please enter a valid ID.")
            AppGlobal.logger.error( msg )

    # ------------------------
    def clear_detail_fields(self):
        """
        what it says, read
        what fields, need a bunch of rename here
        clear_detail_fields  clear_detail_fields
        """
        self.id_field.clear()

        self.text_data_field.clear()
        # self.name_field.clear()
        # self.url_field.clear()

    # -------------------------
    def update_new_record(self):
        """
        Returns:
            None.

        """
        print( f"update_new_record  {self.record_state=}")

        if not self.record_state  == base_document_tabs.RECORD_NEW:
            debug_msg  = ( f"update_new_record bad state, return  {self.record_state=}")
            logging.error( debug_msg )
            return

        model      = self.detail_text_model
        new_id     = self.idField.text()
        new_text   = self.textField.toPlainText()
        if new_id and new_text:
            record = model.record()
            record.setValue("id", int(new_id))
            record.setValue("text_data", new_text)
            model.insertRecord(self.model.rowCount(), record)
            model.submitAll()
            self.record_state    = base_document_tabs.RECORD_FETCHED
            QMessageBox.information(self, "Save New", "New record saved!")
        else:
            debug_msg   = ( f"do not seem to have new id and text {new_id=} { new_text=}")
            logging.error( debug_msg )

    # ----------------------
    def update_record_fetched(self):
        debug_msg  = ( f"update_record_fetched  {self.record_state=}")
        logging.error( debug_msg )

        if not self.record_state  == base_document_tabs.RECORD_FETCHED:
            debug_msg    = ( f"update_record_fetched bad state, return  {self.record_state=}")
            logging.error( debug_msg )
            return

        model      = self.detail_text_model
        id_value = self.idField.text()
        if id_value:
            model.setFilter(f"id = {id_value}")
            model.select()
            if self.model.rowCount() > 0:
                record = model.record(0)
                record.setValue("id", int(id_value))
                record.setValue("text_data", self.textField.toPlainText())
                model.setRecord(0, record)
                model.submitAll()
                # QMessageBox.information(
                #     self, "Save", "Record ( fetched ) saved!")
            model.setFilter("")

    def update_text( self, ):
        """

        """
        debug_msg  = ( "update text in album used? promoted??")
        logging.log( LOG_LEVEL,  debug_msg, )

        if self.record_state   == base_document_tabs.RECORD_NULL:
            print( "update_db record null no action, return ")

        elif self.record_state   == base_document_tabs.RECORD_NEW:
            self.update_new_record()

        elif self.record_state   == base_document_tabs.RECORD_FETCHED:
            self.update_record_fetched()

        elif self.record_state   == base_document_tabs.RECORD_DELETE:
            self.delete_record_update()

        else:
            print( f"update_db wtf  {self.record_state=} ")

        print( f"update_db record state now:  {self.record_state=} ")

    # ---------------------
    def delete_record_update(self):
        """


        Returns:
            None.

        """
        if not self.record_state  == self.RECORD.DELETE:
            print( f"delete_record_update bad state, return  {self.record_state=}")
            return

        model       = self.detail_text_model
        id_value    = self.deleted_id
        if id_value:
            model.setFilter(f"id = {id_value}")
            model.select()
            if model.rowCount() > 0:
                model.removeRow(0)
                model.submitAll()
                self.clear_fields()  # will fix record state
                self.record_state       = base_document_tabs.RECORD_NULL
                QMessageBox.information(
                    self, "delete_record_update", "Record deleted!")
            model.setFilter( "" )
# ----------------------------------------
class AlbumHistoryTab(  base_document_tabs.HistoryTabBase  ):
    """
    """
    # ---------------------------
    def __init__(self, parent_window ):
        """
        what it says read -- the usual -- but ancestor matters

        """
        super().__init__( parent_window )
        self.tab_name            = "AlbumHistorylTab"

# ----------------------------------------
class AlbumPictureSubTab( base_document_tabs.SubTabBaseOld  ):
    #class AlbumDetailListTab( base_document_tabs.SubTabBase  ):
    """
    This is the list of photos in the album
    see photo_in_show_join_chat.py

    should this be pictuer list like other tabs, I think different from
    subjects


    """
    # ------------------------------------------
    def __init__(self, parent_window ):
        """
        so i can have 2 lists, one of adds, one of deletes each can
        be a dict of info.
        manually put the data in the relational view and
        on submit generate queries for each

        the dict would be different for adds and deletes
        deletes only needs the Album_photo.id
        the add needs to display so needs some photo information:
        the dict would have the photo.id name and file_name for each photo and

        """
        super().__init__( parent_window )

        self.sub_window      = parent_window.parent_window   # two levels up but name is bad

        self.picture_tab     = self.sub_window.picture_tab
        self.list_ix         = -1  # should track selected an item in detail
        self.list_table_name = "photo_in_show"
        self.table_name      = self.list_table_name # -- clean up

        # xxxx  AppGlobal.add_photo_target   = self
        self.db             = AppGlobal.qsql_db_access.db

        self._build_model()
        self._build_gui()

        # sort of guessing  work on these
        # columns to find the respecitve data
        self.ix_photo_fn              = 6  # 5
        self.ix_photo_name            = 9
        self.ix_sub_dir               = 8
        self.ix_seq_no                = 3
        self.ix_photoshow_id          = 10   # album_id
        self.ix_photo_id              = 7

# Column 0: id
# Column 1: photo_id_old
# Column 2: photo_show_id_old
# Column 3: sequence
# Column 4: photo_in_show_id_old
# Column 5: camera
# Column 6: file
# Column 7: photo_id
# Column 8: sub_dir
# Column 9: name
# Column 10: photo_show_id
# Column 11: photo_in_show_id


    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says, read

        """
        page                = self

        main_layout         = QVBoxLayout( self )
        photo_layout        = QHBoxLayout( self )

        main_layout.addLayout( photo_layout )

        # # ---- "Copy File Name" comes out at bottom
        # label           = "Copy File Name?????"
        # widget          = QPushButton( label )
        # # connect_to  =  functools.partial( self.run_python_idle, text_entry_widget )
        # # widget.clicked.connect( connect_to )
        # #widget.clicked.connect( self.text_edit_ext_obj.strip_lines_in_selection  )
        # main_layout.addWidget( widget, )


        model       = self.model
        view        = self.view

        view.setEditTriggers(QTableView.NoEditTriggers) # no editiong

        debug_col = True
        if debug_col:
            self.col_head_no()
        self.col_head_names()


        # ---- view   -- built with model here layout only
        # self.view           = QTableView()
        # self.view.setSelectionBehavior(QTableView.SelectRows)
        photo_layout.addWidget( self.view )

        self.view.clicked.connect( self._on_list_click  )
        # photo_layout.addWidget( self.view_read )
        self.create_context_menu()

        # ---- picture viewer
        a_photo_viewer      = picture_viewer.PictureViewer( self )
        self.photo_viewer   = a_photo_viewer
        photo_layout.addWidget( a_photo_viewer )

        # ----
        button_layout       = QHBoxLayout( self )
        main_layout.addLayout( button_layout )

        widget          = QPushButton('Next>')
        connect_to      = functools.partial( self.prior_next, 1 )
        widget.clicked.connect( connect_to )
        button_layout.addWidget( widget )

        #
        widget          = QPushButton( '<Prior')
        connect_to      = functools.partial( self.prior_next, -1 )
        widget.clicked.connect( connect_to )
        button_layout.addWidget( widget )

        #
        widget        = QPushButton( 'Delete')
        widget.clicked.connect( self.delete_selected )
        button_layout.addWidget( widget )

        #
        widget        = QPushButton( 'Copy FN')
        widget.clicked.connect( self.copy_file_name )
        button_layout.addWidget( widget )

        #
        widget        = QPushButton( 'Shell')
        # connect_to     = functools.partial( self.prior_next, -1 )
        widget.clicked.connect( self.shell_file_name )
        button_layout.addWidget( widget )

        # ---- edit
        widget        = QPushButton( 'Edit')
        widget.clicked.connect( self.edit_file_name )
        button_layout.addWidget( widget )

        #
        widget        = QPushButton( 'Jump to Pic')
        widget.clicked.connect( self.open_picture_document )
        button_layout.addWidget( widget )

        #
        widget        = QPushButton( 'Copy to Album')
        widget.clicked.connect( self.copy_to_album )
        button_layout.addWidget( widget )

        # # Create buttons for CRUD operations
        # widget        = QPushButton('AddDlg')
        # # add_button    = widget
        # # widget.clicked.connect(self.add_record)
        # button_layout.addWidget( widget )

        # #
        # widget        = QPushButton('EditDlg')
        # # add_button    = widget
        # # widget.clicked.connect(self.edit_record)
        # button_layout.addWidget( widget )

        # #
        # widget        = QPushButton('Delete')
        # # add_button    = widget
        # # widget.clicked.connect(self.delete_record)
        # button_layout.addWidget( widget )

        # #
        # widget        = QPushButton( 'save_select_model_test')
        # widget.clicked.connect(self.save_select_model_test)
        # button_layout.addWidget( widget )

        #
        widget        = QPushButton( 'add_photo_test')
        widget.clicked.connect(self.add_photo_test)
        button_layout.addWidget( widget )

        #
        widget        = QPushButton( 'reselect')
        widget.clicked.connect(self.reselect)
        button_layout.addWidget( widget )

        #
        widget        = QPushButton( 'get_max_seq')
        widget.clicked.connect(self.get_max_seq)
        button_layout.addWidget( widget )

        #
        widget        = QPushButton( 'inspect')
        widget.clicked.connect( self.inspect )
        button_layout.addWidget( widget )

    # ------------------------------------------
    def _build_model( self, ):
        """
        what it says, read
        does both the model the view

        revised based on qt_by_example

        if you change the model then  self.ix_sub_dir  needs to be changed ... perhaps others

        """
        # Create the model and set up the relation for file and sub_dir
        self.model = QSqlRelationalTableModel(self)
        # self.model          = qt_with_logging.QSqlRelationalTableModelWithLogging(
        #     self )
        self.model.setTable( "photo_in_show" )
            # primry table id sequence  photo_id  photo_show_id  photo_in_show_id

        # Setting the relation to include `file` and `sub_dir.....`
        # if you change this there are a bunch of other changes to make
        self.model.setRelation(
            self.model.fieldIndex( "photo_id" ),       # column in primary table used for join
            QSqlRelation( "photo", "id", "camera, dt_item, file, photo_id, sub_dir, name" )
        )

        # coordinate with above
        self.id_col_ix          = 0
        self.seq_col_ix         = 3
        self.dt_item_col_ix     = 6
        self.file_col_ix        = 7

        self.sub_dir_col_ix     = 9
        self.name_col_ix        = 10



        #self.dt_item_col_ix   = 1



        # Set filter for the specific `photo_show_id`
        # self.model.setFilter( f"photo_show_id = {10028}" )

        # Configure headers and load data
        # self.model.setEditStrategy(QSqlRelationalTableModel.OnFieldChange)
        self.model.setEditStrategy( QSqlRelationalTableModel.OnManualSubmit )
        self.model.select()

        # ---- view -- see up in gui ??
        view            = QTableView()
        self.view       = view
        view.setModel( self.model )

        view.setEditTriggers(QTableView.DoubleClicked | QTableView.SelectedClicked)

    # --------------------
    def col_head_names(self):
        """


        """
        # start using these  self.dt_item_col_ix   = 1
        model    = self.model
        view     = self.view

        model.setHeaderData(  self.id_col_ix, Qt.Horizontal, "ID" )
        view.setColumnWidth(  self.id_col_ix, 50)  # Set ix_col  width in pixels
        view.setColumnHidden( self.id_col_ix, True )

        # ix_col      = 1
        # view.setColumnHidden( ix_col, True )  # might or might not change
        #     # cloumn numbers -- beware in all of order of operations

        # ix_col      = 2
        # view.setColumnHidden( ix_col, True )


        model.setHeaderData(  self.seq_col_ix, Qt.Horizontal, "Seq" )
        view.setColumnWidth(  self.seq_col_ix, 50)

        print( f"{self.dt_item_col_ix = }")
        delegate = base_document_tabs.DateFormatDelegate( view )
        view.setItemDelegateForColumn( self.dt_item_col_ix, delegate)
        model.setHeaderData(  self.dt_item_col_ix, Qt.Horizontal, "Dt Item" )
        view.setColumnWidth(  self.dt_item_col_ix, 100)

        # # view.setColumnHidden( ix_col, True )
        # ix_col      += 1
        # view.setColumnHidden( ix_col, True )

        # ix_col      += 1
        # model.setHeaderData(  ix_col, Qt.Horizontal, "Camera" )
        # view.setColumnWidth(  ix_col, 80)

        # ix_col      += 1
        # model.setHeaderData(  ix_col, Qt.Horizontal, "File" )
        # view.setColumnWidth(  ix_col, 180)

        # ix_col      += 1    #  7 perhaps
        # model.setHeaderData(  ix_col, Qt.Horizontal, "Photo ID" )
        # view.setColumnWidth(  ix_col, 80)

        # ix_col      += 1
        # model.setHeaderData(  ix_col, Qt.Horizontal, "SubDir" )
        # view.setColumnWidth(  ix_col, 80)

        # ix_col      += 1
        model.setHeaderData(  self.name_col_ix  , Qt.Horizontal, "Name" )
        view.setColumnWidth(  self.name_col_ix  , 120)

    # --------------------
    def col_head_no(self):
        """
        what it says -- for debug only
        6 is date
        7 is file
        0 is id
        3 is sequence
        9 is subdir
        """
        model    = self.model
        view     = self.view
        for ix_col in range( 7 ):
            model.setHeaderData(  ix_col, Qt.Horizontal, str( ix_col ) )
            view.setColumnWidth(  ix_col, 80)  # Set column 0 width to  pixels


    # --------------------
    def create_context_menu(self):
        """
        what it says
        """
        self.contextMenu = QMenu(self)

        addAction        = QAction("Add Row", self)
        #addAction.triggered.connect(self.addRow)
        self.contextMenu.addAction(addAction)

        deleteAction = QAction("Delete Row", self)
        #deleteAction.triggered.connect(self.deleteRow)
        self.contextMenu.addAction(deleteAction)

        self.view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.view.customContextMenuRequested.connect( self.show_context_menu )

    # --------------------
    def show_context_menu( self, pos ):
        """
        what it says
        !! change my name

        Args:
            pos (TYPE): DESCRIPTION.

        """
        self.contextMenu.exec_( self.view_read.mapToGlobal(pos) )

    # ------------------------------------------
    def _on_list_click( self, index,   ):
        """
        what it says, read
        now just a table  !! promote me??
        """
        debug_msg   = ( f">> _on_list_click {index = }"   )  # the row?
        logging.debug( debug_msg )

        row                     = index.row()
        # column                  = index.column()
        debug_msg = ( f"PhotoshowDetailListTab_on_list_click {row = }  ")
        logging.debug( debug_msg )

        self.list_ix            = row
        self.prior_next( 0 )

    # ------------------------------------------
    def select_by_id ( self, a_id ):
        """
        black box
        what it says, read
        id is the id of the photo show
        self.edit_model.setFilter( "id = 33 " )

        #model.setFilter(f'photoshow.id = {photoshow_id}')

        # Set the sort order
        column_to_sort_by   = 0  # Index of the column to sort by (e.g., 0 for the first column)
        sort_order          = Qt.AscendingOrder  # or Qt.DescendingOrder
        self.edit_model.setSort(column_to_sort_by, sort_order)

        msg       = f"{self.edit_model.selectStatement()}"

        """
        self.album_id       = a_id    # change to album_id in all of this tab
        model               = self.model
        debug_msg = ( f"select_by_id  {id = }")
        logging.debug( debug_msg )

        # ---- write
        model.setFilter( f"photo_show_id = {a_id} " )
        # self.table_model_write.select()
        # self.view_write.setModel( self.table_model_write )
        self.prior_next( 0, absolute = True  )

    # ------------------------------------------
    def prior_next( self, delta, absolute = False  ):
        """
        get and put in control the prior or next photo
        using delta to determine which

        what it says, read
        direction  + forward, -backward 0 at start
        -- perhaps let it use any number so as to jump around

        watch for off by one, assume zero indexing
        if delta = 0 go to zero if it exists --- no
        could add second argument is_absolute or not_delta
        """
        view                    = self.view
        model                   = self.model
        #prior_list_ix    = self.list_ix  # ng
        no_rows                 = model.rowCount()
        list_ix                 = self.list_ix

        if absolute:
            new_list_ix           = delta
        else:
            new_list_ix           = list_ix + delta

        if no_rows <= 0:
            file_name    =  base_document_tabs.fix_pic_filename( None )
            debug_msg    = f"prior_next {no_rows = } {delta = } should clear display"
            logging.debug( debug_msg )

            self._display_photo_by_fn( file_name )
            # bad !!
            self.parent_window.parent_window.picture_tab.display_file( file_name )  # the other tab in sub window
            return None

        if new_list_ix >= no_rows:
            new_list_ix  =  no_rows -1
            debug_msg     = f"prior_next {no_rows = } {delta = } tried to index past end"
            logging.debug( debug_msg )

        elif new_list_ix < 0:
            new_list_ix  =  0
            debug_msg     = f"prior_next {no_rows = } {delta = } tired to index before start"
            logging.debug( debug_msg )

        # else in range

        self.list_ix        = new_list_ix
        # fn_index               = self.query_model_read.index( new_list_ix, 1 )
        # file_name              = self.query_model_read.data( fn_index, Qt.DisplayRole )

        #fn_item               =  model.item( self.list_ix,  ix_fn )  # may need to be model or ....
        fn_item             =  model.data( model.index( self.list_ix, self.ix_photo_fn  ) )

        #file_name  = fn_item.text() if fn_item is not None else ""
        file_name           = fn_item
        debug_msg = ( f"prior_next { file_name  = }")
        logging.debug( debug_msg )

        fn_item             =  model.data( model.index( self.list_ix, self.ix_sub_dir ) )
        sub_dir             = fn_item
        debug_msg = ( f"prior_next {sub_dir  = }")
        logging.debug( debug_msg )

        # for degug
        data                =  model.data( model.index( self.list_ix, self.ix_photo_name ) )
        debug_msg = ( f"for self.ix_photo_name {data} = " )
        logging.debug( debug_msg )

        index               = self.model.index( self.list_ix, 0)

        selection_model     = self.view.selectionModel()
        selection_model.clearSelection()
        # Select the entire row
        selection_model.select( index, selection_model.Select | selection_model.Rows )
        self.view.scrollTo( index )

        # # debug explore model
        # for ix_col in range( 15 ): # 10 works
        #     data               =  model.data( model.index( self.list_ix, ix_col ) ) # row col
        #     print( f"album picture sub tab prior_next: {ix_col = } / { data  = }")  file_name, sub_dir

        file_name   = base_document_tabs.build_pic_filename( file_name = file_name, sub_dir = sub_dir )
        file_name   = base_document_tabs.fix_pic_filename( file_name )

        #rint( f"change to prior next 0 {file_name = }" )
        self._display_photo_by_fn( file_name )

        # bad !!
        self.parent_window.parent_window.picture_tab.display_file( file_name )  # the other tab in sub window
        #rint( "above bad because hard to find self.picture_tab.display_file( file_name )"  )

        return file_name

    # ------------------------------------------
    def add_photo_test(self):
        """
        this is old ready to delete, only photo id now matters

        what it says,
        add a record just into seq fields regardless of style
        from russ qrm
        """
        #self.model.submitAll()
        # we will use key gen to get a photo id
        #photo_id                      = AppGlobal.key_gen.get_next_key( self.table_name)
        #this_photo_id                      =  # see parms
        # seq_no                        = AppGlobal.key_gen.get_next_key( self.table_name )
        #seq_no                        =         self.get_max_seq()
        data_dict                     = {}
        # data_dict["photoshow_id"]     = photoshow_id
        photo_id                        = 8579
        data_dict["photo_id"]           = photo_id

        data_dict["photo_file"]           = "withdaddy.jpg"
        data_dict["photo_sub_dir"]            = "04//"

        data_dict["photo_name"]         = "this is the test"

        #self.data_to_model_photo( data_dict )

        self.add_row( data_dict )

        # print( "!! add_model_test  submitAll


    # ------------------------------------------
    def reselect(self):
        """
        what it says,
        """
        model           = self.model

        # ---- inspect
        self_view       = self.view
        self_model      = model

        wat_inspector.go(
              msg            = "save_select_model_test:",
              a_locals       = locals(),
              a_globals      = globals(), )

        self.select_by_id ( self.album_id )

    # ------------------------------------------
    def get_max_seq(self):
        """
        what it says, read
        from a chat question
        for adding records seems to be ok oct 31
        """
        max_seq     = 0
        model       = self.model
        if model is None:
            return

        row_count       = model.rowCount()
        column_count    = model.columnCount()

        for row in range( row_count ):
            index     = model.index( row,   self.ix_seq_no    ) # row column
            data      = model.data( index )
            try:
                seq       = int( data )

            except Exception as an_except:
                debug_msg     = f"get_max_seq a_except for int()        >>{an_except}<<  type  >>{type( an_except)}<<"
                logging.debug( debug_msg )

                seq     = 0

            if seq > max_seq:
                max_seq  = seq

        debug_msg = ( f"{max_seq = }")
        logging.debug( debug_msg )

        return max_seq

    # ------------------------------------------
    def add_row(self, data_in_dict ):
        """
        !! add flag for reselect or not for optimization
        need to modify all callers


        give up on relational table doing job alone
        use an QSqlQuery and do immediate update
        come back and look at later perhaps

        or use this?
            db = AppGlobal.qsql_db_access.db

        !! does not handle errors
        """
        model           = self.model
        db              = model.database()
        if not db.transaction():
            msg  = ("Failed to start transaction: {db.lastError().text()} "  )
            logging.error( msg )

        table_name      = self.table_name   #  photo_in_show

        key             = AppGlobal.key_gen.get_next_key( self.table_name )

        sequence        = self.get_max_seq( ) + 1

        # ---- so now all the data in lined uup
        query           = QSqlQuery( db )

        sql     = """INSERT INTO photo_in_show (
            id,
            sequence,
            photo_id,
            photo_show_id )

            VALUES (?, ?, ?, ? )
        """

        query.prepare( sql )

        if not query.prepare(sql):
            msg = (f"Prepare failed: {query.lastError().text()}")
            logging.error( msg )

        query.addBindValue( key )
        query.addBindValue( sequence )
        query.addBindValue( data_in_dict["photo_id"]  )
        query.addBindValue( self.album_id  )

        if not query.exec_():
            msg = (f"Execution failed: {query.lastError().text()}")
            logging.error( msg )
        else:
            pass
            #print("Insert successful.")

        #rint( "do a select here 888 8")
        self.select_by_id ( self.album_id )
        return

        # print( "inspect  -----------------------------------------")
        # self_view       = self.view
        # wat_inspector.go(
        #       msg            = "add_row(self, data_dict ) end no update or select",
        #       a_locals       = locals(),
        #       a_globals      = globals(), )

        #rint( "after try inspect again  -----------------------------------------")

        # Set up a view to display the data  --- do we need this ?? try without
        # view = QTableView()
        # self.view.setModel(model)

        # self.view.show()

    # ------------------------------------------
    def add_row_still_not_working_chat_says(self, data_in_dict ):
        """deleted see backup for what i tried  """

    # ------------------------------------------
    def add_row_model(self, data_dict ):
    # # ------------------------------------------
    # def data_to_model_photo(self, data_dict ):
        """
        what it says - read   change name just to data-to_model
        from russ qrm
        this will do an update or an insert
        what needs to be in data dict, see below
            this figures out
            the key
            the seq_no
            the album_id
        it needs the data_dict


        # looks like we need to add to the record not the model !! see relational model 2
        # maybe add to both or add the record to the model, go back to relational model 2


        """
        model           = self.model

        debug_msg = ( ".................... using data_to_model_photo hard coded indexes ??")
        logging.debug( debug_msg )
        table_name      = self.table_name   #  photo_in_show

        key             = AppGlobal.key_gen.get_next_key( self.table_name )

        sequence        = self.get_max_seq( )

        # # ---- inspect
        # self_view       = self.view
        # self_model      = model

        # wat_inspector.go(
        #       msg            = "add_row(self, data_dict ):",
        #       a_locals       = locals(),
        #       a_globals      = globals(), )

        debug_msg = ( "this is code after first inspect -----------------------------------------")
        logging.debug( debug_msg )
        # row count here becomes rowcount - 1 later
        model.insertRow( model.rowCount() )
        ix_row               = model.rowCount() - 1   # model row that get the data here new row
        # model.index makes an index row col for the data
        model.setData( model.index( ix_row, 0 ), key ) # 0 alway column for key

        # data_dict["photo_id"]         = photo_id

        # *key, *album_id, *seq_no *photo_id   photo_fn  sub_dir  photo_name
        # ---- photoshow_id
        # data       = data_dict["photoshow_id"]
        data        = self.album_id
        ix_col      = self.ix_photoshow_id
        # we can get the index by name see es_qtsql.....
        debug_msg = ( f"data_to_model_photo photoshow_id { data } {ix_col = }" )
        logging.debug( debug_msg )
        model.setData( model.index(  ix_row, ix_col  ), data )

        # ---- seq_no --- should gen here
        data        = self.get_max_seq() + 1
        ix_col      = self.ix_seq_no
        debug_msg = ( f"data_to_model_photo seq_no { data } {ix_col = }" )
        logging.debug( debug_msg )

        model.setData( model.index(  ix_row, ix_col  ), data )

        # ---- photo_id
        data        =  data_dict["photo_id"]
        ix_col      = self.ix_photo_id
        debug_msg = ( f"data_to_model_photo_photo photo_id { data } {ix_col = }" )
        logging.debug( debug_msg )
        model.setData( model.index(  ix_row, ix_col  ), data )

        # ---- photo_fn
        data        =  data_dict[ "photo_fn" ]
        ix_col      = self.ix_photo_fn
        debug_msg = ( f"data_to_model_photo_photo_fn { data  } {ix_col = }" )
        logging.debug( debug_msg )
        model.setData( model.index(  ix_row, ix_col  ), data )

        # ---- sub_dir
        data        =  data_dict[ "sub_dir" ]
        ix_col      = self.ix_sub_dir
        debug_msg = ( f"data_to_model__photo sub_dir { data } {ix_col = }" )
        model.setData( model.index(  ix_row, ix_col  ), data )

        # ---- photo_name
        data        =  data_dict[ "photo_name" ]
        ix_col      = self.ix_photo_name
        debug_msg = ( f"data_to_model_photo photo_name { data } {ix_col = }" )
        logging.debug( debug_msg )
        model.setData( model.index(  ix_row, ix_col  ), data )

        # print( "try inspect again  -----------------------------------------")
        # wat_inspector.go(
        #      msg            = "add_row(self, data_dict ) end no update or select",
        #      a_locals       = locals(),
        #      a_globals      = globals(), )

        # print( "after try inspect again  -----------------------------------------")

    # ------------------------------------------
    def _display_photo_by_fn( self, file_name  ):
        """
        what it says
        do we need this?
        """
        self.photo_viewer.display_file( file_name )

    # ------------------------------------------
    def add_photo_to_show( self, photo_dict  ):
        """
        what it says
            this is sent from some photo usually
            this may be dead already
            revisition end of nov 2024
        """
        debug_msg = ( f"add_photo_to_show_delete_later way down in photoshowdetaillist tab {photo_dict = }")
        logging.debug( debug_msg )

        self.add_row( photo_dict )

        # self.data_to_model_photo( photo_dict )
        # print( "!! add_photo_to_show  submitAll  ")
        # self.model.submitAll()

    # ------------------------------------------
    def delete_selected( self,    ):
        """
        testing selection no delete
        right now only 1 can be selected, may change
        transaction seems incomplete
        """

        if not base_document_tabs.is_delete_ok():
            return

        debug_msg = ( f"delete_selected {1 = }")
        logging.debug( debug_msg )

        view            = self.view
        # Assuming `view` is your QTableView
        selection_model = view.selectionModel()
        if selection_model:
            selected_indexes = selection_model.selectedRows()

            for index in selected_indexes:
                row     = index.row()  # Get the row number
                msg     = ( f"Selected row: {row = }" )
                logging.debug(  msg )


        model           = self.model
        column_name = "id"

        # Get the column index for the column name
        column = model.fieldIndex( column_name )

        if column == -1:
            msg = ( f"Column '{column_name}' not found in the model." )
            logging.debug(  msg )
        else:
            # Retrieve the QModelIndex for the specified cell
            index = model.index( row, column)

            # Get the data from the model at the specified index
            a_id    = model.data(index)
            msg     = ( f"Value at   {row = },   '{column_name = }': {a_id = }" )
            logging.debug(  msg )


        # return   #======================================= for now

        # ---- the delete  may not be done
        model           = self.model
        db              = model.database()
        # if not db.transaction():
        #     msg  = ("Failed to start transaction: {db.lastError().text()} "  )
        #     logging.error( msg )

        table_name      = self.table_name
        query           = QSqlQuery( db )

        sql             = f"""DELETE FROM {table_name} WHERE id = ? """

        query.prepare( sql )

        if not query.prepare(sql):
            msg = (f"Prepare failed: {query.lastError().text()}")
            logging.error( msg )

        query.addBindValue( a_id )

        if not query.exec_():
            msg = (f"Execution failed: {query.lastError().text()}")
            logging.error( msg )
        else:
            pass
            #print("Insert successful.")

        self.select_by_id ( self.album_id )
        return

    # ------------------------------------------
    def get_selected_row( self, ):
        """
        what it says

        not right for multiple selections or none !

        """
        view            = self.view

        selection_model = view.selectionModel()
        if selection_model:
            selected_indexes = selection_model.selectedRows()

            for index in selected_indexes:
                row     = index.row()  # Get the row number
                msg     = ( f"Selected row: {row = }" )
                logging.debug(  msg )
        else:
            1/0

        return row

    # ------------------------------------------
    def get_file_name( self,    ):
        """
        get the file name
        """
        row          = self.get_selected_row()

        file_name    = self.get_data_for_column( row, "file"  )
        sub_dir      = self.get_data_for_column( row, "sub_dir" )

        file_name   = base_document_tabs.build_pic_filename( file_name = file_name, sub_dir = sub_dir )
        return file_name

    # ------------------------------------------
    def copy_file_name( self,    ):
        """
        get the file name into the clipboard
        """
        file_name   = self.get_file_name()
        QApplication.clipboard().setText( file_name )

    # ------------------------------------------
    def shell_file_name( self,    ):
        """
        get the file name into the clipboard
        """
        file_name   = self.get_file_name()
        subprocess.call(('xdg-open', file_name ) )  # linux only for now
        #subprocess.Popen([ "bash", file_name ])

    # ------------------------------------------
    def edit_file_name( self,    ):
        """
        get the file name into the clipboard
        """
        file_name   = self.get_file_name()

        editor      = AppGlobal.parameters.picture_editor

        subprocess.Popen([ editor, file_name ])
        QApplication.clipboard().setText( file_name )

    # ------------------------------------------
    def open_picture_document( self,    ):
        """
        what it says
            if none open, if multiple open
            what about save
        """

        picture_docs    = AppGlobal.mdi_management.get_picture_docs()
        if  len( picture_docs ) == 0:
            1/0

        picture_doc     = picture_docs[ 0 ]
        row             = self.get_selected_row()
        a_id            = self.get_data_for_column( row, "photo_id"  )
        picture_doc.select_record( a_id  )

        AppGlobal.mdi_management.show_document( picture_doc )

    # --------------------------------------
    def copy_pic_setup( self,  ):
        """
        check that the setup is ok

        have a single album to add the pictures to

        return -- album document....
        raise  some exception if error
        """
        detail_tab      = self.parent_window
        document        = detail_tab.parent_window

        album_docs      = AppGlobal.mdi_management.get_album_docs()
        len_album_docs  = len( album_docs )

        if len_album_docs !=  2:
            msg     = f"For this to work you need 2 Album Document open, you have {len_album_docs}."
            raise app_exceptions.ReturnToGui( msg )

        album_target = None
        for i_album_doc in album_docs:
            if i_album_doc.instance_ix != document.instance_ix:
                album_target = i_album_doc
                break

        if album_target is None:
                msg     = f"Problem: I cannot find a target album, this should not happen ."
                raise app_exceptions.ReturnToGui( msg )

        record_state    = album_target.detail_tab.data_manager.record_state

        if record_state == data_manager.RECORD_NULL:   # not 0 look it up
            msg     = "For this to work you need an item in your target Album Document."
            raise app_exceptions.ReturnToGui( msg )

        #rint( f"!!!!!!Error still need to check it has a record {record_state}")
        # ---- are files present
        # if self.model.rowCount() < 1:
        #     msg       = ( "For this to work you need to have some files in this tab.")
        #     logging.debug( msg )
        #     raise app_exceptions.ReturnToGui( msg )

        return album_target

    # --------------------------------------
    def copy_to_album( self,  ):
        """
        copy pictures to another album
        for now all at end of items in the other album
        """
        try:
            album_target = self.copy_pic_setup()

        except app_exceptions.ReturnToGui as an_except:
            msg       = f"{str( an_except)}"
            logging.debug( msg )
            QMessageBox.information( AppGlobal.main_window,
                                     "That is a No Go", msg )
            return

        model       = self.model   # QSqlRelationalTableModel(self)
        #ix_debug    = 0
        # start with all later with some selections

        for ix_row in range( model.rowCount() ):
            self.add_to_album( album_target, ix_row )


        # msg         = ( "\n maybe finished return ++++++++++++++++++++++++++++++++++++++++++++")
        # logging.debug( msg )

    # -----------------------------
    def add_to_album( self, album_target, ix_row ):
    #def add_to_show( self, ): in picture detail, now movdify above
        """
        will add one to the show need to call over and over
        took from picture detail  was add_to_show
        # change name to add to album when ewe get farther along
        add a picture to a show -- which must be open in another window
        query.addBindValue( data_in_dict["photo_id"]  )
        """

        model         = self.model
        # dict is a bit odd  --- some is wrong all we really need i photo_id
        #photo_id      =  int( self.id_field.text() )  # may be available elsewhere   this worul db test
        photo_id_ix   = 7
        photo_id      =  model.data( model.index( ix_row, photo_id_ix))
        #photo_fn      =  self.file_field.text()
        # may want to double check but seems now only photo id matters set rest to None, drop weh it works
        row_dict            = { "photo_name":               "from album_picture_sub_tab",
                                "photo_fn":                  None,
                                "photo_id":                  photo_id,
                                "photoshow_photo_id":        None,
                               }

        #photo_target     = AppGlobal.mdi_management.get_album_doc()
        #photo_target   = AppGlobal.add_photo_target

        print( "add commented out for now -- check stuff above with debug {photo_id} = " )
        album_target.add_photo_to_show( row_dict )
                # perhaps in album picture sub tab

    # ------------------------------------------
    def get_data_for_column( self, row, column_name  ):
        """
        may want to make more reusuable and promote
        """
        model           = self.model

        column = model.fieldIndex( column_name )

        if column == -1:
            msg = ( f"get_data_for_column Column '{column_name}' not found in the model." )
            logging.error(  msg )
        else:
            # Retrieve the QModelIndex for the specified cell
            index   = model.index( row, column)

            # Get the data from the model at the specified index
            data    = model.data(index)
            # msg     = ( f"Value at   {row = },   '{column_name = }': {data = }" )
            # logging.debug(  msg )

        return data

    # ------------------------------------------
    def inspect( self,  ):
        """
        the usual
        """
        # make some locals for inspection
        #parent_window           = self.parent( ).parent( ).parent().parent()
        #a_db                    = parent_window.sample_db
        self_model        = self.model
        self_view         = self.view
        wat_inspector.go(
             msg            = "inspect for AlbumPictureSubTab",
             #inspect_me     = self.people_model,
             a_locals       = locals(),
             a_globals      = globals(), )


# ---- eof ------------------------------
