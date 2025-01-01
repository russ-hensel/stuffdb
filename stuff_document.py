#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
# ---- main
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    main.main()
# --------------------


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


# ---- begin pyqt from import_qt.py

#from   functools import partial
import functools
import time

import gui_qt_ext
import string_util
from app_global import AppGlobal
from pubsub import pub
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


# ---- imports local
import base_document_tabs
import custom_widgets
import key_words
import mdi_management
import qt_sql_query
import qt_with_logging
import stuff_document_edit
import info_about
import data_manager

FIF       = info_about.INFO_ABOUT.find_info_for

# ----------------------------------------
class StuffDocument( base_document_tabs.DocumentBase ):
    """
    for the stuff table....
    """
    def __init__(self, ):
        """
        the usual
        """
        super().__init__()

        mdi_area                = AppGlobal.main_window.mdi_area
        # we could return the subwindow for parent to addS
        sub_window              = self
        # sub_window.setWindowTitle( "this title may be replaced " )
        self.db                 = AppGlobal.qsql_db_access.db

        self.detail_table_name      = "stuff"
        self.key_word_table_name    = "stuff_key_word"
        self.text_table_name        = "stuff_text"  # text tables always id and text_data

        self.subwindow_name         = "StuffSubWindow"

        self.setWindowTitle( self.subwindow_name )
        self._build_gui()
        # self.__init_2__( ) # back to parent for more init

    # --------------------------------
    def get_topic( self ):
        """
        move code down to detail in future --- less copling
        of the detail record -- now info
        !! make this smarter for empty fields....
        need to sync to picture get_stuff_info, a pain

                info      = (f"ID: {a_id = }  { name = }  {descr = }  ")
                # consider check for empty, too long so far just debug
                return info

        """
        info     = "stuff info false record_state "
        if self.record_state:
            a_id        = self.detail_tab.id_field.get_raw_data()
            name        = self.detail_tab.name_field.get_raw_data()
            descr       = self.detail_tab.descr_field.get_raw_data()
            #topic    = f"{topic} {self.record_state = }"
            #topic     = f"{topic} {self.detail_tab.name_field.text() = }"
            info      = (f"{ name = }  {descr = }  ") #!! this is a debug format
            # info    = (f"{ name} {descr}")strip()
            if info == "":
                info = f"stuff {a_id} has blank name and description"
        return  info

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
        self.detail_tab_index     = ix
        self.detail_tab           = StuffDetailTab( self )
        main_notebook.addTab( self.detail_tab, "Detail"     )

        ix                       += 1
        self.picture_tab_index     = ix
        self.picture_tab           = base_document_tabs.StuffdbPictureTab( self )
        main_notebook.addTab( self.picture_tab, "Picture"     )

        ix                         += 1
        self.detail_text_index      = ix
        self.text_tab               = StuffTextTab( self )
        main_notebook.addTab( self.text_tab, "Text"     )

        ix                         += 1
        self.history_tab_index     = ix
        self.history_tab           = StuffHistoryTab( self )
        main_notebook.addTab( self.history_tab, "History"    )

        sub_window.setWidget( main_notebook )
        mdi_area.addSubWindow( sub_window )  # perhaps add to register_document in midi_management

        sub_window.show()

    # ---------------------------------------
    def fetch_id_testxxxx( self, ):
        """
        just for testing will be deleted
        """
        id  = 55
        print( f"fetch_id_test{id=}")
        self.fetch_row_by_id(  id )
        # self.text_tab.fetch_text_row_by_id(  id )

    # -------------------------------------
    def i_am_hsw(self):
        """
        make sure call is to here for testing
        """
        print( f"{self.tab_name} stuff sub window, i_am_hsw")

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

    # -- ------------------------------------
    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = ">>>>>>>>>>* StuffDocument  *<<<<<<<<<<<<"


        b_str   = self.super().__str__( self )
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
        !! ?? promote
        """
        super().__init__( parent_window )
        self.tab_name            = "StuffCriteriaTab"

    # ------------------------------------------
    def _build_tab( self, ):
        """
        what it says, read

        """
        page            = self
        tab             = page

        placer          = gui_qt_ext.PlaceInGrid(
            central_widget=page,
            a_max=0,
            by_rows=False  )

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

        # ----descr
        widget                = QLabel( "descr" )
        placer.new_row()
        placer.place( widget )

        widget                  = custom_widgets.CQLineEditCriteria( get_type = "string", set_type = "string")
        self.key_words_widget   = widget
        self.critera_widget_list.append( widget )
        widget.critera_name    = "descr"
        widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        placer.place( widget, columnspan = 3 )

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
        do select base on the criteria_dict
        """
        parent_document                 = self.parent_window

        model                           = parent_document.list_tab.list_model
        #rint( "begin channel_select for the list")
        query                           = QSqlQuery()
        query_builder                   = qt_sql_query.QueryBuilder( query, print_it = False, )

        kw_table_name                   = "stuff_key_words"
        column_list                     = [ "id", "id_old", "name", "descr",  "add_kw",         ]

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


        # widget.addItem('Ascending')
        # widget.addItem('Decending')
        order_by_dir   = criteria_dict[ "order_by_dir" ].lower( )

        msg    = f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{column_name = }  {order_by_dir = }"
        print( msg )

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
                                                  msg = f"{self.tab_name} criteria_select" )

        msg      = (  query.executedQuery()   )
        AppGlobal.logger.info( msg )
        print( msg )
        parent_document.main_notebook.setCurrentIndex( parent_document.list_tab_index )
        self.critera_is_changed = False

