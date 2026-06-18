#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 08:28:36 2024

old stuff_document_edit.EditStuffEvents( model, keygen, index = None, parent = None)
now
stuff_document_edit.EditStuffEvents(

"""
# ---- tof
# --------------------
if __name__ == "__main__":
    import main   # noqa  stops auto removal by pycln
    pass

# --------------------

# ---- imports

import logging
from   pathlib import Path

from qtpy.QtCore    import Qt

from qtpy.QtCore    import QDateTime

from qtpy.QtGui     import QKeySequence

from qtpy.QtWidgets import ( QComboBox,

                             QDialog,
                             QLabel,
                             QDialogButtonBox,
                             QShortcut,

                             QWidget,
                             QFormLayout,
                             QHBoxLayout,
                             QLineEdit,
                             QPushButton,
                             QSpinBox,
                             QVBoxLayout)

# ---- imports local
from   coord_panel import CoordPanel
from   map_scene   import MapScene
from   map_view    import MapView

# ---- end imports

logger          = logging.getLogger( )
# for custom logging level at module
LOG_LEVEL  = 20   # higher is more


#--------------------------------------
class LatLongMap( QDialog ):
    """
    map    = lat_long_map.LatLongMap()   # import  lat_long_map

    """
    #--------------------------------
    def __init__(
        self,
        parent          = None,
        data            = None,
        image_path      = None,
        alt_image_path  = None,
        image_label     = "Map",
        alt_image_label = "View",
        title           = "Select a Latitude and Longitude",
        read_only       = False,
    ):
        """
        includes the building of the form which is not
        done in planting_event

        data mutated and "passed" as a return

        image_path      : primary background PNG (default: world_equirectangular.png
                          next to this module -- the country-borders "map")
        alt_image_path  : alternate background PNG (default: world_satellite.png
                          next to this module -- the "view")
        image_label     : human-readable name of the primary background; used
                          in the toggle button text ("Show <image_label>")
        alt_image_label : human-readable name of the alternate background
        title           : window-title string; pass something like
                          "View photo location" together with read_only=True
                          when using the dialog as a viewer.
        read_only       : if True, user clicks on the map do NOT drop a new
                          marker.  Hover still works, the initial point from
                          ``data`` is still shown, and the toggle / zoom /
                          pan / shortcut machinery is unchanged.  The OK
                          button still works -- since lat/long never moves
                          in this mode, accepting just writes the unchanged
                          values back.

        Both PNGs must be equirectangular (width = 2 * height); the
        projection is rebuilt from the actual pixmap dimensions on every
        swap, so the two images do not need to share a resolution.
        """
        super().__init__( parent )

        self.setWindowTitle( title )

        print( data )
         #   "lat" "long" "place"

        self.data       = data
        self._read_only = bool( read_only )

        if parent is None:
            1/0 # need parent which is the tab where the model is

        # ---- resolve image paths (defaults live next to this module) ----
        here_dir = Path( __file__ ).resolve().parent

        if image_path is None:
            image_path     = here_dir / "world_equirectangular.png"

        if alt_image_path is None:
            alt_image_path = here_dir / "world_satellite.png"

        self._image_path        = Path( image_path ).resolve()
        self._alt_image_path    = Path( alt_image_path ).resolve()
        self._image_label       = image_label
        self._alt_image_label   = alt_image_label
        self._current_path      = self._image_path

        # ---- build gui
        self.scene      = MapScene( self._current_path )
        self.view       = MapView( self.scene )     # the main graphic of map
        self.panel      = CoordPanel( self, )       # control panel for it
                # too early for data

        layout          = QVBoxLayout( self  )

        layout.setContentsMargins( 0, 0, 0, 0 )
        layout.setSpacing( 0 )
        layout.addWidget( self.view,  stretch = 1 )
        layout.addWidget( self.panel, stretch = 0 )

        # ---- background toggle row -------------------------------------
        toggle_row              = QHBoxLayout( )
        toggle_row.setContentsMargins( 6, 4, 6, 6 )
        self.toggle_button      = QPushButton( )
        self.toggle_button.clicked.connect( self._toggle_map )
        self._update_toggle_label()    # set initial text
        toggle_row.addStretch( 1 )
        toggle_row.addWidget( self.toggle_button )
        toggle_row.addStretch( 1 )
        layout.addLayout( toggle_row, stretch = 0 )

        # self.statusBar().showMessage("Hover over the map, click to lock.")
        #     # may need to be a main window to have this
        # widget     =  QLabel( "status_bar" )
        # self.status_bar  = widget

        # disabled as not status bar for a dialog
        self._zoom_label = QLabel( "100%" )
        self._zoom_label.setMinimumWidth(60)
        #self.statusBar().addPermanentWidget(self._zoom_label)

        # ---- wiring ---------------------------------------------------
        self.view.coordsHovered.connect( self._on_hover)
        self.view.coordsCleared.connect( self._on_cleared)
        # Only forward USER clicks to _on_picked when not in read-only mode.
        # The initial-position _on_picked() call at the end of __init__ is a
        # direct method call and still runs, so the starting marker shows
        # either way.

        if not self._read_only:
            self.view.coordsPicked.connect( self._on_picked )

        self.view.zoomChanged  .connect( self._on_zoom_changed)
        self.panel.resetRequested.connect( self._on_reset)
        # self.panel.copied.connect(
        #     lambda txt: self.statusBar().showMessage(f"Copied: {txt}", 3000)
        # )

        # ---- Keyboard shortcuts.
        esc = QShortcut( QKeySequence( Qt.Key_Escape ), self)
        esc.activated.connect ( self.panel.reset )

        fit = QShortcut(QKeySequence( "Ctrl+0" ), self )
        fit.activated.connect( self.view.fit_in_view )

        mtog = QShortcut( QKeySequence( "M" ), self )
        mtog.activated.connect( self._toggle_map )

        # ---- load data lat long size
        self._on_picked(
             data[ "lat" ],
             data[ "long" ] )

        # size
        self.panel.size_widget.setText( str( data[ "size" ] ) )

    # --- slots ---------------------------------------------------------
    def _on_hover(self, lat: float, lon: float) -> None:
        """ """
        self.panel.update_hover(lat, lon)
        if not self.panel.is_locked:
            self.panel.set_status( f"Hovering..." )
            #self.statusBar().showMessage(f"Hover: {lat:+.5f}, {lon:+.5f}")

    # -------------------------------
    def _on_cleared(self) -> None:
        """ """
        self.panel.clear_hover()
        if not self.panel.is_locked:
            msg         = ( "Hover:click to lock." )
            self.panel.set_status(msg )

    # ----------------------------------------
    def _on_picked(self, lat: float, lon: float) -> None:
        """
        On every click: panel.lock_at() takes care of clearing the previous
        marker, updating the readout, and dropping a fresh marker at the
        new (lat, lon).  data is not written here -- it is committed in ok().
        """
        self.panel.lock_at(lat, lon)

        # # could wait for accept
        # data            = self.data
        # data[ "lat" ]   = lat
        # data[ "long"]   = lon

        msg         = ("Lat Long locked ")
        self.panel.set_status(msg )
        # self.statusBar().showMessage(
        #     f"Locked: {lat:+.5f}, {lon:+.5f}   (Esc or Reset to unlock)"
        # )

    # ----------------------------------------
    def _on_reset(self) -> None:
        # self.statusBar().showMessage("Hover over the map, click to lock.")
        msg         = ("Hover, click to lock.")
        self.panel.set_status( msg  )

        # restore the map: drop every marker / line / text the draw API
        # added.  Pixmap and the live (hover) crosshair are untouched, so
        # the map looks fresh and the user can pick again.
        self.clear_drawings()

    # ----------------------------------------
    def _on_zoom_changed(self, zoom: float) -> None:
        """ """
        self._zoom_label.setText(f"{int(round(zoom * 100))}%")

    # ----------------------------------------
    def _toggle_map( self ) -> None:
        """
        Swap the background pixmap between `image_path` and `alt_image_path`.

        MapScene.reload_pixmap() rebuilds the projection from the new
        pixmap's actual dimensions, so a swap between images of different
        resolution still produces correct lat/lon math.  If the user has
        already locked a lat/lon, the crosshair is replaced at the
        equivalent pixel of the new image.
        """
        if self._current_path == self._image_path:
            new_path = self._alt_image_path
        else:
            new_path = self._image_path

        if not Path( new_path ).is_file():
            msg = f"_toggle_map: file not found, staying put: {new_path}"
            logging.warning( msg )
            self.panel.set_status( f"Missing: {Path( new_path ).name}" )
            return

        self._current_path = Path( new_path ).resolve()
        self.scene.reload_pixmap( self._current_path )

        # If the panel was locked at a lat/lon before the swap, put the
        # crosshair back where it geographically belongs in the new image.
        if getattr( self.panel, "is_locked", False ):
            try:
                lat     = float( self.panel.lat_edit.text() )
                lon     = float( self.panel.lon_edit.text() )
                x, y    = self.scene.projection.latlon_to_pixel( lat, lon )
                self.scene.show_crosshair_at( x, y )
            except ( ValueError, AttributeError ):
                pass

        self._update_toggle_label()

    # ----------------------------------------
    def _update_toggle_label( self ) -> None:
        """
        The button always advertises the OTHER background -- the one a
        click would switch to.
        """
        if self._current_path == self._image_path:
            target = self._alt_image_label
        else:
            target = self._image_label
        self.toggle_button.setText( f"Show {target}" )


    # --- public API for callers ---------------------------------------------
    # ----------------------------------------
    def set_cursor( self, lat: float, lon: float ) -> None:
        """
        Pre-position the dialog at (lat, lon) before showing it.

        Equivalent to a user click at the geographic point:
          * crosshair shown there,
          * panel locked at the value,
          * view centered on it,
          * self.data["lat"]/["long"] mutated (same as a real pick),
          * status updated.
        """
        proj    = self.scene.projection
        x, y    = proj.latlon_to_pixel( lat, lon )

        self.scene.show_crosshair_at( x, y )
        self.view.center_on_latlon( lat, lon )
        self.panel.lock_at( lat, lon )

        if self.data is not None:
            self.data[ "lat"  ] = lat
            self.data[ "long" ] = lon

        self.panel.set_status( f"Cursor set to {lat:+.5f}, {lon:+.5f}" )

    # --- drawing pass-throughs ----------------------------------------------
    # ----------------------------------------
    def add_marker( self, lat: float, lon: float, **kwargs ):
        """
        Drop a marker on the map.  See MapScene.add_marker for kwargs:
        color, radius, label.  Returns the underlying QGraphicsItem.
        """

        return self.scene.add_marker( lat, lon, **kwargs )

    # ----------------------------------------
    def add_line( self, points, **kwargs ):
        """
        Connect a sequence of (lat, lon) tuples.  See MapScene.add_line.
        """
        return self.scene.add_line( points, **kwargs )

    # ----------------------------------------
    def add_text( self, lat: float, lon: float, text: str, **kwargs ):
        """
        Add a text label anchored at (lat, lon).  See MapScene.add_text.
        """
        return self.scene.add_text( lat, lon, text, **kwargs )

    # ----------------------------------------
    def clear_drawings( self ) -> None:
        """
        Remove every marker / line / text added through this dialog.
        Pixmap and crosshair are untouched.
        """
        self.scene.clear_drawings()

    # ----------------------------------------
    def reload_pixmap( self, image_path = None ) -> None:
        """
        Reload the underlying world map.  If image_path is None, the path
        passed at construction is reused -- a cheap "restore the picture"
        call.  Drawings are kept; call clear_drawings() first to nuke them.

        If image_path is provided, it also becomes the toggle's notion of
        the "current" image so the Show <other> button keeps making sense.
        """
        self.scene.reload_pixmap( image_path )
        if image_path is not None:
            self._current_path = Path( image_path ).resolve()
            self._update_toggle_label()

    # ----------------------------------------
    def ok( self, ) -> None:
        """

        """
        try:
            long = float( self.panel.lon_edit.text( ) )

        except:
            long = 0.

        try:
            lat  = float( self.panel.lat_edit.text( ) )

        except:
            lat = 0.

        try:
            size   = float( self.panel.size_widget.text( ) )

        except:
            size = 100.

        # perhaps drop
        self.data[ "lat"  ] = lat
        self.data[ "long" ] = long
        self.data[ "size" ] = size

        self.accept()


# ---- eof




