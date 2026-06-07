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
            # key is db id

    #----------------------------------
    def add_point( self, photo_id, photo_point ):
        """
        what it says, read
        """
        self.photo_point_dict[ photo_id ] = photo_point



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
    #----------------------------------
    def make_album( self, a_album_id ):
        """
        what it says, read
        """
        a_album    =  PhotoAlbum( a_album_id )
        return a_album


    #----------------------------------
    def query( self, a_album ):
        """
        what it says, read
        """
        query   = QSqlQuery( AppGlobal.qsql_db_access.db )

        sql     = self.sql
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

            a_album.add_point( a_point )
            print( f"ID: {a_point} " )




# ---- eof ---------------------------


