#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    main.main()
# --------------------

# ---- imports

#from   functools import partial
#import collections

import inspect
import logging
import os
import shutil
#import functools
#import sqlite3
#import sys
import time
from pathlib import Path

import data_dict
import gui_qt_ext
import wat_inspector
from app_global import AppGlobal
# ---- QtCore
from PyQt5.QtCore import (QAbstractTableModel,
                          QDate,
                          QModelIndex,
                          QRectF,
                          QSortFilterProxyModel,
                          Qt,
                          QTimer,
                          pyqtSlot)
from PyQt5.QtGui import (QIntValidator,
                         QPainter,
                         QPixmap,
                         QStandardItem,
                         QStandardItemModel)
# ---- QtSql
from PyQt5.QtSql import (QSqlDatabase,
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
                             QDataWidgetMapper,
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
                             QSpinBox,
                             QTableView,
                             QTableWidget,
                             QTableWidgetItem,
                             QTabWidget,
                             QTextEdit,
                             QVBoxLayout,
                             QWidget)

# ---- imports local
import base_document_tabs
import custom_widgets
import file_browse
import key_words
import parameters
# import  ia_qt
import picture_viewer
import qsql_utils
#import  string_util
import qt_sql_query
import qt_with_logging
#import  mdi_management
import table_model
import app_exceptions

