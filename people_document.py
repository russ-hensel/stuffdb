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

# import sqlite3

# from PyQt5.QtCore import QDate, QModelIndex, Qt, QTimer, pyqtSlot
# from PyQt5.QtGui import QStandardItem, QStandardItemModel
# from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
# from PyQt5.QtWidgets import (QAction,
#                              QActionGroup,
#                              QApplication,
#                              QButtonGroup,
#                              QDateEdit,
#                              QDockWidget,
#                              QLabel,
#                              QLineEdit,
#                              QListWidget,
#                              QMainWindow,
#                              QMdiSubWindow,
#                              QMenu,
#                              QMessageBox,
#                              QPushButton,
#                              QSpinBox,
#                              QTableView,
#                              QTableWidget,
#                              QTableWidgetItem,
#                              QTabWidget,
#                              QTextEdit,
#                              QWidget)


"""
my reference list of qt imports in qt_imports.py


"""
# ---- begin pyqt from import_qt.py

#from   functools import partial
#import collections
import functools
import logging
import sqlite3
import time

import data_dict
#import  picture_viewer
#import  tracked_qsql_relational_table_model  # dump for qt with logging
import gui_qt_ext
import string_util
from app_global import AppGlobal
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
# ---- QtCore
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
import base_document_tabs
import custom_widgets
import key_words
import mdi_management
import people_document_edit
import qt_sql_query
import qt_with_logging

logger          = logging.getLogger( )
LOG_LEVEL       = 20 # level form much debug    higher is more debugging    logging.log( LOG_LEVEL,  debug_msg, )




