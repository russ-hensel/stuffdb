#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
import  slideshow_subwindow
# or a document, not really not in db ....



"""


# ---- tof

# --------------------
if __name__ == "__main__":
    import main    # noqa  stops auto removal by pycln
    pass
# --------------------

# ---- imports
from   functools import partial
import table_model
#import inspect
import logging
#import pprint
import traceback
import os
import time

#from functools import partial
from pathlib import Path


from qtpy.QtCore   import ( Slot,
                           QSortFilterProxyModel,
                           QModelIndex,
                           )


from qtpy.QtSql import ( QSqlQuery )

#from PyQt.QtGui import ( QAction, QActionGroup, )

from qtpy.QtGui import QTextCursor

from qtpy.QtWidgets import (
                             QApplication,
                             QFileDialog,
                             QComboBox,
                             QGroupBox,
                             QHBoxLayout,
                             QLabel,
                             QLineEdit,
                             QMdiSubWindow,
                             QTableView,
                             QMessageBox,
                             QPushButton,
                             QSpacerItem,
                             QSizePolicy,
                             QTabWidget,
                             QTextEdit,
                             QVBoxLayout,
                             QWidget
                             )

# ---- local imports

import collections
import parameters

import file_utils
import string_utils
import base_document_tabs

import picture_viewer
import info_about
import photo_website
import random_index
import wat_inspector
from   app_global     import AppGlobal


# ---- import end

FIF             = info_about.INFO_ABOUT.find_info_for

EXEC_RUNNER     = None  # setup below
# MARKER              = ">snip"

# PERHAPS IN DATA DICT
# list


# ----------------------------------------
class SlideShowSubWindow( QMdiSubWindow ):
    """
    db_management_subwindow.SlideShowSubWindow( )
    """
    def __init__(self, instance_ix = 0 ):
        """
        This is the parent for the document
        It holds our tabs
        when a document is created it registers itself with what mdi...?
        """
        super().__init__()

        self.subwindow_name     = "SlideShow"

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

        self.file_out = None
        self._build_gui()
        self.__init_2__()

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says
            main notebook and tabs
        """
        main_notebook           = self.tab_folder   # create in parent
        self.main_notebook      = main_notebook

        sub_window              = self
        mdi_area                = AppGlobal.main_window.mdi_area
        # main_notebook.currentChanged.connect( self.on_tab_changed )

        a_tab                   = SetupTab( self  )
        main_notebook.addTab( a_tab, "Setup" )
        self.setup_tab          = a_tab

        a_tab       = PictureTab( self  )
        main_notebook.addTab( a_tab, "Pictures" )
        self.picture_tab          = a_tab

        # a_tab       = RecordMatchTab( self  )
        # main_notebook.addTab( a_tab, "RecordMatchTab" )

        a_tab                   = OutputTab( self  )
        self.output_tab         = a_tab
        main_notebook.addTab( a_tab, "Output" )

        self.output_edit        = a_tab.output_edit

        sub_window.setWidget( main_notebook )
        mdi_area.addSubWindow( sub_window )
             # perhaps add to register_document in midi_management

        sub_window.show()

    # --------------------------------
    def __init_2__( self ):
        """
        call at end of child __init__
        """
        # !! perhaps in ancestor to a post innit
        title       = self.subwindow_name
        if self.instance_ix !=0:
            title  += f" {self.instance_ix}"

        self.setWindowTitle( title )
        # AppGlobal.mdi_management.update_menu_item( self )
        #self.set_size_pos()

    # --------------------------------
    def get_topic( self ):
        """
        for compat with midi manager
         'SlideShowSubWindow' object has no attribute 'get_topic'
        """
        return None

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
        print( msg )

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
        what it says, read.
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
    @Slot()
    def on_close( self ):
        """
        just debug for now
        """
        debug_msg  = (f"{self.windowTitle()} has been closed")
        logging.debug( debug_msg )

    # ------------------------------------------
    def add_album( self, row_dict  ):
        """
        links
        row_dict -- see caller and callee
        """
        # debug_msg = ( "SlideShowSubWindow  add_album probably comes from a album_document  ")
        # logging.debug( debug_msg )

        self.setup_tab.add_album( row_dict )

    # ------------------------------------------
    def doc_wat_inspect( self, ):
        """
        links to main menu bar for debug
        """
        debug_msg    = ( f"doc_inspect may want to add to  {self}" )
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

    #-------------------------- import string_utils
    def __str__( self ):
        """
        universal __str__
        """
        return string_utils.obj_to_str( self )