# ----------------------------------------
class PictureDocument( base_document_tabs.DocumentBase ):
    """
    for the photo table....
    a single picture, its subjects, and albums
    """
    def __init__(self,  ):
        """
        the usual
        """
        super().__init__()

        self.db                 = AppGlobal.qsql_db_access.db

        self.detail_table_name  = "photo"
        self.text_table_name    = "photo_text"  # text tables always id and text_data
        self.help_filename      = "picture_doc.txt"
        self.subwindow_name     = "PictureDocument"
        self.setWindowTitle( self.subwindow_name )
        # wat_inspector.go( self, locals() )
        self._build_gui()

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says
        """
        mdi_area                = AppGlobal.main_window.mdi_area
            #we could return the sub window for parent to add
        sub_window              = self
            # sub_window.setWindowTitle( "this title may be replaced " )

        self.prior_tab          = 0
        self.current_tab        = 0

        self.prior_criteria     = None
        self.current_criteria   = None    # init just after criteria tab created

        # Main notebook with  tabs
        main_notebook           = self.tab_folder   # create in parent
        self.main_notebook      = main_notebook

        main_notebook.currentChanged.connect( self.on_tab_changed )

        # ---- tab building
        ix                        = -1

        ix                       += 1
        self.criteria_tab_index   = ix
        self.criteria_tab         = PictureCriteriaTab( self )
        main_notebook.addTab(       self.criteria_tab,  "Criteria" )

        ix                       += 1
        self.list_tab_index      = ix
        self.list_tab            = PictureListTab(   self  )
        main_notebook.addTab(             self.list_tab  ,   "List"    )
        # print( "!! fix monkey patch ")
        # #self.list_tab.parent_window     = self

        ix                       += 1
        self.detail_tab_index     = ix
        self.detail_tab           = PictureDetailTab( self )
        main_notebook.addTab( self.detail_tab,    "Detail"     )

        ix                         += 1
        self.text_tab_index      = ix
        self.text_tab               = PictureTextTab( self )
        main_notebook.addTab( self.text_tab,    "Text"     )

        ix                         += 1
        self.picture_tab_index       = ix
        self.picture_tab             = base_document_tabs.StuffdbPictureTab( self )
        main_notebook.addTab( self.picture_tab,    "Picture"     )

        ix                        += 1
        self.history_tab_index     = ix
        self.history_tab           = PictureHistorylTab( self )
        main_notebook.addTab( self.history_tab ,   "History"    )

        sub_window.setWidget( main_notebook )
        mdi_area.addSubWindow( sub_window )

        sub_window.show()

    # ---- capture events ----------------------------

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

        msg       = ( f"Clicked on row {row}, column {column}, value tbd" )
        logging.debug( msg )

    # ---- sub window interactions ---------------------------------------
    # --------------------------
    def delete_record( self,   ):
        """
        also know as update -- update detail tab and text...
        looks promotable
        """
        #self.detail_tab.db_update()
        if self.popup_delete_question():

            self.detail_tab.delete_record()
            self.text_tab.delete_record()

            msg     = "delete_record.... -- done ??"

            logging.debug( msg )
        else:
            pass # for now

    #-------------------------------------
    def copy_prior_row( self ):
        """tail_tab.default_new_row( next_key )
        default values with copy for a new row in the detail and the
               text tabs
        probably can promote, may need different func name on text so tabs can be the same?
        Returns:
            None.
            """
        next_key      = AppGlobal.key_gen.get_next_key(   self.detail_table_name )
        self.detail_tab.copy_prior_row( next_key )
        self.text_tab.copy_prior_row(  next_key )

    # ------------------------------------------
    def criteria_select( self,     ):
        """
        uses info in criteria tab to build list in list tab
        uses info from 2 tabs
        """
        self.criteria_tab.criteria_select()
        return

    # -----------------------------------
    def add_row_historyxxx( self, index ):
        """
        pretty much from chat

        def add_row_to_tab2(self, index):
        # Get the data from the selected row
        id_data = self.model.data(self.model1.index(index.row(), 0))
        name_data = self.model1.data(self.model1.index(index.row(), 2))

        # Create items for the second model
        id_item = QStandardItem(str(id_data))
        name_item = QStandardItem(name_data)

        # Add a new row to the second model
        self.history_model.appendRow([id_item, name_item])

        """
        1/0
        return

        # Get the data from the selected row
        detail_model    = self.detail_tab.tab_model
        history_model   = self.history_tab.history_model
        #ia_qt.q_sql_query_model( self.detail_tab.tab_model, "add_row_history photo_sub" )

        id_data         = detail_model.data( detail_model.index( index.row(), 0))
        name_data       = detail_model.data( detail_model.index( index.row(), 2))
        msg       = ( f"in add_row_history {id_data = }   {name_data = }")

        logging.debug( msg )

        # Create items for the second model
        id_item     = QStandardItem( str(id_data) )
        name_item   = QStandardItem( name_data )

        # Add a new row to the second model
        history_model.appendRow([id_item, name_item])

        # if not self.index:   # new row  self.index and index not the same
        #     print( ">>>>>>>>>>>>new row AppGlobal.key_gen       = a_key_gen")
        #     key             = AppGlobal.key_gen.get_next_key( table_name )
        #     # row count here becomes rowcount - 1 later
        #     model.insertRow( model.rowCount() )
        #     ix_row               = model.rowCount() - 1   # model row that get the data here new row
        #     # model.index makes an index row col for the data
        #     model.setData( model.index( ix_row, 0), key )

    # ---------------------------------------
    def display_picture( self, file_name  ):
        """
        what it says, mostly focused on the detail tab
        may be promotable
        """
        # rint( f"<<<<<< display_photo  {self.photo_tab = }")
        self.picture_tab.display_file( file_name )

    #-------------------------------------
    def i_am_hsw(self):
        """
        make sure call is to here for testing
        """
        print( f"i_am_hsw { self.subwindow_name = }")

    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = ">>>>>>>>>>* PictureDocument  *<<<<<<<<<<<<"

        return a_str

# ----------------------------------------
class PictureCriteriaTab( base_document_tabs.CriteriaTabBase, ):
    """
    criteria for list selection
    """
    def __init__(self, parent_window ):
        """
        the usual

        """
        super().__init__( parent_window )
        self.tab_name            = "PictureCriteriaTab"

    # ------------------------------------------
    def _build_tab( self,   ):
        """
        what it says, read

        """
        page            = self
        tab             = page

        placer          = gui_qt_ext.PlaceInGrid(
            central_widget  = page,
            a_max           = 0,
            by_rows         = False  )

        self._build_top_widgets(  placer )

        # ----id
        widget                = QLabel( "ID" )
        placer.new_row()
        placer.place( widget )

        #widget                  = QLineEdit()
        widget                  = custom_widgets.CQLineEditCriteria( get_type = "string", set_type = "string")
        self.key_words_widget   = widget
        widget.critera_name     = "table_id"
        self.critera_widget_list.append( widget )
        widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        placer.place( widget, )    # columnspan = 3 )

        # ----id_old
        widget                = QLabel( "ID Old" )
        placer.new_row()
        placer.place( widget )

        #widget                  = QLineEdit()
        widget                  = custom_widgets.CQLineEditCriteria( get_type = "string", set_type = "string")
        self.key_words_widget   = widget
        widget.critera_name     = "id_old"
        self.critera_widget_list.append( widget )
        widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        placer.place( widget, )    # columnspan = 3 )

        # ----key words
        widget                = QLabel( "Key Words" )
        placer.new_row()
        placer.place( widget )

        #widget                  = QLineEdit()
        widget                  = custom_widgets.CQLineEditCriteria( get_type = "string", set_type = "string")
        self.key_words_widget   = widget
        widget.critera_name     = "key_words"
        self.critera_widget_list.append( widget )
        widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        placer.place( widget, columnspan = 3 )

        # ---- name like
        placer.new_row()
        widget  = QLabel( "Name (like)" )
        placer.place( widget )

        #widget                  = QLineEdit()
        widget                  = custom_widgets.CQLineEditCriteria( get_type = "string", set_type = "string")
        self.name_widget        = widget
        widget.critera_name     = "name"
        self.critera_widget_list.append( widget )
        widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        placer.place( widget )

        # ---- with file
        placer.new_row()
        widget  = QLabel( "With file?" )
        placer.place( widget )

        # widget                      = QComboBox()
        widget                      = custom_widgets.CQComboBoxEditCriteria( get_type = "string", set_type = "string")
        self.file_name_empty_widget = widget
        widget.critera_name         = "file_name_empty"
        self.critera_widget_list.append( widget )
        widget.currentIndexChanged.connect( lambda: self.criteria_changed(  True   ) )
        widget.addItem('Any')
        widget.addItem('Yes')

        widget.addItem('No')
        placer.place( widget )

        # ---- file name like
        placer.new_row()
        widget  = QLabel( "File Name Like" )
        placer.place( widget )

        # widget                  = QLineEdit()
        widget                  = custom_widgets.CQLineEditCriteria( get_type = "string", set_type = "string")
        self.file_name_widget   = widget
        widget.critera_name     = "file_name_like"
        self.critera_widget_list.append( widget )
        widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        placer.place( widget )

        # ---- Order by
        placer.new_row()
        widget  = QLabel( "Order by" )
        placer.place( widget )

        #widget                 = QComboBox()
        widget                 = custom_widgets.CQComboBoxEditCriteria( get_type = "string", set_type = "string")
        self.order_by_widget   = widget
        widget.critera_name    = "order_by"
        self.critera_widget_list.append( widget )
        widget.addItem('dt_enter')
        widget.addItem('dt_enter')
        widget.addItem('Title??')
        placer.place( widget )

        # ---- criteria changed should be in parent
        placer.new_row()
        widget  = QLabel( "criteria_changed_widget" )
        self.criteria_changed_widget  = widget
        placer.place( widget )

        # ---- dates
        self.add_date_widgets( placer, row_lables = ( "dt_item", "dt_enter") )

        self.add_buttons( placer )

    # -------------
    def criteria_select( self,     ):
        """
        do the select
        """
        parent_document                 = self.parent_window

        model                           = parent_document.list_tab.list_model

        query                           = QSqlQuery()
        query_builder                   = qt_sql_query.QueryBuilder( query, print_it = False, )

        kw_table_name                   = "photo_key_words"

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
        id_old      = criteria_dict[ "id_old" ].strip().lower()
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
            query_builder.sql_inner_join    = " photo_key_word  ON photo.id = photo_key_word.id "
            query_builder.sql_having        = f" count(*) = {key_word_count} "

            query_builder.add_to_where( f" key_word IN {criteria_key_words}" , [] )

        # ---- name like
        name                          = criteria_dict[ "name" ].strip().lower()
        if name:
            add_where       = "lower( name )  like :name"   # :is name of bind var below
            query_builder.add_to_where( add_where, [(  ":name",
                                                     f"%{name}%" ) ])

        # ---- file name null  or empty -- note misname
        file_name_empty     = criteria_dict[ "file_name_empty" ].strip().lower()
        if file_name_empty == "yes":
            add_where       =  ' file IS NOT NULL and  file != "" '   # :is name of bind var below
            query_builder.add_to_where( add_where, [ ])

        if file_name_empty == "no":
            add_where       = ' file IS NULL or  file = "" '
            query_builder.add_to_where( add_where, [ ])

        # ---- file_name_like
        file_name_like             = criteria_dict[ "file_name_like" ].strip().lower()
        if file_name_like:
            add_where       = "lower( file )  like :file_name_like"   # :is name of bind var below
            query_builder.add_to_where( add_where, [(  ":file_name_like",
                                                     f"%{file_name_like}%" ) ])

        # ---- dates
        # # ---- dates promote  -- may not work here or anywhere
        # dt_enter and dt_item are the names  first is edit we are using the picture date

        msg       = ( "only have one date so far and names are a bit of a dyslexia mess")
        logging.info( msg )

        start_date_edit   = criteria_dict[ "start_edit_date" ]
        # rint( f"{start_date_edit}")
        if start_date_edit:
            add_where         = " dt_enter >= :start_date_edit"
            query_builder.add_to_where( add_where, [ ( ":start_date_edit", start_date_edit ) ])

        end_date_edit   = criteria_dict[ "end_edit_date" ]
        if end_date_edit:
            # rint( f"{start_date_edit}")
            add_where         = " dt_enter >= :end_date_edit"
            query_builder.add_to_where( add_where, [ ( ":end_date_edit", end_date_edit ) ])

        # ---- order by
        order_by   = criteria_dict[ "order_by" ]

        #dt_item  does not seem to exist  -- but this may be error

        if   order_by == "dt_enter":
            column_name = "dt_enter"
        elif order_by == "dt_enter":
            column_name = "dt_enter"
        else:   # !! might better handle this
            column_name = "dt_item"

        query_builder.add_to_order_by(    column_name, "ASC",   )

        query_builder.prepare_and_bind()

        msg      = f"{query_builder = }"
        logging.debug( msg )

        is_ok  = AppGlobal.qsql_db_access.query_exec_model( query,
                                                  model,
                                                  msg = "HelpSubWindow criteria_select" )

        msg       = ( f"init StuffTextTab    {query.executedQuery() = }" )
        logging.debug( msg )

        parent_document.main_notebook.setCurrentIndex( parent_document.list_tab_index )
        self.critera_is_changed = False

# ----------------------------------------
class PictureListTab( base_document_tabs.ListTabBase  ):
    """ """
    def __init__(self, parent_window ):
        """
        the usual
        """
        super().__init__( parent_window )

        self.tab_name        = "PictureListTab"
        self._build_gui()

    # ------------------------------------------
    def _build_guixxx( self,  ):
        """
        what it says, read
            for columns see criteria select in criteria table
        ?? looks pretty promotable

        """
        page            = self
        tab             = page
        #a_notebook.addTab( page, 'Channels ' )
        placer          = gui_qt_ext.PlaceInGrid(
            central_widget  = page,
            a_max           = 0,
            by_rows         = False  )

        model               = QSqlTableModel( self, self.parent_window.db ) # perhaps a global
        self.list_model     = model

        model.setTable( self.parent_window.detail_table_name )

        model.setEditStrategy( QSqlTableModel.OnManualSubmit) # = never

        view                 = QTableView()
        self.list_view       = view
        view.setSelectionBehavior( QTableView.SelectRows )
        view.setModel( model )
        placer.place(  view )
        view.clicked.connect( self.parent_window.on_list_clicked )

# ----------------------------------------
class PictureDetailTab( base_document_tabs.DetailTabBase   ):
    """
    """
    def __init__(self, parent_window  ):
        """
        Args:
            parent_window (TYPE): DESCRIPTION.
        """
        # ---- parent init
        super().__init__( parent_window )

        # ---- post parent init
        self.tab_name               = "PictureDetailTab"
        self.key_word_table_name    = "photo_key_word"
        self.post_init()

    #-------------------------------------
    def _build_gui( self ):
        """
        what it says read
        """
        page            = self
        tab             = self

        box_layout_1    =  QVBoxLayout( page )

        placer          = gui_qt_ext.PlaceInGrid(
                            central_widget  = box_layout_1,
                            a_max           = 4,
                            by_rows         = False  )

        tab_layout      = placer
        # ---- code_gen: sql_to_fields  -- begin table entries
        # ---- put picture in to right

        placer.set_col( 5,  )
        placer.set_row( 1,  )

        viewer              = picture_viewer.PictureViewer( self )
        viewer.set_fnf( parameters.PARAMETERS.pic_nf_file_name )
        self.viewer         = viewer

        placer.place( viewer, rowspan  = 5, )
        placer.set_col( 0  )
        placer.set_row( 0  )

        # ---- build_fields
        self._build_fields( placer )

        # ---- tab area
        # ---------------
        tab_folder   = QTabWidget()
        # tab_folder.setTabPosition(QTabWidget.West)
        tab_folder.setMovable(True)
        box_layout_1.addWidget( tab_folder )

        sub_tab      = PictureSubjectSubTab( self )
        self.subject_sub_tab   = sub_tab
        tab_folder.addTab( sub_tab, "Subjects" )

        sub_tab      = PictureBrowseSubTab( self )
        tab_folder.addTab( sub_tab, "Browse" )

        sub_tab             = PictureAlbumtSubTab( self )
        self.album_sub_tab  = sub_tab
        tab_folder.addTab( sub_tab, "Albums" )

        self.prior_tab          = 0
        self.current_tab        = 0

        # Main notebook with 3 tabs
        detail_notebook           = QTabWidget()
        self.detail_notebook      = detail_notebook

        #main_notebook.currentChanged.connect( self.on_tab_changed )

        # ---- buttons
        widget  = QPushButton( "Add To Album" )
        widget.clicked.connect(self.add_to_show)
        placer.place( widget)

        widget  = QPushButton( "Clip FileName" )
        widget.clicked.connect(self.clip_filename)
        placer.place( widget)

    #---------------------------------
    def _build_fields( self, layout ):
        """
        What it says, read
        self.sub_dir_field.  !! fnd file field need manual add


        gen the code then tweak -- this now out of date some is auto
             form_id          = parent_window.id_field.get_raw_data()
             form_sub_dir     = parent_window.sub_dir_field.get_raw_data()

            self.id_field            = edit_field
            self.sub_dir_field       = edit_field

        """
        # ---- code_gen: detail_tab_build_gui use for _build_gui  -- begin table entries

        # ---- id
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "id",
                                                db_type        = "integer",
                                                display_type   = "integer",
                                                 )
        self.id_field     = edit_field
        edit_field.setPlaceholderText( "id" )
        edit_field.edit_to_rec     = edit_field.edit_to_rec_str_to_int
        edit_field.rec_to_edit     = edit_field.rec_to_edit_int_to_str
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )

        # ---- id_old
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "id_old",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.id_old_field     = edit_field
        edit_field.setPlaceholderText( "id_old" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- name
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "name",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.name_field     = edit_field
        edit_field.setPlaceholderText( "name" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- add_kw
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "add_kw",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.add_kw_field     = edit_field
        edit_field.setPlaceholderText( "add_kw" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field )


        # ---- descr
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "descr",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.descr_field     = edit_field
        edit_field.setPlaceholderText( "descr" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field )


        # ---- type
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "type",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.type_field     = edit_field
        edit_field.setPlaceholderText( "type" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- series
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "series",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.series_field     = edit_field
        edit_field.setPlaceholderText( "series" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- author
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "author",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.author_field     = edit_field
        edit_field.setPlaceholderText( "author" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field )


        # ---- dt_enter
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "dt_enter",
                                                db_type        = "integer",
                                                display_type   = "timestamp",
                                                 )
        self.dt_enter_field     = edit_field
        edit_field.setPlaceholderText( "dt_enter" )
        edit_field.edit_to_rec     = edit_field.edit_to_rec_str_to_int
        edit_field.rec_to_edit     = edit_field.rec_to_edit_int_to_str
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- format
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "format",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.format_field     = edit_field
        edit_field.setPlaceholderText( "format" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- inv_id
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "inv_id",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.inv_id_field     = edit_field
        edit_field.setPlaceholderText( "inv_id" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- cmnt
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "cmnt",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.cmnt_field     = edit_field
        edit_field.setPlaceholderText( "cmnt" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- status
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "status",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.status_field     = edit_field
        edit_field.setPlaceholderText( "status" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- c_name
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "c_name",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.c_name_field     = edit_field
        edit_field.setPlaceholderText( "c_name" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- title
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "title",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.title_field     = edit_field
        edit_field.setPlaceholderText( "title" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field )


        # ---- tag
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "tag",
                                                db_type        = "string",
                                                display_type   = "skip",
                                                 )
        self.tag_field     = edit_field
        edit_field.setPlaceholderText( "tag" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- old_inv_id
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "old_inv_id",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.old_inv_id_field     = edit_field
        edit_field.setPlaceholderText( "old_inv_id" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- file
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "file",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.file_field     = edit_field
        edit_field.setPlaceholderText( "file" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- sub_dir
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "sub_dir",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.sub_dir_field     = edit_field
        edit_field.setPlaceholderText( "sub_dir" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- photo_url
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "photo_url",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.photo_url_field     = edit_field
        edit_field.setPlaceholderText( "photo_url" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- camera
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "camera",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.camera_field     = edit_field
        edit_field.setPlaceholderText( "camera" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- lens
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "lens",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.lens_field     = edit_field
        edit_field.setPlaceholderText( "lens" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- f_stop
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "f_stop",
                                                db_type        = "string",
                                                display_type   = "skip",
                                                 )
        self.f_stop_field     = edit_field
        edit_field.setPlaceholderText( "f_stop" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- shutter
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "shutter",
                                                db_type        = "integer",
                                                display_type   = "string",
                                                 )
        self.shutter_field     = edit_field
        edit_field.setPlaceholderText( "shutter" )
        edit_field.edit_to_rec     = edit_field.edit_to_rec_str_to_int
        edit_field.rec_to_edit     = edit_field.rec_to_edit_int_to_str
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- copyright
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "copyright",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.copyright_field     = edit_field
        edit_field.setPlaceholderText( "copyright" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


    # ---------------------------
    def select_record( self, id_value  ):
        """
        extension to support picture in detail tab
        """
        super( ).select_record( id_value )
        file_name     = self.get_picture_file_name()
        file_name     = base_document_tabs.fix_pic_filename( file_name )
        self.viewer.display_file( file_name )

    # ---------------------------
    def display_selected_pic( self,  ):
        """
        use when poking in a picture
        !! integrate with above
        """
        file_name     = self.get_picture_file_name()
        file_name     = base_document_tabs.fix_pic_filename( file_name )
        self.viewer.display_file( file_name )

    # -------------------------------------
    def new_record( self,  next_key, option = "default" ):
        """
        do not delete
        need to extend because we hava a picture
        if next_key is None key generated in the data manager
        """
        super().new_record( next_key, option = option )

        msg       = ( "new_record in picture document on to get picture")
        logging.debug( msg )

        file_name     = self.get_picture_file_name()
        file_name     = base_document_tabs.fix_pic_filename( file_name )
        self.viewer.display_file( file_name )

    # -----------------------------------------
    def update_db( self, ):
        """
        promoted, but now extend for subjects, may later re-promote
        """
        super().update_db()
        self.subject_sub_tab.update_db()

    # -----------------------------
    def clip_filename( self, ):
        """
        what it says
        """
        file_name    = self.get_picture_file_name()
        q_app        = AppGlobal.q_app
        clipboard    = q_app.clipboard()
        clipboard.setText(file_name)

    # -----------------------------
    def add_to_show( self, ):
        """
        # change name to add to album wehne ewe get farther alogn
        add a picture to a show -- which must be open in another window
        query.addBindValue( data_in_dict["photo_id"]  )
        """
        # dict is a bit odd  --- some is wrong all we really need i sphot_id
        #photo_id      =  int( self.id_field.text() )  # may be available elsewhere   this worul db test
        photo_id      =  self.data_manager.current_id
        photo_fn      =  self.file_field.text()
        row_dict            = { "photo_name":               "from photo sub_window",
                                "photo_fn":                  photo_fn,
                                "photo_id":                  photo_id,
                                "photoshow_photo_id":        photo_id,
                               }

        photo_target     = AppGlobal.mdi_management.get_album_doc()
        #photo_target   = AppGlobal.add_photo_target
        if   photo_target is not None:
            msg       = ( f" check target has a current id  {photo_target = }")
            logging.debug( msg )
            photo_target.add_photo_to_show( row_dict )
                # perhaps in album picture sub tab

        else:
            msg    = "add_to_show not sure why we have this else message "
            qsql_utils.ok_message_box(  title = "Action Needed:",
                                        msg = msg )
            logging.debug( msg )

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
        #descr      = self.descr_field.text()
        name       = self.name_field.text()
        add_kw     = self.add_kw_field.text()
        #print(  ia_qt.q_line_edit( self.name_field,
        #                   msg = "this is the name field",  ) # include_dir = True ) )

        # add_ts   = self.add_ts_field.text()
        edit_ts  = self.edit_ts_field.text()
        edit_ts  = "self.edit_ts_field.text()"   # !! test

        self.default_new_row(  next_key )

        # ---- set the defaults

        #self.descr_field.setText( descr + "*" )
        self.name_field.setText( name + "*" )

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
        self.clear_fields()

        # ---- ??redef add_ts
        a_ts   = str( time.time() ) + "sec"
        # record.setValue( "add_ts",  a_ts    )
        self.add_ts_field.setText(  a_ts )
        self.edit_ts_field.setText( a_ts )

        self.id_field.setText( str( next_key ) )

    # ------------------------
    def get_picture_file_name(self):
        """
        some promotable -- but picture is special only one file, rest
        work differently
        what it says, read
        build from parameters, and record fields
        fix \  /  and make sure no dups of //

        return file_name or None if no file name
        """
        # self.sub_dir_field.text()
        # self.file_field.text()

        full_file_name  = base_document_tabs.build_pic_filename( self.file_field.text(), self.sub_dir_field.text() )


        # root         = AppGlobal.parameters.picture_db_root + "/"
        # file_dir     = self.sub_dir_field.text() + "/"
        # file_name    = self.file_field.text().strip()
        # if file_name == "":
        #     return None

        # full_file_name   = f"{root}{file_dir}{file_name}".replace( "\\", "/" )
        # full_file_name   = full_file_name.replace( "///", "/" )  # just in case we have dups
        # full_file_name   = full_file_name.replace( "//", "/" )   # just in case we have dups

        msg       = ( f"picture_document.get_picture_file_name{full_file_name}")
        logging.debug( msg )

        return full_file_name

# ==================================
class PictureTextTab( base_document_tabs.TextTabBase   ):

    def __init__(self, parent_window  ):
        """
        the usual

        """
        super().__init__( parent_window )

        msg       = ( "init PictureTextTab" )
        logging.debug( msg )

        super().__init__( parent_window )
        self.tab_name            = "PictureTextTab"

        msg       = ( "init end PictureTextTab {self.tab_name = }" )
        logging.debug( msg )

        self.post_init()

    #-------------------------------------
    def __build_gui( self ):
        """
        what it says read
        promotable ??
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
    def default_new_row(self, key ):
        """
        what it says
            this is for a new row on the window -- no save
            needs key but timestamp Picture from detail not text
        arg:
            next_key for table, just trow out if not used
        Returns:
            None.

        """
        self.clear_fields()

        self.text_data_field.setText( f"this is the default text for id { key = }" )

        # # ---- ??redef add_ts
        # a_ts   = str( time.time() ) + "sec"
        # # record.setValue( "add_ts",  a_ts    )
        # self.add_ts_field.setText(  a_ts )
        # self.edit_ts_field.setText( a_ts )

        self.id_field.setText( str( key ) )

    # ----------------------------
    def fetch_detail_row( self,  a_id = None ):
        """
        Args:
            id can be external or as chat has it fetched

        Returns:
            None.
        !! could be promoted
        """
        a_id      = self.id_field.text()

        msg       = (  f"Picture text tab fetch_row { a_id = }")
        logging.debug( msg )

        self.fetch_detail_row_by_id( a_id )

    # -----------------------------
    def delete_detail_row(self):
        """
        looks like could be promoted -- db key needs to stay id
              but need to delete detail_children as well
              but need to delete key words as well
        what it says read
         delete_detail_row delete_detail_row
        Returns:
            None.

        """
        model       = self.tab_model
        a_id          = self.id_field.text()
        if a_id:
            model.setFilter( f"a_id = {a_id}" )
            model.select()
            if model.rowCount() > 0:
                model.removeRow(0)
                model.submitAll()
                QMessageBox.information(self, "Delete Ok",
                            "detail_text_model Record deleted successfully.")
                self.clear_fields()
            else:
                msg   = "Delete Error: No record found with the given ID. { a_id = } "
                QMessageBox.warning(self, "Error",  msg )
                AppGlobal.logger.error( msg )
        else:
            msg  = f"Please enter a valid ID. { a_id = }"
            QMessageBox.warning(self, "Input Error", "Please enter a valid ID.")
            AppGlobal.logger.error( msg )


    # ---------------------
    def delete_record_update(self):
        """
        from russ crud  --- think ok in picture_text
        try in picture_detail
        !! should this still exist
        """
        model    = self.tab_model
        if not self.record_state  == base_document_tabs.RECORD_DELETE:
            print( f"delete_record_update  is !! obsolete bad state, return  {self.record_state  = }")
            return
        id_value    = self.deleted_record_id
        if id_value:
            model.setFilter(f"id = {id_value}")
            model.select()
            if model.rowCount() > 0:
                model.removeRow(0)
                model.submitAll()
                self.clear_fields()  # will fix record state
                self.record_state       = base_document_tabs.RECORD_NULL
                QMessageBox.information(self, "Delete", "Record deleted!")
            model.setFilter( "" )

