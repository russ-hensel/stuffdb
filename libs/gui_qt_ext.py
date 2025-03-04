#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Purpose:
    Just starting new version for qt, some may be same as old or not

        still tk code for some items

    part of my ( rsh ) library of reusable code
    a library module for multiple applications
    sometimes included with applications but not used
        as this make my source code management easier.

    Test:  see sub dir and programs where used like
        web_search

        Search:
            PlaceInGrid

Various classes to extend qt5 functionality
     browsers
     message frames




master in rsh_lib, gui_qt_ext

us sys path for development, then copy over file and edit for git hub

sys.path.append( "../rshlib" )
import gui_ext

AppGlobal is needed to run this,
look for links
        .parameters
        .logger


"""
# ---- tof


# ---- imports

# perhaps lazy import better  tk.
#import tkinter as tk
#from   tkinter.filedialog import askopenfilename
#from   tkinter.filedialog import askdirectory
#from   tkinter.messagebox import showinfo
#import tkinter.ttk as ttk

#import PyQt5.QtWidgets as qtw    #  qt widgets avaoid so much import below
from   PyQt5.QtCore import Qt, QTimer
from   PyQt5 import QtGui

from PyQt5.QtWidgets import QApplication,  QMainWindow
from PyQt5.QtWidgets import QGridLayout,   QVBoxLayout
from PyQt5.QtWidgets import QLabel,      QTextEdit, QGroupBox,  QPushButton
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox


import sys
import os
# import pyperclip

import string_util

from   app_global import AppGlobal
# for above to work need to have an AppGlobal in the dir
# where app was started, or provide another in this dir
# seems to work

# STICKY_ALL          = tk.N + tk.S + tk.E + tk.W

import logging

logger          = logging.getLogger( )


# for custom logging level at module
LOG_LEVEL  = 5   # higher is more


#---------------------
def bring_to_top( root_frame  ):
    """
    What it says, read code
    gui_ttk_ext.bring_to_top( root )
    """
    #rint( f"bring_to_top() {__name__}"  )

    # ---- ---- method one, did not work ?
    # self.root.attributes('-topmost', 1)
    # self.root.attributes('-topmost', 0)  # else it will stay on top as a pain

    # method 2
    root_frame.iconify()
    root_frame.update()
    root_frame.deiconify()

#---------------------
def minimize_gui( root_frame  ):
    """
    What it says, read code
    gui.ttk_ext.minimize_gui( root )
    root frame is QMainWindow
    """
    #root_frame.ShowMimized()
    root_frame.showMinimized()
    #rint( f"bring_to_top() {__name__}"  )
    # method 2
    #root_frame.iconify()
    #.showMinimized()
    #root_frame.update()
    #root_frame.deiconify()

#---------------------
def maximize_gui( root_frame  ):
    """
    What it says, read code
    gui.ttk_ext.minimize_gui( root )
    root_frame may be central_widget or its parent or....
    """
    #root_frame.ShowMimized()
    root_frame.showMaximized()
    #rint( f"bring_to_top() {__name__}"  )
    # method 2
    #root_frame.iconify()
    #.showMinimized()
    #root_frame.update()
    #root_frame.deiconify()

#---------------------
def about(  controller  ):
    """
    interfaces with controller and called back from gui
    What it says, read code
            url   =  r"comming soon not at http://www.opencircuits.com/TBD"
        __, mem_msg   = cls.show_process_memory( )
        msg  = f"{cls.controller.app_name}  version:{cls.controller.version} \n  by Russ Hensel\n  Memory in use {mem_msg} \n  Check <Help> or \n     {url} \n     for more info."
        messagebox.showinfo( "About", msg,  )   #   tried ng: width=20  icon = "spark_plug_white.ico"

    """
    message_box = QMessageBox( controller.gui )
    message_box.setWindowTitle( "About this Application" )

    msg         = ( f"{ controller.app_name}  version:{ controller.app_version}"
                    f"\n  by Russ Hensel"
                    # f"\n  Memory in use {mem_msg} "
                    f"\n  Check <Help> or "
                    f"\n  {controller.app_url} \n"
                   )

    message_box.setText( msg )

    # message_box.setIcon(QMessageBox.Information)
    message_box.exec_()

#---------------------
def make_root( parameters  ):
    """
    What it says, read code
    make a root window with support for themes
    """
    root = None   # for qt ??
    # # ----- start building gui  -- may need root stuff at top
    # if  parameters.gui_theme_type  in ["none", "ttk" ]:
    #     # valid values see gui_with_tabs

    #     root      = tk.Tk()
    #     style     = ttk.Style()

    #     style.theme_use( parameters.gui_ttk_theme )
    #         # may throw error if not compatible with
    #         # the .gui_ttk_theme

    # elif parameters.gui_theme_type  in [ "ttkthemes", ]:
    #     from ttkthemes import ThemedTk
    #     #a_theme    = "blue"  #Adapta arc aquativo
    #     #a_theme    = "plastik"  # bad name seem to fall back to default without error
    #     root     = ThemedTk( theme = parameters.gui_ttk_theme )

    #     print( f"available themes are:  {root.pixmap_themes}" )

    # else:
    #     1/0   # poor man's exception

    return root

# ---------------------------------
class FileBrowseWidget( QWidget ):
    """
    where alreay used ??
    gui_qt_ext.FileBrowseWidget


    in stuff db
       /mnt/WIN_D/Russ/0000/python00/python3/_projects/stuffdb/file_browse.py
       but apparently not used instead code in our test

    adding to ./test


    """

    #-----------------------------
    def __init__(self, parent=None, entry_width=None):
        """
        unclear wht this is or does is not a widget but
        seems to contain widgets

        for now just see stuff code.

        Args:
            parent (TYPE, optional): DESCRIPTION. Defaults to None.
            entry_width (TYPE, optional): DESCRIPTION. Defaults to None.

        Returns:
            None.

        """
        super().__init__(parent)
        self.setWindowTitle("File Browse Widget")
        self.resize(400, 100)

        if entry_width is None:
            entry_width = 100

        self.label_widget   = QLabel("Get File Name:", self)
        self.label_widget.setGeometry(10, 10, 100, 30)

        self.entry_1 = QLineEdit(self)
        self.entry_1.setGeometry(120, 10, entry_width, 30)

        self.button_2 = QPushButton("Browse...", self)
        self.button_2.setGeometry(240, 10, 80, 30)
        self.button_2.clicked.connect(self.browse)

        self.initialdir     = "./"
        self.title          = "Select file for db"
        self.filetypes      = "All Files (*)"

    #-----------------------------
    def browse(self):
        """
        what it says
        Returns:
            None.

        """
        options  = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setOptions(options)
        file_dialog.setDirectory(    self.initialdir )
        file_dialog.setWindowTitle(  self.title      )
        file_dialog.setNameFilter(   self.filetypes  )

        if file_dialog.exec_():
            filenames = file_dialog.selectedFiles()
            self.set_text(filenames[0])

    #--------------------
    def set_text(self, a_string):
        self.entry_1.setText(a_string)

    def get_text(self):
        return self.entry_1.text()


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     widget = FileBrowseWidget()
#     widget.show()
#     sys.exit(app.exec_())

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     widget = DirBrowseWidget()
#     widget.show()
#     sys.exit(app.exec_())




class DirBrowseWidget(QWidget):
    """





    """

    def __init__(self, parent=None, initialdir=None, browse_title=None):
        super().__init__(parent)
        self.setWindowTitle("Directory Browse Widget")
        self.resize(400, 100)

        self.label_widget = QLabel("Get Directory Name:", self)
        self.label_widget.setGeometry(10, 10, 120, 30)

        self.entry_1 = QLineEdit(self)
        self.entry_1.setGeometry(140, 10, 200, 30)

        self.button_2 = QPushButton("Browse...", self)
        self.button_2.setGeometry(350, 10, 80, 30)
        self.button_2.clicked.connect(self.browse)

        self.initialdir = initialdir if initialdir else "/"
        self.browse_title = browse_title if browse_title else "Select Directory"

    def browse(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks

        dir_dialog = QFileDialog()
        dir_dialog.setFileMode(QFileDialog.Directory)
        dir_dialog.setOptions(options)
        dir_dialog.setDirectory(self.initialdir)
        dir_dialog.setWindowTitle(self.browse_title)

        if dir_dialog.exec_():
            selected_dir = dir_dialog.selectedFiles()
            self.set_text(selected_dir[0])

    def set_text(self, a_string):
        self.entry_1.setText(a_string)

    def get_text(self):
        return self.entry_1.text()


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     widget = DirBrowseWidget()
#     widget.show()
#     sys.exit(app.exec_())

#  --------
class MessageArea( QGroupBox  ):
    def __init__( self ):

        """
        widget   =  gui_qt_ext.MessageArea()
    need to add or make new class to be an edit window
         get rid of buttons
         get all text programatically
         make ctrl-c -v work

    add arguments to init
    make buttons optiona !!
    make disable always on !!

    message frame used in so many apps

        a_frame            = gui_qt_ext.MessageArea( parent,  )


    # ----------- from web search -------------------------------   gui_qt_ext.MessageArea
    def _make_message_frame( self, parent,  ):
        x""
        make the message frame for user feedback
        x""
        message_widget       = gui_qt_ext.MessageArea()
        self.message_frame   = message_widget
        return message_widget



        self.message_frame = a_frame
        return a_frame

    Interface
         functions
         self.max_lines
         self.msg_text
         self.button_widgets
         do_clear_button()
         print_string()


    """
        super().__init__()
        group_placer   = PlaceInGrid(  self, by_rows = False )

        copy_button = QPushButton( "Copy Text" )
        copy_button.clicked.connect(lambda: self.copy_text(text_edit))
        group_placer.place( copy_button, rowspan = 1, columnspan = 1 )

        # Create QTextEdit widget
        text_edit = QTextEdit()
        # layout.addWidget(text_edit, 4, 0, 1, 3)  # Row 4, Column 0, RowSpan 1, ColumnSpan 3
        self.text_edit  = text_edit
        group_placer.place( text_edit, rowspan = 8, columnspan = 3 )

        widget = QPushButton( "Delete Text" )
        widget.clicked.connect(lambda: self.delete_text(text_edit))
        widget.setMaximumWidth(150)
        #widget       = delete_button
        group_placer.new_row( )
        group_placer.place( widget, rowspan = 1, columnspan = 1 )

        insert_button = QPushButton("Insert Text")
        insert_button.clicked.connect(lambda: self.insert_text(text_edit, "Inserted Text"))
        widget        = insert_button
        group_placer.new_row( )
        group_placer.place( widget, rowspan = 1, columnspan = 1 )

        copy_selected_button = QPushButton("Copy Selected Text")
        copy_selected_button.clicked.connect(lambda: self.copy_selected_text(text_edit))
        widget = copy_selected_button
        # layout.addWidget(copy_selected_button, 6, 0)
        group_placer.new_row( )
        group_placer.place( widget, rowspan = 1, columnspan = 1 )

        widget = QPushButton("Clear")
        widget.clicked.connect( lambda: self.clear_text( ) )
        clear_button = widget
        # layout.addWidget(copy_selected_button, 6, 0)
        group_placer.new_row( )
        group_placer.place( widget, rowspan = 1, columnspan = 1 )

    # ---------------  end of button actions and class
    # ---------------------------------------
    def print_string( self, a_string,
                     plus_newline    = True,
                     title           = "",
                     clear           = False,
                     update_now      = False ):
        """
        this is old tk  .... fix ?? for now redirect o display_string
        msg_frame.print( a_string _  )
        print to message area, with scrolling and
        log if we are configured for it
        should we have a prefix, or just do in the call?? or gui
        parameters.gui_text_log_fn    = False  # "gui_text.log"       # a file name or something false

        parameters.log_gui_text       = False # True or false to log text
        parameters.log_gui_text_level = 10    # logging level for above

        a_string,
        plus_newline,
        title = "",
        clear = False,
        update_now = False
        plus_newline
        !! dup with display_string ??

        """
        self.display_string( a_string )

        return



        if  AppGlobal.parameters.gui_text_log_fn:

            with open( AppGlobal.parameters.gui_text_log_fn, "a"  ) as a_file:
                a_file.write( a_string )   # do we need \n check
                #rint(   a_string )

        if  AppGlobal.parameters.log_gui_text:
            AppGlobal.logger.log( AppGlobal.parameters.log_gui_text_level, a_string, )

        if clear:
            self.clear_message_area()

        if  title != "":
            self.msg_text.insert( tk.END, title, )

        if plus_newline:
            a_string = a_string + "\n"

        # now the meat
        self.msg_text.insert( tk.END, a_string, )      # this is going wrong, why how

        # limit the number of lines
        try:
            numlines = int( self.msg_text.index('end - 1 line').split('.')[0] )
                # !! beware int( None ) how could it happen ?? it did this is new
        except Exception as exception:
            # look in logs to find
            msg  = f"MessageFrame, indexing exception {exception}"
            AppGlobal.logger.error( msg )
            print( msg )
            numlines = 0

        if numlines > self.max_lines:
            cut  = int( numlines/2  )    # lines to keep/remove
            self.msg_text.delete( 1.0, str( cut ) + ".0" )               # remove excess text
#            msg     = "Delete from test area at " + str( cut )
#            self.logger.info( msg )

        # auto scroll
        if self.cb_scroll_var.get():
            self.msg_text.see( tk.END )

        if update_now:
            AppGlobal.gui.root.update()
            print( "!! self.root not valid here ")

    # ---------------------------------------
    def display_string( self, a_string, update_now = False ):
        """
        !! we may phase out for print_string  or the reverse ??
             make one call the other
        print to message area, with scrolling and
        log if we are configured for it

        parameters.gui_text_log_fn    = False  # "gui_text.log"
                                               # a file name or something false


        parameters.log_gui_text       = False # True or false to log text
        parameters.log_gui_text_level = 10    # logging level for above

        !! add parameter clear_msg = True or false

        """
        print(  f"in display_string, with a_string = {a_string}")
        # return
        #   try  !!!  QTextEdit.clear()
        cursor = self.text_edit.textCursor()
        # cursor.movePosition( QTextCursor::End )
        cursor.insertText( a_string )

#         #rint( "debug for display_string")
#         if  AppGlobal.parameters.gui_text_log_fn:
#             # for now open close.... later perhaps improve
#             with open( AppGlobal.parameters.gui_text_log_fn, "a"  ) as a_file:
#                 a_file.write( a_string )   # do we need \n check
#                 #rint(   a_string )

#         if  AppGlobal.parameters.log_gui_text:
#             AppGlobal.logger.log( AppGlobal.parameters.log_gui_text_level, a_string, )

#         self.msg_text.insert( tk.END, a_string, )      # this is going wrong, why how
#         try:
#             numlines = int( self.msg_text.index( 'end - 1 line' ).split('.')[0] )
#                 # !! beware int( None ) how could it happen ?? it did this is new
#         except Exception as exception:
#         # Catch the custom exception -- !! to broad execpt
#             AppGlobal.logger.error( str( exception ) )
#             print( exception )
#             numlines = 0
#         if numlines > self.max_lines:
#             cut  = int( numlines/2  )    # lines to keep/remove
#             self.msg_text.delete( 1.0, str( cut ) + ".0" )
#                 # remove excess text
# #            msg     = "Delete from test area at " + str( cut )
# #            self.logger.info( msg )

#         if self.cb_scroll_var.get():
#             self.msg_text.see( tk.END )

#         if update_now:
#             AppGlobal.gui.root.update()
#             print( "!! self.root not valid here ")

    #  --------
    def print_message(self, text):
        print("Button clicked:", text)

    #  --------
    def clear_text( self ):
        self.text_edit.clear()

    #  --------
    def copy_text(self, text_edit):
        selected_text = text_edit.toPlainText()
        QApplication.clipboard().setText(selected_text)
        print(  f" copy_text -> {selected_text }" )

    # ----
    def delete_text(self, text_edit):
        text_edit.clear()

    # ----
    def insert_text(self, text_edit, text):
        cursor = text_edit.textCursor()
        cursor.insertText(text)

    def copy_selected_text(self, text_edit):
        selected_text = text_edit.textCursor().selectedText()
        QApplication.clipboard().setText(selected_text)
        print(  f" copy_selected_text -> {selected_text }" )



# ----------------------------------------
class ListboxScroll( ):
    """
    scrolling listbox with title and utility functions
    master in rsh_lib, gui_ext

    consider making descandant of Frame

    note that self.   hold components for possible use

    so far single selection
    How to interface

           a_obj        = gui_ttk_ext.ListboxScroll( parent_frame, a_title = "a title", width = None, height = None )
           place  ... a_obj.outer_frame

        use functions
            .....
        access
            self.listbox       to access any pure listbox attributes
            self.outer_frame   to place the frame

    used in:

    """
    def __init__( self, parent_frame, a_title = "a title", width = None, height = None ):
        """
        if title is None do not construct that part

        """
        self.version        = "2021_08_04"
        self.parent         = parent_frame
        self.title          = a_title
        self.click_function = None     # set later or externally
        self.frame          = None     # the frame this is in use xxx.frame
        self.listbox        = None     # the listbox
        self.outer_frame    = None

        if width is None:
            width = 100

        if height is None:
            height = 100

        self._make_titled_listbox_( width, height )

    # ----------------------------------------
    # """
    # functions needed
    # set command  -- just a property ... no needs function could make a propeety @
    # inset_row
    # """
    # ----------------------------------------
    def insert_row( self, value ):
        """
        what is says
        """
        self.listbox.insert(  tk.END, value )

     # ----------------------------------------
    def clear_rows( self,  ):
        """
        what is says
        """
        self.listbox.delete( 0, tk.END )

    # ----------------------------------------
    def set_values( self, values ):
        """
        what is says
        can we use to clear set list without using insert row
        """
        #self.listbox.configure( values )
        # clear
        #for

    # ----------------------------------------
    def set_width( self, width ):
        """
        what is says -- read
        """
        # label seems to be the controlling thing
        self.label_widget.configure( width = width )

    # ----------------------------------------
    def set_height( self, height ):
        """
        what is says -- read
        """
        # label seems to be the controlling thing
        self.listbox.configure( height = height )
        print( "!! implement set_height if not working" )

    # ----------------------------------------
    def set_click_function( self, a_function ):
        """
        what is says -- would bind be better
        we want an index or contents of row or both need
        more work here
        """
        self.click_function =  a_function

    # ------------------
    def _click_function( self, event ):
        """
        what is says -- would bind be better -- on the list box?, search
        we want an index or contents of row or both need
        more work here
        """
        if self.click_function is None:
            print( "ListboxScroll -- click_function not set" )
        else:
            # sending the selection get, but perhaps should
            #    send the event and let click function ....!!!
            # a_key   = event.widget.selection_get()
            #rint( a_key )
            # self.click_function( a_key )
            self.click_function( event )

    # ------------------
    def get_row_text( self, a_index ):
        """
        if ix not valid then ?? return None

        """
        if self.listbox.size() >= a_index:
            a_value  = self.listbox.get( a_index )
        else:
            a_value  = None

        return a_value

    # ------------------
    def get_selected_ix( self ):
        """
        return 0 based selection -1 if nothing
        assumes in single select mode
        """
        selected_ix   = self.listbox.curselection()

        if selected_ix == tuple(  ):
            selected_ix  = -1
        else:
            selected_ix  =  selected_ix[0]   # since we allow only 1 selection

        return selected_ix

    # ----------------------------------------
    def _make_titled_listbox_( self, width, height  ):
        """
        make a frame ( at top will become self.outer_frame )
        in it a listbox ( self.listbox )
        and a scrollbar
        and a label

        for snips and snippets?
        return ( famelike_thing, listbox_thing)  ?? make a class, better access to components
        """
        a_frame       = tk.Frame( self.parent, width = 1000 )

        a_frame.grid_rowconfigure(    0, weight = 0 )
        a_frame.grid_rowconfigure(    1, weight = 1 )
        a_frame.grid_rowconfigure(    1, weight = 1 )

        a_frame.grid_columnconfigure( 0, weight = 1 )
        a_frame.grid_columnconfigure( 1, weight = 0 )

        a_label = ttk.Label( a_frame, text = self.title, width = width )
        a_label.grid( column = 0, row = 0, sticky = ( tk.N, tk.E, tk.W) )
        self.label_widget  = a_label

        a_listbox       = tk.Listbox( a_frame, height = 5 )
        self.listbox    = a_listbox
        a_listbox.grid( column = 0, row = 1, sticky = STICKY_ALL )

        a_listbox.bind( "<<ListboxSelect>>", self._click_function  )

        a_scrollbar     = ttk.Scrollbar( a_frame,
                                    orient    = tk.VERTICAL,
                                    command   = a_listbox.yview)

        a_scrollbar.grid( column=1, row=1, sticky = STICKY_ALL )   # (tk.N, tk.S)
        a_listbox[ 'yscrollcommand'] = a_scrollbar.set

        # for overall widget
        self.set_width( width  )
        self.set_height( height )

        self.listbox     = a_listbox
        self.frame       = a_frame
        self.outer_frame = a_frame

        return a_frame

