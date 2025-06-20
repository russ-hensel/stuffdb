#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
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

# ---- imports

#from   functools import partial
import collections
import functools
import logging
import sys

from app_global import AppGlobal

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

# !! think we just use the document so shorten see main_window
import album_document
import help_document
import people_document
import picture_document
import plant_document
import planting_document
import stuff_document
import db_management_subwindow  # db_management_subwindow.DbManagementSubWindow( )

import string_util

from collections import defaultdict

# Create a defaultdict with int as default_factory (defaults to 0)
counter = defaultdict(int)
# ---- imports end

logger          = logging.getLogger( )
#for custom logging level at module
LOG_LEVEL  = 20   # higher is more


# ---- dict constants
SEARCH_COMMAND_DICT                     = defaultdict( lambda: None )
SEARCH_COMMAND_DICT["search_help"   ]   = help_document.HelpDocument
SEARCH_COMMAND_DICT["search_stuff"  ]   = stuff_document.StuffDocument
SEARCH_COMMAND_DICT["search_pics"   ]   = picture_document.PictureDocument

# !! perhaps change to default
SEARCH_CRITERIA_DICT    = defaultdict( lambda: None )

SEARCH_CRITERIA_DICT["sys"]     =  "system"
#SEARCH_CRITERIA_DICT["system"]  =    "system"
SEARCH_CRITERIA_DICT["subsys"]  = "sub_system"
#SEARCH_CRITERIA_DICT["name"]    =  "name"
SEARCH_CRITERIA_DICT["id"]      =  "id",

#SEARCH_CRITERIA_DICT["name"]    =  "name"
SEARCH_CRITERIA_DICT["ob"]      =  "id",



#mdi_management
TopicData   = collections.namedtuple(   "TopicData", "table, id, topic" )
# WindowData  = collections.namedtuple(   "WindowData",
#                                        "menu_id, window_title" )  # maybe another dict ?/
# WindowData( menu_id = menu_it, window_title = title)

    # name is first argument  --- second arg space sep or a tuple

# an_example   = MenuInfo( window  = "aaa", menu_item = "bbb",   )     # no quotes on instance names
# print( an_example.window )


