#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""


# ---- tof
#import adjust_path
# --------------------
if __name__ == "__main__":
    import main
# --------------------

# ---- imports
import functools
import inspect
import logging
import pprint
import subprocess
import os
#from functools import partial
from pathlib import Path




from qt_compat import QApplication, QAction, exec_app, qt_version
from PyQt.QtWidgets import QMainWindow, QToolBar, QMessageBox
from qt_compat import Qt, DisplayRole, EditRole, CheckStateRole
from qt_compat import TextAlignmentRole



from PyQt.QtCore   import QDate, QModelIndex, Qt, QTimer, pyqtSlot
from PyQt.QtCore   import Qt, QDateTime
from PyQt.QtWidgets import QStyledItemDelegate
from PyQt.QtGui import (QFont,
                         QIntValidator,
                         QStandardItem,
                         QStandardItemModel,
                         QTextCursor)

from PyQt.QtSql import (QSqlDatabase,
                         QSqlQuery,
                         QSqlQueryModel,
                         QSqlRelation,
                         QSqlRelationalDelegate,
                         QSqlRelationalTableModel,
                         QSqlTableModel)

# next causing problems but not even used ?
# from PyQt.QtGui import ( QAction, QActionGroup, )   # role

from PyQt.QtWidgets import (
                             QFileDialog,
                             QApplication,
                             QButtonGroup,
                             QCheckBox,
                             QComboBox,
                             QDialog,
                             QDateEdit,
                             QDockWidget,
                             QFileDialog,
                             QFrame,
                             QGroupBox,
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
                             QSpacerItem,
                             QSpinBox,
                             QSizePolicy,
                             QTableView,
                             QTableWidget,
                             QTableWidgetItem,
                             QTabWidget,
                             QTextEdit,
                             QVBoxLayout,
                             QWidget)

import collections
import parameters
import data_dict
import check_fix

#import gui_qt_ext
import info_about
#import key_words
#import string_utils as string_util
#import text_edit_ext
#import table_model
import wat_inspector
from app_global     import AppGlobal
import qsql_utils
import geo_track
import photo_ext
#import ex_qt
#import exec_qt
#import mdi_management


# ---- import end

FIF             = info_about.INFO_ABOUT.find_info_for

EXEC_RUNNER     = None  # setup below
# MARKER              = ">snip"

# PERHAPS IN DATA DICT
# list
ALL_TABLES  = [
                    "help_info",
                    "help_key_word",
                    "help_text",
                    "people",
                    "people_key_word",
                    "people_phone", ""
                    "people_text",
                    "photo",
                    "photoshow",
                    "photoshow_key_word",
                    "photo_in_show",
                    "photo_in_show_text",
                    "photo_key_word",
                    "photo_text",
                    "plant",
                    "plant_text",
                    "plant_key_word",
                    "planting",
                    "planting_text",
                    "planting_event",
                    "planting_key_word",
                    "stuff",
                    "stuff_key_word",
                    "stuff_text",
                    "stuff_event",

                            ]
# dict   what is this
TABLE_DICT  = {
                         'photo_in_show': "photo_in_show_text",
                         'help_info': "help_text",
                         'stuff': "stuff_text",
                         'plant':       "plant_text",
                         'planting':    "planting_text",
                         'photoshow':   "photoshow_text",
                         'people': "people_text",
                         'photo': "photo_text",
                            }

KW_TABLE_DICT  = {
                         'help_info':  "help_key_word",
                         'stuff':       "stuff_key_word",
                         'plant':       "plant_key_word",
                         'planting':    "planting_key_word",
                         'photo':       "photo_key_word",
                         'photoshow':   "photoshow_key_word",
                         'people':      "people_key_word",
                            }

IKW_TABLE_DICT = {value: key for key, value in KW_TABLE_DICT.items()}

FileInfo        = collections.namedtuple( "FileInfo", "file_name path_name full_file_name" )

def  clean_path_part( path_part ):
    """
    consider add to some lib ??
    """

    # ---- crude but i hope effective
    if path_part:
        path_part    = path_part.replace( "\\", "/" )
    else:
        path_part    = ""

    path_part    = path_part.replace( "///", "/" )
    path_part    = path_part.replace( "//",  "/" )
    path_part    = path_part.removeprefix( "/" )
    path_part    = path_part.removesuffix( "/" )

    return path_part

# ------------------------------------
def open_file_dialog( parent, default_dir ):
    """
    What it says

    """


    dialog = QFileDialog(parent, "Select Files")

    # --- dialog options ---
    dialog.setFileMode(QFileDialog.ExistingFiles)     # multiple selection allowed
    dialog.setViewMode(QFileDialog.Detail)            # list vs detail view
    dialog.setOption(QFileDialog.DontUseNativeDialog, True)  # force Qt dialog
    dialog.setOption(QFileDialog.ReadOnly, False)     # allow editing file name
    dialog.setOption(QFileDialog.DontResolveSymlinks, False)
    dialog.setOption(QFileDialog.HideNameFilterDetails, False)

    # --- default directory ---
    #dialog.setDirectory("/mnt")  # change as needed
    dialog.setDirectory( default_dir )

    # --- filters ---
    dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp *.gif)")
    dialog.setNameFilters([
        "Images (*.png *.jpg *.jpeg *.bmp *.gif)",
        "Text files (*.txt *.md *.log)",
        "All files (*)"
    ])

    # --- default selected filter ---
    dialog.selectNameFilter("Images (*.png *.jpg *.jpeg *.bmp *.gif)")

    # --- default file suggestion ---
    dialog.selectFile("untitled.txt")

    # --- execute the dialog ---
    if dialog.exec_():
        selected_files = dialog.selectedFiles()
        return selected_files

    else:
        return []