# -----------------------------------
class CQGridLayout( QGridLayout ) :
    """
    a custom grid layout from PlaceInGrid but this is a layout
    """
    def __init__( self,   *, col_max = 0, indent = 0   ):
        super().__init__(  )
        self.col_max    = col_max  # 0 no max
        self.ix_row     = 0
        self.ix_col     = 0
        self.indent     = indent  # an idea but what idea
        # for debug
        self.last_ix_row  = None
        self.last_ix_col  = None
        self.last_stretch = None
        # or call reset

    def reset( self,  *, col_max = 0, indent = 0   ):
        """
        for debug may become more pearmanent """
        self.col_max    = col_max  # 0 no max
        self.ix_row     = 0
        self.ix_col     = 0
        self.indent     = indent  # an idea but what idea no implemented
        # for debug
        self.last_ix_row  = None
        self.last_ix_col  = None
        self.last_stretch = None

        print( "reset================>", self )

    # -----------------------------------
    def addWidget( self,
               widget,
               ix_row       = None,
               ix_col       = None,
               *,
               columnspan   = 1,
               rowspan      = 1,
               stretch      = None,
               ):
        """
        to work like QLayouts but do ix_row, ix_col automatically
        this is preliminary
        layout.addWidget( widget, ix_row, ix_col, row_span, col_span )

        rowspan not yet implementd


        """
        if ix_row is None:
            ix_row  = self.ix_row

        if ix_col is None:
            ix_col = self.ix_col

        self.last_ix_row     = ix_row
        self.last_ix_col     = ix_col
        self.last_columnspan = columnspan

        # later check for nones and delta
        super().addWidget( widget, self.ix_row, self.ix_col, rowspan, columnspan   )

        # if columnspan is None: not sure what is devault
        #     # make default
        #     columnspan = 1

        # this computes the next
        self.ix_col    += columnspan
        if self.col_max and ( self.ix_col  >= self.col_max ):
            self.ix_row    += 1
            self.ix_col    = 0

            debug_msg       = f"addWidget__increment row {self}  "
            logging.log( LOG_LEVEL,  debug_msg, )
        # else:  # for debug
        #     pass
        #     print( self )

    def get_add_parm_str( self, ):
        """
        for debugging lable controls wit this
        """
        msg       = f"r{self.last_ix_row},c{self.last_ix_col} s{self.last_columnspan}"
        return msg
        #super().addWidget( widget, self.ix_row, self.ix_col )

    def __str__( self, ):
        """ """
        a_str   = ""
        a_str   = ">>>>>>>>>>* CQGridLayout *<<<<<<<<<<<<"
        a_str   = string_util.to_columns( a_str, ["col_max",
                                           f"{self.col_max}" ] )
        a_str   = string_util.to_columns( a_str, ["indent",
                                           f"{self.indent}" ] )
        a_str   = string_util.to_columns( a_str, ["ix_col",
                                           f"{self.ix_col}" ] )
        a_str   = string_util.to_columns( a_str, ["ix_row",
                                           f"{self.ix_row}" ] )
        return a_str

    # -----------------------------------
    def new_row( self, delta_row = 1, indent = None ):
        """
        start a new row in col 0
        !! also for col
        """
        if indent is None:
            indent = self.indent    # or vise versa
        else:
            self.indent = indent
        self.ix_row     += delta_row
        self.ix_col      = indent
        debug_msg       =( f"new_row {self.ix_row = }  {self.ix_col = }")
        logging.log( LOG_LEVEL,  debug_msg, )


