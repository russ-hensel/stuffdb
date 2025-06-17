#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0325,E0611,W0201
"""
this is the code for the StuffDocument
"""
# ---- tof

# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    main.main()
# --------------------


import functools
import inspect
import logging
import time
from   datetime import datetime
from   functools import partial



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
                             QVBoxLayout,
                             QWidget)

# ---- imports local
import base_document_tabs
import custom_widgets as cw
#import data_manager
import key_words
import mdi_management
import qt_sql_query
import qt_with_logging
import stuff_document_edit
import combo_dict_ext
import data_dict
import gui_qt_ext
import info_about
import string_util
from app_global import AppGlobal

# ---- end imports

logger              = logging.getLogger( )
LOG_LEVEL           = 20
    # level form much debug    higher is more debugging

FIF                 = info_about.INFO_ABOUT.find_info_for
WIDTH_MULP          = 10   # for some column widths, search


# ----------------------------------------
class StuffDocument( base_document_tabs.DocumentBase ):
    """
    for the stuff tables....
    """
    def __init__(self, instance_ix = 0 ):
        """
        the usual
        """
        super().__init__( instance_ix )
        # need fair bit of app to be init, this may be best place for this
        combo_dict_ext.build_it( AppGlobal.qsql_db_access.db )   # do not forget

        self.detail_table_name      = "stuff"
        self.key_word_table_name    = "stuff_key_word"
        self.text_table_name        = "stuff_text"  # text tables always id and text_data
            # used in text tab base
        self.help_filename          = "stuff_doc.txt"
        self.subwindow_name         = "StuffDocument"

        self._build_gui()
        self.__init_2__()

    # --------------------------------
    def get_topic( self ):
        """
        this version seems promotable
        of the detail record -- now info
        see picture get plant info....
        """
        info   = self.detail_tab.data_manager.get_topic_string()
        return info

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says
        """
        # Main notebook with  tabs
        main_notebook           = self.tab_folder   # create in parent
        self.main_notebook      = main_notebook

        sub_window              = self
        mdi_area                = AppGlobal.main_window.mdi_area
        main_notebook.currentChanged.connect( self.on_tab_changed )

        ix                        = -1

        ix                       += 1
        self.criteria_tab_index   = ix
        self.criteria_tab         = StuffCriteriaTab( self  )
        main_notebook.addTab(       self.criteria_tab, "Criteria" )

        ix                       += 1
        self.list_tab_index      = ix
        self.list_tab            = StuffListTab( self  )
        main_notebook.addTab(  self.list_tab, "List"    )

        ix                       += 1
        self.detail_tab_index     = ix  #
        self.detail_tab           = StuffDetailTab( self )
        main_notebook.addTab( self.detail_tab, "Detail"     )

        ix                       += 1
        self.picture_tab_index     = ix
        self.picture_tab           = base_document_tabs.StuffdbPictureTab( self )
        main_notebook.addTab( self.picture_tab, "Picture"     )

        ix                         += 1
        self.detail_text_index      = ix  # phase out !!
        self.text_tab_index         = ix
        self.text_tab               = StuffTextTab( self )
        main_notebook.addTab( self.text_tab, "Text"     )

        ix                         += 1
        self.history_tab_index     = ix
        self.history_tab           = StuffHistoryTab( self )
        main_notebook.addTab( self.history_tab, "History"    )

        sub_window.setWidget( main_notebook )
        mdi_area.addSubWindow( sub_window )
             # perhaps add to register_document in midi_management

        sub_window.show()

    # -------------------------------------
    def i_am_hsw(self):
        """
        make sure call is to here for testing
        """
        debug_msg  = ( f"{self.tab_name} stuff sub window, i_am_hsw")
        logging.debug( debug_msg )

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

    # ---- capture events ----------------------------


    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = "\n>>>>>>>>>>* StuffDocument  *<<<<<<<<<<<<"
        #super(   ).__init__(   )
        b_str   =  super().__str__(  )
        a_str   = a_str + "\n" + b_str

        return a_str

# ----------------------------------------
class StuffCriteriaTab( base_document_tabs.CriteriaTabBase, ):
    """
    criteria for list selection
    """
    def __init__(self, parent_window ):
        """
        the usual
        """
        super().__init__( parent_window )
        self.tab_name   = "StuffCriteriaTab"

    # ------------------------------------------
    def _build_tab( self, ):
        """
        what it says, read

        """
        page            = self
        layout           = QHBoxLayout( page )
                # can we fold in to next

        grid_layout      = gui_qt_ext.CQGridLayout( col_max = 10 )
        layout.addLayout( grid_layout )

        self._build_top_widgets_grid( grid_layout )

        # ----id
        widget                = QLabel( "ID" )
        grid_layout.new_row()
        grid_layout.addWidget( widget )

        widget                  = cw.CQLineEdit( field_name  = "table_id", )
        self.critera_widget_list.append( widget )
        widget.textChanged.connect( lambda: self.criteria_changed( True ) )
        grid_layout.addWidget( widget )    # columnspan = 3 )

        # ----id_old
        widget              = QLabel( "ID Old" )
        grid_layout.new_row()
        grid_layout.addWidget( widget )

        widget              = cw.CQLineEdit( field_name  = "id_old", )
        self.critera_widget_list.append( widget )
        widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        grid_layout.addWidget( widget )    # columnspan = 3 )

        # ----key words
        widget                = QLabel( "Key Words" )
        grid_layout.new_row()
        grid_layout.addWidget( widget )

        widget                  = cw.CQLineEdit( field_name  = "key_words", )
        self.critera_widget_list.append( widget )
        self.key_words_widget   = widget  # is needed for paste
        widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        grid_layout.addWidget( widget, columnspan = 3 )

        # ----descr
        widget                = QLabel( "descr" )
        grid_layout.new_row()
        grid_layout.addWidget( widget )

        widget                  = cw.CQLineEdit( field_name  = "descr", )
        self.critera_widget_list.append( widget )
        widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        grid_layout.addWidget( widget, columnspan = 3 )

        # ----name
        widget                = QLabel( "name" )
        grid_layout.new_row()
        grid_layout.addWidget( widget )

        widget                  = cw.CQLineEdit( field_name  = "name", )
        self.critera_widget_list.append( widget )
        widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        grid_layout.addWidget( widget, columnspan = 3 )

        # ---- Order by  CQComboBox
        widget  = QLabel( "Order by" )
        grid_layout.new_row()
        grid_layout.addWidget( widget )

        widget                 = cw.CQComboBox( field_name  = "order_by",  )
        self.critera_widget_list.append( widget )

        widget.addItem('descr')
        widget.addItem('name')
        widget.addItem("name - ignore case")
        widget.addItem('id')
        widget.addItem('id_old')
        # widget.addItem('Title??')

        debug_msg    = ( f"{self.tab_name} build_tab build criteria change put in as marker ")
        logging.log( LOG_LEVEL,  debug_msg, )

        widget.currentIndexChanged.connect( lambda: self.criteria_changed( True ) )
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

        debug_msg   = ( f"{self.tab_name} build_tab build criteria change put in as marker ")
        logging.log( LOG_LEVEL, debug_msg, )

        widget.currentIndexChanged.connect( lambda: self.criteria_changed(  True   ) )
        grid_layout.addWidget( widget )


        # ---- criteria changed should be in parent
        widget  = QLabel( "criteria_changed_widget" )
        self.criteria_changed_widget  = widget
        grid_layout.new_row()
        grid_layout.addWidget( widget )

        # ---- function_on_return( self )
        for i_widget in self.critera_widget_list:
            # ---- new  only really changes some edits
            i_widget.on_return_pressed     = self.criteria_select

    # -------------
    def criteria_select( self,     ):
        """
        do select base on the criteria_dict
        """
        parent_document                 = self.parent_window

        model                           = parent_document.list_tab.list_model
        view                            = parent_document.list_tab.list_view
        #rint( "begin channel_select for the list")
        query                           = QSqlQuery()
        query_builder                   = qt_sql_query.QueryBuilder( query, print_it = False, )

        kw_table_name                   = "stuff_key_words"


        # !!  may want clear as in help
        # !! next is too much
        columns    = data_dict.DATA_DICT.get_list_columns( self.parent_window.detail_table_name )
        #col_head_texts   = [ "seq" ]  # plus one for sequence
        col_names        = [   ]

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
            query_builder.sql_inner_join    = " stuff_key_word  ON stuff.id = stuff_key_word.id "
            query_builder.sql_having        = f" count(*) = {key_word_count} "

            query_builder.add_to_where( f" key_word IN {criteria_key_words}" , [] )

        # ---- descr
        descr                          = criteria_dict[ "descr" ].strip().lower()
        if descr:
            add_where       = "lower( descr )  like :descr"   # :is name of bind var below
            query_builder.add_to_where( add_where, [(  ":descr",
                                                     f"%{descr}%" ) ])

        # ---- name
        stuff_name                          = criteria_dict[ "name" ].strip().lower()
        if stuff_name:
            add_where       = "lower( name )  like :stuff_name"   # :is name of bind var below
            query_builder.add_to_where( add_where, [(  ":stuff_name",
                                                      f"%{stuff_name}%" ) ])

        # ---- order by
        order_by   = criteria_dict[ "order_by" ]

        if   order_by == "descr":
            column_name = "descr"
        elif order_by == "name":
            column_name = "name"
        elif order_by == "name - ignore case":
            column_name = "lower(name)"
        elif order_by == "id":
            column_name = "id"
        elif order_by == "id_old":
            column_name = "id_old"
        else:   # !! might better handel this
            column_name = "descr"

        order_by_dir   = criteria_dict[ "order_by_dir" ].lower( )

        loc        = f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name} "
        debug_msg  = f"{loc} >>> {column_name = }  {order_by_dir = }"
        logging.log( LOG_LEVEL, debug_msg )

        if "asc" in order_by_dir:
            literal   = "ASC"
        else:
            literal   = "DESC"

        query_builder.add_to_order_by( column_name, literal,   )

        query_builder.prepare_and_bind()

        debug_msg      = f"{query_builder = }"
        logging.log( LOG_LEVEL, debug_msg )

        is_ok  = AppGlobal.qsql_db_access.query_exec_model( query,
                                                  model,
                                                  msg = f"{self.tab_name} criteria_select" )

        loc        = f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name} "
        debug_msg  = f"{loc} >>> {query.executedQuery() = }  "
        logging.log( LOG_LEVEL, debug_msg )

        # !! next is too much
        columns         = data_dict.DATA_DICT.get_list_columns( self.parent_window.detail_table_name )
        col_head_texts  = []  # plus one for sequence
        col_names       = []
        col_head_widths = []
        for i_column in columns:
            col_names.append(        i_column.column_name  )
            col_head_texts.append(   i_column.col_head_text  )
            col_head_widths.append(  i_column.col_head_width  )

        #rint( "try width again after select says chat   )
        for ix_col, i_width in enumerate( col_head_widths ):
            #rint( f" {ix_col = } { i_width = }")
            view.setColumnWidth( ix_col, i_width * WIDTH_MULP )

        # a check chat suggests
        #rint(view.horizontalHeader().sectionResizeMode(3))

        parent_document.main_notebook.setCurrentIndex( parent_document.list_tab_index )
        self.critera_is_changed = False

# ----------------------------------------
class StuffListTab( base_document_tabs.ListTabBase  ):

    def __init__(self, parent_window ):

        super().__init__( parent_window  )

        self.tab_name           = "StuffListTab"
        self._build_gui()

# ----------------------------------------
class StuffDetailTab( base_document_tabs.DetailTabBase  ):
    """
    the document for the stuff and associated tables
    """
    #--------------------------------------------
    def __init__(self, parent_window  ):
        """
        the usual
        """
        super().__init__( parent_window )

        self.tab_name                   = "StuffDetailTab"
        self.key_word_table_name        = "stuff_key_word"
        self.enable_send_topic_update   = True

        self.post_init()

    # -------------------------------------
    def _build_gui( self ):
        """
        what it says read
        """
        page            = self

        max_col         = 10
        self.max_col    = max_col

        # rename !!
        box_layout_1    =  QVBoxLayout( page )

        # !! change name
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

        sub_tab                 = StuffPictureListSubTab( self )
        self.picture_sub_tab    = sub_tab    # !! phase out ?? no is special
        self.sub_tab_list.append( sub_tab )
        tab_folder.addTab( sub_tab, "Pictures" )

        sub_tab             = StuffEventSubTab( self )
        self.event_sub_tab  = sub_tab
        self.sub_tab_list.append( sub_tab )
        tab_folder.addTab( sub_tab, "Events" )

        # Main notebook
        detail_notebook           = QTabWidget()
        self.detail_notebook      = detail_notebook

        # ---- buttons
        # create_button = QPushButton("Create Default")
        # create_button.clicked.connect( self.create_default_row )
        # button_layout.addWidget(create_button)

    # ----------------------------
    def fetch_detail_row( self,  a_id = None ):
        """
        Args:
            id can be external or as chat has it fetched

        Returns:
            None.
        !!  promoted check does not exist in other tabsl
                and is it ever called
        """
        a_id      = self.id_field.text()
        msg       = (  f"shold be promoted ?? fetch_detail_row { a_id = }")
        logging.debug( msg )

        self.fetch_detail_row_by_id( a_id )


    #---------------------------------
    def _build_fields( self, layout ):
        """
        What it says, read
            this is generated code, then tweaked.
            *still needs to be manual setReadOnly

            Tweaks
                 *tweak a field to drop down a info on other stuff that is containers
                use CQComboBox or something more advanced
                see tweak for in_id old
        """
        width  = 50
        for ix in range( self.max_col ):  # try to tweak size to make it work
            widget   = QSpacerItem( width, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
            layout.addItem( widget, 0, ix  )  # row column

        self.stuff_combo_dict_ext   = combo_dict_ext.STUFF_COMBO_DICT_EXT


        # ---- code_gen: TableDict.to_build_form 2025_04_01 for stuff
        # -- begin table entries -----------------------

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
        edit_field.is_keep_prior_enabled        = True
        edit_field.setPlaceholderText( "name" )
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field, columnspan = 4 )

        # ---- descr
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "descr", )
        self.descr_field     = edit_field
        edit_field.is_keep_prior_enabled        = True
        edit_field.setPlaceholderText( "descr" )
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

        # ---- cont_type
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "cont_type", )
        self.cont_type_field     = edit_field
        edit_field.setPlaceholderText( "cont_type" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- id_in_old
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "id_in_old", )
        self.id_in_old_field     = edit_field
        edit_field.setPlaceholderText( "id_in_old" )
        edit_field.setReadOnly( True )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- loc_add_info
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "loc_add_info", )
        self.loc_add_info_field     = edit_field
        edit_field.setPlaceholderText( "loc_add_info" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- status
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "status", )
        self.status_field     = edit_field
        edit_field.setPlaceholderText( "status" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- model
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "model", )
        self.model_field     = edit_field
        edit_field.setPlaceholderText( "model" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- manufact
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "manufact", )
        self.manufact_field     = edit_field
        edit_field.setPlaceholderText( "manufact" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- serial_no
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "serial_no", )
        self.serial_no_field     = edit_field
        edit_field.setPlaceholderText( "serial_no" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- title
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "title", )
        self.title_field     = edit_field
        edit_field.is_keep_prior_enabled        = True
        edit_field.setPlaceholderText( "title" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- author
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "author", )
        self.author_field     = edit_field
        edit_field.setPlaceholderText( "author" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- publish
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "publish", )
        self.publish_field     = edit_field
        edit_field.setPlaceholderText( "publish" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- performer
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "performer", )
        self.performer_field     = edit_field
        edit_field.setPlaceholderText( "performer" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- format
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "format", )
        self.format_field     = edit_field
        edit_field.setPlaceholderText( "format" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- value
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "value", )
        self.value_field     = edit_field
        edit_field.setPlaceholderText( "value" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- project
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "project", )
        self.project_field     = edit_field
        edit_field.setPlaceholderText( "project" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- file
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "file", )
        self.file_field     = edit_field
        edit_field.setPlaceholderText( "file" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- owner
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "owner", )
        self.owner_field     = edit_field
        edit_field.setPlaceholderText( "owner" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- start_ix
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "start_ix", )
        self.start_ix_field     = edit_field
        edit_field.setPlaceholderText( "start_ix" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- end_ix
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "end_ix", )
        self.end_ix_field     = edit_field
        edit_field.setPlaceholderText( "end_ix" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- sign_out
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "sign_out", )
        self.sign_out_field     = edit_field
        edit_field.setPlaceholderText( "sign_out" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- inv_id
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "inv_id", )
        self.inv_id_field     = edit_field
        edit_field.setPlaceholderText( "inv_id" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- c_name
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "c_name", )
        self.c_name_field     = edit_field
        edit_field.setPlaceholderText( "c_name" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- url
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "url", )
        self.url_field     = edit_field
        edit_field.setPlaceholderText( "url" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- author_f
        edit_field                  = cw.CQLineEdit(
                                                parent         = None,
                                                field_name     = "author_f", )
        self.author_f_field     = edit_field
        edit_field.setPlaceholderText( "author_f" )
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 2 )

        # ---- dt_enter
        edit_field                  = cw.CQDateEdit(
                                                parent         = None,
                                                field_name     = "dt_enter", )
        self.dt_enter_field     = edit_field
        edit_field.setPlaceholderText( "dt_enter" )
        edit_field.rec_to_edit_cnv        = edit_field.cnv_int_to_qdate
        edit_field.dict_to_edit_cnv       = edit_field.cnv_int_to_qdate
        edit_field.edit_to_rec_cnv        = edit_field.cnv_qdate_to_int
        edit_field.edit_to_dict_cnv       = edit_field.cnv_qdate_to_int
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 1 )

        # ---- dt_item
        edit_field                  = cw.CQDateEdit(
                                                parent         = None,
                                                field_name     = "dt_item", )
        self.dt_item_field     = edit_field
        edit_field.setPlaceholderText( "dt_item" )
        edit_field.rec_to_edit_cnv        = edit_field.cnv_int_to_qdate
        edit_field.dict_to_edit_cnv       = edit_field.cnv_int_to_qdate
        edit_field.edit_to_rec_cnv        = edit_field.cnv_qdate_to_int
        edit_field.edit_to_dict_cnv       = edit_field.cnv_qdate_to_int
        self.data_manager.add_field( edit_field, is_key_word = False )
        layout.addWidget( edit_field, columnspan = 1 )



    # ---------------------------
    def select_record( self, id_value  ):
        """
        extension for the ddl
        read it
        """
        super().select_record( id_value )
        # this next should be gathered from the record
        # self.plant_combo_dict_ext.get_info_for_id_if( id_value )

        # !! temp remove till fixed
        # # see if this works, no select
        # self.stuff_combo_dict_ext.get_info_from_record(
        #                 self.data_manager.current_id,
        #                 self.data_manager.current_record  )

    # ------------------------
    def get_picture_file_name(self):
        """
        some promotable -- but picture is special only one file, rest
        work differently
        see picture document

        return file_name or None if no file name
        """
        debug_msg    = ( f"{self.tab_name}get_picture_file_name to be implemented" )
        logging.log( LOG_LEVEL, debug_msg, )
        return


    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = "\n>>>>>>>>>>* StuffDetailTab *<<<<<<<<<<<<"

        a_str   = string_util.to_columns( a_str, ["key_word_table_name",
                                           f"{self.key_word_table_name}" ] )

        a_str   = string_util.to_columns( a_str, ["detail_notebook",
                                           f"{self.detail_notebook}" ] )
        a_str   = string_util.to_columns( a_str, ["enable_send_topic_update",
                                           f"{self.enable_send_topic_update}" ] )
        a_str   = string_util.to_columns( a_str, ["event_sub_tab",
                                           f"{self.event_sub_tab}" ] )
        # a_str   = string_util.to_columns( a_str, ["record_state",
        #                                    f"{self.record_state}" ] )

        # a_str   = string_util.to_columns( a_str, ["tab_model",
        #                                    f"{self.tab_model}" ] )
        # a_str   = string_util.to_columns( a_str, ["tab_name",
        #                                    f"{self.tab_name}" ] )
        # a_str   = string_util.to_columns( a_str, ["table",
        #                                            f"{self.table}" ] )

        # a_str   = string_util.to_columns( a_str, ["add_kw_field",
        #                                    f"{self.add_kw_field}" ] )
        # a_str   = string_util.to_columns( a_str, ["author_f_field",
        #                                    f"{self.author_f_field}" ] )
        # a_str   = string_util.to_columns( a_str, ["author_field",
        #                                    f"{self.author_field}" ] )
        # a_str   = string_util.to_columns( a_str, ["c_name_field",
        #                                    f"{self.c_name_field}" ] )
        # a_str   = string_util.to_columns( a_str, ["cmnt_field",
        #                                    f"{self.cmnt_field}" ] )
        # a_str   = string_util.to_columns( a_str, ["cont_type_field",
        #                                    f"{self.cont_type_field}" ] )
        # a_str   = string_util.to_columns( a_str, ["descr_field",
        #                                    f"{self.descr_field}" ] )

        # a_str   = string_util.to_columns( a_str, ["dt_enter_field",
        #                                    f"{self.dt_enter_field}" ] )
        # a_str   = string_util.to_columns( a_str, ["dt_item_field",
        #                                    f"{self.dt_item_field}" ] )

        # a_str   = string_util.to_columns( a_str, ["end_ix_field",
        #                                    f"{self.end_ix_field}" ] )

        # a_str   = string_util.to_columns( a_str, ["file_field",
        #                                    f"{self.file_field}" ] )
        # a_str   = string_util.to_columns( a_str, ["format_field",
        #                                    f"{self.format_field}" ] )
        # a_str   = string_util.to_columns( a_str, ["id_field",
        #                                    f"{self.id_field}" ] )
        # a_str   = string_util.to_columns( a_str, ["id_in_old_field",
        #                                    f"{self.id_in_old_field}" ] )
        # a_str   = string_util.to_columns( a_str, ["id_old_field",
        #                                    f"{self.id_old_field}" ] )
        # a_str   = string_util.to_columns( a_str, ["inv_id_field",
        #                                    f"{self.inv_id_field}" ] )
        # a_str   = string_util.to_columns( a_str, ["loc_add_info_field",
        #                                    f"{self.loc_add_info_field}" ] )
        # a_str   = string_util.to_columns( a_str, ["manufact_field",
        #                                    f"{self.manufact_field}" ] )
        # a_str   = string_util.to_columns( a_str, ["model_field",
        #                                    f"{self.model_field}" ] )
        # a_str   = string_util.to_columns( a_str, ["name_field",
        #                                    f"{self.name_field}" ] )
        # a_str   = string_util.to_columns( a_str, ["owner_field",
        #                                    f"{self.owner_field}" ] )
        # a_str   = string_util.to_columns( a_str, ["performer_field",
        #                                    f"{self.performer_field}" ] )
        a_str   = string_util.to_columns( a_str, ["picture_sub_tab",
                                           f"{self.picture_sub_tab}" ] )
        # a_str   = string_util.to_columns( a_str, ["project_field",
        #                                    f"{self.project_field}" ] )
        # a_str   = string_util.to_columns( a_str, ["publish_field",
        #                                    f"{self.publish_field}" ] )

        # a_str   = string_util.to_columns( a_str, ["serial_no_field",
        #                                    f"{self.serial_no_field}" ] )
        # a_str   = string_util.to_columns( a_str, ["sign_out_field",


        # b_str   = self.super().__str__( self )
        # a_str   = a_str + "\n" + b_str

        # ---- causing recursion ??
        # b_str   =  super().__str__(  )
        # a_str   = a_str + "\n" + b_str

        return a_str

# ==================================
class StuffTextTab( base_document_tabs.TextTabBase  ):
    """
    """
    #--------------------------------------
    def __init__(self, parent_window  ):
        """
        Args:
            parent_window (TYPE): DESCRIPTION.
        """
        super().__init__( parent_window )

        # msg       = ( "init StuffTextTab" )
        # logging.debug( msg )

        #super().__init__( parent_window )
        self.tab_name            = "StuffTextTab"

        # msg       = ( "init end StuffTextTab {self.tab_name = }" )
        # logging.debug( msg )

        self.post_init()

# ----------------------------------------
class StuffHistoryTab( base_document_tabs.HistoryTabBase   ):
    """
    """
    def __init__(self, parent_window ):
        """
        """
        super().__init__( parent_window )

        self.tab_name            = "StuffHistorylTab"

# ------------------------------------
class EventSqlTableModel(QSqlTableModel):
    """
    from chat as a way to control editabllity and
    centering, is this a good idea
    what happened to column 1 stuff id
    """
    def __init__(self, parent=None, db=QSqlDatabase()):
        super().__init__(parent, db)
        # Specify multiple columns to make non-editable (e.g., columns 1 and 2)
        #self.non_editable_columns = { 0, 1, }  # Columns ..doe it have to be in init or is synamic ..
        self.non_editable_columns = { 99 }

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

    # ----------------------------
    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        """
        for special formatting
        and alignment
        """
        col = index.column()

        # Check role first
        if role == Qt.DisplayRole:
            # Handle display formatting for event_dt (column 2)
            if col == 2:
                value = super().data(index, Qt.EditRole)
                if value is not None:
                    return datetime.fromtimestamp(value).strftime("%Y-%m-%d")
                return value  # Return raw value if None

        elif role == Qt.EditRole:
            # Return raw value for editing/database sync
            if col == 2:
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


    def data_old(self, index: QModelIndex, role=Qt.DisplayRole):
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
class StuffEventSubTab( base_document_tabs.SubTabBaseOld  ):

    def __init__(self, parent_window ):
        """

        """
        super().__init__( parent_window )
        #self.parent_window   = parent_window
        self.list_ixxx         = 5  # should track selected an item in detail

        self.table_name      = "stuff_event"
        self.list_table_name = self.table_name   # delete this
        self.tab_name        = "StuffEventSubTab"
        #self.tab_name            = "StuffEventSubTab  not needed tis is a sub tab
        #self.current_id      = None
        #self.current_id      = 28
        #rint( "fix stuff event select and delete line above should be select_by_id  ")
        self._build_model()
        self._build_gui()

        #self.parent_window.sub_tab_list.append( self )    # a function might be better may be obsolete

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
           # now do not need stuff in EventSql.....

        view.setSelectionBehavior( QTableView.SelectRows )

        ix_col = -1   # could make loop or even list comp

        ix_col += 1
        model.setHeaderData( ix_col, Qt.Horizontal, "ID" )
        view.setColumnWidth( ix_col, 100)  # Set  width in  pixels

        ix_col += 1
        model.setHeaderData( ix_col, Qt.Horizontal, "Stuff ID" )
        view.setColumnWidth( ix_col, 100)  # Set  width in  pixels
        #view.setColumnHidden( 1, True )  # view or model

        ix_col += 1
        model.setHeaderData( ix_col, Qt.Horizontal, "Date" )
        view.setColumnWidth( ix_col, 100)  # Set  width in  pixels

        ix_col += 1
        model.setHeaderData( ix_col, Qt.Horizontal, "$ Amount" )
        view.setColumnWidth( ix_col, 100)  # Set  width in  pixels

        ix_col += 1
        model.setHeaderData( ix_col, Qt.Horizontal, "Comment" )
        view.setColumnWidth( ix_col, 300)  # Set  width in  pixels

        ix_col += 1
        model.setHeaderData( ix_col, Qt.Horizontal, "Type" )
        view.setColumnWidth( ix_col, 100)  # Set  width in  pixels

        #view.setColumnHidden( 1, True )  # view or model

        # might want a loop for this
        # seems to be only after set model
        # STUFF_ID_COL    = 1
        # view.hideColumn( STUFF_ID_COL )

        layout.addWidget( view )

        # ---- buttons
        widget        = QPushButton( 'Add' )
        #add_button    = widget
        widget.clicked.connect( self.add_new_event )
        button_layout.addWidget( widget )

        #
        widget        = QPushButton('Edit')
        #add_button    = widget
        widget.clicked.connect(self.edit_selected_event )
        button_layout.addWidget( widget )

        #
        widget        = QPushButton('Delete')
        #add_button    = widget
        widget.clicked.connect(self.delete_record)
        button_layout.addWidget( widget )

    # ---------------------------------
    def _build_model( self, ):
        """

        """
        #model              = qt_with_logging.QSqlTableModelWithLogging(  self, self.db    )
        model              = EventSqlTableModel(  self, self.db    )
        #model              = QSqlTableModel(  self, self.db    )
        self.model         = model

        model.setTable( self.list_table_name )
        model.setEditStrategy( QSqlTableModel.OnManualSubmit )
        #model.non_editable_columns = {0, 1, }  # really only work on custom model


    # ---------------------------------------
    def select_by_id( self, id ):
        """
        maybe make anscestor and promote but filter need name of key field

        """
        # ---- write
        model               = self.model

        self.current_id     = id
        model.setFilter( f"stuff_id = {id}" )  # for stuff_event
        # model_write.setFilter( f"pictureshow_id = {id} " )
        model.select()

        debug_msg    = ( f"event subtab select_by_id do we need next stuff_id = {id}" )
        logging.debug( debug_msg )

    # -------------------------------------
    def i_am_hsw(self):
        """
        make sure call is to here

        """
        debug_msg   = ( f"{self.tab_name} i_am_hsw" )
        logging.debug( debug_msg )

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
    def add_record_old(self):
        """
        what it says, read?
        add test for success an refactor??
        """
        model      = self.model
        dialog     = stuff_document_edit.EditStuffEvents( model, index = None, parent = self )
        if dialog.exec_() == QDialog.Accepted:
            #self.model.submitAll()
            ok     = base_document_tabs.model_submit_all(
                       model,  f"StuffEventsSubTab.add_record " )
            model.select()

    # ------------------------------------------
    def edit_record_old(self):
        """
        what it says, read?
        """
        index       = self.view.currentIndex()
        model       = self.model
        if index.isValid():
            #dialog = stuff_document_edit.EditStuffEvents( model, index, parent = self )
            dialog = stuff_document_edit.EditStuffEvents( self )
            if dialog.exec_() == QDialog.Accepted:
                #self.model.submitAll()
                ok     = base_document_tabs.model_submit_all(
                           model,  f"StuffEventsSubTab.add_record " )
                #ia_qt.q_sql_table_model( self.model, "post edit_record submitAll()" )
                model.select()
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

    #---------------- restart here model view dialog name
    #  ---- chat functions
    def add_new_event(self):
        """Open dialog to add a new event and insert it into the model."""
        #dialog = StuffEventDialog(self)
        dialog = stuff_document_edit.EditStuffEvents( self )  # the parent tab
        model    = self.model
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
            model.setData( model.index(row, 0), a_id )
            old_non_editable                = model.non_editable_columns
            model.non_editable_columns  = { 99 } # beyond all columns

            debug_id  = self.current_id
            # model.setData( model.index(row, 1), form_data["stuff_id"])
            model.setData( model.index(row, 1), self.current_id )

            model.non_editable_columns  = old_non_editable

            model.setData( model.index(row, 2), form_data["event_dt"])
            model.setData( model.index(row, 3), form_data["dlr"])
            model.setData( model.index(row, 4), form_data["cmnt"])
            model.setData( model.index(row, 5), form_data["type"])

    #------------------------
    def get_selected_row_data(self):
        """Get the data from the currently selected row."""
        # Get the currently selected row
        model    = self.model

        indexes = self.view.selectedIndexes()
        if not indexes:
            QMessageBox.warning(self, "Warning", "No record selected.")
            return None

        # Get the model row index
        model_row = indexes[0].row()


        a_timestamp = self.model.data(self.model.index(0, 2), Qt.EditRole)
        print(f"Raw timestamp: {a_timestamp = }")


        # Extract data from the row
        data = {
            "id":        model.data( model.index( model_row, 0)),
            "stuff_id":  model.data( model.index( model_row, 1)),

            # "event_dt":  model.data( model.index( model_row, 2)),
            "event_dt":  a_timestamp,

            "dlr":       model.data( model.index( model_row, 3)),
            "cmnt":      model.data( model.index( model_row, 4)),
            "type":      model.data( model.index( model_row, 5))
        }

        return (model_row, data)

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
        dialog = stuff_document_edit.EditStuffEvents( self, edit_data=data )
            # self the parent tab

        model     = self.model

        if dialog.exec_() == QDialog.Accepted:
            form_data = dialog.get_form_data()

            # Update the row with the new data
            model.setData( model.index(row, 0), form_data["id"])
            model.setData( model.index(row, 1), form_data["stuff_id"])
            model.setData( model.index(row, 2), form_data["event_dt"])
            model.setData( model.index(row, 3), form_data["dlr"])
            model.setData( model.index(row, 4), form_data["cmnt"])
            model.setData( model.index(row, 5), form_data["type"])

    # ----------------------------------
    def delete_selected_event(self):
        """Delete the currently selected event."""
        selected_data = self.get_selected_row_data()
        if selected_data is None:
            return

        row, data = selected_data

        # Confirm deletion with the user
        reply = QMessageBox.question(self, "Confirm Deletion",
                                    f"Are you sure you want to delete the selected event (ID: {data['id']})?",
                                    QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Remove the row from the model
            self.model.removeRow(row)

    def submit_changes(self):
        """Submit all changes to the database."""
        if self.model.submitAll():
            pass
            #QMessageBox.information(self, "Success", "Changes saved to database successfully.")

        else:
            msg   = f"Database error: {self.model.lastError().text()}"
            logging.error( msg )
            QMessageBox.warning(self, "Error", msg )

    #-------------------------------
    def update_db( self ):
        """update_db
        for now a forward, pull back later
        """
        self.submit_changes( )

    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = "\n>>>>>>>>>>* StuffEventSubTab  *<<<<<<<<<<<<"

        return a_str

# ------------------------------------
class StuffPictureListSubTab( base_document_tabs.PictureListSubTabBase ):
    """
    almost all promoted even this may not be necessary
    """
    def __init__(self, parent_window ):
        super().__init__( parent_window )
        self.pictures_for_table  = "stuff"


# ---- eof ------------------------------