class FileIterator:
    """expand later with dir depth and filters  """
    def __init__(self, directory):
        self.directory = directory
        self._files = os.listdir(directory)  # list of entries
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        while self._index < len(self._files):
            filename = self._files[self._index]
            self._index += 1
            full_path = os.path.join(self.directory, filename)
            if os.path.isfile(full_path):
                return full_path
        raise StopIteration



# ------------------------------------
def open_directory_dialog( parent, default_dir  ):
    """
    What it says

    """
    dialog = QFileDialog(parent, "Select a Directory")

    # --- dialog options ---
    dialog.setFileMode(QFileDialog.Directory)           # directory selection
    dialog.setOption(QFileDialog.ShowDirsOnly, True)    # show only directories
    dialog.setOption(QFileDialog.DontUseNativeDialog, True)  # force Qt dialog
    dialog.setOption(QFileDialog.ReadOnly, False)       # allow typing path manually
    dialog.setOption(QFileDialog.DontResolveSymlinks, False)

    # --- default start directory ---
    parent.picture_dir_default
    #dialog.setDirectory("/mnt")  # adjust as needed
    dialog.setDirectory( default_dir )

    # --- default directory suggestion ---
    dialog.selectFile("Photos")  # highlights/suggests this folder if exists

    # --- execute the dialog ---
    if dialog.exec_():
        selected_dirs = dialog.selectedFiles()  # list, usually one item
        # print("You selected:")
        # for i_dirs  in selected_dirs:

        #     self.append_msg( msg )
        return selected_dirs

    else:
        return []

# --------------------------------------
class ExploreArgs(   ):
    """
    used in path travisrse form process files
    args passed down recursive explore functions, treat as constants once set
    may want a copy for each thread and possibly accumulate data here

    also functions used for processing  .... perhaps a rename ??
    but some args are functions, here or in helper_thread ??
    kind of mess keep counters in app_state
    explore_args
    """
    #---------------------
    def __init__( self, max_dir_depth  ):
        """
        Usual init see class doc string
        explore_args.max_dir_depth
        """
        self.max_dir_depth    = max_dir_depth

