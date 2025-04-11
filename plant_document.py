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
    main.main()
# --------------------

import functools
import logging
import sqlite3
import time

import gui_qt_ext
import string_util
from app_global import AppGlobal

# ---- QtCore
from PyQt5.QtCore import QDate, QModelIndex, QRectF, Qt, QTimer, pyqtSlot
from PyQt5.QtGui import (QIntValidator,
                         QPainter,
                         QPixmap,
                         QStandardItem,
                         QStandardItemModel)

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
                             QTableView,
                             QTableWidget,
                             QTableWidgetItem,
                             QTabWidget,
                             QTextEdit,
                             QVBoxLayout,
                             QWidget)

# ---- imports local

import base_document_tabs
import custom_widgets as cw
import key_words
import mdi_management
import qt_sql_query
import qt_with_logging
import combo_dict_ext
#import plant_document_edit


logger          = logging.getLogger( )
LOG_LEVEL       = 20 # level form much debug    higher is more debugging    logging.log( LOG_LEVEL,  debug_msg, )
        # logging.log( LOG_LEVEL,  debug_msg, )

# ------------------------------------
class PlantingtSqlTableModel( QSqlTableModel ):
    def __init__(self, parent=None, db=QSqlDatabase()):
        """
        think chat had me do this to make non editable
        but just a QSqlQuery with the triggers off might
        be a better solution

        """
        super().__init__(parent, db)
        # Specify multiple columns to make non-editable (e.g., columns 1 and 2)
        self.non_editable_columns = {0, 1, }  # Columns ..doe it have to be in init or is synamic ..

    def flags(self, index: QModelIndex):
        """ """

        # Get default flags from the base class
        flags = super().flags(index)
        # Remove editable flag for the specified columns
        if index.column() in self.non_editable_columns:
            return flags & ~Qt.ItemIsEditable  # Make these columns non-editable
        return flags

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        """ """
        # Handle text alignment for specific columns (optional)
        if role == Qt.TextAlignmentRole:
            if index.column() == 0:  # Left-align column 0
                return Qt.AlignLeft | Qt.AlignVCenter
            elif index.column() == 1:  # Center-align column 1
                return Qt.AlignCenter | Qt.AlignVCenter
            elif index.column() == 2:  # Right-align column 2
                return Qt.AlignRight | Qt.AlignVCenter
        # Default to base class implementation for other roles
        return super().data(index, role)