# -----------------------------------
class PlaceInGrid( ):
    """
    old tk comment, some applies to qt some not
    called sequentially to help layout grids in a row and column format
    columnspan=2, rowspan=2
    add columnspan to place  make it increment in direction we are moving ....??

    to do
    add column span row span -- keep delta ? delta is span in direction, but may need both ?
    add setup for stickyness ??
    tested through my use, works in my apps, but may nt even be used

    placer    = gui_qt_ext.PlaceInGrid( 99,  central_widget = a_widget, by_rows = False )
    placer.place(  a_widget, columnspan = None,   rowspan = None, sticky = None )

    Interface
        tried to use _xxx for non interface functions and var
        debug_id


      gui_qt_ext.PlaceInGrid(  a_widget )

    """
    def __init__( self,  central_widget, a_max = 0, by_rows = True  ):
        """
        and see class doc.... combine
        uses  layout a QGridLayout()
        placer = gui_qt_ext.PlaceInGrid( parent_widget, a_max, by_rows = False)
        Args:
               parent_widget  container for the widges that this will place
                a_max, may want to change to by name and default to 0 which is unlimited
                by_rows  --- require name ?? default

        """
        # if central_widget:
        #     self.central_widget = central_widget
        # else:
        #     print( "creating central widget " )
        #     self.central_widget = QWidget()

        # a_window.setCentralWidget( self.central_widget )

        # self.window   = a_window   # for later ref

        # if layout:
        #     self.layout   = layout
        # else:
        #     print( "creating layout" )
        #     self.layout   = QGridLayout()

        self.central_widget = central_widget
        self.layout         = QGridLayout()
        if  isinstance(  central_widget,  QVBoxLayout ):  # should be more here
            self.central_widget.addLayout( self.layout )
        else:
            self.central_widget.setLayout( self.layout )

        #rint( f"PlaceInGrid __init__ central_widget.layout(){ central_widget.layout()} " )
        self.debug_id       = "default_id"  # use as part of interface
        self.max            = a_max
        self.ix_row         = 0
        self.ix_col         = 0     # ix_col   += 1 to move across one
        self.ix_col_max     = 0 # may be used by filler
        self.by_rows        = by_rows
        self.indent         = 0    # interface and set by new_row
        if by_rows:
            self.function =  self._place_down_row_
        else:
            self.function =  self._place_across_col_

    # def addWidget( self,
    #            a_widget,
    #            columnspan   = None,
    #            rowspan      = None,
    #            sticky       = None
    #            ):

    #     self.place(
    #            a_widget,
    #            columnspan   = None,
    #            rowspan      = None,
    #            sticky       = None
    #            )

    # -----------------------------------
    def addWidget( self,
               a_widget,
               columnspan   = None,
               rowspan      = None,
               sticky       = None
               ):
        """
        to work like QLayouts
        """
        self.place(
               a_widget     = a_widget,
               columnspan   = columnspan,
               rowspan      = rowspan,
               sticky       = sticky
               )

    # -----------------------------------
    def place( self,
               a_widget,
               columnspan   = None,
               rowspan      = None,
               sticky       = None
               ):
        """

        move row or column by delta grid spacings after pacing control
        what is row span vs deltac
        args:
            widget     -> the widget being placed
            columnspan -> the column span               left over from tk not implemented
            rowspan    -> the rowspan                    left over from tk not implemented
            sticky     -> temporary override of sticky via argument   left over from tk not implemented
        """
        if columnspan is None:
            columnspan = 1

        if rowspan is None:
            rowspan    = 1

        #app_global.print_debug( f"row,co = {self.ix_row}, {self.ix_col}" )
        self.function( a_widget,  columnspan = columnspan, rowspan = rowspan, sticky = sticky )

    # -----------------------------------
    def place_filler( self,  stretch   = 1, widget = None  ):
        """
        place a filler widget that will streach
        filler is layed out in the central_widget layout ?
        need to fix for widget = None
        """
        #rint( f"&&&&&&&&&& place_filler {self}")

        widget          = QWidget()
        widget          = QGroupBox( f"filler {self.debug_id}" )   # just for debugging

        # which of next ??
        ix_col_stretch  = self.ix_col_max + 1
        ix_col_stretch  = self.ix_col + 1

        self.layout.setColumnStretch( ix_col_stretch, stretch )
        print( f"-------- end place filler  ----- col >{ix_col_stretch}<  row >{self.ix_row}< ---- {stretch}-----")
        # seems keywords not allowed in addWidget, just by position
        self.layout.addWidget(  widget,
                                self.ix_row,
                                ix_col_stretch ,
                                # column_span,       # columnSpan -1, then the widget will extend to the
                                                    #     bottom and/or right edge, respectively.
                                # row_span,          # rowSpan

                                #1,    #Alignment or flag  Qt.Alignment()]]])     # is it a list ? The alignment is specified by alignment .
                                                    #The default alignment is 0, which means that the widget fills the entire cell.
                                )

    # -----------------------------------
    def _place_down_row_( self, a_widget, columnspan, rowspan, sticky = None ):
        """
        one of the value intended for self.function
        does its name
        not much tested
        need to add sticky
        """
        # if sticky is None:
        #     sticky = self.sticky

        #rint( f"_place_down_row_ row = {self.ix_row} col = {self.ix_col}"  )
        # a_widget.grid( row          = self.ix_row,
        #               column        = self.ix_col,
        #               rowspan       = rowspan,
        #               sticky        = sticky,  )
        1/0

        self.layout.addWidget( a_widget,
                               self.ix_row,
                               self.ix_col ,
                               columnSpan     = columnspan,
                               rowSpan        = rowspan,    )

        self.ix_row += rowspan
        if ( self.max > 0  ) and ( self.ix_row >= self.max ):
            #rint( f"{self.debug_id} hit max row {self.max}"  )
            self.ix_col += 1
            self.ix_row  = 0

    # -----------------------------------
