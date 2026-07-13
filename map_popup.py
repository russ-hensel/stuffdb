#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 12:00:00 2026

@author: russ

map_popup.py

pop up a small window with a zoomable map ( leaflet.js + OpenStreetMap tiles,
via folium ) centered on a single lat/long point.  no API key needed, OSM
tiles are free.

usage
    from map_popup import show_map_popup
    self.map_dialog     = show_map_popup( 42.3601, -71.0589, parent = self )
        # non modal by default -- keep a reference ( self.map_dialog ) or
        # PyQt will garbage collect the dialog and the window will vanish
"""

# --------------------
if __name__ == "__main__":
    import main
    main.main()
# --------------------

# ---- imports
import folium

from qtpy.QtWidgets          import QDialog, QVBoxLayout
from qtpy.QtWebEngineWidgets import QWebEngineView
# ---- import end


#-------------------------------------
class MapPopup( QDialog ):
    """
    a dialog holding one zoomable ( mouse pan/zoom ) map, centered on and
    marked at a single lat/long, built with folium
    """

    #-------------------------
    def __init__( self, latitude, longitude, parent = None, *, zoom_start = 15, title = None ):

        super().__init__( parent )

        self.latitude   = latitude
        self.longitude  = longitude

        if title is None:
            title   = f"map  {latitude:.5f}, {longitude:.5f}"
        self.setWindowTitle( title )
        self.resize( 700, 600 )

        # ---- build the folium map and get its html, no temp file needed
        a_map   = folium.Map( location = [ latitude, longitude ], zoom_start = zoom_start )
        folium.Marker( [ latitude, longitude ] ).add_to( a_map )
        html    = a_map.get_root().render()

        # ---- show it
        self.web_view   = QWebEngineView( self )
        self.web_view.setHtml( html )

        layout  = QVBoxLayout( self )
        layout.addWidget( self.web_view )


#-------------------------------------
def show_map_popup( latitude, longitude, parent = None, *, zoom_start = 15, title = None, modal = True ):
    """
    open a pop up window with a zoomable map centered on latitude, longitude

    Parameters
        latitude, longitude -- the point to center the map on ( floats )
        parent              -- parent widget, or None
        zoom_start          -- initial zoom level ( folium/leaflet convention,
                                    higher = closer ), default 15
        title               -- window title, default is the lat/long
        modal               -- True  = block ( self.exec_() )
                                False = non modal ( self.show() ), the caller
                                    must keep a reference to the returned
                                    dialog or it will be garbage collected

    Returns
        the MapPopup dialog instance -- keep a reference if modal = False
    """
    dialog  = MapPopup( latitude, longitude, parent, zoom_start = zoom_start, title = title )

    if modal:
        dialog.exec_()
    else:
        dialog.show()

    return dialog

# ---- eof
