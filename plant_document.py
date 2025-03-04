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

# --------------------

import functools
import sqlite3
import time


from PyQt5.QtCore import QDate, QModelIndex, Qt, QTimer, pyqtSlot
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt5.QtWidgets import (QAction,
                             QActionGroup,
                             QApplication,
                             QButtonGroup,
                             QDateEdit,
                             QDockWidget,
                             QLabel,
                             QLineEdit,
                             QListWidget,
                             QMainWindow,
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
                             QWidget)

import base_document_tabs
#import document_maker
import qt_sql_query
import gui_qt_ext
import string_util
from app_global import AppGlobal


# ---- begin pyqt from import_qt.py

#from   functools import partial
#import collections
import functools
import sqlite3
import time

#from pubsub import pub
# ---- QtCore
from PyQt5.QtCore import QDate, QModelIndex, QRectF, Qt, QTimer, pyqtSlot
from PyQt5.QtGui import (QIntValidator,
                         QPainter,
                         QPixmap,
                         QStandardItem,
                         QStandardItemModel)
# ---- QtSql
from PyQt5.QtSql import (QSqlDatabase,
                         QSqlQuery,
                         QSqlQueryModel,
                         QSqlRelation,
                         QSqlRelationalDelegate,
                         QSqlRelationalTableModel,
                         QSqlTableModel)
# ---- not in standard imports
# ----QtWidgets Boxes, Dialogs
# ----QtWidgets layouts
# ----QtWidgets big
# ----QtWidgets
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
                             QSpinBox,
                             QTableView,
                             QTableWidget,
                             QTableWidgetItem,
                             QTabWidget,
                             QTextEdit,
                             QVBoxLayout,
                             QWidget)

