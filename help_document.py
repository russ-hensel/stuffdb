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

# ---- begin pyqt from import_qt.py

#from   functools import partial
import collections
import functools
import pprint
import sqlite3
import time

import gui_qt_ext
import string_util
from app_global import AppGlobal
# ---- QtCore
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

#import  document_maker
import base_document_tabs
import custom_widgets
#import  ia_qt
import key_words
import qt_sql_query


# ---- imports local


DATE_ZERO        = QDate(  1025, 1, 1 )
DATE_INFINITY    = QDate(  3025, 1, 1 )

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

        mdi_area                = AppGlobal.main_window.mdi_area
            #we could return the subwindow for parent to addS
        sub_window              = self
            # sub_window.setWindowTitle( "this title may be replaced " )
        self.db                 = AppGlobal.qsql_db_access.db

        self.detail_table_name  = "help_info"
        self.text_table_name    = "help_text"  # text tables always id and text_data

        self.prior_tab          = 0
        self.current_tab        = 0

        self.prior_criteria     = None
        self.current_criteria   = None    # init just after criteria tab created

        self.subwindow_name     = "HelpSubWindow"
        self.setWindowTitle( self.subwindow_name )

        AppGlobal.mdi_management.update_menu_item( self )

        self._build_gui()

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
        self.criteria_tab         = HelpCriteriaTab( self )
        main_notebook.addTab(       self.criteria_tab,  "Criteria" )

        ix                       += 1
        self.list_tab_index      = ix
        self.list_tab            = HelpListTab( self  )
        main_notebook.addTab(  self.list_tab  ,   "List"    )

        ix                       += 1
        self.detail_tab_index     = ix
        self.detail_tab           = HelpDetailTab( self )
        main_notebook.addTab( self.detail_tab,    "Detail"     )

        ix                         += 1
        self.detail_text_index      = ix
        self.text_tab               = HelpTextTab(  self )
        main_notebook.addTab( self.text_tab,    "Text"     )

        # now some magic? ref fields normally on the text tab to be on
        # detail tab
        #self.text_tab.fake_gui( self.detail_tab )   # moves ref to text_tab

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

        id_index                = self.list_tab.list_model.index( index.row( ), 0 )
        db_key                  = self.list_tab.list_model.data( id_index, Qt.DisplayRole )
        #print( f"photo Clicked on list row {row}, column {column}, {db_key = }" )

        self.select_record( db_key )

        self.main_notebook.setCurrentIndex( self.detail_tab_index )

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

    # --------------------------
    def on_tab_changed_promoted( self, event ):
        """
        not currently use, but may trigger a save or other action
        in the future
        """
        #old_prior               = self.prior_tab
        self.prior_tab          = self.current_tab  # because not updated yet
        self.current_tab        = self.main_notebook.currentIndex()
        current_text            = self.main_notebook.tabText( self.current_tab )
        #rint( f"on_tab_changed {self.prior_tab = } {self.current_tab = }   {current_text = }" )

        # # could be done at any time
        # self.tap_page_Stuff_fn   = self.a_notebook.tab( self.a_notebook.select(), 'text' ) + ".txt"
        # print( f"tap_page_Stuff_fn  >>{self.tap_page_Stuff_fn}<< "
        #        "for tabpage on_changed need to remove spaces" )
        # #rint( f"on_changed  {event} for tabpage" )
        # #rint( self.get_info() )

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
        a_str   = ">>>>>>>>>>* HelpDocument  *<<<<<<<<<<<<"

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


        widget                  = custom_widgets.CQLineEditCriteria( get_type = "string", set_type = "string")
        self.key_words_widget   = widget
        widget.critera_name     = "key_words"
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
        self.critera_widget_list.append( widget )
        widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        placer.place( widget, columnspan = 2 )

        # ---- placer.new_row()
        placer.new_row()
        widget          = QLabel( "System" )
        placer.place( widget  )

        widget                  = custom_widgets.CQComboBoxEditCriteria( get_type = "string", set_type = "string")
        self.system_widget      = widget
        widget.critera_name     = "system"
        self.critera_widget_list.append( widget )

        placer.place( widget )
        widget.addItem( '' )
        widget.addItem( 'Powerbuilder')
        widget.addItem( 'One')
        widget.addItem('Two')
        widget.addItem('Three')
        widget.addItem('Four')

        widget.setCurrentIndex( 0 )

        # ---- Order by
        placer.new_row()
        widget  = QLabel( "Order by" )
        placer.place( widget )

        widget                 = custom_widgets.CQComboBoxEditCriteria( get_type = "string", set_type = "string")
        self.order_by_widget   = widget
        self.critera_widget_list.append( widget )
        widget.critera_name    = "order_by"

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

        widget                 = custom_widgets.CQComboBoxEditCriteria( get_type = "string", set_type = "string")
        self.order_by_dir_widget   = widget
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
        """
        print( "criteria_select in Help doc, trying to add key words needs work add dates " )

        parent_document                 = self.parent_window

        help_document                   = self.parent_window

        model                           = help_document.list_tab.list_model
        #rint( "begin channel_select for the list")
        query                           = QSqlQuery()
        query_builder                   = qt_sql_query.QueryBuilder( query )

        kw_table_name                   = "help_key_words"
        column_list                     = [ "id",   "title", "system", "key_words"   ]

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
            query_builder.sql_inner_join    = " help_key_word  ON help_info.id = help_key_word.id "
            query_builder.sql_having        = f" count(*) = {key_word_count} "

            query_builder.add_to_where( f" key_word IN {criteria_key_words}" , [] )



        #- ---- title like
        title                          = criteria_dict[ "title" ].strip().lower()
        if title:
            add_where       = "lower( title )  like :title"   # :is name of bind var below
            #where_dict      = {"channel_name_like":  f"%{channel_name_like}%"}
            #query_builder.add_to_where( add_where, where_dict )
            query_builder.add_to_where( add_where, [(  ":title",  f"%{title}%" ) ])

        # ---- order by may need work

        # ---- order by
        order_by   = criteria_dict[ "order_by" ]

        if   order_by == "title":
            column_name = "title"
        elif order_by == "system":
            column_name = "system"
        # elif order_by == "name - ignore case":
        #     column_name = "lower(name)"
        elif order_by == "id":
            column_name = "id"
        elif order_by == "id_old":
            column_name = "id_old"
        else:   # !! might better handel this
            column_name = "title"

        # widget.addItem('Ascending')
        # widget.addItem('Decending')
        order_by_dir   = criteria_dict[ "order_by_dir" ].lower( )

        msg    = f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{column_name = }  {order_by_dir = }"
        print( msg )

        if "asc" in order_by_dir:
            literal   = "ASC"
        else:
            literal   = "DESC"

        print( "uncomment next !!")
        query_builder.add_to_order_by(    column_name, literal,   )

        query_builder.prepare_and_bind()

        msg      = f"{query_builder = }"
        AppGlobal.logger.debug( msg )

        is_ok  = AppGlobal.qsql_db_access.query_exec_model( query,
                                                  model,
                                                  msg = "HelpSubWindow criteria_select" )

        help_document.main_notebook.setCurrentIndex( help_document.list_tab_index )
        self.critera_is_changed = False

# ----------------------------------------
class HelpListTab( base_document_tabs.DetailTabBase  ):

    def __init__(self, parent_window ):
        """

        """
        super().__init__( parent_window )

        self.list_ix            = 5  # should track selected an item in detail
            # needs work
        self.tab_name           = "HelpListTab"

        self._build_gui()

    # ------------------------------------------
    def _build_gui( self,  ):
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

        self.record_state       = base_document_tabs.RECORD_NULL


        self._build_gui()
        #self.tab_name     = "photoDetailTab"   # { self.tab_name = }
        self.table_name         = "help_info"
        self.tab_name           = "HelpDetailTab"

        model                   = QSqlTableModel( self, AppGlobal.qsql_db_access.db )
        self.tab_model          = model
        self.table              = parent_window.detail_table_name

        model.setTable( self.table )

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
        page            = self
        tab             = self

        box_layout_1    =  QVBoxLayout( page )

        placer          = gui_qt_ext.PlaceInGrid(
                            central_widget  = box_layout_1,
                            a_max           = 4,
                            by_rows         = False  )

        tab_layout      = placer

        # ----fields
        self._build_fields( placer )

        # ---- tab pages
        detail_notebook           = QTabWidget()
        self.detail_notebook      = detail_notebook


        # ---- buttons
        button_layout = QHBoxLayout()

        # fetch_button = QPushButton("Fetch")
        # fetch_button.clicked.connect(self.fetch_detail_row)
        # button_layout.addWidget(fetch_button)



    #---------------------------------
    def _build_fields( self, layout ):
        """
        What it says, read

        """
        # ---- code_gen: detail_tab_build_gui use for _build_fields was_build_gui  -- begin table entries

                                                # qdates make these non editable

        # ---- id
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "id",
                                                db_type        = "integer",
                                                display_type   = "string" )
        self.id_field         = edit_field
        #edit_field.setPlaceholderText( "id" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- id_old
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "id_old",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.id_old_field         = edit_field
        edit_field.setPlaceholderText( "id_old" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- type
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "type",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.type_field         = edit_field
        edit_field.setPlaceholderText( "type" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- sub_system
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "sub_system",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.sub_system_field         = edit_field
        edit_field.setPlaceholderText( "sub_system" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- system
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "system",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.system_field         = edit_field
        edit_field.setPlaceholderText( "system" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- key_words
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "key_words",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.key_words_field         = edit_field
        edit_field.setPlaceholderText( "key_words" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- add_ts
        edit_field                  = custom_widgets.CQDateEdit(
                                                parent         = None,
                                                field_name     = "add_ts",
                                                db_type        = "timestamp",
                                                display_type   = "qdate" )
        self.add_ts_field         = edit_field
        #edit_field.setPlaceholderText( "add_ts" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

                                                # timestamp to qdates make these non editable

        # ---- edit_ts
        edit_field                  = custom_widgets.CQDateEdit(
                                                parent         = None,
                                                field_name     = "edit_ts",
                                                db_type        = "timestamp",
                                                display_type   = "qdate" )
        self.edit_ts_field         = edit_field
        #edit_field.setPlaceholderText( "edit_ts" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- table_name
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "table_name",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.table_name_field         = edit_field
        edit_field.setPlaceholderText( "table_name" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- column_name
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "column_name",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.column_name_field         = edit_field
        edit_field.setPlaceholderText( "column_name" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- java_type
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "java_type",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.java_type_field         = edit_field
        edit_field.setPlaceholderText( "java_type" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- java_name
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "java_name",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.java_name_field         = edit_field
        edit_field.setPlaceholderText( "java_name" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- java_package
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "java_package",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.java_package_field         = edit_field
        edit_field.setPlaceholderText( "java_package" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- title
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "title",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.title_field         = edit_field
        edit_field.setPlaceholderText( "title" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- is_example
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "is_example",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.is_example_field         = edit_field
        edit_field.setPlaceholderText( "is_example" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- can_execute
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "can_execute",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.can_execute_field         = edit_field
        edit_field.setPlaceholderText( "can_execute" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- code_gen: detail_tab_build_gui use for _build_fields was_build_gui  -- end table entries

        # ---- code_gen: detail_tab_build_gui use for _build_gui  -- begin table entries\

    # ----------------------------
    def fetch_detail_row( self,  id = None ):
        """
        Args:
            id can be external or as chat has it fetched

        Returns:
            None.
        !! could be promoted
        """
        id      = self.id_field.text()
        print( f"fetch_row { id = }")
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





        self.clear_detail_fields()

        # ---- ??redef add_ts
        a_ts   = str( time.time() ) + "sec"
        # record.setValue( "add_ts",  a_ts    )
        self.add_ts_field.setText(  a_ts )
        self.edit_ts_field.setText( a_ts )

        self.id_field.setText( str( next_key ) )


# ==================================
class HelpTextTab( base_document_tabs.TextTabBase  ):
    """
    """
    # ----------------------
    def __init__(self, parent_window  ):
        """ """
        pass
        super().__init__( parent_window )
        self.tab_name            = "HelpTextTab"


        # self._build_gui()

        # model                    = QSqlTableModel( self, AppGlobal.qsql_db_access.db )
        # self.tab_model           = model # !! change everywhere
        # #self.detail_text_model   = model # !! remove  everywhere
        # model.setTable( parent_window.text_table_name )
        # print( f"on text tab {parent_window.text_table_name = }" )


    #-------------------------------------
    def _build_gui_hide( self ):
        """
        lets assume the gui is really build
        by the detail tab so do not do anything here
        but capture the field names in

        self.fake_gui( a_foreign_layout )
        Returns:
            none
        """
        page            = self
        tab             = self

        box_layout_1    =  QVBoxLayout( page )

        placer          = gui_qt_ext.PlaceInGrid(
                            central_widget  = box_layout_1,
                            a_max           = 4,
                            by_rows         = False  )

        tab_layout      = placer

        # ----fields
        self._build_fields( placer )

    #---------------------------------
    def _build_fieldsxxxxx( self, layout ):
        """
        What it says, read
            layout a placer ??
        """
        # ---- code_gen: detail_tab_build_gui use for _build_fields was_build_gui  -- begin table entries
                                                # qdates make these non editable

        # ---- id
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "id",
                                                db_type        = "integer",
                                                display_type   = "string" )
        self.id_field         = edit_field
        #edit_field.setPlaceholderText( "id" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- id_old
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "id_old",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.id_old_field         = edit_field
        edit_field.setPlaceholderText( "id_old" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- text_data
        layout.new_row()
        edit_field                  = custom_widgets.CQTextEdit(
                                                parent         = None,
                                                field_name     = "text_data",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.text_data_field         = edit_field
        edit_field.setPlaceholderText( "text_data" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field, columnspan = 3 )

        # ---- QPushButtons ------------------------------
        layout.new_row()
        widget          = QPushButton("Execute")
        # widget.clicked.connect(lambda: self.print_message(widget.text()))
        a_widget        = widget
        widget.clicked.connect( lambda: self.inspect( ) )
        layout.addWidget( widget )

        # ---- code_gen: detail_tab_build_gui use for _build_fields was_build_gui  -- end table entries

#    end code gen
    # ---------------------------
    def select_record_hide( self, id_value  ):
        """
        extend to send text back to detail tab, a kluge for now
        """
        #self.super(  ).select_record( id_value )
        #super( base_document_tabs.DetailTabBase, self).select_record( id_value)
        super().select_record( id_value)
        print( "############################################# got here ")


    #-------------------------------------
    def fake_guixxxxx( self, a_foreign_subwindow ):
        """
        unclear to me seems to be way of moving text to detail tab, or just for debug
        lets assume the gui is really build
        by the detail tab so do not do anything here
        but capture the field names in

        self.fake_gui( a_foreign_subwindow )
        call this from the subwindow after tabs are built
        """
        msg                     = "fake_gui +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        self.id_field           = a_foreign_subwindow.id_field_fake
        self.text_data_field    = a_foreign_subwindow.text_data_field_fake


    # ----------------------------
    def fetch_detail_row_hide( self,  id = None ):
        """
        Args:
            id can be external or as chat has it fetched

        Returns:
            None.
        !! could be promoted
        """
        id      = self.id_field.text()
        print( f"stuff text tab fetch_row { id = }")
        self.fetch_detail_row_by_id( id )

    # -----------------------------
    def fetch_text_row_by_id_hide( self,  id   ):
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
            # self.mypref_field.setText(str(record.value(  "mypref")   ))
            # self.mygroup_field.setText(record.value(     "mygroup"   ))
        else:

            msg     = f"Fetch Error: No record tor text_data found with the given ID. { id = }"
            QMessageBox.warning(self, "Error",  msg )
            AppGlobal.logger.error( msg )

        # else:
        #     QMessageBox.warning(self, "Input Error", f"Please enter a valid ID. { id = }")

    # -----------------------------
    def delete_detail_row_hide(self):
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
                QMessageBox.information(self, "Delete Success", "detail_text_model Record deleted successfully.")
                self.clear_detail_fields()
            else:
                msg   = "Delete Error: No record found with the given ID. { id = } "
                QMessageBox.warning(self, "Error",  msg )
                AppGlobal.logger.error( msg )
        else:
            msg  = f"Please enter a valid ID. { id = }"
            QMessageBox.warning(self, "Input Error", "Please enter a valid ID.")
            AppGlobal.logger.error( msg )

    # -------------------------
    def update_text_row_hide(self):
        """
        what it says, read
        row is the model   detail.model ??
        !! change to update_detail_row
        Returns:
            None.
        update_detail_row update_detail_row
        """
        model   = self.detail_model
        id = self.id_field.text()
        if id:
            model.setFilter(f"id = {id}")
            model.select()
            if model.rowCount() > 0:
                record = model.record(0)
                record.setValue( "text_data",    self.text_data_field.text() )
                # record.setValue("name",     self.name_field.text())
                # record.setValue("url",      self.url_field.text())
                # record.setValue("mypref",   int(self.mypref_field.text()) if self.mypref_field.text() else None )
                # record.setValue("mygroup",  self.mygroup_field.text())

                if model.setRecord(0, record):
                    model.submitAll()
                    msg    = "Text data Record updated successfully. text_data"
                    AppGlobal.logger.debug( msg )
                    QMessageBox.information(self, "Update Success", msg )
                else:
                    msg    =  f"text data Update Error Failed to update record. text_data {id = }"
                    AppGlobal.logger.error( msg )
                    QMessageBox.warning(self, "Error", msg )
            else:
                msg    = f"No record found with the given ID.text_data {id = } "
                AppGlobal.logger.error( msg )
                QMessageBox.warning(self, "Update Error", msg )
        else:
            msg    = f"Input Error", "Please enter a valid ID.text_data  {id = } "
            AppGlobal.logger.debug( msg )

            QMessageBox.warning(self, "Input Error", msg )

    # ------------------------
    def clear_fields_hide(self):
        """
        what it says, read
        what fields, need a bunch of rename here
        clear_detail_fields  clear_detail_fields
        """
        self.id_field.clear()
        self.text_data_field.clear()
        # self.name_field.clear()
        # self.mygroup_field.clear()

    # ------------------------
    def field_to_record_hide( self, record ):
        """
        in photo may be promotable --- need new ancestor
        for the updates, get the gui data into the record
        assume for new add time and id are already there?? or in a self.xxx
        since not sure how works put in instance
        """
        # if self.record_state    == self.RECORD_NEW:  # may be needed
        #     # self.record_id
        #     self.id_field.setText(  str( self.record_id     ) )
        #     pass

        if self.record_state    == base_document_tabs.RECORD_NEW:  # may be needed
            record.setValue("id", int( self.new_record_id ) )

        # record.setValue( "add_kw",     self.add_kw_field.text())

        record.setValue( "text_data", self.text_data_field.toPlainText())

        # ---- timestamps
        #record.setValue( "add_ts",   self.add_ts_field.text()) # should have already been set
        #record.setValue( "edit_ts",  self.edit_ts_field.text())

        # new_id     = self.id_field.text()
        # new_text   = self.text_data_field.toPlainText()
        # if new_id and new_text:
        #     record = model.record()
        #     record.setValue("id", int( new_id) )
        #     record.setValue("text_data", new_text)
        #     model.insertRecord( model.rowCount(), record


    # ------------------------
    def record_to_field_hide(self, record ):
        """
        in photo may be promotable
        should be for fetch
        """
        if self.record_state    == base_document_tabs.RECORD_NEW:  # may be needed
            # self.record_id
            self.id_field.setText(  str( self.new_record_id     ) )

        self.id_field.setText(str(record.value( "id" )))
        #self.textField.setText(record.value("text_data"))
        self.text_data_field.setText(  record.value( "text_data"     ))

# ----------------------------------------
class HelpHistorylTab( base_document_tabs.StuffdbHistoryTab  ):
    """
    """
    def __init__(self, parent_window ):
        """
        what it says read -- the usual -- note ancestor matters
        """
        super().__init__( parent_window )
        self.tab_name            = "HelpHistorylTab"

    #-------------------------------------
    def _build_gui( self ):
        """
        what it says read
        Returns:
            none
        """
        tab                  = self
        table                = QTableWidget( 0, 10, self )  # row column third arg parent
        self.history_table   = table

        ix_col   = 1
        table.setColumnWidth( ix_col, 22 )

        #table.clicked.connect( self.parent_window.on_history_clicked )
        #table.clicked.connect( self.on_list_clicked )
        table.cellClicked.connect( self.on_cell_clicked )

        layout2     = QVBoxLayout()
        layout2.addWidget( table )
        tab.setLayout( layout2 )

    # -------------------------------------
    def record_to_table( self, record ):
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

        ix_col          += 1
        item             = QTableWidgetItem( str( record.value( "id" ) ) )
        table.setItem( ix_row, ix_col, item   )
        print( f"just set {record.value( "id"       ) = } ")

        # ---- code_gen: history tab -- build_gui -- begin table entries

        ix_col          += 1
        item             = QTableWidgetItem( str( record.value( "title" ) ) )
        table.setItem( ix_row, ix_col, item   )


        ix_col          += 1
        item             = QTableWidgetItem( str( record.value( "key_words" ) ) )
        table.setItem( ix_row, ix_col, item   )


        ix_col          += 1
        item             = QTableWidgetItem( str( record.value( "xxxx" ) ) )
        table.setItem( ix_row, ix_col, item   )

        # ---- code_gen: history tab -- build_gui -- end table entries

# ---- eof ------------------------------
