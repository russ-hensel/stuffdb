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
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
my reference list of qt imports in qt_imports.py


"""
# ---- begin pyqt from import_qt.py

from PyQt5.QtGui import (
    QStandardItemModel,
    QStandardItem,
                        )
# ---- QtCore
from PyQt5.QtCore  import  (
    QDate,
    QModelIndex,
    QTimer,
    Qt,
    pyqtSlot,
                            )

from PyQt5.QtGui import (
    QIntValidator,
    )

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction, QTableWidget, QTableWidgetItem, QMessageBox
# ----QtWidgets
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QAction,

    QDateEdit,
    QMenu,
    QAction,
    QLineEdit,
    QActionGroup,
    QApplication,
    QDockWidget,
    QTabWidget,
    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QSpinBox,
    QMdiSubWindow,
    QTextEdit,
    QButtonGroup,

    )

# ----QtWidgets big
from PyQt5.QtWidgets import (
    QAction,
    QMenu,
    QApplication,
    QMainWindow,

    QTableView,
    QFrame,
    QMainWindow,
    QMdiArea,
    QMdiSubWindow,
    QMdiArea,
    QMdiSubWindow,
    )

# ----QtWidgets layouts
from PyQt5.QtWidgets import (
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    )

# ----QtWidgets Boxes, Dialogs
from PyQt5.QtWidgets import (
    QAction,
    QActionGroup,
    QDockWidget,
    QFileDialog,
    QInputDialog,

    QLabel,
    QListWidget,
    QMenu,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QCheckBox,
    QComboBox,
    )

# ---- QtSql
from PyQt5.QtSql import (
    QSqlDatabase,
    QSqlTableModel,
    QSqlQuery,
    QSqlQueryModel
    )

# ---- not in standard imports
from PyQt5.QtWidgets import ( QApplication, QMainWindow,
 QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
 QVBoxLayout, QWidget, QPushButton, QDockWidget
 )
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QRectF


import sqlite3


#from   functools import partial
import collections
import functools
import time

# import winsound windows only


# ---- imports local

import  sql_query_model_plus
from    app_global import AppGlobal

import  gui_qt_ext
import  string_util
import  qt_sql_query
import  document_maker
import  stuffdb_tabbed_sub_window
import  ia_qt
import  photo_viewer

# ----------------------------------------
class PhotoshowSubWindow( stuffdb_tabbed_sub_window.StuffdbTabbedSubWindow ):
    """
    for the photo table....
    """
    def __init__(self,  ):
        """
        the usual


        """
        super().__init__()

        mdi_area                = AppGlobal.main_window.mdi_area
            #we could return the subwindow for parent to add
        sub_window              = self
            # sub_window.setWindowTitle( "this title may be replaced " )
        self.db                 = AppGlobal.qsql_db_access.db

        self.detail_table_name  = "photoshow"
        self.text_table_name    = "photoshow_text"  # text tables always id and text_data

        self.prior_tab          = 0
        self.current_tab        = 0

        self.prior_criteria     = None
        self.current_criteria   = None    # init just after criteria tab created

        # Main notebook with  tabs
        main_notebook           = QTabWidget()
        self.main_notebook      = main_notebook

        main_notebook.currentChanged.connect( self.on_tab_changed )

        # for testing, generalization and ability not to create
        self.criteria_tab       = None
        self.list_tab           = None
        self.detail_tab         = None
        self.text_tab           = None
        self.history_tab        = None

        self.criteria_tab_index = None

        # ---- tab building
        ix                        = -1

        ix                       += 1
        self.criteria_tab_index   = ix
        self.criteria_tab         = self._build_tab_criteria( self )
        main_notebook.addTab(       self.criteria_tab,  "Criteria" )

        ix                             += 1
        self.list_tab_index             = ix
        self.list_tab                   = self._build_tab_list(  self  )
        main_notebook.addTab(             self.list_tab  ,   "List"    )


        # ix                         += 1
        # self.detail_text_index      = ix
        # self.text_tab               = self._build_tab_text( self )
        # main_notebook.addTab( self.text_tab,    "Text"     )

        ix                         += 1
        self.photo_index           = ix
        #rint( f"__init__  {self = }")
        self.photo_tab             = self._build_tab_photo( self )
        #rint( f">>>>> SubWindow _build_tab_photo __init__  {self.photo_tab = }")
        main_notebook.addTab( self.photo_tab,    "Photo"     )


        ix                       += 1
        self.detail_tab_index     = ix
        self.detail_tab           = self._build_tab_detail( self )
        main_notebook.addTab( self.detail_tab,    "Detail"     )


        ix                        += 1
        self.history_tab_index     = ix
        self.history_tab           = self._build_tab_history( self )
        main_notebook.addTab( self.history_tab ,   "History"    )

        sub_window.setWidget( main_notebook )
        mdi_area.addSubWindow( sub_window )

        sub_window.show()

    # ------------------------------------------
    def _build_tab_list( self, parent_window   ):
        """
        what it says, read
        """
        return PhotoshowListTab( parent_window )

    # ------------------------------------------
    def _build_tab_criteria( self,   parent_window ):
        """
        what it says, read
        put page into the notebook
        """
        return PhotoshowCriteriaTab( parent_window  )

    #-------------------------------------
    def _build_tab_detail( self, parent_window ):
        """
        '_build_tab_detail'
        """
        return PhotoshowDetailTab(  parent_window )

    #-------------------------------------
    def _build_tab_photo( self, parent_window ):
        """
        'build_tab_detail'
        """
        print( f"_build_tab_photo  {parent_window = }")
        return PhotoshowPhotoTab( parent_window )

    # #-------------------------------------
    # def _build_tab_text( self, parent_window ):
    #     """
    #     '_build_tab_detail'
    #     """
    #     return PhotoshowTextTab(  parent_window )

    #-----------------------------
    def _build_tab_history( self, parent_window ):
        """
        what it says, read
        """
        return PhotoshowHistorylTab( parent_window )

    # ---- capture events ----------------------------
    # ------------------------------------------
    def on_history_clicked( self, index: QModelIndex ):
        """
        !! finish me
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
        self.detail_tab.id_field.setText( str( db_key )  )

    # ------------------------------------------
    def on_list_clicked( self, index: QModelIndex ):
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
        #rint( f"photo Clicked on list row {row}, column {column}, {db_key = }" )

        #self.detail_tab.fetch_detail_row_by_id( db_key )
        self.fetch_row_by_id( db_key )

        self.main_notebook.setCurrentIndex( self.detail_tab_index )
        #self.detail_tab.id_field.setText( str( db_key )  ) # fetch currently does not include the id

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
    def on_tab_changed( self, event ):
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
        # self.tap_page_photo_fn   = self.a_notebook.tab( self.a_notebook.select(), 'text' ) + ".txt"
        # print( f"tap_page_photo_fn  >>{self.tap_page_photo_fn}<< "
        #        "for tabpage on_changed need to remove spaces" )
        # #rint( f"on_changed  {event} for tabpage" )
        # #rint( self.get_info() )

    # ---- sub window interactions ---------------------------------------

    #-------------------------------------
    def add_photo_to_show( self ):
        """
         use app global until i have something better
         for awhile same function down down there
        """
        1/0



    #-------------------------------------
    def default_new_row( self ):
        """
        defaults values for a new row in the detail and the
        text tabs

        Changes state of detail and related tabs

        """
        next_key      = AppGlobal.key_gen.get_next_key( self.detail_table_name )
        self.detail_tab.default_new_row( next_key )
        self.text_tab.default_new_row(   next_key )

    # ------------------------------------------
    def save( self,   ):
        """
        phase up
        also know as update -- update detail tab and related
        """
        # self.detail_tab.update_detail_row()
        # self.text_tab.update_text_row()

        #rint( "save.... need to complete")
        print( "change save to update db " )
        self.update_db()


    def update_db( self, ):
        """


        Args:
             (TYPE): DESCRIPTION.null

        Returns:
            None.

        """
        # was
        self.detail_tab.update_detail_row()
        self.text_tab.update_text()

        # # was
        # self.detail_tab.update_detail_row()
        # self.text_tab.update_text_row()


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

    # ------------------------------------------
    def criteria_select( self,     ):
        """
        uses info in criteria tab to build list in list tab
        uses info from 2 tabs
        """
        print( "criteria_select in photo sub window next pull over channel_select " )

        #rint( "begin channel_select for the list")
        query                       = QSqlQuery()
        query_builder               = qt_sql_query.QueryBuilder( query )

        # ---- add criteria
        criteria_dict               = self.criteria_tab.get_criteria()
        model                       = self.list_tab.list_model

        query_builder.table_name    = self.detail_table_name
        query_builder.column_list   = [
            "id",
            "name",
            "cmnt",

              ]

        key_words           = criteria_dict[ "key_words" ].strip().lower()
        if key_words:
            add_where       = "lower( photo.name )  like :key_words"   # :is name of bind var below
            #where_dict      = {"channel_name_like":  f"%{channel_name_like}%"}
            #query_builder.add_to_where( add_where, where_dict )
            query_builder.add_to_where( add_where, [(  ":key_words",
                                                     f"%{key_words}%" ) ])

        query_builder.prepare_and_bind()

        msg      = f"{query_builder = }"
        AppGlobal.logger.debug( msg )

        msg      = f"Executing SQL query:  {query.executedQuery() = }"
        AppGlobal.logger.debug( msg )

        if query.exec():
            model.setQuery( query )
            if model.lastError().isValid():
                msg     = f"Query Error: {model.lastError().text() = }"
                print(  msg )
                AppGlobal.logger.error( msg )
        else:
            print( "Query Execution Error:", query.lastError().text())
            print(  msg )
            AppGlobal.logger.error( msg )

        self.main_notebook.setCurrentIndex( self.list_tab_index )

    # -----------------------------------
    def detail_to_history_premote( self, ):
        """
        what it says, read
        links two sub_windows

        """
        index    = self.detail_tab.detail_model.index( 0, 0 )
        self.add_row_history( index )

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
        # Get the data from the selected row
        detail_model    = self.detail_tab.tab_model
        history_model   = self.history_tab.history_model

        id_data         = detail_model.data( detail_model.index( index.row(), 0))
        name_data       = detail_model.data( detail_model.index( index.row(), 2))
        #rint( f"in add_row_history {id_data = }   {name_data = }")
        # Create items for the second model
        id_item     = QStandardItem( str(id_data) )
        name_item   = QStandardItem( name_data )

        # Add a new row to the second model
        history_model.appendRow([id_item, name_item])

    # ---------------------------------------
    def fetch_row_by_id( self, id ):
        """
        what it says, mostly focused on the detail tab
        """
        self.detail_tab.fetch_detail_row_by_id(  id )
        if self.text_tab is not None:
            self.text_tab.fetch_text_row_by_id(  id )
        self.detail_to_history()

    # ---------------------------------------
    def display_photo( self, file_name  ):
        """
        what it says, mostly focused on the detail tab
        should not be in photoshow
        """
        print( f"<<<<<< display_photo  {self.photo_tab = }")
        self.photo_tab.display_file( file_name )


    # ---------------------------------------
    def fetch_id_test( self,  ):
        """
        just for testing will be deleted
        """
        id  = 55
        print( f"fetch_id_test{id = }")
        self.fetch_row_by_id(  id )
        #self.text_tab.fetch_text_row_by_id(  id )

    #-------------------------------------
    def i_am_hsw(self):
        """
        make sure call is to here for testing
        """
        print( "photoshow sub window, i_am_hsw")

    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = ">>>>>>>>>>* photoSubWindow  *<<<<<<<<<<<<"

        return a_str

# ----------------------------------------
class PhotoshowCriteriaTab( stuffdb_tabbed_sub_window.StuffdbTab, ):
    """
    criteria for list selection
    """
    def __init__(self, parent_window ):
        """
        the usual

        """
        super().__init__()
        self.parent_window   = parent_window
        self._build_tab()

    # ------------------------------------------
    def _build_tab( self,   ):
        """
        what it says, read
        put page into the notebook
        !! put widgets in dict for several methods
        dict - named tuple
        name
            widget
            get_method  ???
            set method

            fields ??


        """
        page            = self
        tab             = page

        placer          = gui_qt_ext.PlaceInGrid(
        central_widget  = page,
        a_max           = 0,
        by_rows         = False  )

        # # ----
        # a_widget  = QLabel( "" )
        # placer.new_row()
        # placer.place( a_widget )

        # a_widget    = QLineEdit()
        # placer.place( a_widget )
        # self.key_words_widget    = a_widget

        # ---- Channel Like
        a_widget  = QLabel( "Name (like)" )
        placer.new_row()
        placer.place( a_widget )

        a_widget    = QLineEdit()
        placer.place( a_widget )
        self.name_widget    = a_widget

        # # ---- MyPref
        # a_widget  = QLabel( "Ch MyPref" )
        # placer.place( a_widget )

        # a_widget    = QComboBox()
        # values      = [ "Ignore", "Item 1", "Item 2", "Item 3"]
        # a_widget.addItems( values )
        # placer.place( a_widget )
        # self.channel_pref_widget    = a_widget

        # # self.channel_pref_widget.setCurrentText("Ignore")
        # # text = self.channel_pref_widget.currentText()

        # # ----Ch MyGroup
        # a_widget  = QLabel( "Ch MyGroup" )
        # #placer.new_row()
        # placer.place( a_widget )

        # a_widget    = QComboBox()
        # values      = ( "Ignore", 'Group1'  )
        # a_widget.addItems( values )
        # #a_widget.setCurrentText("Ignore")
        # placer.place( a_widget )
        # self.channel_group_widget  = a_widget

        # # ----"Order By:"
        # a_widget    = QLabel( "Order By:" )
        # placer.new_row()
        # placer.place( a_widget )

        # a_widget    = QComboBox()
        # values      = ( "Ignore", "title", 'pub_date', 'watched',
        #                       'view_count',  )
        # a_widget.addItems( values )
        # placer.place( a_widget )
        # self.channel_order_by_widget  = a_widget

        # ---- buttons -- put in ancestor??
        a_widget        = QPushButton( "Clear Criteria" )
        a_widget.clicked.connect(  self.clear_criteria )
        placer.new_row()
        placer.place( a_widget )

        a_widget        = QPushButton( "Run Select" )
        print( "fix 235")
        a_widget.clicked.connect(  self.parent_window.criteria_select )
        #placer.new_row()
        placer.place( a_widget )

    # ---- Actions
    def get_criteria( self ):
        """
        What it says, read

            note: strip the strings -- can we set up when build gui in a dict?
        """
        criteria_dict                        = {}

        # text() for line edit
        #criteria_dict[ "key_words" ]         = self.key_words_widget.text().strip()
        # criteria_dict[ "channel_group" ]        = self.channel_group_widget.currentText().strip()
        # criteria_dict[ "channel_name_like" ]    = self.channel_like_widget.text().strip()
        criteria_dict[ "name_like" ]              = self.name_widget.text().strip()


        msg      = f"photo {criteria_dict = }"
        print(  msg )
        AppGlobal.logger.debug( msg )

        return criteria_dict

    # -------------------------
    def clear_criteria( self,   ):
        """
        what it says, read

        """
        #self.key_words_widget.setText( "" )
        self.name_widget.setText( "" )
        # self.channel_pref_widget.setCurrentText(  "Ignore" )
        # self.channel_group_widget.setCurrentText( "Ignore" )

# ----------------------------------------
class PhotoshowListTab( stuffdb_tabbed_sub_window.StuffdbTab  ):

    def __init__(self, parent_window ):

        pass
        super().__init__()
        self.parent_window   = parent_window
        self.list_ix         = 5  # should track selected an item in detail
            # needs work
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
        # model.setHeaderData( 1, Qt.Horizontal, "TEXT DATA"  )
        # model.setHeaderData( 2, Qt.Horizontal, "Name"   )
        # model.setHeaderData( 3, Qt.Horizontal, "Url")
        # model.setHeaderData( 4, Qt.Horizontal, "mypref")
        # model.setHeaderData( 5, Qt.Horizontal, "mygroup")

        # Set up the view
        view                 = QTableView()
        self.list_view       = view
        view.setModel( model )
        placer.place(  view )

        self.select_all_for_test()

    # ------------------------------------------
    def select_all_for_test( self,  ):
        """
        what it says, read

        """
        model      = self.list_model

        query_ok   = model.select()

        msg        = f"{ query_ok = }"
        #rint( msg )
        AppGlobal.logger.debug( msg )

        #AppGlobal.yt_db.error_info( self.channel_model.lastError() )
        # AppGlobal.photo_db_db.error_info( model.lastError() )
        ia_qt.q_sql_error( model.lastError(),
                       msg   =  "now in code at:select_all_for_test")

        if not query_ok:
            msg     = f"select_all_for_test not query_ok {1} "  #"{AppGlobal.photo_db_db}"
            AppGlobal.logger.error( msg )
            print(  msg )

            print( " next 1/0    ", flush = True)
            1/0

        self.list_view.resizeColumnsToContents()

        #print( "need on list clicked")
        self.list_view.clicked.connect( self.parent_window.on_list_clicked )
        #view.doubleClicked.connect( self.on_list_double_clicked )

# ----------------------------------------
class PhotoshowDetailTab( stuffdb_tabbed_sub_window.StuffdbTab  ):
    """
    """
    def __init__(self, parent_window  ):
        """

        Args:
            parent_window (TYPE): DESCRIPTION.

        """
        super().__init__()
        self.parent_window      = parent_window

        self._build_gui()
        self.this_subwindow     = "photoshowDetailTab"   # { self.this_subwindow = }

        model                   = QSqlTableModel( self, AppGlobal.qsql_db_access.db )
        self.tab_model       = model
        self.table              = parent_window.detail_table_name

        model.setTable( self.table )

        #print( f"!! maybe do not want this select { self.this_subwindow = } now gone ")
        #model.select( )

    #-------------------------------------
    def _build_gui( self ):
        """
        what it says read
        Returns:
            none
        """
        tab             = self
        tab_layout      = QVBoxLayout(tab)

        # ---- field defs
        self.id_field   = QLineEdit()
        self.id_field.setValidator( QIntValidator() )
        self.id_field.setPlaceholderText( "Enter ID" )
        tab_layout.addWidget(self.id_field)

        field_widget       = QLineEdit()
        self.name_field    = field_widget
        field_widget.setPlaceholderText( "name" )
        tab_layout.addWidget( field_widget )

        # self.add_kw_field = QLineEdit()
        # self.add_kw_field.setPlaceholderText( "add_kw" )
        # tab_layout.addWidget(self.add_kw_field)

        # edit_field              = QLineEdit()
        # self.photo_fn_field     = edit_field
        # edit_field.setPlaceholderText( "photo_fn" )
        # tab_layout.addWidget( edit_field )

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


        # # ---- new style field def
        # new_field           = QLineEdit( )
        # self.edit_ts_field  = new_field
        # new_field.setPlaceholderText( "edit_ts" )
        # tab_layout.addWidget( new_field )

        # ---- tab area
        # ---------------
        tab_folder   = QTabWidget()
        # tab_folder.setTabPosition(QTabWidget.West)
        tab_folder.setMovable(True)
        tab_layout.addWidget( tab_folder )

        sub_tab          = PhotoshowDetailListTab( self )
        self.photos_tab  = sub_tab
        tab_folder.addTab( sub_tab, "Photos" )

        sub_tab      = TestDetaiSubTab( self )
        tab_folder.addTab( sub_tab, "a test" )

        self.prior_tab          = 0
        self.current_tab        = 0

        # self.prior_criteria     = None
        # self.current_criteria   = None    # init just after criteria tab created

        # Main notebook with 3 tabs
        detail_notebook           = QTabWidget()
        self.detail_notebook      = detail_notebook

        #main_notebook.currentChanged.connect( self.on_tab_changed )

        # ix                        = -1

        # ix                       += 1
        # self.criteria_tab_index   = ix
        # self.criteria_tab         = self._build_tab_criteria( self )
        # detail_notebook.addTab(   self.criteria_tab,  "Criteria"  )

        # ---- buttons
        button_layout = QHBoxLayout()

        fetch_button = QPushButton("Fetch")
        fetch_button.clicked.connect(self.fetch_detail_row)
        button_layout.addWidget(fetch_button)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_detail_row)
        button_layout.addWidget(delete_button)

        # button = QPushButton( "Clear" )
        # button.clicked.connect(self.clear_detail_fields )
        # button_layout.addWidget( button )

        # _build_button = QPushButton("Create")
        # _build_button.clicked.connect(self._build_detail_row)
        # button_layout.addWidget(_build_button)

        # _build_button = QPushButton("Create Default")
        # _build_button.clicked.connect( self._build_default_row )
        # button_layout.addWidget(_build_button)

        update_button = QPushButton("Update")
        update_button.clicked.connect(self.update_detail_row )
        button_layout.addWidget(update_button)

        button = QPushButton( "To History" )
        print( "need detail_to_history")
        button.clicked.connect( self.parent_window.detail_to_history )
        button_layout.addWidget(update_button)

        tab_layout.addLayout( button_layout )

        # a second sub layout
        button_layout = QHBoxLayout()
        tab_layout.addLayout( button_layout )

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
    def fetch_detail_row_by_id( self,  id   ):
        """
        what it says, read
        or is is not a fetch, a copy over, not what I want
        !! need to fix -- updates may no         t work
        also need to check for more id errors, perhaps
        Args:
            id (TYPE): DESCRIPTION.

        """
        model     = self.tab_model
        model.setFilter( (f"id = {id}") )
        model.select()
        if model.rowCount() > 0:
            record = model.record(0)
            #self.id_field.setText(  record.value(    "id"      ))
            self.name_field.setText(   record.value(    "name"       ))
            # self.add_kw_field.setText(  record.value(    "add_kw"       ))
            #self.photo_fn_field.setText(  record.value(    "photo_fn"       ))
            #self.add_kw_field.setText(   "test_fix add kw"      )
            # self.mypref_field.setText(str(record.value(  "mypref")   ))
            # self.mygroup_field.setText(record.value(     "mygroup"   ))
            # self.add_ts_field.setText(record.value(      "add_ts"    ))
            self.edit_ts_field.setText(record.value(     "edit_ts"   ))
            self.add_ts_field.setText(record.value(       "add_ts"   ))
            # seems to work
            # a_ts   = str( time.time() )
            # #self.add_ts_field.clear()
            # self.edit_ts_field.setText(  a_ts   )
            print( "still need update for edit ts" )
            # does this work
            self.id_field.setText(  str( record.value(    "id"      ) ) )

            # msg     = f"{self.photo_fn_field.text( ) =}"
            # print( msg )

            #rint( f"error in next line for {self.parent = }")
            #self.parent_window.display_photo( "/mnt/WIN_D/PhotoDB/02/102-0253_img.jpg" )   #self.photo_fn_field.text( ) )

            print( "no display photo here" )
            self.photos_tab.select_by_id( id )
            #self.parent_window.display_photo( self.photo_fn_field.text( ) )


            #self.photo_tab.display_file( file_name )

        else:
            msg     = f"Fetch Error: No record found with the given ID. { self.this_subwindow = } { id = }"
            QMessageBox.warning(self, "Error",  msg )
            AppGlobal.logger.error( msg )

        # else:
        #     QMessageBox.warning(self, "Input Error", f"Please enter a valid ID. { id = }")

    # -----------------------------
    def delete_detail_row(self):
        """
        looks like could be promoted -- dbkey needs to stay id
              but need to delete detail_children as well
              but need to delete key words as well
        what it says read
         delete_detail_row delete_detail_row
        Returns:
            None.

        """
        model       = self.tab_model
        id          = self.id_field.text()
        if id:
            model.setFilter( f"id = {id}" )
            model.select()
            if model.rowCount() > 0:
                model.removeRow(0)
                model.submitAll()
                QMessageBox.information(self, "Delete Success", f"Record deleted successfully.{ self.this_subwindow = }")
                self.clear_detail_fields()
            else:
                msg   = f"Delete Error: No record found with the given ID.{ self.this_subwindow = } { id = } "
                QMessageBox.warning(self, "Error",  msg )
                AppGlobal.logger.error( msg )
        else:
            msg  = f"Please enter a valid ID. { self.this_subwindow = } { id = }"
            QMessageBox.warning(self, "Input Error",  msg )
            AppGlobal.logger.error( msg )

    # -----------------------------
    def _build_next_keyxxxxx(self):
        """
        what it says
            this is for a new row on the window -- no save

        Returns:
            None.

        """
        next_key    = AppGlobal.key_gen.get_next_key( self.parent_window.detail_table_name  )
        print( f"{ next_key = }")

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
        name       = self.name_field.text()
        #add_kw     = self.add_kw_field.text()
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

        #self.descr_field.setText( descr + "*" )
        self.name_field.setText( name + "*" )


        #self.url_field.setText( url )

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

        # model    = self.tab_model


        # yt_id    = self.yt_id_field.text()
        # name     = self.name_field.text()
        # #print(  ia_qt.q_line_edit( self.name_field,
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

    # -------------------------
    def update_detail_row( self ):
        """
        what it says, read
        row is the model   detail.model ??
        !! change to update_detail_row
        Returns:
            None.
        update_detail_row update_detail_row
        """
        model       = self.tab_model
        id          = self.id_field.text()
        if id:
            model.setFilter(f"id = {id}")
            model.select()
            if model.rowCount() > 0:
                record = model.record(0)

                # ---- special for this table
                record.setValue("name",       self.name_field.text())
                #record.setValue("add_kw",     self.add_kw_field.text())
                # record.setValue("url",      self.url_field.text())
                # record.setValue("mypref",   int(self.mypref_field.text()) if self.mypref_field.text() else None )
                # record.setValue("mygroup",  self.mygroup_field.text())

                # ---- timestamps
                record.setValue("add_ts",   self.add_ts_field.text())
                record.setValue("edit_ts",  self.edit_ts_field.text())

                if model.setRecord(0, record):
                    model.submitAll()
                    msg    = "Record updated successfully. { self.this_subwindow = }"
                    AppGlobal.logger.debug( msg )
                    QMessageBox.information(self, "Update Success", msg )
                else:
                    msg    =  f"Update Error Failed to update record. { self.this_subwindow = } {id = }"
                    AppGlobal.logger.error( msg )
                    QMessageBox.warning(self, "Error", msg )
            else:
                msg    = f"No record found with the given ID.{ self.this_subwindow = } {id = } "
                AppGlobal.logger.error( msg )
                QMessageBox.warning(self, "Update Error", msg )
        else:
            msg    = f"Input Error", "Please enter a valid ID. { self.this_subwindow = } {id = } "
            AppGlobal.logger.debug( msg )
            QMessageBox.warning(self, "Input Error", msg )

    # ------------------------
    def clear_detail_fields(self):
        """
        what it says, read
        what fields, need a bunch of rename here
        clear_detail_fields  clear_detail_fields  -- or is this default
        !! but should users be able to?? may need on add -- this may be defaults
        """
        self.id_field.clear()
        #self.descr_field.clear()
        self.name_field.clear()
        #self.add_kw_field.clear()
        # self.url_field.clear()
        # self.mypref_field.clear()
        # self.mygroup_field.clear()

        # a_ts   = str( time.time() )
        # #self.add_ts_field.clear()
        # self.edit_ts_field.setText(  a_ts   )
        # self.edit_ts_field.clear()


    # ------------------------
    def field_to_record( self, record ):
        """
        for the updates, get the gui data into the record
        assume for new add time and id are already there?? or in a self.xxx
        since not sure how works put in instance
        we still need more fields her and probably in record to field
        """


        if self.record_state    == self.RECORD_NEW:  # may be needed
            record.setValue("id", int( self.new_record_id ) )


        record.setValue( "name",       self.name_field.text())
        # record.setValue( "add_kw",     self.add_kw_field.text())
        # record.setValue( "descr",      self.descr_field.text())
        # record.setValue( "photo_fn",      self.photo_fn_field.text())
        # ---- timestamps
        #record.setValue( "add_ts",   self.add_ts_field.text()) # should have already been set
        # record.setValue( "edit_ts",  self.edit_ts_field.text())

    # ------------------------
    def record_to_field(self, record ):
        """
        """
        #self.descr_field.setText(     record.value(    "descr"       ))
        self.name_field.setText(     record.value(    "name"       ))
        self.add_kw_field.setText(    record.value(    "add_kw"       ))
        self.photo_fn_field.setText(  record.value(    "photo_fn"       ))


        # # self.add_ts_field.setText(record.value(      "add_ts"    ))
        # self.edit_ts_field.setText(record.value(     "edit_ts"   ))
        # self.add_ts_field.setText(record.value(       "add_ts"   ))
        # # seems to work
        # # a_ts   = str( time.time() )
        # # #self.add_ts_field.clear()
        # # self.edit_ts_field.setText(  a_ts   )
        # print( "still need update for edit ts" )
        # self.parent_window.display_photo( self.photo_fn_field.text( ) )



# ----------------------------------------
class TestDetaiSubTab( stuffdb_tabbed_sub_window.StuffdbTab,    ):

    def __init__(self, parent_window ):
        """
        the usual

        """
        super().__init__()
        self.parent_window   = parent_window
        self._build_gui()

    # ------------------------------------------
    def _build_gui( self,   ):
        """
        what it says, read
        put page into the notebook

        """
        page            = self
        tab             = page

        placer          = gui_qt_ext.PlaceInGrid(
        central_widget = page,
        a_max = 0,
        by_rows = False  )

        # a_widget        = QPushButton( "Get Criteria test" )
        # a_widget.clicked.connect(  self.get_criteria )
        # placer.place( a_widget )

        # ---- Channel Like
        a_widget  = QLabel( "xxx:" )
        placer.new_row()
        placer.place( a_widget )

        a_widget    = QLineEdit()

        placer.place( a_widget )
        self.channel_like_widget    = a_widget

        # ---- MyPref
        a_widget  = QLabel( "rrr" )
        placer.place( a_widget )

        a_widget    = QComboBox()
        values      = [ "Ignore", "Item 1", "Item 2", "Item 3"]
        a_widget.addItems( values )
        placer.place( a_widget )
        self.channel_pref_widget    = a_widget

        # self.channel_pref_widget.setCurrentText("Ignore")
        # text = self.channel_pref_widget.currentText()

        # ----Ch MyGroup
        a_widget  = QLabel( "ccc" )
        #placer.new_row()
        placer.place( a_widget )

        a_widget    = QComboBox()
        values      = ( "Ignore", 'Group1'  )
        a_widget.addItems( values )
        #a_widget.setCurrentText("Ignore")
        placer.place( a_widget )
        self.channel_group_widget  = a_widget

        # ----"Order By:"
        a_widget    = QLabel( "Order By:" )
        placer.new_row()
        placer.place( a_widget )

        a_widget    = QComboBox()
        values      = ( "Ignore", "title", 'pub_date', 'watched',
                              'view_count',  )
        a_widget.addItems( values )
        placer.place( a_widget )
        self.channel_order_by_widget  = a_widget

        # ---- buttons
        a_widget        = QPushButton( "Do Nothing" )
        #a_widget.clicked.connect(  self.clear_criteria )
        placer.new_row()
        placer.place( a_widget )

# ----------------------------------------
class PhotoshowHistorylTab( stuffdb_tabbed_sub_window.StuffdbTab  ):

    def __init__(self, parent_window ):

        super().__init__()

        self.parent_window   = parent_window
        self._build_gui()
        self.list_ix         = 0  # should track selected an item in detail

    #-------------------------------------
    def _build_gui( self ):
        """
        what it says read
        Returns:
            none
        """
        tab                 = self
        model               = QStandardItemModel()
        self.history_model  = model
        #self.model2         = model  # get rid of this

        model.setHorizontalHeaderLabels([ "ID", "descr"] )

        self.history_view = QTableView()       # !! table_history_view
        self.history_view.setModel( model )

        layout2     = QVBoxLayout()
        layout2.addWidget( self.history_view )
        tab.setLayout( layout2 )

        self.history_view.clicked.connect( self.parent_window.on_history_clicked )

# ==================================
class PhotoTextTab( stuffdb_tabbed_sub_window.StuffdbTab  ):

    def __init__(self, parent_window  ):

        pass
        super().__init__()
        self.parent_window   = parent_window
        self.__build_gui()

        model                    = QSqlTableModel( self, AppGlobal.qsql_db_access.db )
        self.detail_text_model   = model # !! change everywhere
        model.setTable( parent_window.text_table_name )
        print( f"on text tab {parent_window.text_table_name = }" )
        # print( "!! maybe do not want this select ")
        # model.select( )
        self.record_state   = self.RECORD_NULL


    #-------------------------------------
    def __build_gui( self ):
        """
        what it says read
        Returns:
            none
        """

        tab                 = self
        tab_layout          = QVBoxLayout(tab)

        self.id_field       = QLineEdit()
        self.id_field.setValidator( QIntValidator() )
        self.id_field.setPlaceholderText("Enter ID")
        tab_layout.addWidget(self.id_field)

        entry_widget         = QTextEdit()
        self.text_data_field = entry_widget
        entry_widget.setPlaceholderText( "Some Long \n text on a new line " )
        tab_layout.addWidget( entry_widget  )

        # self.name_field = QLineEdit()
        # self.name_field.setPlaceholderText("Name")
        # tab_layout.addWidget(self.name_field)

        # self.url_field = QLineEdit()
        # self.url_field.setPlaceholderText("URL")
        # tab_layout.addWidget(self.url_field)

        # self.mypref_field = QLineEdit()
        # self.mypref_field.setValidator(QIntValidator())
        # self.mypref_field.setPlaceholderText("Preference")
        # tab_layout.addWidget(self.mypref_field)

        # self.mygroup_field = QLineEdit()
        # self.mygroup_field.setPlaceholderText("Group")
        # tab_layout.addWidget(self.mygroup_field)

        button_layout = QHBoxLayout()

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
        # capture needed fields
        # yt_id    = self.yt_id_field.text()
        text_data       = self.text_data_field.text()

        self.default_new_row(  next_key )

        self.text_data_field.setTtext( f"{text_data} \n ------ \n {text_data}")

    # -----------------------------
    def default_new_row(self, next_key ):
        """
        what it says
            this is for a new row on the window -- no save
            needs key but timestamp photo from detail not text
        arg:
            next_key for table, just trow out if not used
        Returns:
            None.

        """
        self.clear_detail_fields()

        self.text_data_field.setText( f"this is the default text for id { next_key = }" )

        # # ---- ??redef add_ts
        # a_ts   = str( time.time() ) + "sec"
        # # record.setValue( "add_ts",  a_ts    )
        # self.add_ts_field.setText(  a_ts )
        # self.edit_ts_field.setText( a_ts )

        self.id_field.setText( str( next_key ) )





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
        print( f"photoshow text tab fetch_row { id = }")
        self.fetch_detail_row_by_id( id )

    # -----------------------------
    def fetch_text_row_by_id( self,  id   ):
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

        else:

            msg     = f"Fetch Error: No record tor text_data found with the given ID. { id = }"
            QMessageBox.warning(self, "Error",  msg )
            AppGlobal.logger.error( msg )

        # else:
        #     QMessageBox.warning(self, "Input Error", f"Please enter a valid ID. { id = }")

    # -----------------------------
    def delete_detail_row(self):
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

    # -----------------------------
    def _build_detail_rowxxxx(self):
        """
        what it says
        !! change to _build_detail_row  _build_detail_row

        Returns:
            None.

        """
        model       = self.detail_text_model
        text_data   = self.text_data_field.text()
        # name    = self.name_field.text()
        # url     = self.url_field.text()
        # mypref  = self.mypref_field.text()
        # mygroup = self.mygroup_field.text()

        record  = self.detail_text_model.record()
        record.setValue("text_data", text_data)
        # record.setValue("name", name)
        # record.setValue("url", url)
        # record.setValue("mypref", int(mypref) if mypref else None)
        # record.setValue("mygroup", mygroup)

        if  model.insertRecord(-1, record):
            model.submitAll()
            QMessageBox.information(self, "Create Success", "Record created successfully. text_detail")
            self.clear_detail_fields()  # really default?
        else:
            msg     = f"Create Error Failed to create record. text_detail {record = }"
            QMessageBox.warning(self, "Error", msg )
            AppGlobal.logger.error( msg )


    # ------------------------
    def clear_detail_fields(self):
        """
        what it says, read
        what fields, need a bunch of rename here
        clear_detail_fields  clear_detail_fields
        """
        self.id_field.clear()


        self.text_data_field.clear()
        # self.name_field.clear()
        # self.url_field.clear()
        # self.mypref_field.clear()
        # self.mygroup_field.clear()



    # -------------------------
    def update_text_rowxxxxx(self):
        """
        what it says, read
        row is the model   detail.model ??
        !! change to update_detail_row
        Returns:
            None.
        update_detail_row update_detail_row
        """
        model   = self.tab_model
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

    # -------------------------
    def update_new_record(self):
        """


        Returns:
            None.

        """
        print( f"update_new_record  {self.record_state  = }")

        if not self.record_state  == self.RECORD_NEW:
            print( f"save_new_record bad state, return  {self.record_state  = }")
            return

        model      = self.detail_text_model
        new_id     = self.idField.text()
        new_text   = self.textField.toPlainText()
        if new_id and new_text:
            record = model.record()
            record.setValue("id", int(new_id))
            record.setValue("text_data", new_text)
            model.insertRecord(self.model.rowCount(), record)
            model.submitAll()
            self.record_state    = self.RECORD_FETCHED
            QMessageBox.information(self, "Save New", "New record saved!")
        else:
            print( f"do not seem to have new id and text {new_id = } { new_text = }")

    # ----------------------
    def update_record_fetched(self):
        print( f"update_record_fetched  {self.record_state  = }")

        if not self.record_state  == record_fetched:
            print( f"update_record_fetched bad state, return  {self.record_state  = }")
            return

        model      = self.detail_text_model
        id_value = self.idField.text()
        if id_value:
            model.setFilter(f"id = {id_value}")
            model.select()
            if self.model.rowCount() > 0:
                record = model.record(0)
                record.setValue("id", int(id_value))
                record.setValue("text_data", self.textField.toPlainText())
                model.setRecord(0, record)
                model.submitAll()
                QMessageBox.information(self, "Save", "Record ( fetched ) saved!")
            model.setFilter("")



    #def update_db( self, ):
    def update_text( self, ):
       """


       """
       if   self.record_state   == self.RECORD_NULL:
           print( "update_db record null no action, return ")

       elif  self.record_state   == self.RECORD_NEW:
           self.update_new_record()

       elif  self.record_state   == self.RECORD_FETCHED:
           self.update_record_fetched()

       elif  self.record_state   == self.RECORD_DELETE:
           self.delete_record_update()

       else:
           print( f"update_db wtf  {self.record_state = } ")

       print( f"update_db record state now:  {self.record_state = } ")

    # ---------------------
    def delete_record_update(self):
        """


        Returns:
            None.

        """
        if not self.record_state  == self.RECORD.DELETE:
            print( f"delete_record_update bad state, return  {self.record_state  = }")
            return

        model       = self.detail_text_model
        id_value    = self.deleted_id
        if id_value:
            model.setFilter(f"id = {id_value}")
            model.select()
            if model.rowCount() > 0:
                model.removeRow(0)
                model.submitAll()
                self.clear_fields()  # will fix record state
                self.record_state       = self.RECORD_NULL
                QMessageBox.information(self, "delete_record_update", "Record deleted!")
            model.setFilter( "" )


# ==================================
class PhotoshowPhotoTab( QWidget  ):
    """
    think not in photoshow
    """
    def __init__(self, parent_window  ):
        """
        this tab does not interact with the db directly

        Args:
            parent_window (TYPE): DESCRIPTION.


        """
        super().__init__()
        self.parent_window   = parent_window
        #rint( f"PhotoPhotoTab __init__ {parent_window = }")
        self.__build_gui()

    #-------------------------------------
    def __build_gui( self ):
        """
        what it says read
        Returns:
            none
        """
        tab                 = self
        tab_layout          = QVBoxLayout(tab)

        viewer              = photo_viewer.PhotoViewer( self )
        self.viewer         = viewer
        tab_layout.addWidget( viewer )


        self.display_file()

        # ---- buttons
        a_widget        = QPushButton( "fit" )
        a_widget.clicked.connect(  self.fit_in_view )
        tab_layout.addWidget( a_widget )

        #---- buttons
        a_widget        = QPushButton( "<prior" )
        a_widget.clicked.connect(  self.fit_in_view )
        tab_layout.addWidget( a_widget )

        #---- buttons
        a_widget        = QPushButton( "next>" )
        a_widget.clicked.connect(  self.fit_in_view )
        tab_layout.addWidget( a_widget )


        print( "see chat_photo.py for more ... zoom to fit rectangle         chat_photo_3.py " )
        return

    # -----------------------------
    def display_file( self,  file_name = "/mnt/WIN_D/PhotoDB/02/102-0255_img.jpg"  ):
        """
        what it says, read

        """
        # pixmap      = QPixmap( file_name )
        # self.viewer.set_photo( pixmap )
        self.viewer.display_file( file_name )
        self.fit_in_view()

    #-------------------------------------
    def zoom_in(self):
        self.viewer.zoom_in
        print("Zoomed In")

    #-------------------------------------
    def zoom_out(self):
        self.viewer.zoom_out
        print("Zoomed Out")

    def reset_zoom(self):
        self.viewer.reset_zoom()
        print("Zoom Reset")

    #-------------------------------------
    def fit_in_view(self):
        self.viewer.fit_in_view()
        print("PhotoPhotoTab Fit in View")



# ----------------------------------------
class DetailSubWindow( QMdiSubWindow  ):
    """
    """

    def __init__(self, parent ):
        """
        the usual

        """
        super().__init__()

        self.parent    = parent
        # self is the subwindow

        sub_window              = self
        # sub_window.setWindowTitle( "this title may be replaced " )

        #self.connection         = None  # see get connection

        print( "DetailSubWindow this self.init_db is probably needs more work  move p to top window AppDb?")

        #self.db                 = AppGlobal.qsql_db_access.db

        #s#elf.detail_table_name  = "channel"

        self.prior_tab          = 0
        self.current_tab        = 0

        self.prior_criteria     = None
        self.current_criteria   = None    # init just after critera tab created

        # Main notebook with 3 tabs
        # main_notebook           = QTabWidget()
        # self.main_notebook      = main_notebook

        #main_notebook.currentChanged.connect( self.on_tab_changed )

        ix                        = -1

        ix                       += 1
        self.criteria_tab_index   = ix
        self.criteria_tab         = PhotoshowCriteriaTab( parent  )
        self.addTab(       self.criteria_tab,  "Criteria"  )
        #parent.midi_area

        # ix                              += 1
        # self.list_tab_index             = ix
        # self.list_tab                   = self._build_tab_list(  self  )
        # main_notebook.addTab(             self.list_tab  ,   "List"    )
        # # print( "!! fix monkey patch ")
        # # #self.list_tab.parent_window     = self

        # ix                       += 1
        # self.detail_tab_index     = ix
        # self.detail_tab           = self._build_tab_detail( self )
        # main_notebook.addTab( self.detail_tab,    "Detail"     )

        # ix                         += 1
        # self.detail_text_index      = ix
        # self.text_tab               = self._build_tab_text( self )
        # main_notebook.addTab( self.text_tab,    "Text"     )

        # ix                        += 1
        # self.history_tab_index     = ix
        # self.history_tab           = self._build_tab_history( self )
        # main_notebook.addTab( self.history_tab ,   "History"    )

        # # next move to tabs -- list and history should have same interface
        # # self.list_ix              = 0
        # # self.history_ix           = 0

        # sub_window.setWidget( main_notebook )
        # mdi_area.addSubWindow( sub_window )

        sub_window.show()

# ----------------------------------------
class PhotoshowEventTab( QWidget  ):
    """
    no events for photo show, this might be photos
    """

    def __init__(self, parent_window ):

        pass
        super().__init__()
        self.parent_window   = parent_window
        self.list_ix         = 5  # should track selected an item in detail
            # needs work
        self._build_tab()

    # ------------------------------------------
    def _build_tab( self,  ):
        """
        what it says, read
        !! initial query should come out

        """
        # !!
        #self.get_connection()   # does work yes else table not found

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
        model.setHeaderData( 0, Qt.Horizontal, "ID")
        #model.setHeaderData( 1, Qt.Horizontal, "YT ID"  )
        model.setHeaderData( 2, Qt.Horizontal, "Name"   )
        # model.setHeaderData( 3, Qt.Horizontal, "Url")
        # model.setHeaderData( 4, Qt.Horizontal, "mypref")
        # model.setHeaderData( 5, Qt.Horizontal, "mygroup")

        # Set up the view
        view                 = QTableView()
        self.list_view       = view

        view.setModel( model )

        placer.place(  view )

        self.select_all_for_test()

    # ------------------------------------------
    def select_all_for_test( self,  ):
        """
        what it says, read


        """
        model      = self.list_model

        query_ok   = model.select()

        msg        = f"{ query_ok = }"
        #rint( msg )
        AppGlobal.logger.debug( msg )

        #AppGlobal.yt_db.error_info( self.channel_model.lastError() )
        # AppGlobal.photo_db_db.error_info( model.lastError() )
        ia_qt.q_sql_error( model.lastError(),
                       msg   =  "now in code at:select_all_for_test")


        if not query_ok:
            msg     = f"select_all_for_test not query_ok {1} "  #"{AppGlobal.photo_db_db}"
            AppGlobal.logger.error( msg )
            print(  msg )

            print( " next 1/0    ", flush = True)
            1/0


        self.list_view.resizeColumnsToContents()

        #print( "need on list clicked")
        self.list_view.clicked.connect( self.parent_window.on_list_clicked )
        #view.doubleClicked.connect( self.on_list_double_clicked )

    # ---------------------------------------
    def fetch_id_test( self,  ):

        """
        """
        id  = 55
        print( f"fetch_id_test{id = }")
        self.fetch_row_by_id(  id )
        #self.text_tab.fetch_text_row_by_id(  id )


    # ---------------------------------------
    def fetch_row_by_id( self, id ):

        """
        """
        self.detail_tab.fetch_detail_row_by_id(  id )
        #self.text_tab.fetch_text_row_by_id(  id )
        self.detail_to_history()


    #-------------------------------------
    def i_am_hsw(self):
        """
        make sure call is to here

        """
        print( "i_am_hsw")

    #-------------------------------------
    def default_new_row( self ):
        """tail_tab.default_new_row( next_key )
        default values for a new row in the detail and the
        text tabs

        Returns:
            None.

        """
        next_key      = AppGlobal.key_gen.get_next_key(   self.detail_table_name )
        self.detail_tab.default_new_row( next_key )
        self.text_tab.default_new_row(   next_key )

    #-------------------------------------
    def copy_prior_row( self ):
        """tail_tab.default_new_row( next_key )
        default values for a new row in the detail and the
        text tabs
        probably can promote, may need different func name on text so tabs can be the same?
        Returns:
            None.
            """
        next_key      = AppGlobal.key_gen.get_next_key(   self.detail_table_name )
        self.detail_tab.copy_prior_row( next_key )
        self.text_tab.copy_prior_row(  next_key )

    # ------------------------------------------
    def _build_tab_list( self, parent_window   ):
        """
        what it says, read
        """
        return PhotoListTab( parent_window )

    # ------------------------------------------
    def _build_tab_criteria( self,   parent_window ):
        """
        what it says, read
        put page into the notebook

        """
        #return PhotophotoCriteriaTab( parent_window  )

    #-------------------------------------
    def _build_tab_detail( self, parent_window ):
        """
        '_build_tab_detail'
        """
        return PhotoDetailTab(  parent_window )

    #-------------------------------------
    def _build_tab_text( self, parent_window ):
        """
        '_build_tab_detail'
        """
        return PhotoTextTab(  parent_window )

    #-----------------------------
    def _build_tab_history( self,   parent_window ):
        """
        what it says, read

        """
        return PhotoHistorylTab( parent_window )

    # ------------------------------------------
    def criteria_select( self,     ):
        """
        what it says, read
        uses info from 2 tabs
        """
        print( "criteria_select in photo sub window next pull over channel_select " )

        #rint( "begin channel_select for the list")
        query                       = QSqlQuery()
        query_builder               = qt_sql_query.QueryBuilder( query )

        # ---- add criteria
        criteria_dict               = self.criteria_tab.get_criteria()

        model                       = self.list_tab.list_model

        query_builder.table_name    = "channel"
        query_builder.column_list   = [
            "id",
            "yt_id",
            "name",
            "url",
            "mypref",
            "mygroup"   ]


        channel_name_like  = criteria_dict["channel_name_like"].strip().lower()
        if channel_name_like:
            add_where       = "lower( channel.name )  like :channel_name_like"
            #where_dict      = {"channel_name_like":  f"%{channel_name_like}%"}
            #query_builder.add_to_where( add_where, where_dict )
            query_builder.add_to_where( add_where, [(  ":channel_name_like",
                                                     f"%{channel_name_like}%" ) ])

        query_builder.prepare_and_bind()

        msg      = f"{query_builder = }"
        AppGlobal.logger.debug( msg )

        msg      = f"Executing SQL query:  {query.executedQuery() = }"
        AppGlobal.logger.debug( msg )

        if query.exec():
            model.setQuery( query )
            if model.lastError().isValid():
                msg     = f"Query Error: {model.lastError().text() = }"
                print(  msg )
                AppGlobal.logger.error( msg )
        else:
            print( "Query Execution Error:", query.lastError().text())
            print(  msg )
            AppGlobal.logger.error( msg )

        self.main_notebook.setCurrentIndex( self.list_tab_index )

        #rint( "end channel_select" )

    # ------------------------------------------
    def channel_selectxxxx( self,     ):
        """
        what it says, read
        !! looks like execution of query can be promoted

        """
        #rint( "begin channel_select for the list")
        query                       = QSqlQuery()
        query_builder               = qt_sql_query.QueryBuilder( query )

        # ---- add criteria
        criteria_dict               = self.get_criteria()

        model                       = self.list_model

        query_builder.table_name    = "channel"
        query_builder.column_list   = [
            # "id",
            "yt_id",
            "name",
            "url",
            "mypref",
            "mygroup"   ]

        channel_name_like  = criteria_dict["channel_name_like"].strip().lower()
        if channel_name_like:
            add_where       = "lower( channel.name )  like :channel_name_like"
            #where_dict      = {"channel_name_like":  f"%{channel_name_like}%"}
            #query_builder.add_to_where( add_where, where_dict )
            query_builder.add_to_where( add_where, [(  ":channel_name_like",
                                                     f"%{channel_name_like}%" ) ])

        query_builder.prepare_and_bind()

        msg      = f"{query_builder = }"
        AppGlobal.logger.debug( msg )

        msg      = f"Executing SQL query:  {query.executedQuery() = }"
        AppGlobal.logger.debug( msg )

        if query.exec():
            model.setQuery( query )
            if model.lastError().isValid():
                msg     = f"Query Error: {model.lastError().text() = }"
                print(  msg )
                AppGlobal.logger.error( msg )
        else:
            print( "Query Execution Error:", query.lastError().text())
            print(  msg )
            AppGlobal.logger.error( msg )

        self.main_notebook.setCurrentIndex( self.list_tab_index )

        #rint( "end channel_select" )

    # ------------------------------------------
    def on_list_clicked( self, index: QModelIndex ):
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
        print( f"Clicked on list row {row}, column {column}, {db_key = }" ) # " value: {value}" )

        #self.detail_tab.fetch_detail_row_by_id( db_key )
        self.fetch_row_by_id( db_key )

        self.main_notebook.setCurrentIndex( self.detail_tab_index )
        #self.detail_tab.id_field.setText( str( db_key )  ) # fetch currently does not include the id


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
    def on_tab_changed( self, event ):
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
        # self.tap_page_photo_fn   = self.a_notebook.tab( self.a_notebook.select(), 'text' ) + ".txt"
        # print( f"tap_page_photo_fn  >>{self.tap_page_photo_fn}<< "
        #        "for tabpage on_changed need to remove spaces" )
        # #rint( f"on_changed  {event} for tabpage" )
        # #rint( self.get_info() )

    # ---- sub window interactions
    # -----------------------------------
    def detail_to_history( self, ):
        """
        what it says, read
        links two sub_windows

        """
        index    = self.detail_tab.detail_model.index( 0, 0 )
        self.add_row_history( index )

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
        # Get the data from the selected row
        detail_model    = self.detail_tab.detail_model
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
        !! finish me
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


    # # -----------------------------
    # def next_list_to_detail( self ):
    #     """
    #     !! promote as nothing seem to depend on which window type
    #     based on code in python programming and development
    #     Returns:
    #         None.

    #     """
    #     tab                =  self.list_tab
    #     tab.list_ix += 1
    #     if  tab.list_ix >    tab.list_model.rowCount() - 1:
    #         tab.list_ix   =  tab.list_model.rowCount() - 1
    #         # beep and return
    #         #self.list_ix    = 0

    #     record          = tab.list_model.record( tab.list_ix  )
    #     id_data         = record.value( "id")
    #     print( f"next_list_to_detail {id_data = } {record = } " )

    #     self.detail_tab.fetch_detail_row_by_id( id_data )
    #     self.detail_tab.id_field.setText( str( id_data )  ) # fetch currently does not include the id



    # # -----------------------------
    # def prior_list_to_detail( self ):
    #     """
    #     !! promote as nothing seem to depend on which window type
    #     based on code in python programming and development
    #     Returns:
    #         None.

    #     """
    #     tab                =  self.list_tab
    #     tab.list_ix -= 1
    #     if  tab.list_ix <    0:
    #         tab.list_ix   =  0
    #         print( "and you are at the beginning" )
    #         #!! is return ok
    #         # frequency_hz   = 2500  # windows only
    #         # duration_ms    = 1000
    #         # winsound.Beep( frequency_hz, duration_ms )
    #         # beep and return
    #         #self.list_ix    = 0

    #     record          = tab.list_model.record( tab.list_ix  )
    #     id_data         = record.value( "id")
    #     #rint( f"next_list_to_detail {id_data = } {record = } " )

    #     self.detail_tab.fetch_detail_row_by_id( id_data )
    #     self.detail_tab.id_field.setText( str( id_data )  ) # fetch currently does not include the id

    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = ">>>>>>>>>>* channel sub model  *<<<<<<<<<<<<"


        return a_str