# ----------------------------------------
class PlantDocument( base_document_tabs.DocumentBase ):
    """
    for the plant table....
    """
    def __init__(self, ):
        """
        the usual
        """
        super().__init__()


        self.detail_table_name  = "plant"
        self.text_table_name    = "plant_text"  # text tables always id and text_data
        self.subwindow_name     = "Plant Document"

        self.setWindowTitle( self.subwindow_name )
        self._build_gui()

    # --------------------------------
    def get_topic( self ):
        """
        this version seems promotable
        of the detail record -- now info
        see picture get plant info....
        """
        info   = self.detail_tab.data_manager.get_topic_string()
        return info

    # --------------------------------
    def get_topic_old( self ):
        """
        of the detail record -- now info
        see picture get plant info....
        """
        # topic     = "plant topic "
        # if self.record_state:
        #     topic    = f"{topic} {self.record_state = }"
        # topic    = f"{topic} {self.detail_tab.name_field.text()}"

        # return   topic
        # info     = "get_topic plant need to fix record state  "
        # return info
        record_state    = self.detail_tab.data_manager.record_state
        # probably in data manager
        if record_state:  # else no record
            a_id        = self.detail_tab.id_field.get_raw_data()
            name        = self.detail_tab.name_field.get_raw_data()
            descr       = self.detail_tab.descr_field.get_raw_data()
            latin_name  = self.detail_tab.latin_name_field.get_raw_data()
            add_kw      = self.detail_tab.add_kw_field.get_raw_data()

            #topic    = f"{topic} {self.record_state = }"
            #topic     = f"{topic} {self.detail_tab.name_field.text() = }"
            #info      = (f"{name} {latin_name} {descr = }  ") #!! this is a debug format
            info    = (f"{ name} {latin_name} {descr}").strip()

            if info == "":
                info = f"plant {a_id} has blank name and ...."

        else:
            # maybe an error
            info   = "null record in plant document "

        return  info

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says
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
        self.criteria_tab         = PlantCriteriaTab( self )
        main_notebook.addTab(       self.criteria_tab, "Criteria" )

        ix                       += 1
        self.list_tab_index      = ix
        self.list_tab            = PlantListTab( self  )
        main_notebook.addTab(  self.list_tab, "List"    )

        ix                       += 1
        self.detail_tab_index     = ix
        self.detail_tab           = PlantDetailTab( self )
        main_notebook.addTab( self.detail_tab, "Detail"     )

        ix                       += 1
        self.picture_tab_index     = ix
        self.picture_tab           = base_document_tabs.StuffdbPictureTab( self )

        main_notebook.addTab( self.picture_tab, "Picture"     )

        ix                         += 1
        self.text_tab_index         = ix
        self.text_tab               = PlantTextTab( self )
        main_notebook.addTab( self.text_tab, "Text"     )

        ix                        += 1
        self.history_tab_index     = ix
        self.history_tab           = PlantHistorylTab( self )
        main_notebook.addTab( self.history_tab, "History"    )

        sub_window.setWidget( main_notebook )
        mdi_area.addSubWindow( sub_window )

        sub_window.show()

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
        print( f"Clicked on row {row}, column {column}, value tbd" )

    # ---- sub window interactions ---------------------------------------
    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = ">>>>>>>>>>* plantSubWindow  *<<<<<<<<<<<<"

        return a_str

