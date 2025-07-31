#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=C0325,E0611,W0201
"""
  disable=E221,E201,E202,C0325,E0611,W0201

"""
# ---- tof
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    #main.main()
# --------------------

import functools
import logging
import time
from functools import partial


from PyQt5.QtCore import QDate, QModelIndex, Qt, QTimer, pyqtSlot
# ---- Qt
from PyQt5.QtGui import QFont, QIntValidator, QStandardItem, QStandardItemModel

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
#import  document_maker

import data_dict
import gui_qt_ext
import string_util
import text_edit_ext
from   app_global import AppGlobal


import base_document_tabs
import custom_widgets as cw
import data_manager
#import example_code  # against code in tex
#import  ia_qt
import key_words
import parameters
import qt_sql_query

# ---- constants
SYSTEM_LIST     = parameters.PARAMETERS.systems_list

logger          = logging.getLogger( )

LOG_LEVEL       = 5   # higher is more

# ----------------------------------------
class HelpDocument( base_document_tabs.DocumentBase ):
    """
    for the help tables....
    """
    def __init__(self, instance_ix = 0 ):
        """
        the usual
        """
        super().__init__( instance_ix )

        self.detail_table_name  = "help_info"
        self.text_table_name    = "help_text"  # text tables always id and text_data
        self.help_filename      = "help_doc.txt"
        self.subwindow_name     = "Notes Window"
        self.add_history_to_data_manager = True
        self._build_gui()
        self.__init_2__()

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
        perhaps promote !! need to look around help may be special
        defaults values for a new row in the detail and the
        text tabs

        Changes state of detail and related tabs

        """
        next_key      = AppGlobal.key_gen.get_next_key(   self.detail_table_name )
        self.detail_tab.default_new_row( next_key )
        self.text_tab.default_new_row(   next_key )

    #-------------------------------------
    def copy_prior_row( self ):
        """
        looks promotable

        tail_tab.default_new_row( next_key )
        default values with copy for a new row in the detail and the
               text tabs
        probably can promote, may need different func name on text so tabs can be the same?
        Returns:
            None.
            """
        next_key      = AppGlobal.key_gen.get_next_key(
                                  self.detail_table_name )
        self.detail_tab.copy_prior_row( next_key )
        self.text_tab.copy_prior_row(   next_key )

    #----------------------------
    def on_tab_changedPromoted( self, index ):
        """
        will kick off criteria select if ...
        what it says, read it
        !!
        extend
        """
        # debug_msg   = ( "on_tab_changed need validate update db but may be"
        #                " redundant in some cases so perhaps provide a mechanism to skip" )
        # logging.debug( debug_msg )
        super().on_tab_changed( index )

        if index == self.criteria_tab_index:
            self.criteria_tab.key_words_widget.setFocus()
        # old_index                = self.current_tab_index
        # self.current_tab_index   = index
        # #self.tab_page_info()
        # if old_index == 0 and index != 0:  # !=0 happens at construct
        #     self.criteria_tab.criteria_select_if( )


    # ---- sub window interactions ---------------------------------------
     # ------------------------------------------
    def criteria_select( self,     ):
        """
        uses info in criteria tab to build list in list tab
        uses info from 2 tabs
        """
        self.criteria_tab.criteria_select()

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
        the usual
        """
        super().__init__( parent_window )
        self.tab_name   = "HelpCriteriaTab"

    # ------------------------------------------
    def _build_tab( self,   ):
        """
        what it says, read
        put page into the notebook
        for system
                widget.setEditable(True)
        """
        page            = self
        layout          = QHBoxLayout( page )
                # can we fold in to next

        grid_layout      = gui_qt_ext.CQGridLayout( col_max = 12 )
        layout.addLayout( grid_layout )

        self._build_top_widgets_grid( grid_layout )

        # ---- "Key Words"
        grid_layout.new_row()
        widget  = QLabel( "Key Words" )
        grid_layout.addWidget( widget )

        widget                    = cw.CQHistoryComboBox(
                                       field_name = "key_words" )

        # widget                    = cw.CQLineEdit(
        #                                field_name = "key_words" )
        self.key_words_widget     = widget   # not this one at least not yet
        # self.key_word_widget        = None      # set to value in gui if used
        widget.setPlaceholderText( "key_words"  )
        self.critera_widget_list.append( widget )
        #widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        grid_layout.addWidget( widget )


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

        # ----id_old
        widget                = QLabel( "ID Old" )
        grid_layout.new_row()
        grid_layout.addWidget( widget )

        widget                  = cw.CQLineEdit(
                                   field_name = "id_old" )
        self.critera_widget_list.append( widget )
        # widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        grid_layout.addWidget( widget, )    # columnspan = 3 )



        # ---- grid_layout.new_row()
        grid_layout.new_row()
        widget  = QLabel( "Title (like)" )
        grid_layout.addWidget( widget )

        widget                  = cw.CQLineEdit(
                                                 field_name = "title" )
        self.critera_widget_list.append( widget )
        #widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        grid_layout.addWidget( widget, columnspan = 2 )

        # ---- system
        grid_layout.new_row()
        widget          = QLabel( "System" )
        grid_layout.addWidget( widget  )

        widget                  = cw.CQComboBox(
                                        field_name = "system" )
        self.critera_widget_list.append( widget )
        widget.setMaxVisibleItems( 25 )
        grid_layout.addWidget( widget )
        widget.addItems( SYSTEM_LIST )
        widget.addItem( "<none>" )
        # widget.addItem( '' )

        widget.setCurrentIndex( 0 )
        widget.setEditable( True )

        # ---- Order by
        grid_layout.new_row()
        widget  = QLabel( "Order by" )
        grid_layout.addWidget( widget )

        widget                 = cw.CQComboBox(
                                     field_name = "order_by" )
        self.critera_widget_list.append( widget )

        widget.addItem('title - ignore case')
        widget.addItem('descr')
        widget.addItem('name')
        widget.addItem('system')
        widget.addItem("name - ignore case")
        widget.addItem('id')
        widget.addItem('id_old')
        # widget.addItem('Title??')

        debug_msg  = ( f"{self.tab_name} build_tab build criteria change put in as marker ")
        logging.log( LOG_LEVEL,  debug_msg, )

        #widget.currentIndexChanged.connect( lambda: self.criteria_changed(  True   ) )
        grid_layout.addWidget( widget )

        # ---- Order by Direction
        widget  = QLabel( "Direction" )
        grid_layout.addWidget( widget )

        widget                      = cw.CQComboBox(
                                          field_name = "order_by_dir" )
        #self.order_by_dir_widget    = widget
        self.critera_widget_list.append( widget )
        #widget.critera_name    = "order_by_dir"

        widget.addItem('Ascending')
        widget.addItem('Decending')
        # widget.addItem('id')
        # widget.addItem('Title??')

        #widget.currentIndexChanged.connect( lambda: self.criteria_changed(  True   ) )
        #grid_layout.new_row()  # because seems to be missing
        grid_layout.addWidget( widget )

        widget  = QLabel( "<<<Direction" )
        grid_layout.addWidget( widget )

        # ---- criteria changed should be in parent
        print( f"{self.tab_name} build_tab build criteria change put in as marker ")
        grid_layout.new_row()
        widget  = QLabel( "criteria_changed_widget" )
        self.criteria_changed_widget  = widget
        grid_layout.addWidget( widget )

        # # ---- push up on page still needs adjust
        # widget   = QSpacerItem( 350, 110, QSizePolicy.Expanding, QSizePolicy.Minimum )
        #     # width, height..... pixels
        # grid_layout.new_row()
        # # grid_layout.place( widget )
        # grid_layout.addItem( widget, grid_layout.ix_row, grid_layout.ix_col    )  # row column

        # ---- function_on_return( self )
        for i_widget in self.critera_widget_list:
            # ---- new  only really changes some edits
            i_widget.on_value_changed       = lambda: self.criteria_changed( True )
            i_widget.on_return_pressed      = self.criteria_select

    # -------------
    def criteria_select( self, ):
        """
        moved down from document
        uses info in criteria tab to do selection build list in list tab
        uses info from 2 tabs

        test in sql browser -- when testing look out for bind variables

            use fully qualified names in all sql

        """
        parent_document                 = self.parent_window
        help_document                   = self.parent_window

        model                           = help_document.list_tab.list_model

        # ---- try this to clear
        model.setFilter( "id = -99" )
        model.select()

        #rint( "begin channel_select for the list")
        query                           = QSqlQuery()
        query_builder                   = qt_sql_query.QueryBuilder( query, print_it = True  )

        kw_table_name                   = "help_key_words"

        # !! next is too much
        columns         = data_dict.DATA_DICT.get_list_columns( self.parent_window.detail_table_name )
        #col_head_texts   = [ "seq" ]  # plus one for sequence
        col_names       = [  ]
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
        if   system == "<none>":
            #add_where       =  f' help_info.system)= "{system}" '
            add_where       =  ' help_info.system  IS NULL OR TRIM(help_info.system)= "" '
            #WHERE system IS NULL OR TRIM(system) = ''
            query_builder.add_to_where( add_where, [ ])

        elif system:
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
            query_builder.sql_having        = f" count(*) >= {key_word_count} "    # >+ for key word errors

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
        logging.log( LOG_LEVEL,  debug_msg, )

        if "asc" in order_by_dir:
            literal   = "ASC"
        else:
            literal   = "DESC"

        query_builder.add_to_order_by(  column_name, literal,   )

        query_builder.prepare_and_bind()

        debug_msg      = f"{query_builder = }"
        logging.log( LOG_LEVEL,  debug_msg, )

        is_ok   = AppGlobal.qsql_db_access.query_exec_model( query,
                                                  model,
                                                  msg = "HelpSubWindow criteria_select" )

        # parent_document might be improvement !!
        help_document.main_notebook.setCurrentIndex( help_document.list_tab_index )
        self.critera_is_changed = False

    def search_me_new(self, criteria ):
        """
        see a promoted version in base
        external search should be overridden maybe in each document type
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

        #criteria  = criteria.strip()
        key_words    = criteria[ "key_words" ]

        # msg   = f"made it to help document {criteria =}"
        # logging.debug( msg )

        # tab_widget.setCurrentIndex( tab_index )
        tab_index     = parent_window.criteria_tab_index

        parent_window.tab_folder.setCurrentIndex(  tab_index )
        self.clear_criteria()


        self.key_words_widget.set_data( key_words )

        # mayb this maybe not
        #self.criteria_select_if()    # may need to select is changed
        self.criteria_select()



    # -----------------------------
    def search_me_old(self, criteria ):
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

        # mayb this maybe not
        #self.criteria_select_if()    # may need to select is changed
        self.criteria_select()

    # -----------------------------
    def clear_criteria( self ):
        """
        What it says, read
        extend
        we should be able to generalize this
        might make default in ancestor, overrid if desired
        or pass a field name

        !! use       get_criteria_widget  no self.key_words_widget

        """
        super().clear_criteria(   )
        widget   = self.get_criteria_widget( "key_words" )
        widget.setFocus()


# ----------------------------------------
class HelpListTab( base_document_tabs.ListTabBase  ):

    def __init__(self, parent_window ):
        """

        """
        super().__init__( parent_window )

        #self.list_ix            = 5  # should track selected an item in detail
            # needs work
        self.tab_name           = "HelpListTab"

        self._build_gui()

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

        # ---- data manager
        self.text_data_manager      = data_manager.DataManager( self.text_model )
        # next is a bit ass backwards
        self.pseodo_text_tab        = self.text_data_manager

        page            = self

        max_col         = 12
        self.max_col    = max_col

        box_layout_1    =  QVBoxLayout( page )

        layout          = gui_qt_ext.CQGridLayout( col_max = 12 )
        box_layout_1.addLayout( layout )

        # ----fields
        self._build_fields( layout  )

        # ---- text fields
        self._build_text_gui( box_layout_1 )

        # ---- tab pages
        detail_notebook           = QTabWidget()
        self.detail_notebook      = detail_notebook

    #---------------------------------
    def _build_fields( self, layout ):
        """
        What it says, read
                tweaks    may need         widget.setReadOnly( True )
                system and sub_system need to be editable combo
                #---- system TO combo box
                   and edit_field.setMaxVisibleItems( 25 )  # Number of rows shown in the popup
        for a grid# Row 1, Column 0, Span 1 row and 2 columns

        row_span      = 1 # default is 1
        col_span      = 1 # default is 1

        # rowSpan: (Optional) The number of rows the widget should span. Defaults to 1.
        # columnSpan: (Optional) The number of columns the widget should span. Defaults to 1.

        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget( widget, ix_row, ix_col, row_span, col_span )


        """

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

        edit_field.setToolTip("This is the hover text!")

        """
        for ix in range( self.max_col ):
            widget   = QSpacerItem( 50, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
            layout.addItem( widget, 0, ix  )  # row column

        # ---- code_gen: TableDict.to_build_form 2025_02_01 for help_info -- begin table entries -----------------------

        # ---- id
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "id",
                                                 )
        self.id_field     = edit_field
        edit_field.rec_to_edit_cnv    = edit_field.cnv_int_to_str
        edit_field.edit_to_rec_cnv    = edit_field.cnv_str_to_int
        edit_field.setReadOnly( True )
        edit_field.setPlaceholderText( "id" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 1 )
        edit_field.setReadOnly( True )

        # ---- id_old
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "id_old",
                                                 )
        self.id_old_field     = edit_field
        # edit_field.rec_to_edit_cnv    = edit_field.cnv_int_to_str
        # edit_field.edit_to_rec_cnv    = edit_field.cnv_str_to_int
        edit_field.setReadOnly( True )
        edit_field.setPlaceholderText( "id_old" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 1 )

        # ---- title
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "title",
                                                is_keep_prior_enabled  = True
                                                       )
        self.title_field     = edit_field
        edit_field.is_keep_prior_enabled        = True
        edit_field.setPlaceholderText( "title" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 4 )

        # ---- key_words
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "key_words",
                                                is_keep_prior_enabled  = True
                                                 )
        self.key_words_field     = edit_field
        edit_field.setToolTip("Key Words field")
        # this is too late
        #edit_field.is_keep_prior_enabled        = True
        edit_field.setPlaceholderText( "key_words" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 4 )

        # ---- system deleted
        # edit_field                  = cw.CQLineEdit(
        #                                         parent         = None,
        #                                         field_name     = "system",
        #                                         db_type        = "VARCHAR(15)",
        #                                         display_type   = "string",
        #                                          )
        # self.system_field     = edit_field
        # edit_field.setPlaceholderText( "system" )
        # # still validator / default func  None
        # self.data_manager.add_field( edit_field, is_key_word = True )
        # layout.addWidget( edit_field, columnspan = 1 )

        # ---- system
        edit_field                  = cw.CQComboBox(
                                                parent         = None,
                                                field_name     = "system",
                                                is_keep_prior_enabled        = True   )
        self.system_field     = edit_field
        #edit_field.setEditable( True )
        edit_field.setPlaceholderText( "system" )
        edit_field.clear()
        edit_field.setEditable( True )
        edit_field.setMaxVisibleItems( 25 )  # Number of rows shown in the popup
        edit_field.add_items( SYSTEM_LIST )
        # still validator / default func  None
        edit_field.is_keep_prior_enabled        = True
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 1 )



        # ---- sub_system
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "sub_system",
                                                           )
        self.sub_system_field     = edit_field
        edit_field.setPlaceholderText( "sub_system" )
        edit_field.setToolTip("SubSystem field")
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- java_package
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "java_package",
                                                            )
        self.java_package_field     = edit_field
        edit_field.is_keep_prior_enabled        = True
        edit_field.setPlaceholderText( "java_package" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- java_type
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "java_type",
                                                              )
        self.java_type_field     = edit_field
        edit_field.setPlaceholderText( "java_type" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- java_name
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "java_name",
                                                            )
        self.java_name_field     = edit_field
        edit_field.is_keep_prior_enabled        = True
        edit_field.setPlaceholderText( "java_name" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- table_name
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "table_name",
                                                                )
        self.table_name_field     = edit_field
        edit_field.setPlaceholderText( "table_name" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- column_name
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "column_name",
                                                         )
        self.column_name_field     = edit_field
        edit_field.setPlaceholderText( "column_name" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- type
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "type",
                                                              )
        self.type_field     = edit_field
        edit_field.setPlaceholderText( "type" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- is_example
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "is_example",
                                                          )
        self.is_example_field     = edit_field
        edit_field.setPlaceholderText( "is_example" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- edit_ts
        edit_field                      = cw.CQDateEdit(
                                                parent         = None,
                                                field_name     = "edit_ts",
                                                          )
        self.edit_ts_field     = edit_field
        edit_field.rec_to_edit_cnv      = edit_field.cnv_int_to_qdate
        edit_field.edit_to_rec_cnv      = edit_field.cnv_qdate_to_int
        edit_field.setPlaceholderText( "edit_ts" )
        # still validator / default func  None
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 1 )
        edit_field.setReadOnly( True )

    # -------------------------------------
    def _build_text_gui( self, a_layout ):
        """
        like to build gui on text tabs borrowed here
        in help_document, try to make copy over to base document text tab
        we may be able to make this a method in base see base document ??


        new since last back lets use boxes
        like to build gui on text tabs borrowed here
        in help_document, try to make copy over to base document text tab
        we may be able to make this a method in base see base document ??
        """
        tab_layout      = QHBoxLayout()
        a_layout.addLayout( tab_layout )

        button_layout   = QVBoxLayout()
        tab_layout.addLayout( button_layout )

        # ---- text layout lets favor it for space
        text_layout     = QVBoxLayout()
        tab_layout.addLayout( text_layout, stretch=2 )

        data_manager    = self.text_data_manager

        # ---- TextEdit   needs to be defined at beginning with exte4nsion object
        # and monkey patch
        edit_field          = cw.CQTextEdit(
                                    parent         = None,
                                    field_name     = "text_data",
                                                  )
        text_entry_widget   = edit_field
        font                = QFont( * parameters.PARAMETERS.text_edit_font ) # ("Arial", 12)
        edit_field.setFont(font)
        self.text_data_field = edit_field    # may be used for editing
        edit_field.setPlaceholderText( "Some Long \n   text on a new line " )
        data_manager.add_field( edit_field, )
        text_layout.addWidget( edit_field, )  # what order row column
        text_edit_ext_obj         = text_edit_ext.TextEditExt( AppGlobal.parameters, text_entry_widget)
        self.text_edit_ext_obj    = text_edit_ext_obj

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
        widget          =  cw.CQLineEdit(
                                     parent         = None,
                                     field_name     = "id",
                                                )
        self.id_field   = widget
        widget.setReadOnly( True )

        data_manager.add_field( widget, )
        button_layout.addWidget( widget, )

        # label           = "Paste Clip"
        # widget          = QPushButton( label )
        # # connect_to  =  functools.partial( self.run_python_idle, text_entry_widget )
        # # widget.clicked.connect( connect_to )
        # widget.clicked.connect( self.text_edit_ext_obj.paste_clipboard  )
        # button_layout.addWidget( widget, )

        # ---- template may not even need in self
        print( "monkey_patch_here_please")
        ddl_widget, ddl_button_widget  = self.text_edit_ext_obj.build_up_template_widgets()

        button_layout.addWidget( ddl_widget  )
        button_layout.addWidget( ddl_button_widget  )

        # # ---- copy line  copy ling without selecting
        # label           = "!!Copy\nLine"
        # widget = QPushButton( label )
        # # connect_to  =  functools.partial( self.copy_line_of_text, text_entry_widget )
        # # widget.clicked.connect( connect_to )
        # button_layout.addWidget( widget, )

        # ---- Paste Prior
        label           = "Paste Prior"
        widget          = QPushButton( label )
        widget.clicked.connect( self.text_edit_ext_obj.paste_cache )
        button_layout.addWidget( widget, )

        # ---- !!To_Smart
        label           = "Cnv Hyper...tbd"
        widget          = QPushButton( label )
        # connect_to  =  functools.partial( self.run_python_idle, text_entry_widget )
        # widget.clicked.connect( connect_to )
        #widget.clicked.connect( self.text_edit_ext_obj.strip_lines_in_selection  )
        button_layout.addWidget( widget, )

        # ---- !!To_Smart
        label           = "To_Smart...tbd"
        widget          = QPushButton( label )
        # connect_to  =  functools.partial( self.run_python_idle, text_entry_widget )
        # widget.clicked.connect( connect_to )
        #widget.clicked.connect( self.text_edit_ext_obj.strip_lines_in_selection  )
        button_layout.addWidget( widget, )

        # ---- Remove Lead/Trail"
        label           = "Remove Lead/Trail"
        widget          = QPushButton( label )
        # connect_to  =  functools.partial( self.run_python_idle, text_entry_widget )
        # widget.clicked.connect( connect_to )
        widget.clicked.connect( self.text_edit_ext_obj.strip_lines_in_selection  )
        button_layout.addWidget( widget, )

        # ---- search text
        search_layout       = QHBoxLayout()
        text_layout.addLayout( search_layout )
        # ix_row          -= 1
        # ix_col          += 1
        widget              = QLineEdit()
        search_line_edit    = widget
        widget.setPlaceholderText("Enter search text")
        search_layout.addWidget( widget,   )

        # ---- up down Buttons
        widget              = QPushButton("Down")
        down_button         = widget
        # connect below
        connect_to      = functools.partial( self.text_edit_ext_obj.search_down, search_line_edit ,)
                  #text_entry_widget  ) # entry_widget =.CQTextEdit(
        down_button.clicked.connect( connect_to )
        search_layout.addWidget( widget,  )

        widget          = QPushButton("Up")
        up_button       = widget
        connect_to      = functools.partial( self.text_edit_ext_obj.search_up, search_line_edit ,)
        up_button.clicked.connect( connect_to )
        search_layout.addWidget( widget,   )

        # # ---- qt_exec
        # label           = "qt_exec"
        # widget          = QPushButton( label )
        # connect_to  =  functools.partial( text_edit_ext.qt_exec, text_entry_widget )
        # widget.clicked.connect( connect_to )
        # # # widget.clicked.connect( self.qt_exec )
        # text_layout.addWidget( widget,  )

        # ---- >>
        label       = "Go  >> ..."
        widget      = QPushButton( label )
        #connect_to  = functools.partial( text_edit_ext_obj.cmd_exec, text_entry_widget )
        connect_to  = text_edit_ext_obj.cmd_exec
        widget.clicked.connect( connect_to )
        text_layout.addWidget ( widget,     )

    # ----------------------------
    def fetch_detail_rowpromoted( self,  a_id = None ):
        """
        Args:
            id can be external or as that has it fetched

        Returns:
            None.
        !! could be promoted
        """
        a_id          = self.id_field.text()
        debug_msg     = ( f"fetch_row { a_id = }")
        logging.log( LOG_LEVEL,  debug_msg, )

        self.fetch_detail_row_by_id( a_id )

    # -----------------------------
    def copy_prior_row( self, next_key ):
        """
        !! may be dead
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

        # edit_ts  = self.edit_ts_field.text()
        # edit_ts  = "self.edit_ts_field.text()"   # !! test

        self.default_new_row( next_key )

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
    The usual history tab
    """
    def __init__(self, parent_window ):
        """
        what it says read -- the usual -- note ancestor matters
        """
        super().__init__( parent_window )
        self.tab_name            = "HelpHistorylTab"

# ---- eof ------------------------------