# ----------------------------------------
class SetupTab( QWidget ):
    """
    what it says
    """
    def __init__(self, parent_window ):
        """
        self.model
        """
        super().__init__()

        self.parent_window          = parent_window
        self.key_words_widget       = None      # set to value in gui if used

        self.tab_name               = "SetupTab"
        self.build_gui()

    # -----------------------------
    def build_gui( self,   ):
        """

        """
        main_layout         = QHBoxLayout( self )

        layout              = QVBoxLayout(  )  # all but model
        main_layout.addLayout( layout )


        # ---- Run
        widget              = QPushButton( "Run" )
        connect_to          = self.run
        widget.clicked.connect(  connect_to   )
        layout.addWidget( widget )


        widget              = QLabel( "Delay ( sec ):" )
        layout.addWidget( widget )

        widget              = QLineEdit( "..." )
        self.delay_widget   = widget

        layout.addWidget( widget )

        # ----  "Sequence:"
        widget              = QLabel( "Sequence:" )
        layout.addWidget( widget )

        widget              = QComboBox()
        self.seq_widget     = widget
        values              =  [ "In Sequence", "Random", "Rand. Adv."   ]
        widget.addItems( values )
        widget.setCurrentIndex( 0 )
        widget.setMinimumWidth( 200 )
        layout.addWidget( widget )


        # ---- "Make Website"
        widget              = QPushButton( "Make Website" )
        connect_to          = self.make_website
        widget.clicked.connect(  connect_to   )
        layout.addWidget( widget )

        widget              = QPushButton( "move_up" )
        connect_to          = self.delete_row
        #widget.clicked.connect(  connect_to   )
        layout.addWidget( widget )

        widget              = QPushButton( "move_dwn" )
        connect_to          = self.delete_row
        #widget.clicked.connect(  connect_to   )
        layout.addWidget( widget )

        widget              = QPushButton( "delete_row" )
        connect_to          = self.delete_row
        widget.clicked.connect(  connect_to   )
        layout.addWidget( widget )


        # ---- model and headers
        headers = [ "File Name", "Date", "What" ] # search width

        self.model          = table_model.TableModel( headers )

        # Proxy model for sorting
        proxy_model         = QSortFilterProxyModel()
        proxy_model.setSourceModel( self.model )
        self.proxy_model    = proxy_model

        # ---- table view
        table_view          = QTableView()
        self.table_view     = table_view

        # ---- timedateformatting
        date_column         = 1
        delegate            = base_document_tabs.TableModelDateTimeDelegate(
                                     date_column = date_column,
                                     parent = self  )
        table_view.setItemDelegateForColumn( date_column, delegate )

        #table_view.clicked.connect( self.on_row_clicked )
        # table_view.setModel( self.model )
        table_view.setModel( proxy_model )  # table_model for no sorting

        table_view.setSelectionBehavior( QTableView.SelectRows )

        table_view.setSortingEnabled( True )
            # Enables sorting by clicking column headers may need QSort....

        # ---- new layout
        layout              = QHBoxLayout(  )  # all but model
        main_layout.addLayout( layout )

        layout.addWidget( table_view )

        return

    #------------------------------------------
    def delete_row( self, ):
        """


        """
        # table_name      = "table_name"
        # table_id        = "table_id"
        # topic           = "topic"

        # row_data            = [ table_name, table_id, topic ]
        # self.model.add_or_update_row( row_data )

        model           = self.model
        view            = self.table_view

        row             = -1
        # Assuming `view` is your QTableView
        selection_model = view.selectionModel()
        if selection_model:
            selected_indexes = selection_model.selectedRows()

            # will get the first selected
            for index in selected_indexes:
                row = index.row()
                #print(f"delete_row Selected row: {row = }")
                break   # only get one

        if row == -1:
            # print( "delete_row no selected row")
            return

        self.model.removeRow( row )

    # #------------------------------------------
    # def add_row( self, ):
    #     """
    #     probably defunct see add_album

    #     """
    #     table_name      = "table_name"
    #     table_id        = "table_id"
    #     topic           = "topic"

    #     row_data            = [ table_name, table_id, topic ]
    #     #self.model.add_or_update_row( row_data )
    #     self.model.addRow( row_data )

    # ------------------------------------------
    def add_album( self, row_dict):
        """
        links
        row_dict -- see caller and callee  -- started at album_document?
        """
        # debug_msg = ( "SetupTab  add_album ")
        # logging.debug( debug_msg )

        row_data     = [ row_dict[ "album_id" ], row_dict[ "album_id" ],   row_dict[ "album_name" ],  ]
        self.model.addRow( row_data)

    # ------------------------------------------
    def run( self,    ):
        """

        """
        photo_list      = self._build_photo_list()

        # ?? maybe move this stuff there
        parent_window    =  self.parent_window

        parent_window.main_notebook.setCurrentWidget( parent_window.picture_tab  )

        QApplication.processEvents()
        parameters          = AppGlobal.parameters

        try:
            delay     = float( self.delay_widget.text() )

        except:
            delay     = parameters.picture_sleep

        seq_type      = self.seq_widget.currentText( )


        parent_window.picture_tab.run( photo_list, seq_type, delay )

    # ------------------------------------------
    def _build_photo_list( self, ):
        """
        Iterate the SetupTab table and build a flat list of photo dicts,
        one entry per photo in every album that has been added.

        Side-effect: also stashes the list on self.photo_list, matching
        what run() used to do inline.

        Shared by run() (slideshow) and make_website() (static gallery).
        """
        photo_list      = []
        self.photo_list = photo_list

        model           = self.model

        for row in range( model.rowCount( QModelIndex() ) ):
            album_id    = model.data( model.index( row, 0 ) )
            self.add_photo_for_id( album_id, photo_list )

        return photo_list

    # ------------------------------------------
    def make_website( self, ):
        """
        Build a static HTML photo gallery from every photo in every album
        that has been added to the SetupTab table, then open index.html in
        the user's default browser.

        Output goes to
            <AppGlobal.parameters.output_dir>/website_album_<first_id>/

        Rebuilds wipe and recreate that directory in full.
        """
        import webbrowser

        parent_window   = self.parent_window
        photo_list      = self._build_photo_list()

        if not photo_list:
            msg = "make_website: no photos in any selected album -- nothing to do"
            logging.warning( msg )
            parent_window.output_msg( msg, clear = True )
            parent_window.activate_output_tab()
            return

        # ---- derive directory name + title from the album table ----
        model           = self.model
        n_albums        = model.rowCount( QModelIndex() )
        first_id        = model.data( model.index( 0, 0 ) )
        first_name      = model.data( model.index( 0, 2 ) ) or "Photos"

        if n_albums == 1:
            title       = str( first_name )
        else:
            title       = f"{first_name} (+{n_albums - 1} more)"

        output_root     = AppGlobal.parameters.output_dir
        picture_root    = AppGlobal.parameters.picture_db_root
        site_dir        = f"{output_root}/website_album_{first_id}"

        msg = f"make_website: building site for {len( photo_list )} photos -> {site_dir}"
        logging.info( msg )
        parent_window.output_msg( msg, clear = True )
        parent_window.activate_output_tab()
        QApplication.processEvents()

        site            = photo_website.PhotoWebsite(
            photo_list      = photo_list,
            output_dir      = site_dir,
            picture_root    = picture_root,
            title           = title, )
        site.build()

        msg = f"make_website: wrote {site.index_path}"
        logging.info( msg )
        parent_window.output_msg( msg )

        webbrowser.open( site.index_path.as_uri() )


    # ------------------------------------------
    def add_photo_for_id( self, album_id, photo_list ):
        """
        this way does not reuse the query  .... refactor ??
        mutates photo_list
        """
        db      = AppGlobal.qsql_db_access.db
        sql     = ( "SELECT photo.id, photo.file, photo.sub_dir,  "
                    " photo.name,  photo.exif_ts, photo.exif_lat, photo.exif_lon, photo.exif_make, photo.exif_model "
                    " FROM photo "
                    " JOIN photo_in_show ON photo_in_show.photo_id = photo.id "
                    " WHERE photo_in_show.photo_show_id = :album_id "  )

        query = QSqlQuery( db )
        query.prepare( sql )
        query.bindValue( ":album_id", album_id )

        if not query.exec_():  # Check if execution failed
            msg = ( f"query_print_tab Error executing query:  {query.lastError().text()}" )
            logging.error(msg)

        while query.next():
            photo_id        = query.value(0)
            photo_file      = query.value(1)
            photo_sub_dir   = query.value(2)
            photo_name      = query.value(3)
            photo_dict      =  {
                                    "photo_id":        photo_id,
                                    "photo_file":      photo_file,
                                    "photo_sub_dir":   photo_sub_dir,
                                    "photo_name":      photo_name,
                                    }
                        # change to tuple for efficency ??

            #rint( f"ID: {photo_id},  {photo_id = },   {photo_name = }")
            photo_list.append( photo_dict )

    # -----------------------------------
    def __str__( self ):
        """
        universal __str__
        """
        return string_utils.obj_to_str( self )