# ----------------------------------------
class PlantCriteriaTab( base_document_tabs.CriteriaTabBase, ):
    """
    criteria for list selection
    """
    def __init__(self, parent_window ):
        """
        the usual

        """
        super().__init__( parent_window )
        self.tab_name   = "PlantCriteriaTab"

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

        # ----name
        widget                = QLabel( "Name" )
        grid_layout.new_row()
        grid_layout.addWidget( widget )

        widget                  = cw.CQLineEdit(
                                                 field_name = "name"   )
        self.critera_widget_list.append( widget )
        widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        grid_layout.addWidget( widget, )

        # ----latin_name
        widget                = QLabel( "latin_name" )
        grid_layout.new_row()
        grid_layout.addWidget( widget )

        widget                  = cw.CQLineEdit(
                                                 field_name = "latin_name"   )
        self.critera_widget_list.append( widget )
        widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        grid_layout.addWidget( widget,  )

        # ----key words
        widget                = QLabel( "Key Words" )
        grid_layout.new_row()
        grid_layout.addWidget( widget )

        widget                  = cw.CQLineEdit(
                                                 field_name = "key_words"   )
        self.key_words_widget   = widget  # is needed for paste
        self.critera_widget_list.append( widget )
        widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        grid_layout.addWidget( widget, columnspan = 3 )

        # ---- Order by
        grid_layout.new_row()
        widget  = QLabel( "Order by" )
        grid_layout.addWidget( widget )

        widget                 = cw.CQComboBox(
                                                 field_name = "order_by"   )
        self.critera_widget_list.append( widget )
        widget.addItem('name')
        widget.addItem('latin_name')
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

        widget.currentIndexChanged.connect( lambda: self.criteria_changed(  True   ) )
        grid_layout.addWidget( widget )

        debug_msg = ( "build_tab build criteria change put in as marker ")
        logging.debug( debug_msg )
        widget.currentIndexChanged.connect( lambda: self.criteria_changed(  True   ) )
        grid_layout.addWidget( widget )

        # ---- criteria changed should be in parent
        grid_layout.new_row()
        widget  = QLabel( "criteria_changed_widget" )
        self.criteria_changed_widget  = widget
        grid_layout.addWidget( widget )

        # # ---- push controls up page, may need adjuxtment
        # width    = 350
        # widget   = QSpacerItem( width, 310, QSizePolicy.Expanding, QSizePolicy.Minimum )
        # grid_layout.new_row()
        # # grid_layout.addWidget( widget )
        # grid_layout.addItem( widget, grid_layout.ix_row, grid_layout.ix_col )

        # ---- function_on_return( self )
        for i_widget in self.critera_widget_list:
            i_widget.function_on_return   = self.criteria_select

    # ------------------------------------------
    def _build_tab_old_almost( self, ):
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

        # ----name
        widget                = QLabel( "Name" )
        grid_layout.new_row()
        grid_layout.addWidget( widget )

        widget                  = cw.CQLineEdit(
                                                 field_name = "name"   )
        self.critera_widget_list.append( widget )
        widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        grid_layout.addWidget( widget, )

        # ----latin_name
        widget                = QLabel( "latin_name" )
        grid_layout.new_row()
        grid_layout.addWidget( widget )

        widget                  = cw.CQLineEdit(
                                                 field_name = "latin_name"   )
        self.critera_widget_list.append( widget )
        widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        grid_layout.addWidget( widget,  )

        # ----key words
        widget                = QLabel( "Key Words" )
        grid_layout.new_row()
        grid_layout.addWidget( widget )

        widget                  = cw.CQLineEdit(
                                                 field_name = "key_words"   )
        self.key_words_widget   = widget  # is needed for paste
        self.critera_widget_list.append( widget )
        widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        grid_layout.addWidget( widget, columnspan = 3 )

        # ---- Order by
        grid_layout.new_row()
        widget  = QLabel( "Order by" )
        grid_layout.addWidget( widget )

        widget                 = cw.CQComboBox(
                                                 field_name = "order_by"   )
        self.critera_widget_list.append( widget )
        widget.addItem('name')
        widget.addItem('latin_name')
        # widget.addItem('Title??')

        print( "build_tab build criteria change put in as marker ")
        widget.currentIndexChanged.connect( lambda: self.criteria_changed(  True   ) )
        grid_layout.addWidget( widget )

        # ---- criteria changed should be in parent
        grid_layout.new_row()
        widget  = QLabel( "criteria_changed_widget" )
        self.criteria_changed_widget  = widget
        grid_layout.addWidget( widget )

        # ---- push controls up page, may need adjuxtment
        width    = 350
        widget   = QSpacerItem( width, 310, QSizePolicy.Expanding, QSizePolicy.Minimum )
        grid_layout.new_row()
        # grid_layout.addWidget( widget )
        grid_layout.addItem( widget, grid_layout.ix_row, grid_layout.ix_col )

        # ---- function_on_return( self )
        for i_widget in self.critera_widget_list:
            i_widget.function_on_return   = self.criteria_select

    # -------------
    def criteria_select( self,     ):
        """
        from help   mod in process -- at least some works

        """
        parent_document                 = self.parent_window

        model                           = parent_document.list_tab.list_model

        query                           = QSqlQuery()
        query_builder                   = qt_sql_query.QueryBuilder( query, print_it = False, )

        kw_table_name                   = "plant_key_words"
        column_list                     = [ "id", "id_old", "name", "latin_name", "add_kw", ]
            # might be able to get from data dict, perhaps even at startup

        a_key_word_processor            = key_words.KeyWords( kw_table_name, AppGlobal.qsql_db_access.db )
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
            query_builder.sql_inner_join    = " plant_key_word  ON plant.id = plant_key_word.id "
            query_builder.sql_having        = f" count(*) = {key_word_count} "

            query_builder.add_to_where( f" key_word IN {criteria_key_words}" , [] )

        # ---- name like
        name                          = criteria_dict[ "name" ].strip().lower()
        if name:
            add_where       = "lower( name )  like :name"   # :is name of bind var below
            query_builder.add_to_where( add_where, [(  ":name",
                                                     f"%{name}%" ) ])

        # ---- name like
        latin_name                          = criteria_dict[ "latin_name" ].strip().lower()
        if name:
            add_where       = "lower( latin_name )  like :latin_name"   # :is name of bind var below
            query_builder.add_to_where( add_where, [(  ":latin_name",
                                                     f"%{latin_name}%" ) ])

        # ---- order by
        order_by   = criteria_dict[ "order_by" ]

        if   order_by == "name":
            column_name = "name"
        elif order_by == "latin_name":
            column_name = "latin_name"
        else:   # !! might better handle this
            column_name = "name"

        query_builder.add_to_order_by(    column_name, "ASC",   )

        query_builder.prepare_and_bind()

        msg      = f"{query_builder = }"
        logging.log( LOG_LEVEL,  msg, )

        is_ok  = AppGlobal.qsql_db_access.query_exec_model( query,
                                                  model,
                                                  msg = "HelpSubWindow criteria_select" )

        msg      = (  query.executedQuery()   )
        logging.log( LOG_LEVEL,  msg, )

        parent_document.main_notebook.setCurrentIndex( parent_document.list_tab_index )
        self.critera_is_changed = False