# ----------------------------------------
class PhotoshowDetailListTab( QWidget  ):
    """
    tab in a tab, this is a list of the photos
    in the show
    """

    def __init__(self, parent_window ):
        """
        so i can have 2 lists, one of adds, one of deletes each can
        be a dict of info.
        manually put the data in the relational view and
        on submit generate queries for each

        the dict would be different for adds and deletes
        deletes only needs the photoshow_photo.id
        the add needs to display so needs some photo information:
        the dict would have the photo.id name and file_name for each photo and

        """

        super().__init__()
        self.parent_window   = parent_window
        self.sub_window      = parent_window.parent_window   # two levels up

        self.photo_tab       =  self.sub_window.photo_tab
        self.list_ix         = -1  # should track selected an item in detail
        self.list_table_name = "photoshow_photo"


        # # do we hanv this is whole table   no implied
        # self.sql_update = """
        #     SELECT
        #       photoshow_photo.id
        #       photoshow_photo.seq_no,
        #       photoshow_photo.photo_id
        #       photoshow_photo.photoshow_id

        #     FROM   photoshow_photo
        #     WHERE  photoshow_photo.photoshow_id.  = :id;
        # """
        AppGlobal.add_photo_target   = self
        self.db     = AppGlobal.qsql_db_access.db


        self.setup_models(  )

        self._build_gui()
        # self.select_by_id( id = 5529  )   # model   = self.setup_model( id = 5529 )

    # ------------------------------------------
    def _build_gui( self,  ):
        """
        what it says, read

        """
        page            = self
        tab             = page


        # ---- read
        main_layout          = QVBoxLayout( self )
        photo_layout         = QHBoxLayout( self )

        main_layout.addLayout( photo_layout )

        #view_read         = QTableView()     # claud could not get to work
        view_read         = QTableWidget()   # blackbox
        self.view_read    = view_read
        self.view_read.setColumnCount(5)
        self.view_read.setHorizontalHeaderLabels(["Photo Name",
                                             "Photo File Name",
                                             "Photo ID",
                                             "Photo Show Name",
                                             "Photo Show ID",
                                             ])



        view_read.cellClicked.connect( self._on_list_click  )
        photo_layout.addWidget( self.view_read )
        self.create_context_menu()

        # ---- photo
        a_photo_viewer            = photo_viewer.PhotoViewer( self )
        self.photo_viewer         = a_photo_viewer
        photo_layout.addWidget( a_photo_viewer )

        # view                = QTableView()
        # self.view_display   = view
        # view.setModel( model )


        # ---- write
        self.view_write    = QTableView()
        main_layout.addWidget( self.view_write )
        # # Set up the layout

        # self.widget.setLayout( self.layout )

        # self.layout.addWidget( view )


        # ---- buttons -- test photo select
        button_layout          = QHBoxLayout( self )
        main_layout.addLayout( button_layout )

        a_widget  = QLabel( "for the photos>>" )
        button_layout.addWidget( a_widget )


        a_widget        = QPushButton( "29" )
        connect_to      = functools.partial( self.select_by_id,
                                              29  )
        a_widget.clicked.connect(  connect_to )
        button_layout.addWidget( a_widget )

        # a_widget        = QPushButton( "2299" )
        # connect_to      = functools.partial( self.select_by_id,
        #                                      2299  )
        # a_widget.clicked.connect(  connect_to )
        # self.layout.addWidget( a_widget )

        # #
        # a_widget        = QPushButton( "<prior" )
        # #a_widget.clicked.connect(  self.fit_in_view )
        # button_layout.addWidget( a_widget )

        # #
        # a_widget        = QPushButton( "next>" )
        # #a_widget.clicked.connect(  self.fit_in_view )
        # button_layout.addWidget( a_widget )

        #
        a_widget        = QPushButton( "add row" )
        a_widget.clicked.connect(  self.add_row )
        button_layout.addWidget( a_widget )

    # --------------------
    def create_context_menu(self):
        """
        what it says

        """
        self.contextMenu = QMenu(self)

        addAction        = QAction("Add Row", self)
        #addAction.triggered.connect(self.addRow)
        self.contextMenu.addAction(addAction)

        deleteAction = QAction("Delete Row", self)
        #deleteAction.triggered.connect(self.deleteRow)
        self.contextMenu.addAction(deleteAction)

        self.view_read.setContextMenuPolicy(Qt.CustomContextMenu)
        self.view_read.customContextMenuRequested.connect( self.showContextMenu )

    def showContextMenu( self, pos ):
        """
        what it says
        !! change my name

        Args:
            pos (TYPE): DESCRIPTION.

        Returns:
            None.

        """
        self.contextMenu.exec_( self.view_read.mapToGlobal(pos) )

    # ---------------------------------
    def setup_models( self,  ):
        """
        may have too many instances
        Returns:
            modifies self, establishes -- wrong names
            self.view_model
            self.edit_model
            self.sql_read
        """
        # ---- read model

        self.sql_read = """
            SELECT
              photo.name,
              photo.photo_fn,
              photo.id,
              photoshow.name,
              photoshow.id,
              photoshow_photo.seq_no,
              photoshow_photo.photoshow_id
            FROM   photo
            JOIN   photoshow_photo
            ON     photoshow_photo.photo_id = photo.id
            JOIN   photoshow
            ON     photoshow.id = photoshow_photo.photoshow_id
            WHERE  photoshow.id = :id;
        """


        # """
        # #model        = QSqlQueryModel()
        # # next to allow additions
        # model               = sql_query_model_plus.SqlQueryModelPlus( )
        # # self.model_display  = model
        # # Prepare the SQL query
        # query              = QSqlQuery()
        # query.prepare( model )

        # # model              =  QSqlTableModel()
        # # self.model_update  = model
        # # Prepare the SQL query

        #model        = QSqlQueryModel()
        # pre bb for model
        # query_model_read       =  sql_query_model_plus.SqlQueryModelPlus()
        # self.query_model_read  = query_model_read

        query_read            = QSqlQuery()
        self.query_read_prep  = query_read  # looks wrong


        query_read.prepare(  self.sql_read  )

        # Bind values to the query  --- can leave until we do query
        query_read.bindValue(":id", id )


        # Execute the query and set the model
       # query.exec_()
        # query_model_read.setQuery( query_read,  )

        # ---- write model
        #db     = AppGlobal.qsql_db_access.db

        table_model_write        = QSqlTableModel( self,  self.db )
        self.table_model_write   = table_model_write

        self.table_model_write.setTable("photoshow_photo")
        self.table_model_write.setEditStrategy( QSqlTableModel.OnManualSubmit )
        self.table_model_write.setFilter( "photoshow_id = 29 " )


    # ------------------------------------------
    def _on_list_click( self, row, column ):
        """
        what it says, read
        now just a table
        """
        print("Row %d and Column %d was clicked" % (row, column))

        print( f"PhotoshowDetailListTab_on_list_click   ")
        # row                     = index.row()
        # column                  = index.column()
        self.list_ix           = row
        self.prior_next( 0 )


    # ------------------------------------------
    def _display_photo_by_fn( self, file_name  ):
        """
        what it says, read
        do we need this?
        """
        self.photo_viewer.display_file( file_name )


    # ------------------------------------------
    def prior_next( self, delta  ):
        """
        get and put in control the prior or next photo
        using delta to determine which

        what it says, read
        direction  + forward, -backward 0 at start
        -- perhaps let it use any number so as to jump around


        watch for off by one, assume zero indexing

        """
        #prior_list_ix    = self.list_ix  # ng
        no_rows    = self.view_read.rowCount()

        list_ix                  = self.list_ix
        new_list_ix              = list_ix + delta
        # self.list_ix           = row
        if no_rows <= 0:
            msg     = f"prior_next {no_rows = } {delta = } should clear display"
            print( msg )

        if new_list_ix >= no_rows:
            new_list_ix  =  no_rows -1
            msg     = f"prior_next {no_rows = } {delta = } tried to index past end"
            print( msg )

        elif new_list_ix < 0:
            new_list_ix  =  0
            msg     = f"prior_next {no_rows = } {delta = } tired to index before start"
            print( msg )
        # else in range

        self.list_ix           = new_list_ix
        # fn_index               = self.query_model_read.index( new_list_ix, 1 )
        # file_name              = self.query_model_read.data( fn_index, Qt.DisplayRole )

        fn_item               =  self.view_read.item( self.list_ix,  1 )
        file_name  = fn_item.text() if fn_item is not None else ""

        #rint( f"change to prior next 0 {file_name = }" )
        self._display_photo_by_fn( file_name )

        self.photo_tab.display_file( file_name )  # the other tab in sub window
        print( "above bad because hard to find self.photo_tab.display_file( file_name )"  )


    #-------------------------------------
    def add_photo_to_show( self, row_dict  ):
        """
         use app global until i have something better
         for awhile same function down down there
         call via app_global
         AppGlobal.add_photo_target.add_photo_to_show( row_dict )
        """
        print( f"add_photo_to_show I was targeted  {row_dict}")
        self.add_row( row_dict )


    # ------------------------------------------
    def add_row( self,  row_dict = None   ):
        """
        None until get more hooked up
        post black box
        looks like we are missing sequence no
        and will need update for it ?
        add row data will be missing some values
        we will add here
        for now only at end
        """
        if row_dict is None:
            row_dict  = {}  # but will have error later


        # ---- setup data

        next_key                = AppGlobal.key_gen.get_next_key( self.list_table_name )

        # ---- sequence no
        max_seq            = 0
        seq_no_field_id    = 3
        for ix      in  range( 0, self.table_model_write.rowCount() ):
            ix_index          = self.table_model_write.index( ix, seq_no_field_id )
            seq_no            = self.table_model_write.data(  ix_index, Qt.DisplayRole )
            max_seq           = max( max_seq, seq_no )

        seq_no   = max_seq + 1
        #rint( f"{seq_no = }   ")
        photoshow_photo_id      = next_key


        # much is phony data -- later in call
        row_dict ["photoshow_id" ]             = self.photoshow_id
        row_dict ["photoshow_photo_seq_no" ]   = 999,
        row_dict ["seq_no" ]                   = seq_no,
        row_dict[ "photoshow_name" ]           = "don't need ps name"

        # must match the select order
        row_list    = [ row_dict[ "photo_name" ],
                               row_dict[ "photo_fn" ],
                               row_dict[ "photo_id" ],
                               row_dict[ "photoshow_name" ],
                               row_dict[ "photo_name" ],
                               row_dict[ "photoshow_id" ],
                               row_dict[ "photoshow_photo_seq_no" ],
                               row_dict[ "photoshow_photo_id" ],
                            ]

        # ---- read
        # self.query_model_read.addRow( row_list )
        # self.query_model_read.layoutChanged.emit()



        view_read      = self.view_read
        row            =  view_read.rowCount()
        #rint( f"{row = }")  -- look at query
        view_read.setRowCount( row + 1 )
        view_read.setItem(row, 0, QTableWidgetItem( row_dict[ "photo_name" ]  ) )
        view_read.setItem(row, 1, QTableWidgetItem( row_dict[ "photo_fn" ]  ) )
        view_read.setItem(row, 2, QTableWidgetItem( row_dict[ "photo_id" ]  ) )
        view_read.setItem(row, 3, QTableWidgetItem( row_dict[ "photoshow_name" ]  ) )
        view_read.setItem(row, 4, QTableWidgetItem( row_dict[ "photoshow_id" ]  ) )
        # may be more

        # ---- write
        record          =  self.table_model_write.record()
        record.setValue(  "id",   photoshow_photo_id               )

        record.setValue(  "photoshow_id",   row_dict[ "photoshow_id" ]    )
        record.setValue(  "photo_id",       row_dict[ "photo_id" ]    )

        field_name  = "seq_no"
        record.setValue(  field_name,       row_dict[ field_name ]    )

        ok   = self.table_model_write.insertRecord( -1,  record  )  #const QSqlRecord &record)addRow( custom_row_data)
        print( f"add_row  insert record {ok = }")

        self.table_model_write.layoutChanged.emit()

    # ------------------------------------------
    def add_row_pre_bb( self,    ):
        """
        looks like we are missing sequence no
        and will need update for it ?
        add row data will be missing some values
        we will add here

        """

        # ---- setup data

        next_key                = AppGlobal.key_gen.get_next_key( self.list_table_name )

        # ---- sequence no
        max_seq            =0
        seq_no_field_id    = 3
        for ix      in  range( 0, self.table_model_write.rowCount() ):
            ix_index          = self.table_model_write.index( ix, seq_no_field_id )
            seq_no            = self.table_model_write.data(  ix_index, Qt.DisplayRole )
            max_seq           = max( max_seq, seq_no )

        seq_no   = max_seq + 1
        #rint( f"{seq_no = }   ")


        photoshow_photo_id      = next_key
        row_dict            = { "photo_name":               "this is a photo_name",
                               "photo_fn":                 "/mnt/WIN_D/PhotoDB/13/Dsc02602.jpg",
                               "photo_id":                  999,
                               "photoshow_name":           "photoshow_name data ",
                               "photoshow_id":              self.photoshow_id,
                               "photoshow_photo_seq_no":    999,
                               "photoshow_photo_id":        photoshow_photo_id,
                               "seq_no":                    seq_no,
                               }

        # must match the select order
        row_list    = [ row_dict[ "photo_name" ],
                               row_dict[ "photo_fn" ],
                               row_dict[ "photo_id" ],
                               row_dict[ "photoshow_name" ],
                               row_dict[ "photo_name" ],
                               row_dict[ "photoshow_id" ],
                               row_dict[ "photoshow_photo_seq_no" ],
                               row_dict[ "photoshow_photo_id" ],
                            ]

        # ---- read
        self.query_model_read.addRow( row_list )
        self.query_model_read.layoutChanged.emit()

        # ---- write
        record          =  self.table_model_write.record()
        record.setValue(  "id",   photoshow_photo_id               )

        record.setValue(  "photoshow_id",   row_dict[ "photoshow_id" ]    )
        record.setValue(  "photo_id",       row_dict[ "photo_id" ]    )

        field_name  = "seq_no"
        record.setValue(  field_name,       row_dict[ field_name ]    )


        ok   = self.table_model_write.insertRecord( -1,  record  )  #const QSqlRecord &record)addRow( custom_row_data)
        print( f"add_row  insert record {ok = }")

        self.table_model_write.layoutChanged.emit()

        """
        record = model.record()

        # Populate the QSqlRecord with data
        record.setValue("name", "New Photo")
        record.setValue("photo_fn", "new_photo.jpg")
        record.setValue("id", None)  # Assuming the ID is auto-increment
        record.setValue("photoshow_id", 1)  # Example value

        # Insert the QSqlRecord into the model
        if model.insertRecord(-1, record):
            print("Record inserted successfully")
             # query_model_read
             # table_model_write
"""

    # ------------------------------------------
    def select_by_id ( self, id ):
        """
        black box
        what it says, read
        id is the id of the photo show
        self.edit_model.setFilter( "id = 33 " )

        #model.setFilter(f'photoshow.id = {photoshow_id}')

        # Set the sort order
        column_to_sort_by   = 0  # Index of the column to sort by (e.g., 0 for the first column)
        sort_order          = Qt.AscendingOrder  # or Qt.DescendingOrder
        self.edit_model.setSort(column_to_sort_by, sort_order)


        msg       = f"{self.edit_model.selectStatement()}"
        print( msg )
        """
        self.photoshow_id   = id

        print( f"select_by_id  {id = }")

        # ---- write
        self.table_model_write.setFilter( f"photoshow_id = {id} " )
        self.table_model_write.select()
        self.view_write.setModel( self.table_model_write )

        # ---- read
        sql_read = f"""
            SELECT
              photo.name AS photo_name,
              photo.photo_fn,
              photo.id AS photo_id,
              photoshow.name AS photoshow_name,
              photoshow.id AS photoshow_id
            FROM   photo
            JOIN   photoshow_photo
            ON     photoshow_photo.photo_id = photo.id
            JOIN   photoshow
            ON     photoshow.id = photoshow_photo.photoshow_id
            WHERE  photoshow.id = :id;
        """

        query_read      = QSqlQuery( self.db )

        query_read.prepare( sql_read )
        query_read.bindValue( ":id", id )

        #is_ok      =  query_read.exec( )

        view_read  = self.view_read

        if query_read.exec_():
            while query_read.next():
                row =  view_read.rowCount()
                #rint( f"{row = }")
                view_read.setRowCount( row + 1 )
                view_read.setItem(row, 0, QTableWidgetItem( query_read.value(0)))
                view_read.setItem(row, 1, QTableWidgetItem( query_read.value(1)))
                view_read.setItem(row, 2, QTableWidgetItem( str(query_read.value(2))))
                view_read.setItem(row, 3, QTableWidgetItem( query_read.value(3)))
                view_read.setItem(row, 4, QTableWidgetItem( str(query_read.value(4))))
        else:
            QMessageBox.critical(self, "Error", "view_read Failed to execute query")


        # photo display
        self.list_ix    = 0
        self.prior_next( 0 )


# ---- eof ------------------------------
