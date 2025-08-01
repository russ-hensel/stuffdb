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


#from   functools import partial
#import collections
import functools
import logging
import sqlite3
import time
from   datetime import datetime


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

import data_dict
#import  picture_viewer
#import  tracked_qsql_relational_table_model  # dump for qt with logging
import gui_qt_ext
import string_util
from   app_global import AppGlobal
import base_document_tabs
import custom_widgets  as cw
import key_words
#import mdi_management
import people_document_edit
import qt_sql_query
import qt_with_logging

logger          = logging.getLogger( )
LOG_LEVEL       = 20 # level form much debug
      #   higher is more debugging    logging.log( LOG_LEVEL,  debug_msg, )

# one of two can we combine or at least improve name
PEOPLE_CONTACT_COLUMN_DICT         = None
    # search for build location  or put here and call back
    # map from name to column #


EVENT_FIELD_DICT          = None
PHONE_FIELD_DICT          = None


# def build_pccd( ):
#     """
#     put in some init do delay build = lazy
#     """
#     global PEOPLE_CONTACT_COLUMN_DICT

#     if PEOPLE_CONTACT_COLUMN_DICT is None:
#         a_table    = data_dict.DATA_DICT.get_table( "people_phone" )
#         PEOPLE_CONTACT_COLUMN_DICT   = a_table.make_name_to_ix_dict()