# ----------------------------------------
class PlantListTab( base_document_tabs.ListTabBase   ):

    def __init__(self, parent_window ):

        super().__init__( parent_window )

        self.list_ix            = 5  # should track selected an item in detail

        self.tab_name           = "PlantListTab"

        self._build_gui()

# ----------------------------------------
class PlantDetailTab( base_document_tabs.DetailTabBase  ):
    """
    """
    def __init__(self, parent_window  ):
        """
        Args:
            parent_window (TYPE): DESCRIPTION.

        """
        super().__init__( parent_window )

        self.tab_name                       = "PlantDetailTab"
        self.enable_send_topic_update       = True
        self.key_word_table_name            = "plant_key_word"
        self.post_init()

    # -------------------------------------
    def _build_gui( self ):
        """
        modeled on picture
        """
        page            = self

        max_col         = 12
        self.max_col    = max_col

        box_layout_1    = QVBoxLayout( page )

        # !! change name
        placer          = gui_qt_ext.CQGridLayout( col_max = max_col )

        tab_layout      = placer
        box_layout_1.addLayout( placer )

        # ----fields
        self._build_fields( placer )

        # ---- tab area
        # ---------------
        tab_folder   = QTabWidget()
        # tab_folder.setTabPosition(QTabWidget.West)

        tab_folder.setMovable(True)
        tab_layout.new_row()
        tab_layout.addWidget( tab_folder, columnspan   = max_col )

        # sub_tab      = PlantEventSubTab( self )
        # self.event_sub_tab   = sub_tab
        # tab_folder.addTab( sub_tab, "Events" )

        # ---- PictureListSubTab
        sub_tab      = PictureListSubTab( self )
        # self.pictures_tab   = sub_tab
        self.picture_sub_tab    = sub_tab
        self.sub_tab_list.append( sub_tab )
        tab_folder.addTab( sub_tab, "Pictures" )

        # ---- PlantPlantingSubTab
        sub_tab      = PlantPlantingSubTab( self )
        # self.pictures_tab   = sub_tab
        self.planting_sub_tab    = sub_tab
        self.sub_tab_list.append( sub_tab )
        tab_folder.addTab( sub_tab, "Plantings" )

        # Main notebook
        detail_notebook           = QTabWidget()
        self.detail_notebook      = detail_notebook

        # # ---- buttons
        # button_layout = QHBoxLayout()

        # create_button = QPushButton("Create Default")
        # create_button.clicked.connect( self.create_default_row )
        # button_layout.addWidget(create_button)

        # button = QPushButton( "To History" )
        # print( "need detail_to_history")
        # button.clicked.connect( self.parent_window.detail_to_history )
        # button_layout.addWidget(update_button)

        #tab_layout.addLayout( button_layout )

    #---------------------------------
    def _build_fields( self, layout ):
        """
        What it says, read
            this is generated code
            tweaks
                spacing
                plnat_combo_dict look for code
        """
        width  = 50
        for ix in range( self.max_col ):  # try to tweak size to make it work
            widget   = QSpacerItem( width, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
            layout.addItem( widget, 0, ix  )  # row column

        self.plant_combo_dict_ext    = combo_dict_ext.PLANT_COMBO_DICT_EXT
            # see main window
        # ---- code_gen: TableDict.to_build_form 2025_04_01 for plant -- begin table entries -----------------------

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

        # ---- latin_name
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "latin_name", )
        self.latin_name_field     = edit_field
        edit_field.is_keep_prior_enabled        = True
        edit_field.setPlaceholderText( "latin_name" )
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 4 )

        # ---- descr
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "descr", )
        self.descr_field     = edit_field
        edit_field.setPlaceholderText( "descr" )
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
        edit_field.is_keep_prior_enabled        = True
        edit_field.setPlaceholderText( "add_kw" )
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 4 )

        # ---- plant_type
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "plant_type", )
        self.plant_type_field     = edit_field
        edit_field.setPlaceholderText( "plant_type" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- type_sub
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "type_sub", )
        self.type_sub_field     = edit_field
        edit_field.setPlaceholderText( "type_sub" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- life
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "life", )
        self.life_field     = edit_field
        edit_field.setPlaceholderText( "life" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- water
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "water", )
        self.water_field     = edit_field
        edit_field.setPlaceholderText( "water" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- sun_min
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "sun_min", )
        self.sun_min_field     = edit_field
        edit_field.setPlaceholderText( "sun_min" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- sun_max
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "sun_max", )
        self.sun_max_field     = edit_field
        edit_field.setPlaceholderText( "sun_max" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- zone_min
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "zone_min", )
        self.zone_min_field     = edit_field
        edit_field.setPlaceholderText( "zone_min" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- zone_max
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "zone_max", )
        self.zone_max_field     = edit_field
        edit_field.setPlaceholderText( "zone_max" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- height
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "height", )
        self.height_field     = edit_field
        edit_field.setPlaceholderText( "height" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- form
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "form", )
        self.form_field     = edit_field
        edit_field.setPlaceholderText( "form" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- color
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "color", )
        self.color_field     = edit_field
        edit_field.setPlaceholderText( "color" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- pref_unit
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "pref_unit", )
        self.pref_unit_field     = edit_field
        edit_field.setPlaceholderText( "pref_unit" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- hybridizer
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "hybridizer", )
        self.hybridizer_field     = edit_field
        edit_field.setPlaceholderText( "hybridizer" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- hybridizer_year
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "hybridizer_year", )
        self.hybridizer_year_field     = edit_field
        edit_field.setPlaceholderText( "hybridizer_year" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- color2
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "color2", )
        self.color2_field     = edit_field
        edit_field.setPlaceholderText( "color2" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- color3
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "color3", )
        self.color3_field     = edit_field
        edit_field.setPlaceholderText( "color3" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- life2
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "life2", )
        self.life2_field     = edit_field
        edit_field.setPlaceholderText( "life2" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- tag1
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "tag1", )
        self.tag1_field     = edit_field
        edit_field.setPlaceholderText( "tag1" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- chromosome
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "chromosome", )
        self.chromosome_field     = edit_field
        edit_field.setPlaceholderText( "chromosome" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- bloom_time
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "bloom_time", )
        self.bloom_time_field     = edit_field
        edit_field.setPlaceholderText( "bloom_time" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- bloom_dia
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "bloom_dia", )
        self.bloom_dia_field     = edit_field
        edit_field.setPlaceholderText( "bloom_dia" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- fragrance
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "fragrance", )
        self.fragrance_field     = edit_field
        edit_field.setPlaceholderText( "fragrance" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- rebloom
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "rebloom", )
        self.rebloom_field     = edit_field
        edit_field.setPlaceholderText( "rebloom" )
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

        # ---- extended
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "extended", )
        self.extended_field     = edit_field
        edit_field.setPlaceholderText( "extended" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- plant_class
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "plant_class", )
        self.plant_class_field     = edit_field
        edit_field.setPlaceholderText( "plant_class" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- source_type
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "source_type", )
        self.source_type_field     = edit_field
        edit_field.setPlaceholderText( "source_type" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- source_detail
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "source_detail", )
        self.source_detail_field     = edit_field
        edit_field.setPlaceholderText( "source_detail" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- spider
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "spider", )
        self.spider_field     = edit_field
        edit_field.setPlaceholderText( "spider" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- spider_ratio
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "spider_ratio", )
        self.spider_ratio_field     = edit_field
        edit_field.setPlaceholderText( "spider_ratio" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- double
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "double", )
        self.double_field     = edit_field
        edit_field.setPlaceholderText( "double" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )



    # ---------------------------
    def select_record( self, id_value  ):
        """
        extension for read it
        """
        super().select_record( id_value )
        # this next should be gathered from the record
        # self.plant_combo_dict_ext.get_info_for_id_if( id_value )

        # see if this works, no select
        self.plant_combo_dict_ext.get_info_from_record(
                        self.data_manager.current_id,
                        self.data_manager.current_record  )

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
        #rint( f"PlantDocumentDetaiTab fetch_row { id=}")
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
        #!! this may all be wrong
        # ---- capture needed fields
        descr      = self.descr_field.text()
        add_kw     = self.add_kw_field.text()
        # print(  ia_qt.q_line_edit( self.name_field,
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
        pass

    # ------------------------
    def get_picture_file_name(self):
        """
        some promotable -- but picture is special only one file, rest
        work differently
        see picture document

        return file_name or None if no file name
        """
        msg   = ( "get_picture_file_name to be implemented" )
        logging.debug( msg )

        return ""  # none will cause exception  , just need file name that does not exist