# ----------------------------------------
class PhotoUtilSubWindow( QMdiSubWindow ):
    """
    db_management_subwindow.DbManagementSubWindow( )
    """
    def __init__(self, instance_ix = 0 ):
        """
        This is the parent for the document
        It holds our tabs
        when a document is created it registers itself with what mdi...?
        """
        super().__init__()

        self.subwindow_name     = "Photo Utilities and Test"

        self.instance_ix        = instance_ix

        mdi_area                = AppGlobal.main_window.mdi_area
            #we could return the subwindow for parent to add
        #sub_window              = self
            # sub_window.setWindowTitle( "this title may be replaced " )
        self.db                 = AppGlobal.qsql_db_access.db

        self.prior_tab          = 0
        self.current_tab        = 0
        self.detail_table_id    = None # for compatible with midi management

        # self.record_state
        self.current_tab_index      = 0       # assumed to be criteria

        self.tab_folder             = QTabWidget() # create for descendants

        # may want to keep at end of this init
        AppGlobal.mdi_management.register_document(  self )

        self.detail_table_name      = "xxx"  # need for framework do not delete
        # self.key_word_table_name    = "stuff_key_word"
        # self.text_table_name        = "stuff_text"  # text tables always id and text_data
            # used in text tab base
        self.help_filename          = "stuff_doc.txt"
        self.subwindow_name         = "Database Management"
        self.file_out = None
        self._build_gui()
        self.__init_2__()

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
        # main_notebook.currentChanged.connect( self.on_tab_changed )

        # ix                        = -1

        # ix                       += 1
        # self.criteria_tab_index   = ix
        # self.first_tab         = BasicsTab( self  )
        # main_notebook.addTab(       self.first_tab, "BasicsTab" )

        # self.first_tab         = KeyWordTab( self  )
        # main_notebook.addTab( self.first_tab, "Key Words" )

        # self.first_tab         = RecordMatchTab( self  )
        # main_notebook.addTab( self.first_tab, "RecordMatchTab" )

        self.first_tab         = PictureUtilTab( self  )
        main_notebook.addTab( self.first_tab, "PictureUtilTab" )

        tab                 = OutputTab( self  )
        self.output_tab     = tab
        main_notebook.addTab( tab, "Output" )

        self.output_edit    = tab.output_edit   # self.output_edit

        sub_window.setWidget( main_notebook )
        mdi_area.addSubWindow( sub_window )
        #      # perhaps add to register_document in midi_management

        sub_window.show()

    # --------------------------------
    def __init_2__( self ):
        """call at end of child __init__ """
        # !! perhaps in ancestor to a post innit
        title       = self.subwindow_name
        if self.instance_ix !=0:
            title  += f" {self.instance_ix}"

        self.setWindowTitle( title )
        AppGlobal.mdi_management.update_menu_item( self )
        self.set_size_pos()


    # --------------------------------
    def get_topic( self ):
        """
        for compat with midi manager
         'DbManagementSubWindow' object has no attribute 'get_topic'
        """
        return None


    # --------------------------------
    def set_size_pos( self ):
        """
        run after tab is added??
        """
        debug_msg = ( "set_size_pos--------------------------------------  " )
        logging.debug( debug_msg )

        # # --- works but window is hidden
        # self.showMaximized()
        # self.show()

        # ---- next partly works
        # this is a bit crude a kluge for now
        my_parameters       = AppGlobal.parameters
        qt_xpos             = my_parameters.doc_qt_xpos
        qt_ypos             = my_parameters.doc_qt_ypos
        qt_width            = my_parameters.doc_qt_width
        qt_height           = my_parameters.doc_qt_height

        self.setGeometry(  qt_xpos,
                           qt_ypos,
                           qt_width,
                           qt_height  )

    # --------------------------------
    def activate_output_tab( self,    ):
        """

        self.parent_window.activate_output_tab()
        """
        self.main_notebook.setCurrentWidget( self.output_tab  )

    # --------------------------------
    def output_msg( self, msg, clear = False  ):
        """
        dup with line_out
        """
        self.append_msg( msg, clear = clear  )

    # --------------------------------
    def output_to_file( self, msg ):
        """
        self.parent_window.output_to_file( msg )


        """
        self.file_out.write( msg + "\n" )
        print( msg )

    # --------------------------------
    def open_file_out( self, file_name = "data_management_out.txt" ):
        """

        """
        self.file_name_out   = parameters.PARAMETERS.output_dir + "/" + file_name
        self.file_out        = open( self.file_name_out,
                                    'w',
                                    encoding  = "utf8",
                                    errors    = 'ignore' )

        return self.file_name_out
    # --------------------------------
    def close_file_out( self,  ):
        """

        """
        if self.file_out:
            self.file_out.close()
        self.file_out = None

    #----------------------------
    def append_msg( self, msg, clear = False ):
        """
        read it --
            and print to console
        msg is just the name of the function
        """
        #msg     = f"----==== {msg} ====----"
        # if clear:
        #     self.clear_msg(  )
        if clear:
            self.output_edit.clear()
        self.output_edit.append( msg )


    #----------------------------
    def to_top_of_msg( self,   ):
        """
        read it --

        """
        text_edit   = self.output_edit
        cursor      = text_edit.textCursor()
        cursor.movePosition( cursor.Start )
        text_edit.setTextCursor(cursor)
        text_edit.ensureCursorVisible()


    #----------------------------
    def get_output_edit( self, ):
        """
        read it --

        may not need
        """
        return self.output_edit


    # --------------------------------
    def closeEvent(self, event):
        """
        may not be complete -- for example pending updates
        """
        AppGlobal.mdi_management.forget_document(  self )
        self.on_close()
        event.accept()

    # --------------------------------
    @pyqtSlot()
    def on_close( self ):
        """
        just debug for now
        """
        debug_msg  = (f"{self.windowTitle()} has been closed")
        logging.debug( debug_msg )

    # ------------------------------------------
    def system_rpt( self, ):
        """

        """



    # ------------------------------------------
    def doc_wat_inspect( self, ):
        """
        links to main menu bar for debug
        """
        debug_msg    = ( f"doc_inspect may want to add to  {self}")
        logging.debug( debug_msg )
        # make some locals for inspection
        self_detail_tab         = self.detail_tab
        self_text_tab           = self.text_tab
        self_detail_table_name  = self.detail_table_name
        # parent_window = self.parent( ).parent( ).parent().parent()

        todo = """
           """

        wat_inspector.go(
             msg            = "inspect !! more locals would be nice ",
             # inspect_me     = self.people_model,
             a_locals       = locals(),
             a_globals      = globals(), )

    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = "\n>>>>>>>>>>* DB Manatement   *<<<<<<<<<<<<"


        # a_str   = string_util.to_columns( a_str, ["criteria_tab_index",
        #                                    f"{self.criteria_tab_index}" ] )
        # a_str   = string_util.to_columns( a_str, ["current_id",
        #                                    f"{self.current_id}" ] )
        # a_str   = string_util.to_columns( a_str, ["current_tab_index",
        #                                    f"{self.current_tab_index}" ] )

        # a_str   = string_util.to_columns( a_str, ["detail_table_id",
        #                                    f"{self.detail_table_id}" ] )
        # a_str   = string_util.to_columns( a_str, ["detail_table_name",
        #                                    f"{self.detail_table_name}" ] )
        # a_str   = string_util.to_columns( a_str, ["history_tab",
        #                                    f"{self.history_tab}" ] )
        # a_str   = string_util.to_columns( a_str, ["list_tab",
        #                                    f"{self.list_tab}" ] )
        # # a_str   = string_util.to_columns( a_str, ["mapper",
        # #                                    f"{self.mapper}" ] )
        # a_str   = string_util.to_columns( a_str, ["menu_action_id",
        #                                    f"{self.menu_action_id}" ] )
        # a_str   = string_util.to_columns( a_str, ["picture_tab",
        #                                    f"{self.picture_tab}" ] )
        # a_str   = string_util.to_columns( a_str, ["subwindow_name",
        #                                    f"{self.subwindow_name}" ] )
        # a_str   = string_util.to_columns( a_str, ["tab_folder",
        #                                    f"{self.tab_folder}" ] )
        # a_str   = string_util.to_columns( a_str, ["text_tab",
        #                                     f"{self.text_tab}" ] )

        # b_str   = self.super().__str__( self )
        # a_str   = a_str + "\n" + b_str

        return a_str


# ----------------------------------------

