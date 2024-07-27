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
    QSqlQuery
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
#import collections
import functools
import time

# import winsound windows only


# ---- imports local

from    app_global import AppGlobal

import  gui_qt_ext
import  string_util
import  qt_sql_query
#import  document_maker
import  stuffdb_tabbed_sub_window
import  ia_qt
import  photo_viewer

# ----------------------------------------
class PhotoSubWindow( stuffdb_tabbed_sub_window.StuffdbTabbedSubWindow ):
    """
    for the photo table....
    """
    def __init__(self,  ):
        """
        the usual


        """
        super().__init__()

        self.db                 = AppGlobal.qsql_db_access.db

        self.detail_table_name  = "photo"
        self.text_table_name    = "photo_text"  # text tables always id and text_data

        # # for testing, generalization and ability not to create -- promoted
        # self.criteria_tab       = None
        # self.list_tab           = None
        # self.detail_tab         = None
        # self.text_tab           = None
        # self.history_tab        = None
        # self.criteria_tab_index = None

        self.subwindow_name     = "PhotoSubWindow"

        self._build_gui()


    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says
        """
        mdi_area                = AppGlobal.main_window.mdi_area
            #we could return the sub window for parent to add
        sub_window              = self
            # sub_window.setWindowTitle( "this title may be replaced " )

        self.prior_tab          = 0
        self.current_tab        = 0

        self.prior_criteria     = None
        self.current_criteria   = None    # init just after criteria tab created

        # Main notebook with  tabs
        main_notebook           = QTabWidget()
        self.main_notebook      = main_notebook

        main_notebook.currentChanged.connect( self.on_tab_changed )

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
        # print( "!! fix monkey patch ")
        # #self.list_tab.parent_window     = self

        ix                       += 1
        self.detail_tab_index     = ix
        self.detail_tab           = self._build_tab_detail( self )
        main_notebook.addTab( self.detail_tab,    "Detail"     )

        ix                         += 1
        self.detail_text_index      = ix
        self.text_tab               = self._build_tab_text( self )
        main_notebook.addTab( self.text_tab,    "Text"     )

        ix                         += 1
        self.photo_index           = ix
        #rint( f"__init__  {self = }")
        self.photo_tab             = self._build_tab_photo( self )
        #rint( f">>>>> Sub Window _build_tab_photo __init__  {self.photo_tab = }")
        main_notebook.addTab( self.photo_tab,    "Photo"     )

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
        return PhotoListTab( parent_window )

    # ------------------------------------------
    def _build_tab_criteria( self,   parent_window ):
        """
        what it says, read
        put page into the notebook
        """
        return PhotoCriteriaTab( parent_window  )

    #-------------------------------------
    def _build_tab_detail( self, parent_window ):
        """
        '_build_tab_detail'
        """
        return PhotoDetailTab(  parent_window )

    #-------------------------------------
    def _build_tab_photo( self, parent_window ):
        """
        'build_tab_detail'
        """
        print( f"_build_tab_photo  {parent_window = }")
        return PhotoPhotoTab( parent_window )

    #-------------------------------------
    def _build_tab_text( self, parent_window ):
        """
        '_build_tab_detail'
        """
        return PhotoTextTab(  parent_window )

    #-----------------------------
    def _build_tab_history( self, parent_window ):
        """
        what it says, read
        """
        return PhotoHistorylTab( parent_window )

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

        #self.fetch_row_by_id( db_key )
        self.select_record( db_key )

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
        print( f"photo Clicked on list row {row}, column {column}, {db_key = }" )

        #self.detail_tab.fetch_detail_row_by_id( db_key )
        #self.fetch_row_by_id( db_key )

        self.select_record( db_key )


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

    # ------------------------------------------
    def save( self,   ):
        """
        also know as update -- update detail tab and related
        """
        # self.db_update( )

        print( "save.... need to complete and route to update_db ")
        self.update_db()

    # --------------------------
    def update_db_try_premote( self,   ):
        """
        also know as update -- update detail tab and text...
        """
        #self.detail_tab.db_update()

        self.detail_tab.update_db()
        self.text_tab.update_db()

        msg     = "update_db.... need to complete and route to db_update -- done ??"
        print( msg )

    # --------------------------
    def delete_record( self,   ):
        """
        also know as update -- update detail tab and text...
        """
        #self.detail_tab.db_update()

        if self.popup_delete_question():

            self.detail_tab.delete_record()
            self.text_tab.delete_record()

            msg     = "delete_record.... -- done ??"
            print( msg )
        else:
            pass # for now

    # --------
    def popup_delete_question_promote(self):
        """
        Generate a popup ........
        consider add more info later
        """
        msgbox  =  QMessageBox()
        msgbox.setWindowTitle("Confirm Delete")
        msgbox.setIcon( QMessageBox.Warning)
        msgbox.setText("Do you want to Delete this Record")
        botonyes =  QPushButton("Yes")
        msgbox.addButton(botonyes, QMessageBox.YesRole)
        botonno =  QPushButton("No")
        msgbox.addButton(botonno, QMessageBox.NoRole)
        msgbox.exec_()
        if msgbox.clickedButton() == botonno:
            return False
        else:
            return True

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
            "add_kw",
            "photo_fn",
              ]

        key_words           = criteria_dict[ "key_words" ].strip().lower()
        if key_words:
            add_where       = "lower( photo.add_kw )  like :key_words"   # :is name of bind var below
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
    def detail_to_history_promote( self, ):
        """
        what it says, read
        links two sub_windows

        """
        index    = self.detail_tab.tab_model.index( 0, 0 )
        self.add_row_history( index )

    # -----------------------------------
    def add_row_history( self, index ):
        """
        pretty much from chat

        def add_row_to_tab2(self, index):
        # Get the data from the selected row
        id_data = self.model.data(self.model1.index(index.row(), 0))
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
        ia_qt.q_sql_query_model( self.detail_tab.tab_model, "add_row_history photo_sub" )


        id_data         = detail_model.data( detail_model.index( index.row(), 0))
        name_data       = detail_model.data( detail_model.index( index.row(), 2))
        print( f"in add_row_history {id_data = }   {name_data = }")
        # Create items for the second model
        id_item     = QStandardItem( str(id_data) )
        name_item   = QStandardItem( name_data )

        # Add a new row to the second model
        history_model.appendRow([id_item, name_item])

    # ---------------------------------------
    def select_record( self, a_id ):
        """
        what it says, mostly focused on the detail tab
        """
        # self.detail_tab.fetch_detail_row_by_id(  a_id )
        # self.text_tab.fetch_text_row_by_id(  a_id )

        self.detail_tab.select_record(  a_id )
        self.text_tab.select_record(  a_id )

        self.detail_to_history()

    # ---------------------------------------
    def display_photo( self, file_name  ):
        """
        what it says, mostly focused on the detail tab
        """
        print( f"<<<<<< display_photo  {self.photo_tab = }")
        self.photo_tab.display_file( file_name )

        # self.text_tab.fetch_text_row_by_id(  id )
        # self.detail_to_history()

    #-------------------------------------
    def i_am_hsw(self):
        """
        make sure call is to here for testing
        """
        print( f"i_am_hsw { self.subwindow_name = }")

    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = ">>>>>>>>>>* photoSubWindow  *<<<<<<<<<<<<"

        return a_str