# ==================================
class PlantTextTab( base_document_tabs.TextTabBase  ):
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
        super().__init__( parent_window )
        self.tab_name           = "PlantTextTab"
        # for a text tab the table will be set incorrectly
        self.table              = "plant_text"
        self.table_name         = self.table   # !! eliminate one or other

        self.post_init()

# ----------------------------------------
class PlantHistorylTab( base_document_tabs.HistoryTabBase   ):
    """ """
    def __init__(self, parent_window ):
        """
        """
        super().__init__( parent_window )
        self.tab_name            = "PlantHistorylTab"

# ----------------------------------------
class PlantEventSubTab( base_document_tabs.SubTabBaseOld  ):
    """
    """
    def __init__(self, parent_window ):
        """
        """
        super().__init__( parent_window )

        self.list_ix         = 5  # should track selected an item in detail
        # needs work
        self.db              = AppGlobal.qsql_db_access.db

        self.table_name      = "plant_event"
        self.list_table_name = self.table_name   # delete this
        #self.tab_name            = "PlantEventSubTab  not needed this is a sub tab
        self.current_id      = None

        self._build_model()
        self._build_gui()

        self.parent_window.sub_tab_list.append( self )    # a function might be better

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says, read
        !! initial query should come out

        """
        page                = self

        layout              = QVBoxLayout( page )
        button_layout       = QHBoxLayout()

        layout.addLayout( button_layout )

        # Set up the view
        view                 = QTableView()
        self.list_view       = view
        self.view            = view

        view.setModel( self.model_write )

        layout.addWidget( view )
        #placer.place(  view )

        # ---- buttons
        widget        = QPushButton( 'add_record' )
        #add_button    = widget
        widget.clicked.connect( self.add_record )
        button_layout.addWidget( widget )

        #
        widget        = QPushButton('edit_record')
        #add_button    = widget
        widget.clicked.connect(self.edit_record)
        button_layout.addWidget( widget )

        #
        widget        = QPushButton('delete_record')
        #add_button    = widget
        widget.clicked.connect(self.delete_record)
        button_layout.addWidget( widget )

    # ---------------------------------
    def _build_model( self, ):
        """
        may have too many instances
        Returns:
            modifies self, establishes -- wrong names

        """
        model              = qt_with_logging.QSqlTableModelWithLogging(  self, self.db    )

        self.model_write   = model
        self.model         = model

        model.setTable( self.list_table_name )
        model.setEditStrategy( QSqlTableModel.OnManualSubmit )
        # model_write.setEditStrategy( QSqlTableModel.OnFieldChange )
        model.setFilter( "-99" )   # just in case we get a select too soon

    # ------------------------------------------
    def select_all_for_test( self, ):
        """
        what it says, read

        """
        query_ok   = self.model_write.select()

        msg        = f"{ query_ok = }"
        # rint( msg )
        AppGlobal.logger.debug( msg )

        # AppGlobal.yt_db.error_info( self.channel_model.lastError() )
        # AppGlobal.plant_db_db.error_info( model.lastError() )
        # ia_qt.q_sql_error( self.model_write.lastError(),
        #                    msg="now in code at:select_all_for_test")

        if not query_ok:
            msg     = f"select_all_for_test not query_ok {query_ok} "  # "{AppGlobal.stuff_db_db}"
            logging.error( msg )

            print( " next 1/0    ", flush=True)
            1 / 0

        self.list_view.resizeColumnsToContents()

    # ---------------------------------------
    def select_by_id( self, id ):
        """
        maybe make ancestor and promote

        Returns:
            None.

        """
        # ---- write
        model           = self.model_write

        self.current_id  = id   # may not be used but keep in case
        model.setFilter( f"plant_id = {id}" )
        model.select()

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

        """
        next_key      = AppGlobal.key_gen.get_next_key(
            self.detail_table_name )
        self.detail_tab.default_new_row( next_key )
        self.text_tab.default_new_row(   next_key )

    # ------------------------------------------
    def add_record(self):
        """
        what it says, read?
        add test for success an refactor??
        """
        model      = self.model_write
        dialog     = plant_document_edit.EditPlantEvents( model, index = None, parent = self )
        if dialog.exec_() == QDialog.Accepted:
            #self.model.submitAll()
            ok     = base_document_tabs.model_submit_all(
                       model,  f"PlantEventsSubTab.add_record " )
            self.model.select()

    # ------------------------------------------
    def edit_record(self):
        """
        what it says, read?
        """
        index       = self.view.currentIndex()
        model       = self.model
        if index.isValid():
            dialog = plant_document_edit.EditPlantEvents( self.model, index, parent = self )
            if dialog.exec_() == QDialog.Accepted:
                #self.model.submitAll()
                ok     = base_document_tabs.model_submit_all(
                           model,  f"PlantEventsSubTab.add_record " )
                #ia_qt.q_sql_table_model( self.model, "post edit_record submitAll()" )
                self.model.select()
        else:
            msg   = "Click on row to edit..."
            QMessageBox.warning(self, "Please", msg )

    # ------------------------------------------
    def delete_record(self):
        """
        what it says, read?

        set current id, get children
        """
        msg   = "delete_record ... not implemented"
        QMessageBox.warning(self, "Sorry", msg )

    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = ">>>>>>>>>>* PlantEventSubTab  *<<<<<<<<<<<<"

        return a_str