# ----------------------------------------
class PictureTab( QWidget ):
    """
    what it says
    """
    def __init__(self, parent_window ):
        """
        self.model
        """
        super().__init__()

        self.parent_window          = parent_window
        self.key_words_widget       = None      # set to value in gui if used
        self.continue_flag          = True
        self.tab_name               = "SetupTab"
        self.build_gui()

    # -----------------------------
    def build_gui( self,   ):
        """

        """
        main_layout         = QHBoxLayout( self )

        layout              = QVBoxLayout(  )
        main_layout.addLayout( layout )

        widget              = QLabel( "photo_name" )
        self.name_widget    = widget
        widget.setMinimumSize(  100, 50 )
        widget.setMaximumWidth( 300 )
        widget.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Fixed )
        #connect_to          = self.add_row
        #widget.clicked.connect(  connect_to   )
        layout.addWidget( widget )

        # widget              = QLabel( "photo_date" )
        # self.date_widget    = widget
        # layout.addWidget( widget )

        widget              = QPushButton( "Pause" )
        self.pause_widget   = widget
        widget.clicked.connect(  self.pause   )
        layout.addWidget( widget )

        widget              = QPushButton( "Stop" )
        widget.clicked.connect(  self.stop   )
        self.stop_widget    = widget
        layout.addWidget( widget )

        #------------------------------
        layout              = QVBoxLayout(  )
        main_layout.addLayout( layout )

        # ---- picture viewer
        widget                  = picture_viewer.PictureViewer( self )
        self.picture_viewer     = widget
        layout.addWidget( widget )

        # # ---- model and headers
        # headers = [ "File Name", "Date", "What" ] # search width

        # self.model          = table_model.TableModel( headers )

    # -----------------------------
    def stop( self, ):
        """
        what it says, read
        """
        self.continue_flag  = False

    # -----------------------------
    def pause( self, ):
        """
        what it says, read
        """
        self.pause_flag     = not self.pause_flag
        text                = "Pause"

        if   self.pause_flag:
            text            = "Continue"
        # change the button
        self.pause_widget.setText( text )

    # -----------------------------
    def run( self, photo_list, seq_type, delay ):
        """
        what it says, read
        """
        # for i_photo in photo_list:
        #     print( i_photo )

        self.show_pictures(  photo_list, seq_type, delay )

     # ----------------------------------------------
    def show_pictures( self, photo_list, seq_type, delay ):
        """
        what it says, read,
        call from ht through queue
        * note early return
        """
        self.pause_flag     = False
        self.continue_flag  = True
        parameters          = AppGlobal.parameters
        picture_root        = parameters.picture_db_root

        if len( photo_list ) == 0:
            msg         = f"No Display as it appears you have not read a list?\n"
            print( msg )
            #self.gui_write( msg )
            return
 #[ "In Sequence", "Random", "Rand. Adv."   ]
        if   seq_type  ==  "In Sequence":
            pass
            seq_clas    =  random_index.SequentialIndex

        elif seq_type  ==  "Random":
            pass
            seq_clas    =  random_index.PureRandomIndex

        else:
            seq_clas    =  random_index.SlightlyRandomIndex

        # change to local
        self.seq_gen     = seq_clas(
                                    len( photo_list ),
                                    width      = parameters.picture_ran_width,
                                    bias       = parameters.picture_ran_bias )

        while  self.continue_flag:

                ix                  = self.seq_gen.get_next()
                i_photo             = photo_list[ ix ]

                # msg                 = f"show_pictures  {i_photo} at index {ix}\n"
                # print( msg )
                #self.gui_write( msg )

                full_file_name      = picture_root + "/" + i_photo[ "photo_sub_dir" ] +  "/" + i_photo[ "photo_file" ]
                full_file_name      = file_utils.fewer_slashes( full_file_name )
                self.picture_viewer.display_file( full_file_name )
                self.name_widget.setText( i_photo[ "photo_name" ] )
                self.name_widget.setText( i_photo[ "photo_name" ] )


                time_continue       = time.time() + delay
                while time.time()  < time_continue:
                    # are 4 better than 1?
                    QApplication.processEvents()
                    QApplication.processEvents()
                    QApplication.processEvents()
                    QApplication.processEvents()

                while self.pause_flag: # combine with above ?
                    QApplication.processEvents()
                    QApplication.processEvents()
                    QApplication.processEvents()
                    QApplication.processEvents()