# ----------------------------------------
class StuffListTab( base_document_tabs.DetailTabBase  ):

    def __init__(self, parent_window ):

        super().__init__( parent_window  )

        self.list_ix            = 5  # should track selected an item in detail

        self.tab_name           = "StuffListTab"

        self._build_gui()

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says, read
        !! initial query should come out
            except for table seems promotobable, but then extend to set the table
            or get table from parent
        """
        page            = self
        tab             = page
        # a_notebook.addTab( page, 'Channels ' )
        placer          = gui_qt_ext.PlaceInGrid(
            central_widget=page,
            a_max=0,
            by_rows=False  )

        # Set up the model
        model_class         = QSqlTableModel
        model_class         = base_document_tabs.ReadOnlySqlTableModel
        model               = model_class(
            self, self.parent_window.db )  # perhaps a global
        self.list_model     = model

        model.setTable( self.parent_window.detail_table_name )

        model.setEditStrategy( QSqlTableModel.OnManualSubmit )

        # COMMENT  out to default headers
        # model.setHeaderData( 0, Qt.Horizontal, "ID")
        # model.setHeaderData( 1, Qt.Horizontal, "TEXT DATA"  )

        # ----view
        view                 = QTableView()
        self.list_view       = view     # consider change to just self.view\
        view.setSelectionBehavior( QTableView.SelectRows )
        view.setModel( model )
        placer.place(  view )
        view.clicked.connect( self.parent_window.on_list_clicked )

# ----------------------------------------
class StuffDetailTab( base_document_tabs.DetailTabBase  ):
    """
    """
    def __init__(self, parent_window  ):
        """
        the usual
        """
        super().__init__( parent_window )


        self.tab_name           = "StuffDetailTab"
        #self.table_name         = "stuff"      # probably should get from parent
        #self.table_name         = parent_window.detail_table_name  # promote me


        self.enable_send_topic_update    = True
        self.key_word_table_name         = "stuff_key_word"
        self.post_init()


    # -------------------------------------
    def _build_gui( self ):
        """
        what it says read
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


    #---------------------------------
    def _build_fields( self, layout ):
        """
        What it says, read
            this is generated code, then tweaked.
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
        edit_field.setPlaceholderText( "id" )
        self.data_manager.add_field( edit_field )
        layout.addWidget( edit_field )

        # ---- id_old
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "id_old",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.id_old_field         = edit_field
        edit_field.setPlaceholderText( "id_old" )
        self.data_manager.add_field( edit_field )
        #self.data_manager.add_field( edit_field )
        layout.addWidget( edit_field )

        # ---- add_kw
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "add_kw",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.add_kw_field         = edit_field
        edit_field.setPlaceholderText( "add_kw", )
        edit_field.set_data_to_default    = edit_field.set_data_to_pass

        # self.id_field         = edit_field     # not sre names are ever used
        self.data_manager.add_field( edit_field, is_key_word = True )


        #self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- descr
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "descr",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.descr_field         = edit_field
        edit_field.setPlaceholderText( "descr" )
        #self.field_list.append( edit_field )
        self.data_manager.add_field( edit_field, is_key_word = True )
        layout.addWidget( edit_field )

        # ---- type
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "type",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.type_field         = edit_field
        edit_field.setPlaceholderText( "type" )
        self.data_manager.add_field( edit_field, )
        layout.addWidget( edit_field )

        # ---- type_sub
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "type_sub",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.type_sub_field         = edit_field
        edit_field.setPlaceholderText( "type_sub" )
        self.data_manager.add_field( edit_field, )
        layout.addWidget( edit_field )

        # ---- author
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "author",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.author_field         = edit_field
        edit_field.setPlaceholderText( "author" )
        #self.field_list.append( edit_field )
        self.data_manager.add_field( edit_field, )
        layout.addWidget( edit_field )

        # ---- publish
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "publish",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.publish_field         = edit_field
        edit_field.setPlaceholderText( "publish" )
        self.data_manager.add_field( edit_field, )
        layout.addWidget( edit_field )

        # ---- model
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "model",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.model_field         = edit_field
        edit_field.setPlaceholderText( "model" )
        self.data_manager.add_field( edit_field, )
        layout.addWidget( edit_field )

        # ---- serial_no
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "serial_no",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.serial_no_field         = edit_field
        edit_field.setPlaceholderText( "serial_no" )
        self.data_manager.add_field( edit_field, )
        layout.addWidget( edit_field )

                                                # timestamp to qdates make these non editable

        # ---- value
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "value",
                                                db_type        = "integer",
                                                display_type   = "string" )
        self.value_field         = edit_field
        edit_field.setPlaceholderText( "value" )
        self.data_manager.add_field( edit_field, )
        layout.addWidget( edit_field )

        # ---- project
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "project",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.project_field         = edit_field
        edit_field.setPlaceholderText( "project" )
        self.data_manager.add_field( edit_field, )
        layout.addWidget( edit_field )

        # ---- file
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "file",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.file_field         = edit_field
        edit_field.setPlaceholderText( "file" )
        self.data_manager.add_field( edit_field, )
        layout.addWidget( edit_field )

        # ---- owner
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "owner",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.owner_field         = edit_field
        edit_field.setPlaceholderText( "owner" )
        self.data_manager.add_field( edit_field, )
        layout.addWidget( edit_field )

                                                # timestamp to qdates make these non editable

        # ---- dt_enter
        edit_field                  = custom_widgets.CQDateEdit(
                                                parent         = None,
                                                field_name     = "dt_enter",
                                                db_type        = "timestamp",
                                                display_type   = "qdate" )
        self.dt_enter_field         = edit_field
        #edit_field.setPlaceholderText( "dt_enter" )
        #self.field_list.append( edit_field )
        self.data_manager.add_field( edit_field )
        layout.addWidget( edit_field )

        # ---- start_ix
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "start_ix",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.start_ix_field         = edit_field
        edit_field.setPlaceholderText( "start_ix" )
        #self.field_list.append( edit_field )
        self.data_manager.add_field( edit_field )
        layout.addWidget( edit_field )

        # ---- end_ix
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "end_ix",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.end_ix_field         = edit_field
        edit_field.setPlaceholderText( "end_ix" )
        self.data_manager.add_field( edit_field )
        #self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- sign_out
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "sign_out",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.sign_out_field         = edit_field
        edit_field.setPlaceholderText( "sign_out" )
        #self.field_list.append( edit_field )
        self.data_manager.add_field( edit_field )
        layout.addWidget( edit_field )

        # ---- format
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "format",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.format_field         = edit_field
        edit_field.setPlaceholderText( "format" )
        #self.field_list.append( edit_field )
        self.data_manager.add_field( edit_field )
        layout.addWidget( edit_field )

        # ---- inv_id
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "inv_id",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.inv_id_field         = edit_field
        edit_field.setPlaceholderText( "inv_id" )
        self.data_manager.add_field( edit_field )
        # self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- cmnt
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "cmnt",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.cmnt_field         = edit_field
        edit_field.setPlaceholderText( "cmnt" )
        self.data_manager.add_field( edit_field )
        #self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- status
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "status",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.status_field         = edit_field
        edit_field.setPlaceholderText( "status" )
        self.data_manager.add_field( edit_field )
        #self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- id_in_old
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "id_in_old",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.id_in_old_field         = edit_field
        edit_field.setPlaceholderText( "id_in_old" )
        self.data_manager.add_field( edit_field )
        #self.field_list.append( edit_field )
        layout.addWidget( edit_field )

                                                # timestamp to qdates make these non editable

        # ---- dt_item
        edit_field                  = custom_widgets.CQDateEdit(
                                                parent         = None,
                                                field_name     = "dt_item",
                                                db_type        = "timestamp",
                                                display_type   = "qdate" )
        self.dt_item_field         = edit_field
        #edit_field.setPlaceholderText( "dt_item" )

        self.data_manager.add_field( edit_field )
        layout.addWidget( edit_field )

        # ---- c_name
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "c_name",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.c_name_field         = edit_field
        edit_field.setPlaceholderText( "c_name" )
        self.data_manager.add_field( edit_field )
        #self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- performer
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "performer",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.performer_field         = edit_field
        edit_field.setPlaceholderText( "performer" )
        self.data_manager.add_field( edit_field )
        layout.addWidget( edit_field )

        # ---- cont_type
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "cont_type",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.cont_type_field         = edit_field
        edit_field.setPlaceholderText( "cont_type" )
        self.data_manager.add_field( edit_field )
        layout.addWidget( edit_field )

        # ---- url
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "url",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.url_field         = edit_field
        edit_field.setPlaceholderText( "url" )
        self.data_manager.add_field( edit_field )
        layout.addWidget( edit_field )

        # ---- author_f
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "author_f",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.author_f_field         = edit_field
        edit_field.setPlaceholderText( "author_f" )
        self.data_manager.add_field( edit_field )
        layout.addWidget( edit_field )

        # ---- title
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "title",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.title_field         = edit_field
        edit_field.setPlaceholderText( "title" )
        self.data_manager.add_field( edit_field )
        layout.addWidget( edit_field )

        # ---- name
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "name",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.name_field         = edit_field
        edit_field.setPlaceholderText( "name" )
        self.data_manager.add_field( edit_field )
        self.data_manager.add_field( edit_field, )
        layout.addWidget( edit_field )

        # ---- loc_add_info
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "loc_add_info",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.loc_add_info_field         = edit_field
        edit_field.setPlaceholderText( "loc_add_info" )
        self.data_manager.add_field( edit_field, )
        layout.addWidget( edit_field )

        # ---- manufact
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "manufact",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.manufact_field         = edit_field
        edit_field.setPlaceholderText( "manufact" )
        self.data_manager.add_field( edit_field, )
        layout.addWidget( edit_field )

        # ---- code_gen: detail_tab_build_gui use for _build_fields was_build_gui  -- end table entries

    # -----------------------------
    def copy_prior_rowxxx( self, next_key ):
        """
        info is in the edits
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
        # rint(  ia_qt.q_line_edit( self.name_field,
        #                   msg = "this is the name field",  ) # include_dir = True ) )

        # add_ts   = self.add_ts_field.text()
        edit_ts  = self.edit_ts_field.text()
        edit_ts  = "self.edit_ts_field.text()"   # !! test

        self.default_new_row(  next_key )

        # ---- set the defaults

        self.descr_field.setText( descr + "*" )
        # self.url_field.setText( url )

        # # ---- ??redef add_ts

    # -----------------------------
    def default_new_rowxxxx(self, next_key ):
        """
        what it says
            this is for a new row on the window -- no save
        arg:
            next_key for table, just trow out if not used
        Returns:
            None.
        """

        # model    = self.detail_model

        # yt_id    = self.yt_id_field.text()
        # name     = self.name_field.text()
        # #rint(  ia_qt.q_line_edit( self.name_field,
        # #                   msg = "this is the name field",  ) # include_dir = True ) )
        # url      = self.url_field.text()
        # mypref   = self.mypref_field.text()
        # mygroup  = self.mygroup_field.text()
        # add_ts   = self.add_ts_field.text()

        self.clear_detail_fields()

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
        see picture document

        return file_name or None if no file name
        """
        print( f"{self.tab_name}get_picture_file_name to be implemented" )
        return

    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = ">>>>>>>>>>* StuffDetailTab *<<<<<<<<<<<<"

        a_str   = string_util.to_columns( a_str, ["key_word_table_name",
                                           f"{self.key_word_table_name}" ] )

        a_str   = string_util.to_columns( a_str, ["detail_notebook",
                                           f"{self.detail_notebook}" ] )
        a_str   = string_util.to_columns( a_str, ["enable_send_topic_update",
                                           f"{self.enable_send_topic_update}" ] )
        a_str   = string_util.to_columns( a_str, ["event_sub_tab",
                                           f"{self.event_sub_tab}" ] )
        a_str   = string_util.to_columns( a_str, ["record_state",
                                           f"{self.record_state}" ] )

        a_str   = string_util.to_columns( a_str, ["tab_model",
                                           f"{self.tab_model}" ] )
        a_str   = string_util.to_columns( a_str, ["tab_name",
                                           f"{self.tab_name}" ] )
        a_str   = string_util.to_columns( a_str, ["table",
                                                   f"{self.table}" ] )

        a_str   = string_util.to_columns( a_str, ["add_kw_field",
                                           f"{self.add_kw_field}" ] )
        a_str   = string_util.to_columns( a_str, ["author_f_field",
                                           f"{self.author_f_field}" ] )
        a_str   = string_util.to_columns( a_str, ["author_field",
                                           f"{self.author_field}" ] )
        a_str   = string_util.to_columns( a_str, ["c_name_field",
                                           f"{self.c_name_field}" ] )
        a_str   = string_util.to_columns( a_str, ["cmnt_field",
                                           f"{self.cmnt_field}" ] )
        a_str   = string_util.to_columns( a_str, ["cont_type_field",
                                           f"{self.cont_type_field}" ] )
        a_str   = string_util.to_columns( a_str, ["descr_field",
                                           f"{self.descr_field}" ] )

        a_str   = string_util.to_columns( a_str, ["dt_enter_field",
                                           f"{self.dt_enter_field}" ] )
        a_str   = string_util.to_columns( a_str, ["dt_item_field",
                                           f"{self.dt_item_field}" ] )

        a_str   = string_util.to_columns( a_str, ["end_ix_field",
                                           f"{self.end_ix_field}" ] )

        a_str   = string_util.to_columns( a_str, ["file_field",
                                           f"{self.file_field}" ] )
        a_str   = string_util.to_columns( a_str, ["format_field",
                                           f"{self.format_field}" ] )
        a_str   = string_util.to_columns( a_str, ["id_field",
                                           f"{self.id_field}" ] )
        a_str   = string_util.to_columns( a_str, ["id_in_old_field",
                                           f"{self.id_in_old_field}" ] )
        a_str   = string_util.to_columns( a_str, ["id_old_field",
                                           f"{self.id_old_field}" ] )
        a_str   = string_util.to_columns( a_str, ["inv_id_field",
                                           f"{self.inv_id_field}" ] )
        a_str   = string_util.to_columns( a_str, ["loc_add_info_field",
                                           f"{self.loc_add_info_field}" ] )
        a_str   = string_util.to_columns( a_str, ["manufact_field",
                                           f"{self.manufact_field}" ] )
        a_str   = string_util.to_columns( a_str, ["model_field",
                                           f"{self.model_field}" ] )
        a_str   = string_util.to_columns( a_str, ["name_field",
                                           f"{self.name_field}" ] )
        a_str   = string_util.to_columns( a_str, ["owner_field",
                                           f"{self.owner_field}" ] )
        a_str   = string_util.to_columns( a_str, ["performer_field",
                                           f"{self.performer_field}" ] )
        a_str   = string_util.to_columns( a_str, ["picture_sub_tab",
                                           f"{self.picture_sub_tab}" ] )
        a_str   = string_util.to_columns( a_str, ["project_field",
                                           f"{self.project_field}" ] )
        a_str   = string_util.to_columns( a_str, ["publish_field",
                                           f"{self.publish_field}" ] )

        a_str   = string_util.to_columns( a_str, ["serial_no_field",
                                           f"{self.serial_no_field}" ] )
        a_str   = string_util.to_columns( a_str, ["sign_out_field",
                                           f"{self.sign_out_field}" ] )
        a_str   = string_util.to_columns( a_str, ["start_ix_field",
                                           f"{self.start_ix_field}" ] )

        a_str   = string_util.to_columns( a_str, ["title_field",
                                           f"{self.title_field}" ] )
        a_str   = string_util.to_columns( a_str, ["type_field",
                                           f"{self.type_field}" ] )
        a_str   = string_util.to_columns( a_str, ["type_sub_field",
                                           f"{self.type_sub_field}" ] )
        a_str   = string_util.to_columns( a_str, ["url_field",
                                           f"{self.url_field}" ] )
        a_str   = string_util.to_columns( a_str, ["value_field",
                                           f"{self.value_field}" ] )
        a_str   = string_util.to_columns( a_str, ["status_field",
                                           f"{self.status_field}" ] )


        b_str   = self.super().__str__( self )
        a_str   = a_str + "\n" + b_str

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
        print( "init StuffTextTab" )
        super().__init__( parent_window )
        self.tab_name            = "StuffTextTab"
        print( "init end StuffTextTab {self.tab_name = }" )

        self.post_init()


# ----------------------------------------
class StuffHistoryTab( base_document_tabs.StuffdbHistoryTab   ):
    """
    """
    def __init__(self, parent_window ):
        """
        """
        super().__init__( parent_window )
        self.tab_name            = "StuffHistorylTab"

    # -------------------------------------
    def _build_gui( self ):
        """
        what it says read
        update ver 21 to picture_sub_window
        Returns:
            none
        """
        tab                     = self
        table                   = QTableWidget(
                                    0, 10, self )  # row column third arg parent
        self.history_table      = table

        ix_col                  = 1
        table.setColumnWidth( ix_col, 22 )

        table.setSelectionBehavior( QTableWidget.SelectRows )  # Select entire rows

        base_document_tabs.table_widget_no_edit( table )

        # table.clicked.connect( self.parent_window.on_history_clicked )
        # table.clicked.connect( self.on_list_clicked )
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

        ix_col          += 1
        item             = QTableWidgetItem( str( self.ix_seq  ) )
        table.setItem( ix_row, ix_col, item   )

        # # begin code gen ?
        ix_col          += 1
        item             = QTableWidgetItem( str( record.value( "id" ) ) )
        table.setItem( ix_row, ix_col, item   )


        ix_col          += 1
        item             = QTableWidgetItem( str( record.value( "add_kw" ) ) )
        table.setItem( ix_row, ix_col, item   )


        ix_col          += 1
        item             = QTableWidgetItem( str( record.value( "descr" ) ) )
        table.setItem( ix_row, ix_col, item   )

        # ----- end code gen

# ----------------------------------------
class StuffEventSubTab( base_document_tabs.SubTabBase  ):

    def __init__(self, parent_window ):
        """

        """
        super().__init__( parent_window )
        #self.parent_window   = parent_window
        self.list_ix         = 5  # should track selected an item in detail
        # needs work
        #self.db              = AppGlobal.qsql_db_access.db

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

        # model.setHeaderData( 0, Qt.Horizontal, "ID")
        # model.setHeaderData( 1, Qt.Horizontal, "YT ID"  )

        # Set up the view
        view                 = QTableView()
        #self.list_view       = view
        self.view            = view

        view.setSelectionBehavior( QTableView.SelectRows )
        view.setModel( self.model )

        # might want a loop for this
        # seems to be only after set model
        STUFF_ID_COL    = 1
        view.hideColumn( STUFF_ID_COL )

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

        # #
        # widget        = QPushButton( 'save_model')
        # #add_button    = widget
        # #widget.clicked.connect(self.save_model)
        # button_layout.addWidget( widget )

    # ---------------------------------
    def _build_model( self, ):
        """
        may have too many instances
        Returns:
            modifies self, establishes -- wrong names

        """
        model              = qt_with_logging.QSqlTableModelWithLogging(  self, self.db    )

        #self.model_write   = model   # phase out
        self.model         = model

        model.setTable( self.list_table_name )
        model.setEditStrategy( QSqlTableModel.OnManualSubmit )
        # model_write.setEditStrategy( QSqlTableModel.OnFieldChange )
        model.setFilter( "stuff_id = 28 " )
        print( "!!fix stuff_id = 28 ")

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

        print( "do we need next ")
        #self.list_view.setModel( model_write )

    # -------------------------------------
    def i_am_hsw(self):
        """
        make sure call is to here

        """
        print( f"{self.tab_name} i_am_hsw" )

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
        dialog     = stuff_document_edit.EditStuffEvents( model, index = None, parent = self )
        if dialog.exec_() == QDialog.Accepted:
            #self.model.submitAll()
            ok     = base_document_tabs.model_submit_all(
                       model,  f"StuffEventsSubTab.add_record " )
            model.select()

    # ------------------------------------------
    def edit_record(self):
        """
        what it says, read?
        """
        index       = self.view.currentIndex()
        model       = self.model
        if index.isValid():
            dialog = stuff_document_edit.EditStuffEvents( model, index, parent = self )
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

    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = ">>>>>>>>>>* StuffEventSubTab  *<<<<<<<<<<<<"

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