#    delta_row_col( delta_row, delta_col )
#    add a span argument
    # -----------------------------------
    def new_column( self, delta = 1,  ):
        """
        start a new column in row 0
        for going down columns not aacross

        """
        self.ix_row     = 0
        self.ix_col     += delta

    # -----------------------------------
    def new_row( self, delta_row = 1, indent = None ):
        """
        start a new row in col 0
        !! also for col
        """
        if indent is None:
            indent = self.indent    # or vise versa
        else:
            self.indent = indent
        self.ix_row     += delta_row
        self.ix_col      = indent

        # -----------------------------------
    def dwn_and_back( self,  delta_row = 1 ):
        """
        just an idea
        for now just us direct manipulation of ix_row, ix_col
        go dwn row and back column
        to set up directly below last placement
        delta_row = 1 !! add this
        set up for next placer, then will need a self.ix_row     -= 1
        """
        self.ix_row     += 1
        self.ix_col     -= 1

    # -----------------------------------
    def set_row( self, row,  ):
        """
        what if beyond max
        """
        self.ix_row = row

    # -----------------------------------
    def set_col( self,  col ):
        """
        what it says, why not just the property

        """
        self.ix_col = col

    # -----------------------------------
    def _place_across_col_( self, a_widget, *, columnspan,  rowspan, sticky, ):
        """
        # layout.addWidget(text_edit, 4, 0, 1, 3)  # Row 4, Column 0, RowSpan 1, ColumnSpan 3
        what it says
        one of the value intended for self.function
        args:
            widget     -> the widget being placed
            columnspan -> the column span
            rowspan    -> the rowspan
            sticky     -> temporary override of sticky via argument
        """
        #rint( f"_place_across_col_ row = {self.ix_row} col = {self.ix_col}"  )
        # defaulting should be done in place
        # if columnspan is None:
        #     columnspan = 1

        # if rowspan is None:
        #     rowspan = 1

        # probably wrong but not using sticky
        if sticky is None:
            self.sticky = sticky

        #rint( f"_place_across_col_ ({self.ix_col}, {self.ix_row})"
        #                               f"columnspan = {columnspan}" )
        #rint( f"for {self.debug_id} placing   {a_widget}  at {self.ix_col}, row {self.ix_row}")
        #	addWidget(QWidget *widget, int stretch = 0, Qt::Alignment alignment = Qt::Alignment())

        self.layout.addWidget( a_widget,
                               self.ix_row,
                               self.ix_col,
                               rowspan,
                               columnspan,
                               )
        # ---- code that may be useful?
        # self.gridLayout.addWidget(textEdit1, 0, 0)
        # self.gridLayout.addWidget(textEdit2, 1, 1)
        # self.gridLayout.addWidget(textEdit3, 0, 1)
        # self.gridLayout.setColumnStretch(0, 1)
        # self.gridLayout.setColumnStretch(1, 3)
        # self.gridLayout.setRowStretch(0, 3)
        # self.gridLayout.setRowStretch(1, 1)



        # self.layout.addWidget( a_widget,
        #                        self.ix_row,
        #                        self.ix_col,
        #                        rowspan,              # streah
        #                        # sticky,  #  Qt.AlignCenter,       # allignment ??    Qt.AlignCenter works but makes a mess
        #                        )

        self.ix_col         += columnspan
        self.ix_col_max      = max( self.ix_col_max, self.ix_col )
        if ( self.max > 0  ) and ( self.ix_col >= self.max ):
            #rint( f"hit max row {self.max}"  )
            self.new_row()

        #rint("_place_across_col_",  self.ix_row, self.ix_col  )
        #rint( f"end placing   self = {self}  ") 2023-08-03 10:18:53

    # -----------------------------------
    def __str__( self,   ):
        """
        what is says, read, for debugging

        """
        a_str = f"/n>>>>>>>>>>* __str__ for PlaceInGrid  debug id =  {self.debug_id} * <<<<<<<<<<<<"
        a_str = f"{a_str}\n   ix_row                 {self.ix_row }"
        a_str = f"{a_str}\n   ix_col                 {self.ix_col }"

        a_str = f"{a_str}\n   ix_col_max             {self.ix_col_max}"

        #a_str = f"{a_str}\n   function               {self.function}"
        # a_str = f"{a_str}\n   xxx        {self.xxx}"
        return a_str