# ----------------------------------------
class PhotoCriteriaTab( stuffdb_tabbed_sub_window.StuffdbTab , ):
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

        # ----
        a_widget  = QLabel( "photo Key Words" )
        placer.new_row()
        placer.place( a_widget )

        a_widget    = QLineEdit()
        placer.place( a_widget )
        self.key_words_widget    = a_widget

        # ----
        a_widget  = QLabel( "Name (like)" )
        placer.new_row()
        placer.place( a_widget )

        a_widget    = QLineEdit()
        placer.place( a_widget )
        self.name_widget    = a_widget



        # a_widget    = QComboBox()
        # values      = [ "Ignore", "Item 1", "Item 2", "Item 3"]
        # a_widget.addItems( values )
        # placer.place( a_widget )
        # self.channel_pref_widget    = a_widget

        # # self.channel_pref_widget.setCurrentText("Ignore")
        # # text = self.channel_pref_widget.currentText()


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

        # ---- buttons
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

            note: strip the strings
        """
        criteria_dict                        = {}

        # text() for line edit
        criteria_dict[ "key_words" ]         = self.key_words_widget.text().strip()
        # criteria_dict[ "channel_group" ]        = self.channel_group_widget.currentText().strip()
        # criteria_dict[ "channel_name_like" ]    = self.channel_like_widget.text().strip()
        criteria_dict[ "name" ]              = self.name_widget.text().strip()

        msg      = f"photo {criteria_dict = }"
        print(  msg )
        AppGlobal.logger.debug( msg )

        return criteria_dict

    # -------------------------
    def clear_criteria( self,   ):
        """
        what it says, read

        """
        self.key_words_widget.setText( "" )
        self.name_widget.setText( "" )
        # self.channel_pref_widget.setCurrentText(  "Ignore" )
        # self.channel_group_widget.setCurrentText( "Ignore" )

# ----------------------------------------
class PhotoListTab( stuffdb_tabbed_sub_window.StuffdbTab   ):

    def __init__(self, parent_window ):
        """
        the usual

        """
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
        # ia_qt.q_sql_error( model.lastError(),
        #                msg   =  "now in code at:select_all_for_test")

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
class PhotoDetailTab( stuffdb_tabbed_sub_window.StuffdbTab   ):
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
        #self.tab_name     = "photoDetailTab"   # { self.tab_name = }

        self.tab_name           = "PhotoDetailTab"

        model                   = QSqlTableModel( self, AppGlobal.qsql_db_access.db )
        self.tab_model          = model
        self.table              = parent_window.detail_table_name

        model.setTable( self.table )

        #print( f"!! maybe do not want this select { self.tab_name = } now gone ")
        #model.select( )

    #-------------------------------------
    def _build_gui( self ):
        """
        what it says read
        trying with placer to add labels
        Returns:
            none
        """
        # tab             = self
        # tab_layout      = QVBoxLayout(tab)


        page            = self
        tab             = page

        box_layout_1    =  QVBoxLayout( page )

        # placer          = gui_qt_ext.PlaceInGrid(
        #                     central_widget  = page,
        #                     a_max           = 0,
        #                     by_rows         = False  )

        placer          = gui_qt_ext.PlaceInGrid(
                            central_widget  = box_layout_1,
                            a_max           = 0,
                            by_rows         = False  )

        #box_layout_1.addLayout( box_layout_1 )


        # ---- new template code
        # # ---- add_ts
        # a_widget  = QLabel( "add_ts" )
        # placer.new_row()
        # placer.place( a_widget )

        # a_field                 = QLineEdit()
        # self.add_ts_field       = a_field
        # a_field.setPlaceholderText("add_ts")
        # placer.place( a_field )



        # ---- define fields
        # ---- Id
        a_widget            = QLabel( "Id" )
        placer.new_row()
        placer.place( a_widget )

        a_field                 = QLineEdit()
        self.id_field           = a_field
        a_field.setValidator( QIntValidator() )
        a_field.setPlaceholderText( "Enter ID" )
        placer.place( a_field )


        # ---- Name
        a_widget                = QLabel( "Name" )
        placer.new_row()
        placer.place( a_widget )

        a_field                 = QLineEdit()
        self.name_field         = a_field
        #a_field.setValidator( QIntValidator() )
        a_field.setPlaceholderText( "Name" )
        placer.place( a_field )

        # ---- descr_field
        a_widget                = QLabel( "Descr" )
        placer.new_row()
        placer.place( a_widget )

        a_field                 = QLineEdit()
        self.descr_field        = a_field
        #a_field.setValidator( QIntValidator() )
        a_field.setPlaceholderText( "descr...." )
        placer.place( a_field )

        # # ---- key words --- is this a field -- for testing
        # a_widget  = QLabel( "photo Key Words" )
        # placer.new_row()
        # placer.place( a_widget )

        # a_widget    = QLineEdit()
        # placer.place( a_widget )
        # self.key_words_widget    = a_widget

        # self.descr_field = QLineEdit()
        # self.descr_field.setPlaceholderText( "descr" )
        # #tab_layout.addWidget(self.descr_field )

# ------------------
#         self.add_kw_field = QLineEdit()
#         self.add_kw_field.setPlaceholderText( "add_kw" )
#         #tab_layout.addWidget(self.add_kw_field)

        # ---- key_words
        a_widget                = QLabel( "Key Words" )
        placer.new_row()
        placer.place( a_widget )

        a_field                 = QLineEdit()
        self.add_kw_field       = a_field
        #a_field.setValidator( QIntValidator() )
        a_field.setPlaceholderText( "key_words...." )
        placer.place( a_field )


# --------------------
#         edit_field              = QLineEdit()
#         self.photo_fn_field     = edit_field

        # ---- photo_fn_field
        a_widget                = QLabel( "File name" )
        placer.new_row()
        placer.place( a_widget )

        a_field                 = QLineEdit()
        self.photo_fn_field     =  a_field
        #a_field.setValidator( QIntValidator() )
        a_field.setPlaceholderText( "photo_fn_field...." )
        placer.place( a_field )

        # ---- add_ts
        a_widget  = QLabel( "add_ts" )
        placer.new_row()
        placer.place( a_widget )

        a_field                 = QLineEdit()
        self.add_ts_field       = a_field
        a_field.setPlaceholderText("add_ts")
        placer.place( a_field )

        # ---- edit_ts
        a_widget  = QLabel( "edit_ts" )
        #placer.new_row()
        placer.place( a_widget )

        a_field                 = QLineEdit()
        self.edit_ts_field      = a_field
        a_field.setPlaceholderText("edit_ts")
        placer.place( a_field )

        # button = QPushButton( "Clear" )
        # button.clicked.connect(self.clear_fields )
        # button_layout.addWidget( button )

        # _build_button = QPushButton("Create")
        # _build_button.clicked.connect(self._build_detail_row)
        # button_layout.addWidget(_build_button)

        # _build_button = QPushButton("Create Default")
        # _build_button.clicked.connect( self._build_default_row )
        # button_layout.addWidget(_build_button)    = edit_field
        # edit_field.setPlaceholderText( "photo_fn" )
        #tab_layout.addWidget( edit_field )

        # self.add_kw_field = QLineEdit()
        # self.add_kw_field.setPlaceholderText("add_kw")
        # tab_layout.addWidget(self.add_kw_field)

        self.edit_ts_field = QLineEdit()
        self.edit_ts_field.setPlaceholderText("edit_ts")
        #tab_layout.addWidget( self.edit_ts_field)

        # # ---- new template code
        # edit_field              = QLineEdit()
        # self.add_ts_field       = edit_field
        # edit_field.setPlaceholderText("add_ts")
        # #tab_layout.addWidget( edit_field )


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


        box_layout_1.addWidget( tab_folder )
        sub_tab      = TestDetaiSubTab( self )
        tab_folder.addTab( sub_tab, "a test" )

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

        # # ---- buttons
        button_layout = QHBoxLayout()
        # box_layout_1.addLayout( button_layout )
        # fetch_button = QPushButton("Fetch")
        # fetch_button.clicked.connect(self.fetch_detail_row)
        # button_layout.addWidget(fetch_button)

        # delete_button = QPushButton("Delete")
        # delete_button.clicked.connect(self.delete_detail_row)
        # button_layout.addWidget(delete_button)



        # # update_button = QPushButton("db_update detail")
        # # update_button.clicked.connect(self.db_update )
        # # button_layout.addWidget(update_button)

        # button = QPushButton( "To History" )
        # print( "need detail_to_history")
        # button.clicked.connect( self.parent_window.detail_to_history )

        # ---- buttons
        a_widget        = QPushButton( "Add to Show" )
        a_widget.clicked.connect(  self.add_to_show )
        button_layout.addWidget( a_widget )

    #-------------------------------------
    def _build_gui_box( self ):
        """
        what it says read
        Returns:
            none
        """
        tab             = self
        tab_layout      = QVBoxLayout(tab)

        # ---- define fields
        self.id_field   = QLineEdit()
        self.id_field.setValidator( QIntValidator() )
        self.id_field.setPlaceholderText( "Enter ID" )
        tab_layout.addWidget(self.id_field)

        # --- use this style
        a_field             = QLineEdit()
        self.name_field     = a_field
        a_field.setPlaceholderText( "name" )
        tab_layout.addWidget( a_field )



        self.descr_field = QLineEdit()
        self.descr_field.setPlaceholderText( "descr" )
        tab_layout.addWidget(self.descr_field )


        self.add_kw_field = QLineEdit()
        self.add_kw_field.setPlaceholderText( "add_kw" )
        tab_layout.addWidget(self.add_kw_field)

        edit_field              = QLineEdit()
        self.photo_fn_field     = edit_field
        edit_field.setPlaceholderText( "photo_fn" )
        tab_layout.addWidget( edit_field )

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

        sub_tab      = TestDetaiSubTab( self )
        tab_folder.addTab( sub_tab, "a test" )

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
        # button.clicked.connect(self.clear_fields )
        # button_layout.addWidget( button )

        # _build_button = QPushButton("Create")
        # _build_button.clicked.connect(self._build_detail_row)
        # button_layout.addWidget(_build_button)

        # _build_button = QPushButton("Create Default")
        # _build_button.clicked.connect( self._build_default_row )
        # button_layout.addWidget(_build_button)

        update_button = QPushButton("db_update detail only")
        update_button.clicked.connect(self.db_update )
        button_layout.addWidget(update_button)

        button = QPushButton( "To History" )
        print( "need detail_to_history")
        button.clicked.connect( self.parent_window.detail_to_history )

        # ---- buttons
        a_widget        = QPushButton( "Add to Show" )
        a_widget.clicked.connect(  self.add_to_show )
        button_layout.addWidget( a_widget )



        button_layout.addWidget(update_button)

        tab_layout.addLayout( button_layout )

        # a second sub layout
        button_layout = QHBoxLayout()
        tab_layout.addLayout( button_layout )

    # ----------------------------
    def fetch_detail_row( self,  a_id = None ):
        """
        Args:
            id can be external or as chat has it fetched

        Returns:
            None.
        !! could be promoted
        """
        a_id      = self.id_field.text()
        print( f"fetch_row { a_id = }")
        self.fetch_detail_row_by_id( a_id )

    # -----------------------------
    def add_to_show( self, ):
        """




        """
        photo_id      =  int( self.id_field.text() )
        photo_fn      =  self.photo_fn_field.text()
        row_dict            = { "photo_name":               "from photo sub_window",
                                "photo_fn":                  photo_fn,
                                "photo_id":                  photo_id,
                                "photoshow_photo_id":        photo_id,
                               }

        AppGlobal.add_photo_target.add_photo_to_show( row_dict )



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

        self.clear_fields()

        # ---- ??redef add_ts
        a_ts   = str( time.time() ) + "sec"
        # record.setValue( "add_ts",  a_ts    )
        self.add_ts_field.setText(  a_ts )
        self.edit_ts_field.setText( a_ts )

        self.id_field.setText( str( next_key ) )



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
        record.setValue( "add_kw",     self.add_kw_field.text())
        record.setValue( "descr",      self.descr_field.text())
        record.setValue( "photo_fn",      self.photo_fn_field.text())
        # ---- timestamps
        #record.setValue( "add_ts",   self.add_ts_field.text()) # should have already been set
        record.setValue( "edit_ts",  self.edit_ts_field.text())

    # ------------------------
    def record_to_field(self, record ):
        """
        """
        self.descr_field.setText(     record.value(    "descr"       ))
        self.name_field.setText(     record.value(    "name"       ))
        self.add_kw_field.setText(    record.value(    "add_kw"       ))
        self.photo_fn_field.setText(  record.value(    "photo_fn"       ))


        # self.add_ts_field.setText(record.value(      "add_ts"    ))
        self.edit_ts_field.setText(record.value(     "edit_ts"   ))
        self.add_ts_field.setText(record.value(       "add_ts"   ))
        # seems to work
        # a_ts   = str( time.time() )
        # #self.add_ts_field.clear()
        # self.edit_ts_field.setText(  a_ts   )
        print( "still need update for edit ts" )
        self.parent_window.display_photo( self.photo_fn_field.text( ) )

        # does this work
        # self.id_field.setText(  str( record.value(    "id"      ) ) )


    # ------------------------
    def clear_fields(self):
        """
        what it says, read
        what fields, need a bunch of rename here
        clear_fields  clear_fields  -- or is this default
        !! but should users be able to?? may need on add -- this may be defaults
        """
        self.id_field.clear()
        #self.descr_field.clear()
        self.name_field.clear()
        self.add_kw_field.clear()
        # self.url_field.clear()
        # self.mypref_field.clear()
        # self.mygroup_field.clear()

        # a_ts   = str( time.time() )
        # #self.add_ts_field.clear()
        # self.edit_ts_field.setText(  a_ts   )
        # self.edit_ts_field.clear()

# ----------------------------------------
class TestDetaiSubTab( stuffdb_tabbed_sub_window.StuffdbTab ,    ):

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
class PhotoHistorylTab( stuffdb_tabbed_sub_window.StuffdbTab   ):

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
class PhotoTextTab( stuffdb_tabbed_sub_window.StuffdbTab   ):

    def __init__(self, parent_window  ):
        """
        the usual
    CREATE TABLE photo_text (
                id          INTEGER PRIMARY KEY  UNIQUE NOT NULL,
                text_data   TEXT

        )

        """

        super().__init__()
        self.parent_window       = parent_window
        self.__build_gui()

        model                    = QSqlTableModel( self, AppGlobal.qsql_db_access.db )
        self.tab_model           = model # !! change everywhere
        model.setTable( parent_window.text_table_name )
        self.record_state   = self.RECORD_NULL


        print( f"on text tab {parent_window.text_table_name = }" )
        # print( "!! maybe do not want this select ")
        # model.select( )

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
    def default_new_row(self, key ):
        """
        what it says
            this is for a new row on the window -- no save
            needs key but timestamp photo from detail not text
        arg:
            next_key for table, just trow out if not used
        Returns:
            None.

        """
        self.clear_fields()

        self.text_data_field.setText( f"this is the default text for id { key = }" )

        # # ---- ??redef add_ts
        # a_ts   = str( time.time() ) + "sec"
        # # record.setValue( "add_ts",  a_ts    )
        # self.add_ts_field.setText(  a_ts )
        # self.edit_ts_field.setText( a_ts )

        self.id_field.setText( str( key ) )

    # ----------------------------
    def fetch_detail_row( self,  a_id = None ):
        """
        Args:
            id can be external or as chat has it fetched

        Returns:
            None.
        !! could be promoted
        """
        a_id      = self.id_field.text()
        print( f"photo text tab fetch_row { a_id = }")
        self.fetch_detail_row_by_id( a_id )



    # -----------------------------
    def delete_detail_row(self):
        """
        looks like could be promoted -- db key needs to stay id
              but need to delete detail_children as well
              but need to delete key words as well
        what it says read
         delete_detail_row delete_detail_row
        Returns:
            None.

        """
        model       = self.tab_model
        a_id          = self.id_field.text()
        if a_id:
            model.setFilter( f"a_id = {a_id}" )
            model.select()
            if model.rowCount() > 0:
                model.removeRow(0)
                model.submitAll()
                QMessageBox.information(self, "Delete Success", "detail_text_model Record deleted successfully.")
                self.clear_fields()
            else:
                msg   = "Delete Error: No record found with the given ID. { a_id = } "
                QMessageBox.warning(self, "Error",  msg )
                AppGlobal.logger.error( msg )
        else:
            msg  = f"Please enter a valid ID. { a_id = }"
            QMessageBox.warning(self, "Input Error", "Please enter a valid ID.")
            AppGlobal.logger.error( msg )
    # ------------------------
    def clear_fields(self):
        """
        what it says, read
        what fields, need a bunch of rename here
        clear_fields  clear_fields
        """
        self.id_field.clear()
        self.text_data_field.clear()
        # self.name_field.clear()
        # self.url_field.clear()
        # self.mypref_field.clear()
        # self.mygroup_field.clear()


    # ------------------------
    def field_to_record( self, record ):
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

        if self.record_state    == self.RECORD_NEW:  # may be needed
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
    def record_to_field(self, record ):
        """
        in photo may be promotable
        should be for fetch
        """
        if self.record_state    == self.RECORD_NEW:  # may be needed
            # self.record_id
            self.id_field.setText(  str( self.new_record_id     ) )


        self.id_field.setText(str(record.value( "id" )))
        #self.textField.setText(record.value("text_data"))
        self.text_data_field.setText(  record.value( "text_data"     ))

    # ---------------------
    def delete_record_update(self):
        """
        from russ crud  --- think ok in photo_text
        try in photo_detail

        """
        model    = self.tab_model
        if not self.record_state  == self.RECORD_DELETE:
            print( f"delete_record_update bad state, return  {self.record_state  = }")
            return
        id_value    = self.deleted_record_id
        if id_value:
            model.setFilter(f"id = {id_value}")
            model.select()
            if model.rowCount() > 0:
                model.removeRow(0)
                model.submitAll()
                self.clear_fields()  # will fix record state
                self.record_state       = self.RECORD_NULL
                QMessageBox.information(self, "Delete", "Record deleted!")
            model.setFilter( "" )


# ==================================
class PhotoPhotoTab( stuffdb_tabbed_sub_window.StuffdbTab   ):
    """
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

        print( "see chat_photo.py for more ... zoom to fit rectangle      chat_photo_3.py " )

    # -----------------------------
    def display_file( self,  file_name = "/mnt/WIN_D/PhotoDB/02/102-0255_img.jpg"  ):
        """
        what it says, read

        """
        # pixmap      = QPixmap( file_name )
        # self.viewer.set_photo( pixmap )
        self.viewer.display_file( file_name )
        self.fit_in_view()

    # ---- zooms, may also be in context map, may want buttons for these
    #          or delete
    #-------------------------------------
    def zoom_in(self):
        self.viewer.zoom_in()
        #rint("Zoomed In")

    #-------------------------------------
    def zoom_out(self):
        self.viewer.zoom_out()
        #rint("Zoomed Out")

    def reset_zoom(self):
        self.viewer.reset_zoom()
        #rint("Zoom Reset")

    #-------------------------------------
    def fit_in_view(self):
        self.viewer.fit_in_view()
        #rint("PhotoPhotoTab Fit in View")

# ---- eof ------------------------------
