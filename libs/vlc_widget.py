#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""
vlc_widget.py

KEY_WORDS:      vlc widget mp4 video python-vlc libvlc QFrame object oop
WIDGETS:        VlcVideoFrame  ( a QFrame subclass that owns the vlc instance/player )
                VlcVideoWidget ( QWidget -- VlcVideoFrame + all the playback
                                 controls, a complete drop-in "video player" )
DESCRIPTION:    self-contained, reusable vlc video-playing widgets, factored
                out of tab_vlc_qt_object_widget.py so any tab/window can drop
                one in without pulling in that tab's demo-specific code.
MORE:           play local video via python-vlc, embedded via
                winId()/set_xwindow() -- all the vlc-specific code --
                instance, player, embedding, event marshaling,
                load/play/resume/pause/stop/seek/volume -- lives inside
                VlcVideoFrame( QFrame ). all the playback controls --
                status label, seek slider/time, volume, a Play/Pause
                toggle button, Stop button -- live inside VlcVideoWidget
                ( QWidget ), which wraps a VlcVideoFrame.
"""


# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main   # noqa  stops auto removal by pycln
# --------------------


import sys

import vlc

from qtpy.QtCore    import ( Qt, QTimer, Signal )
from qtpy.QtGui     import ( QPalette )
from qtpy.QtWidgets import (
                             QDoubleSpinBox,
                             QFrame,
                             QHBoxLayout,
                             QLabel,
                             QPushButton,
                             QSlider,
                             QStyle,
                             QVBoxLayout,
                             QWidget
                             )


# ---- end imports


#-----------------------------------------------
class VlcVideoFrame( QFrame ):
    """
    a QFrame that is both the vlc video surface ( libvlc paints directly
    into its native/X11 window via set_xwindow() ) and the owner of the
    vlc instance/player -- all the vlc-specific plumbing lives here instead
    of in a tab class, so this widget can be dropped into any other
    tab/window as a self-contained "play a video" widget
    a_video_frame  = vlc_widget.VlcVideoFrame()
    for a frame with all the playback controls, use VlcVideoWidget instead
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
        self.vlc_shut_down  = False    # set by shutdown(), guards against doing it twice

        # ---- libvlc instance/player -- unlike QMediaPlayer these are not
        # owned/cleaned-up by Qt, and its threads keep running ( including
        # audio ) even after this widget is gone unless shutdown() is called
        vlc_instance         = vlc.Instance()
        vlc_player           = vlc_instance.media_player_new()
        self.vlc_instance    = vlc_instance
        self.vlc_player      = vlc_player

        # the event types attached below are kept so shutdown() can detach
        # them -- each attach hands libvlc a bound method of self, which is
        # a reference cycle ( libvlc's C side -> self ) that would otherwise
        # keep this frame alive/undead even after nothing else references it
        vlc_event_types      = (
                                 vlc.EventType.MediaPlayerPlaying,
                                 vlc.EventType.MediaPlayerPaused,
                                 vlc.EventType.MediaPlayerStopped,
                                 vlc.EventType.MediaPlayerEndReached,
                                 vlc.EventType.MediaPlayerEncounteredError,
                                 )
        self.vlc_event_types = vlc_event_types

        event_manager        = vlc_player.event_manager()
        self.vlc_event_manager = event_manager
        event_manager.event_attach( vlc.EventType.MediaPlayerPlaying,          self._vlc_on_playing )
        event_manager.event_attach( vlc.EventType.MediaPlayerPaused,           self._vlc_on_paused )
        event_manager.event_attach( vlc.EventType.MediaPlayerStopped,          self._vlc_on_stopped )
        event_manager.event_attach( vlc.EventType.MediaPlayerEndReached,       self._vlc_on_end_reached )
        event_manager.event_attach( vlc.EventType.MediaPlayerEncounteredError, self._vlc_on_error )

    # -------------------------------------
    def _ensure_embedded( self, ):
        """
        read it -- hook libvlc's rendering into this frame's native
        window. done lazily on first play rather than in __init__
        since winId() should be called after this frame is part of a
        shown widget hierarchy, and a widget is normally constructed
        before its parent window has shown anything
        linux needs X11 ( or XWayland, QT_QPA_PLATFORM=xcb ) for set_xwindow
        """
        if self.vlc_embedded:
            return

        win_id              = int( self.winId() )

        if sys.platform.startswith( "win" ):
            self.vlc_player.set_hwnd( win_id )
        elif sys.platform == "darwin":
            self.vlc_player.set_nsobject( win_id )
        else:
            self.vlc_player.set_xwindow( win_id )

        self.vlc_embedded   = True

    # -------------------------------------
    def load( self, file_name ):
        """
        what it says -- load file_name but do NOT start playback ( unlike
        play() ). leaves the player in libvlc's "Opening"/"NothingSpecial"
        state until resume()/play() actually starts it -- useful when a
        caller wants to pick a file and let the user press Play separately
        """
        self._ensure_embedded()

        media               = self.vlc_instance.media_new( file_name )
        self.vlc_player.set_media( media )

    # -------------------------------------
    def play( self, file_name ):
        """
        what it says -- load and immediately play file_name. for
        load-without-playing ( then starting later via resume() ), use
        load() instead
        """
        self.load( file_name )
        self.vlc_player.play()

    # -------------------------------------
    def resume( self, ):
        """
        what it says -- start/resume playback of whatever is currently
        loaded ( libvlc's play() both starts a freshly loaded/stopped
        media and un-pauses a paused one ). see pause()/stop() for how
        this differs from those
        """
        self.vlc_player.play()

    # -------------------------------------
    def pause( self, ):
        """ what it says -- toggle pause/resume ( libvlc's own pause() behavior ) """
        self.vlc_player.pause()

    # -------------------------------------
    def stop( self, ):
        """
        what it says -- stop playback outright ( vs. pause() ) -- see
        VlcVideoWidget's class docstring for the pause/stop distinction
        """
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
    def set_rate( self, rate ):
        """
        playback speed, 1.0 is normal. returns libvlc's result, 0 ok, -1 if
        refused. vlc keeps the audio pitch by default ( scaletempo ), but
        may mute audio at high rates
        """
        return self.vlc_player.set_rate( float( rate ) )

    # -------------------------------------
    def get_rate( self, ):
        """ what it says, 1.0 is normal speed """
        return self.vlc_player.get_rate()

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

    # -------------------------------------
    def shutdown( self, ):
        """
        read it -- fully stop and release the libvlc player/instance. this
        is NOT automatic on widget deletion: libvlc's decode/audio threads
        are not owned by Qt, and the event callbacks attached in __init__
        hold a reference from libvlc's C side back to self, so without an
        explicit shutdown() the player ( and its audio ) keeps running even
        after this widget is removed from its tab -- see closeEvent() and
        pyqt_by_example.close_tab()
        """
        if self.vlc_shut_down:
            return
        self.vlc_shut_down  = True

        self.vlc_player.stop()

        for event_type in self.vlc_event_types:
            self.vlc_event_manager.event_detach( event_type )

        self.vlc_player.release()
        self.vlc_instance.release()

    # -------------------------------------
    def closeEvent( self, event ):
        """ what it says -- belt-and-suspenders for when this widget IS closed the normal Qt way """
        self.shutdown()
        super().closeEvent( event )

