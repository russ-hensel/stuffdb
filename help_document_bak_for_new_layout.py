#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""



"""
# ---- tof
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    main.main()
# --------------------



#from   functools import partial
#import collections
import functools
import logging
import pprint
#import sqlite3
import time
from functools import partial

import data_dict
import gui_qt_ext
import string_util
import text_edit_ext
from app_global import AppGlobal
import parameters


# ---- QtCore
from PyQt5.QtGui  import QFont
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
from PyQt5.QtCore import QDate, QModelIndex, Qt, QTimer, pyqtSlot
from PyQt5.QtGui import QIntValidator, QStandardItem, QStandardItemModel
# ---- QtSql
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
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
#import  document_maker
import base_document_tabs
import custom_widgets
import data_manager
#import  ia_qt
import key_words
import qt_sql_query

import example_code


# move to parameters
SYSTEM_LIST     = parameters.PARAMETERS.systems_list

LOG_LEVEL  = 5   # higher is more



# ----------------------------------------
class HelpDocument( base_document_tabs.DocumentBase ):
    """
    for the stuff table....
    """
    def __init__(self,  ):
        """
        the usual
        """
        super().__init__()

        # mdi_area                = AppGlobal.main_window.mdi_area
        #     #we could return the subwindow for parent to addS
        # sub_window              = self
        #     # sub_window.setWindowTitle( "this title may be replaced " )
        # self.db                 = AppGlobal.qsql_db_access.db

        self.detail_table_name  = "help_info"
        self.text_table_name    = "help_text"  # text tables always id and text_data
        self.help_filename      = "help_doc.txt"
        self.subwindow_name     = "HelpSubWindow"
        self.setWindowTitle( self.subwindow_name )

        AppGlobal.mdi_management.update_menu_item( self )

        self._build_gui()

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says
        """
        main_notebook           = self.tab_folder    # create in parent
        self.main_notebook      = main_notebook      #

        sub_window              = self
        mdi_area                = AppGlobal.main_window.mdi_area
        main_notebook.currentChanged.connect( self.on_tab_changed )

        ix                        = -1

        ix                       += 1
        self.criteria_tab_index   = ix
        self.criteria_tab         = HelpCriteriaTab( self )
        main_notebook.addTab(       self.criteria_tab, "Criteria" )

        ix                       += 1
        self.list_tab_index      = ix
        self.list_tab            = HelpListTab( self  )
        main_notebook.addTab(  self.list_tab,   "List"    )

        ix                       += 1
        self.detail_tab_index     = ix
        self.detail_tab           = HelpDetailTab( self )
        main_notebook.addTab( self.detail_tab,    "Detail"     )

        ix                        += 1
        self.history_tab_index     = ix
        self.history_tab           = HelpHistorylTab( self )
        main_notebook.addTab( self.history_tab ,   "History"    )

        sub_window.setWidget( main_notebook )
        mdi_area.addSubWindow( sub_window )

        sub_window.show()

    #-------------------------------------
    def default_new_row( self ):
        """
        defaults values for a new row in the detail and the
        text tabs

        Changes state of detail and related tabs

        """
        next_key      = AppGlobal.key_gen.get_next_key(   self.detail_table_name )
        self.detail_tab.default_new_row( next_key )
        self.text_tab.default_new_row(   next_key )

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
        print( f"Clicked on row {row}, column {column}, value tbd" ) # " value: {value}" )

    # ---- sub window interactions ---------------------------------------
     # ------------------------------------------
    def criteria_select( self,     ):
        """
        uses info in criteria tab to build list in list tab
        uses info from 2 tabs
        """
        self.criteria_tab.criteria_select()

        return


    # -----------------------------------
    def add_row_history( self, index ):
        """
        pretty much from chat

        def add_row_to_tab2(self, index):
        # Get the data from the selected row
        id_data = self.model1.data(self.model1.index(index.row(), 0))
        name_data = self.model1.data(self.model1.index(index.row(), 2))

        # Create items for the second model
        id_item = QStandardItem(str(id_data))
        name_item = QStandardItem(name_data)

        # Add a new row to the second model
        self.history_model.appendRow([id_item, name_item])

        """
        return


        # Get the data from the selected row
        detail_model    = self.detail_tab.tab_model
        history_model   = self.history_tab.history_model

        id_data         = detail_model.data( detail_model.index( index.row(), 0))
        name_data       = detail_model.data( detail_model.index( index.row(), 2))
        print( f"in add_row_history {id_data = }   {name_data = }")
        # Create items for the second model
        id_item     = QStandardItem( str(id_data) )
        name_item   = QStandardItem( name_data )

        # Add a new row to the second model
        history_model.appendRow([id_item, name_item])

    # ------------------------------------------
    def on_history_clicked( self, index: QModelIndex ):
        """
        !! finish me --- can i be promoted
        Args:
            index (QModelIndex): DESCRIPTION.

        !! promote the whole thing?? need key to be id col 0 seems ok
        might be functioalize if we use an argument for self.list.tab
        """
        print( f"on_history_clicked  save first if necessary")
        row                     = index.row()
        column                  = index.column()

        self.list_tab.list_ix   = row

        id_index                = self.history_tab.history_model.index( index.row( ), 0 )
        db_key                  = self.history_tab.history_model.data( id_index, Qt.DisplayRole )
        print( f"on_history_clicked Clicked on list row {row}, column {column}, {db_key = }" ) # " value: {value}" )

        self.fetch_row_by_id( db_key )

        # set tab
        self.main_notebook.setCurrentIndex( self.detail_tab_index )
        self.detail_tab.id_field.setText( str( db_key )  ) # fetch currently does not include the id

    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = "\n>>>>>>>>>>* HelpDocument  *<<<<<<<<<<<<"
        b_str   =  super().__str__(  )
        a_str   = a_str + "\n" + b_str

        return a_str

