#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

The point of this module is to manage the general aspects of
the multi document interface
It
    open documents
    provides menu items to tile, cascade... the documents
    allow navigation to documents base on their titles
    signals between components


so topics the list should be a dict, key a tuple  ( table_name, id )
add topic should be called on both fetch and save
keep one and only one up to date,  value should be record info still working out

typically in AppGlobal as:
    AppGlobal.mdi_management

"""

# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    main.main()
# --------------------

#from   functools import partial
import collections
import functools
import sys

from app_global import AppGlobal
from pubsub import pub
from PyQt5.QtCore import (QDate,
                          QModelIndex,
                          QObject,
                          Qt,
                          QTimer,
                          pyqtSignal,
                          pyqtSlot)
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
                             QTabWidget,
                             QTextEdit,
                             QVBoxLayout,
                             QWidget)

import adjust_path
import album_document
import base_document_tabs
import help_document
import mdi_info
import people_document
import picture_document
import plant_document
import planting_document
import stuff_document

# ---- imports


#import gui_qt_ext

MenuInfo   = collections.namedtuple( 'MenuInfo', "window, menu_item" )

#mdi_management
TopicData   = collections.namedtuple(   "TopicData", "table, id, topic" )
# WindowData  = collections.namedtuple(   "WindowData",
#                                        "menu_id, window_title" )  # maybe another dict ?/
# WindowData( menu_id = menu_it, window_title = title)

    # name is first argument  --- second arg space sep or a tuple

an_example   = MenuInfo( window  = "aaa", menu_item = "bbb",   )     # no quotes on instance names
print( an_example.window )
#print( an_example [ window ] )


#if type( i_doc ) == picture_document.PictureDocument:

NOT_FOR_SUBJECTS   = {  picture_document.PictureDocument, album_document.AlbumDocument,  }
# the above document should not be the subjects of pictures



#TOPIC_DELETED      = "topic_del"

# instead make document properties ??
# class document_info():
#     """
#     keep track of document, their id's some sort of identifier.....
#     plan now is to use for photo subjects
#     """
#     def __init__( self, window_id ):
#         """

#         """
#         self.window_id      = window_id
#         self.menu_action    = None
#         self.title          = None
#         self.


class SendSignals( QObject ):
    """
    my signals for db changes and document topics
    some for picture topics

    """
    topic_update_signal = pyqtSignal(str, int, str )

    def send_topic_update(self, table, table_id, info):
        print( "send_topic_update emit next")
        self.topic_update_signal.emit( table, table_id, info )