# ----------------------------------------
class PeopleDocument( base_document_tabs.DocumentBase ):
    """
    for the people table....
    """
    def __init__(self, ):
        """
        the usual
        """
        super().__init__()

        self.db                     = AppGlobal.qsql_db_access.db

        self.detail_table_name      = "people"
        self.text_table_name        = "people_text"  # text tables always id and text_data
        self.key_word_table_name    = "people_key_word"
        self.help_filename          = "people_doc.txt"
        self.subwindow_name         = "PeopleDccument"

        self.setWindowTitle( self.subwindow_name )
        self._build_gui()

    # --------------------------------
    def get_topic( self ):
        """
        of the detail record
        !! make
        """
        topic           = "people topic "

        record_state    = self.detail_tab.data_manager.record_state

        # # !! next is too much
        # columns          = data_dict.DATA_DICT.get_topic_columns( self.parent_window.detail_table_name )
        # col_head_texts   = [  ]  # plus one for sequence
        # col_names        = [  ]
        # col_head_widths  = [  ]
        # for i_column in columns:
        #     col_names.append(        i_column.column_name  )
        #     col_head_texts.append(   i_column.col_head_text  )
        #     col_head_widths.append(  i_column.col_head_width  )

        if record_state:
            topic    = f"{topic} {self.record_state = }"
        topic    = f"{topic} {self.detail_tab.l_name_field .text()}"

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

    # ---------------------------------------
    def fetch_row_by_id_promoted( self, id ):
        """
        rename call, delete
        what it says, mostly focused on the detail tab
        """
        self.select_record( id )
        return

        self.detail_tab.fetch_detail_row_by_idxxx(  id )
        self.text_tab.fetch_text_row_by_id(  id )
        self.detail_to_history()

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

    # ---- capture events ----------------------------
    # ------------------------------------------
    def on_list_clicked_promoted( self, index: QModelIndex ):
        """
        Args:
            index (QModelIndex): DESCRIPTION.

        !! promote the whole thing?? need key to be id col 0 seems ok
        might be functioalize if we use an argument for self.list.tab
        """
        print( f"on_list_clicked  save first if necessary")
        row                     = index.row()
        column                  = index.column()

        self.list_tab.list_ix   = row

        id_index                = self.list_tab.list_model.index(
            index.row( ), 0 )
        db_key                  = self.list_tab.list_model.data(
            id_index, Qt.DisplayRole )
        print( f"People Clicked on list row {row}, column {column}, {db_key=}" )  # " value: {value}" )

        # self.detail_tab.fetch_detail_row_by_id( db_key )
        self.fetch_row_by_id( db_key )

        self.main_notebook.setCurrentIndex( self.detail_tab_index )
        # self.detail_tab.id_field.setText( str( db_key )  ) # fetch currently does not include the id

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

        placer          = gui_qt_ext.PlaceInGrid(
            central_widget=page,
            a_max=0,
            by_rows=False  )

        self._build_top_widgets( placer )

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

        # ---- name like
        placer.new_row()
        widget  = QLabel( "Last Name (like)" )
        placer.place( widget )

        widget                  = custom_widgets.CQLineEditCriteria( get_type = "string", set_type = "string")
        self.name_widget        = widget
        widget.critera_name     = "last_name"
        self.critera_widget_list.append( widget )
        widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        placer.place( widget )

        # ---- Order by
        placer.new_row()
        widget  = QLabel( "Order by" )
        placer.place( widget )

        widget                 = custom_widgets.CQComboBoxEditCriteria( get_type = "string", set_type = "string")
        self.order_by_widget   = widget
        self.critera_widget_list.append( widget )
        widget.critera_name    = "order_by"

        widget.addItem('l_name')
        widget.addItem('f_name')
        #widget.addItem('Title??')

        debug_msg = ( "build_tab build criteria change put in as marker ")
        logging.log( LOG_LEVEL,  debug_msg, )

        widget.currentIndexChanged.connect( lambda: self.criteria_changed(  True   ) )
        placer.place( widget )

        # ---- criteria changed should be in parent
        placer.new_row()
        widget  = QLabel( "criteria_changed_widget" )
        self.criteria_changed_widget  = widget
        placer.place( widget )


        # ---- buttons
        # a_widget        = QPushButton( "Clear Criteria" )
        # a_widget.clicked.connect(  self.clear_criteria )
        # placer.new_row()
        # placer.place( a_widget )

        # ---- push controls up page, may need adjuxtment
        width    = 350
        widget   = QSpacerItem( width, 310, QSizePolicy.Expanding, QSizePolicy.Minimum )
        placer.new_row()
        # placer.place( widget )
        placer.layout.addItem( widget, placer.ix_row, placer.ix_col    )  # row column

        # done wth next !! ??
        #self.add_buttons( placer )


        return

    # #================= old
    #     page            = self
    #     tab             = page

    #     placer          = gui_qt_ext.PlaceInGrid(
    #     central_widget  = page,
    #     a_max           = 0,
    #     by_rows         = False  )

    #     # ----
    #     widget  = QLabel( "People Key Words" )
    #     placer.new_row()
    #     placer.place( widget )

    #     widget    = QLineEdit()
    #     self.key_words_widget    = widget
    #     widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
    #     placer.place( widget )


    #     # ----
    #     widget                = QLabel( "Key Words" )
    #     placer.new_row()
    #     placer.place( widget )

    #     widget                  = QLineEdit()
    #     self.key_words_widget   = widget
    #     widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
    #     placer.place( widget, columnspan = 3 )

    #     # ----
    #     placer.new_row()
    #     widget  = QLabel( "Last Name (like)" )
    #     placer.place( widget )

    #     widget                      = QLineEdit()
    #     self.last_name_widget        = widget
    #     placer.place( widget )

    #     # ----
    #     placer.new_row()
    #     widget  = QLabel( "First Name (like)" )
    #     placer.place( widget )

    #     widget                       = QLineEdit()
    #     self.first_name_widget        = widget
    #     placer.place( widget )

    #     # # ----
    #     # placer.new_row()
    #     # widget  = QLabel( "File Name Empty" )
    #     # placer.place( widget )

    #     # # ---- combo_1
    #     # widget                       = QComboBox()
    #     # self.file_name_empty_widget  = widget
    #     # widget.currentIndexChanged.connect( lambda: self.criteria_changed(  True   ) )
    #     # widget.addItem('Any')
    #     # widget.addItem('Yes')
    #     # widget.addItem('No')
    #     # placer.place( widget )



    #     # # ----"Order By:"
    #     # a_widget    = QLabel( "Order By:" )
    #     # placer.new_row()
    #     # placer.place( a_widget )

    #     self.add_date_widgets( placer )

    #     self.add_buttons( placer )

    #     # # ---- buttons
    #     # a_widget        = QPushButton( "Clear Criteria" )
    #     # a_widget.clicked.connect(  self.clear_criteria )
    #     # placer.new_row()
    #     # placer.place( a_widget )

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

        # self._build_gui()

        self.tab_name           = "PeopleDetailTab"

        # self.table_name         = parent_window.detail_table_name
        # model                   = QSqlTableModel(
        #     self, AppGlobal.qsql_db_access.db )
        # self.model              = model
        # self.tab_model          = model   # phase me out

        # self.mapper             = None
        # self._build_mapper()

        # model.setTable( self.table )
        # self.enable_send_topic_update    = True
        self.key_word_table_name         = "people_key_word"
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
        # ---------------
        tab_folder   = QTabWidget()
        # tab_folder.setTabPosition(QTabWidget.West)
        tab_folder.setMovable(True)
        tab_layout.new_row()
        tab_layout.addWidget( tab_folder, columnspan = max_col   )

        sub_tab      = PeoplePictureListSubTab( self )
        self.pictures_tab       = sub_tab  # think this is wrong
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
        """
        width  = 50
        for ix in range( self.max_col ):  # try to tweak size to make it work
            widget   = QSpacerItem( width, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
            layout.addItem( widget, 0, ix  )  # row column

        # ---- code_gen: TableDict.to_build_form 2025_02_01 for people -- begin table entries -----------------------

        # ---- id
        edit_field                  = custom_widgets.CQLineEdit(
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
        edit_field                  = custom_widgets.CQLineEdit(
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
        layout.addWidget( edit_field, columnspan = 2 )

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
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- f_name
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "f_name",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.f_name_field     = edit_field
        self.topic_edits.append( (edit_field, 1 ) )
        edit_field.setPlaceholderText( "f_name" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 4 )

        # ---- m_name
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "m_name",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.m_name_field     = edit_field
        edit_field.setPlaceholderText( "m_name" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- l_name
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "l_name",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.l_name_field     = edit_field
        self.topic_edits.append( (edit_field, 2 ) )
        edit_field.setPlaceholderText( "l_name" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 4 )

        # ---- st_adr_1
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "st_adr_1",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.st_adr_1_field     = edit_field
        edit_field.setPlaceholderText( "st_adr_1" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- st_adr_2
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "st_adr_2",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.st_adr_2_field     = edit_field
        edit_field.setPlaceholderText( "st_adr_2" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- st_adr_3
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "st_adr_3",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.st_adr_3_field     = edit_field
        edit_field.setPlaceholderText( "st_adr_3" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- city
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "city",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.city_field     = edit_field
        edit_field.setPlaceholderText( "city" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- state
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "state",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.state_field     = edit_field
        edit_field.setPlaceholderText( "state" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- zip
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "zip",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.zip_field     = edit_field
        edit_field.setPlaceholderText( "zip" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

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
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- type_sub
        edit_field                  = custom_widgets.CQLineEdit(
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
        layout.addWidget( edit_field, columnspan = 2 )

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
        layout.addWidget( edit_field, columnspan = 4 )

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
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- dt_item
        edit_field                  = custom_widgets.CQLineEdit(
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
        edit_field                  = custom_widgets.CQLineEdit(
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
        edit_field                  = custom_widgets.CQLineEdit(
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
        edit_field                  = custom_widgets.CQLineEdit(
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
        edit_field                  = custom_widgets.CQLineEdit(
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
        edit_field                  = custom_widgets.CQLineEdit(
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
        edit_field                  = custom_widgets.CQLineEdit(
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
        edit_field                  = custom_widgets.CQLineEdit(
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
        edit_field                  = custom_widgets.CQLineEdit(
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
        edit_field                  = custom_widgets.CQLineEdit(
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
        edit_field                  = custom_widgets.CQLineEdit(
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
        edit_field                  = custom_widgets.CQLineEdit(
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



    # -------------------------------------
    def _build_fields_old( self, layout ):
        """
        place fields into tab_layout, a sub layout is ok
        tweaks
               edit_field.setReadOnly( True )   on the id's'
        """

        # ---- code_gen: detail_tab_build_gui use for _build_fields was_build_gui  -- begin table entries
        #self._build_fields_pre_key( layout )
        # ---- code_gen: detail_tab_build_gui use for _build_fields was_build_gui  -- begin table entries


        # ---- code_gen: detail_tab_build_gui use for _build_fields was_build_gui  -- begin table entries


        # ---- id
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "id",
                                                db_type        = "integer",
                                                display_type   = "string",
                                                 )
        self.id_field     = edit_field
        edit_field.setPlaceholderText( "id" )
        edit_field.setReadOnly( True )
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
        self.id_old_field     = edit_field
        edit_field.setReadOnly( True )
        edit_field.setPlaceholderText( "id_old" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- f_name
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "f_name",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.f_name_field     = edit_field
        self.topic_edits.append( (edit_field, 1 ) )
        edit_field.setPlaceholderText( "f_name" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field )


        # ---- l_name
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "l_name",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.l_name_field     = edit_field
        self.topic_edits.append( (edit_field, 2 ) )
        edit_field.setPlaceholderText( "l_name" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field )


        # ---- st_adr_1
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "st_adr_1",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.st_adr_1_field     = edit_field
        edit_field.setPlaceholderText( "st_adr_1" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- st_adr_2
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "st_adr_2",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.st_adr_2_field     = edit_field
        edit_field.setPlaceholderText( "st_adr_2" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- st_adr_3
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "st_adr_3",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.st_adr_3_field     = edit_field
        edit_field.setPlaceholderText( "st_adr_3" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- city
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "city",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.city_field     = edit_field
        edit_field.setPlaceholderText( "city" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- state
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "state",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.state_field     = edit_field
        edit_field.setPlaceholderText( "state" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- zip
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "zip",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.zip_field     = edit_field
        edit_field.setPlaceholderText( "zip" )
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
        self.add_kw_field     = edit_field
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
        self.descr_field     = edit_field
        edit_field.setPlaceholderText( "descr" )
        # still need validater
        # still default func  None
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
        self.type_sub_field     = edit_field
        edit_field.setPlaceholderText( "type_sub" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
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
        self.cmnt_field     = edit_field
        edit_field.setPlaceholderText( "cmnt" )
        # still need validater
        # still default func  None
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
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- m_name
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "m_name",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.m_name_field     = edit_field
        edit_field.setPlaceholderText( "m_name" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field )


        # ---- dt_item
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "dt_item",
                                                db_type        = "integer",
                                                display_type   = "timestamp",
                                                 )
        self.dt_item_field     = edit_field
        edit_field.setPlaceholderText( "dt_item" )
        # still need validater
        # still default func  None
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
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
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
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- dddd
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "dddd",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.dddd_field     = edit_field
        edit_field.setPlaceholderText( "dddd" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- department
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "department",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.department_field     = edit_field
        edit_field.setPlaceholderText( "department" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- floor
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "floor",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.floor_field     = edit_field
        edit_field.setPlaceholderText( "floor" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- location
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "location",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.location_field     = edit_field
        edit_field.setPlaceholderText( "location" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- role_text
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "role_text",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.role_text_field     = edit_field
        edit_field.setPlaceholderText( "role_text" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- assoc_msn
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "assoc_msn",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.assoc_msn_field     = edit_field
        edit_field.setPlaceholderText( "assoc_msn" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- bussiness_house
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "bussiness_house",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.bussiness_house_field     = edit_field
        edit_field.setPlaceholderText( "bussiness_house" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- country
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "country",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.country_field     = edit_field
        edit_field.setPlaceholderText( "country" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- autodial
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "autodial",
                                                db_type        = "integer",
                                                display_type   = "integer",
                                                 )
        self.autodial_field     = edit_field
        edit_field.setPlaceholderText( "autodial" )
        # still need validater
        # still default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )

        # ---- code_gen: detail_tab_build_gui use for _build_fields was_build_gui  -- end table entries

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
    def field_to_recordxxxx( self, record ):
        """
        for People now from photo
        for the updates, get the gui data into the record
        assume for new add time and id are already there?? or in a self.xxx
        since not sure how works put in instance
        we still need more fields her and probably in record to field
        """
        print( "field_to_record disabled ")
        return

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
        # self.table_name          = "stuff"  not needed we get fro parent

        super().__init__( parent_window )
        self.tab_name            = "PeopleTextTab"

        self.table              = "people_text"
        self.table_name         = self.table   # !! eliminate one or other

        self.post_init()

# ----------------------------------------
class PeopleHistorylTab( base_document_tabs.HistoryTabBase   ):

    def __init__(self, parent_window ):
        """
        """
        super().__init__( parent_window )

        self.tab_name            = "PeopleHistorylTab"

    # -------------------------------------
    def _build_guixxx( self ):
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

    # -------------------------------------
    def record_to_tablexxx( self, record ):
        """
        what it says read
        from photo plus code gen

        """
        table           = self.history_table

        a_id            = record.value( "id" )
        str_id          = str( a_id )

        ix_row          = self.find_id_in_table( a_id )
        if ix_row:
            print( f"found row {ix_row} in future update maybe")

        # ---- insert
        self.ix_seq     += 1
        row_position    = table.rowCount()
        table.insertRow( row_position )
        ix_col          = -1
        ix_row          = row_position   # or off by 1
        ix_col          = -1

        ix_col          += 1
        item             = QTableWidgetItem( str( self.ix_seq  ) )
        table.setItem( ix_row, ix_col, item   )

        # # begin code gen ?



        # ---- code_gen: history tab -- build_gui -- begin table entries

        ix_col          += 1
        item             = QTableWidgetItem( str( record.value( "id" ) ) )
        table.setItem( ix_row, ix_col, item   )


        ix_col          += 1
        item             = QTableWidgetItem( str( record.value( "name" ) ) )
        table.setItem( ix_row, ix_col, item   )



        # ---- code_gen: history tab -- build_gui -- end table entries


        # ----- end code gen

# ----------------------------------------
class PeopleEventSubTab( base_document_tabs.SubTabBase ):
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
        #self.current_id      = 28
        #print( "fix people event select and delete line above should be select_by_id  ")
        self._build_model()
        self._build_gui()

        self.parent_window.sub_tab_list.append( self )    # a function might be better

        #self.select_all_for_test()

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says, read
        !! initial query should come out

        """
        page            = self
        tab             = page
        # a_notebook.addTab( page, 'Channels ' )
        # placer          = gui_qt_ext.PlaceInGrid(
        #     central_widget=page,
        #     a_max=0,
        #     by_rows=False  )

        layout                     = QVBoxLayout( tab )
        button_layout              = QHBoxLayout()

        layout.addLayout( button_layout )

        # Set up the model

        # Line 20 sets the edit strategy of the model to OnFieldChange.
        # This strategy allows the model to automatically update the data
        # in your database if the user modifies any of the data directly in the view.

        # model.setHeaderData( 0, Qt.Horizontal, "ID")
        # model.setHeaderData( 1, Qt.Horizontal, "YT ID"  )
        # model.setHeaderData( 2, Qt.Horizontal, "Name"   )
        # model.setHeaderData( 3, Qt.Horizontal, "Url")
        # model.setHeaderData( 4, Qt.Horizontal, "mypref")
        # model.setHeaderData( 5, Qt.Horizontal, "mygroup")

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
        # model_write.setEditStrategy( QSqlTableModel.OnFieldChange )
        # model.setFilter( "people_id = 28 " )
        # print( "!!fix people_id = 28 ")

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
class PeopleContactSubTab( base_document_tabs.SubTabBase   ):
    """
    """
    def __init__(self, parent_window ):
        """
        """
        super().__init__( parent_window )
        #self.parent_window   = parent_window
        self.list_ixxx         = 5  # should track selected an item in detail


        self.table_name      = "people_contact"
        self.table_name      = "people_phone"
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
        model                = self.model
        #self.list_view       = view
        self.view            = view
        view.setModel( self.model )

        # print( "_build_gui  this may be in wrong place ")
        # layout.addWidget( view )
        #placer.place(  view )

        ix_col = -1   # could make loop or even list comp
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
        ix_col += 1
        model.setHeaderData( ix_col, Qt.Horizontal, "seq_id" )
        view.setColumnWidth( ix_col, 100)  # Set  width in  pixels

        ix_col += 1
        model.setHeaderData( ix_col, Qt.Horizontal, "people_id" )
        view.setColumnWidth( ix_col, 100)  # Set  width in  pixels

        ix_col += 1
        model.setHeaderData( ix_col, Qt.Horizontal, "type" )
        view.setColumnWidth( ix_col, 100)  # Set  width in  pixels

        ix_col += 1
        model.setHeaderData( ix_col, Qt.Horizontal, "phone_old" )
        view.setColumnWidth( ix_col, 100)  # Set  width in  pixels

        ix_col += 1
        model.setHeaderData( ix_col, Qt.Horizontal, "Comment" )
        view.setColumnWidth( ix_col, 300)  # Set  width in  pixels

        ix_col += 1
        model.setHeaderData( ix_col, Qt.Horizontal, "phone" )
        view.setColumnWidth( ix_col, 100)  # Set  width in  pixels

        ix_col += 1
        model.setHeaderData( ix_col, Qt.Horizontal, "autodial" )
        view.setColumnWidth( ix_col, 100)  # Set  width in  pixels

        #view.setColumnHidden( 1, True )  # view or model

        layout.addWidget( view )

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

        """
        model              = ContactSqlTableModel(  self, self.db    )
        self.model         = model

        model.setTable( self.table_name )
        model.setEditStrategy( QSqlTableModel.OnManualSubmit )

    # ---------------------------------
    def _build_model_old( self, ):
        """
        may have too many instances
        Returns:
            modifies self, establishes -- wrong names

        """

        #model              = QSqlTableModel( self, self.db )

        model              = qt_with_logging.QSqlTableModelWithLogging(  self, self.db    )

        #self.model_write   = model  # detete
        self.model         = model

        model.setTable( self.list_table_name )
        model.setEditStrategy( QSqlTableModel.OnManualSubmit )
        # model_write.setEditStrategy( QSqlTableModel.OnFieldChange )
        # model.setFilter( "people_id = 28 " )
        # print( "!!fix people_id = 28 ")

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
    def add_record(self):
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

    # ------------------------------------------
    def edit_record(self):
        """
        what it says, read?
        """
        index       = self.view.currentIndex()
        model       = self.model
        if index.isValid():
            dialog = people_document_edit.EditPeopleContact( self.model, index, parent = self )
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
        self.non_editable_columns = {0, 1, }  # Columns ..doe it have to be in init or is synamic ..

    def flags(self, index: QModelIndex):
        # Get default flags from the base class
        flags = super().flags(index)
        # Remove editable flag for the specified columns
        if index.column() in self.non_editable_columns:
            return flags & ~Qt.ItemIsEditable  # Make these columns non-editable
        return flags

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
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
# ---- eof ------------------------------