# ----------------------------------------
class PictureUtilTab( QWidget ):
    """
    what it says

    maint and report on key word tables
    """
    def __init__(self, parent_window ):
        """

        """
        super().__init__()

        # self.criteria_dict          = {}
        # self.critera_widget_list    = []
        # self.critera_is_changed     = True
        self.parent_window          = parent_window
        self.key_words_widget       = None      # set to value in gui if used

        self.tab_name               = "PictureUtilTab"

        self.picture_dir_default    = "../"
        self.picture_dir_default    = AppGlobal.parameters.picture_browse

        self.picture_file_default    = "../"
        self.picture_file_default    = "/mnt/WIN_D/PhotoDB/25/DSCF0013.JPG"

        self.disptach_dict          = {}
        self.was_app                = geo_track.WasApp()
        self.photo_plus             = photo_ext.PhotoPlus()
        self.build_gui()

    # -----------------------------
    def build_gui( self,   ):
        """

        """
        vlayout              = QVBoxLayout( self )

        # ---- arguments
        #groupbox   = QGroupBox()  # no title
        groupbox   = QGroupBox( "Arguments ( see help for required args )" )   # version with title

        groupbox.setStyleSheet("""
            QGroupBox {
                border: 2px solid blue;
                border-radius: 10px;
                margin-top: 15px;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
                background-color: white;
            }
        """)

        # layout the groupbox and make
        # another layout inside it

        vlayout.addWidget( groupbox )

        self.build_gui_arguments( groupbox )

        # ---- actions
        groupbox   = QGroupBox( "Actions" )   # version with title

        groupbox.setStyleSheet("""
            QGroupBox {
                border: 2px solid blue;
                border-radius: 10px;
                margin-top: 15px;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
                background-color: white;
            }
        """)

        # layout the groupbox and make
        # another layout inside it

        vlayout.addWidget( groupbox )

        self.build_gui_actions( groupbox )


    def build_gui_arguments( self, groupbox ):
        """


        """
        layout     = QHBoxLayout( groupbox )

        # ---- set dir
        widget              = QPushButton( "Set Dir" )
        connect_to          = self.get_dir
        widget.clicked.connect( connect_to  )
        layout.addWidget( widget )

        widget              = QLineEdit( )
        self.dir_widget     = widget
        layout.addWidget( widget )

        # ---- set file
        widget              = QPushButton( "Set File" )
        connect_to          = self.get_file
        widget.clicked.connect( connect_to  )
        layout.addWidget( widget )

        widget              = QLineEdit( )
        self.file_widget     = widget
        layout.addWidget( widget )

    def build_gui_actions( self, groupbox ):
        """


        """
        layout              = QHBoxLayout( groupbox )

        # ---- table combobox
        widget              = QComboBox()

        self.go_widget      = widget
        # self.disptach_dict[ "find_dirs" ]                  = self.find_dirs
        # self.disptach_dict[ "pictures_not_in albums" ]     = self.find_dirs
        # self.disptach_dict[ "pictures missing dates" ]     = self.find_dirs
        # self.disptach_dict[ "find_file_missing" ]          = self.find_file_missing
        # self.disptach_dict[ "find_record_missing" ]        = self.find_record_missing
        # self.disptach_dict[ "clean_file_sub_dir" ]         = self.clean_file_sub_dir
        self.disptach_dict[ "get_geo_photo_data" ]               = self.get_geo_photo_data
        self.disptach_dict[ "make_file_list_debug" ]             = self.make_file_list_debug
        self.disptach_dict[ "is_dup_debug" ]                     = self.is_dup_debug

        a_list              = [key for key in self.disptach_dict.keys() ]

        widget.addItems( a_list )
        widget.setCurrentIndex( 0 )
        layout.addWidget( widget )

        # ---- buttons
        widget              = QPushButton( "Go" )
        connect_to          = self.go
        widget.clicked.connect( connect_to  )
        layout.addWidget( widget )

        widget              = QPushButton( "Help" )
        connect_to          = self.help
        widget.clicked.connect( connect_to  )
        layout.addWidget( widget )

    # -------------------------
    def help( self,   ):
        """
        What it says, read
            parse the args yourself
            use convention for about 1 hit
        """
        go_item      = self.go_widget.currentText()
        go_item      = go_item.replace( "_", " " )
        search_args = [ "stuffdbhelp", "pictureutiltab", go_item ]
        AppGlobal.mdi_management.stuffdb_help( search_args = search_args )

    # ---- reports
    # -------------------------
    def go( self,   ):
        """
        What it says, read
            better make dict based inc dropdown
        """
        go_item      = self.go_widget.currentText()
        self.disptach_dict[ go_item ]()




    def get_dir( self,   ):
        """ """
        dirs    = open_directory_dialog( self, self.picture_dir_default )
        if dirs:
            #file_name_path              = Path( files[0] )
            self.picture_dir_default   = dirs[0]

            self.dir_widget.setText( dirs[0] )

    def get_file( self,   ):
        """
        self.picture_file_default   = "../"
        self.picture_dir_default    = "../"

        """
        files    = open_file_dialog( self, self.picture_file_default )
        if files:
            file_name_path              = Path( files[0] )
            self.picture_file_default   = str( file_name_path.parent )
            msg              = ( f"setting {self.picture_file_default = }" )

            self.file_widget.setText( files[0] )

    # ---- go functions
    # -------------------------
    def is_dup_debug( self,   ):
        """
        What it says, read
        get the geo and photo data for a single file
        seems to work
        photo_util_subwindow.is_dup_debug
        """
        db                  = AppGlobal.qsql_db_access.db
        base_photo_dir      = parameters.PARAMETERS.picture_db_root

        dir_path_name       = self.dir_widget.text()
        dup_rows            = []
        #self.was_app.gpx_to_pp( file_name )
        file_list           = photo_ext.make_file_list( dir_path_name )

        print( "file_list follows")
        for ix_file, i_file_name in enumerate( file_list):
            msg    = (f"    {ix_file} {i_file_name}  ")
            print( msg )
            file_path           = Path( i_file_name )
            i_short_file_name   = file_path.name   # string
            long_file_name      = str( file_path.resolve() )

            """
            for the following table
            for table table_name = 'photo'
            CREATE TABLE  photo    (
                 id  INTEGER,
                 id_old  VARCHAR(15),
                 name  VARCHAR(150),
                 add_kw  VARCHAR(50),
                 descr  VARCHAR(240),
                 type  VARCHAR(15),
                 series  VARCHAR(15),
                 author  VARCHAR(35),
                 dt_enter  INTEGER,
                 format  VARCHAR(20),
                 inv_id  VARCHAR(15),
                 cmnt  VARCHAR(250),
                 status  VARCHAR(15),
                 dt_item  INTEGER,
                 c_name  VARCHAR(40),
                 title  VARCHAR(35),
                 tag  DECIMAL(50),
                 old_inv_id  VARCHAR(15),
                 file  VARCHAR(100),
                 sub_dir  VARCHAR(25),
                 photo_url  VARCHAR(75),
                 camera  VARCHAR(20),
                 lens  VARCHAR(20),
                 f_stop  DECIMAL(52),
                 shutter  INTEGER,
                 copyright  VARCHAR(50)
                )

                i would like to select the following fields
                id  INTEGER,
                 file  VARCHAR(100),
                 sub_dir  VARCHAR(25),

                 where file =  file_to_find

                 file to find is a python variable

                 for the program use python with sqllite and at5
                 use bind variables in the code avoid ? syntax
                    """
            # from PyQt.QtSql import QSqlDatabase, QSqlQuery
            # from PyQt.QtCore import QVariant


            # Create query with named bind variable
            query = QSqlQuery(db)
            query.prepare("""
                SELECT id, file, sub_dir
                FROM photo
                WHERE file = :file_name
            """)

            # Bind the variable using named parameter
            query.bindValue(':file_name', i_short_file_name )

            # Execute query
            if not query.exec_():
                print(f"Query error: {query.lastError().text()}")
                db.close()
                return []


            rows = []
            # ix_results  = 0
            while query.next():
                record = {
                    'id': query.value(0),
                    'file': query.value(1),
                    'sub_dir': query.value(2)
                }
                full_file           = f"{base_photo_dir}/{record['sub_dir']}/{record['file']}"
                full_file           = full_file.replace( "//", "/")
                record['full_file'] = full_file
                rows.append(record)
                print( f"found {record}")
            if len( rows ) > 0:
                # later insert original name
                dup_rows.append( rows )


        print( "listing of dup rows follows:" )
        for ix, i_item in enumerate( dup_rows ):
            if long_file_name  == full_file:
                print( "super duper" )
            msg     = f"    {ix}:{long_file_name}  in db: {i_item}"
            print( msg )

    # -------------------------
    def make_file_list_debug( self,   ):
        """
        What it says, read
        get the geo and photo data for a single file
        """
        db                  = AppGlobal.qsql_db_access.db
        dir_path_name       = self.dir_widget.text()



        #self.was_app.gpx_to_pp( file_name )
        file_list   = photo_ext.make_file_list( dir_path_name )

        print( "file_list follows")
        for ix_file, i_file_name in enumerate( file_list):
            msg    = (f"    {ix_file} {i_file_name}  ")
            print( msg )


        return


    # -------------------------
    def get_geo_photo_data( self,   ):
        """
        What it says, read
        get the geo and photo data for a single file
        """
        db                  = AppGlobal.qsql_db_access.db
        file_name           = self.file_widget.text()

        if not os.path.isfile( file_name ):
            1/0

        #self.was_app.gpx_to_pp( file_name )
        self.photo_plus.reset( file_name = file_name, )
        # this will get fast data
        # !! so why do we do this

        # msg    =  self.photo_plus.exif_string()
        # print( msg )

        a_dict  =  self.photo_plus.get_exif_dict_from_pil()
        print( "---------------exif_dict_from_pil")
        #print( a_dict )
        # but comes back as empty dict
        if a_dict is not None:
            for key, value in a_dict.items():
                msg    = (f"{key} {value}  {type(value)}")
                print( msg )
        else:
            msg    = (f"get_exif_dict_from_pil returned None")
            print( msg )

        a_dict  =  self.photo_plus.get_os_dict()
        print( "---------------get_os_dict")
        #print( a_dict )
        # but comes back as empty dict
        if a_dict is not None:
            for key, value in a_dict.items():
                msg    = (f"{key} {value}  {type(value)}")
                print( msg )
        else:
            msg    = (f"get_exif_dict_from_pil returned None")
            print( msg )

        # can use PhotoPlus and its instance variables

        return

        # ---- return above

        # --- run the query for unique sub_dir values ---
        query = QSqlQuery( db )
        sql = """
            SELECT DISTINCT sub_dir
            FROM photo
            WHERE sub_dir IS NOT NULL AND sub_dir <> ''
            ORDER BY sub_dir ASC
        """
        if not query.exec(sql):
            print("Query failed:", query.lastError().text())
            return

        # --- print results ---
        print("Unique sub_dir values (alphabetical):")
        while query.next():
            sub_dir = query.value(0)
            msg     = sub_dir
            #print(sub_dir)

            self.parent_window.output_msg(  msg )
        self.parent_window.activate_output_tab()



    # -------------------------
    def find_dirs( self,   ):
        """
        What it says, read

        """
        db                  = AppGlobal.qsql_db_access.db

        # --- run the query for unique sub_dir values ---
        query = QSqlQuery( db )
        sql = """
            SELECT DISTINCT sub_dir
            FROM photo
            WHERE sub_dir IS NOT NULL AND sub_dir <> ''
            ORDER BY sub_dir ASC
        """
        if not query.exec(sql):
            print("Query failed:", query.lastError().text())
            return

        # --- print results ---
        print("Unique sub_dir values (alphabetical):")
        while query.next():
            sub_dir = query.value(0)
            msg     = sub_dir
            #print(sub_dir)

            self.parent_window.output_msg(  msg )
        self.parent_window.activate_output_tab()


    # -------------------------
    def find_dup_filexx( self, path  ):
        """
        work through files in a path ( and descendants )
        and ouput possible duplicates for deletion


        """
        pass

    # -------------------------
    def clean_file_sub_dir( self,    ):

        """
        Loop through all records in the photo table, read file and sub_dir, modify them,
        and update the same record with the modified values.
        Returns:
            bool: True if all updates succeed, False if any error occurs.
        """
        # Query to select all records

        db                  = AppGlobal.qsql_db_access.db
        select_query        = QSqlQuery( db )
        select_query_str = """
            SELECT id, file, sub_dir
            FROM photo
        """

        if not select_query.exec_(select_query_str):
            print("Error executing select query:", select_query.lastError().text())
            return False

        # Prepare update query with named bind variables
        update_query = QSqlQuery( db )
        update_query_str = """
            UPDATE photo
            SET file = :new_file, sub_dir = :new_sub_dir
            WHERE id = :id
        """
        update_query.prepare(update_query_str)

        # Loop through records
        while select_query.next():
            record_id   = select_query.value(0)
            file        = select_query.value(1)
            sub_dir     = select_query.value(2)

            # ---- crude but i hope effective

            new_file       = clean_path_part( file )
            new_sub_dir    = clean_path_part( sub_dir )

            # ---- not good if new_file is blank or null
            msg      = f"{new_sub_dir}/{new_file}"
            #self.parent_window.output_msg( msg, )
            print( msg )

            # new_sub_dir = f"{sub_dir}_mod" if sub_dir else sub_dir

            # Bind values and execute update
            update_query.bindValue( ":new_file",     new_file)
            update_query.bindValue( ":new_sub_dir",  new_sub_dir)
            update_query.bindValue( ":id",           record_id)

            if not update_query.exec_():
                print(f"Error updating record id={record_id}:", update_query.lastError().text())
                return False

        return True

    # -------------------------
    def find_if_dupsxxx( self,   ):
        """
        work thru the files in a directory and see if already in db

        --- old
        #max_dir_depth 0 is unlimited
        self.parent_window.close_file_out( )
        ?? open output file on output window
        ?? do a lookup without the extension ??
        ?? enable delete but keep report

        """
        indent      = "    "
        file_out    = self.parent_window.open_file_out( "find_if_dups.txt" )
        db          = AppGlobal.qsql_db_access.db
        query       = QSqlQuery(db)
        sql         =   ( "SELECT id,  sub_dir, file  FROM photo "
                         " WHERE  file = :file_path_name " )

        # a_sub_dir   = full_dir.removeprefix( parameters.PARAMETERS.picture_db_root )
        starting_dir       = self.dir_widget.text()
        #msg    = f"Done find_if_dups {starting_dir = } {ix_file =}  "


        msg    = f"Start find_if_dups {starting_dir = }  "
        self.parent_window.output_to_file( msg )
        self.parent_window.output_msg(  msg, clear = True )

        ix_file            = -1 # in case no files
        a_file_itterator   = FileIterator( starting_dir )
        for ix_file, i_file_name in enumerate( a_file_itterator ):
            file_path      = Path( i_file_name )
            full_file_name = str( file_path.resolve() )
            file_path_name = file_path.name
            msg         = (f"checking {ix_file}  {full_file_name = }")
            self.parent_window.output_to_file( msg )

            if not query.prepare(sql):  # do we need to prep and bind ove and over
                msg     = ( f"Prepare failed: {query.lastError().text()}" )
                self.parent_window.output_to_file( msg )
                return

            query.bindValue(":file_path_name", file_path_name )

            if not query.exec_():
                msg     = ("Error executing query:" + query.lastError().text())
                self.parent_window.output_to_file( msg )

            ix_record_count  = 0
            while query.next():
                ix_record_count     += 1
                a_id                = query.value(0)
                sub_dir             = query.value(1)
                file                = query.value(2)

                msg         = (f"{indent} ---- found {ix_file} id={a_id}, sub_dir={sub_dir}, file={file} {ix_record_count = }")
                self.parent_window.output_to_file( msg )
                self.parent_window.output_msg(  msg )

            if ix_record_count == 0:
                msg         = (f"{indent} ++++ NOT FOUND {ix_file} {file_path_name = }")
                self.parent_window.output_to_file( msg )
                self.parent_window.output_msg(  msg )

        msg    = f"Done find_if_dups {starting_dir = } {ix_file =}  "
        self.parent_window.output_msg(  msg, ) #clear = True )
        self.parent_window.output_to_file( msg )

        self.parent_window.close_file_out( )
        self.parent_window.activate_output_tab()
        msg    = f"Now opeining output file for you {file_out}"
        self.parent_window.output_msg(  msg, ) #
        #AppGlobal.os_popen_file( file_out )  # what
        AppGlobal.os_open_txt_file( file_out )

    # -------------------------
    def find_file_missingxxx( self,   ):
        """
        work through records with file names and
        see if file exists, output is file name for records
        whenre that file is missing.
        self.parent_window.open_file_out( )
        starting_dir   = self.dir_widget.text()
        self.explore_dir( starting_dir, 0 , explore_args )

        #max_dir_depth 0 is unlimited
        self.parent_window.close_file_out( )

        """
        self.parent_window.open_file_out( )

        full_dir    = self.dir_widget.text()

        a_sub_dir   = full_dir.removeprefix( parameters.PARAMETERS.picture_db_root )

        db          = AppGlobal.qsql_db_access.db

        query       = QSqlQuery(db)

        sql = """
            SELECT id, sub_dir, file
            FROM photo
            WHERE sub_dir = :a_sub_dir
            ORDER BY id ASC
        """
        if not query.prepare(sql):
            msg     = ( f"Prepare failed: {query.lastError().text()}" )
            self.parent_window.output_to_file( msg )
            return

        query.bindValue(":a_sub_dir", a_sub_dir )

        # --- print results ---
        msg     =  (f"Files in sub_dir='{a_sub_dir}':")
        self.parent_window.output_to_file( msg )

        if not query.exec_():
            msg     = ("Error executing query:" + query.lastError().text())
            self.parent_window.output_to_file( msg )

            # msg      = query_str
            # self.parent_window.output_to_file( msg )

        ix_record_count  = 0
        while query.next():
            ix_record_count     += 1
            a_id                = query.value(0)
            sub_dir             = query.value(1)
            file                = query.value(2)

            msg         = (f"id={a_id}, sub_dir={sub_dir}, file={file} {ix_record_count = }")
            self.parent_window.output_msg(  msg )

            got_file    = self.find_file( sub_dir, file )

            if got_file:
                pass

            else:
                msg     = f"error no file found for {a_id}, file f{sub_dir}/{file}"
                self.parent_window.output_to_file( msg )

        # if   ix_record_count == 0:
        #     msg    = f"error no record found for file f{sub_dir}/{file}"
        #     self.parent_window.output_to_file( msg )

        # elif ix_record_count == 1:
        #     msg    = f"1 record found for file f{full_file_name} {base_path}"
        #     self.parent_window.output_to_file( msg )

        # else:
        #     msg    = f"errorish duplicate records found for file f{full_file_name} {base_path}"
        #     self.parent_window.output_to_file( msg )
        self.parent_window.close_file_out( )
        self.parent_window.activate_output_tab()


    # -------------------------
    def find_record_missingxx( self,   ):
        """
        work through files ( perhaps of a given directory )
        and see if they have 1 or more files
        output is the file names whre the record is missing.

        """
        explore_args   = ExploreArgs( max_dir_depth = 1 )
        self.parent_window.open_file_out( )
        starting_dir   = self.dir_widget.text()
        self.explore_dir( starting_dir, 0 , explore_args )

        #max_dir_depth 0 is unlimited
        self.parent_window.close_file_out( )

        msg     = (f"find_record_missing complete look for output file in {parameters.PARAMETERS.output_dir}")
        self.parent_window.output_msg(  msg )
        self.parent_window.activate_output_tab()

    # ---- support functions
    # ----------------------------------------------
    def explore_dir( self, starting_dir, dir_depth, explore_args  ):
        """
        set up to run process was for dups and keeps not part of this app
        recursive
        could collect files in a list and process as a batch at the end
        probably more efficient but for now one at a time

        explore and list files in dir and recursive to sub dirs
            starting_dir  = name of dir we start from
            dir_depth     = depth of starting_dir, 0 for initial call
            additional args   current depth
                           filter

        Args:
            starting_dir -- now a path or string ... may need bigger fix for now either !!

        """

        # starting_dir    = starting_dir.replace( "\\", "/" )    # normalize win/linux names
        new_dir_depth   = dir_depth + 1
        names           = os.listdir( starting_dir )  # may throw [WinError 3]

        msg             = f"exploring at depth {new_dir_depth}: {starting_dir}"
        # AppGlobal.logger.info( msg )
        # self.gui_write( msg + "\n" )
        self.parent_window.output_to_file( msg )

        for i_name in names:
            # file from / file to
            i_name        = i_name.replace( "\\", "/" )
            i_full_name   = os.path.join( starting_dir, i_name )
                ## ?? just default to / why not and remove next
            i_full_name   = i_full_name.replace( "\\", "/" )   # !! revise for path
            # next a named tuple
            i_file_info   = FileInfo( file_name         = i_name,
                                      path_name         = starting_dir,
                                      full_file_name    = i_full_name )

            # ---- for now no pause or cancel
            # could have pause here too #
            # if self.app_state.cancel_flag:
            #     msg = "user cancel"
            #     raise app_global.UserCancel( msg )

            # if self.app_state.pause_flag:
            #     time.sleep( self.parameters.ht_pause_sleep )

            # ---- is dir
            if os.path.isdir( i_full_name ):
                # msg     = ( f"os.path.isdir self.app_state.ix_explore_dir = "
                #             f"{self.app_state.ix_explore_dir} new_dir_depth = {new_dir_depth}"
                #             f"    explore_args.max_dir_depth = {explore_args.max_dir_depth}" )
                msg      = ( f"found sub dir {i_full_name}")
                self.parent_window.output_to_file( msg )


                if ( ( explore_args.max_dir_depth == 0  ) or
                     ( explore_args.max_dir_depth  >  new_dir_depth  ) ):
                         # may be more efficient placement of this so called once
                    #self.app_state.count_dir      += 1
                        # or one for file, one for dir, and one for error better ??
                    # if explore_args.df( i_full_name ):   # the filter for dir
                    #     msg     = f"making recursive call {i_full_name} {new_dir_depth}"
                    #     print( msg )
                    self.explore_dir( i_full_name, new_dir_depth, explore_args )
                    # else:
                    #     msg     = f"\nhit false on dir filter df  {i_full_name} "
                    #     print( msg )
                else:
                    msg         = f"\nhit max dir depth {i_full_name} {new_dir_depth} "
                    self.parent_window.output_to_file( msg )

                continue
            #import pdb; pdb.set_trace()
            # ---- is file
            # ==== we got a file not a dir
            file_size               = os.path.getsize(  i_full_name )
            base_path               = parameters.PARAMETERS.picture_db_root
            full_file_name          = i_full_name
            self.find_photo_by_full_file_name( base_path      = base_path,
                                               full_file_name = full_file_name )


    def find_file( self, sub_dir, file  ):
        """
        could be a file or a directory may want to make better
        assumes output file is open
        Find a record in the photo table where the concatenated sub_dir and file match the provided values.
        path = Path("/mnt/WIN_D/PhotoDB/14/dscn2802.jpg")

        if path.exists():
        """
        full_file_name    = f"{parameters.PARAMETERS.picture_db_root}{sub_dir}/{file}"
        path              = Path( full_file_name )

        is_found          = path.exists()

        msg  = ( f"find_file  >>{full_file_name}<< {is_found = }")
        self.parent_window.output_to_file( msg )

        return is_found


    def find_photo_by_full_file_name( self, *, base_path,  full_file_name ):
        """
        Find a record in the photo table where the concatenated BASE_PATH, sub_dir, and file match the provided values.
        Args:
            sub_dir (str): The subdirectory name.
            file_name (str): The file name.
        Returns:
            dict or None: A dictionary containing all fields of the matching record, or None if no match or error.
        """
        db                  = AppGlobal.qsql_db_access.db
        #BASE_PATH = "/photos/"  # Constant string for the base directory
        query = QSqlQuery( db)
        query_str = ( ""
            "SELECT id, "
            # " id_old, "
                   # name, add_kw, descr, type, series, author, dt_enter, format,
                   # inv_id, cmnt, status, dt_item, c_name, title, tag, old_inv_id,
                   " file, sub_dir "
                   # photo_url, camera, lens, f_stop, shutter, copyright
            " FROM photo "
            " WHERE :base_path || TRIM(sub_dir, '/' )  || '/' || file = :full_file_name "
            )

        query.prepare(query_str)
        #full_path = f"{sub_dir}/{file_name}"
        query.bindValue(":base_path",      base_path )
        query.bindValue(":full_file_name", full_file_name )

        if not query.exec_():
            msg     = ("Error executing query:" + query.lastError().text())
            self.parent_window.output_to_file( msg )

            msg      = query_str
            self.parent_window.output_to_file( msg )

            return None
        ix_record_count  = 0
        if query.next():
            ix_record_count  += 1
            record = {
                "id": query.value(0),
                # "id_old": query.value(1),
                # "name": query.value(2),
                # "add_kw": query.value(3),
                # "descr": query.value(4),
                # "type": query.value(5),
                # "series": query.value(6),
                # "author": query.value(7),
                # "dt_enter": query.value(8),
                # "format": query.value(9),
                # "inv_id": query.value(10),
                # "cmnt": query.value(11),
                # "status": query.value(12),
                # "dt_item": query.value(13),
                # "c_name": query.value(14),
                # "title": query.value(15),
                # "tag": query.value(16),
                # "old_inv_id": query.value(17),
                "file": query.value(1),
                "sub_dir": query.value(2)
                # "photo_url": query.value(20),
                # "camera": query.value(21),
                # "lens": query.value(22),
                # "f_stop": query.value(23),
                # "shutter": query.value(24),
                # "copyright": query.value(25)
            }
            msg    = str( record )
            self.parent_window.output_to_file( msg )

        if   ix_record_count == 0:
            msg    = f"error no record found for file f{full_file_name} {base_path}"
            self.parent_window.output_to_file( msg )

        elif ix_record_count == 1:
            msg    = f"1 record found for file f{full_file_name} {base_path}"
            self.parent_window.output_to_file( msg )

        else:
            msg    = f"errorish duplicate records found for file f{full_file_name} {base_path}"
            self.parent_window.output_to_file( msg )
        return

