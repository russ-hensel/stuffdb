#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""
Created on Sat Jul 13 15:31:33 2024

@author: chat

photo_viewer.PhotoViewer()

NOT USED IN STUFF, MAY BE BROKEN SEE PICTURE VIEWER INSTEAD
REMOVE 1/0 IF YOU WANT TO RUN

"""
# --------------------
if __name__ == "__main__":
    pass
# --------------------
1/0

from   pathlib import Path
#import sys
from   qtpy.QtWidgets import (
                            QGraphicsView,
                            QGraphicsScene,
                            QFrame,
                            QGraphicsPixmapItem,
                            QMenu,
                                )

from   qtpy.QtGui import  ( QPixmap, QPainter )
from   qtpy.QtGui import ( QPalette )

#from qtpy.QtCore import Qt, QRectF
from   qtpy.QtCore import (Qt, QTimer, Signal, QRectF,  )

import vlc
from   app_global import AppGlobal

#-----------------------------------------------
class VlcVideoFrame( QFrame ):
    """
    a QFrame that is both the vlc video surface ( libvlc paints directly
    into its native/X11 window via set_xwindow() ) and the owner of the
    vlc instance/player -- all the vlc-specific plumbing from
    tab_vlc_qt_widget.py lives here instead of in the tab class, so this
    widget can be dropped into any other tab/window as a self-contained
    "play a video" widget
    """

    # libvlc fires these on its own internal thread, not the Qt main thread --
    # emitting a signal from that thread queues the slot call onto the main
    # thread instead of touching widgets directly from a foreign thread
    vlc_state_signal        = Signal( str )

    def __init__( self, parent = None ):
        """
        """
        super().__init__( parent )

        # libvlc paints directly into this frame's native window, bypassing
        # Qt's own paint system, so give it a black background rather than
        # leave the default widget fill showing through before playback starts
        self.setMinimumHeight( 300 )
        self.setAutoFillBackground( True )
        a_palette           = self.palette()
        a_palette.setColor( QPalette.Window, Qt.black )
        self.setPalette( a_palette )

        self.vlc_embedded   = False    # set_xwindow() done lazily, see _ensure_embedded

        # ---- libvlc instance/player -- unlike QMediaPlayer these are not
        # owned/cleaned-up by Qt
        vlc_instance         = vlc.Instance()
        vlc_player           = vlc_instance.media_player_new()
        self.vlc_instance    = vlc_instance
        self.vlc_player      = vlc_player

        event_manager        = vlc_player.event_manager()
        event_manager.event_attach( vlc.EventType.MediaPlayerPlaying,          self._vlc_on_playing )
        event_manager.event_attach( vlc.EventType.MediaPlayerPaused,           self._vlc_on_paused )
        event_manager.event_attach( vlc.EventType.MediaPlayerStopped,          self._vlc_on_stopped )
        event_manager.event_attach( vlc.EventType.MediaPlayerEndReached,       self._vlc_on_end_reached )
        event_manager.event_attach( vlc.EventType.MediaPlayerEncounteredError, self._vlc_on_error )

    # -------------------------------------
    def _ensure_embedded( self, ):
        """
        read it -- hook libvlc's rendering into this frame's native
        ( X11 ) window. done lazily on first play rather than in __init__
        since winId() should be called after this frame is part of a
        shown widget hierarchy, and a widget is normally constructed
        before its parent window has shown anything
        """
        if self.vlc_embedded:
            return

        win_id              = int( self.winId() )
        self.vlc_player.set_xwindow( win_id )
        self.vlc_embedded   = True

    # -------------------------------------
    def set_video( self, file_name ):
        """
        what it says -- load   file_name
        """
        self._ensure_embedded()

        media               = self.vlc_instance.media_new( file_name )
        self.vlc_player.set_media( media )
        # self.vlc_player.play()

    # -------------------------------------
    def play( self, file_name = None ):
        """
        what it says -- load and play file_name
        """
        self._ensure_embedded()
        if file_name is not None:
            media               = self.vlc_instance.media_new( file_name )
            self.vlc_player.set_media( media )
            # or call above
        self.vlc_player.play()

    # -------------------------------------
    def pause( self, ):
        """ what it says -- toggle pause/resume ( libvlc's own pause() behavior ) """
        self.vlc_player.pause()

    # -------------------------------------
    def stop( self, ):
        """ what it says """
        self.vlc_player.stop()

    # -------------------------------------
    def get_time_ms( self, ):
        """ current playback position in ms, -1 if unknown """
        return self.vlc_player.get_time()

    # -------------------------------------
    def get_length_ms( self, ):
        """ media length in ms, -1 if unknown """
        return self.vlc_player.get_length()

    # -------------------------------------
    def seek_to_ms( self, ms ):
        """ what it says """
        self.vlc_player.set_time( int( ms ) )

    # -------------------------------------
    def set_volume( self, value ):
        """ value is 0-100 """
        self.vlc_player.audio_set_volume( value )

    # -------------------------------------
    def get_volume( self, ):
        """ what it says, 0-100 """
        return self.vlc_player.audio_get_volume()

    # -------------------------------------
    def _vlc_on_playing( self, event ):
        """ called on a libvlc thread -- just marshal to Qt via signal """
        self.vlc_state_signal.emit( "playing" )

    # -------------------------------------
    def _vlc_on_paused( self, event ):
        """ called on a libvlc thread -- just marshal to Qt via signal """
        self.vlc_state_signal.emit( "paused" )

    # -------------------------------------
    def _vlc_on_stopped( self, event ):
        """ called on a libvlc thread -- just marshal to Qt via signal """
        self.vlc_state_signal.emit( "stopped" )

    # -------------------------------------
    def _vlc_on_end_reached( self, event ):
        """ called on a libvlc thread -- just marshal to Qt via signal """
        self.vlc_state_signal.emit( "end reached" )

    # -------------------------------------
    def _vlc_on_error( self, event ):
        """ called on a libvlc thread -- just marshal to Qt via signal """
        err_msg             = vlc.libvlc_errmsg()    # often None, libvlc is inconsistent about setting this
        err_msg             = err_msg.decode() if err_msg else "unknown libvlc error"
        self.vlc_state_signal.emit( f"error: {err_msg}" )


# ------------------------------------------------
class PhotoViewer( QGraphicsView ):

    #--------------------------
    def __init__( self, parent = None ):
        """
        """
        super( PhotoViewer, self ).__init__( parent )
        self.scene              = QGraphicsScene(self)
        self.setScene( self.scene )
        self.pixmap_item        = QGraphicsPixmapItem()
        self.scene.addItem( self.pixmap_item )

        self.setRenderHint( QPainter.Antialiasing )
        self.setRenderHint( QPainter.SmoothPixmapTransform )
        self.setTransformationAnchor( QGraphicsView.AnchorUnderMouse )
        self.setResizeAnchor( QGraphicsView.AnchorUnderMouse )
        self.vlc_media_frame    = None   # if present for mp4......
            # interface  photo_viewer.vlc_media_frame   = xxx

    # -----------------------------
    def display_file( self, file_name  ):
        """
        what it says, read
            untested, prrhaps you menat picture_viewer
        """
        file_name     = file_name
        file_path     = Path( file_name )
        ext           = file_path.suffix.lower()
        ext           = file_path.suffix.lower()
        if ext in [ ".mp4" ]:
            # we may be able to do the cover art so lets do that even if
            # we cannot do the mp4
            #
            file_path_png   = file_path.joinpath( file_path.parent, file_path.stem  +  ".png" )
                # this is the cover file, but it may not exist so ...
            if not Path( file_path_png ).exists():
                file_path_png   = AppGlobal.parameters.motion_picture_cv_file_name
                # if this does not exist then config error
            # have cover art or art not found

            vlc_media_frame   = self.vlc_media_frame

            if vlc_media_frame:
                if Path( file_name ).exists():
                    vlc_media_frame.set_video( )

            self.display_file_base( file_path_png )
                # the cover art

        else:
            self.display_file_base( file_name )
                # the file

    # -----------------------------
    def display_file_base( self,  file_name ):
        """
        what it says, read
            do not feed mp4....
            file_name  file to display, limit to displayable files
            was display_file
        """
        pixmap      = QPixmap( file_name )
        ok          = self.set_pixmap( pixmap )
        if not ok:
            print( f"display_file error    { file_name = }")
        else:
            #rint( f"display_   { file_name = }")
            pass
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
            print("Failed to load image pixmap is null")
            return False

    # -----------------------------
    def photo_1(self):
        self.display_file( "/mnt/WIN_D/PhotoDB/02/102-0253_img.jpg" )

    # -----------------------------
    def photo_2(self):
        self.display_file( "/mnt/WIN_D/PhotoDB/02/102_motor2.jpg" )

    # -----------------------------
    def zoom_in(self):
        self.scale(1.2, 1.2)
        #p#rint("Zoomed In")

    # -----------------------------
    def zoom_out(self):
        self.scale(0.8, 0.8)
        #rint("Zoomed Out")

    # -----------------------------
    def reset_zoom(self):
        self.resetTransform()
        #rint("Zoom Reset")

    # -----------------------------
    def fit_in_view(self):
        pass
        self.fitInView( self.scene.sceneRect(), Qt.KeepAspectRatio )
        #rint("Fit in View")
        pass

    # -----------------------------
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fit_in_view()
        #rint("Window Resized and Image Fit in View")

    # -----------------------------
    def contextMenuEvent(self, event):
        context_menu        = QMenu(self)

        zoom_in_action      = context_menu.addAction("Zoom In")
        zoom_out_action     = context_menu.addAction("Zoom Out")
        reset_zoom_action   = context_menu.addAction("Reset Zoom")
        fit_in_view_action  = context_menu.addAction("Fit in View")

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



# ---- eof