# --------------------------------------
class TitledFrame(  ):
    """
    new not tested
    About this class.....
    make a color coded frame ( two frames one above the other )
    with a title in the top one and color coded
    see ex_tk_frame.py for the master
    """
    #----------- init -----------
    def __init__( self, a_parent_frame,
                  a_title,
                  a_title_color,
                  button_width = 10,
                  button_height = 2 ):
        """
        Usual init see class doc string
        add to gui_ext !!
        """
        a_frame      = tk.Frame( a_parent_frame,
                                 # bg ="red",
                                 bg = "gray", )

        a_frame.rowconfigure(    0, weight= 1 )
        a_frame.rowconfigure(    1, weight= 1 )

        a_frame.columnconfigure( 0, weight= 1 )
        #master.columnconfigure( 1, weight= 1 )
        self.frame      = a_frame
        p_frame         = a_frame

        a_frame  = tk.Frame( p_frame,   bg = a_title_color, )
            # padx = 2, pady = 2, relief= tk.GROOVE, )
        a_frame.grid( row = 0,  column = 0 ,sticky = tk.E + tk.W )
        self.top_inner_frame    = a_frame

        a_label             = ttk.Label( a_frame,
                                        text    = a_title,
                                        #bg      = a_title_color ,
                                        )
                                     #   relief = RAISED,  )
        a_label.grid( row = 0, column = 0, )
            # columnspan = 1, sticky = tk.W + tk.E )

        a_frame  = ttk.Frame( p_frame,   )
            # bg = "blue", )  # use neutral color or the title color
            # padx = 2, pady = 2, relief= tk.GROOVE, )
        a_frame.grid( row = 1,  column = 0,sticky = tk.E + tk.W )
        self.bottom_inner_frame    = a_frame

        self.button_width  = button_width
        self.button_height = button_height
        self.button_row    = 0
        self.button_column = 0

    #----------------------------------------------------------------------
    def make_button( self, button_text = "default text", command = None ):
        """
        !! have function make the button with the command
        !! may not be best way to do, may just want to return inner frame
        """
        a_button = ttk.Button( self.bottom_inner_frame ,
                             width     = self.button_width,
                             #height    = self.button_height,
                             text      = button_text )
        a_button.grid( row  = self.button_row, column = self.button_column )
        self.button_column += 1

        if command is not None:
            a_button.config( command = command  )

        return a_button