# ----------------------------------------
class HelpCriteriaTab( base_document_tabs.CriteriaTabBase ):
    """
    criteria for list selection
    """
    def __init__(self, parent_window ):
        """
        the usual  -- some is promotable

        """
        super().__init__( parent_window )
        self.tab_name               = "HelpCriteriaTab"


    # ------------------------------------------
    def _build_tab( self,   ):
        """
        what it says, read
        put page into the notebook
        """
        page            = self
        tab             = page

        placer          = gui_qt_ext.PlaceInGrid(
            central_widget  = page,
            a_max           = 0,
            by_rows         = False  )

        self._build_top_widgets( placer )

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

        # ---- "Key Words"
        placer.new_row()
        widget  = QLabel( "Key Words" )
        placer.place( widget )

        widget                    = custom_widgets.CQLineEditCriteria( get_type = "string", set_type = "string")
        self.key_words_widget     = widget
        widget.setPlaceholderText( "key_words"  )
        widget.critera_name       = "key_words"
        widget.functon_on_return  = self.criteria_select
        self.critera_widget_list.append( widget )
        widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        placer.place( widget )

        # ---- placer.new_row()
        placer.new_row()
        widget  = QLabel( "Title (like)" )
        placer.place( widget )

        widget                  = custom_widgets.CQLineEditCriteria( get_type = "string", set_type = "string")
        self.title_widget       = widget
        widget.critera_name     = "title"
        widget.functon_on_return  = self.criteria_select
        self.critera_widget_list.append( widget )
        widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        placer.place( widget, columnspan = 2 )

        # ---- system placer.new_row()
        placer.new_row()
        widget          = QLabel( "System" )
        placer.place( widget  )

        widget                  = custom_widgets.CQComboBoxEditCriteria( get_type = "string", set_type = "string")
        self.system_widget      = widget
        widget.critera_name     = "system"
        self.critera_widget_list.append( widget )

        placer.place( widget )
        widget.addItems( SYSTEM_LIST )
        # widget.addItem( '' )


        widget.setCurrentIndex( 0 )

        # ---- Order by
        placer.new_row()
        widget  = QLabel( "Order by" )
        placer.place( widget )

        widget                 = custom_widgets.CQComboBoxEditCriteria( get_type = "string", set_type = "string")
        self.order_by_widget   = widget
        self.critera_widget_list.append( widget )
        widget.critera_name    = "order_by"

        widget.addItem('title - ignore case')
        widget.addItem('descr')
        widget.addItem('name')
        widget.addItem('system')
        widget.addItem("name - ignore case")
        widget.addItem('id')
        widget.addItem('id_old')
        # widget.addItem('Title??')

        print( f"{self.tab_name} build_tab build criteria change put in as marker ")
        widget.currentIndexChanged.connect( lambda: self.criteria_changed(  True   ) )
        placer.place( widget )

        # ---- Order by Direction
        #placer.new_row()
        widget  = QLabel( "Direction" )
        placer.place( widget )

        widget                      = custom_widgets.CQComboBoxEditCriteria( get_type = "string", set_type = "string")
        self.order_by_dir_widget    = widget
        #widget.functon_on_return    = self.criteria_select
        self.critera_widget_list.append( widget )
        widget.critera_name    = "order_by_dir"

        widget.addItem('Ascending')
        widget.addItem('Decending')
        # widget.addItem('id')
        # widget.addItem('Title??')

        print( f"{self.tab_name} build_tab build criteria change put in as marker ")
        widget.currentIndexChanged.connect( lambda: self.criteria_changed(  True   ) )
        placer.place( widget )

        # ---- criteria changed should be in parent
        placer.new_row()
        widget  = QLabel( "criteria_changed_widget" )
        self.criteria_changed_widget  = widget
        placer.place( widget )

    # -------------
    def criteria_select( self,     ):
        """
        moved down from document
        uses info in criteria tab to build list in list tab
        uses info from 2 tabs

        test in sql browser -- when testing look out for bind variables

            use fully qualified names in all sql

        """
        print( "criteria_select in Help doc,  needs work add dates " )

        parent_document                 = self.parent_window

        help_document                   = self.parent_window

        model                           = help_document.list_tab.list_model

        # ---- try this to clear
        model.setFilter( f"id = -99" )
        model.select()

        #rint( "begin channel_select for the list")
        query                           = QSqlQuery()
        query_builder                   = qt_sql_query.QueryBuilder( query, print_it = True  )

        kw_table_name                   = "help_key_words"
        #column_list                     = [ "id",   "title", "system", "key_words"   ]

        # !! next is too much
        columns         = data_dict.DATA_DICT.get_list_columns( self.parent_window.detail_table_name )
        #col_head_texts   = [ "seq" ]  # plus one for sequence
        col_names       = [   ]
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
            add_where       =  f' help_info.id = {table_id} '
            query_builder.add_to_where( add_where, [ ])

        # ---- id_old
        id_old     = criteria_dict[ "id_old" ].strip().lower()
        if id_old:
            add_where       =  f' help_info.id_old = "{id_old}" '
            query_builder.add_to_where( add_where, [ ])

        # ---- system
        system     = criteria_dict[ "system" ].strip().lower()
        if system:
            add_where       =  f' lower(help_info.system)= "{system}" '
            query_builder.add_to_where( add_where, [ ])

        # ---- key words
        criteria_key_words              = criteria_dict[ "key_words" ]
        criteria_key_words              = a_key_word_processor.string_to_key_words( criteria_key_words )
        key_word_count                  = len( criteria_key_words )

        criteria_key_words              = ", ".join( [ f'"{i_word}"' for i_word in criteria_key_words ] )
        criteria_key_words              = f'( {criteria_key_words} ) '    # ( "one", "two" )

        if key_word_count > 0:
            query_builder.group_by_c_list   = column_list
            query_builder.sql_inner_join    = " help_key_word  ON help_info.id = help_key_word.id "
            query_builder.sql_having        = f" count(*) = {key_word_count} "

            query_builder.add_to_where( f" key_word IN {criteria_key_words}" , [] )

        #- ---- title like
        title                          = criteria_dict[ "title" ].strip().lower()
        if title:
            add_where       = "lower( help_info.title )  like :title"   # :is name of bind var below
            #where_dict      = {"channel_name_like":  f"%{channel_name_like}%"}
            #query_builder.add_to_where( add_where, where_dict )
            query_builder.add_to_where( add_where, [(  ":title",  f"%{title}%" ) ])

        # ---- order by may need work

        # ---- order by

        # widget.addItem('title - ignore case')
        # widget.addItem('descr')
        # widget.addItem('name')


        order_by   = criteria_dict[ "order_by" ]

        if   order_by == "title - ignore case":
            column_name = "lower(help_info.title)"

        elif order_by == "system":
            column_name = "help_info.system"

        elif order_by == "name - ignore case":
            column_name = "lower(help_info.name)"

        elif order_by == "id":
            column_name = "help_info.id"

        elif order_by == "id_old":
            column_name = "help_info.id_old"

        else:   # !! might better handel this
            print( "order by issue, getting default column ")
            column_name = "help_info.title"

        # widget.addItem('Ascending')
        # widget.addItem('Decending')
        order_by_dir   = criteria_dict[ "order_by_dir" ].lower( )

        debug_msg     = f"help_document >>>>>> {column_name = }  {order_by_dir = }"
        #logging.debug( debug_msg )
        logging.log( LOG_LEVEL,  debug_msg, )

        if "asc" in order_by_dir:
            literal   = "ASC"
        else:
            literal   = "DESC"

        query_builder.add_to_order_by(  column_name, literal,   )

        query_builder.prepare_and_bind()

        msg      = f"{query_builder = }"
        logging.log( LOG_LEVEL,  debug_msg, )

        is_ok   = AppGlobal.qsql_db_access.query_exec_model( query,
                                                  model,
                                                  msg = "HelpSubWindow criteria_select" )

        # parent_document might be improvement !!
        help_document.main_notebook.setCurrentIndex( help_document.list_tab_index )
        self.critera_is_changed = False

    # -----------------------------
    def search_me(self, criteria ):
        """
        external search should be overridden in each document type
        for now just key words

            save
            activate criteria tab
            clear criteria
            set value of key words with criteria
                self.key_words_widget
            run criteria select


        """
        parent_window    = self.parent_window
        parent_window.update_db()

        criteria  = criteria.strip()

        # msg   = f"made it to help document {criteria =}"
        # logging.debug( msg )

        # tab_widget.setCurrentIndex( tab_index )
        tab_index     = parent_window.criteria_tab_index

        parent_window.tab_folder.setCurrentIndex(  tab_index )
        self.clear_criteria()

        self.key_words_widget.set_data( criteria )

        self.criteria_select_if()    # may need to select is changed

