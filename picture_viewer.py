#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 15:31:33 2024



came from
photo_viewer.Photo-----Viewer()


"""
# ---- tof
# --------------------
if __name__ == "__main__":
    import main  # noqa  stops auto removal by pycln
# --------------------
# ---- import
import logging
import os
from pathlib import Path

import vlc_widget
from qtpy.QtCore import QMimeData, QRectF, Qt, QTimer, QUrl, Signal
from qtpy.QtGui import QDrag, QImageReader, QPainter, QPalette, QPixmap
from qtpy.QtWidgets import (QApplication,
                            QFrame,
                            QGraphicsPixmapItem,
                            QGraphicsScene,
                            QGraphicsView,
                            QHBoxLayout,
                            QLabel,
                            QMenu,
                            QPushButton,
                            QSizePolicy,
                            QSlider,
                            QTabWidget,
                            QTextEdit,
                            QVBoxLayout,
                            QWidget)

#import vlc
from app_global import AppGlobal

# from   qtpy.QtWidgets import (
#                             QGraphicsView,
#                             QGraphicsScene,
#                             QFrame,
#                             QGraphicsPixmapItem,
#                             QMenu,
#                                 )


#from qtpy.QtCore import Qt, QRectF
# from   qtpy.QtCore import (Qt, QTimer, Signal, QRectF,  )



logger          = logging.getLogger( )
# for custom logging level at module
LOG_LEVEL  = 10   # higher is more

# -----------------------------
def load_pixmap_exif_corrected( file_name ):
    """
    what it says, read
    QPixmap( file_name ) ignores EXIF orientation, so photos taken in
    portrait come in rotated 90 -- xviewer and friends apply it, we did not
    """
    reader          = QImageReader( file_name )
    reader.setAutoTransform( True )
    image           = reader.read()
    pixmap          = QPixmap.fromImage( image )
    return pixmap

# -----------------------------
class PictureViewer( QGraphicsView ):
    def __init__(self, parent=None):
        """
        what it says, read it
        used like where
            stuffdb picture document i think
                may be in qt5 by example
        """
        super( PictureViewer, self ).__init__(parent)
        self.scene          = QGraphicsScene(self)
        self.setScene( self.scene )
        self.pixmap_item    = QGraphicsPixmapItem()

        self.pixmap         = QPixmap( "" )  # initial null item
        self.scene.addItem( self.pixmap_item )

        #self.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Expanding )
        self.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Expanding )

        #
        sb_policy           = Qt.ScrollBarAlwaysOn

            #  Qt.ScrollBarAsNeeded Qt.ScrollBarAlwaysOff  Qt.ScrollBarAlwaysOn
        self.setHorizontalScrollBarPolicy(  sb_policy )
        self.setVerticalScrollBarPolicy(    sb_policy )

        # # Set the scene for the view  -- does this need to be done again
        # self.view.setScene(self.scene)

        self.setRenderHint( QPainter.Antialiasing )
        self.setRenderHint( QPainter.SmoothPixmapTransform )
        self.setTransformationAnchor( QGraphicsView.AnchorUnderMouse )
        self.setResizeAnchor( QGraphicsView.AnchorUnderMouse )

        # ---- drag
        # drag with left mouse button to pan the image
        self.setDragMode( QGraphicsView.ScrollHandDrag )

        # once the user zooms manually, stop auto fit on resize/show
        # cleared by display_file() and the Fit in View menu action
        self.user_zoomed            = False

        self.file_name              = None
        self.file_name_not_found    = AppGlobal.parameters.picture_nf_file_name
        self.vlc_video_widget       = None

    # -----------------------------
    def display_file( self, file_name  ):
        """
        what it says, read
            deal with mp4, and thumbnails

        """
        file_name     = file_name
        file_path     = Path( file_name )
        ext           = file_path.suffix.lower()

        if ext in [ ".mp4" ]:
            # we may be able to do the thumbnail so lets do that even if
            # we cannot do the mp4

            file_path_thumb   = file_path.joinpath( file_path.parent, file_path.stem  +  ".png" )
                # this is the cover file, but it may not exist so ...

            if not Path( file_path_thumb ).exists():
                file_path_thumb   = AppGlobal.parameters.video_thumb_nf_file_name
                    # if this does not exist then config error
                    # have thumbnail art or art not found

            vlc_video_widget   = self.vlc_video_widget

            if vlc_video_widget:
                if Path( file_name ).exists():
                    vlc_video_widget.load( file_name )

            self.display_file_base( file_path_thumb )

        else:
            self.display_file_base( file_name )
                # the file is a "picture"


    # -----------------------------
    def display_file_base( self, file_name ):
        """
        what it says, read
        """
        self.file_name  = file_name
        pixmap          = load_pixmap_exif_corrected( file_name )
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

        self.user_zoomed    = False
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
    def display_file_fnf( self, ):
        """
        what it says

        """
        file_name       = self.file_name_not_found
        self.display_file( file_name )

    # -----------------------------
    def display_fnf( self, ):
        """
        what
        no error checking here
        not sure if use, did not do what I wanted so added display_file_fnf
        """
        file_name       = self.file_name_not_found
        self.file_name  = file_name
        pixmap          = load_pixmap_exif_corrected( file_name )

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


    # -----------------------------
    def wheelEvent( self, event ):
        """
        zoom with the mouse wheel, up zooms in, down zooms out
        factors are exact inverses so in then out returns to start
        zoom centers on the mouse from AnchorUnderMouse in __init__
        """
        delta      = event.angleDelta().y()
        if delta > 0:
            zoom   = 1.25
        else:
            zoom   = 0.8

        self.user_zoomed    = True
        self.scale( zoom, zoom )

    # -----------------------------
    def zoom_in(self):
        """
        what it says, read it
        """
        self.user_zoomed    = True
        self.scale(1.5, 1.5)
        #p#rint("Zoomed In")

    # -----------------------------
    def zoom_out(self):
        """
        what it says, read it
        """
        self.user_zoomed    = True
        self.scale(0.75, 0.75)
        #rint("Zoomed Out")

    # -----------------------------
    def reset_zoom(self):
        """
        what it says, read it
        """
        self.user_zoomed    = True   # 1:1 is a manual choice, keep it on resize
        self.resetTransform()
        #rint("Zoom Reset")

    # -----------------------------
    def fit_image_may(self):
        """
        new in may, older grok code not working
            this seem to do what i want always can see all of picture
        """
        if self.pixmap_item:
            self.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)

    # -----------------------------
    def fit_in_view( self ):
        """
        what it says, read it
        but what does it mean
            a redirect for experiment
            seems to get called all to often debug !!
        """
        #self.fit_image()
        self.fit_image_may()

        #self.fitInView( self.scene.sceneRect(), Qt.KeepAspectRatio)
        #rint("Fit in View")

    # -----------------------------
    def fit_in_view_1( self ):
        """
        what it says, read it
        but what does it mean
        """
        self.fitInView( self.scene.sceneRect(), Qt.KeepAspectRatio)
        #rint("Fit in View")

    # ------------------------------------
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.user_zoomed:
            self.fit_in_view()

    # ------------------------------------
    def showEvent(self, event):
        super().showEvent(event)
        if not self.user_zoomed:
            self.fit_in_view()  # fit once widget is visible and sized

    # ------------------------------------
    def mousePressEvent( self, event ):
        """
        what it says, read it
        Ctrl + left-drag starts an outbound file drag of self.file_name
        ( to a file manager, email, gimp, etc ) -- plain left-drag is left
        alone so it keeps panning ( see ScrollHandDrag in __init__ )
        """
        ctrl_held       = bool( event.modifiers() & Qt.ControlModifier )
        left_button     = event.button() == Qt.LeftButton

        if ctrl_held and left_button and self.file_name:
            self.start_file_drag()
            return

        super().mousePressEvent( event )

    # ------------------------------------
    def start_file_drag( self ):
        """
        what it says, read it
        drags self.file_name out as a file url -- source only for now,
        this widget does not accept drops
        """
        file_path       = Path( self.file_name )

        if not file_path.exists():
            return

        mime_data       = QMimeData()
        mime_data.setUrls( [ QUrl.fromLocalFile( str( file_path ) ) ] )

        thumb           = self.pixmap.scaled( 100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation )

        drag            = QDrag( self )
        drag.setMimeData( mime_data )
        drag.setPixmap( thumb )
        drag.exec_( Qt.CopyAction )

    # ------------------------------------
    def get_file_name( self, event ):
        """
        just debug
        """
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
        drag_file_action    = context_menu.addAction("Drag Image File Out")

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
            self.user_zoomed    = False   # auto fit on resize/show resumes
            self.fit_in_view()
        elif action == photo_1_action:
            self.photo_1()
        elif action == photo_2_action:
            self.photo_2()
        elif action == get_file_name_action:
            self.clip_file_name( )
        elif action == drag_file_action:
            self.start_file_drag( )

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


    # ----------------------------------
    def add_video( self, video_widget ):
        """
        to the PictureViewer
        """
        self.vlc_video_widget    = video_widget


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

        widget =    picture_viewer.PictureViewerPlus( parent = )  # import picture_viewer

    QWidget
    QGraphicsView
    used like where
            may be in qt5 by example

    """

    # ----------------------------------
    def __init__(self, parent = None):
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
        some half baked idea does what ??
        """
        fn      = self.picture_viewer_widget.file_name
        info    = fn

        self.info_widget.clear()
        cursor  = self.info_widget.textCursor()
        cursor.insertText( info )

    # ----------------------------------
    def add_video( self,  video_widget ):
        """
        to the PictureViewer
        """
        self.picture_viewer_widget.add_video( video_widget )

# ---- eof



