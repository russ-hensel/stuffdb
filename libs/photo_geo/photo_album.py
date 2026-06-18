#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 09:00:43 2026

@author: russ
"""

# ---- tof

# # --------------------
# if __name__ == "__main__":
#     import main   # noqa  stops auto removal by pycln
# # --------------------

# ---- imports
#from enum import Enum
import logging
from   qtpy.QtSql import (
                            QSqlQuery, )

import subprocess
#import folium
#import pytz
# from folium.plugins import HeatMap
#import webbrowser
import http.server
import socketserver
import threading
import urllib.parse
import simplekml
from   pathlib import Path

# ---- imports local -- then constants
from   app_global import AppGlobal
import string_utils


# ---- module-level helper: tiny local-only HTTP server for photo files ----
#
# Google Earth Pro on Linux silently refuses to navigate file:// links from
# its balloon (Qt WebKit / Chromium sandbox). Serving the photos over
# http://127.0.0.1:<port>/... sidesteps the restriction entirely, and the
# "open photo" link is then handed to your default browser
# (xdg-settings get default-web-browser).
#
# The server:
#   - is bound to 127.0.0.1, so nothing on the network can reach the photos
#   - picks a free port automatically (port 0 => OS chooses)
#   - serves from AppGlobal.parameters.picture_db_root
#   - runs in a daemon thread, so it dies with the Python process

_photo_server_lock  = threading.Lock( )
_photo_server_info  = None    # (host, port) once started, else None


def _ensure_photo_server( ):
    """
    Start the photo HTTP server on first call, return (host, port).
    Subsequent calls return the same (host, port) without restarting.
    """
    global _photo_server_info

    with _photo_server_lock:
        if _photo_server_info is not None:
            return _photo_server_info

        photo_root  = str( AppGlobal.parameters.picture_db_root )

        class _Handler( http.server.SimpleHTTPRequestHandler ):
            def __init__( self, *a, **kw ):
                super().__init__( *a, directory = photo_root, **kw )

            def log_message( self, *_args ):
                # silence default access-log spam on stderr
                pass

        srv                 = socketserver.ThreadingTCPServer(
            ( "127.0.0.1", 0 ), _Handler )
        srv.daemon_threads  = True
        host, port          = srv.server_address

        threading.Thread( target = srv.serve_forever, daemon = True ).start()

        _photo_server_info  = ( host, port )

        msg = ( f"photo HTTP server: http://{host}:{port}  "
                f"root={photo_root}" )
        logging.info( msg )

        return _photo_server_info


#----------------------------------
class PhotoAlbum( ):
    """
    see __init__
    """
    #----------------------------------
    def __init__( self, a_id ):
        """
        pretty much a dict in a class
            a_id is the album db id
            this stores photo points by db id
        """
        self.id                 = a_id
        self.photo_point_dict   = { }
        self.point_list         = []
            # key is db id

    #----------------------------------
    def add_point( self, photo_id, photo_point ):
        """
        what it says, read
            photo_id is in photo_point ... so
        """
        self.photo_point_dict[ photo_id ] = photo_point

     #----------------------------------
    def get_ts_sort_key( self, a_point ):
        """
        given an item, returns a key for sorting purposes
        these functions are often done as lambda functions
        but that can be confusing if you are not used to lambda
        """
        key   =  a_point.ts
        return key

    #----------------------------------
    def make_list_by_ts( self, ):
        """
        what it says, read

        """
        the_list      = []
        for i_point in self.photo_point_dict.values():
            # values are the dicts, but no longer can look up by id, so what

            if i_point.ts == "" or i_point.ts is None:
                continue

            if i_point.lat == "" or i_point.lat is None:
                continue

            if i_point.long == "" or i_point.long is None:
                continue

            the_list.append( i_point )

        # ---- now sort assending by ts
        the_list.sort( key  = self.get_ts_sort_key )  # sort in place

        self.point_list     = the_list

        return the_list

    # --------------------------------------
    def list_to_kmz( self, and_open = True, use_local_server = True ):
        """
        Build a styled KMZ from self.point_list and (optionally) open it
        in Google Earth.

            - styled polyline connecting the photos in timestamp order
            - one camera-icon placemark per photo
            - balloon text with timestamp, filename, and a clickable link
              to the local image file
        """
        # base_dir      = AppGlobal.parameters.picture_db_root
        photo_points  = self.point_list

        out_dir       = Path( AppGlobal.parameters.output_dir )
        out_dir.mkdir( parents = True, exist_ok = True )
        file_name     = str( ( out_dir / f"album_{self.id}.kmz" ).resolve() )

        kml                 = simplekml.Kml()
        kml.document.name   = f"Album {self.id}"

        # ---- shared point style (define once, reuse for every photo) ----
        pt_style                            = simplekml.Style()
        pt_style.iconstyle.icon.href        = (
            "http://maps.google.com/mapfiles/kml/shapes/camera.png" )
        pt_style.iconstyle.scale            = 1.0
        pt_style.iconstyle.color            = simplekml.Color.rgb( 255, 220, 0 )
        pt_style.labelstyle.scale           = 0.0   # hide on-map labels; sidebar still shows name
        pt_style.balloonstyle.text          = (
            "<h3>$[name]</h3>"
            "$[description]" )

        # ---- the polyline ----
        linestring                              = kml.newlinestring( name = "My Path" )
        linestring.tessellate                   = 1
        linestring.altitudemode                 = simplekml.AltitudeMode.clamptoground
        linestring.style.linestyle.color        = simplekml.Color.rgb( 255, 80, 0, 220 )  # orange
        linestring.style.linestyle.width        = 3
        linestring.style.linestyle.gxouterwidth = 1                                       # subtle halo
        linestring.style.linestyle.gxoutercolor = simplekml.Color.rgb( 0, 0, 0, 180 )

        # ---- decide URL prefix once (not per photo) ----------------
        # use_local_server = True  -> "http://127.0.0.1:<port>/"
        #                             reliable "open photo" via your default
        #                             browser; only usable on this machine
        #                             while the Python process is alive
        # use_local_server = False -> "file://<picture_db_root>/"
        #                             portable but GE Pro on Linux usually
        #                             swallows file:// link clicks; requires
        #                             the "allow access to local files and
        #                             personal data" GE preference to be on

        if use_local_server:
            msg         = ( ">>>>>>>>>>>>>>>>.Using Local Server <<<<<<<<<<<<<<<<<<<<" )
            logging.info( msg )
            host, port  = _ensure_photo_server()
            url_prefix  = f"http://{host}:{port}/"

        else:
            url_prefix  = f"file://{AppGlobal.parameters.picture_db_root}/"

        # ---- one placemark + one line vertex per photo ----
        for i_idx, i_photo_plus in enumerate( photo_points ):

            # this should never happen but just in case
            if i_photo_plus.lat is None or i_photo_plus.long is None:
                continue

            linestring.coords.addcoordinates(
                [ ( i_photo_plus.long, i_photo_plus.lat, 0 ) ] )

            pnt         = kml.newpoint(
                name    = f"#{i_idx + 1}",
                coords  = [ ( i_photo_plus.long, i_photo_plus.lat ) ], )
            pnt.style   = pt_style

            ts_txt      = str( i_photo_plus.ts ) if i_photo_plus.ts else ""
            file_txt    = i_photo_plus.file or ""
            photo_name  = i_photo_plus.photo_name

            # urllib.parse.quote handles spaces / unicode in filenames so
            # "my photo.jpg" -> "my%20photo.jpg". Safe for both http and
            # file:// URLs.
            sub_q       = urllib.parse.quote( i_photo_plus.sub_dir or "" )
            file_q      = urllib.parse.quote( i_photo_plus.file    or "" )
            url         = f"{url_prefix}{sub_q}/{file_q}"

            # Balloon HTML:
            #   - <h2> gives a proper large title (plain <b> is just bold,
            #     same size).
            #   - <img src="..." width="320"> shows the photo inline. The
            #     renderer scales the image down on the fly; source file is
            #     not modified.
            #   - target="_blank" asks GE to hand the click off to the
            #     system browser instead of navigating the embedded balloon
            #     view. With http URLs this Just Works; with file:// it also
            #     needs Tools > Options > General > "Show web results in
            #     external browser" plus "allow access to local files".
            pnt.description = (
                f"<h2>{photo_name}</h2>"
                f'<img src="{url}" width="320"><br>'
                f'<a href="{url}" target="_blank">open photo</a>' )

            # for debug keep for now
            if i_idx < 5:
                print( pnt.description )

            # truly hidden data, available to balloon templates as $[photo_url]
            # pnt.extendeddata.newdata( name = "photo_id",  value = str( i_photo_plus.id ) )
            # pnt.extendeddata.newdata( name = "photo_url", value = url )

        kml.savekmz( file_name )

        msg    = f"list_to_kmz: wrote {file_name}"
        logging.info( msg )

        if and_open:
            GE          = "/opt/google/earth/pro/google-earth-pro" # move to parameters??

            subprocess.Popen(
                [ GE, file_name ],
                stdout              = subprocess.DEVNULL,
                stderr              = subprocess.DEVNULL,
                start_new_session   = True, )

        return file_name

    #--------------------------
    def __str__( self ):
        """
        universal __str__
        """
        return string_utils.obj_to_str( self )

#----------------------------------
class PhotoPoint():
    """
    see __init__
    """
    def __init__(self, a_id   ):
        """
        in memory data about photos for
        mapping etc
        """
        self.id         = a_id
        self.ts         = None
        self.lat        = None
        self.long       = None
        self.file       = None
        self.sub_dir    = None
        self.base_dir   = None
        self.photo_name = None

    #--------------------------
    def __str__( self ):
        """
        universal __str__
        """
        return string_utils.obj_to_str( self )

#----------------------------------
class PhotoAlbumCreator():
    """
    see __init__
    """
    #------------------------
    def __init__(self, a_album_id ):
        """
        the usual
        """
        self.id     = a_album_id
        self.sql    = ( "SELECT photo.id, photo.file, photo.sub_dir,  photo.dt_item, "
                        " photo.exif_ts, photo.exif_lat, "
                         " photo.exif_lon, photo.exif_make, photo.exif_model, "
                         " photo.name "
                        " FROM photo "
                        " JOIN photo_in_show ON photo_in_show.photo_id = photo.id "
                        " WHERE photo_in_show.photo_show_id =  :arg_id "  )

        self.album   = self.make_album()
        self.query()

    #----------------------------------
    def make_album( self,   ):
        """
        what it says, read
        """
        a_album    =  PhotoAlbum(  self.id   )

        return a_album

    #----------------------------------
    def query( self, ):
        """
        what it says, read
        """
        query       = QSqlQuery( AppGlobal.qsql_db_access.db )
        sql         = self.sql
        a_album     = self.album

        query.prepare( sql )
        query.bindValue( ":arg_id",  self.id )

        if not query.exec_():  # Check if execution failed
            msg = ( "PhotoAlbumCreator query_print_tab Error executing query:"
                    f"  {query.lastError().text()}" )
            logging.error(msg)

        while query.next():
            # match to sql
            a_id                = query.value( 0 )

            a_point             = PhotoPoint( a_id )

            a_point.file        = query.value( 1 )
            a_point.sub_dir     = query.value( 2 )
            #a_point.dt_item    = query.value( 3 )
            a_point.ts          = query.value( 4 )
            a_point.lat         = query.value( 5 )
            a_point.long        = query.value( 6 )
            a_point.photo_name  = query.value( 9 )
            a_point.base_dir    = AppGlobal.parameters.picture_db_root

            a_album.add_point( a_id, a_point )
            #rint( f"ID: {a_point} " )
            #rint( a_point.photo_name )


# ---- eof ---------------------------