# ----------------------------------------
class PeopleDocument( base_document_tabs.DocumentBase ):
    """
    for the people table....
    """
    def __init__(self, instance_ix = 0 ):
        """
        the usual
        """
        super().__init__( instance_ix )

        self.db                     = AppGlobal.qsql_db_access.db

        self.detail_table_name      = "people"
        self.text_table_name        = "people_text"  # text tables always id and text_data
        self.key_word_table_name    = "people_key_word"
        self.help_filename          = "people_doc.txt"
        self.subwindow_name         = "PeopleDccument"

        self._build_gui()
        self.__init_2__()

    # --------------------------------
    def get_topic( self ):
        """
        of the detail record
        !! make
        """
        topic           = "people topic "

        record_state    = self.detail_tab.data_manager.record_state

        if record_state:
            topic    = f"{topic} {record_state = }"
        topic    = f"{topic} {self.detail_tab.l_name_field.text()}"

        return   topic

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says
        """
        main_notebook           = self.tab_folder   # create in parent
        self.main_notebook      = main_notebook

        sub_window              = self
        mdi_area                = AppGlobal.main_window.mdi_area
        main_notebook.currentChanged.connect( self.on_tab_changed )

        ix                        = -1

        ix                       += 1
        self.criteria_tab_index   = ix
        self.criteria_tab         = PeopleCriteriaTab( self  )
        main_notebook.addTab(       self.criteria_tab, "Criteria" )

        ix                       += 1
        self.list_tab_index      = ix
        self.list_tab            = PeopleListTab( self  )
        main_notebook.addTab(  self.list_tab, "List"    )

        ix                       += 1
        self.detail_tab_index     = ix
        self.detail_tab           = PeopleDetailTab( self )
        main_notebook.addTab( self.detail_tab, "Detail"     )

        ix                       += 1
        self.picture_tab_index     = ix
        self.picture_tab           = base_document_tabs.StuffdbPictureTab( self )
        main_notebook.addTab( self.picture_tab, "Picture"     )

        ix                         += 1
        self.text_tab_index         = ix
        self.text_tab               = PeopleTextTab( self )
        main_notebook.addTab( self.text_tab, "Text"     )

        ix                        += 1
        self.history_tab_index     = ix
        self.history_tab           = PeopleHistorylTab( self )
        main_notebook.addTab( self.history_tab, "History"    )

        sub_window.setWidget( main_notebook )
        mdi_area.addSubWindow( sub_window )  # perhaps add to register_document in midi_management

        sub_window.show()

    # -------------------------------------
    def i_am_hsw(self):
        """
        make sure call is to here for testing
        """
        print( "people sub window, i_am_hsw")

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

    # ---- sub window interactions ---------------------------------------
    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = ">>>>>>>>>>* peopleSubWindow  *<<<<<<<<<<<<"

        return a_str

# ----------------------------------------
class PeopleCriteriaTab( base_document_tabs.CriteriaTabBase,  ):
    """
    criteria for list selection
    """
    def __init__(self, parent_window ):
        """
        the usual
        """
        super().__init__( parent_window )
        self.tab_name            = "PeopleCriteriaTab"

    # ------------------------------------------
    def _build_tab( self, ):
        """
        what it says, read
        """
        page            = self
        layout          = QHBoxLayout( page )
                # can we fold in to next

        grid_layout     = gui_qt_ext.CQGridLayout( col_max = 10 )
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
        widget          = QLabel( "Key Words" )
        grid_layout.new_row()
        grid_layout.addWidget( widget )

        widget          = cw.CQLineEdit(
                                    field_name = "key_words" )
        self.critera_widget_list.append( widget )
        widget.textChanged.connect( lambda: self.criteria_changed( True ) )
        grid_layout.addWidget( widget, columnspan = 3 )

        # ---- name like
        grid_layout.new_row()
        widget  = QLabel( "Last Name (like)" )
        grid_layout.addWidget( widget )

        widget                  = cw.CQLineEdit(
                                                 field_name = "last_name" )
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

        widget.addItem('l_name')
        widget.addItem('f_name')
        #widget.addItem('Title??')

        widget.currentIndexChanged.connect( lambda: self.criteria_changed( True ) )
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


        debug_msg = ( "build_tab build criteria change put in as marker ")
        logging.log( LOG_LEVEL,  debug_msg, )

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
        # grid_layout.addItem( widget, grid_layout.ix_row, grid_layout.ix_col    )

        # ---- function_on_return( self )
        for i_widget in self.critera_widget_list:
            i_widget.function_on_return   = self.criteria_select

    # -------------
    def criteria_select( self,     ):
        """
        use criteria to select into list tab

        """
        parent_document                 = self.parent_window

        model                           = parent_document.list_tab.list_model
        #rint( "begin channel_select for the list")
        query                           = QSqlQuery()
        query_builder                   = qt_sql_query.QueryBuilder( query, print_it = False, )

        kw_table_name                   = "platning_key_words"

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
        # old below
        # column_list                     = [ "id", "id_old", "name", "descr",  "add_kw",         ]
        #column_list                     = [ "id", "id_old",   "add_kw", "f_name",  "l_name",     ]


        a_key_word_processor            = key_words.KeyWords( kw_table_name, AppGlobal.qsql_db_access.db )
        query_builder.table_name        = parent_document.detail_table_name
        query_builder.column_list       = column_list

        # ---- add criteria
        criteria_dict                   = self.get_criteria()

        # ---- key words
        criteria_key_words              = criteria_dict[ "key_words" ]
        criteria_key_words              = a_key_word_processor.string_to_key_words( criteria_key_words )
        key_word_count                  = len( criteria_key_words )

        criteria_key_words              = ", ".join( [ f'"{i_word}"' for i_word in criteria_key_words ] )
        criteria_key_words              = f'( {criteria_key_words} ) '    # ( "one", "two" )

        if key_word_count > 0:
            query_builder.group_by_c_list   = column_list
            query_builder.sql_inner_join    = " people_key_word  ON people.id = people_key_word.id "
            query_builder.sql_having        = f" count(*) = {key_word_count} "

            query_builder.add_to_where( f" key_word IN {criteria_key_words}" , [] )

        # ---- name like
        last_name                          = criteria_dict[ "last_name" ].strip().lower()
        if last_name:
            add_where       = "lower( l_name )  like :last_name"   # :is name of bind var below
            query_builder.add_to_where( add_where, [(  ":last_name",
                                                     f"%{last_name}%" ) ])

        # ---- order by
        order_by   = criteria_dict[ "order_by" ]

        if   order_by == "_lname":
            column_name = "_lname"
        elif order_by == "f_name":
            column_name = "f_name"
        else:   # !! might better handel this
            column_name = "l_name"

        query_builder.add_to_order_by(    column_name, "ASC",   )

        query_builder.prepare_and_bind()

        msg      = f"{query_builder = }"
        AppGlobal.logger.debug( msg )

        is_ok  = AppGlobal.qsql_db_access.query_exec_model( query,
                                                  model,
                                                  msg = "People_critera_tab criteria_select" )

        debug_msg      = (  query.executedQuery()   )
        logging.log( LOG_LEVEL,  debug_msg, )

        parent_document.main_notebook.setCurrentIndex( parent_document.list_tab_index )
        self.critera_is_changed = False

# ----------------------------------------
class PeopleListTab( base_document_tabs.ListTabBase  ):
    """
    """
    def __init__(self, parent_window ):
        """
        """
        super().__init__( parent_window )
        self.tab_name           = "PeopleListTab"
        self._build_gui()

# ----------------------------------------
class PeopleDetailTab( base_document_tabs.DetailTabBase  ):
    """
    """
    def __init__(self, parent_window  ):
        """

        """
        super().__init__( parent_window )

        self.tab_name            = "PeopleDetailTab"
        self.key_word_table_name = "people_key_word"
        self.post_init()

    # -------------------------------------
    def _build_gui( self ):
        """
        what it says read
        Returns:
            none
        """
        page            = self
        tabxxx             = self

        box_layout_1    =  QVBoxLayout( page )
        max_col         = 10
        self.max_col    = max_col

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
        tab_layout.addWidget( tab_folder, columnspan = max_col   )

        sub_tab      = PeoplePictureListSubTab( self )
        self.pictures_tab       = sub_tab    # think this is wrong
        self.picture_sub_tab    = sub_tab    # !! phase out ?? no is special
        self.sub_tab_list.append( sub_tab )
        tab_folder.addTab( sub_tab, "Pictures" )

        sub_tab      = PeopleEventSubTab( self )
        self.event_sub_tab   = sub_tab
        self.sub_tab_list.append( sub_tab )
        tab_folder.addTab( sub_tab, "Events" )

        sub_tab      = PeopleContactSubTab( self )
        self.event_sub_tab   = sub_tab
        self.sub_tab_list.append( sub_tab )
        tab_folder.addTab( sub_tab, "ContactInfo" )

        # Main notebook
        detail_notebook           = QTabWidget()
        self.detail_notebook      = detail_notebook

    # -------------------------------------
    def _build_fields( self, layout ):
        """
        place fields into tab_layout, a sub layout is ok
        tweaks
               spacer code at top
               watch for ddl but may not be any yet
        """
        width  = 50
        for ix in range( self.max_col ):  # try to tweak size to make it work
            widget   = QSpacerItem( width, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
            layout.addItem( widget, 0, ix  )  # row column


        # ---- code_gen: TableDict.to_build_form 2025_04_01 for people -- begin table entries -----------------------

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
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- descr
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "descr", )
        self.descr_field     = edit_field
        edit_field.setPlaceholderText( "descr" )
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- add_kw
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "add_kw", )
        self.add_kw_field     = edit_field
        edit_field.setPlaceholderText( "add_kw" )
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- f_name
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "f_name", )
        self.f_name_field     = edit_field
        self.topic_edits.append( (edit_field, 1 ) )
        edit_field.setPlaceholderText( "f_name" )
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 4 )

        # ---- m_name
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "m_name", )
        self.m_name_field     = edit_field
        edit_field.setPlaceholderText( "m_name" )
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- l_name
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "l_name", )
        self.l_name_field     = edit_field
        self.topic_edits.append( (edit_field, 2 ) )
        edit_field.setPlaceholderText( "l_name" )
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 4 )

        # ---- st_adr_1
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "st_adr_1", )
        self.st_adr_1_field     = edit_field
        edit_field.setPlaceholderText( "st_adr_1" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- st_adr_2
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "st_adr_2", )
        self.st_adr_2_field     = edit_field
        edit_field.setPlaceholderText( "st_adr_2" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- st_adr_3
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "st_adr_3", )
        self.st_adr_3_field     = edit_field
        edit_field.setPlaceholderText( "st_adr_3" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- city
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "city", )
        self.city_field     = edit_field
        edit_field.setPlaceholderText( "city" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- state
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "state", )
        self.state_field     = edit_field
        edit_field.setPlaceholderText( "state" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- zip
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "zip", )
        self.zip_field     = edit_field
        edit_field.setPlaceholderText( "zip" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- type
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "type", )
        self.type_field     = edit_field
        edit_field.setPlaceholderText( "type" )
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

        # ---- dt_enter
        edit_field                  = cw.CQDateEdit(
                                                parent         = None,
                                                field_name     = "dt_enter", )
        self.dt_enter_field     = edit_field
        edit_field.setPlaceholderText( "dt_enter" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- cmnt
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "cmnt", )
        self.cmnt_field     = edit_field
        edit_field.setPlaceholderText( "cmnt" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 4 )

        # ---- status
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "status", )
        self.status_field     = edit_field
        edit_field.setPlaceholderText( "status" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )


        # ---- dt_item
        edit_field                  = cw.CQDateEdit(
                                                parent         = None,
                                                field_name     = "dt_item", )
        self.dt_item_field                = edit_field
        edit_field.rec_to_edit_cnv        = edit_field.cnv_int_to_qdate
        edit_field.dict_to_edit_cnv       = edit_field.cnv_int_to_qdate
        edit_field.edit_to_rec_cnv        = edit_field.cnv_qdate_to_int
        edit_field.edit_to_dict_cnv       = edit_field.cnv_qdate_to_int
        edit_field.setPlaceholderText( "dt_item" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- c_name
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "c_name", )
        self.c_name_field     = edit_field
        edit_field.setPlaceholderText( "c_name" )
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- title
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "title", )
        self.title_field     = edit_field
        edit_field.setPlaceholderText( "title" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- dddd
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "dddd", )
        self.dddd_field     = edit_field
        edit_field.setPlaceholderText( "dddd" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- department
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "department", )
        self.department_field     = edit_field
        edit_field.setPlaceholderText( "department" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- floor
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "floor", )
        self.floor_field     = edit_field
        edit_field.setPlaceholderText( "floor" )
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

        # ---- role_text
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "role_text", )
        self.role_text_field     = edit_field
        edit_field.setPlaceholderText( "role_text" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- assoc_msn
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "assoc_msn", )
        self.assoc_msn_field     = edit_field
        edit_field.setPlaceholderText( "assoc_msn" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- bussiness_house
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "bussiness_house", )
        self.bussiness_house_field     = edit_field
        edit_field.setPlaceholderText( "bussiness_house" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- country
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "country", )
        self.country_field     = edit_field
        edit_field.setPlaceholderText( "country" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- autodial
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "autodial", )
        self.autodial_field     = edit_field
        edit_field.setPlaceholderText( "autodial" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

    # -------------------------------------
    def _build_fields_old( self, layout ):
        """
        place fields into tab_layout, a sub layout is ok
        tweaks
               spacer code at top
               watch for ddl but may not be any yet
        """
        width  = 50
        for ix in range( self.max_col ):  # try to tweak size to make it work
            widget   = QSpacerItem( width, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
            layout.addItem( widget, 0, ix  )  # row column

        # ---- code_gen: TableDict.to_build_form 2025_02_01 for people -- begin table entries -----------------------

        # ---- id
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "id",
                                                db_type        = "integer",
                                                display_type   = "string",
                                                 )
        self.id_field     = edit_field
        edit_field.setReadOnly( True )
        edit_field.setPlaceholderText( "id" )
        edit_field.edit_to_rec     = edit_field.edit_to_rec_str_to_int
        edit_field.rec_to_edit     = edit_field.rec_to_edit_int_to_str
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 1 )
        edit_field.setReadOnly( True )

        # ---- id_old
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "id_old",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.id_old_field     = edit_field
        edit_field.setReadOnly( True )
        edit_field.setPlaceholderText( "id_old" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- descr
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "descr",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.descr_field     = edit_field
        edit_field.setPlaceholderText( "descr" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- add_kw
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "add_kw",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.add_kw_field     = edit_field
        edit_field.setPlaceholderText( "add_kw" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- f_name
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "f_name",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.topic_edits.append( (edit_field, 1 ) )
        edit_field.setPlaceholderText( "f_name" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 4 )

        # ---- m_name
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "m_name",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "m_name" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- l_name
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "l_name",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.topic_edits.append( (edit_field, 2 ) )
        edit_field.setPlaceholderText( "l_name" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 4 )

        # ---- st_adr_1
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "st_adr_1",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "st_adr_1" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- st_adr_2
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "st_adr_2",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "st_adr_2" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- st_adr_3
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "st_adr_3",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "st_adr_3" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- city
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "city",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "city" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- state
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "state",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "state" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- zip
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "zip",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        edit_field.setPlaceholderText( "zip" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- type
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "type",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.type_field     = edit_field
        edit_field.setPlaceholderText( "type" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- type_sub
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "type_sub",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.type_sub_field     = edit_field
        edit_field.setPlaceholderText( "type_sub" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- dt_enter
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "dt_enter", )
        self.dt_enter_field     = edit_field
        edit_field.rec_to_edit_cnv        = edit_field.cnv_int_to_qdate
        edit_field.dict_to_edit_cnv       = edit_field.cnv_int_to_qdate
        edit_field.edit_to_rec_cnv        = edit_field.cnv_qdate_to_int
        edit_field.edit_to_dict_cnv       = edit_field.cnv_qdate_to_int
        edit_field.setPlaceholderText( "dt_enter" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- cmnt
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "cmnt",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.cmnt_field     = edit_field
        edit_field.setPlaceholderText( "cmnt" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 4 )

        # ---- status
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "status",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.status_field     = edit_field
        edit_field.setPlaceholderText( "status" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- dt_item
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "dt_item",
                                                db_type        = "integer",
                                                display_type   = "timestamp",
                                                 )
        self.dt_item_field     = edit_field
        edit_field.setPlaceholderText( "dt_item" )
        edit_field.edit_to_rec     = edit_field.edit_to_rec_str_to_int
        edit_field.rec_to_edit     = edit_field.rec_to_edit_int_to_str
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- c_name
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "c_name",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.c_name_field     = edit_field
        edit_field.setPlaceholderText( "c_name" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- title
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "title",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.title_field     = edit_field
        edit_field.setPlaceholderText( "title" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- dddd
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "dddd",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.dddd_field     = edit_field
        edit_field.setPlaceholderText( "dddd" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- department
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "department",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.department_field     = edit_field
        edit_field.setPlaceholderText( "department" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- floor
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "floor",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.floor_field     = edit_field
        edit_field.setPlaceholderText( "floor" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- location
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "location",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.location_field     = edit_field
        edit_field.setPlaceholderText( "location" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- role_text
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "role_text",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.role_text_field     = edit_field
        edit_field.setPlaceholderText( "role_text" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- assoc_msn
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "assoc_msn",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.assoc_msn_field     = edit_field
        edit_field.setPlaceholderText( "assoc_msn" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- bussiness_house
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "bussiness_house",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.bussiness_house_field     = edit_field
        edit_field.setPlaceholderText( "bussiness_house" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- country
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "country",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.country_field     = edit_field
        edit_field.setPlaceholderText( "country" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- autodial
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "autodial",
                                                db_type        = "integer",
                                                display_type   = "integer",
                                                 )
        self.autodial_field     = edit_field
        edit_field.setPlaceholderText( "autodial" )
        edit_field.edit_to_rec     = edit_field.edit_to_rec_str_to_int
        edit_field.rec_to_edit     = edit_field.rec_to_edit_int_to_str
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

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

        edit_ts  = self.edit_ts_field.text()
        edit_ts  = "self.edit_ts_field.text()"   # !! test

        self.default_new_row(  next_key )

        # ---- set the defaults
        self.descr_field.setText( descr + "*" )
        # self.url_field.setText( url )

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
    def get_picture_file_name(self):
        """
        some promotable -- but picture is special only one file, rest
        work differently
        see picture document

        return file_name or None if no file name
        """
        debug_msg  = ( "get_picture_file_name to be implemented" )
        logging.log( LOG_LEVEL,  debug_msg, )
        return ""  # none will cause exception  , just need file name that does not exist


# ==================================
class PeopleTextTab( base_document_tabs.TextTabBase  ):
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
        self.tab_name         = "PeopleTextTab"

        self.table            = "people_text"
        self.table_name       = self.table   # !! eliminate one or other

        self.post_init()

# ----------------------------------------
class PeopleHistorylTab( base_document_tabs.HistoryTabBase   ):

    def __init__(self, parent_window ):
        """
        """
        super().__init__( parent_window )

        self.tab_name            = "PeopleHistorylTab"

# ----------------------------------------
class PeopleEventSubTab( base_document_tabs.SubTabBase ):
    """
    """
    def __init__(self, parent_window ):
        """
        """
        super().__init__( parent_window )

        self.table_name      = "people_phone"

        global EVENT_FIELD_DICT
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
        global PEOPLE_CONTACT_COLUMN_DICT

        if PEOPLE_CONTACT_COLUMN_DICT is None:
            a_table    = data_dict.DATA_DICT.get_table( self.table_name )
            PEOPLE_CONTACT_COLUMN_DICT   = a_table.make_name_to_ix_dict()


        model              = ContactSqlTableModel(  self, self.db    )
        self.model         = model

        model.setTable( self.table_name )
        model.setEditStrategy( QSqlTableModel.OnManualSubmit )

    # ------------------------------------------
    def _build_dialog( self, data ):
        """
        what it says, read
        # Open dialog with the current data
        #dialog = StuffEventDialog(self, edit_data=data)
        """
        dialog   = people_document_edit.EditPeopleContact( self, data )
        return   dialog

    # ------------------------------------------
    def fix_add_keys( self, form_data ):
        """ """
        # print( "SubTabBase still need to fix this perahps add_dict_adjust( form_data ) not clear how to paramaterize ")
        # ver 3  --- but some may be passed in ?
        a_id    = AppGlobal.key_gen.get_next_key( self.table_name )

        form_data[ "seq_id" ]     = a_id
        form_data[ "people_id" ]  = self.current_id

    # ---------------------------------------
    def select_by_id( self, id ):
        """
        maybe make anscestor and promote
        could be paramaterized with key name ??
        """
        model               = self.model

        self.current_id     = id
        model.setFilter( f"people_id = {id}" )
        # model_write.setFilter( f"pictureshow_id = {id} " )
        model.select()


# ----------------------------------------
class PeopleEventSubTabOld( base_document_tabs.SubTabBaseOld ):
    """
    """
    def __init__(self, parent_window ):
        """
        """
        super().__init__( parent_window )

        self.list_ix         = 5  # should track selected an item in detail
        # needs work
        self.db              = AppGlobal.qsql_db_access.db

        self.table_name      = "people_event"
        self.list_table_name = self.table_name   # delete this
        #self.tab_name            = "PeopleEventSubTab  not needed tis is a sub tab
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
        page            = self

        layout                     = QVBoxLayout( page )
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
        #model              = QSqlTableModel( self, self.db )

        model              = qt_with_logging.QSqlTableModelWithLogging(  self, self.db    )
        self.model_write   = model
        self.model         = model

        model.setTable( self.list_table_name )
        model.setEditStrategy( QSqlTableModel.OnManualSubmit )


    # ---------------------------------------
    def select_by_id( self, id ):
        """
        maybe make anscestor and promote

        Args:
            id (TYPE): DESCRIPTION.

        Returns:
            None.

        """
        # ---- write
        model           = self.model_write

        self.current_id  = id
        model.setFilter( f"people_id = {id}" )
        # model_write.setFilter( f"pictureshow_id = {id} " )
        model.select()

    # -------------------------------------
    def i_am_hsw(self):
        """
        make sure call is to here

        """
        print( "i_am_hsw")

    # -------------------------------------
    def default_new_row( self ):
        """

        tail_tab.default_new_row( next_key )
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
        dialog     = people_document_edit.EditPeopleEvents( model, index = None, parent = self )
        if dialog.exec_() == QDialog.Accepted:
            #self.model.submitAll()
            ok     = base_document_tabs.model_submit_all(
                       model,  f"PeopleEventsSubTab.add_record " )
            self.model.select()

    # ------------------------------------------
    def edit_record(self):
        """
        what it says, read?
        """
        index       = self.view.currentIndex()
        model       = self.model
        if index.isValid():
            dialog = people_document_edit.EditPeopleEvents( self.model, index, parent = self )
            if dialog.exec_() == QDialog.Accepted:
                #self.model.submitAll()
                ok     = base_document_tabs.model_submit_all(
                           model,  f"PeopleEventsSubTab.add_record " )
                #ia_qt.q_sql_table_model( self.model, "post edit_record submitAll()" )
                self.model.select()
        else:
            msg   = "Click on row to edit..."
            QMessageBox.warning(self, "Please", msg )

    # ------------------------------------------
    def delete_record(self):
        """
        what it says, read?
        set curent id, get children
        """
        msg   = "delete_record ... not implemented"
        QMessageBox.warning(self, "Sorry", msg )

    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = ">>>>>>>>>>* PeopleEventSubTab  *<<<<<<<<<<<<"

        return a_str