# ----------------------------------------
class HelpListTab( base_document_tabs.ListTabBase  ):

    def __init__(self, parent_window ):
        """

        """
        super().__init__( parent_window )

        self.list_ix            = 5  # should track selected an item in detail
            # needs work
        self.tab_name           = "HelpListTab"

        self._build_gui()

    # ------------------------------------------
    def _build_guipromoted( self,  ):
        """
        what it says, read
        !! initial query should come out

        """
        page            = self
        tab             = page
        #a_notebook.addTab( page, 'Channels ' )
        placer          = gui_qt_ext.PlaceInGrid(
            central_widget  = page,
            a_max           = 0,
            by_rows         = False  )

        # Set up the model
        model               = QSqlTableModel( self, self.parent_window.db ) # perhaps a global
        self.list_model     = model

        model.setTable( self.parent_window.detail_table_name )
        # Line 20 sets the edit strategy of the model to OnFieldChange.
        # This strategy allows the model to automatically update the data
        # in your database if the user modifies any of the data directly in the view.
        model.setEditStrategy( QSqlTableModel.OnFieldChange )

        # COMMENT  out to default
        # model.setHeaderData( 0, Qt.Horizontal, "ID")

        view                 = QTableView()
        self.list_view       = view
        view.setModel( model )
        placer.place(  view )
        view.clicked.connect( self.parent_window.on_list_clicked )

# ----------------------------------------
class HelpDetailTab( base_document_tabs.DetailTabBase  ):
    """
    """
    def __init__(self, parent_window  ):
        """
        Args:
            parent_window (TYPE): DESCRIPTION.

        """
        super().__init__( parent_window )

        self.tab_name               = "HelpDetailTab"
        self.key_word_table_name    = "help_key_word"

        # ---- post init
        self.post_init()

        #self.text_edit_ext_obj


    #-------------------------------------
    def _build_gui( self ):
        """
        lets assume the gui is really build
        by the detail tab so do not do anything here
        but capture the field names in

        self.fake_gui( a_foreign_layout )
        Returns:
            none
        """
        # post init will have buildt up db manager for detail bu
        # not for text ( unless in different page, lets do this here )

        text_model                   = QSqlTableModel(
                                          self, AppGlobal.qsql_db_access.db )
        self.text_model              = text_model
        text_model.setTable( "help_text" )

        # ---- data maanager
        self.text_data_manager      = data_manager.DataManager( self.text_model )
        # next is a bit ass backwards
        self.pseodo_text_tab        = self.text_data_manager
        #self.text_data_manager.next_key_function     = AppGlobal.key_gen.get_next_key
                # a_key_gen               = key_gen.KeyGenerator( a_qsql_db_access.db  )  #  AppGlobal.qsql_db_access.db
                # AppGlobal.key_gen       = a_key_gen.key_gen     # some_function( table_name )
        # if self.key_word_table_name != "":
        #     self.data_manager.enable_key_words(  self.key_word_table_name  )

        page            = self
        tab             = self

        box_layout_1    =  QVBoxLayout( page )

        if False:
            placer          = gui_qt_ext.PlaceInGrid(
                                central_widget  = box_layout_1,
                                a_max           = 8,
                                by_rows         = False  )

            layout          = placer

        else:
            layout          = gui_qt_ext.CQGridLayout( col_max = 8,  )
            box_layout_1.addLayout( layout )
            # CQGridLayout