#----------------------------------------------------------------------
def make_titled_listbox( parent_frame, a_title ):
    """
    for snips and snippets?
    return ( famelike_thing, listbox_thing)  ?? make a class, better access to components
    widget like built in its own frame
    """
    a_frame      = ttk.Frame(parent_frame)
    a_listbox    = tk.Listbox( a_frame, height = 5 )
    a_listbox.grid( column=0, row=1, sticky = STICKY_ALL )

    s = ttk.Scrollbar( a_frame, orient=tk.VERTICAL, command=a_listbox.yview)
    s.grid( column=1, row = 1, sticky = ( tk.N, tk.S ))
    a_listbox['yscrollcommand'] = s.set

    a_label = ttk.Label( a_frame, text= a_title )
    a_label.grid( column=0, row=0, sticky=( tk.N, tk.E, tk.W) )
    #  ttk.Sizegrip().grid(column=1, row=1, sticky=(tk.S, tk.E)) size grip not appropriate here

    a_frame.grid_columnconfigure( 0, weight=1 )
    a_frame.grid_rowconfigure(    0, weight=0 )
    a_frame.grid_rowconfigure(    1, weight=1 )
    return ( a_frame, a_listbox )

# both of these in use !! why or explain

    #----------------------------------------------------------------------
    def make_button( self, button_text = "default text", command = None ):
        """
        !! have function make the button with the command
        or is this just unreachable
        """
        a_button = ttk.Button( self.bottom_inner_frame ,
                             width      = self.button_width,
                            # height     = self.button_height,
                             text       = button_text )
        a_button.grid( row  = self.button_row, column = self.button_column )
        self.button_column += 1

        if command is not None:
            a_button.config( command = command  )

        return a_button