# ==================================
class PicturePictureTab_promoted ( base_document_tabs.DetailTabBase   ):
    """
    look at promotion in parents not sure why this needs to be here as well
    this one is for one photo per detail only may need to be different
    """
    def __init__(self, parent_window  ):
        """
        this tab does not interact with the db directly
        big view of the picture

        """
        super().__init__( parent_window )

        #rint( f"PicturePictureTab __init__ {parent_window = }")
        self.__build_gui()

    #-------------------------------------
    def __build_gui( self ):
        """
        what it says read
        Returns:
            none
        """
        tab                 = self
        tab_layout          = QVBoxLayout(tab)

        #viewer              = picture_viewer.PictureViewer( self )
        viewer              = picture_viewer.PictureViewerPlus( self )
        self.viewer         = viewer
        tab_layout.addWidget( viewer )

        self.display_file()

        # ---- buttons
        a_widget        = QPushButton( "fit" )
        a_widget.clicked.connect(  self.fit_in_view )
        tab_layout.addWidget( a_widget )

        #rint( "see chat_photo.py for more ... zoom to fit rectangle      chat_photo_3.py " )

    # -----------------------------
    def display_file( self,  file_name = "/mnt/WIN_D/PhotoDB/02/102-0255_img.jpg"  ):
        """
        what it says, read
        acll from ?
        !! use instead filename  = base_document_tabs.fix_pic_filename( filename   )
        """
        file_path       = Path( file_name )
        if not file_path.exists():
            # !! print a message
            # should be a no file file

            # msg         = f"picture_document display_file, file not found {file_name} will use file not found "
            # AppGlobal.logger.info( msg )
            # print( msg )
            file_name   = AppGlobal.parameters.pic_nf_file_name

        self.viewer.display_file( file_name )
        self.fit_in_view()

    # ---------------------------
    def select_record( self, id_value  ):
        """
        this is override of parent as we get file name from
        our detail sister tab
        """
        picture_file_name    = self.parent_window.detail_tab.get_picture_file_name()
        #rint( f"picture picture tab, select_record {picture_file_name}")

        self.display_file( picture_file_name )

    # ------------------------------------------
    def select_by_id ( self, id ):
        """
        try to get one that works
        """
        msg       = ( f"picture picture tab select_by_id, do I get called ................................select_by_id")
        logging.debug( msg )

    # ---- zooms, may also be in context map, may want buttons for these
    #          or delete
    #-------------------------------------
    def zoom_in(self):
        self.viewer.zoom_in()
        #rint("Zoomed In")

    #-------------------------------------
    def zoom_out(self):
        self.viewer.zoom_out()
        #rint("Zoomed Out")

    def reset_zoom(self):
        self.viewer.reset_zoom()
        #rint("Zoom Reset")

    #-------------------------------------
    def fit_in_view(self):
        self.viewer.fit_in_view()
        #rint("PicturePictureTab Fit in View")