# ----------------------------------------
class PlantPlantingSubTab( base_document_tabs.SubTabBaseOld  ):

    def __init__(self, parent_window ):
        """
        this is a read only sub tab
        PlantingtSqlTableModel( QSqlTableModel ):
        QTableView
        would this be better with just a QSqlQuery

        """
        super().__init__( parent_window )

        self.table_name      = "planting"
        self.list_table_name = self.table_name   # delete this
        self.tab_name        = "PlantPlantingSubTab"

        self._build_model()
        self._build_gui()

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says, read
        """
        page                = self

        layout              = QVBoxLayout( page )
        button_layout       = QHBoxLayout()

        layout.addLayout( button_layout )

        # model.setHeaderData( 0, Qt.Horizontal, "ID")
        # model.setHeaderData( 1, Qt.Horizontal, "YT ID"  )

        # Set up the view
        view                 = QTableView()
        model                = self.model
        #self.list_view       = view
        self.view            = view
        view.setModel( self.model )

        view.setEditTriggers(QTableView.NoEditTriggers)  # Disable all edit triggers make non-edit
        view.setSelectionBehavior( QTableView.SelectRows )

        ix_col = -1   # could make loop or even list comp

        # ix_col += 1
        # model.setHeaderData( ix_col, Qt.Horizontal, "ID" )
        # view.setColumnWidth( ix_col, 100)  # Set  width in  pixels

        # ix_col += 1
        # model.setHeaderData( ix_col, Qt.Horizontal, "Stuff ID" )
        # view.setColumnWidth( ix_col, 100)  # Set  width in  pixels

        # ix_col += 1
        # model.setHeaderData( ix_col, Qt.Horizontal, "Date" )
        # view.setColumnWidth( ix_col, 100)  # Set  width in  pixels

        # ix_col += 1
        # model.setHeaderData( ix_col, Qt.Horizontal, "$ Amount" )
        # view.setColumnWidth( ix_col, 100)  # Set  width in  pixels

        # ix_col += 1
        # model.setHeaderData( ix_col, Qt.Horizontal, "Comment" )
        # view.setColumnWidth( ix_col, 300)  # Set  width in  pixels

        # ix_col += 1
        # model.setHeaderData( ix_col, Qt.Horizontal, "Type" )
        # view.setColumnWidth( ix_col, 100)  # Set  width in  pixels

        # view.setColumnHidden( 1, True )  # view or model

        # might want a loop for this
        # seems to be only after set model
        # STUFF_ID_COL    = 1
        # view.hideColumn( STUFF_ID_COL )

        layout.addWidget( view )

        # ---- buttons gone
        # widget        = QPushButton( 'Add' )
        # #add_button    = widget
        # widget.clicked.connect( self.add_new_event )
        # button_layout.addWidget( widget )

        # #
        # widget        = QPushButton('Edit')
        # #add_button    = widget
        # widget.clicked.connect(self.edit_selected_event )
        # button_layout.addWidget( widget )

        # #
        # widget        = QPushButton('Delete')
        # #add_button    = widget
        # widget.clicked.connect(self.delete_record)
        # button_layout.addWidget( widget )

    # ---------------------------------
    def _build_model( self, ):
        """

        """
        #model              = qt_with_logging.QSqlTableModelWithLogging(  self, self.db    )
        model              = PlantingtSqlTableModel(  self, self.db    )
        #model              = QSqlTableModel(  self, self.db    )
        self.model         = model

        model.setTable( self.list_table_name )
        model.setEditStrategy( QSqlTableModel.OnManualSubmit )
        #model.non_editable_columns = {0, 1, }  # really only work on custom model

    # ---------------------------------------
    def select_by_id( self, a_id ):
        """
        maybe make anscestor and promote but filter need name of key field

        """
        # ---- write
        model               = self.model

        self.current_id     = a_id
        model.setFilter( f"plant_id = {a_id}" )  #
        # model_write.setFilter( f"pictureshow_id = {id} " )
        model.select()

        debug_msg    = ( f"plant_planting subtab select_by_id do we need next  {a_id =}" )
        logging.debug( debug_msg )

    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = "\n>>>>>>>>>>* PlantPlantingSubTab  *<<<<<<<<<<<<"

        return a_str

# ------------------------------------
class PictureListSubTab( base_document_tabs.PictureListSubTabBase ):
    """
    almost all promoted even this may not be necessary
    """
    def __init__(self, parent_window ):
        super().__init__( parent_window )
        self.pictures_for_table  = "plant"
        # perhaps call first ??
        # self.list_table_name = "photoshow_photo"
        # self.table_name      = self.list_table_name # -- clean up


# ---- eof ------------------------------