# # ----------------------------------------
# class ComboboxHistory( ttk.Combobox ):
#     """
#     combo box with a ddl of its history
#         set_values        # not config( values =
#         get_text( self )  # always use this or history will not be updated
#         max_history

#         config(   height
#                   width

#     """

#     # ----------------------------------------
#     def __init__( self, parent, values = None, width  = None ):
#         """
#         reduced init, use config or enhance this



#         """
#         super().__init__( parent, values = values, width = width )

#         self.the_values    = values           # may already be available in widget
#         self.get_var       = tk.StringVar()   # consider drop
#         self.max_history   = 15

#         self.config( height = self.max_history )

#         self.config( textvariable  =  self.get_var )
#         self.bind("<<ComboboxSelected>>", self._cb_selected )
#         self.bind('<Return>', self.enter_event )   # return = enter key

#     # ----------------------------------------
#     def set_values( self,  values ):
#         """
#         use instead of the usual config ( values = )

#         """
#         #rint( f"set_values -> {values}")
#         self.the_values     = values
#         self.config( values = values )

#     # ----------------------------------------
#     def enter_event( self,  event ):
#         """
#         a function to explore events, not all may work

#         """
#         #rint( f"enter_event -> {event}")

#     # ------------------------------
#     def __str__( self ):

#         a_str   = f"__class__.__name__         = {self.__class__.__name__} "