# ==================================
#class PictureBrowseSubTab( base_document_tabs.StuffdbTab   ):
class PictureBrowseSubTab( QWidget ):
    """
    """
    def __init__(self, parent_window  ):
        """
        this tab does not interact with the db directly
        it browses and previews picture files, and
        can fill the picture id in other tabs
        """
        super().__init__()
        self.parent_window   = parent_window
        #rint( f"PicturePictureTab __init__ {parent_window = }")
        self.__build_gui()

    #-------------------------------------
    def __build_gui( self ):
        """
        what it says read
        Returns:
            none
            and model

        """
        tab                 = self
        tab_layout          = QHBoxLayout(tab)
        button_layout       = QVBoxLayout( )
        tab_layout.addLayout( button_layout )

        # Column headers
        headers = ["File Name", "Date", "What"]
        #self.view           = QTableView()
        self.model          = table_model.TableModel( headers)
        #self.model.set_data( data )

        # Proxy model for sorting
        proxy_model         = QSortFilterProxyModel()
        proxy_model.setSourceModel( self.model )
        self.proxy_model    = proxy_model

        table_view          = QTableView()
        self.table_view     = table_view
        # Connect the clicked signal to a slot
        table_view.clicked.connect( self.on_row_clicked )
        # table_view.setModel( self.model )
        table_view.setModel( proxy_model )  # table_model for no sorting

        table_view.setSelectionBehavior(QTableView.SelectRows)

        table_view.setSortingEnabled( True )
            # Enables sorting by clicking column headers may need QSort....

        tab_layout.addWidget( table_view )

        #self.view.clicked.connect( self._on_list_click  )

        viewer              = picture_viewer.PictureViewer( self )
        viewer.set_fnf( parameters.PARAMETERS.pic_nf_file_name )
        self.viewer         = viewer
        tab_layout.addWidget( viewer )

        self.display_file()

        # ---- buttons
        a_widget        = QPushButton( "Browse" )
        a_widget.clicked.connect( self.browse )
        button_layout.addWidget( a_widget )

        a_widget        = QPushButton( "move_to_pic" )
        a_widget.clicked.connect( self.move_to_pic )
        button_layout.addWidget( a_widget )

        a_widget        = QPushButton( "move_all" )
        a_widget.clicked.connect( self.move_all )
        button_layout.addWidget( a_widget )


        a_widget        = QPushButton( "fit" )
        a_widget.clicked.connect( self.fit_in_view )
        button_layout.addWidget( a_widget )

    # -------------------------
    def browse( self, ):
        """
        what it says, read.... more coming maybe
        should auto select the first file
        or the fnf image if not if cancel
        just leave alone

        get date and populate
        can we sort ?

        """
        initial_dir     = AppGlobal.parameters.picture_browse

        file_dialog     = QFileDialog(self, "Select Files")

        file_dialog.setFileMode(QFileDialog.ExistingFiles) #multiple file selection
        file_dialog.setNameFilter("All Files (*);;Text Files (*.txt)")
        file_dialog.setDirectory(    initial_dir )
        # file_dialog.setWindowTitle(  title      )
        # #file_dialog.setNameFilter(   file_types  )

        if not file_dialog.exec_():
            return

        files = file_dialog.selectedFiles()
        self.model.clear_data()

        # msg       = ("browse Selected files:")
        # logging.debug( msg )

        for file in files:
            print(file)
            file_path    = Path( file )
            st_size      = file_path.stat().st_size
            st_mtime     = file_path.stat().st_mtime
                # or atime } "      .st_mtime st_ctime st_atime

            row_data     = [ file, st_mtime, st_size ]
            self.model.addRow( row_data)

        self.display_file_at_row(  0  )

    # --------------------------------------
    def move_all_setup( self,  ):
        """
        check that the setup is ok
        have apicture in the current document
            perhaps has a title...
            has a file

        have a single album to add the pictures to

        return -- album document....
        raise  some exception if error
        check we have some photos


        """
        detail_tab          = self.parent_window

        current_filename    = detail_tab.file_field.get_raw_data().strip( )
        if current_filename == "":
            msg       = ( f"You need to have a file_name for the picture ")
            #logging.debug( msg )
            raise app_exceptions.ApplicationError( msg )

        # next from add to show in detail, perhaps factor out
        #photo_target     = AppGlobal.mdi_management.get_album_doc()
        album_docs       = AppGlobal.mdi_management.get_album_docs()
        len_album_docs   = len( album_docs )

        if len_album_docs == 0:
            msg     = "For this to work you need 1 Album Document open, you have none 0."
            raise app_exceptions.ReturnToGui( msg )

        if len_album_docs >  1:
            msg     = f"For this to work you need 1 Album Document open, you have {len_album_docs}."
            raise app_exceptions.ReturnToGui( msg )

        album_target    = album_docs[ 0 ]
        record_state    = album_target.detail_tab.data_manager.record_state

        if record_state == 0:
            msg     = f"For this to work you need an item in your Album Document."
            raise app_exceptions.ReturnToGui( msg )

        #rint( f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Error still need to check it has a record {record_state}")

        if self.model.rowCount() < 1:
            msg       = ( f"For this to work you need to have some files in this tab.")
            logging.debug( msg )
            raise app_exceptions.ReturnToGui( msg )

        return album_target

    # --------------------------------------
    def move_all( self,  ):
        """
        move all picture files to new picture documents

        """
        # msg       = ( "\n move_all ")
        # logging.debug( msg )

        try:
            # msg       = ( "\n trying move_all_setup")
            # logging.debug( msg )

            album_target = self.move_all_setup()

        except app_exceptions.ReturnToGui as an_except:
            msg       = f"{str( an_except)}"
            QMessageBox.information( AppGlobal.main_window,   "Info", msg )
            return


        model       = self.model
        ix_debug    = 0
        while True:
            if self.model.rowCount() < 1:
                break
            ix_debug +=1
            if ix_debug > 3:
                break
            # need to add a record
            self.parent_window.parent_window.add_copy()  # document =
            print( "^^^^^^^^^^^^^^^^^^^^^^^ break and see if we have added one record, did we save the last ")
            break
            # Typically use column 0 for row operations
            parent  = QModelIndex()  # Usually an invalid/empty parent index for table models
                    ## perhaps just use none

            index = model.index(0, 0, parent)
            # will send off to move_to_pic





        msg         = ( "\n unfinished return ++++++++++++++++++++++++++++++++++++++++++++")
        logging.debug( msg )
        return

        #--------------------------------------------------

        parameters          = AppGlobal.parameters
        db_root             = parameters.picture_db_root
        db_sub              = parameters.picture_db_sub

        # only want to remove beginning and end do not use replace
        # assume embedded are ok
        #db_sub              = db_sub.replace( "/", "" )

        if db_sub.startswith( "/" ):
            db_sub         = db_sub[ 1: ]

        if db_sub.endswith( "/" ):
            db_sub         = db_sub[ :-1 ]

        detail_tab          = self.parent_window

        current_filename    = detail_tab.file_field.get_raw_data().strip( )
        if current_filename != "":

            qsql_utils.ok_message_box(  title = "That is a No Go",
                                        msg   = "You already have a picture file! "   )

            # or perhaps an exception
            return


    # --------------------------------------
    def move_to_pic( self, index: QModelIndex):
        """
        move picture file to correct directory and
        names to the form, then save as file is moved
        may link to double click?

        still need to wory about saves at begin and end
        the sub dir needs to fill with default

        a bit of a mess some check made twice
 /mnt/WIN_D/temp_photo/99/new_test
'/mnt/WIN_D/temp_photo/99new_test/PXL_20240703_171511213.jpg')
        """
        msg       = ( "\nmove_to_pic")
        logging.debug( msg )

        parameters          = AppGlobal.parameters
        db_root             = parameters.picture_db_root
        db_sub              = parameters.picture_db_sub

        # only want to remove beginning and end do not use replace
        # assume embedded are ok
        #db_sub              = db_sub.replace( "/", "" )

        if db_sub.startswith( "/" ):
            db_sub         = db_sub[ 1: ]

        if db_sub.endswith( "/" ):
            db_sub         = db_sub[ :-1 ]

        detail_tab          = self.parent_window

        current_filename    = detail_tab.file_field.get_raw_data().strip( )
        if current_filename != "":

            qsql_utils.ok_message_box(  title = "That is a No Go",
                                        msg   = "You already have a picture file! "   )

            # or perhaps an exception
            return

        #rint( "make sure we have a file to move ")

        view            = self.table_view
        row             = -1
        # Assuming `view` is your QTableView
        selection_model = view.selectionModel()
        if selection_model:
            selected_indexes = selection_model.selectedRows()

            # Iterate over the selected rows
            for index in selected_indexes:
                row = index.row()
                msg       = (f"Selected row: {row = }")
                logging.debug( msg )

                break   # only get one

        if row == -1:
            msg       = ( "no selected row")
            logging.debug( msg )

            return

        # set up the sub dir
        db_sub_widget       = detail_tab.sub_dir_field
        db_sub_widget.set_preped_data( db_sub, is_changed = True )

        model               = self.model
        index               = model.index( row, 0 )
        # Get the data for the current index
        filename            = model.data( index )
        file_name_path_src  = Path( filename )

        file_name_path_name = file_name_path_src.name

        file_name_path_dest = Path().joinpath( db_root, db_sub, file_name_path_name )

        # now need to get access to detail tabl may be my parent check if we need all
        parent_window    = self.parent_window
        form_id          = parent_window.id_field.get_raw_data()
        form_sub_dir     = parent_window.sub_dir_field.get_raw_data()
        form_file        = parent_window.file_field.get_raw_data().strip()

        print( "some debug -- inspect might be better ")

        print( f"{form_id = }   ")
        print( f"{form_sub_dir = }   ")
        print( f"{form_file = }   ")

        print( f"{db_root = }   ")
        print( f"{db_sub = }  ")
        print( f"{file_name_path_name = }  ")
        print( f"{file_name_path_src =  }  ")
        print( f"{file_name_path_dest = } ")

        if not form_file == "":
            msg       = ( "file is already set, you need a new record")
            logging.debug( msg )

            return

        #rint( "!! need to check that the destination file does not exist ")
        if os.path.exists( file_name_path_dest ):
            msg   = ( "dest file   already exists")
            logging.debug( msg )
            return

        # parent_window.sub_dir_field.set_preped_data( db_sub )
        parent_window.file_field.set_preped_data( str( file_name_path_name ),  is_changed = True )

        try:
            shutil.move( file_name_path_src, file_name_path_dest )

        except Exception as a_except:
            msg       = ( f"Exception {a_except = }" )
            logging.error( msg )

            1/0

        #rint( "delete from the browse seems not working ")

        model.removeRow( row )

        #rint(  "might be nice to select the next logical row if any ")
        self.display_file_at_row( row )

        msg       = (  "might be nice to select the next logical row if any .. and more print here ")
        logging.debug( msg )

        print( "we should automically save here !! ")

        print( "need to make display seems ok !! ")

        parent_window.display_selected_pic()
        document_window    = parent_window.parent_window

        document_window.update_db()

        return

    # --------------------------------------
    def on_row_clicked( self, index: QModelIndex):
        """

        """
        row = index.row()

        # Retrieve the data for the entire row
        row_data = [self.model.data(self.model.index(row, col)) for col in range(self.model.columnCount())]

        msg     = (f"on_row_clicked Row {row + 1} clicked: {row_data}")
        logging.debug( msg )

        file_name   = row_data[0]   # what is 0 file name
        self.display_file( file_name )

    # -----------------------------
    def display_file_at_row( self,  row  ):
        """
        what it says, read
        note that this row may not exist, then work towards 0
        combine with on_row_clicked !!
        need to select the row
        """
        model       =  self.model
        row_count   = model.rowCount()
        if row_count == 0:
            pass
            msg    = ( "display_file_at_row how display 404")
            logging.debug( msg )
            return

        if not row < model.rowCount():
            row = row_count -1

        self.select_row( row )
        row_data = [self.model.data(self.model.index(row, col)) for col in range(self.model.columnCount())]

        msg       = ( f"display_file_at_row Row {row + 1} clicked: {row_data}" )
        logging.debug( msg )

        file_name   = row_data[0]   # what is 0 file name
        self.display_file( file_name )

    #-----------------------------------------------
    def select_row(self, row_index ):
          """
          Select a specific row.
          """
          model           = self.model
          view            = self.table_view

          selection_model = view.selectionModel()

          row_start       = model.index(row_index, 0)
          row_end         = model.index(row_index, model.columnCount() - 1)

          selection_model.select(row_start, selection_model.Select | selection_model.Rows)

    # -----------------------------
    def display_file( self,  file_name = "/mnt/WIN_D/PhotoDB/02/102-0255_img.jpg"  ):
        """
        what it says, read
        call from ?
        """
        # pixmap      = QPixmap( file_name )
        # self.viewer.set_photo( pixmap )
        self.viewer.display_file( file_name )
        self.fit_in_view()

    # ---- zooms, may also be in context map, may want buttons for these
    #          or delete
    #-------------------------------------
    def zoom_in(self):
        self.viewer.zoom_in()
        #rint("Zoomed In")

    #-------------------------------------
    def zoom_out(self):
        self.viewer.zoom_out()
        #rint("Zoomed Out")

    def reset_zoom(self):
        self.viewer.reset_zoom()
        #rint("Zoom Reset")

    #-------------------------------------
    def fit_in_view(self):
        self.viewer.fit_in_view()
        #rint("PicturePictureTab Fit in View")