# -------------------------------
class MdiManagement():
    """
    manage the mdi interface.  Need to fix the dyslexia
    midma
    """
    def __init__( self, main_window ):
        self.main_window       = main_window
        #rint( f"hello from MidManagement {1}")
        #self.window_menu        = main_window.window_menu
        self.window_dict        = {}   # WindowData key is window id  ... or hide in a class
            # window dict --- perhaps should be document dict keeps a dict by id
            # of all registered document windows -- still in flux about what data to keep
            # note we also have
                # for sub_window in mdi_area.subWindowList():
                #     sub_window.resize( mdi_area_size )
            # keys:
            #     title
            #     table
            #     table_id
            #     info           description of the item for photo subjects
            #     "action_id"    this is the action on the menu, consider name change



        self.closed_topics   = []   # _list of dicts      a list of windows that are close but have had topics
        self._open_topics    = []
        # pub.unsubAll( TOPIC_UPDATE )
        self.send_signals    = SendSignals()

    # -------------------------
    def register_document( self,  window_id  ):
        """
        when a new window is created register
        keep a list, or dict.... for now a list
        !! in process sigh up for pubsub
        """
        #self.window_list.append( window_id )
        self.window_dict[ window_id ]     = { "title": window_id.windowTitle(),
                                              "action_id":  None }   # title action_id
        self.add_new_menu_item( window_id )

    # -------------------------
    def forget_document( self,  window_id  ):
        """
        when a new is to be forgotten, probably closed....
        keep a list, or dict.... for now a list
        !! unsubscribe
        """
        msg     = f"forget_document begin { window_id } !! update closed_topics "
        print( msg )
        self.remove_menu_item( window_id  )

        del self.window_dict[ window_id ]    # not sure still need window_dict
        # a_index   =  self.window_list.index( window_id )
        #self.window_dict[ window_id ]    =  WindowData( menu_id = None )
        # msg     = f"forget_document found window at index {a_index = }"
        # print( msg )

        # self.window_list.remove( window_id )

        # msg     = f"forget_document end {len(self.window_list) = }"
        # print( msg )

    # # -------------------------
    # def get_window_info_dict ( self,     ):
    #     """
    #     will get from each active window
    #     as a dict, perhaps could make a generator instead
    #     """
    #     for i_window, this_dict   in self.window_dict.items(   ):
    #         title       = i_window.windowTitle()
    #         this_dict
    #         topic     = None




        # a_index   =  self.window_list.index( window_id )
        #self.window_dict[ window_id ]    =  WindowData( menu_id = None )
        # msg     = f"forget_document found window at index {a_index = }"
        # print( msg )

        # self.window_list.remove( window_id )

        # msg     = f"forget_document end {len(self.window_list) = }"
        # print( msg )


    # --------------------------------------
    def cascade_documents( self, ):
        """
        what it says, read

        """
        mdi_area       = self.main_window.mdi_area
        mdi_area.cascadeSubWindows()
        # cascade_action = QAction("Cascade", self)
        # cascade_action.triggered.connect(self.mdi_area.cascadeSubWindows)
        # window_menu.addAction(cascade_action)

        # tile_action = QAction("Tile", self)
        # tile_action.triggered.connect(self.mdi_area.tileSubWindows)
        # window_menu.addAction(tile_action)

        # layer_action = QAction("Layer", self)
        # layer_action.triggered.connect(self.layer_sub_windows)
        # window_menu.addAction(layer_action)

    # --------------------------------------
    def tile_documents( self, ):
        """
        what it says, read
        """
        mdi_area       = self.main_window.mdi_area
        mdi_area.tileSubWindows()

    # ---------------------
    def layer_documents(self):
        """
        what it says, read

        """
        # from chat
        mdi_area        = self.main_window.mdi_area
        mdi_area_size   = mdi_area.size()
        for sub_window in mdi_area.subWindowList():
            sub_window.resize( mdi_area_size )
            sub_window.showNormal()
            # Ensure the sub-window is not maximized_area       = self.main_window.mdi_area

    # -------------------------------------
    def show_document( self, sub_window ):
        """
        what it says, read
        """
        sub_window.show()
        sub_window.setFocus()

    #----------------------------
    def update_menu_item(self, window_id ):
        """
        perhaps at end of select_by_id ish

        """
        action   = self.window_dict[ window_id ]["action_id"]
        action.setText( window_id.windowTitle()   )
                # getTitle setTitle
                # is a get for set self.setWindowTitle

    # --------------------------------------
    def remove_menu_item( self, window_id ):
        """
        from chat not so useful
        probably needs tweak to work in this context
        see self.add_new_menu_item
        """
        menu_id     = self.window_dict[window_id][ "action_id"]

        actions     = self.file_menu.actions()
        if actions:
            for i_action in actions:
                if menu_id == i_action:
                    #action_to_remove = actions[-1]  # Remove the last item added
                    self.file_menu.removeAction( menu_id )
                    QMessageBox.information(self, "Info", f"Removed item: {menu_id}")
        else:
            QMessageBox.information(self, "Info", "No items to remove")

    # --------------------------------------
    def add_new_menu_item( self,  window_id ):
        """
        what it says, read.... more coming maybe
        assumes this is a new window
        title is used for id, would be good to use an object ref

        """
        a_dict       = self.window_dict[ window_id ]
        title        = window_id.windowTitle()
        if not title:
            title    = str( type( window_id ))
        main_window                       = self.main_window
        #self.add_menu_item( title, main_window.window_menu )

        activate_window             = functools.partial( self.show_document, window_id )

        #show_sub_window_by_title( self, sub_window_title):

        action    = QAction( title, self.main_window )
        window_id.menu_action_id  = action
        a_dict[ "action_id" ]     = action    # probably phase out ??

        #action.triggered.connect( lambda: self.menu_item_clicked( title ) )
        action.triggered.connect( activate_window )
        main_window.window_menu.addAction( action )

    # -------------------------
    def get_album_doc(self, ):
        """
        what it says, read.... more coming maybe
        for now only one, return None if not found
        this is not quite right need to make sure one
        album is selected.

         self.window_dict[ window_id ]     = { "title": window_id.windowTitle(),
                                       "action_id":  None }   # title action_id
         AlbumDocument

        """
        album_docs    = []
        for i_doc in  self.window_dict.keys():
            if type( i_doc ) == album_document.AlbumDocument:
                album_docs.append( i_doc )
        if len( album_docs ) == 1:
            # should have a bit more testing here
            return album_docs[0]
        elif len( album_docs ) == 0:
            msg   = "You have no albums open, please open one"
        #elif len( album_docs ) == 0:
        else:
            msg     = "You have more than one album open, please close one."

        QMessageBox.information( AppGlobal.main_window,   "Info", msg )

        # # old version
        # album_docs    = []
        # for i_doc in self.window_list:
        #     if type( i_doc ) == picture_document.PictureDocument:
        #         album_docs.append( i_doc )
        # if len( album_docs ) == 1:
        #     # should have a bit more testing here
        #     return album_docs[0]
        # elif len( album_docs ) == 0:
        #     msg   = "You have no albums open, please open one"
        # #elif len( album_docs ) == 0:
        # else:
        #     msg     = "You have more than one album open, please close one."

        # QMessageBox.information( AppGlobal.main_window,   "Info", msg )

    # -------------------------
    def menu_item_clicked(self, name):
        """
        what it says, read.... more coming maybe

        """
        QMessageBox.information(self, "Info", f"You clicked on {name}")

    # -------------------------
    @property
    def open_topics( self,     ):
        """
        not clear now what this is for -- where used?  picture_document self.model_other
            subjects need a table_name  and perhaps the table_id but more importantly
            they need some info about the item ... like a stuff name
            lets try to add this at the document level with a function -- this seems to be document.topic


        what it says, read.... more coming maybe
        could do this more dynamically or make a generator
        note how it is a list of dicts  -- or not
        no need to be instance var
        does it need to be a dict, a list might do as well
        """
        print( "midi_management open_topics under test ...........................")

        topic_list           = []

        for i_window in self.main_window.mdi_area.subWindowList():
            if  i_window.detail_table_name not in [ "photo", "photoshow" ]:
                topic_dict                = {}

                topic_dict[ "window_id" ] = i_window
                topic_dict[ "table"]      = i_window.detail_table_name
                topic_dict[ "table_id"]   = i_window.detail_table_id
                #topic_dict[ "topic"]      = i_window.topic
                topic_dict[ "topic"]      = i_window.get_topic()
                topic_list.append( topic_dict )

            # key                 =  (  i_window.detail_table_name, i_window.detail_table_id )

            # #open_topics[ key ]  =   i_window.topic
            # open_topics[ key ]  =   "mdi_m broken in open_topics"
            # print( )

        print( f"{topic_list = }")
        return topic_list

    # # ----------------------------------
    # def send_topic_update( self, table, table_id, info):
    #     # Emit the signal when needed
    #     self.topic_update_signal.emit( table, table_id, info )


    # # ---------------------------------
    # def topic_update( self, table, table_id, info  ):
    #     """
    #     could just be the window id and we could get the rest
    #     send from mdi_management, but perhaps just as well from the window

    #     consider adding window_id

    #     """
    #     pub.sendMessage( TOPIC_UPDATE,  table = table, table_id = table_id, info = info   )

    # # ---------------------------------
    # def topic_delete( self, ):
    #     """
    #     send from mdi_management, but perhaps just as well from the window

    #      placeholder not implemented yet

    #     """
    #     #pub.sendMessage( TOPICS_DELETE, topic_dict = self.topic_dict,   )

    # -------------------------
    def show_mdi_info( self,     ):
        """
        what it says, read.... more coming maybe

        """
        print( "show_midi_info .....................................")

        for i_window in self.main_window.mdi_area.subWindowList():
            a_str     = ""
            a_str     = f"{a_str}\n{type( i_window ) = }"
            a_str     = f"{a_str}\n    {i_window.detail_table_id = }"
            a_str     = f"{a_str}\n    {i_window.detail_table_name  = }"
            a_str     = f"{a_str}\n    {i_window.menu_action_id = }"
            a_str     = f"{a_str}\n    {i_window.detail_table_id = }"

            a_str     = f"{a_str}\n    {i_window.topic  = }"
            a_str     = f"{a_str}\n    {i_window.record_state = }"
            rsn       = base_document_tabs.RECORD_STATE_DICT[ i_window.record_state ]
            a_str     = f"{a_str}\n    {rsn = }"
            is_for_subject    = type( i_window )  not in NOT_FOR_SUBJECTS
            a_str     = f"{a_str}\n    {is_for_subject = }"
            a_str     = f"{a_str}\n    {i_window.window_title = }"
            print( a_str )


        # dialog     = mdi_info.MdiInfo( topics   = self.topics   )
        # if dialog.exec_() == QDialog.Accepted:
        #     pass

    # -------------------------
    def make_document( self,  window_type ):
        """
        from chat_sub window.py
            then from document_maker which will be gone
        """
        msg              = f"add_subwindow for window_type {window_type }"
        # mdi_area       = self.main_window.mdi_area


        if    window_type == "help":
            sub_window      = help_document.HelpDocument()

        elif  window_type == "picture":
            sub_window      = picture_document.PictureDocument()

        elif  window_type == "album":
            sub_window      = album_document.AlbumDocument()

        elif  window_type == "stuff":
            sub_window      = stuff_document.StuffDocument()

        elif  window_type == "planting":
            sub_window      = planting_document.PlantingDocument()

        elif  window_type == "plant":
            sub_window      = plant_document.PlantDocument()

        # elif  window_type == "criteria":
        #     sub_window      = CriteriaSubWindow()


        elif  window_type == "people":
            sub_window      = people_document.PeopleDocument()


        else:
            1/0
            #sub_window      = CriteriaSubWind


# ---- eof