#         a_str   = f"{a_str}\n      max_history = {self.max_history}"
#         #a_str   = f"{a_str}\n      max_history = {self.max_history}"
#         # a_str   = f"{a_str}\n      cap        value = {self._value_c}"
#         return a_str

#     # ------------------------------
#     def _cb_selected_2( self,  event ):
#         """
#         call back see which control attached to above
#         should be on change or any value selected in the combobox

#         """
#         print( "cb_selected_2() replace with your callback" )

#     # ------------------------------
#     def _cb_selected( self,  event ):
#         """
#         call back see which control attached to above
#         should be on change or any value selected in the combobox

#         """
#         msg   = f"cb_selected >{event}<"
#         print( msg )

#         msg = f"cb_selected value is via get >{ self.get( ) }<"
#         print( msg )

#         msg = f"cb_selected value is via variable get >{ self.get_var.get( ) }<"
#         print( msg )

#         self._cb_selected_2( event )

#     # --------------
#     def get_text( self ):
#         """
#         Purpose:
#             get the current text and add it to the history
#             limit history to max
#             note: strip

#         """
#         current_text   = self.get().strip()
#         #rint( f"get_text  current_text {current_text}" )

#         if current_text == self.the_values[0]:
#             return current_text

#         self.the_values.insert( 0, current_text)

#         if len( self.the_values  ) > self.max_history:
#             self.the_values   = self.the_values[ :self.max_history ]   # or mutate it

#         self.config( values = self.the_values )

#         return current_text

# #----------------------------------------
# # ----  class ... actually for real work, will move master to.....
# class FileTreeview( ttk.Frame ):
#     """
#     see also ex_ttk_treeview.py

#     Add:
#         columns for date and size
#         ability to sort
#         ability to filter
#         callbacks
#         multiple selections
#         update
#         ...

#     """

#     def __init__(self, master, path):
#         ttk.Frame.__init__( self, master)

#         self.config( bg = "red")
#         treeview        = ttk.Treeview(self)
#         self.treeview   = treeview
#         ysb             = ttk.Scrollbar(self, orient='vertical',    command = treeview.yview )
#         xsb             = ttk.Scrollbar(self, orient='horizontal',  command = treeview.xview )

#         treeview.configure( yscroll=ysb.set, xscroll=xsb.set)
#         treeview.heading('#0', text = path, anchor = 'w')    #0   = index to col heading

#         abspath     = os.path.abspath(path)
#         root_node   = treeview.insert( '', 'end', text=abspath, open=True )

#         # consider wait cursor...
#         print( f"for init call to process_dir root_node = {root_node}, abspath = {abspath} please wait a bit.....")
#         self.process_directory( root_node, abspath )

#         treeview.grid( row=0, column=0, sticky = "nsew" )
#         ysb.grid(row=0, column=1, sticky='ns')
#         xsb.grid(row=1, column=0, sticky='ew')

#         self.rowconfigure(    0, weight= 1 )
#         self.columnconfigure( 0, weight= 1 )

#         treeview.bind( "<<TreeviewSelect>>", self.on_select )

#     # ----------------------------------
#     def on_select_cb( self, full_path, full_path_list = None,   event = None ):
#         """
#         !! not written, does what

#         """
#         print( f"on_select_cb:")
#         print( f"full_path {full_path}, full_path_list: {full_path_list} event: {event}")

#     # ----------------------------------
#     def on_select( self, event ):
#         """
#         from: ex_working_from_web may be below


#         """
#         item     = self.treeview.identify( 'item', event.x, event.y )
#         cur_item = self.treeview.focus()
#         #rint( f" self.treeview.item(cur_item) =  {self.treeview.item(cur_item)}" )

#         #while True:
#         full_path_list   = []
#         for ix in range( 20 ): # limit on while True  do some other way

#             if cur_item =="":
#                 #rint( "cur_item is empty string" )
#                 break   # perhaps throw exception
#             else:
#                 #rint( f"cur_item  = {repr(cur_item)}")
#                 #rint( f" self.treeview.item(cur_item) =  {self.treeview.item(cur_item)}" )
#                 this_text     = self.treeview.item(cur_item)["text"]
#                 #full_path_list.append(this_text)
#                 full_path_list.insert( 0, this_text)
#                 #rint( f"this_text = {this_text}")
#                 cur_item    = self.treeview.parent( cur_item )
#             #rint( full_path_list )

#         full_path  = "\\".join( full_path_list )
#         #rint( f"File Treeview on_select: this is the full_path ={full_path}" )
#         self.on_select_cb( full_path, full_path_list = full_path_list,   event = event )

#     # ----------------------------------
#     def filter_file_cb( self, p, path, isdir ):
#         """
#         use as callback for file filtering, try to use file_filters
#         return True for ok
#         """
#         return True

#     # ----------------------------------
#     def process_directory(self, parent, path ):
#         """
#         parent  -- determines the location of the insert is a node int the treevie see oid and
#         initial call
#         path -- directory, path full? to build
#         populate the directories with files and call recursivelly to get
#         all subdirectories, this can take a lot of memory and possibly
#         time
#         does not check for a refresh
#         !! bad names
#         """
#         #rint( f"process_directory path = {path}")

#         for p in os.listdir( path ):
#             abspath     = os.path.join( path, p )
#             isdir       = os.path.isdir( abspath )
#             include_ok  = self.filter_file_cb( p, path, isdir )

#             oid         = self.treeview.insert( parent, 'end', text=p, open=False )

#             """
#             tree.insert('', 'end',text="1",values=('1','C++'))
#             tree.insert('', 'end',text="2",values=('2', 'Java'))
#             tree.insert('', 'end',text="3",values=('3', 'Python'))

#             search on python ttk treeview insert text and values
#             """

#             if isdir:
#                 self.process_directory( oid, abspath )

# ---- ex_file_treeview
# ----------------------------------------