NOT_FOR_SUBJECTS   = { picture_document.PictureDocument, album_document.AlbumDocument,  }
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
    also stuff containers
    """
    # these seem to be class level objects
    topic_update_signal            = pyqtSignal(str, int, str )
    stuff_container_update_signal  = pyqtSignal( str, int, dict )

    def send_topic_update(self, table, table_id, info):
        debug_msg   = ( "send_topic_update emit next")
        logging.log( LOG_LEVEL,  debug_msg, )

        self.topic_update_signal.emit( table, table_id, info )

    # --------------------------
    def stuff_container_update_xxx( self, update_type, stuff_id, stuff_data, ):
        debug_msg   = ( "stuff_container_update emit next")
        logging.log( LOG_LEVEL,  debug_msg, )

        self.stuff_container_update_signal.emit( update_type, stuff_id, stuff_data,   )

    # --------------------------
    def stuff_container_update_old( self, update_type, stuff_id, stuff_data, ):
        debug_msg   = ( "stuff_container_update emit next")
        logging.log( LOG_LEVEL,  debug_msg, )

        self.stuff_container_update_signal.emit( update_type, stuff_id, stuff_data,   )


# -------------------------------
class MdiManagement():
    """
    manage the mdi interface.  Need to fix the dyslexia
    mid
    look for creation in main_window
    AppGlobal.mdi_management        = a_mdi_management
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


        self.closed_topics      = []   # _list of dicts      a list of windows that are close but have had topics
        self._open_topics       = []
        # pub.unsubAll( TOPIC_UPDATE )
        self.send_signals       = SendSignals()
        # we have a class for this but we are just using a dict -- lets get rid of the class
        # bad name for just a dict

        self.plant_containers   = { None: "", 1: "1one", 2: "2two" }
        self.text_edit_search   = TextEditSearch( self, AppGlobal.parameters,   )


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
        debug_msg     = f"forget_document begin { window_id } !! update closed_topics "
        logging.log( LOG_LEVEL,  debug_msg, )

        self.remove_menu_item( window_id  )

        window_id.deleteLater()
        # Remove the reference

        del self.window_dict[ window_id ]    # not sure still need window_dict
        window_id  = None  # this does not matter but all othere reverences do

    # --------------------------------------
    def cascade_documents( self, ):
        """
        what it says, read

        """
        mdi_area       = self.main_window.mdi_area
        mdi_area.cascadeSubWindows()
        self.main_window.assign_icon()   # reassign to see if we can keep it


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
        !! may need more for minimized documents
        midi_management.show_document( sub_window )
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
        chat grok and me may have fixed !! do not need messages in future
        """
        menu_id     = self.window_dict[window_id][ "action_id"]
        main_window = self.main_window

        actions     = main_window.window_menu.actions()  # no file menu here in main window
        if actions:
            for i_action in actions:
                if menu_id == i_action:
                    #action_to_remove = actions[-1]  # Remove the last item added
                    #self.file_menu.removeAction( menu_id )
                    # feb 2025 fix ??

                    main_window.window_menu.removeAction( i_action )
                    # QMessageBox.information( AppGlobal.main_window, "Info", f"Removed item: {menu_id}??")
        else:
            pass
            QMessageBox.information( AppGlobal.main_window, "Info", "Item to remove not found.")

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
    def get_a_doc_for_class( self, window_class, open = True ):
        """
        a_doc      = AppGlobal.mdi_management.get_a_doc_for_class( window_class )

        what it says, read

        if open = true open one if necessary

        """
        docs  = self.get_docs_for_class(  window_class )
        if len( docs ) == 0: # then need to open one
            a_doc   = self.make_document( window_class, instance_ix = 1 )
        else:
            a_doc   = docs[0]
        return a_doc

    # -------------------------
    def get_docs_for_class( self, window_class ):
        """
        docs      = AppGlobal.mdi_management.get_docs_for_class( window_class )

        what it says, read

        what:
             self.window_dict[ window_id ]     = { "title": window_id.windowTitle(),
                                       "action_id":  None }   # title action_id

        """
        docs    = []
        for i_doc in  self.window_dict.keys():   # !! better a comp
            if type( i_doc ) == window_class :
                docs.append( i_doc )

        return docs


    # -------------------------
    def get_help_docs( self, ):
        """
        docs      = AppGlobal.mdi_management.get_help_docs()

        !! why not get_docs_for_class
        what it says, read
          may replace !! get_album_doc
              may generalize even more

         does this matter

         self.window_dict[ window_id ]     = { "title": window_id.windowTitle(),
                                       "action_id":  None }   # title action_id

        """
        docs    = []
        for i_doc in  self.window_dict.keys():   # !! better a comp
            if type( i_doc ) == help_document.HelpDocument:
                docs.append( i_doc )

        return docs

    # -------------------------
    def get_stuff_docs(self, ):
        """
        album_docs      = AppGlobal.mdi_management..get_album_docs()

        what it says, read
          may replace !! get_album_doc
              may generalize even more

         does this matter

         self.window_dict[ window_id ]     = { "title": window_id.windowTitle(),
                                       "action_id":  None }   # title action_id
         AlbumDocument

        """
        docs    = []
        for i_doc in  self.window_dict.keys():   # !! better a comp
            if type( i_doc ) == stuff_document.StuffDocument:
                docs.append( i_doc )

        return docs

    # -------------------------
    def get_picture_docs(self, ):
        """
        picture_docs      = AppGlobal.mdi_management..get_picture_docs()

        what it says, read
          may replace !! get_album_doc
              may generalize even more

         does this matter

         self.window_dict[ window_id ]     = { "title": window_id.windowTitle(),
                                       "action_id":  None }   # title action_id


        """
        picture_docs    = []
        for i_doc in  self.window_dict.keys():   # !! better a comp
            if type( i_doc ) == picture_document.PictureDocument:
                picture_docs.append( i_doc )

        return picture_docs

    # -------------------------
    def get_album_docs(self, ):
        """
        album_docs      = AppGlobal.mdi_management..get_album_docs()

        what it says, read
          may replace !! get_album_doc
              may generalize even more

         does this matter

         self.window_dict[ window_id ]     = { "title": window_id.windowTitle(),
                                       "action_id":  None }   # title action_id
         AlbumDocument

        """
        album_docs    = []
        for i_doc in  self.window_dict.keys():   # !! better a comp
            if type( i_doc ) == album_document.AlbumDocument:
                album_docs.append( i_doc )

        return album_docs

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

    # -------------------------
    def do_db_search( self, cmd, args, ):
        """
        what it says, read
            just a relay to text....
        """
        self.text_edit_search.do_db_search( cmd, args, )

    # -------------------------
    def menu_item_clicked(self, name):
        """
        what it says, read.... more coming maybe

        """
        QMessageBox.information(self, "Info", f"You clicked on {name}")

    # -------------------------
    def update_stuff_container_movedtostuffdocument( self, update_type, stuff_id, stuff_data):
        """
        update should include add, delete, update
        what it says, read.... more coming maybe

        """
        #QMessageBox.information(self, "Info", f"You clicked on {name}")
        if update_type == stuff_document.UPDATE:
            if stuff_id in self.stuff_containers:
                self.stuff_container[ stuff_id ].update( stuff_id, stuff_data )
            else:
                self.stuff_containers[ stuff_id ] = StuffContainer( stuff_id, stuff_data )

        else:
            # delete
            debug_msg     = ( f"update_stuff_container delete needs imp { stuff_id }   " )
            logging.error(    debug_msg, )

        pass  # debugging

        # now finc all the stuff windows and send them notification
        # to rebuild dd list for stuff containers

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
        debug_msg   = ( "mdi_management open_topics under test ...........................")
        logging.log( LOG_LEVEL,  debug_msg, )

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


        debug_msg    = ( f"{topic_list = }" )
        logging.log( LOG_LEVEL,  debug_msg, )
        return topic_list


    # -------------------------
    def show_mdi_info( self,     ):
        """
        what it says, read.... more coming maybe

        """
        print( "show_mdi_info .....................................")

        for i_window in self.main_window.mdi_area.subWindowList():
            a_str     = ""
            a_str     = f"{a_str}\n{type( i_window ) = }"
            a_str     = f"{a_str}\n    {i_window.detail_table_id = }"
            a_str     = f"{a_str}\n    {i_window.detail_table_name  = }"
            a_str     = f"{a_str}\n    {i_window.menu_action_id = }"
            a_str     = f"{a_str}\n    {i_window.detail_table_id = }"

            a_str     = f"{a_str}\n    {i_window.topic  = }"
            a_str     = f"{a_str}\n    {i_window.record_state = }"
            # rsn       = base_document_tabs.RECORD_STATE_DICT[ i_window.record_state ]
            # a_str     = f"{a_str}\n    {rsn = }"
            is_for_subject    = type( i_window )  not in NOT_FOR_SUBJECTS
            a_str     = f"{a_str}\n    {is_for_subject = }"
            a_str     = f"{a_str}\n    {i_window.window_title = }"
            print( a_str )


        # dialog     = mdi_info.MdiInfo( topics   = self.topics   )
        # if dialog.exec_() == QDialog.Accepted:
        #     pass

    # -------------------------
    def make_document( self, window_class, instance_ix = 0 ):
        """
        better name open_document
        if instance already open just show it

            instance    for a particular instance
        changed api an now return the instance

        do we have registration issues
        """
        #msg              = f"add_subwindow for window_type {window_type } {instance_ix}"
        # mdi_area       = self.main_window.mdi_area

        if instance_ix != 0:
            docs    = self.get_docs_for_class( window_class )
            for i_doc in docs:
                if i_doc.instance_ix  == instance_ix:
                    self.show_document( i_doc )
                    return i_doc

        # create it if above fails
        sub_window      = window_class( instance_ix )  # sub window is a doc

        # because sometims missing -- grok fix
        sub_window.setWindowFlags(Qt.SubWindow | Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint)
        if AppGlobal.parameters.set_doc_maximized:
            sub_window.showMaximized()

        self.show_document
        self.main_window.assign_icon()   # reassign to see if we can keep it
        return sub_window

    #--------------------------------
    def plant_container_update( self, update_type, table_id, table_info ):
        """first warn, then change
        if we used signals and slots we would go directly to the detail
        tab, maybe later

        stuff_container_update(  update_type = , stuff_id = , stuff_data = )
        """
        planting_docs   = self.get_planting_docs()
        for i_doc in planting_docs:
            i_doc.stuff_containers_update( just_warning = True )

        # self.stuff_containers
        self.update_plant_containers( update_type = update_type,
                                     table_id     = table_id,
                                     table_info   = table_info)
        for i_doc in planting_docs:
            i_doc.plant_containers_update( just_warning = False )

    # ----------------------------------------------
    def update_plant_containers( self, *, update_type, table_id, table_info ):
        """
        CHANGE THE DICTIONARY
        update should include add, delete, update
        what it says, read.... more coming maybe
        sometimes an update may not actually change the dict ?
        """
        #QMessageBox.information(self, "Info", f"You clicked on {name}")
        if update_type == UPDATE:
            if table_id in self.plant_containers:
                self.plant_containers[ table_id ].update( table_id, table_info )
            else:
                self.plant_containers[ table_id ] = stuff_document.StuffContainer( table_id, table_info )

        else:
            # delete
            debug_msg     = ( f"update_plant_containers delete needs imp { table_id }   " )
            logging.error(    debug_msg, )

        pass  # debugging

        self.show_document( sub_window  )
        return sub_window



class TextEditSearch( ):
    """
    About this class.....
    self.text_edit_ext_obj         = text_edit_ext.TextEditExt( AppGlobal.parameters, entry_widget)
    """
    #----------- init -----------
    def __init__( self, mdi_management, parameters,   ):
        """
        Usual init see class doc string
        """
        # this is the constructor run when you create
        # like  app = AppClass( 55 )
        self.parameters       = parameters
        self.mdi_management   = mdi_management

        # msg   = ( f"second instance of TextEditExt created move all methods in this object ?  {1  = }  ")
        # logging.error( msg )


    # ----------------------------------
    def parse_search_part( self, criteria, part ):
        """

        still needs error check
        mutates
            criteria, hence no return
        """
        splits    = part.split( "=", 1 )
        if len( splits ) < 2:
            msg    = "{part =} is not valid for a criteria so ..."
            raise ValueError( msg )

        key0      = (splits[0].strip()).lower()
        value     = splits[1].strip()
        # may need type conversion when get to dates
        key       = SEARCH_CRITERIA_DICT[key0]
        if  key is None:
            key  = key0
        criteria[key] = value
        #return criteria

    # ----------------------------------
    def parse_search( self, a_string ):
        """
        >>search jeoe sue   /sys=python /subsys=qt
        change to a dict

        cirteria = {key_words: "joe" "sue" }

        """
        criteria    = defaultdict( None )
        parts       = a_string.split( "/" )
        key_words   = parts[0].strip()
        criteria[ "key_words" ] = key_words

        for i_part in parts[ 1: ]:
            try:
                self.parse_search_part( criteria, i_part  )
            except ValueError as error:
                # Access the error message
                error_message = str(error)
                msg  = (f"Parse >>search Caught an error: {error_message}")
                msg_box             = QMessageBox()
                msg_box.setIcon( QMessageBox.Information )
                msg_box.setText( msg )
                msg_box.setWindowTitle( "Sorry that is a No Go " )
                msg_box.setStandardButtons( QMessageBox.Ok )
                msg_box.exec_()
                return criteria
        # print( criteria )

        return criteria


    #------------------------------------
    def do_db_search(self, cmd, args, ):
        """
        perhaps throw some exceptions back here to end the search !!
        cmd has been .lowrer()
        """
        # strip off comment if any ?? save the comment ?
        #     # logging.debug( msg )
        mdi_area    = self.mdi_management.main_window.mdi_area
        new_args    =  []  # drop after #
        for i_arg in args:
            if i_arg.startswith( "#" ):
                break
            new_args.append( i_arg )
        # put the search sting back together
        search_string    = " ".join( new_args )
        criteria         = self.parse_search( search_string )

        # need to send criteria to the right document/sub_window
        if cmd == "search":
            # get current window
            target_subwindow    = mdi_area.activeSubWindow() # grok says
        else:  # zz
            # breakpoint()
            # determine window type
            window_class        = SEARCH_COMMAND_DICT[ cmd ]
            if window_class is None:
                msg     = ( f"{cmd = } not a valid search command" )
                #raise ValueError( f"{cmd = } not a valid search command" )

                msg_box         = QMessageBox()
                msg_box.setIcon( QMessageBox.Information )
                msg_box.setText(  msg  )
                msg_box.setWindowTitle( "Sorry that is a No Go " )
                msg_box.setStandardButtons( QMessageBox.Ok )
                msg_box.exec_()
                return

            target_subwindow    = self.mdi_management.get_a_doc_for_class(  window_class, open = True )

        # !! bring focus to window
        target_subwindow.search_me( criteria )




# ---- eof