# layout.setColumnStretch(0, 1)  # First column takes 1 part of horizontal space
# layout.setColumnStretch(1, 2)  # Second column takes 2 parts (wider than first)
# layout.setRowStretch(0, 2)     # First row takes 2 parts of vertical space
# layout.setRowStretch(1, 1)


        tab_layout      = layout

        # ----fields
        self._build_fields( layout  )

        # ---- text fields
        self._build_text_gui( box_layout_1 )

        # ---- tab pages
        detail_notebook           = QTabWidget()
        self.detail_notebook      = detail_notebook

        # # ---- buttons
        # button_layout = QHBoxLayout()

        # # fetch_button = QPushButton("Fetch")
        # # fetch_button.clicked.connect(self.fetch_detail_row)
        # # button_layout.addWidget(fetch_button)


    #-------------------------------------
    def build_gui_layout( self ):
        """
        """

    #-------------------------------------
    def build_gui_layout_test( self ):
        """
        """

    #-------------------------------------
    def build_gui_layout_stable( self ):
        """
        """




    #---------------------------------
    def _build_fields( self, layout ):
        """
        What it says, read
                tweaks    may need         widget.setReadOnly( True )
                #---- system TO combo box
        for a grid# Row 1, Column 0, Span 1 row and 2 columns

        row_span      = 1 # default is 1
        col_span      = 1 # default is 1

        # rowSpan: (Optional) The number of rows the widget should span. Defaults to 1.
        # columnSpan: (Optional) The number of columns the widget should span. Defaults to 1.

        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget( widget, ix_row, ix_col, row_span, col_span )


        """
        # self._build_fields_test( layout )
        self._build_fields_stable( layout )

    #---------------------------------
    def _build_fields_test( self, layout ):
        """
        What it says, read
                tweaks    may need         widget.setReadOnly( True )
                # ---- system TO combo box
        for a grid# Row 1, Column 0, Span 1 row and 2 columns

        row_span      = 1 # default is 1
        col_span      = 1 # default is 1

        # rowSpan: (Optional) The number of rows the widget should span. Defaults to 1.
        # columnSpan: (Optional) The number of columns the widget should span. Defaults to 1.

        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget( widget, ix_row, ix_col, row_span, col_span )


        """
        # ---- code_gen: detail_tab_build_gui use for _build_fields was_build_gui  -- begin table entries
        # ---- code_gen: TableDict.to_build_form 2025_02_01 for help_info -- begin table entries -----------------------

        row_span      = 1
        col_span      = 1

        # for ix in range( 8 ):
        #     widget   = QLineEdit( )
        #     #widget   = QSpacerItem( 0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum )
        #     layout.addWidget( widget, columnspan = col_span  )

        # this seems to stabalize the grid at top not visible
        for ix in range( 8 ):
            widget   = QSpacerItem( 50, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
            layout.addItem( widget, 0, ix  )  # row column


        row_span      = 1
        col_span      = 1
        # ---- id
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "id",
                                                db_type        = "integer",
                                                display_type   = "integer",
                                                 )
        self.id_field               = edit_field
        edit_field.setPlaceholderText( "id" )
        edit_field.setReadOnly( True )
        edit_field.edit_to_rec      = edit_field.edit_to_rec_str_to_int
        edit_field.rec_to_edit      = edit_field.rec_to_edit_int_to_str
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = col_span  )

        # ---- id_old
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "id_old",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.id_old_field     = edit_field
        edit_field.setPlaceholderText( "id_old" )
        edit_field.setReadOnly( True )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = col_span  )

        # ---- title
        col_span      = 2
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
        layout.addWidget( edit_field, columnspan = 4  )

        # # ---- system
        # edit_field                  = custom_widgets.CQLineEdit(
        #                                         parent         = None,
        #                                         field_name     = "system",
        #                                         db_type        = "string",
        #                                         display_type   = "string",
        #                                          )
        # self.system_field     = edit_field
        # edit_field.setPlaceholderText( "system" )
        # # still validator / default func  None
        # self.data_manager.add_field( edit_field, is_key_word = True )
        # layout.addWidget( edit_field )

        # ---- system:  combo
        edit_field                  = custom_widgets.CQComboBox(
                                                parent         = None,
                                                field_name     = "system",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.system_field     = edit_field
        edit_field.setPlaceholderText( "system" )
        edit_field.clear()
        edit_field.add_items( SYSTEM_LIST )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = col_span  )


        # ---- sub_system
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "sub_system",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.sub_system_field     = edit_field
        edit_field.setPlaceholderText( "sub_system" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = col_span  )

        # ---- key_words
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "key_words",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.key_words_field     = edit_field
        edit_field.setPlaceholderText( "key_words" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = col_span  )

        # ---- java_package
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "java_package",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.java_package_field     = edit_field
        edit_field.setPlaceholderText( "package" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = col_span  )

        # ---- java_type
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "java_type",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.java_type_field     = edit_field
        edit_field.setPlaceholderText( "type" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = col_span  )

        # ---- java_name
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "java_name",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.java_name_field     = edit_field
        edit_field.setPlaceholderText( "name" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = col_span  )

        # ---- table_name
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "table_name",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.table_name_field     = edit_field
        edit_field.setPlaceholderText( "table_name" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = col_span  )

        # ---- column_name
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "column_name",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.column_name_field     = edit_field
        edit_field.setPlaceholderText( "column_name" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = col_span  )

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
        layout.addWidget( edit_field, columnspan = col_span  )

        # ---- edit_ts
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "edit_ts",
                                                db_type        = "integer",
                                                display_type   = "timestamp",
                                                 )
        self.edit_ts_field     = edit_field
        edit_field.setPlaceholderText( "edit_ts" )
        edit_field.edit_to_rec     = edit_field.edit_to_rec_str_to_int
        edit_field.rec_to_edit     = edit_field.rec_to_edit_int_to_str
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = col_span  )

        # ---- is_example
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "is_example",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.is_example_field     = edit_field
        edit_field.setPlaceholderText( "is_example" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = col_span  )

        # ---- can_execute
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "can_execute",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.can_execute_field     = edit_field
        edit_field.setPlaceholderText( "can_execute" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = col_span  )

    #---------------------------------
    def _build_fields_stable( self, layout ):
        """
        What it says, read
                tweaks    may need         widget.setReadOnly( True )
                # ---- system TO combo box
                for ix in range( 8 ):
                    widget   = QSpacerItem( 50, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
                    layout.addItem( widget, 0, ix  )  # row column

        self.system_field     = edit_field
        edit_field.setPlaceholderText( "system" )
        edit_field.clear()
        edit_field.add_items( SYSTEM_LIST )


        for a grid# Row 1, Column 0, Span 1 row and 2 columns

        row_span      = 1 # default is 1
        col_span      = 1 # default is 1

        # rowSpan: (Optional) The number of rows the widget should span. Defaults to 1.
        # columnSpan: (Optional) The number of columns the widget should span. Defaults to 1.

        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget( widget, ix_row, ix_col, row_span, col_span )

        think this sort of thing is obsolete
        edit_field.ct_prior   = partial( edit_field.do_ct_value, - 99 )
        edit_field.ct_default = partial( edit_field.do_ct_value, - 99 )

        """
        for ix in range( 8 ):  # layout.col_max
            widget   = QSpacerItem( 50, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
            layout.addItem( widget, 0, ix  )  # row column


        # ---- code_gen: TableDict.to_build_form 2025_02_01 for help_info -- begin table entries -----------------------

        # ---- id
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "id",
                                                db_type        = "integer",
                                                display_type   = "integer",
                                                 )
        self.id_field     = edit_field
        edit_field.setReadOnly( True )
        edit_field.setPlaceholderText( "id" )
        edit_field.edit_to_rec     = edit_field.edit_to_rec_str_to_int
        edit_field.rec_to_edit     = edit_field.rec_to_edit_int_to_str
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 1 )

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
        layout.addWidget( edit_field, columnspan = 1 )

        # ---- title
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "title",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.title_field     = edit_field
        edit_field.is_keep_prior_enabled        = True
        edit_field.setPlaceholderText( "title" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- system
        edit_field                  = custom_widgets.CQComboBox(
                                                parent         = None,
                                                field_name     = "system",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.system_field     = edit_field
        edit_field.setPlaceholderText( "system" )
        edit_field.clear()
        edit_field.add_items( SYSTEM_LIST )
        # still validator / default func  None
        edit_field.is_keep_prior_enabled        = True
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- sub_system
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "sub_system",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.sub_system_field     = edit_field
        edit_field.setPlaceholderText( "sub_system" )
        edit_field.is_keep_prior_enabled        = True
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- key_words
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "key_words",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.key_words_field     = edit_field
        edit_field.is_keep_prior_enabled        = True
        edit_field.setPlaceholderText( "key_words" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- java_package
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "java_package",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.java_package_field     = edit_field
        edit_field.is_keep_prior_enabled        = True
        edit_field.setPlaceholderText( "java_package" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- java_type
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "java_type",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.java_type_field     = edit_field
        edit_field.setPlaceholderText( "java_type" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- java_name
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "java_name",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.java_name_field     = edit_field
        edit_field.is_keep_prior_enabled        = True
        edit_field.setPlaceholderText( "java_name" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- table_name
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "table_name",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.table_name_field     = edit_field
        edit_field.setPlaceholderText( "table_name" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- column_name
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "column_name",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.column_name_field     = edit_field
        edit_field.setPlaceholderText( "column_name" )
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

        # ---- edit_ts
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "edit_ts",
                                                db_type        = "integer",
                                                display_type   = "timestamp",
                                                 )
        self.edit_ts_field     = edit_field
        edit_field.setPlaceholderText( "edit_ts" )
        edit_field.edit_to_rec     = edit_field.edit_to_rec_str_to_int
        edit_field.rec_to_edit     = edit_field.rec_to_edit_int_to_str
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- is_example
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "is_example",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.is_example_field     = edit_field
        edit_field.setPlaceholderText( "is_example" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )





    #---------------------------------
    def _build_fields_bak_2( self, layout ):
        """
        What it says, read
                tweaks    may need         widget.setReadOnly( True )
                # ---- system TO combo box
        for a grid# Row 1, Column 0, Span 1 row and 2 columns

        row_span      = 1 # default is 1
        col_span      = 1 # default is 1

        # rowSpan: (Optional) The number of rows the widget should span. Defaults to 1.
        # columnSpan: (Optional) The number of columns the widget should span. Defaults to 1.

        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget( widget, ix_row, ix_col, row_span, col_span )

        think this sort of thing is obsolete
        edit_field.ct_prior   = partial( edit_field.do_ct_value, - 99 )
        edit_field.ct_default = partial( edit_field.do_ct_value, - 99 )

        """
        # ---- code_gen: detail_tab_build_gui use for _build_fields was_build_gui  -- begin table entries
        # ---- code_gen: TableDict.to_build_form 2025_02_01 for help_info -- begin table entries -----------------------

        row_span      = 1
        col_span      = 1
        # ---- id
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "id",
                                                db_type        = "integer",
                                                display_type   = "integer",
                                                 )
        self.id_field               = edit_field
        edit_field.setPlaceholderText( "id" )
        edit_field.setReadOnly( True )
        edit_field.edit_to_rec      = edit_field.edit_to_rec_str_to_int
        edit_field.rec_to_edit      = edit_field.rec_to_edit_int_to_str
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = col_span  )

        # ---- id_old
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "id_old",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.id_old_field     = edit_field
        edit_field.setPlaceholderText( "id_old" )
        edit_field.setReadOnly( True )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = col_span  )

        # ---- title
        col_span      = 1
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
        layout.addWidget( edit_field, columnspan = col_span  )

        # # ---- system
        # edit_field                  = custom_widgets.CQLineEdit(
        #                                         parent         = None,
        #                                         field_name     = "system",
        #                                         db_type        = "string",
        #                                         display_type   = "string",
        #                                          )
        # self.system_field     = edit_field
        # edit_field.setPlaceholderText( "system" )
        # # still validator / default func  None
        # self.data_manager.add_field( edit_field, is_key_word = True )
        # layout.addWidget( edit_field )

        # ---- system:  combo
        edit_field                  = custom_widgets.CQComboBox(
                                                parent         = None,
                                                field_name     = "system",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.system_field     = edit_field
        edit_field.setPlaceholderText( "system" )
        edit_field.clear()
        edit_field.add_items( SYSTEM_LIST )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = col_span  )


        # ---- sub_system
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "sub_system",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.sub_system_field     = edit_field
        edit_field.setPlaceholderText( "sub_system" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = col_span  )

        # ---- key_words
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "key_words",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.key_words_field     = edit_field
        edit_field.setPlaceholderText( "key_words" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = col_span  )

        # ---- java_package
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "java_package",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.java_package_field     = edit_field
        edit_field.setPlaceholderText( "package" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = col_span  )

        # ---- java_type
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "java_type",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.java_type_field     = edit_field
        edit_field.setPlaceholderText( "type" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = col_span  )

        # ---- java_name
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "java_name",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.java_name_field     = edit_field
        edit_field.setPlaceholderText( "name" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = col_span  )

        # ---- table_name
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "table_name",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.table_name_field     = edit_field
        edit_field.setPlaceholderText( "table_name" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = col_span  )

        # ---- column_name
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "column_name",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.column_name_field     = edit_field
        edit_field.setPlaceholderText( "column_name" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = col_span  )

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
        layout.addWidget( edit_field, columnspan = col_span  )

        # ---- edit_ts
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "edit_ts",
                                                db_type        = "integer",
                                                display_type   = "timestamp",
                                                 )
        self.edit_ts_field     = edit_field
        edit_field.setPlaceholderText( "edit_ts" )
        edit_field.edit_to_rec     = edit_field.edit_to_rec_str_to_int
        edit_field.rec_to_edit     = edit_field.rec_to_edit_int_to_str
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = col_span  )

        # ---- is_example
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "is_example",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.is_example_field     = edit_field
        edit_field.setPlaceholderText( "is_example" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = col_span  )

        # ---- can_execute
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "can_execute",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.can_execute_field     = edit_field
        edit_field.setPlaceholderText( "can_execute" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = col_span  )

    #---------------------------------
    def _build_fields_bak_1( self, layout ):
        """
        worked but change order
        What it says, read
                tweaks    may need         widget.setReadOnly( True )
                # ---- system TO combo box
        for a grid# Row 1, Column 0, Span 1 row and 2 columns
        """
        # ---- code_gen: detail_tab_build_gui use for _build_fields was_build_gui  -- begin table entries

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


        # ---- sub_system
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "sub_system",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.sub_system_field     = edit_field
        edit_field.setPlaceholderText( "sub_system" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- system line
        # edit_field                  = custom_widgets.CQLineEdit(
        #                                         parent         = None,
        #                                         field_name     = "system",
        #                                         db_type        = "string",
        #                                         display_type   = "string",
        #                                          )
        # self.system_field     = edit_field
        # edit_field.setPlaceholderText( "system" )
        # # still validator / default func  None
        # self.data_manager.add_field( edit_field, is_key_word = True )
        # layout.addWidget( edit_field )

        # ---- system combo
        edit_field                  = custom_widgets.CQComboBox(
                                                parent         = None,
                                                field_name     = "system",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.system_field     = edit_field
        edit_field.setPlaceholderText( "system" )
        edit_field.clear()
        edit_field.add_items( SYSTEM_LIST )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field )


        # ---- key_words
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "key_words",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.key_words_field     = edit_field
        edit_field.setPlaceholderText( "key_words" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field )


        # ---- edit_ts
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "edit_ts",
                                                db_type        = "integer",
                                                display_type   = "timestamp",
                                                 )
        self.edit_ts_field     = edit_field
        edit_field.setPlaceholderText( "edit_ts" )
        edit_field.edit_to_rec     = edit_field.edit_to_rec_str_to_int
        edit_field.rec_to_edit     = edit_field.rec_to_edit_int_to_str
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- table_name
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "table_name",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.table_name_field     = edit_field
        edit_field.setPlaceholderText( "table_name" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field )


        # ---- column_name
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "column_name",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.column_name_field     = edit_field
        edit_field.setPlaceholderText( "column_name" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- java_type
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "java_type",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.java_type_field     = edit_field
        edit_field.setPlaceholderText( "java_type" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- java_name
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "java_name",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.java_name_field     = edit_field
        edit_field.setPlaceholderText( "java_name" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- java_package
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "java_package",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.java_package_field     = edit_field
        edit_field.setPlaceholderText( "java_package" )
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


        # ---- is_example
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "is_example",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.is_example_field     = edit_field
        edit_field.setPlaceholderText( "is_example" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


        # ---- can_execute
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "can_execute",
                                                db_type        = "string",
                                                display_type   = "string",
                                                 )
        self.can_execute_field     = edit_field
        edit_field.setPlaceholderText( "can_execute" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field )


    #---------------------------------
    def _build_fields_bak( self, layout ):
        """
        What it says, read
                tweaks    may need         widget.setReadOnly( True )


        for a grid# Row 1, Column 0, Span 1 row and 2 columns
        """
        # ---- code_gen: detail_tab_build_gui use for _build_fields was_build_gui  -- begin table entries
                                                # qdates make these non editable

        print( "help detail most of fields commentd out for debug --------------------------------------")
        # ---- id
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "id",
                                                db_type        = "integer",
                                                display_type   = "string" )
        self.id_field         = edit_field
        edit_field.setReadOnly( True )
        #edit_field.ct_prior   = edit_field.do_ct_prior
        edit_field.ct_prior   = partial( edit_field.do_ct_value, - 99 )
        edit_field.ct_default = partial( edit_field.do_ct_value, - 99 )
        #edit_field.setPlaceholderText( "id" )
        self.data_manager.add_field( edit_field )
        layout.addWidget( edit_field )

        # ---- id_old
        edit_field              = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "id_old",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.id_old_field       = edit_field
        edit_field.setReadOnly( True )
        edit_field.setPlaceholderText( "id_old" )
        self.data_manager.add_field( edit_field )
        layout.addWidget( edit_field )



        # # # ---- add_ts
        # # edit_field                  = custom_widgets.CQDateEdit(
        # #                                         parent         = None,
        # #                                         field_name     = "add_ts",
        # #                                         db_type        = "timestamp",
        # #                                         display_type   = "qdate" )
        # # self.add_ts_field         = edit_field
        # # #edit_field.setPlaceholderText( "add_ts" )
        # # self.data_manager.add_field( edit_field )
        # # layout.addWidget( edit_field )

        # #        # timestamp to qdates make these non editable

        # # # ---- edit_ts
        # # edit_field                  = custom_widgets.CQDateEdit(
        # #                                         parent         = None,
        # #                                         field_name     = "edit_ts",
        # #                                         db_type        = "timestamp",
        # #                                         display_type   = "qdate" )
        # # self.edit_ts_field         = edit_field
        # # #edit_field.setPlaceholderText( "edit_ts" )
        # # self.data_manager.add_field( edit_field )
        # # layout.addWidget( edit_field )

        # # ---- table_name
        # edit_field                  = custom_widgets.CQLineEdit(
        #                                         parent         = None,
        #                                         field_name     = "table_name",
        #                                         db_type        = "string",
        #                                         display_type   = "string" )
        # self.table_name_field         = edit_field
        # edit_field.setPlaceholderText( "table_name" )
        # self.data_manager.add_field( edit_field )
        # layout.addWidget( edit_field )

        # # ---- column_name
        # edit_field                  = custom_widgets.CQLineEdit(
        #                                         parent         = None,
        #                                         field_name     = "column_name",
        #                                         db_type        = "string",
        #                                         display_type   = "string" )
        # self.column_name_field         = edit_field
        # edit_field.setPlaceholderText( "column_name" )
        # self.data_manager.add_field( edit_field )
        # layout.addWidget( edit_field )

        # # ---- java_type
        # edit_field                  = custom_widgets.CQLineEdit(
        #                                         parent         = None,
        #                                         field_name     = "java_type",
        #                                         db_type        = "string",
        #                                         display_type   = "string" )
        # self.java_type_field         = edit_field
        # edit_field.setPlaceholderText( "java_type" )
        # self.data_manager.add_field( edit_field )
        # layout.addWidget( edit_field )

        # # ---- java_name
        # edit_field                  = custom_widgets.CQLineEdit(
        #                                         parent         = None,
        #                                         field_name     = "java_name",
        #                                         db_type        = "string",
        #                                         display_type   = "string" )
        # self.java_name_field         = edit_field
        # edit_field.setPlaceholderText( "java_name" )
        # self.data_manager.add_field( edit_field )
        # layout.addWidget( edit_field )



        # ---- title
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "title",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.title_field         = edit_field
        edit_field.setPlaceholderText( "title" )
        self.data_manager.add_field( edit_field,  is_key_word = True )
        layout.new_row()
        layout.addWidget( edit_field, columnspan = 2 )


        # ---- key_words
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "key_words",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.key_words_field         = edit_field
        edit_field.setPlaceholderText( "key_words" )
        self.data_manager.add_field( edit_field, is_key_word = True )

        layout.addWidget( edit_field, columnspan = 2 )


        # ---- java_package
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "java_package",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.java_package_field         = edit_field
        edit_field.setPlaceholderText( "java_package" )
        self.data_manager.add_field( edit_field )
        layout.addWidget( edit_field )

        # ---- type
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "type",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.type_field         = edit_field
        edit_field.setPlaceholderText( "type" )
        self.data_manager.add_field( edit_field )
        layout.addWidget( edit_field )

        # ---- sub_system
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "sub_system",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.sub_system_field         = edit_field
        edit_field.setPlaceholderText( "sub_system" )
        self.data_manager.add_field( edit_field )
        layout.addWidget( edit_field )

        # ---- system
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "system",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.system_field         = edit_field
        edit_field.setPlaceholderText( "system" )
        self.data_manager.add_field( edit_field )
        layout.addWidget( edit_field )




        # # ---- is_example
        # edit_field                  = custom_widgets.CQLineEdit(
        #                                         parent         = None,
        #                                         field_name     = "is_example",
        #                                         db_type        = "string",
        #                                         display_type   = "string" )
        # self.is_example_field         = edit_field
        # edit_field.setPlaceholderText( "is_example" )
        # self.data_manager.add_field( edit_field )
        # layout.addWidget( edit_field )

        # # ---- can_execute
        # edit_field                  = custom_widgets.CQLineEdit(
        #                                         parent         = None,
        #                                         field_name     = "can_execute",
        #                                         db_type        = "string",
        #                                         display_type   = "string" )
        # self.can_execute_field         = edit_field
        # edit_field.setPlaceholderText( "can_execute" )
        # self.data_manager.add_field( edit_field )
        # layout.addWidget( edit_field )

        # ---- code_gen: detail_tab_build_gui use for _build_fields was_build_gui  -- end table entries

        # ---- code_gen: detail_tab_build_gui use for _build_gui  -- begin table entries\


    # -------------------------------------
    def _build_text_gui( self, a_layout ):
        """
        like to build gui on text tabs borrowed here
        in help_document, try to make copy over to base document text tab
        we may be able to make this a method in base see base document ??
        """
        # self.build_text_gui_stable()
        self._build_text_gui_test( a_layout )

    # -------------------------------------
    def _build_text_gui_test( self, a_layout ):
        """
        like to build gui on text tabs borrowed here
        in help_document, try to make copy over to base document text tab
        we may be able to make this a method in base see base document ??
        """
        tab_layout      = QGridLayout( )
        a_layout.addLayout( tab_layout )

        data_manager    = self.text_data_manager

        ix_row          = 0
        ix_col          = 0

        # tab                 = self

        # tab_layout          = QGridLayout(tab)
        #     # widget: The widget you want to add to the grid.
        #     # row: The row number where the widget should appear (starting from 0).
        #     # column: The column number where the widget should appear (starting from 0).
        #     # rowSpan (optional): The number of rows the widget should span (default is 1).
        #     # columnSpan (optional): The number of columns the widget should span (default is 1).
        #     # alignment (optional): The ali
        # # could have a button layout down one side ??

        # ---- id
        ix_row      += 1
        ix_col       = 0
        widget                  =  custom_widgets.CQLineEdit(
                                     parent         = None,
                                     field_name     = "id",
                                     db_type        = "integer",
                                     display_type   = "string" )
        self.id_field               = widget
        widget.setReadOnly( True )
        data_manager.add_field( widget, ) # is_key_word = True )
        tab_layout.addWidget( widget, ix_row, ix_col )

        # ---- textedit   entry_widget         = QTextEdit()
        ix_row          += 1
        ix_col          = 1

        edit_field         = custom_widgets.CQTextEdit(
                                    parent         = None,
                                    field_name     = "text_data",
                                    db_type        = "string",   # or text ??
                                    display_type   = "string" )
        entry_widget        = edit_field
        font                = QFont( * parameters.PARAMETERS.text_edit_font ) # ("Arial", 12)
        edit_field.setFont(font)
        self.text_data_field = edit_field    # may be used for editing
        edit_field.setPlaceholderText( "Some Long \n   text on a new line " )
        data_manager.add_field( edit_field, )
        tab_layout.addWidget( edit_field, ix_row, ix_col,  4, 10 )  # what order row column

        # ---- template may not even need in self
        self.text_edit_ext_obj         = text_edit_ext.TextEditExt( AppGlobal.parameters, entry_widget)
        entry_widget.text_edit_ext_obj = self.text_edit_ext_obj
        text_edit_ext.STUFF_DB         = AppGlobal.controller
        ddl_widget, ddl_button_widget  = self.text_edit_ext_obj.build_up_template_widgets()

        ix_row          += 1
        ix_col          = 0
        label           = "Paste Prior"
        widget          = QPushButton( label )
        # connect_to  =  functools.partial( self.run_python_idle, entry_widget )
        # widget.clicked.connect( connect_to )
        widget.clicked.connect( self.text_edit_ext_obj.paste_cache )
        tab_layout.addWidget( widget, ix_row, ix_col )


        ix_row          += 1
        ix_col          = 0
        label           = "Paste Clip"
        widget          = QPushButton( label )
        # connect_to  =  functools.partial( self.run_python_idle, entry_widget )
        # widget.clicked.connect( connect_to )
        widget.clicked.connect( self.text_edit_ext_obj.paste_clipboard  )
        tab_layout.addWidget( widget, ix_row, ix_col )

        # ---- template may not even need in self
        self.text_edit_ext_obj         = text_edit_ext.TextEditExt( AppGlobal.parameters, entry_widget)
        ddl_widget, ddl_button_widget  = self.text_edit_ext_obj.build_up_template_widgets()

        ix_row          += 1
        ix_col          = 0
        tab_layout.addWidget( ddl_button_widget, ix_row, ix_col )

        ix_row          += 1
        ix_col          = 0
        tab_layout.addWidget( ddl_widget, ix_row, ix_col )

        ix_row          += 1
        ix_col          = 0
        label           = "Copy\nLine"
        widget = QPushButton( label )
        # connect_to  =  functools.partial( self.copy_line_of_text, entry_widget )
        # widget.clicked.connect( connect_to )
        tab_layout.addWidget( widget, ix_row, ix_col )

        ix_row          += 1
        ix_col          = 0
        label           = "run\npython idle"
        widget          = QPushButton( label )
        # connect_to  =  functools.partial( self.run_python_idle, entry_widget )
        # widget.clicked.connect( connect_to )
        #widget.clicked.connect( self.do_python )
        tab_layout.addWidget( widget, ix_row, ix_col )

        # ---- qt_exec
        ix_row          += 1
        ix_col          = 0
        label           = "qt_exec"
        widget          = QPushButton( label )
        #connect_to      = functools.partial( text_edit_ext.search_down, search_line_edit , entry_widget  )
        #down_button.clicked.connect( connect_to )
        connect_to  =  functools.partial( text_edit_ext.qt_exec, entry_widget )
        widget.clicked.connect( connect_to )
        # # widget.clicked.connect( self.qt_exec )
        tab_layout.addWidget( widget, ix_row, ix_col )

        # ix_row   += 1
        # label       = ">>"
        # widget      = QPushButton( label )
        # connect_to  =  functools.partial( text_edit_ext.cmd_exec, entry_widget )
        # widget.clicked.connect( connect_to )
        # tab_layout.addWidget ( widget, ix_row, 0,   )

        # ---- search text
        ix_row          -= 1
        ix_col          += 1
        widget                  = QLineEdit()
        search_line_edit        = widget
        widget.setPlaceholderText("Enter search text")
        tab_layout.addWidget( widget, ix_row, ix_col )

        # ---- up down Buttons
        ix_col          += 1
        widget                  = QPushButton("Down")
        down_button             = widget
        # connect below
        tab_layout.addWidget( widget, ix_row, ix_col )

        ix_col          += 1
        widget           = QPushButton("Up")
        up_button        = widget
        # connect below
        tab_layout.addWidget( widget, ix_row, ix_col )

        ix_row   += 1
        ix_col    = 1
        label       = ">>"
        widget      = QPushButton( label )
        connect_to  = functools.partial( text_edit_ext.cmd_exec, entry_widget )
        widget.clicked.connect( connect_to )
        tab_layout.addWidget ( widget, ix_row, ix_col,   )

        connect_to              = functools.partial( text_edit_ext.search_down, search_line_edit , entry_widget  )
        down_button.clicked.connect( connect_to )

        connect_to              = functools.partial( text_edit_ext.search_up, search_line_edit , entry_widget  )
        up_button.clicked.connect( connect_to )





    # -------------------------------------
    def _build_text_gui_stable( self, a_layout ):
        """
        like to build gui on text tabs borrowed here
        in help_document, try to make copy over to base document text tab
        we may be able to make this a method in base see base document ??
        """

        tab_layout      = QGridLayout( )
        a_layout.addLayout( tab_layout )

        data_manager    = self.text_data_manager

        ix_row          = 0
        ix_col          = 0

        # tab                 = self

        # tab_layout          = QGridLayout(tab)
        #     # widget: The widget you want to add to the grid.
        #     # row: The row number where the widget should appear (starting from 0).
        #     # column: The column number where the widget should appear (starting from 0).
        #     # rowSpan (optional): The number of rows the widget should span (default is 1).
        #     # columnSpan (optional): The number of columns the widget should span (default is 1).
        #     # alignment (optional): The ali
        # # could have a button layout down one side ??

        # ---- id
        ix_row      += 1
        ix_col       = 0
        widget                  =  custom_widgets.CQLineEdit(
                                     parent         = None,
                                     field_name     = "id",
                                     db_type        = "integer",
                                     display_type   = "string" )
        self.id_field               = widget
        widget.setReadOnly( True )
        data_manager.add_field( widget, ) # is_key_word = True )
        tab_layout.addWidget( widget, ix_row, ix_col )

        # ---- textedit   entry_widget         = QTextEdit()
        ix_row          += 1
        ix_col          = 1

        edit_field         = custom_widgets.CQTextEdit(
                                    parent         = None,
                                    field_name     = "text_data",
                                    db_type        = "string",   # or text ??
                                    display_type   = "string" )
        entry_widget        = edit_field
        font                = QFont( * parameters.PARAMETERS.text_edit_font ) # ("Arial", 12)
        edit_field.setFont(font)
        self.text_data_field = edit_field    # may be used for editing
        edit_field.setPlaceholderText( "Some Long \n   text on a new line " )
        data_manager.add_field( edit_field, )
        tab_layout.addWidget( edit_field, ix_row, ix_col,  4, 10 )  # what order row column

        # ---- template may not even need in self
        self.text_edit_ext_obj         = text_edit_ext.TextEditExt( AppGlobal.parameters, entry_widget)
        ddl_widget, ddl_button_widget  = self.text_edit_ext_obj.build_up_template_widgets()

        ix_row          += 1
        ix_col          = 0
        label           = "Paste Clip"
        widget          = QPushButton( label )
        # connect_to  =  functools.partial( self.run_python_idle, entry_widget )
        # widget.clicked.connect( connect_to )
        widget.clicked.connect( self.text_edit_ext_obj.paste_clipboard  )
        tab_layout.addWidget( widget, ix_row, ix_col )

        # ---- template may not even need in self
        self.text_edit_ext_obj         = text_edit_ext.TextEditExt( AppGlobal.parameters, entry_widget)
        text_edit_ext.STUFF_DB         = AppGlobal.controller
        ddl_widget, ddl_button_widget  = self.text_edit_ext_obj.build_up_template_widgets()

        ix_row          += 1
        ix_col          = 0
        tab_layout.addWidget( ddl_button_widget, ix_row, ix_col )

        ix_row          += 1
        ix_col          = 0
        tab_layout.addWidget( ddl_widget, ix_row, ix_col )

        ix_row          += 1
        ix_col          = 0
        label           = "Copy\nLine"
        widget = QPushButton( label )
        # connect_to  =  functools.partial( self.copy_line_of_text, entry_widget )
        # widget.clicked.connect( connect_to )
        tab_layout.addWidget( widget, ix_row, ix_col )

        ix_row          += 1
        ix_col          = 0
        label           = "run\npython idle"
        widget          = QPushButton( label )
        # connect_to  =  functools.partial( self.run_python_idle, entry_widget )
        # widget.clicked.connect( connect_to )
        #widget.clicked.connect( self.do_python )
        tab_layout.addWidget( widget, ix_row, ix_col )

        # ---- qt_exec
        ix_row          += 1
        ix_col          = 0
        label           = "qt_exec"
        widget          = QPushButton( label )
        #connect_to      = functools.partial( text_edit_ext.search_down, search_line_edit , entry_widget  )
        #down_button.clicked.connect( connect_to )
        connect_to  =  functools.partial( text_edit_ext.qt_exec, entry_widget )
        widget.clicked.connect( connect_to )
        # # widget.clicked.connect( self.qt_exec )
        tab_layout.addWidget( widget, ix_row, ix_col )

        # ix_row   += 1
        # label       = ">>"
        # widget      = QPushButton( label )
        # connect_to  =  functools.partial( text_edit_ext.cmd_exec, entry_widget )
        # widget.clicked.connect( connect_to )
        # tab_layout.addWidget ( widget, ix_row, 0,   )

        # ---- search text
        ix_row          -= 1
        ix_col          += 1
        widget                  = QLineEdit()
        search_line_edit        = widget
        widget.setPlaceholderText("Enter search text")
        tab_layout.addWidget( widget, ix_row, ix_col )

        # ---- up down Buttons
        ix_col          += 1
        widget                  = QPushButton("Down")
        down_button             = widget
        # connect below
        tab_layout.addWidget( widget, ix_row, ix_col )

        ix_col          += 1
        widget           = QPushButton("Up")
        up_button        = widget
        # connect below
        tab_layout.addWidget( widget, ix_row, ix_col )

        ix_row   += 1
        ix_col    = 1
        label       = ">>"
        widget      = QPushButton( label )
        connect_to  =  functools.partial( text_edit_ext.cmd_exec, entry_widget )
        widget.clicked.connect( connect_to )
        tab_layout.addWidget ( widget, ix_row, ix_col,   )

        connect_to              = functools.partial( text_edit_ext.search_down, search_line_edit , entry_widget  )
        down_button.clicked.connect( connect_to )

        connect_to              = functools.partial( text_edit_ext.search_up, search_line_edit , entry_widget  )
        up_button.clicked.connect( connect_to )



    # ----------------------------
    def fetch_detail_row( self,  id = None ):
        """
        Args:
            id can be external or as that has it fetched

        Returns:
            None.
        !! could be promoted
        """
        id      = self.id_field.text()
        debug_msg     = ( f"fetch_row { id = }")
        logging.log( LOG_LEVEL,  debug_msg, )
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
        #descr      = self.descr_field.text()
        add_kw     = self.add_kw_field.text()
        #print(  ia_qt.q_line_edit( self.name_field,
        #                   msg = "this is the name field",  ) # include_dir = True ) )
        # url      = self.url_field.text()
        # mypref   = self.mypref_field.text()
        # mygroup  = self.mygroup_field.text()
        # add_ts   = self.add_ts_field.text()
        edit_ts  = self.edit_ts_field.text()
        edit_ts  = "self.edit_ts_field.text()"   # !! test

        self.default_new_row(  next_key )

        # ---- set the defaults

        # self.descr_field.setText( descr + "*" )
        #self.url_field.setText( url )

        # # ---- ??redef add_ts
        # a_ts   = str( time.time() ) + "sec"

        # self.add_ts_field.setText(  a_ts )


    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = "\n>>>>>>>>>>* HelpDetailTab *<<<<<<<<<<<<"

        a_str   = string_util.to_columns( a_str, ["key_word_table_name",
                                           f"{self.key_word_table_name}" ] )

        a_str   = string_util.to_columns( a_str, ["detail_notebook",
                                           f"{self.detail_notebook}" ] )
        a_str   = string_util.to_columns( a_str, ["enable_send_topic_update",
                                           f"{self.enable_send_topic_update}" ] )

        return a_str

# ----------------------------------------
class HelpHistorylTab( base_document_tabs.HistoryTabBase  ):
    """
    """
    def __init__(self, parent_window ):
        """
        what it says read -- the usual -- note ancestor matters
        """
        super().__init__( parent_window )
        self.tab_name            = "HelpHistorylTab"


# ---- eof ------------------------------