# ----------------------------------------
class OutputTab( QWidget ):
    """
    what it says


    """
    def __init__(self, parent_window ):
        """

        """
        super().__init__()

        self.parent_window          = parent_window

        self.tab_name               = "Output"
        self.build_gui()

    # -----------------------------
    def build_gui( self,   ):
        """

        """
        vlayout              = QVBoxLayout( self )

        self._build_gui_bot( vlayout )

        # # ---- new row
        # layout              = QHBoxLayout( self )
        # vlayout.addLayout( layout )

        # # ---- table combobox
        # widget              = QComboBox()

        # self.table_widget   = widget

        # a_list              = [
        #                  'help_key_word',
        #                  'stuff_key_word',
        #                  'plant_key_word',
        #                  'people_key_word' ]

        # widget.addItems( a_list )
        # widget.setCurrentIndex( 0 )
        # layout.addWidget( widget )


        # widget              = QPushButton( "key_word_dups" )
        # self.q_pbutton_1    = widget
        # connect_to          = self.key_word_dups
        # widget.clicked.connect(  connect_to   )
        # layout.addWidget( widget )

        # widget              = QPushButton( "!!rebuild_key_words" )
        # # connect_to          = self.record_count_rpt
        # # widget.clicked.connect( connect_to  )
        # layout.addWidget( widget )

        # # ---- new row
        # layout              = QHBoxLayout( self )
        # vlayout.addLayout( layout )

        # widget              = QPushButton( "!!" )
        # # connect_to          = self.system_sub_count_rpt
        # # widget.clicked.connect( connect_to  )
        # layout.addWidget( widget )


    # -------------------------------
    def _build_gui_bot(self, layout  ):
        """
        make the bottom of the gui, mostly the large
        message widget
        layouts
            a vbox for main layout
        """
        # ---- new row
        row_layout      = QHBoxLayout(   )
        layout.addLayout( row_layout,  )

        # ----
        widget              = QTextEdit("load\nthis should be new row ")
        self.msg_widget     = widget
        #widget.clicked.connect( self.load    )
        row_layout.addWidget( widget,   )
        self.output_edit    = widget


    # -------------------------

    # ---- reports
    # -------------------------

    # -------------------------
    def system_sub_count_rpt( self,   ):
        """
        What it says, read

        """



    # ---- Actions none yet


    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = "\n>>>>>>>>>>* xxxxxx *<<<<<<<<<<<<"

        return a_str


def test_clean_path_part(   ):




    path_parts     = [
                        "",
                        None,
                        r"//a_sub_dir\\\\",
                        r"//asub//dir///",
                        r"//asub//dir\\more_dir///",
                        # "/one/tow//three//",
                        # "",
                        # "",
                        # "",
                        # "",
                        # "",
                        ]
    for i_path_part in path_parts:
        path_part    = i_path_part
        clean_part   = clean_path_part( path_part )
        print( f">{path_part}<>{clean_part}<")

# just for prelim test
# if __name__ == "__main__":
#     test_clean_path_part()

# ---- eof