# ----------------------------------------
class OutputTab( QWidget ):
    """
    what it says
        for messages, debug, not much use here
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

    # -------------------------------
    def _build_gui_bot( self, layout  ):
        """
        make the bottom of the gui, mostly the large
        message widget
        layouts
            a vbox for main layout
        """
        # ---- new row
        row_layout      = QHBoxLayout(   )
        layout.addLayout( row_layout, )

        widget          = QPushButton( "Top" )
        #connect_to             = self.pb_1_clicked
        widget.clicked.connect( self.top )
        row_layout.addWidget( widget )

        widget          = QPushButton( "Bottom" )
        # connect_to             = self.pb_1_clicked
        widget.clicked.connect( self.bot )
        row_layout.addWidget( widget )

        # ---- new row
        row_layout      = QHBoxLayout(   )
        layout.addLayout( row_layout, )

        # ----
        widget          = QTextEdit("load\nthis should be new row ")
        self.msg_widget = widget
        #widget.clicked.connect( self.load    )
        row_layout.addWidget( widget, )
        self.output_edit    = widget

    # ---- Actions
    # -----------------------
    def top( self, ):
        """ """
        widget      = self.msg_widget
        cursor      = widget.textCursor()
        cursor.movePosition(QTextCursor.Start)     # or QTextCursor.MoveAnchor mode is default
        widget.setTextCursor(cursor)
        widget.ensureCursorVisible()

    # -----------------------
    def bot( self, ):
        """ """
        widget      = self.msg_widget


        widget.moveCursor(QTextCursor.End)
        widget.ensureCursorVisible()

        # cursor      = widget.textCursor()
        # cursor.movePosition(QTextCursor.Start)     # or QTextCursor.MoveAnchor mode is default
        # widget.setTextCursor(cursor)
        # widget.ensureCursorVisible()

    # -----------------------------------
    def __str__( self ):
        """
        universal __str__
        """
        return string_utils.obj_to_str( self )


# def test_clean_path_part(   ):


#     path_parts     = [
#                         "",
#                         None,
#                         r"//a_sub_dir\\\\",
#                         r"//asub//dir///",
#                         r"//asub//dir\\more_dir///",
#                         # "/one/tow//three//",
#                         # "",
#                         # "",
#                         # "",
#                         # "",
#                         # "",
#                         ]
#     for i_path_part in path_parts:
#         path_part    = i_path_part
#         clean_part   = clean_path_part( path_part )
#         print( f">{path_part}<>{clean_part}<")

# # just for prelim test
# # if __name__ == "__main__":
# #     test_clean_path_part()

# ---- eof


