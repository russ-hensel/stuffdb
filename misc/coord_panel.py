"""
Read-only display of the current (lat, lon) pair, with copy/reset.
"""


from __future__ import annotations

from qtpy.QtCore    import Qt, Signal
from qtpy.QtGui     import QFont
from qtpy.QtWidgets import (
    QApplication, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget, QComboBox,
)
from   app_global import AppGlobal


# ----------------------------------------
class CoordPanel( QWidget, ):
    """Lat/Lon readout below the map.

    Three modes of display:
      * hover  - readout follows the cursor.
      * locked - readout is frozen at the last clicked point.
      * empty  - cursor is off the map and nothing is locked.
    """

    PLACEHOLDER = "—"

    resetRequested = Signal()
    copied         = Signal( str )

    #------------------------------------------
    def __init__( self, parent_dialog, ) -> None:
        super().__init__()

        self.parent_dialog  = parent_dialog
        self.location_dict  = AppGlobal.parameters.dict_lat_lon

        self._latest: tuple[float, float] | None = None
        self._locked        = False

        self.lon_edit       = self._make_edit( "lon (°)" )

        self.parent_dialog  = parent_dialog

        # self.copy_btn  = QPushButton("Copy")
        # self.copy_btn.setShortcut("Ctrl+C")
        # self.copy_btn.clicked.connect( self._on_copy)

        # Reset button removed: a fresh click on the map now clears the old
        # marker and drops a new one, so an explicit reset is unneeded.
        # The reset() method and resetRequested signal are still wired to
        # the Esc shortcut so power users keep that out.

        row                 = QHBoxLayout()

        # ---- status
        row.addWidget( QLabel( "Status:" ) )
        widget              = self._make_edit("status_bar")
        # now tweak
        widget.setMaximumWidth( 500 )
        widget.setSizePolicy( QSizePolicy.Preferred, QSizePolicy.Fixed )
        self.status_bar     = widget
        row.addWidget( widget )

        # ---- location by name
        widget                  = QComboBox(  )
        self.location_widget    = widget
        values                  = self.location_dict.keys()
        widget.addItems( values )
        row.addWidget( widget )

        # ---- .... size
        widget          = QLabel( "Size Km:")
        row.addWidget( widget )
       #self.widget_field_dict[ field_name ] = widget

        field_name              = "size_km"
        widget                  = QLineEdit(  )
        self.size_widget        = widget
        row.addWidget( widget )

        # ---- set at
        widget              = QPushButton( "<- Set at" )
        widget.clicked.connect( self.set_at_location   )
        row.addWidget( widget )

        row.addStretch( 1 )

        # ---- Lat Lon
        row.addWidget( QLabel("Lat:") )
        self.lat_edit       = self._make_edit( "lat (°)" )
        row.addWidget(self.lat_edit)

        row.addSpacing(12)

        row.addWidget(QLabel("Lon:"))
        row.addWidget( self.lon_edit )

        # ---- cancel
        widget  = QPushButton( "Cancel" )
        self.cancel_btn = widget
        #widget.setShortcut("Ctrl+R")
        widget.clicked.connect( self._on_cancel )
        row.addWidget( widget )

        # ---- ok was apply
        widget   = QPushButton( "Ok" )
        widget.clicked.connect( self._on_ok )
        row.addWidget( widget )

        #row.addWidget( self.copy_btn )

        outer = QVBoxLayout(self)
        outer.setContentsMargins(8, 6, 8, 6)
        outer.addLayout(row)

        # move to a pick drop marker
        # self.lat_edit.setText( str( data[ "lat" ] ) )
        # self.lon_edit.setText( str( data[ "long" ] ) )



        #self.clear_hover()

    # --- public API used by MainWindow --------------------------------------
    def set_status( self, msg ) -> None:
        """
        Read, weep
        """

        self.status_bar.setText( msg )
        # if self._locked:
        #     return
        # self._set_text(lat, lon)

    # --- public API used by MainWindow --------------------------------------
    def update_hover(self, lat: float, lon: float) -> None:
        if self._locked:
            return
        self._set_text( lat, lon )

    #------------------------------
    def clear_hover(self) -> None:
        """
        Read, weep
        """
        if self._locked:
            return
        self._latest = None
        self.lat_edit.setText( self.PLACEHOLDER )
        self.lon_edit.setText( self.PLACEHOLDER )

    #------------------------------
    def lock_at(self, lat: float, lon: float) -> None:
        """
        Read, weep
            One-marker-at-a-time: drop any prior marker, then drop a fresh
            one at (lat, lon).  Used by clicks, by the location dropdown,
            and by the programmatic set_cursor() API.
        """
        self.parent_dialog.clear_drawings()
        self._set_text( lat, lon )
        self._locked = True
        self.parent_dialog.add_marker( lat, lon, )

    #------------------------------
    def reset(self) -> None:
        """
        Read, weep
        """
        self._locked = False
        self._latest = None
        self.lat_edit.setText( self.PLACEHOLDER )
        self.lon_edit.setText( self.PLACEHOLDER )
        self.resetRequested.emit()

    #------------------------------
    def set_at_location(self) -> None:
        """
        Read, weep
            set using a named location
        """
        key                     = self.location_widget.currentText()
        self.location_dict      = AppGlobal.parameters.dict_lat_lon
        lat, lon                = self.location_dict[ key ]
        self.lock_at( lat, lon )
        # ?? next move to lock

    #------------------------------
    @property
    def is_locked(self) -> bool:
        """
        Read, weep
        """
        return self._locked

    # --- internals ----------------------------------------------------------
    def _set_text(self, lat: float, lon: float) -> None:
        """
        Read, weep
        """
        self._latest = (lat, lon)
        self.lat_edit.setText(f"{lat:+10.5f}")
        self.lon_edit.setText(f"{lon:+10.5f}")

    # ----------------------------------
    def _on_copy(self) -> None:
        """
        Read, weep
            copy lat long to clipboard
            may not be in use, removed button ?
        """
        if self._latest is None:
            return

        lat, lon    = self._latest
        text        = f"{lat:.6f}, {lon:.6f}"
        QApplication.clipboard().setText(text)
        self.copied.emit(text)

    # ----------------------------------
    def _on_ok( self )  -> None:
        """
        Read, weep
        """
        self.parent_dialog.ok()

    # ----------------------------------
    def _on_cancel( self )  -> None:
        """
        Read, weep
        """
        self.parent_dialog.reject()

    # ----------------------------------
    @staticmethod
    def _make_edit( placeholder: str ) -> QLineEdit:
        """
        Read, weep
        """
        edit = QLineEdit()
        edit.setReadOnly(True)
        edit.setAlignment(Qt.AlignRight)
        edit.setPlaceholderText(placeholder)
        edit.setFont(QFont("Monospace"))
        edit.setMaximumWidth( 140 )
        edit.setSizePolicy( QSizePolicy.Preferred, QSizePolicy.Fixed )
        return edit


# ---- eof