import logging
# ---- imports local
#import  document_maker
import base_document_tabs
import custom_widgets
import key_words
import mdi_management
import qt_sql_query
#import  plant_document_edit
import qt_with_logging


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

        # mdi_area                = AppGlobal.main_window.mdi_area
        # # we could return the subwindow for parent to adds
        # sub_window              = self
        # # sub_window.setWindowTitle( "this title may be replaced " )
        # self.db                 = AppGlobal.qsql_db_access.db

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
        record_state   =          self.detail_tab.data_manager.record_state
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
        tab             = page

        placer          = gui_qt_ext.PlaceInGrid(
            central_widget=page,
            a_max=0,
            by_rows=False  )

        self._build_top_widgets(  placer )

        # ----name
        widget                = QLabel( "name" )
        placer.new_row()
        placer.place( widget )

        widget                  = custom_widgets.CQLineEditCriteria( get_type = "string", set_type = "string")
        self.key_words_widget   = widget
        self.critera_widget_list.append( widget )
        widget.critera_name    = "name"
        widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        placer.place( widget, columnspan = 3 )

        # ----latin_name
        widget                = QLabel( "latin_name" )
        placer.new_row()
        placer.place( widget )

        widget                  = custom_widgets.CQLineEditCriteria( get_type = "string", set_type = "string")
        self.key_words_widget   = widget
        self.critera_widget_list.append( widget )
        widget.critera_name    = "latin_name"
        widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        placer.place( widget, columnspan = 3 )

        # ----key words
        widget                = QLabel( "Key Words" )
        placer.new_row()
        placer.place( widget )

        widget                  = custom_widgets.CQLineEditCriteria( get_type = "string", set_type = "string")
        self.key_words_widget   = widget
        self.critera_widget_list.append( widget )
        widget.critera_name    = "key_words"
        widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        placer.place( widget, columnspan = 3 )

        # ---- Order by
        placer.new_row()
        widget  = QLabel( "Order by" )
        placer.place( widget )

        widget                 = custom_widgets.CQComboBoxEditCriteria( get_type = "string", set_type = "string")
        self.order_by_widget   = widget
        self.critera_widget_list.append( widget )
        widget.critera_name    = "order_by"

        widget.addItem('name')
        widget.addItem('latin_name')
        # widget.addItem('Title??')

        print( "build_tab build criteria change put in as marker ")
        widget.currentIndexChanged.connect( lambda: self.criteria_changed(  True   ) )
        placer.place( widget )

        # ---- criteria changed should be in parent
        placer.new_row()
        widget  = QLabel( "criteria_changed_widget" )
        self.criteria_changed_widget  = widget
        placer.place( widget )


        self.add_buttons( placer )

    # -------------
    def criteria_select( self,     ):
        """
        from help   mod in process -- at least some works

        """
        print( "criteria_select  >>>>>>>>>>>>>>>>>>>>>> " )

        parent_document                 = self.parent_window

        model                           = parent_document.list_tab.list_model
        #rint( "begin channel_select for the list")
        query                           = QSqlQuery()
        query_builder                   = qt_sql_query.QueryBuilder( query, print_it = False, )

        kw_table_name                   = "plant_key_words"
        column_list                     = [ "id", "id_old", "name", "latin_name", "add_kw",         ]

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
        AppGlobal.logger.debug( msg )

        is_ok  = AppGlobal.qsql_db_access.query_exec_model( query,
                                                  model,
                                                  msg = "HelpSubWindow criteria_select" )

        msg      = (  query.executedQuery()   )
        AppGlobal.logger.info( msg )
        print( msg )
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
        tab             = self
        max_col         = 4

        box_layout_1    =  QVBoxLayout( page )

        placer          = gui_qt_ext.PlaceInGrid(
                            central_widget  = box_layout_1,
                            a_max           = max_col,
                            by_rows         = False  )

        tab_layout      = placer

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

        sub_tab      = PictureListSubTab( self )
        # self.pictures_tab   = sub_tab
        self.picture_sub_tab    = sub_tab
        self.sub_tab_list.append( sub_tab )
        tab_folder.addTab( sub_tab, "Pictures" )

        # Main notebook
        detail_notebook           = QTabWidget()
        self.detail_notebook      = detail_notebook

        # ---- buttons
        button_layout = QHBoxLayout()

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
        """
        # ---- code_gen: detail_tab_build_gui use for _build_fields was_build_gui  -- begin table entries
        # ---- code_gen: detail_tab_build_gui use for _build_fields was_build_gui  -- begin table entries


        # ---- id
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "id",
                                                db_type        = "integer",
                                                display_type   = "integer",
                                                 )
        edit_field.setPlaceholderText( "id" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- id_old
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "id_old",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "id_old" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- name
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "name",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "name" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field )


        # ---- latin_name
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "latin_name",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "latin_name" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- add_kw
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "add_kw",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "add_kw" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field )


        # ---- descr
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "descr",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "descr" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field )


        # ---- plant_type
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "plant_type",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "plant_type" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- type_sub
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "type_sub",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "type_sub" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- cmnt
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "cmnt",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "cmnt" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- life
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "life",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "life" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- water
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "water",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "water" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- sun_min
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "sun_min",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "sun_min" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- sun_max
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "sun_max",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "sun_max" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- zone_min
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "zone_min",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "zone_min" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- zone_max
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "zone_max",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "zone_max" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- height
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "height",
                                                db_type        = "integer",
                                                display_type   = "int7-2",
                                                 )
        edit_field.setPlaceholderText( "height" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- form
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "form",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "form" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- color
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "color",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "color" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- pref_unit
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "pref_unit",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "pref_unit" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- hybridizer
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "hybridizer",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "hybridizer" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- hybridizer_year
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "hybridizer_year",
                                                db_type        = "integer",
                                                display_type   = "integer",
                                                 )
        edit_field.setPlaceholderText( "hybridizer_year" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- color2
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "color2",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "color2" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- color3
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "color3",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "color3" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- life2
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "life2",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "life2" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- tag1
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "tag1",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "tag1" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- chromosome
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "chromosome",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "chromosome" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- bloom_time
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "bloom_time",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "bloom_time" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- bloom_dia
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "bloom_dia",
                                                db_type        = "integer",
                                                display_type   = "int5-2",
                                                 )
        edit_field.setPlaceholderText( "bloom_dia" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- fragrance
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "fragrance",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "fragrance" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- rebloom
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "rebloom",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "rebloom" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- itag1
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "itag1",
                                                db_type        = "integer",
                                                display_type   = "integer",
                                                 )
        edit_field.setPlaceholderText( "itag1" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- extended
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "extended",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "extended" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- plant_class
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "plant_class",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "plant_class" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- source_type
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "source_type",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "source_type" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- source_detail
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "source_detail",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "source_detail" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- spider
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "spider",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "spider" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- spider_ratio
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "spider_ratio",
                                                db_type        = "integer",
                                                display_type   = "int5-2",
                                                 )
        edit_field.setPlaceholderText( "spider_ratio" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- double
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "double",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "double" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


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
        print( f"PlantDocumentDetaiTab fetch_row { id=}")
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
        # self.table_name          = "stuff"  not needed we get fro parent
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

        # self.parent_window   = parent_window
        self.tab_name            = "PlantHistorylTab"

    # -------------------------------------
    def _build_guiXXXXXX( self ):
        """
        what it says read
        update ver 21 to picture_sub_window
        Returns:
            none
        """
        tab                  = self
        table                = QTableWidget(
                                    0, 10, self )  # row column third arg parent
        self.history_table   = table

        ix_col   = 1
        table.setColumnWidth( ix_col, 22 )

        # table.clicked.connect( self.parent_window.on_history_clicked )
        # table.clicked.connect( self.on_list_clicked )
        table.cellClicked.connect( self.on_cell_clicked )

        layout2     = QVBoxLayout()
        layout2.addWidget( table )
        tab.setLayout( layout2 )



# ----------------------------------------
class PlantEventSubTab( base_document_tabs.SubTabBase  ):
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
        #self.current_id      = 28
        #print( "fix plant event select and delete line above should be select_by_id  ")
        self._build_model()
        self._build_gui()

        self.parent_window.sub_tab_list.append( self )    # a function might be better

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says, read
        !! initial query should come out

        """
        page            = self
        tab             = page

        layout                     = QVBoxLayout( tab )
        button_layout              = QHBoxLayout()

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
        model.setFilter( "plant_id = 28 " )
        print( "!!fix plant_id = 28 ")

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

        Args:
            id (TYPE): DESCRIPTION.

        Returns:
            None.

        """
        # ---- write
        model           = self.model_write

        self.current_id  = id
        model.setFilter( f"plant_id = {id}" )
        # model_write.setFilter( f"pictureshow_id = {id} " )
        model.select()

        print( "do we need next ")
        #self.list_view.setModel( model_write )

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
