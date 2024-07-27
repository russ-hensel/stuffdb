#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 08:48:29 2024

@author: russ
"""

# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    main.main()

# --------------------



# ---- imports

import sys

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMdiArea,
    QMdiSubWindow,
    QPushButton,
    QAction,
    QMessageBox,
    QDateEdit,

    QMenu,
    QAction,
    QLineEdit,
    QActionGroup,
    QApplication,
    QDockWidget,
    QTabWidget,
    QFileDialog,
    QFrame,
    QInputDialog,
    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QSpinBox,
    QMdiSubWindow,
    QTextEdit,
    QButtonGroup,
    QCheckBox,
    QComboBox,
    )


from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu, QAction,
    QMdiArea,
    QMdiSubWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    )

from PyQt5.QtWidgets import (
    QAction,
    QActionGroup,
    QApplication,
    QDockWidget,
    QFileDialog,
    QFrame,
    QInputDialog,
    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QSpinBox,
    QMdiSubWindow,
    QTextEdit,
    )


from PyQt5.QtCore  import  (
    QTimer,
    QDate,
    pyqtSlot,
    Qt,
    QModelIndex,
  )



#from   functools import partial
import collections
import functools

from   app_global import AppGlobal

sys.path.append( r"D:\Russ\0000\python00\python3\_projects\rshlib"  )
sys.path.append( "../")  # not working today vscode
sys.path.append( "../rshlib" )  # just for rsh, harmless unless the directory
                                # exists on your computer, safe to delete it
# see comment in web_search.py
#sys.path.append( "/media/russ/j_sg_bigcase/sync_py_3/_projects/rshlib/" )

import  gui_qt_ext

MenuInfo   = collections.namedtuple( 'MenuInfo', "window, menu_item" )
    # name is first argument  --- second arg space sep or a tuple

an_example   = MenuInfo( window  = "aaa", menu_item = "bbb",   )     # no quotes on instance names
print( an_example.window )
#print( an_example [ window ] )

class MidManagement():
    """


    """
    def __init__( self, main_window ):
        self.main_window       = main_window
        print( f"hello from MidManagement {1}")
        #self.window_menu        = main_window.window_menu
        self.window_dict        = {}   # for now index by title

    # -------------------------
    def register_document( self, an_identifier_for_the_window  ):
        """
        when a new window is created
        replace add_new_menu_item

        """
        1/0


    # -------------------------
    def add_subwindow_chat( self ):
        """
        from chat_subwindow.py

        """
        mdi_area       = self.main_window.mdi_area
        # Create a sub-window
        sub_window = QMdiSubWindow()
        sub_window.setWindowTitle( "Sub Window with Notebooks" )

        # Central widget and layout for the sub-window
        sub_widget = QWidget()
        sub_layout = QVBoxLayout( sub_widget )
        sub_window.setWidget( sub_widget )
        # mdi_area.addSubWindow( sub_window )

        # First notebook
        notebook1 = QTabWidget()
        notebook1.addTab(self.create_tab_content("Content of Tab 1 - Notebook 1"), "Tab 1")
        notebook1.addTab(self.create_tab_content("Content of Tab 2 - Notebook 1"), "Tab 2")
        sub_layout.addWidget(notebook1)

        # Second notebook
        notebook2 = QTabWidget()
        notebook2.addTab(self.create_tab_content("Content of Tab 1 - Notebook 2"), "Tab 1")
        notebook2.addTab(self.create_tab_content("Content of Tab 2 - Notebook 2"), "Tab 2")
        sub_layout.addWidget(notebook2)

        mdi_area.addSubWindow( sub_window )
        sub_window.show()


        return

    # --------------------------------------
    def cascade_sub_windows( self, ):
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
    def tile_sub_windows( self, ):
        """
        what it says, read

        """
        mdi_area       = self.main_window.mdi_area
        mdi_area.tileSubWindows()

    # --------------------------------------
    def layer_sub_windows( self, ):
        """
        what it says, read

        """
        mdi_area       = self.main_window.mdi_area
        print( "working on layer_sub_windows")
        self.layer_sub_windows()


    def layer_sub_windows(self):
        # from chat
        mdi_area        = self.main_window.mdi_area
        mdi_area_size   = mdi_area.size()
        for sub_window in mdi_area.subWindowList():
            sub_window.resize( mdi_area_size )
            sub_window.showNormal()  # Ensure the sub-window is not maximized_area       = self.main_window.mdi_area


    # --------------------------------------
    def show_sub_window_by_title( self, sub_window_title):
        """
        what it says, read
        an_example   = MenuInfo( window  = "aaa", menu_item = "bbb",   )     # no quotes on instance names
        """
        sub_window    = self.window_dict[ sub_window_title ]

        sub_window.show()
        sub_window.setFocus()


    # --------------------------------------
    def show_sub_window( self, sub_window):
        """
        what it says, read



        """
        sub_window.show()
        sub_window.setFocus()

    # --------------------------------------
    def delete_menu_by_title( self, sub_window_title):
        """
        what it says, read
        """
        print( f"delete_menu_by_title {sub_window_title = }")
        #sub_window    = self.window_dict[ sub_window_title ]
        del self.window_dict[ sub_window_title ]

        self.delete_menu_item( sub_window_title )

    def delete_menu_item(self, title ):
        """
        from chat, modify to work here

        Returns:
            None.

        """
        #title = self.delete_item_input.text()
        if title:
            for action in self.window_menu.actions():
                if action.text() == title:
                    self.window_menu.removeAction(action)
                    msg      = f"Deleted menu item: {title}"
                    print( msg )
                    # self.status_label.setText(f"Deleted menu item: {title}")
                    #self.delete_item_input.clear()
                    return
            msg    = f"No menu item found with title: {title}"
            print( msg )
            #self.status_label.setText(f"No menu item found with title: {title}")
        else:
            msg   = "Please enter a menu item title to delete."
            #self.status_label.setText("Please enter a menu item title to delete.")
            print( msg )

    # --------------------------------------
    def remove_menu_item( self ):
        """
        from chat not so useful
        probably needs tweak to work in this context

        """
        actions = self.file_menu.actions()
        if actions:
            action_to_remove = actions[-1]  # Remove the last item added
            self.file_menu.removeAction(action_to_remove)
            QMessageBox.information(self, "Info", f"Removed item: {action_to_remove.text()}")
        else:
            QMessageBox.information(self, "Info", "No items to remove")

    # --------------------------------------
    def add_new_menu_item( self, title, subwindow ):
        """
        what it says, read.... more coming maybe
        assumes this is a new window
        title is used for id, would be good to use an object ref

        """
        self.window_dict[title]     = subwindow
        main_window                 = self.main_window
        #self.add_menu_item( title, main_window.window_menu )

        activate_window        = functools.partial( self.show_sub_window_by_title, title )

        #show_sub_window_by_title( self, sub_window_title):

        action    = QAction( title, self.main_window )
        #action.triggered.connect( lambda: self.menu_item_clicked( title ) )
        action.triggered.connect( activate_window )
        main_window.window_menu.addAction( action )

        # QMessageBox.information( main_window, "Info", f"New item added to the File menu {title}")


    def menu_item_clicked(self, name):
        """
        what it says, read.... more coming maybe

        """
        QMessageBox.information(self, "Info", f"You clicked on {name}")
