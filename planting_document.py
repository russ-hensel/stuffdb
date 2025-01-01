#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 09:56:07 2024

@author: russ
"""

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

import gui_qt_ext
import string_util
from app_global import AppGlobal
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

if __name__ == "__main__":
    # ----- run the full app
    import main
    main.main()
# --------------------
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
my reference list of qt imports in qt_imports.py


"""
# ---- begin pyqt from import_qt.py

#from   functools import partial
#import collections
import functools
import sqlite3
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
# ---- not in standard imports
# ----QtWidgets Boxes, Dialogs
# ----QtWidgets layouts
# ----QtWidgets big
# ----QtWidgets
from PyQt5.QtWidgets import (QAbstractItemView,
                             QAction,
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

#import  document_maker
import base_document_tabs
import custom_widgets
import key_words
import mdi_management
import planting_document_edit
import qt_sql_query
import qt_with_logging

# import winsound windows only


# ---- imports local


#import  picture_viewer
#import  tracked_qsql_relational_table_model  # dump for qt with logging

# import  debug_util

# ---- end parms


# ----------------------------------------
class PlantingDocument( base_document_tabs.DocumentBase ):
    """
    for the planting table....
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

        self.detail_table_name  = "planting"
        self.text_table_name    = "planting_text"  # text tables always id and text_data

        self.prior_tab          = 0
        self.current_tab        = 0

        self.prior_criteria     = None
        self.current_criteria   = None    # init just after criteria tab created

        self.subwindow_name     = "PlantingSubWindow"

        self.setWindowTitle( self.subwindow_name )
        self._build_gui()

    # --------------------------------
    @property
    def topic( self ):
        """
        of the detail record
        """
        topic     = "planting topic "
        if self.record_state:
            topic    = f"{topic} {self.record_state = }"
        topic    = f"{topic} {self.detail_tab.name_field.text()}"

        return   topic

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says
        """
        main_notebook           = self.tab_folder   # create in parent
        # main_notebook           = QTabWidget()
        self.main_notebook      = main_notebook   # phase out for tab_folder !!

        # main_notebook           = QTabWidget()
        # self.main_notebook      = main_notebook

        sub_window              = self
        mdi_area                = AppGlobal.main_window.mdi_area
        # main_notebook.currentChanged.connect( self.on_tab_changed )

        ix                        = -1

        ix                       += 1
        self.criteria_tab_index   = ix
        self.criteria_tab         = PlantingCriteriaTab( self )
        main_notebook.addTab(       self.criteria_tab, "Criteria" )

        ix                       += 1
        self.list_tab_index      = ix
        self.list_tab            = PlantingListTab( self  )
        main_notebook.addTab(  self.list_tab, "List"    )

        ix                       += 1
        self.detail_tab_index     = ix
        self.detail_tab           = PlantingDetailTab( self )
        main_notebook.addTab( self.detail_tab, "Detail"     )

        ix                       += 1
        self.picture_tab_index     = ix
        self.picture_tab           = base_document_tabs.StuffdbPictureTab( self )
        main_notebook.addTab( self.picture_tab, "Picture"     )

        ix                         += 1
        self.detail_text_index      = ix
        self.text_tab               = PlantingTextTab( self )
        main_notebook.addTab( self.text_tab, "Text"     )

        ix                        += 1
        self.history_tab_index     = ix
        self.history_tab           = PlantingHistorylTab( self )
        main_notebook.addTab( self.history_tab, "History"    )

        # next move to tabs -- list and history should have same interface
        # self.list_ix              = 0
        # self.history_ix           = 0

        sub_window.setWidget( main_notebook )
        mdi_area.addSubWindow( sub_window )

        sub_window.show()

    # ---------------------------------------
    def fetch_id_test( self, ):
        """
        just for testing will be deleted
        """
        id  = 55
        print( f"fetch_id_test{id=}")
        self.fetch_row_by_id(  id )
        # self.text_tab.fetch_text_row_by_id(  id )

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
        print( "planting sub window, i_am_hsw")

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
        print( f"Planting Clicked on list row {row}, column {
            column}, {db_key=}" )  # " value: {value}" )

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
        print( f"Clicked on_list_double_clicked on row {row}, column {column}, value tbd" )

    # --------------------------
    def on_tab_changed_promoted_in_part_maybe( self, event ):
        """
        not currently use, but may trigger a save or other action
        in the future
        """
        # old_prior               = self.prior_tab
        self.prior_tab          = self.current_tab  # because not updated yet
        self.current_tab        = self.main_notebook.currentIndex()
        current_text            = self.main_notebook.tabText(
            self.current_tab )
        # rint( f"on_tab_changed {self.prior_tab = } {self.current_tab = }   {current_text = }" )

        # # could be done at any time
        # self.tap_page_Planting_fn   = self.a_notebook.tab( self.a_notebook.select(), 'text' ) + ".txt"
        # rint( f"tap_page_Planting_fn  >>{self.tap_page_Planting_fn}<< "
        #        "for tabpage on_changed need to remove spaces" )
        # #rint( f"on_changed  {event} for tabpage" )
        # #rint( self.get_info() )

    # ---- sub window interactions ---------------------------------------


    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = ">>>>>>>>>>* plantingSubWindow  *<<<<<<<<<<<<"

        return a_str

# ----------------------------------------
class PlantingCriteriaTab( base_document_tabs.CriteriaTabBase, ):
    """
    criteria for list selection
    """
    def __init__(self, parent_window ):
        """
        the usual

        """
        super().__init__( parent_window )
        self.tab_name            = "PlantingCriteriaTab"

    # ------------------------------------------
    def _build_tab( self, ):
        """
        what it says, read
        put page into the notebook
        """
        # debug_util.get_traceback_list()
        page            = self
        tab             = page

        placer          = gui_qt_ext.PlaceInGrid(
            central_widget=page,
            a_max=0,
            by_rows=False  )

        self._build_top_widgets( placer )


        # # ---- Key Words
        # a_widget  = QLabel( "Key Words" )
        # placer.new_row()
        # placer.place( a_widget )

        # widget                  = custom_widgets.CQLineEditCriteria( get_type = "string", set_type = "string")
        # widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        # widget.critera_name     = "key_words"
        # placer.place( widget )
        # self.key_words_widget    = widget

        # ---- name like
        placer.new_row()
        widget  = QLabel( "Name (like)" )
        placer.place( widget )

        widget                  = custom_widgets.CQLineEditCriteria( get_type = "string", set_type = "string")
        self.name_widget        = widget
        widget.critera_name     = "name"
        self.critera_widget_list.append( widget )
        widget.textChanged.connect( lambda: self.criteria_changed(  True   ) )
        placer.place( widget )

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
        widget  = QLabel( "!!Order by" )
        placer.place( widget )

        widget                 = custom_widgets.CQComboBoxEditCriteria( get_type = "string", set_type = "string")
        self.order_by_widget   = widget
        self.critera_widget_list.append( widget )
        widget.critera_name    = "order_by"

        widget.addItem('name')
        widget.addItem('lbl_name')
        widget.addItem('Title??')

        print( "build_tab build criteria change put in as marker ")
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



        self.add_buttons( placer )

    # ---- Actions

    # -------------------------
    def clear_criteria_promoted( self, ):
        """
        what it says, read
        """
        self.key_words_widget.setText(  "" )
        # self.channel_pref_widget.setCurrentText(  "Ignore" )
        # self.channel_group_widget.setCurrentText( "Ignore" )

    # -------------
    def criteria_select( self,     ):
        """


        """
        #rint( "criteria_select  >>>>>>>>>>>>>>>>>>>>>> " )
        parent_document                 = self.parent_window

        model                           = parent_document.list_tab.list_model
        #rint( "begin channel_select for the list")
        query                           = QSqlQuery()
        query_builder                   = qt_sql_query.QueryBuilder( query, print_it = False, )

        kw_table_name                   = "platning_key_words"
        column_list                     = [ "id", "id_old", "name", "add_kw", "bed",       ]

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
            query_builder.sql_inner_join    = " planting_key_word  ON planting.id = planting_key_word.id "
            query_builder.sql_having        = f" count(*) = {key_word_count} "

            query_builder.add_to_where( f" key_word IN {criteria_key_words}" , [] )

        # ---- name like
        name                          = criteria_dict[ "name" ].strip().lower()
        if name:
            add_where       = "lower( name )  like :name"   # :is name of bind var below
            query_builder.add_to_where( add_where, [(  ":name",
                                                     f"%{name}%" ) ])

        # ---- order by
        order_by   = criteria_dict[ "order_by" ]

        if   order_by == "name":
            column_name = "name"
        elif order_by == "lbl_name":
            column_name = "lbl_name"
        else:   # !! might better handel this
            column_name = "name"

        query_builder.add_to_order_by(    column_name, "ASC",   )

        query_builder.prepare_and_bind()

        msg      = f"{query_builder = }"
        AppGlobal.logger.debug( msg )

        is_ok  = AppGlobal.qsql_db_access.query_exec_model( query,
                                                  model,
                                                  msg = "HelpSubWindow criteria_select" )

        msg      = (  f"criteria_select {query.executedQuery()} "  )
        AppGlobal.logger.info( msg )
        print( msg )
        parent_document.main_notebook.setCurrentIndex( parent_document.list_tab_index )
        self.critera_is_changed = False

# ----------------------------------------
class PlantingListTab( base_document_tabs.DetailTabBase  ):

    def __init__(self, parent_window ):

        super().__init__( parent_window )

        self.list_ix            = 5  # should track selected an item in detail

        self.tab_name           = "PlantingListTab"

        self._build_gui()
# list_self.list_tab.self.list_view.
    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says, read
            for columns see criteria select in criteria tabl
        ?? looks pretty promotable
        """
        page            = self
        tab             = page
        # a_notebook.addTab( page, 'Channels ' )
        placer          = gui_qt_ext.PlaceInGrid(
            central_widget=page,
            a_max=0,
            by_rows=False  )

        model               = QSqlTableModel(
            self, self.parent_window.db )  # perhaps a global

        self.list_model     = model

        model.setTable( self.parent_window.detail_table_name )

        model.setEditStrategy( QSqlTableModel.OnManualSubmit) # = never

        # COMMENT  out to default
        # model.setHeaderData( 0, Qt.Horizontal, "ID")
        # model.setHeaderData( 1, Qt.Horizontal, "TEXT DATA"  )

        # Set up the view
        view                 = QTableView()
        self.list_view       = view
        view.setModel( model )
        placer.place(  view )
        view.clicked.connect( self.parent_window.on_list_clicked )
        #self.select_all_for_test()

        view.setSelectionBehavior(QAbstractItemView.SelectRows)
        # Optionally, set selection mode to single selection or extended selection
        view.setSelectionMode(QAbstractItemView.SingleSelection)

# ----------------------------------------
class PlantingDetailTab( base_document_tabs.DetailTabBase  ):
    """
    """
    def __init__(self, parent_window  ):
        """
        Args:
            parent_window (TYPE): DESCRIPTION.

        """
        super().__init__( parent_window )

        self._build_gui()

        self.tab_name           = "PlantingDetailTab"

        self.table_name         = parent_window.detail_table_name
        model                   = QSqlTableModel(
                                   self, AppGlobal.qsql_db_access.db )
        self.tab_model          = model
        self.table              = parent_window.detail_table_name

        model.setTable( self.table )
        self.enable_send_topic_update    = True

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
        tab_folder   = QTabWidget()

        tab_folder.setMovable( True )
        tab_layout.new_row()
        tab_layout.addWidget( tab_folder, columnspan   = max_col )

        sub_tab      = PlantingEventSubTab( self )
        self.event_sub_tab   = sub_tab
        tab_folder.addTab( sub_tab, "Events" )

        sub_tab      = PlantingPictureSubTab( self )

        #self.pictures_tab       = sub_tab
        self.picture_sub_tab    = sub_tab
        self.sub_tab_list.append( sub_tab )
        tab_folder.addTab( sub_tab, "Pictures" )

        self.prior_tab          = 0
        self.current_tab        = 0

        # Main notebook
        detail_notebook           = QTabWidget()
        self.detail_notebook      = detail_notebook

        # ---- buttons
        button_layout = QHBoxLayout()

        # create_button = QPushButton("Create Default")
        # create_button.clicked.connect( self.create_default_row )
        # button_layout.addWidget(create_button)

        # button = QPushButton( "To History" )
        # rint( "need detail_to_history")
        # button.clicked.connect( self.parent_window.detail_to_history )
        # button_layout.addWidget(update_button)

        #tab_layout.addLayout( button_layout )

    # -------------------------------------
    def _build_gui_old( self ):
        """
        what it says read
        Returns:
            none
        """
        tab             = self
        tab_layout      = QVBoxLayout(tab)



        self.id_field   = QLineEdit()
        self.id_field.setValidator( QIntValidator() )
        self.id_field.setPlaceholderText( "Enter ID" )
        tab_layout.addWidget(self.id_field)

        field = QLineEdit()
        self.name_field      = field
        field.setPlaceholderText( "Name" )
        tab_layout.addWidget( field )

        self.add_kw_field = QLineEdit()
        self.add_kw_field.setPlaceholderText( "add_kw" )
        tab_layout.addWidget(self.add_kw_field)

        # self.add_kw_field = QLineEdit()
        # self.add_kw_field.setPlaceholderText("add_kw")
        # tab_layout.addWidget(self.add_kw_field)

        self.edit_ts_field = QLineEdit()
        self.edit_ts_field.setPlaceholderText("edit_ts")
        tab_layout.addWidget( self.edit_ts_field)

        # ---- new template code
        edit_field              = QLineEdit()
        self.add_ts_field       = edit_field
        edit_field.setPlaceholderText("add_ts")
        tab_layout.addWidget( edit_field )

        # ---- tab area
        # ---------------
        tab_folder   = QTabWidget()
        # tab_folder.setTabPosition(QTabWidget.West)
        tab_folder.setMovable(True)
        tab_layout.addWidget( tab_folder )

        sub_tab      = PlantingEventSubTab( self )
        self.event_sub_tab   = sub_tab
        tab_folder.addTab( sub_tab, "Events" )

        sub_tab      = PictureListSubTab( self )
        self.pictures_tab   = sub_tab
        tab_folder.addTab( sub_tab, "Pictures" )

        self.prior_tab          = 0
        self.current_tab        = 0

        # self.prior_criteria     = None
        # self.current_criteria   = None    # init just after criteria tab created

        # Main notebook
        detail_notebook           = QTabWidget()
        self.detail_notebook      = detail_notebook

        # ---- buttons
        button_layout = QHBoxLayout()

        # create_button = QPushButton("Create Default")
        # create_button.clicked.connect( self.create_default_row )
        # button_layout.addWidget(create_button)


        # button = QPushButton( "To History" )
        # rint( "need detail_to_history")
        # button.clicked.connect( self.parent_window.detail_to_history )
        # button_layout.addWidget(update_button)

        tab_layout.addLayout( button_layout )

    #---------------------------------
    def _build_fields( self, layout ):
        """
        What it says, read
            this is generated code
        """
        # ---- code_gen: detail_tab_build_gui use for _build_gui  -- begin table entries

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

        # ---- name
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "name",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.name_field         = edit_field
        edit_field.setPlaceholderText( "name" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- plant_id
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "plant_id",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.plant_id_field         = edit_field
        edit_field.setPlaceholderText( "plant_id" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- bed_old
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "bed_old",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.bed_old_field         = edit_field
        edit_field.setPlaceholderText( "bed_old" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- location
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "location",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.location_field         = edit_field
        edit_field.setPlaceholderText( "location" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- add_kw
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "add_kw",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.add_kw_field         = edit_field
        edit_field.setPlaceholderText( "add_kw" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- descr
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "descr",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.descr_field         = edit_field
        edit_field.setPlaceholderText( "descr" )
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

        # ---- cmnt
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "cmnt",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.cmnt_field         = edit_field
        edit_field.setPlaceholderText( "cmnt" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- lbl
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "lbl",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.lbl_field         = edit_field
        edit_field.setPlaceholderText( "lbl" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- bed
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "bed",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.bed_field         = edit_field
        edit_field.setPlaceholderText( "bed" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- lbl_name
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "lbl_name",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.lbl_name_field         = edit_field
        edit_field.setPlaceholderText( "lbl_name" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

                                                # timestamp to qdates make these non editable

        # ---- itag1
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "itag1",
                                                db_type        = "integer",
                                                display_type   = "string" )
        self.itag1_field         = edit_field
        #edit_field.setPlaceholderText( "itag1" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- planting_status
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "planting_status",
                                                db_type        = "string",
                                                display_type   = "string" )
        self.planting_status_field         = edit_field
        edit_field.setPlaceholderText( "planting_status" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

                                                # timestamp to qdates make these non editable

        # ---- need_stake
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "need_stake",
                                                db_type        = "integer",
                                                display_type   = "string" )
        self.need_stake_field         = edit_field
        #edit_field.setPlaceholderText( "need_stake" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

                                                # timestamp to qdates make these non editable

        # ---- need_label
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "need_label",
                                                db_type        = "integer",
                                                display_type   = "string" )
        self.need_label_field         = edit_field
        #edit_field.setPlaceholderText( "need_label" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

                                                # timestamp to qdates make these non editable

        # ---- need_work
        edit_field                  = custom_widgets.CQLineEdit(
                                                parent         = None,
                                                field_name     = "need_work",
                                                db_type        = "integer",
                                                display_type   = "string" )
        self.need_work_field         = edit_field
        #edit_field.setPlaceholderText( "need_work" )
        self.field_list.append( edit_field )
        layout.addWidget( edit_field )

        # ---- code_gen: detail_tab_build_gui use for _build_gui  -- end table entries


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
        print( f"PlantingDocumentDetaiTab fetch_row { id=}")
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
        # rint(  ia_qt.q_line_edit( self.name_field,
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

    # ------------------------
    def field_to_record( self, record ):
        """
        for Planting now from photo
        for the updates, get the gui data into the record
        assume for new add time and id are already there?? or in a self.xxx
        since not sure how works put in instance
        we still need more fields her and probably in record to field
        """
        if self.record_state    == base_document_tabs.RECORD_NEW:  # may be needed
            record.setValue("id", int( self.current_id ) )

        # record.setValue( "name",       self.name_field.text())
        #record.setValue( "add_kw", self.add_kw_field.text())
        record.setValue( "name", self.name_field.text())
        # record.setValue( "photo_fn",      self.photo_fn_field.text())
        # ---- timestamps
        # record.setValue( "add_ts",   self.add_ts_field.text()) # should have already been set
        #record.setValue( "edit_ts", self.edit_ts_field.text())

        self.parent_window.record_to_history_table( record )


    # ------------------------
    def clear_fields(self):
        """
        what it says, read
        what fields, need a bunch of rename here
        clear_fields  clear_fields  -- or is this default
        !! but should users be able to?? may need on add -- this may be defaults
        """
        self.id_field.clear()
        # self.descr_field.clear()
        # self.name_field.clear()

        self.name_field.clear()
        #self.add_kw_field.clear()
        # self.url_field.clear()
        # self.mypref_field.clear()


    # ------------------------
    def get_picture_file_name(self):
        """
        some promotable -- but picture is special only one file, rest
        work differently
        see picture document

        return file_name or None if no file name
        """
        print( "get_picture_file_name to be implemented" )
        return ""  # none will cause exception  , just need file name that does not exist

# ==================================
class PlantingTextTab( base_document_tabs.TextTabBase  ):
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
        self.tab_name            = "PlantingTextTab"

# ----------------------------------------
class PlantingHistorylTab( base_document_tabs.StuffdbHistoryTab   ):
    """ """
    def __init__(self, parent_window ):
        """
        """
        super().__init__( parent_window )

        # self.parent_window   = parent_window
        self.tab_name            = "PlantingHistorylTab"

    # -------------------------------------
    def _build_gui( self ):
        """
        what it says read
        seem same for all -- how to columns get named?
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

        table.setSelectionBehavior( QTableWidget.SelectRows )  # Select entire rows

        base_document_tabs.table_widget_no_edit( table )

        # table.clicked.connect( self.parent_window.on_history_clicked )
        # table.clicked.connect( self.on_list_clicked )
        table.cellClicked.connect( self.on_cell_clicked )

        layout2     = QVBoxLayout()
        layout2.addWidget( table )
        tab.setLayout( layout2 )

    # -------------------------------------
    def record_to_table_bak( self, record ):
        """
        what it says read
        from photo plus code gen

        """
        #print( f"record_to_table found row {ix_row} this probably should be promoted !! and different ")
        table           = self.history_table

        a_id            = record.value( "id" )
        str_id          = str( a_id )

        ix_row          = self.find_id_in_table( a_id )
        if ix_row:
            print( f"Planting_history_tab, probable promotes?record_to_table found row {ix_row} in future update maybe")

        # ---- insert
        self.ix_seq     += 1
        row_position    = table.rowCount()
        table.insertRow( row_position )
        ix_col          = -1
        ix_row          = row_position   # or off by 1


        ix_col          += 1
        item             = QTableWidgetItem( str( self.ix_seq  ) )
        table.setItem( ix_row, ix_col, item   )


    # -------------------------------------
    def record_to_table( self, record ):
        """
        what it says read
        from photo plus code gen -- which gen

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
        # ---- code_gen: history_tab_build_gui tab -- build_gui -- begin table entries


        ix_col          += 1
        item             = QTableWidgetItem( str( record.value( "id" ) ) )
        table.setItem( ix_row, ix_col, item   )


        ix_col          += 1
        item             = QTableWidgetItem( str( record.value( "id_old" ) ) )
        table.setItem( ix_row, ix_col, item   )


        ix_col          += 1
        item             = QTableWidgetItem( str( record.value( "name" ) ) )
        table.setItem( ix_row, ix_col, item   )


        ix_col          += 1
        item             = QTableWidgetItem( str( record.value( "plant_id" ) ) )
        table.setItem( ix_row, ix_col, item   )


        ix_col          += 1
        item             = QTableWidgetItem( str( record.value( "bed_old" ) ) )
        table.setItem( ix_row, ix_col, item   )



        # end code gen


# ----------------------------------------
class PlantingEventSubTab( base_document_tabs.SubTabBase  ):
    """
    """
    def __init__(self, parent_window ):
        """
        """
        super().__init__( parent_window )

        self.list_ix         = 5  # should track selected an item in detail
        # needs work
        self.db              = AppGlobal.qsql_db_access.db

        self.table_name      = "planting_event"
        self.list_table_name = self.table_name   # delete this
        #self.tab_name            = "PlantingEventSubTab  not needed this is a sub tab
        self.current_id      = None
        #self.current_id      = 28
        #rint( "fix planting event select and delete line above should be select_by_id  ")
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
        model              = qt_with_logging.QSqlTableModelWithLogging(  self, self.db    )

        self.model_write   = model
        self.model         = model

        model.setTable( self.list_table_name )
        model.setEditStrategy( QSqlTableModel.OnManualSubmit )
        # model_write.setEditStrategy( QSqlTableModel.OnFieldChange )
        model.setFilter( "planting_id = 28 " )
        print( "!!fix planting_id = 28 ")

    # ------------------------------------------
    def select_all_for_testxxxxxx( self, ):
        """
        what it says, read

        """
        query_ok   = self.model_write.select()

        msg        = f"{ query_ok = }"
        # rint( msg )
        AppGlobal.logger.debug( msg )

        # AppGlobal.yt_db.error_info( self.channel_model.lastError() )
        # AppGlobal.planting_db_db.error_info( model.lastError() )
        ia_qt.q_sql_error( self.model_write.lastError(),
                           msg="now in code at:select_all_for_test")

        if not query_ok:
            msg     = f"select_all_for_test not query_ok {
                1} "  # "{AppGlobal.stuff_db_db}"
            AppGlobal.logger.error( msg )
            print(  msg )

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
        model.setFilter( f"planting_id = {id}" )
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
        dialog     = planting_document_edit.EditPlantingEvents( model, index = None, parent = self )
        if dialog.exec_() == QDialog.Accepted:
            #self.model.submitAll()
            ok     = base_document_tabs.model_submit_all(
                       model,  f"PlantingEventsSubTab.add_record " )
            self.model.select()

    # ------------------------------------------
    def edit_record(self):
        """
        what it says, read?
        """
        index       = self.view.currentIndex()
        model       = self.model
        if index.isValid():
            dialog = planting_document_edit.EditPlantingEvents( self.model, index, parent = self )
            if dialog.exec_() == QDialog.Accepted:
                #self.model.submitAll()
                ok     = base_document_tabs.model_submit_all(
                           model,  f"PlantingEventsSubTab.add_record " )
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
        a_str   = ">>>>>>>>>>* PlantingEventSubTab  *<<<<<<<<<<<<"

        return a_str

# ------------------------------------
class PlantingPictureSubTab( base_document_tabs.PictureListSubTabBase ):
    """
    almost all promoted even this may not be necessary
    """
    def __init__(self, parent_window ):
        super().__init__( parent_window )
        self.pictures_for_table  = "planting"
        # perhaps call first ??


# ---- eof ------------------------------