#-----------------------------------------------
class ClickToPositionSlider( QSlider ):
    """
    a QSlider that jumps straight to wherever the user left-clicks in the
    groove. stock QSlider only steps one page toward a groove click --
    you have to already be on the handle to drag it to an arbitrary spot.
    used below for both the seek and volume sliders
    """

    def mousePressEvent( self, event ):
        """
        read it -- set the value from the click position BEFORE calling
        the base implementation, so the handle is already under the
        cursor when it does its own hit-testing -- that makes a
        click-then-drag continue smoothly from the clicked spot instead
        of jumping again
        """
        if event.button() == Qt.LeftButton:

            # Qt6 dropped QMouseEvent.x()/.y() for position() ( a QPointF ),
            # Qt5 has no position() -- pick whichever this binding has
            if hasattr( event, "position" ):
                a_point             = event.position()
            else:
                a_point             = event.pos()

            if self.orientation() == Qt.Horizontal:
                click_pos           = int( a_point.x() )
                slider_length       = self.width()

            else:
                click_pos           = int( a_point.y() )
                slider_length       = self.height()

            value                = QStyle.sliderValueFromPosition(
                                        self.minimum(), self.maximum(), click_pos, slider_length )
            self.setValue( value )

        super().mousePressEvent( event )

#-----------------------------------------------
class VlcVideoWidget( QWidget ):
    """
    a complete, self-contained "video player" widget -- a VlcVideoFrame
    plus all the controls that operate on it: status label, seek
    slider/time label, volume slider, a Play/Pause toggle button, and a
    Stop button. drop this into any tab/window, call play( file_name ) or
    load( file_name ), and the controls just work. the only thing left to
    the caller is deciding *what* file to play ( e.g.
    tab_vlc_qt_object_widget.py has its own "Play Vid 1/2" buttons ).

    pause vs. stop -- both halt playback, but differently:
      * pause  -- freezes the decoding pipeline in place. position is kept,
                  frames/audio buffers stay allocated, and resuming ( play()
                  on a paused player ) is instant since nothing has to be
                  re-opened or re-buffered.
      * stop   -- tears the playback session down: position resets to 0,
                  decoder/output resources are released ( same as if
                  playback had never started ). starting again is more like
                  starting fresh -- the file/stream is re-opened and has to
                  buffer again, and slow/remote media will show it.
    use pause for "user hit space to freeze the video", stop for "done
    with this media" / about to load something else / freeing resources.

            gui_dict   # a dict for special gui stuff, see code
                       #   "stop_button"   -- default True
                       #   "reload_on_end" -- default False, see set_reload_on_end()
                       #   "speed_control" -- default True, the playback speed spin box
    """

    # re-broadcast anything worth logging ( play requests, vlc errors )
    # so a host tab can wire it into its own message/log widget
    status_message_signal   = Signal( str )

    def __init__( self, parent = None, gui_dict = None ):
        """
        """
        super().__init__( parent )

        self.position_slider_dragging = False    # True while user drags the seek slider, see _update_position

        if gui_dict:
            self.gui_dict   = gui_dict

        else:
            self.gui_dict   = {}

        self.file_name      = None     # last file given to load()/play(), used by reload_on_end
        self.reload_on_end  = bool( self.gui_dict.get( "reload_on_end", False ) )
        self.last_state     = None     # last vlc_state_signal text, see _on_media_state_changed

        layout             = QVBoxLayout( self )
        self.setLayout( layout )

        # ---- the video surface -- all the vlc plumbing lives inside this widget
        video_frame          = VlcVideoFrame(   )
        video_frame.vlc_state_signal.connect( self._on_media_state_changed )
        self.video_frame     = video_frame
        layout.addWidget( video_frame, stretch = 2 )

        # ---- status label
        a_widget             = QLabel( "no video loaded" )
        self.media_status_widget   = a_widget
        layout.addWidget( a_widget, stretch = 0 )

        # ---- position row -- slider + elapsed/total time, like vlc's own seek bar
        position_layout      = QHBoxLayout(   )
        layout.addLayout( position_layout, stretch = 0 )

        position_slider      = ClickToPositionSlider( Qt.Horizontal )
        position_slider.setRange( 0, 1000 )    # scaled 0-1000, mapped to get_length_ms()/seek_to_ms()
        position_slider.sliderPressed.connect(  self._on_position_slider_pressed )
        position_slider.sliderReleased.connect( self._on_position_slider_released )
        self.position_slider = position_slider
        position_layout.addWidget( position_slider )

        a_widget             = QLabel( "00:00 / 00:00" )
        self.time_label      = a_widget
        position_layout.addWidget( a_widget )

        # a timer, not vlc's own MediaPlayerPositionChanged/TimeChanged events --
        # those fire ( often, on the libvlc thread ) many times a second, more
        # marshaling than a seek bar needs. polling from the Qt side is simpler
        position_timer        = QTimer( self )
        position_timer.setInterval( 250 )
        position_timer.timeout.connect( self._update_position )
        position_timer.start()
        self.position_timer   = position_timer

        # ---- volume row
        volume_layout         = QHBoxLayout(   )
        layout.addLayout( volume_layout, stretch = 0 )

        a_widget              = QLabel( "Volume" )
        volume_layout.addWidget( a_widget )

        volume_slider         = ClickToPositionSlider( Qt.Horizontal )
        volume_slider.setRange( 0, 100 )
        volume_slider.valueChanged.connect( self._on_volume_changed )
        self.volume_slider    = volume_slider
        volume_layout.addWidget( volume_slider )
        volume_slider.setValue( 80 )    # triggers _on_volume_changed, sets the initial vlc volume too

        # ---- playback speed, same row as volume
        value    = self.gui_dict.get( "speed_control" )
        if value is None or value is True:
            a_widget              = QLabel( "Speed" )
            volume_layout.addWidget( a_widget )

            a_widget              = QDoubleSpinBox(   )
            a_widget.setRange( 0.25, 4.0 )
            a_widget.setSingleStep( 0.25 )
            a_widget.setDecimals( 2 )
            a_widget.setSuffix( " x" )
            a_widget.setValue( 1.0 )
            # without this, typing "1.5" fires valueChanged at "1." then "1.5"
            a_widget.setKeyboardTracking( False )
            a_widget.valueChanged.connect( self._on_rate_changed )
            self.rate_spin_box    = a_widget
            volume_layout.addWidget( a_widget )

        else:
            self.rate_spin_box    = None

        # ---- play/pause + stop -- generic transport controls live here,
        # unlike "Play Vid 1/2" which is demo-specific ( picks a file ) and
        # stays in the host tab
        button_layout         = QHBoxLayout(   )
        layout.addLayout( button_layout, stretch = 0 )

        a_widget              = QPushButton( "Play" )
        a_widget.clicked.connect( self._on_play_pause_clicked )
        self.play_pause_button = a_widget
        button_layout.addWidget( a_widget )

        value    = self.gui_dict.get( "stop_button" )
        if value is None or value is True:
            a_widget              = QPushButton( "Stop" )
            a_widget.clicked.connect( self.stop )
            button_layout.addWidget( a_widget )



    # -------------------------------------
    def load( self, file_name ):
        """
        what it says -- load file_name without starting playback, so the
        Play/Pause button starts it whenever the user is ready. use play()
        instead to load and start immediately
        """
        self.file_name      = file_name
        self.video_frame.load( file_name )

        msg                 = ( f"loaded {file_name = }, not playing  " )
        self.media_status_widget.setText( msg )
        self.status_message_signal.emit( msg )

    # -------------------------------------
    def play( self, file_name ):
        """
        what it says -- load and play file_name, updating the status label
        """
        self.file_name      = file_name
        self.video_frame.play( file_name )

        msg                 = ( f"playing {file_name = }  " )
        self.media_status_widget.setText( msg )
        self.status_message_signal.emit( msg )

    # -------------------------------------
    def set_reload_on_end( self, reload_on_end ):
        """
        what it says -- when True, a video that plays to its end is
        re-loaded but NOT played, so it is back at the start and the
        Play button starts it again. when False ( the default ) libvlc
        leaves it in its "ended" state
        """
        self.reload_on_end  = bool( reload_on_end )

        msg                 = ( f"reload_on_end set to {self.reload_on_end}" )
        self.status_message_signal.emit( msg )

    # -------------------------------------
    def _reload_after_end( self, ):
        """
        read it -- called from _on_media_state_changed on "end reached"
        when reload_on_end is set. this runs on the Qt main thread, which
        matters: calling libvlc player methods from inside libvlc's own
        event callback can deadlock
        """
        file_name           = self.file_name
        if file_name is None:
            return

        self.video_frame.load( file_name )

        # get_length_ms() is -1 until playback starts again, so
        # _update_position will not reset the slider for us
        self.position_slider.blockSignals( True )
        self.position_slider.setValue( 0 )
        self.position_slider.blockSignals( False )

        msg                 = ( f"end reached, reloaded {file_name = }, not playing  " )
        self.media_status_widget.setText( msg )
        self.status_message_signal.emit( msg )

    # -------------------------------------
    def pause( self, ):
        """ what it says -- toggle pause/resume ( status label updates via vlc_state_signal ) """
        self.video_frame.pause()

    # -------------------------------------
    def stop( self, ):
        """ what it says -- ( status label updates via vlc_state_signal ) """
        self.video_frame.stop()

    # -------------------------------------
    def _on_play_pause_clicked( self, ):
        """
        what it says -- the Play/Pause button toggles by asking libvlc
        whether it's currently playing rather than tracking our own state
        ( is_playing() is authoritative, e.g. it also covers "loaded but
        never started" ). resume() both starts a freshly loaded/stopped
        media and un-pauses a paused one, so one branch covers both
        """
        if self.video_frame.vlc_player.is_playing():
            self.video_frame.pause()
        else:
            self.video_frame.resume()

    # -------------------------------------
    def _fmt_ms( self, ms ):
        """
        what it says -- ms ( libvlc's time unit ) to a "mm:ss" string,
        treating negative/unknown ( libvlc returns -1 when there is no
        media, or length is not yet known ) as zero
        """
        ms                  = max( ms, 0 )
        total_seconds       = ms // 1000
        minutes             = total_seconds // 60
        seconds             = total_seconds % 60

        return f"{minutes:02d}:{seconds:02d}"

    # -------------------------------------
    def _update_position( self, ):
        """
        read it -- polled by self.position_timer, keeps the seek slider
        and time label in sync with the actual vlc player position
        """
        length              = self.video_frame.get_length_ms()    # ms, -1 if unknown
        current              = self.video_frame.get_time_ms()      # ms, -1 if unknown

        if length > 0 and not self.position_slider_dragging:
            slider_value        = int( current * 1000 / length )
            self.position_slider.blockSignals( True )
            self.position_slider.setValue( slider_value )
            self.position_slider.blockSignals( False )

        msg                 = ( f"{self._fmt_ms( current )} / {self._fmt_ms( length )}" )
        self.time_label.setText( msg )

    # -------------------------------------
    def _on_position_slider_pressed( self, ):
        """
        what it says -- stop the timer from fighting the user's drag
        """
        self.position_slider_dragging = True

    # -------------------------------------
    def _on_position_slider_released( self, ):
        """
        what it says -- seek to wherever the user dropped the slider
        """
        length              = self.video_frame.get_length_ms()

        if length > 0:
            value               = self.position_slider.value()
            new_time            = int( value * length / 1000 )
            self.video_frame.seek_to_ms( new_time )

        self.position_slider_dragging = False

    # -------------------------------------
    def _on_volume_changed( self, value ):
        """
        what it says -- value is 0-100, straight from the volume slider
        """
        self.video_frame.set_volume( value )

    # -------------------------------------
    def _on_rate_changed( self, value ):
        """
        what it says -- value is the playback speed, 1.0 normal, straight
        from the speed spin box
        """
        result              = self.video_frame.set_rate( value )

        if result != 0:
            msg                 = ( f"vlc refused playback speed {value}  " )
            self.status_message_signal.emit( msg )

    # -------------------------------------
    def set_rate( self, rate ):
        """
        what it says -- set the playback speed from code. goes through the
        spin box ( when there is one ) so it stays in sync with the player
        """
        if self.rate_spin_box is None:
            self._on_rate_changed( rate )
        else:
            self.rate_spin_box.setValue( rate )

    # -------------------------------------
    def _on_media_state_changed( self, state_text ):
        """
        what it says -- reflect the player state in the status label.
        runs on the Qt main thread ( see VlcVideoFrame.vlc_state_signal ),
        unlike the libvlc event callbacks that feed it
        libvlc ( 3.0.20 at least ) sends Stopped right after EndReached --
        keep "end reached" showing rather than let that overwrite it
        """
        last_state          = self.last_state
        self.last_state     = state_text

        if state_text == "stopped" and last_state == "end reached":
            return

        self.media_status_widget.setText( state_text )

        if state_text == "playing":
            self.play_pause_button.setText( "Pause" )
            # re-apply the slider's volume once playback has started, in case
            # libvlc ignored the pre-media setValue( 80 ) in __init__ --
            # tested on libvlc 3.0.20 and not needed, the early volume sticks
            # self.video_frame.set_volume( self.volume_slider.value() )
        elif state_text in ( "paused", "stopped", "end reached" ):
            self.play_pause_button.setText( "Play" )

        if state_text == "end reached" and self.reload_on_end:
            self._reload_after_end()

        if state_text.startswith( "error" ):
            self.status_message_signal.emit( state_text )

    # -------------------------------------
    def shutdown( self, ):
        """
        read it -- stop the position-poll timer and hand off to
        VlcVideoFrame.shutdown() to actually stop/release vlc. a host tab
        should call this before dropping this widget ( e.g. on tab close ) --
        see VlcVideoFrame.shutdown() for why this is not automatic
        """
        self.position_timer.stop()
        self.video_frame.shutdown()

    # -------------------------------------
    def closeEvent( self, event ):
        """ what it says -- belt-and-suspenders for when this widget IS closed the normal Qt way """
        self.shutdown()
        super().closeEvent( event )

# ---- eof