# ----------------------------------------
class PictureSubjectSubTab( base_document_tabs.SubTabBase  ):
    """ """

    def __init__(self, parent_window ):
        """
        the usual
            need to think out the names --- duplicates and where built

                self.model_other
                model_other     subjects in other windows
                index_other
                    select_1_model

                model_history   subjects used in past -- not implemented yet
                indexer_history
                    select_2_model  select2

                model_display   subjects in db for display   TableModel
                    think this is also the history or something similar
                    this is not the history
                    self.model_display

                    self.view_display
                    indexer_display


                 self.model_subject  used for query ( but could just use a qsqlueryy might be better )
                     no view
                     are the subjects decoded and shown from self.model
                     data moved over to model_display for viewing

                self.model           subjects in db               QSqlTableModel
                        we do not do relational because join my be to other
                        tables
                        we should be able to do updates here without need for other
                        query object
                        but we will need another object for display
                view
                indexer
                    model

        logic for this: -- right now just get to work who cares how inefficient

           * relational select on subjects
                find all subjects from other tabs

                delete, hide all subjects from other tabs we have already
                    consider use of index on relational model =

            * add a subject
                use query do save to do this then reselect subjects see above

            * update in another window
                for now be inefficient
                rebuild model.other
                loop thru and delete redundant

            * later

                still need to think of list of recent subjects and how to manage

            --- on topic update -- rebuild the model other then delete subjects we have
                                    or build while checking as more efficient ?

                    after relational select could build a index on it

            ----------------

        """
        super().__init__( parent_window )

        self.table_name     = "photo_subject"
        self.tab_name       = "PictureSubjectSubTab"

        self.model_ituple           = None # to index table, table_id

        self.model_other            = None
        self.model_other_ituple     = ( 0, 1 ) # to index table, table_id
            # ituple is indexer tuple for building index

        self._build_model()
        self._build_gui()

        # next is special for picture
        # ------ init the topics = subjects need to iterate on current_topics and closed topics
        # just for debug
        open_topics         = AppGlobal.mdi_management.open_topics
        msg       = ( f"in init {open_topics = }")
        logging.debug( msg )

        msg       = ( "next should be topic delete and topic update ")
        logging.debug( msg )


        # mdi = MDI()
        #AppGlobal.mdi_management.topic_update_signal.connect( self.topic_update )
        send_signals  = AppGlobal.mdi_management.send_signals
        send_signals.topic_update_signal.connect( self.topic_update )

        self.model_indexer  = table_model.ModelIndexer( self.model, self.model_ituple )  # table,  table_id


    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says, read
        """
        page                = self
        tab                 = page

        layout              = QHBoxLayout( tab )
        left_layout         = QVBoxLayout(   )
        right_layout        = QVBoxLayout(   )
        layout.addLayout( left_layout )
        layout.addLayout( right_layout )

        button_layout        = left_layout  # need not add is a dup

        # ---- views
        # ---- guide to models and views
        # subjects/topics currently open in other windows
            #self.model_other/self.view_other
        # subjects/topics that have been selected for this pic s display only no db
            #self.model_display/self.view_display
        # subject/topics connected to db
            # self.model_subject / self.list_view  / self.model self.model_indexer

        headers = [ "table", "table_id", "info"]   # other is items from other windows, clears when
        model_other           = table_model.TableModel( headers)
        self.model_other      = model_other
        model_other.add_indexer(  self.model_other_ituple )

        view_other            = QTableView()
        self.view_other       = view_other
        view_other.setSelectionBehavior( QTableView.SelectRows )
        view_other.doubleClicked.connect( self.on_row_other_dclicked )
        view_other.setModel( model_other)
        print( "!! _build_gui set indexer tuple next probably wrong -- or not special tab ")
        right_layout.addWidget( view_other )

        # ---- view_history
        headers = ["history", "22", "32", "43"]
        #self.view           = QTableView()
        model_history           = table_model.TableModel( headers)
        self.model_history      = model_history
        view_history            = QTableView()
        self.view_history       = view_history
        view_history.setSelectionBehavior( QTableView.SelectRows )
        #select1_view.clicked.connect( self.on_row_clicked )
        view_history.setModel(  model_history)

        #rint( "_build_gui unhide history layout later ")
        self.save_view_history  = view_history
        #right_layout.addWidget( view_history )
        #ia_qt.q_abstract_table_model( select1_model, "this is my message for my table >>>>>>>>>>>>>>>>>>>>>>>>>>>" )

        # ----  model_display
        headers = ["display", "b", "c", "d"]
        #self.view           = QTableView()
        model_display           = table_model.TableModel( headers)
        self.model_display      = model_display
        model_display.add_indexer( ( 1,2 ) )   # what is the right tuple
        view_display            = QTableView()
        self.view_display       = view_display
        view_display.setSelectionBehavior( QTableView.SelectRows )
        #select1_view.clicked.connect( self.on_row_clicked )
        view_display.setModel(  model_display )
        right_layout.addWidget( view_display )
        info = """
            do seperate join on each table and put in here
            photo_subject.id
            photo_subject.table_joined
            photo_subject.table_id
            photo_subject.photo_id
            table.info ....

        """

        view                    = QTableView()
        self.list_view          = view
        view.setSelectionBehavior( QTableView.SelectRows )
        self.view               = view
        view.setModel( self.model )
        right_layout.addWidget( view )

        widget        = QLabel( 'other\nwin-->' )
        button_layout.addWidget( widget )

        widget        = QPushButton( 'add to\nsubj' )
        widget.clicked.connect( self.add_selected_other )
        button_layout.addWidget( widget )

        #
        #widget        = QPushButton('edit_record')
        #add_button    = widget
        #widget.clicked.connect(self.edit_record)
        #button_layout.addWidget( widget )

        # widget        = QPushButton('save_subjects')
        # #add_button    = widget
        # widget.clicked.connect( self.save_subjects )
        # button_layout.addWidget( widget )

        widget        = QLabel( 'our\nsubj-->' )
        button_layout.addWidget( widget )

        widget        = QPushButton('delete')
        widget.clicked.connect(self.delete_record)
        button_layout.addWidget( widget )

        widget        = QPushButton('lts')
        #add_button    = widget
        widget.clicked.connect(self.loop_thru_subjects )
        button_layout.addWidget( widget )

        widget        = QPushButton('inspect')
        #add_button    = widget
        widget.clicked.connect(self.inspect )
        button_layout.addWidget( widget )

    # ---------------------------------
    def _build_model( self, ):
        """
        Returns:
            modifies self,
            we need 2 models, one for the photo_subjects, and
            one that goes after the subjects
            lets call the first the model
        """
        msg       = ( "look at build model this may be a big mix up !!")
        logging.info( msg )

        # ---- model        ---- gets subjects but for background as we need join to
        #      get good display of inf see
        model              = QSqlTableModel( self, self.db )
        #model              = qt_with_logging.QSqlTableModelWithLogging(  self, self.db    )

        self.model          = model    # these are the subjects in the db

        model.setTable( self.table_name )
        self.model_ituple   = ( 3, 5 ) # to index table, table_id check with table
        model_indexer       = table_model.ModelIndexer( model, self.model_ituple  ) # to index table, table_id )
        self.model_indexer  = model_indexer
        model.setEditStrategy( QSqlTableModel.OnManualSubmit )
        # model_write.setEditStrategy( QSqlTableModel.OnFieldChange )
        # model.setFilter( "stuff_id = 28 " )
        # print( "!!fix stuff_id = 28 ")

        # ---- model subject
        # ============================================================
        # ---- model_subject ---- this will get the subjects, tables will be switched -- no update
        model               = QSqlTableModel( self, self.db )
        self.model_subject  = model   #  is this the display not yet implemented

       # we will switch the table, or maybe later have a bunch

    #-------------------------------------
    def create_index( self, ):
        """
        are we indexing the right guy
        """
        self.model_index.create_index()

        msg       = ( f"{self.model_index = }" )
        logging.debug( msg )

    #-------------------------------------
    def topics_changed( self, topic_dict ):
        """
        dec   2024 looks like may still work but needs list of dicsa zzz
        should not be able to add dups, since it is
        based on a dict it should not unless implementation is changed
        sent from mdi_manager  -- but my not be best
        """
        model   = self.model_other

        msg     = ( f"topics_changed {topic_dict = } !! may need change so we do not reload the whole thing " )
        logging.debug( msg )

        model.clear_data()
        # now populate the model
        for i_key, i_value in topic_dict.items():
            i_table, i_id    = i_key
            i_info           = i_value
            row_data     = [ i_table, str(i_id),  str(i_info) ]
            #rint( f"{row_data = }")
            model.addRow( row_data)

        #ia_qt.q_abstract_table_model( model, "topics_changed" )

    # ------------------------------------------
    def on_row_other_dclicked( self, index: QModelIndex):
        """
        what it says, read, search  --- should be a double clicked
        """
        model    = self.model_other    # table_model.TableModel( headers)
        row      = index.row()

        msg       = ( f"on_row_other_clicked {row = }")
        logging.debug( msg )

        self.add_ix_other( row )

    # -------------------------------------
    def i_am_hsw(self):
        """
        make sure call is to here
        """
        print( "i_am_hsw")

    # -------------------------------------
    def default_new_row( self ):
        """tail_tab.default_new_row( next_key )
        default values for a new row in the detail and the
        text tabs

        Returns:
            None.

        """
        next_key      = AppGlobal.key_gen.get_next_key(
            self.detail_table_name )
        self.detail_tab.default_new_row( next_key )
        self.text_tab.default_new_row(   next_key )

    # ------------------------------------------
    def delete_all(self):
        """
        what it says, read?  promote all
        """
        # msg   = "PictureSubjectSubTab  delete_all ... not implemented yet "
        # QMessageBox
        # model              = QSqlTableModel( self, self.db )
        #model              = qt_with_logging.QSqlTableModelWithLogging(  self, self.db    )
        print( "delete_all note that rows will still be visible unless do something to refresh ")
        model  = self.model
        ia_qt.q_sql_table_model( model )
        # Loop through the rows in reverse order and delete them
        for row in range(model.rowCount() - 1, -1, -1 ):
            model.removeRow(row)
        self.view.show()

        ia_qt.q_sql_table_model( model )
        print( "for now update and select ")

        if model.submitAll():
            model.select()  # Refresh the model to reflect changes in the view
        else:
            model.database().rollback()  # Rollback if submitAll fails
            print( "submitAll fail rollback ")

    # ------------------------------------------
    def delete_record (self):
        """
        what it says, read?

        set current id, get children
        """
        msg   = "delete_record ... not implemented"
        QMessageBox.warning(self, "Sorry", msg )

    # ------------------------------------------
    def add_ix_other(self, ix_row_integer ):
        """
        add the ix_integer other model to the subject models
        """
        model_other     = self.model_other
        data_list       = []
        for ix_col in range( 3 ):
            index     = model_other.index( ix_row_integer, ix_col )
            data      = model_other.data( index, ) #role=Qt.DisplayRole)
            data_list.append( data )

        msg       = ( f"add_ix_other {ix_row_integer = } {data_list = }" )
        logging.debug( msg )
        msg       = ( "next call add to model all subjects>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<")
        logging.debug( msg )

        #self.add_to_model_all_subjects( self.current_id, table, table_id, info )
        self.add_to_model_all_subjects( self.current_id, data_list[0], data_list[1], data_list[2] )

    # ------------------------------------------
    def add_selected_other( self ):
        """
        test routine, add the now selected other  first other to the subjects
        maybe the real thing who says test
        2024Dec   -- review and get to work
        perhaps at first just one then more later
        """
        # got row
        # get values
        # add
        msg       = ( "add_selected_other -- may not do the right thin but does something ")
        logging.debug( msg )

        model_other         = self.model_other  # subject from other windows
        row_count           = model_other.rowCount()
        view                = self.view_other
        selected_indexes    = view.selectionModel().selectedIndexes()
        if selected_indexes:
            for index in selected_indexes:
                i_row = index.row()
                # column = index.column()
                # print(f"Selected Cell - Row: {row}, Column: {column}")
        else:
            msg    = ("add_selected_other No selection !! still print may need dialog ")
            logging.debug( msg )

            return

        msg  = ( "add_selected_other about to add a row, but probably should be rebuilt {row = } probably inside loop")
        logging.debug( msg )

        #ret   = self.add_ix_other( row )
        index       = model_other.index( i_row, 0 )  # table  =at 0 ??
        table       = model_other.data( index )

        index       = model_other.index( i_row, 1 )  # table_id at 1
        table_id    = model_other.data( index )

        self.add_selected_other_2(  table, table_id  )
        msg  = ( "add_selected_other --think we want a save now then select_by_id 2024Dec")

        if self.model.submitAll():
            msg  = ("Changes committed no error detected ")
            logging.debug( msg )
        else:
            msg  = ("Error committing changes:", self.model.lastError().text())
            logging.debug( msg )

        msg  = ( "you may want to select_all or get_data_from_model next ")
        logging.debug( msg )

        # ---- debug inspect
        # self_model          = self.model
        # self_current_id     = self.current_id
        # wat_inspector.go(
        #      msg            = "from picture document add_selected_other_2",
        #      a_locals       = locals(),
        #      a_globals      = globals(), )


        self.select_by_id(   self.current_id  )

        return
        # off to ..... add_to_model_all_subjects
        # think better to add all code back here  or new place


        print( f"add_selected_other {row_count = } not finished delete row if in subjects" )
        # if row_count < 1:
        #     return
        # ret   = self.add_ix_other( row_count - 1 )
        msg  = """
            index, could index 0 to all tables.  In any case have to go thru the
            subjects (  self.model???) at least once which we also have to do to index it.  and it may be long
            for self model other is short so do we even needed an index?  but we do search as many times as we have
            subjects ... also small --- if we index think we should do on the self.model_other but maybe skip as
            premature optimization??

            """
        print( "add_selected_other --think we want a save now then select_by_id 2024Dec")


    def add_selected_other_2( self, table, table_id ):
        """
        test routine, actually do the add to ...
        what does it need to know  table and table_id can figure out the rest
        """
        print( f"need to add {table = } {table_id = } need check for dups ")
        next_key                    = AppGlobal.key_gen.get_next_key(  "photo_subject" )
        # sequence      = get_max there is not sequence
        photo_id                    = self.current_id
        table_id                    = int( table_id )

        # self_model                  = self.model
        # self_model_indexer          = self.model_indexer

        # now do model insert  --  ! but I should know the field names so this do by index is wrong
        model           = self.model
        new_record      = model.record()

        i_name          = new_record.fieldName( 0 ) # 0 = next_key
        new_record.setValue( i_name, next_key )

        i_name          = new_record.fieldName( 3 ) # 0 table_joined
        new_record.setValue( i_name, table )

        i_name          = new_record.fieldName( 4 ) # photo id
        new_record.setValue( i_name, photo_id )

        i_name          = new_record.fieldName( 5 ) # 5 table_id
        new_record.setValue( i_name, table_id )

        if model.insertRecord( -1, new_record):
            pass

        else:
            print("Error inserting record:", model.lastError().text())

        # wat_inspector.go(
        #      msg            = "from picture document add_selected_other_2",
        #      a_locals       = locals(),
        #      a_globals      = globals(), )

    #--------------------------------
    def loop_thru_other( self ):
        """

        """
        # model_subjects is just model
        model    = self.model  # .TableModel( headers) QAbstractTableModel
        ix_table_joined  = 3
        ix_table_id      = 5
        for ix_row in range( model.rowCount()  ):
            record = model.record(ix_row)

            for i in range(record.count()):
                msg   = ( f"loop_thru_other Field by index {i = } {record.fieldName(i)}: {record.value(i)}")
                logging.debug( msg )
            msg   = ( f"{record.value(ix_table_joined)}) {record.value(ix_table_id)})" )
            logging.debug( msg )
            record_key    = (record.value(ix_table_joined), record.value(ix_table_id))
            msg   = ( f"{record_key = }")
            logging.debug( msg )

    # ------------------------------------------
    def loop_thru_subjects( self ):
        """
        test routine, add the first other to the subjects
        maybe the real thing who says test

        new_record      = model.record()
        c_names         = []
        max_col         = new_record.count()
        for ix_col in range( max_col ):    # seems ok to index past end
            i_name     = new_record.fieldName( ix_col )
            c_names.append( i_name )
            self.add_line( f"{self.xin}{INDENT2}{ix_col = }:     {new_record.fieldName( ix_col ) = } " )

        given a QSqlTableModel how can i find the record for any given row.

        def primaryValues(…) # primaryValues(self, row: int) -> QSqlRecord
        record( ix)  according to chat === put this back in info  about
        """

        # model_subjects is just model
        model    = self.model  # QSqlTableModel
        ix_table_joined  = 3
        ix_table_id      = 5
        for ix_row in range( model.rowCount()  ):
            record = model.record(ix_row)

            for i in range(record.count()):
                msg   = ( f"Field by index {i = } {record.fieldName(i)}: {record.value(i)}")
                logging.debug( msg )
            msg   = ( f"{record.value(ix_table_joined)}) {record.value(ix_table_id)})" )
            logging.debug( msg )
            record_key    = (record.value(ix_table_joined), record.value(ix_table_id))
            msg   = ( f"{record_key = }")
            logging.debug( msg )

    # ------------------------------------------
    def get_selected_row(self):
        """
        """
        # Access the selection model
        selection_model = self.table_view.selectionModel()

        # Get the selected rows (returns a list of QModelIndex)
        selected_indexes = selection_model.selectedRows()

        if selected_indexes:
            # Example: Get the row number of the first selected row
            for index in selected_indexes:
                row = index.row()
                # Do something with the selected row
                msg       = (f"Selected row: {row}")
                logging.debug( msg )

                # Optionally, retrieve data from each selected row
                row_data = [self.model.data(self.model.index(row, col),
                            Qt.DisplayRole) for col in range(self.model.columnCount())]

                msg       = (f"get_selected_row Row data: {row_data}")
                logging.debug( msg )
        else:
            msg       = ("get_selected_row No row selected")
            logging.debug( msg )
    # ------------------------------------------
    def add_to_model( self,  photo_id, table_id, table, info   ):
        """
        this is the self.model connected to db
            it also needs to add to all topics hence we pass info as well
        photo_id, table_id, table
        !! still need to check for dups
        !! need to add to two models not just the db on
             may be able to use some code already in place ??

        what it says, read?
            get a row from the topics
            see if already in the subjects
            if not add and update
        """
        msg       = ( "add_to_model ... only partly implemented" )
        logging.error( msg )

        #QMessageBox.warning(self, "Sorry", msg )
        model        =  self.model
        row_data     = [ photo_id, table_id, table ]   # may also need info is there a place
        #rint( f"{row_data = }")
        model.addRow( row_data)

        msg       = ( "add_to_model !! now add to all topics ")
        logging.debug( msg )

    # ---------------------------
    def select_by_id( self, id_value  ):
        """
        customized from PicturSubjectSubTab 2024Dec
        """
        model           = self.model
        model_subject   = self.model_subject

        self.current_id = id_value

        model.setFilter( f"photo_id = {id_value}" )
        model.select()

        #rint( "now loop thru getting table and table id ")
        model_display   = self.model_display
        model_display.clear_data()
        row_count       = model.rowCount()
        column_count    = model.columnCount()
        ix_table_column      = 3
        ix_table_id_column   = 5
        for row in range( row_count ):
            row_data = [] # what is thiis for  -- think dead

            msg       = ( "column loop ok for debug but not needed")
            logging.debug( msg )

            for column in range(column_count):
                # Get the index for the current row and column
                index   = model.index(row, column)
                # Get the data for the current index
                data    = model.data(index)
                row_data.append( data )
                if   column == ix_table_column:     #
                    table_name = data
                elif column == ix_table_id_column:
                    table_id = data

            # as a first pass do a query for each pic
            # print(f"Row {row}: {row_data}")
            # msg     = f"{table_name = } {table_id = }"
            # print( msg )

            #rint( "clear model subject   ")
            #model_subject.clear()    # no clear_data, but chant says clear
            if   table_name == "stuff":
                info     = self.get_info_stuff( table_id  )

            if   table_name == "people":
                info     = self.get_info_people( table_id  )

            if   table_name == "plant":
                info     = self.get_info_plant( table_id  )
                #self.add_to_model_display( id_value, table_name, table_id, info )

            else:

                info    = "info tbd"
            self.add_to_model_display( id_value, table_name, table_id, info )

                # msg     = ( f"need subject processing for {table_name = }")
                # AppGlobal.logger.info( msg )
                # print( msg )
                # pass

            self.model_indexer.refresh_index()
            self.populate_model_other()

    # ------------------------------------------
    def get_info_people( self, a_id ):
        """ """
        msg       = ( "get_info_people")
        logging.debug( msg )

        sql     = """
            SELECT
                id,
                f_name,
                m_name,
                l_name,
                c_name
                FROM people
                WHERE id = :a_id
            """

        query           = QSqlQuery( self.db )

        if not query.prepare(sql):
            msg       = (f"Prepare failed: {query.lastError().text()}")
            logging.error( msg )

        else:
            query.bindValue(":a_id", a_id )

            if not query.exec_():
                msg       = (f"Execution failed: {query.lastError().text()}")
                logging.error( msg )

            else:
                rows_affected = query.numRowsAffected()
                #rint( f"Records udated successfully. {rows_affected = } ")

        while query.next():   # not needed ??
            a_id        = query.value(0)
            f_name      = query.value(1)
            m_name      = query.value(2)
            l_name      = query.value(3)
            c_name      = query.value(4)

        full_name       = f"{f_name} {m_name} {l_name}".strip()
        if full_name    == "":
            full_name   = c_name.strip()
        if full_name    == "":
            full_name   = "name ??"

        info      = full_name

        return info

    # ------------------------------------------
    def get_info_plant( self, a_id ):
        """
        sync to code in plant doc
        """
        sql     = """
            SELECT
                id,
                name,
                latin_name,
                add_kw,
                descr
                FROM plant
                WHERE id = :a_id
            """

        query           = QSqlQuery( self.db )

        if not query.prepare(sql):
            msg     = (f"Prepare failed: {query.lastError().text()}")
            logging.debug( msg )
        else:
            query.bindValue(":a_id", a_id )

            if not query.exec_():
                msg     = (f"Execution failed: {query.lastError().text()}")
                logging.debug( msg )
            else:
                rows_affected = query.numRowsAffected()
                #rint( f"Records udated successfully. {rows_affected = } ")

        while query.next():   # not needed ??
            a_id        = query.value(0)
            name        = query.value(1)
            latin_name  = query.value(2)
            add_kw      = query.value(3)
            descr       = query.value(4)

        info    = (f"{ name} {latin_name} {descr}").strip()
        if info == "":
            info = f"plant {a_id} has blank name and ...."

        return  info

    # ------------------------------------------
    def get_info_stuff( self, stuff_id ):
        """ """
        print( "get_info_stuff")
        sql     = """
            SELECT
                id,
                descr,
                name,
                add_kw
                FROM stuff
                WHERE id = :stuff_id
            """
        query           = QSqlQuery( self.db )

        if not query.prepare(sql):
            msg   = (f"Prepare failed: {query.lastError().text()}")
            logging.error( msg )
        else:
            query.bindValue(":stuff_id", stuff_id )

            if not query.exec_():
                print( f"Execution failed: {query.lastError().text()}")

            else:
                rows_affected = query.numRowsAffected()
                msg    = ( f"Records udated successfully. {rows_affected = } ")
                logging.debug( msg )

        while query.next():   # not needed ??
            a_id        = query.value(0)
            descr       = query.value(1)
            name        = query.value(2)
            add_kw      = query.value(3)

        info      = (f"ID: {a_id = }  { name = }  {descr = }  ")
        # consider check for empty, too long so far just debug
        return info

    # ------------------------------------------
    def get_info_tbd( self, a_id ):
        """ """
        return "info tbd"

    # -----------------------
    def populate_model_other( self,    ):
        """
        redo any time the topics/subjects in other window change this is a total redo
        dec 2024 -- restarting dev   2024Dec
            topic_dict[ "window_id" ] = i_window
            topic_dict[ "table"]      = i_window.detail_table_name
            topic_dict[ "table_id"]   = i_window.detail_table_id  need for dup detect
            topic_dict[ "topic"]      = i_window.topic
        """
        msg       = ( "finish populate_model_other")
        logging.error( msg )
        #return

        open_topics_list    = AppGlobal.mdi_management.open_topics    # list of dicts
        model               = self.model_other
        model.clear_data()
        for i_topic in open_topics_list:
            other_table         = i_topic[ "table" ]
            other_table_id      = i_topic[ "table_id" ]      # watch out for type info may be int
            key                 = ( other_table, other_table_id  )
            if not self.model_indexer.find( key ):  # else None
                row_data     = [ i_topic[ "table" ], str(i_topic[ "table_id" ]),  i_topic[ "topic" ] ]
                print( f"{row_data = }")
                model.addRow( row_data)
        print( "populate_model_other delete dups no add if dup !!")

    # -----------------------
    def update_dbpromotedfornow( self,    ):
        """
        for debugging

        do not need key generation on new
        model               = QSqlTableModel( self, self.db )
        model_indexer       = table_model.ModelIndexer( model )
        self.model_indexer  = model_indexer

        self.model_subject  = model

        """
        print( "update_db debugging method can it be this simple? db commit here??  ")
        model       =  self.model    # QSqlTableModel( self, self.db )
        model.submitAll()
        self.db.commit()                # maybe not here

    # -----------------------
    def topic_update( self, table, table_id,  info, ):
        """
        this is the message receiver
        """
        #print( "got topic update " )  #"{args} {kwargs}")
        msg       = ( f"got topic update {table = } {table_id = } {info = } update_subjects next not but populate_model_other")
        logging.info( msg )

        self.populate_model_other()
        #self.update_subjects( self.current_id, table, table_id,  info  )

    # -----------------------
    def update_subjects( self, photo_id, table, table_id,  info  ):
        """
        2024 dec   may have dropped this approach -- less efficient but optimize later
        for now the update could be a new or existing entry in either
        the current table or the selected_display/view
        may also just be a change in the info

        """
        INFO_COLUMN     = 2  # column where info is found in model_other....

        # exclude these tables
        if table in ( "photo", "photoshow" ):
            return

        key             = ( table, table_id )
        model_subject   = self.model_subject
        row             = self.model_indexer.find( key )

        if row is not None:
            # update this and display then done
            print( "need code to update model_subject")
            return

        model_other     = self.model_other
        indexer         = model_other.indexer
        msg    = ( f"update_subjects {str(indexer ) = }")
        logging.debug( msg )

        row             = model_other.indexer.find( key )
        if row is not None:
            print( "update_subjects update row model_other")
            an_index     = model_other.index( row, INFO_COLUMN )
            model_other.set_data_at_index(self, an_index, info, )

        else:
            print( "update_subjects add row to model_other")
            row_data     = [  table, table_id,  info,    ]
            model_other.addRow( row_data)
            model_other.indexer.set_is_valid( False )

    # ------------------------
    def inspect(self):
        """ """
        #print_func_header( "inspect" )
        # make some locals for inspection
        #the_global_db       = uft.DB_OBJECT
        # parent_window = self.parent( ).parent( ).parent().parent()
        # a_db          = parent_window.sample_db
        # model         = self.people_model
        # view          = self.people_view
        self_model                  = self.model
        self_model_indexer          = self.model_indexer

        self_model_other            = self.model_other
        self_model_other_indexer    = self.model_other.indexer
        wat_inspector.go(
             msg            = "from picture document inspect",
             a_locals       = locals(),
             a_globals      = globals(), )

    # -----------------------
    def add_to_model_display( self, photo_id, table, table_id,  info  ):
        """
        2024 looks like useful
        all_subjects is the display for the db which is self.model

        we need to add toseems to be partly implemented with no view so far -- these two models, one for display
        one for the db, this may not be complete
        also i may be mixed up on which is which
        """
        model_display     = self.model_display
        #rint( f" add_to_model_all_subjects {photo_id = } , {table = }, {table_id = },  {info =} "  )
        key           = ( table, table_id )
        key_row       = model_display.indexer.find( key )
        print( "add_to_model_all_subjects put back dup check if necessary")
        key_row       = False
        if key_row:
            #rint( f"add_to_model_all_subjects model_display found key {key = } in row {key_row}")
            pass
        else:
            # self.view_all_subjects.setModel(  self.model_all_subjects )
            # model        = self.model_display
            row_data     = [  photo_id, table,   table_id, info    ]
            #rint( f"{row_data = }")
            model_display.addRow( row_data)
            model_display.indexer.set_is_valid( False )

            #table_model.model_dump( model_display, msg = "model_display dump after else" )

        # # ---- now the model
        # print( "is this right ")
        # #rint( "begin model")
        # model         = self.model
        # model_indexer = self.model_indexer
        # key_row       = model_indexer.find( key )
        # key_row       = False
        # print( "fix key_row = False ")
        # if key_row:
        #     print( f"add_to_model_all_subjects model found key {key = } in row {key_row} no add")  # no add if already there
        # else:
        #     #rint( f"add_to_model_all_subjects model NOT found key {key = }  continue with add")
        #     # self.view_all_subjects.setModel(  self.model_all_subjects )
        #     # model        = self.model_display
        #     # key = self.keygen.get_next_key()
        #     row_index      = model.rowCount()
        #     model.insertRow( row_index  )
        #     model.setData( model.index( row_index, 0), photo_id )
        #     model.setData( model.index( row_index, 1), table_id )
        #     model.setData( model.index( row_index, 2), table    )
        #     model_indexer.set_is_valid( False )
        #     # table_model.model_dump( model, msg = f"model_display dump after insert, {row_index = } {photo_id = }" )

        # #rint( f"add_model_all_subjects done {str(model_display)} {1 = }")

# ---------------
#         id_item     = QStandardItem( str(id_data) )
#         name_item   = QStandardItem( name_data )

#         # Add a new row to the second model
#         history_model.appendRow([id_item, name_item])

#         # if not self.index:   # new row  self.index and index not the same
#         #     print( ">>>>>>>>>>>>new row AppGlobal.key_gen       = a_key_gen")
#         #     key             = AppGlobal.key_gen.get_next_key( table_name )
#         #     # row count here becomes rowcount - 1 later
#         #     model.insertRow( model.rowCount() )
#         #     ix_row               = model.rowCount() - 1   # model row that get the data here new row
#         #     # model.index makes an index row col for the data
#         #     model.setData( model.index( ix_row, 0), key )

# ---------------


    # -----------------------
    def __str__( self ):
        """
        """

        a_str   = ""
        a_str   = ">>>>>>>>>>* StuffEventSubTab  *<<<<<<<<<<<<"

        return a_str

# ----------------------------------------
class PictureAlbumtSubTab(  QWidget  ):
    """
    list albums that picture belongs to
    """

    def __init__(self, parent_window ):
        """
        shows the albums this picture is in
        """
        super().__init__()
        self.parent_window   = parent_window
        self.list_ix         = 5  # should track selected an item in detail
        # needs work
        self.db              = AppGlobal.qsql_db_access.db

        self.table_name      = "photoshow"

        #self.tab_name            = "StuffEventSubTab  not needed this is a sub tab
        self.current_id      = None
        #self.current_id      = 28
        #rint( "fix stuff event select and delete line above should be select_by_id  ")
        self._build_model()   # first so it can be used in gui
        self._build_gui()

        self.parent_window.sub_tab_list.append( self )    # a function might be better

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says, read
        """
        page            = self
        tab             = page

        layout                     = QVBoxLayout( tab )
        button_layout              = QHBoxLayout()

        layout.addLayout( button_layout )

        view                 = QTableView()
        self.view            = view
        view.setModel( self.model )

        layout.addWidget( view )

    # ---------------------------------
    def _build_model( self, ):
        """
        may have too many instances
        Returns:
            modifies self, establishes -- wrong names

        SELECT

        photoshow.name,
        photoshow.id,

        photoshow_photo.photo_id,

        photoshow_photo.seq_no,
        photoshow_photo.photoshow_id


        FROM   photoshow
        JOIN   photoshow_photo  ON   photoshow_photo.photoshow_id  = photoshow.id

        WHERE  photoshow_photo.photo_id = 29 ;


        """
        #model              = QSqlTableModel( self, self.db )
        model              = qt_with_logging.QSqlRelationalTableModelWithLogging(  self, self.db    )
        self.model         = model

        model.setTable( self.table_name )

        model.setEditStrategy( QSqlTableModel.OnManualSubmit )
        # model_write.setEditStrategy( QSqlTableModel.OnFieldChange )

        ix_foreign_key        = 0         # key to   position in table
        foreign_table         = "photoshow_photo"
        foreign_table_key     = "photoshow_id"      # key joining

        print( "_build_model see if there is a relation object" )
        self.model.setRelation( ix_foreign_key, QSqlRelation( foreign_table,
                                foreign_table_key,
                                "id"  ))

    # ---------------------------------------
    def select_by_id( self, id ):
        """
        the usual, read
        """
        msg    = ( "select_by_id PictureAlbumtSubTab  ")
        AppGlobal.logger.info( msg )
        print( msg )
        model           = self.model

        # self.current_id  = id
        model.setFilter( f"photoshow_photo.photo_id = {id}" )
        # # model_write.setFilter( f"pictureshow_id = {id} " )
        model.select()

    # ------------------------------------------
    def delete_all(self):
        """
        what it says, read?

        set current id, get children
        """
        msg   = "PictureAlbumSubTab  delete_all ... not implemented yet "
        QMessageBox.warning(self, "Sorry", msg )

    # -------------------------------------
    def i_am_hsw(self):
        """
        make sure call is to here
        """
        print( "i_am_hsw")

    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = ">>>>>>>>>>* xxx *<<<<<<<<<<<<"

        return a_str

# ----------------------------------------
class PictureHistorylTab( base_document_tabs.HistoryTabBase   ):
    """
    new version -- to QTableWidget
    may change ancestor ??
    """
    def __init__(self, parent_window ):
        """
        what it says read -- the usual -- but ancestor matters

        """
        super().__init__( parent_window )
        self.tab_name            = "PictureHistorylTab"



# ---- eof ------------------------------
