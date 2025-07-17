#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 15:31:33 2024

@author: chat

photo_viewer.PhotoViewer()

I have a QGraphicsView
I would like the graphics in it to fill the layout area.
I would like some code to do this:

"""
# --------------------
if __name__ == "__main__":
    import main
    main.main()
import logging
import os
# --------------------
# ---- import
import sys

from app_global import AppGlobal
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QPainter, QPixmap
# ----QtWidgets
from PyQt5.QtWidgets import (QAction,
                             QActionGroup,
                             QApplication,
                             QButtonGroup,
                             QDateEdit,
                             QDockWidget,
                             QGraphicsPixmapItem,
                             QGraphicsScene,
                             QGraphicsView,
                             QLabel,
                             QLineEdit,
                             QListWidget,
                             QMainWindow,
                             QMdiSubWindow,
                             QMenu,
                             QMessageBox,
                             QPushButton,
                             QSizePolicy,
                             QSpinBox,
                             QTabWidget,
                             QTextEdit,
                             QVBoxLayout,
                             QWidget)

logger          = logging.getLogger( )

# for custom logging level at module
LOG_LEVEL  = 10   # higher is more


# -------------------------------------
class PictureViewer( QGraphicsView ):
    def __init__(self, parent=None):
        """
        what it says, read it
        used like where
            stuffdb picture document i think
                may be in qt5 by example
        """
        super( PictureViewer, self).__init__(parent)
        self.scene          = QGraphicsScene(self)
        self.setScene( self.scene )
        self.pixmap_item    = QGraphicsPixmapItem()

        self.pixmap         = QPixmap( "" )  # initial null item
        self.scene.addItem( self.pixmap_item )
        self.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Expanding )

        #
        sb_policy           = Qt.ScrollBarAlwaysOn
            #  Qt.ScrollBarAsNeeded Qt.ScrollBarAlwaysOff  Qt.ScrollBarAlwaysOn
        self.setHorizontalScrollBarPolicy(  sb_policy )
        self.setVerticalScrollBarPolicy(    sb_policy )

        # # Set the scene for the view  -- does this need to be done again
        # self.view.setScene(self.scene)

        self.setRenderHint( QPainter.Antialiasing )
        self.setRenderHint( QPainter.SmoothPixmapTransform)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor( QGraphicsView.AnchorUnderMouse )
        self.file_name              = None
        self.file_name_not_found    = None

    # -----------------------------
    def display_file( self,  file_name ):
        """
        what it says, read
        """
        self.file_name  = file_name
        pixmap          = QPixmap( file_name )
        self.pixmap     = pixmap
        ok              = self.set_pixmap( pixmap )
        if not ok:
            if file_name is None:
                file_exists   = False
            else:
                file_exists   = os.path.exists( file_name )
            debug_msg   = (  f"PictureViewer display_file error    { file_name = } {file_exists = }")
            logging.log( LOG_LEVEL,  debug_msg, )

            self.clear()

        else:
            #rint( f"display_   { file_name = }")
            pass

        self.fit_in_view()


    # -----------------------------
    def set_fnf( self,  file_name ):
        """
        what it says, read
        this is the file to use if not found
        might want to check for its exist
        good to set at create time

        """
        self.file_name_not_found     = file_name

    # -----------------------------
    def display_fnf( self,    ):
        """
        what
        no error checking here
        """
        file_name       = self.file_name_not_found
        self.file_name  = file_name
        pixmap          = QPixmap( file_name )

        self.pixmap     = pixmap
        ok              = self.set_pixmap( pixmap )
        self.fit_in_view()

    # -----------------------------
    def set_pixmap( self, pixmap ):
        """
        what it says, but keep separate or merge into display_file
        pixmap may be useful for other viewer
        """
        if not pixmap.isNull():
            self.pixmap_item.setPixmap(pixmap)
            self.setSceneRect(QRectF(pixmap.rect()))  # Convert QRect to QRectF
            #rint(f"Image set: {pixmap.size()}")
            self.fit_in_view()  # Automatically fit the image to view when loaded\\\\\\
            return True
        else:
            debug_msg   = ( "PictureViewer Failed to load image pixmap is null")
            logging.log( LOG_LEVEL,  debug_msg, )

            return False

    # # -----------------------------
    # def photo_1(self):
    #     self.display_file( "/mnt/WIN_D/PhotoDB/02/102-0253_img.jpg" )

    # # -----------------------------
    # def photo_2(self):
    #     self.display_file( "/mnt/WIN_D/PhotoDB/02/102_motor2.jpg" )

    def zoom_in(self):
        """
        what it says, read it
        """
        self.scale(1.5, 1.5)
        #p#rint("Zoomed In")
    # -----------------------------
    def zoom_out(self):
        """
        what it says, read it
        """
        self.scale(0.75, 0.75)
        #rint("Zoomed Out")

    def reset_zoom(self):
        self.resetTransform()
        #rint("Zoom Reset")


    def fit_image(self):
            """From Grok
            Scale the image to fill the view while maintaining aspect ratio."""
            if not self.pixmap.isNull():
                # Get the view's viewport size
                view_rect = self.viewport().rect()
                # Get the pixmap's bounding rectangle
                pixmap_rect = QRectF(self.pixmap_item.pixmap().rect())
                # Fit the pixmap in the view
                self.fitInView( pixmap_rect, Qt.KeepAspectRatioByExpanding )
                # Center the scene in the view
                self.centerOn(self.pixmap_item)


    def fit_in_view( self ):
        """
        what it says, read it
        but what does it mean
        """
        self.fit_image()
        #self.fitInView( self.scene.sceneRect(), Qt.KeepAspectRatio)
        #rint("Fit in View")


    def fit_in_view_1( self ):
        """
        what it says, read it
        but what does it mean
        """
        self.fitInView( self.scene.sceneRect(), Qt.KeepAspectRatio)
        #rint("Fit in View")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fit_in_view()

    def get_file_name(self, event):
        """ """
        debug_msg    = ( "PictureViewer finish get_file_name {self.file_name = }" )
        logging.log( LOG_LEVEL,  debug_msg, )

    # ------------------------------------
    def clip_file_name( self,   ):
        """
        ?? clip some more inspect stuff
        """
        clipboard = QApplication.clipboard()

        # Set a string into the clipboard
        clipboard.setText( self.file_name )
        # debug_msg      = ( f"PictureViewer clip_file_name  { self.file_name = }" )
        # logging.log( LOG_LEVEL,  debug_msg, )

        #get_text_out   =   clipboard.text()

    # -----------------------------
    def contextMenuEvent(self, event):
        """
        what it says, read it
        """
        context_menu        = QMenu(self)

        zoom_in_action      = context_menu.addAction("Zoom In")
        zoom_out_action     = context_menu.addAction("Zoom Out")
        reset_zoom_action   = context_menu.addAction("Reset Zoom")
        fit_in_view_action  = context_menu.addAction("Fit in View")
        get_file_name_action  = context_menu.addAction("Clip File Name")

        photo_1_action      = context_menu.addAction("photo_1_action")
        photo_2_action      = context_menu.addAction("photo_2_action")

        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        if action == zoom_in_action:
            self.zoom_in()
        elif action == zoom_out_action:
            self.zoom_out()
        elif action == reset_zoom_action:
            self.reset_zoom()
        elif action == fit_in_view_action:
            self.fit_in_view()
        elif action == photo_1_action:
            self.photo_1()
        elif action == photo_2_action:
            self.photo_2()
        elif action == get_file_name_action:
            self.clip_file_name( )

    # ------------------------------------
    def clear( self,   ):
        """

        """
        scene   = QGraphicsScene()
        #view    = self( scene )
        scene.clear()

        # chat said
        #scene = QGraphicsScene()
        # view    = QGraphicsView( scene )

        # # Clear all items from the scene
        # scene.clear()

        # # Alternatively, if you want to completely clear and reset the scene
        # view.setScene(None)  # Unset the scene to clear it completely
        # scene = QGraphicsScene()  # Create a new empty scene
        # view.setScene(scene)  # Set the new empty scene to the view
        # ion == photo_1_action:
        #             self.photo_1()
        #         elif action == photo_2_action:
        #             self.photo_2()
        #         elif action == get_file_name_action:
        #             self.clip_file_name( )


# -------------------------------------
class PictureViewerPlus( QWidget ):

    """
    Why is ist plus ---
        seems to setup on a tab widget
        display_info ??
    what it says, read it
    will make it accept all the picture viewer stuff

    PictureViewer( QGraphicsView ):
        def __init__(self, parent=None):

    QWidget
    QGraphicsView
    used like where
            may be in qt5 by example

    """

    # ----------------------------------
    def __init__(self, parent=None):
        """
        what it says, read it
        """
       # super( PictureViewer, self).__init__(parent)
        super(   ).__init__( parent  )

        self.build_gui()

    # ----------------------------------
    def build_gui( self ):
        """
        main gui build method -- for some sub layout use other methods
        """
        layout          = QVBoxLayout( self  )

        self.tab_widget = QTabWidget()

        # self.tab_widget.currentChanged.connect(self.on_tab_changed)
        layout.addWidget( self.tab_widget   )

        title    = "Picture"
        tab      = self.build_tab_pic(  )
        self.tab_widget.addTab( tab, title  )

        title    = "Information"
        tab      = self.build_tab_info(  )
        self.tab_widget.addTab( tab, title  )

    # ----------------------------------
    def build_tab_pic( self ):
        """
        what it says
        """
        tab_page     = QWidget( )
        layout       = QVBoxLayout( tab_page  )

        self.picture_viewer_widget   = PictureViewer()
        layout.addWidget( self.picture_viewer_widget )
        file_name     = "/home/russ/Pictures/picture_2024-06-14_10-19-01.jpg"
        self.picture_viewer_widget.display_file(  file_name )

        return tab_page

    # ----------------------------------
    def build_tab_info( self ):
        """

        """
        tab_page             = QWidget(   )
        layout          = QVBoxLayout( tab_page  )
        self.a_layout   = layout

        # self.picture_viewer_widget   = PictureViewer()
        # layout.addWidget( self.picture_viewer_widget )

        widget              = QTextEdit()
        self.info_widget    = widget
        layout.addWidget( widget )


        # widget          = QLabel("Qlabel 1 ")
        # self.qlabel_1   = widget
        # layout.addWidget( self.qlabel_1 )

        # widget          = QLabel("Qlabel  2 ")
        # self.qlabel_2   = widget
        # layout.addWidget( self.qlabel_2 )

        # # widget          = QLabel("Qlabel  3 ")
        # # self.qlabel_3   = widget
        # # #widget.setLayoutDirection( Qt.RightToLeft )
        # # layout.addWidget( widget )

        return tab_page

    # ----------------------------------
    def __getattr__(self, name):
        """
        this is the magic that calls the date control functions
        from this object
        priority goes to this object then QDateEdit

        """
        if name in self.__dict__:
            return self[name]

        try:
            return getattr( self.picture_viewer_widget, name )

        except AttributeError:
            raise AttributeError(
                "'{}' object has no attribute '{}'".format(
                    self.__class__.__name__, name
                )
            )

    # ----------------------------------
    def display_info(self,  ):
        """
        some half baked idea does what
        """
        fn      = self.picture_viewer_widget.file_name
        info    = fn

        self.info_widget.clear()
        cursor  = self.info_widget.textCursor()
        cursor.insertText( info )

# ---- eof