# ----------------------------------------
class PeopleContactSubTab( base_document_tabs.SubTabBaseOld ):
    """
    """
    def __init__(self, parent_window ):
        """
        """
        super().__init__( parent_window )


        self.table_name      = "people_contact"  # revise
        self.table_name      = "people_phone"
        # self.list_table_name = self.table_name   # delete this
        self.current_id      = None  # probably get from somewher else ??

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
        model                = self.model
        #self.list_view       = view
        self.view            = view
        view.setModel( self.model )

        # print( "_build_gui  this may be in wrong place ")
        # layout.addWidget( view )
        #placer.place(  view )

        col_header_dict   = data_dict.rpt_sub_tab_columns_order( self.table_name, verbose = False  )
            # could be done at module level

        ix_col = -1   # could make loop or even list comp
        for i_column_name, col_dict in col_header_dict.items():
            ix_col    += 1

            model.setHeaderData( ix_col, Qt.Horizontal, col_dict[ "col_head_text"  ] )
            view.setColumnWidth( ix_col,                col_dict[ "col_head_width" ] )


# ---------
# CREATE TABLE  people_phone    (
#      seq_id  VARCAR(10),
#      people_id  VARCAR(10),
#      type  VARCAR(10),
#      phone_old  VARCAR(35),
#      cmnt  VARCAR(40),
#      phone  VARCAR(100),
#      autodial  INTEGER
#     )
# ----------
        # ix_col += 1
        # model.setHeaderData( ix_col, Qt.Horizontal, "seq_id" )
        # view.setColumnWidth( ix_col, 100)  # Set  width in  pixels

        # ix_col += 1
        # model.setHeaderData( ix_col, Qt.Horizontal, "people_id" )
        # view.setColumnWidth( ix_col, 100)  # Set  width in  pixels

        # ix_col += 1
        # model.setHeaderData( ix_col, Qt.Horizontal, "Type" )
        # view.setColumnWidth( ix_col, 100)  # Set  width in  pixels

        # ix_col += 1
        # model.setHeaderData( ix_col, Qt.Horizontal, "Phone Old" )
        # view.setColumnWidth( ix_col, 100)  # Set  width in  pixels

        # ix_col += 1
        # model.setHeaderData( ix_col, Qt.Horizontal, "Comment" )
        # view.setColumnWidth( ix_col, 300)  # Set  width in  pixels

        # ix_col += 1
        # model.setHeaderData( ix_col, Qt.Horizontal, "Phone" )
        # view.setColumnWidth( ix_col, 100)  # Set  width in  pixels

        # ix_col += 1
        # model.setHeaderData( ix_col, Qt.Horizontal, "AutoDial" )
        # view.setColumnWidth( ix_col, 100)  # Set  width in  pixels

        #view.setColumnHidden( 1, True )  # view or model

        layout.addWidget( view )

        # ---- buttons
        widget        = QPushButton( 'Add' )
        #add_button    = widget
        widget.clicked.connect( self.add_new_contact )
        button_layout.addWidget( widget )

        #
        widget        = QPushButton('Edit')
        #add_button    = widget
        widget.clicked.connect( self.edit_selected_record )
        button_layout.addWidget( widget )

        #
        widget        = QPushButton('Delete')
        #add_button    = widget
        widget.clicked.connect(self.delete_record)
        button_layout.addWidget( widget )

    # ---------------------------------
    def _build_model( self, ):
        """

        put in some init do delay build = lazy
        """
        global PEOPLE_CONTACT_COLUMN_DICT

        if PEOPLE_CONTACT_COLUMN_DICT is None:
            a_table    = data_dict.DATA_DICT.get_table( self.table_name )
            PEOPLE_CONTACT_COLUMN_DICT   = a_table.make_name_to_ix_dict()


        model              = ContactSqlTableModel(  self, self.db    )
        self.model         = model

        model.setTable( self.table_name )
        model.setEditStrategy( QSqlTableModel.OnManualSubmit )

    # ---------------------------------------
    def select_by_id( self, id ):
        """
        maybe make anscestor and promote

        """
        model               = self.model

        self.current_id     = id
        model.setFilter( f"people_id = {id}" )  # for stuff_event
        # model_write.setFilter( f"pictureshow_id = {id} " )
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
            None.

        """
        next_key      = AppGlobal.key_gen.get_next_key(
                                  self.detail_table_name )
        self.detail_tab.default_new_row( next_key )
        self.text_tab.default_new_row(   next_key )

    # ------------------------------------------
    def add_record_old_may_rename (self):
        """
        what it says, read?
        add test for success an refactor??
        """
        model      = self.model
        dialog     = people_document_edit.EditPeopleContact( model, index = None, parent = self )
        if dialog.exec_() == QDialog.Accepted:
            #self.model.submitAll()
            ok     = base_document_tabs.model_submit_all(
                       model,  f"PeopleEventsSubTab.add_record " )
            self.model.select()

    #---------------- restart here model view dialog name
    #  ---- chat functions
    def add_new_contact(self):
        """
        Open dialog to add a new event and insert it into the model.
        """
        #dialog = StuffEventDialog(self)
        dialog      = people_document_edit.EditPeopleContact( self )  # the parent tab
        model       = self.model
        # parent=None, edit_data=None ):

        if dialog.exec_() == QDialog.Accepted:
            form_data   = dialog.get_form_data()

            # Create a new record
            row         = self.model.rowCount()
            self.model.insertRow(row)

            # key
            # Set data for each field
            #model.setData( model.index(row, 0), form_data["id"])
            a_id    = AppGlobal.key_gen.get_next_key( self.table_name )
            # model.setData( model.index(row, 0), a_id )
            # old_non_editable                = model.non_editable_columns
            model.non_editable_columns  = { 99 } # beyond all columns

            debug_id  = self.current_id
            # model.setData( model.index(row, 1), form_data["stuff_id"])

            # ver 1
            #model.setData( model.index(row, 1), self.current_id )

            # model.non_editable_columns  = old_non_editable

            # ver 1
            # model.setData( model.index(row, 2), form_data["people_id"])
            # model.setData( model.index(row, 3), form_data["phone_old"])

            # ver 2
            # # can convert to loop ??
            # field_name   = "people_id"
            # field_ix     = PEOPLE_CONTACT_COLUMN_DICT[ field_name ]
            # model.setData( model.index( row, field_ix ), form_data[ field_name] )

            # field_name   = "phone_old"
            # field_ix     = PEOPLE_CONTACT_COLUMN_DICT[ field_name ]
            # model.setData( model.index( row, field_ix ), form_data[ field_name] )

            # ver 3  --- but some may be passed in ?
            form_data[ "seq_id" ]     = a_id
            form_data[ "people_id" ]  = self.current_id

            for field_name, field_ix in  PEOPLE_CONTACT_COLUMN_DICT.items():
                model.setData( model.index( row, field_ix ), form_data[ field_name ] )


            # model.setData( model.index(row, 4), form_data["cmnt"])
            # model.setData( model.index(row, 5), form_data["type"])

    # -------------------------------------------
    def get_selected_row_data(self):
        """
        Get the data from the currently selected row.
        """
        # Get the currently selected row
        model       = self.model

        indexes     = self.view.selectedIndexes()
        if not indexes:
            QMessageBox.warning(self, "Warning", "No record selected.")
            return None

        # Get the model row index
        model_row = indexes[0].row()

        # a_timestamp = self.model.data(self.model.index(0, 2), Qt.EditRole)
        # print(f"Raw timestamp: {a_timestamp = }")

        # ver 1
        # # Extract data from the row
        # data = {
        #     "id":         model.data( model.index( model_row, 0)),
        #     "people_id":  model.data( model.index( model_row, 1)),

        #     # # "event_dt":  model.data( model.index( model_row, 2)),
        #     # "event_dt":  a_timestamp,

        #     "phone_old":       model.data( model.index( model_row, 2)),
        #     # "cmnt":      model.data( model.index( model_row, 4)),
        #     # "type":      model.data( model.index( model_row, 5))
        # }

        # ver 2
        data  = {}
        for field_name, field_ix in  PEOPLE_CONTACT_COLUMN_DICT.items():
            #model.setData( model.index( row, field_ix ), form_data[ field_name ] )
            data[field_name]   = model.data( model.index( model_row, field_ix))
        # # Extract data from the row
        # data = {
        #     "id":         model.data( model.index( model_row, 0)),
        #     "people_id":  model.data( model.index( model_row, 1)),

        #     # # "event_dt":  model.data( model.index( model_row, 2)),
        #     # "event_dt":  a_timestamp,

        #     "phone_old":       model.data( model.index( model_row, 2)),
        #     # "cmnt":      model.data( model.index( model_row, 4)),
        #     # "type":      model.data( model.index( model_row, 5))
        # }


        return (model_row, data)

    # ----------------------------------
    def edit_selected_record(self):
        """
        from stuff then update
        Open dialog to edit the currently selected event.
        """
        selected_data = self.get_selected_row_data()
        if selected_data is None:
            return

        row, data = selected_data

        # Open dialog with the current data
        #dialog = StuffEventDialog(self, edit_data=data)
        dialog = people_document_edit.EditPeopleContact( self, edit_data = data )
            # self the parent tab

        model     = self.model

        if dialog.exec_() == QDialog.Accepted:
            form_data = dialog.get_form_data()

            # # Update the row with the new data
            # model.setData( model.index(row, 0), form_data["id"])
            # model.setData( model.index(row, 1), form_data["people_id"])
            # model.setData( model.index(row, 2), form_data["phone_old"])
            # model.setData( model.index(row, 3), form_data["dlr"])
            # model.setData( model.index(row, 4), form_data["cmnt"])
            # model.setData( model.index(row, 5), form_data["type"])
            # ver 3  --- but some may be passed in ?
            # form_data[ "seq_id" ]     = a_id
            # form_data[ "people_id" ]  = self.current_id

            for field_name, field_ix in  PEOPLE_CONTACT_COLUMN_DICT.items():
                model.setData( model.index( row, field_ix ), form_data[ field_name ] )



    # ------------------------------------------
    def edit_record_xxx(self):
        """

        in stuff as edit_selected_event ... will make edit_selected_record
        what it says, read?
        """


    # ------------------------------------------
    def delete_record(self):
        """
        what it says, read?

        set curent id, get children
        """
        msg   = "delete_record ... not implemented"
        QMessageBox.warning(self, "Sorry", msg )

    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = ">>>>>>>>>>* PeopleEventSubTab  *<<<<<<<<<<<<"

        return a_str

# ------------------------------------
class PeoplePictureListSubTab( base_document_tabs.PictureListSubTabBase ):
    """
    almos all promoted even this may not be necessary
    """
    def __init__(self, parent_window ):
        super().__init__( parent_window )
        self.pictures_for_table  = "people"

# ------------------------------------
class ContactSqlTableModel(QSqlTableModel):
    def __init__(self, parent=None, db=QSqlDatabase()):
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
    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        """
        for special formatting
        and alignment
        """
        col = index.column()

        # Check role first
        if role == Qt.DisplayRole:
            # Handle display formatting for event_dt (column 2)
            if col == 222:
                value = super().data(index, Qt.EditRole)
                if value is not None:
                    return datetime.fromtimestamp(value).strftime("%Y-%m-%d")
                return value  # Return raw value if None

        elif role == Qt.EditRole:
            # Return raw value for editing/database sync
            if col == 222:
                return super().data(index, Qt.EditRole)

        elif role == Qt.TextAlignmentRole:
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
