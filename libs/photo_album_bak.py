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
import simplekml
from   pathlib import Path

# ---- imports local -- then constants
from   app_global import AppGlobal
import string_utils


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
    def list_to_kmz( self, and_open = True ):
        """
        photo points are turned into a kmz file, read the code
            return  consider file name None ?? open google earth
        """
        photo_points  = self.point_list

        #file_name     = AppGlobal.parameters.default_kmz_fn
        file_name     = f"{AppGlobal.parameters.output_dir}/album_{self.id}.kmz"

        kml = simplekml.Kml()

        linestring              = kml.newlinestring( name = "My Path" )
        linestring.tessellate   = 1  # Set tessellate to 1 to create a tessellated line

        for i_photo_plus in photo_points:

            # this should never happen but just in case
            if i_photo_plus.lat is None or i_photo_plus.long is None:
                continue

            linestring.coords.addcoordinates( [ ( i_photo_plus.long, i_photo_plus.lat, 0 ) ] )

        # Set altitude mode to clampToGround to ensure the path follows the Earth's surface
        linestring.altitudemode = simplekml.AltitudeMode.clamptoground

        kml.save( file_name  )

        if and_open:
            # make path absolute
            file_name   = str( Path( file_name ).resolve() )

            #msg    = f"in _pp_to_kmz KML file {file_name} has been created."
            #rint( msg )


            GE          = "/opt/google/earth/pro/google-earth-pro" # move to parameters??

            subprocess.Popen( [ GE, file_name ] )

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
                         " photo.exif_lon, photo.exif_make, photo.exif_model "
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
            a_id                = query.value( 0 )

            a_point             = PhotoPoint( a_id )

            a_point.file        = query.value( 1 )
            a_point.sub_dir     = query.value( 2 )
            a_point.ts          = query.value( 3 )
            a_point.ts          = query.value( 4 )
            a_point.lat         = query.value( 5 )
            a_point.long        = query.value( 6 )

            a_album.add_point( a_id, a_point )
            #rint( f"ID: {a_point} " )


# ---- eof ---------------------------


