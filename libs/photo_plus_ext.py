# -*- coding: utf-8 -*-

# ---- tof
"""
consider cahge to photoExif

THIS IS A NEW IMPLEMENTATION OF PhotoPlus..... for the stuff

db, we will leave the old one around for geo_photo


Purpose:
    part of my ( rsh ) library of reusable code
    a library module for multiple applications
    sometimes included with applications but not used
        as this make my source code management easier.

Latitude and Longitude Finder on Map Get Coordinates
    *>url  https://www.latlong.net/

Degrees Minutes Seconds to Decimal Degrees Coordinates
    *>url  https://www.latlong.net/degrees-minutes-seconds-to-decimal-degrees

Map of the World with Latitude and Longitude
    *>url  https://www.mapsofworld.com/world-maps/world-map-with-latitude-and-longitude.html

GPS coordinates, latitude and longitude with interactive Maps
    *>url  https://www.gps-coordinates.net/


try google earth,  may have photos

stuff related to photo extensions

    in the string

    GPSInfo: {1: 'S', 2: (34.0, 4.0, 30.35), 3: 'E', 4: (18.0, 25.0, 19.84), 5: b'\x00', 6: 122.14, 7: (13.0, 33.0, 30.0), 16: 'M', 17: 47.0, 29: '2023:09:29'}
    ResolutionUnit: 2

    https://exiftool.org/TagNames/GPS.html

    GPS Tags
    *>url  https://exiftool.org/TagNames/GPS.html



    in a dict
    GPSLatitudeRef  = 1
    NorS            = 1

        N' = North    or positive number
        'S' = South   or negative number

    0x0002 	GPSLatitude = 2
        example  =  (34.0, 4.0, 30.35

    GPSLongitudeRef  3	string[2] 	(ExifTool will also accept a number when writing this tag, positive for east longitudes or negative for west, or a string containing E, East, W or West)
        'E' = East
        'W' = West

    GPSLongitude 	 = 4   rational64u[3]

        example  = (18.0, 25.0, 19.84)


0x0005 	GPSAltitudeRef 	int8u 	(ExifTool will also accept number when writing this tag, with negative numbers indicating below sea level)
0 = Above Sea Level
1 = Below Sea Level
0x0006 	GPSAltitude 	rational64u
0x0007 	GPSTimeStamp 	rational64u[3] 	(UTC time of GPS fix. When writing, date is stripped off if present, and time is adjusted to UTC if it includes a timezone)
0x0008 	GPSSatellites 	string
0x0009 	GPSStatus 	string[2] 	'A' = Measurement Active
'V' = Measurement Void
0x000a 	GPSMeasureMode 	string[2] 	2 = 2-Dimensional Measurement
3 = 3-Dimensional Measurement
0x000b 	GPSDOP 	rational64u
0x000c 	GPSSpeedRef 	string[2] 	'K' = km/h
'M' = mph
'N' = knots

"""


# ---- imports
#import collections
import stat
#import sys
#import dis

import gmplot
#from   gmplot import gmplot
import geopy
from   geopy.geocoders import Nominatim
import geopy.distance
from   geopy import Point
from   geopy.distance import geodesic


import webbrowser
import requests
import os
#import time
from   datetime import datetime


from typing import Tuple, Optional


import exifread
import PIL.Image
import PIL.ExifTags

from   pathlib import Path
#import haversine as hs
# import Units

# ---- local imports

import string_utils
import data

# FileInfo     = collections.namedtuple( "FileInfo" , "lat long elav date", defaults=( None, None ) )
# or could make a photo plus for each
# GeoInfo      =  collections.namedtuple( "GeoInfo" ,
                                       # "lat long elav date filename speed address",
                                       #  defaults=( None, None, None, None, None, None, None  )
                                       # )
DATETIME_FORMAT         = "%Y:%m:%d %H:%M:%S"

# ----------------------------------------
class PhotoPlus():
    """
    import photo_plus_ext.PhotoPlus
    this is a stripped down revision for old see photo_ext.py
    !!add size date.....

    get and use exif data from phots
    status    works, barely, missing any help with errors
              work on it  test in ./test/...


    """
    # ----------------------------------------
    def __init__( self, filename = None ):
        """
        many old functions about this and that removed may want to look at all versions
        old comments, valid?
        filename     name of a photo that hopefull contains exif data
        filename     is for now assumed to be full path... probably !!
        should convert if not

        filename is none will suppress read of file
        then manually populate


        """
        self.reset( filename )

    # -----------------------------
    def reset( self, filename = None ):
        """
        reset data, mostly to None, but
        if filename is not None
        fetch the data from the file
        reset the file name for reuse of the instance

        better if these were @properties

        filename     name of a photo that hopefull contains exif data
                    may use a None, then push in variables as in ..,,,
                    read_photo_points
                    test if also works with a file_path
        return
            mutates instance
        """
        #rint( "in reset" )
        self.filename           = filename   # work  with path ??
        self.ok                 = 1  # negative numbers for failure !! not implementd yet
        # self.geo_info.filename  = filename
        self.long               = None       # longiude as a desimal
        self.lat                = None       # latitude as a desimal
        self.address            = None
        self.size               = None       # size of file in btes
        self.datetime           = None       # some datetime... the one we use may have zone or not
        self.datetime_nz_str    = ""       # datetime with no zone info as a string
        self.timezone_str       = ""      # timezone as a string  also flag if zone is present use truthyness
        # self.datetime_str       = None       # datetime as a string
        self.timestamp          = None       # from exif
        self.speed              = None       # !! unit conversion not yet done
        self.has_lat_long       = False
        # self.geo_info           = GeoInfo( )
        # if filename:
        #     self.get_fast_data()
        #exif_dict               = {}   # this is my interpertation and includes some derived data


    # #----------------------------------------------------------------------
    # def set_lat_long_from_str( self, lat_decimal_str, long_decimal_str ):
    #     """
    #     set from two strings

    #     accepts blank "" strings then lat long is set to ?
    #         datetime_nz_string     datetime in format: DATETIME_FORMAT            = "%Y:%m:%d %H:%M:%S"
    #         timezone_str
    #     return
    #         mutate self

    #     """
    #     self.has_lat_long   = True

    #     if lat_decimal_str and lat_decimal_str != "None":
    #         self.lat             = float( lat_decimal_str )
    #     else:
    #         self.lat             = None
    #         self.has_lat_long    = False

    #     if long_decimal_str and long_decimal_str != "None":
    #         self.long             = float( long_decimal_str )
    #     else:
    #         self.long             = None
    #         self.has_lat_long    = False

    # #----------------------------------------------------------------------
    # def set_datetime_from_str( self, datetime_nz_str, timezone_str ):
    #     """
    #     set from two strings that are also seved in self.
    #         datetime_nz_string     datetime in format: DATETIME_FORMAT            = "%Y:%m:%d %H:%M:%S"
    #         timezone_str
    #     return
    #         mutate self

    #     """
    #     self.datetime_nz_str  = datetime_nz_str
    #     self.timezone_str     = timezone_str

    #     cont   = False    # b!! move to truthyness
    #     if datetime_nz_str:
    #         if timezone_str:
    #             cont = True

    #     # if datetime_nz_str and timezone_str:
    #     if cont:
    #         # we should be able to make timezone aware datetime
    #         #a_datetime_with_zone  = self.make_dt_with_zone( datetime_nz_str, timezone_str  )

    #         # ------------------------------
    #         # make_dt_with_zonexxx( self, exif_dt_original, exif_dt_offset  ):
    #         # ---- make exif dt timezone aware -- edited to short version
    #         utc_timezone        = datetime.strptime( timezone_str, "%z").tzinfo
    #         #print( f"utc_timezone {utc_timezone}")

    #         #------- now make the date
    #         a_datetime     = datetime.strptime( datetime_nz_str, DATETIME_FORMAT )
    #         # ex_helpers.info_about_datetime( a_datetime, msg = f"dt from {string_date}" )
    #         # ---- add timezone
    #         a_datetime    = a_datetime.astimezone( utc_timezone )

    #         self.datetime  = a_datetime
    #         # self.datetime_nz_str  = datetime_nz_str
    #         # self.timezone_str     = timezone_str
    #         # self.datetime         = a_datetime_with_zone

    #     else:
    #         #------- now make the date not aware
    #         try:
    #             msg     = str( datetime_nz_str )
    #             print( msg )
    #             self.datetime     = datetime.strptime( datetime_nz_str, DATETIME_FORMAT )
    #         except ValueError as an_except:
    #             self.datetime     = None

    #----------------------------------------------------------------------
    def get_name( self, ):
        """
        return
            the short name of the file
            no dir structure at all

        """
        return Path( self.filename ).name

    #----------------------------------------------------------------------
    def exifread_to_degrees( self, exifread_value, ref ):
        """
        Helper function to convert the GPS coordinates stored in the EXIF to degrees in float format
        Args:
            value angle as a tuple degree, min, seconds
        Return
            float
        chat uses list comp -- prob better


        """
        if exifread_value is None:
            return None

        d           = float( exifread_value.values[0].num) / float( exifread_value.values[0].den)
        m           = float( exifread_value.values[1].num) / float( exifread_value.values[1].den)
        s           = float( exifread_value.values[2].num) / float( exifread_value.values[2].den)

        decimal     = d + (m / 60.0) + (s / 3600.0)

        # fix sign these are negative
        if ref.values in ["S", "W"]:
            decimal = -decimal

        return decimal

    #----------------------------------------------------------------------
    def get_exifread_exif_dict( self ):
        """
        read and convert else None
            a dict

         and consider

         elevation_value         = tags.get( 'GPS GPSAltitude' )  # and ref

        return
            the dict -- full with None values if something is missing except
            empty dict if no exif data
        """
        try:
            with open( self.filename, "rb") as f:
                tags = exifread.process_file( f, details = False )
                    # details=False is faster

        except:
            tags  = {}

        # print( ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..")
        # print( f"\n{1} {type(tags) })")

        if tags is {}:
            return {}

        exifread_dict    = {}

        # ---- lat
        lat                         = tags.get( "GPS GPSLatitude" )
        ref                         = tags.get( "GPS GPSLatitudeRef" )
        exifread_dict[ "lat" ]      = self.exifread_to_degrees(
                                        exifread_value = lat, ref = ref )

        # ---- long
        lon                         = tags.get( "GPS GPSLongitude")
        ref                         = tags.get( "GPS GPSLongitudeRef" )

        exifread_dict[ "lon" ]      = self.exifread_to_degrees(
                                        exifread_value = lon, ref = ref )

        # ---- date -- as timestamp
        a_date                      = tags.get( "EXIF DateTimeOriginal" )

        if a_date is None:
            a_date                  = None

        else:
            a_date                  = str( a_date )
            try:
                a_date              = datetime.strptime( a_date, DATETIME_FORMAT )

            except Exception as exception:
                error_message = str( exception )
                msg  = ( f"!!Caught an error: strptime {error_message} string was {a_date}" )
                print( msg )
                a_date              = None
            if a_date is None:
                a_date = None
            else:
                a_date                  = int( a_date.timestamp() )
                #rint( a_date )

        exifread_dict[ "ts" ]       = a_date

        # ---- more -- have found trailing spaces
        exifread_dict[ "make" ]      = str( tags.get("Image Make" ) ).strip()
        exifread_dict[ "model" ]     = str( tags.get("Image Model" ) ).strip()

        return exifread_dict

    # # ----------------------------------
    # def make_dt_with_zonexxx( self, exif_dt_original, exif_dt_offset  ):
    #     """
    #     args are strings or string like
    #     change ?? to with zone or not depending on extif_dt_offset
    #     use extif data to make a timezone aware dt
    #     in ex_exif_tags.py ex_dates_and_times_with_zone  and photo_ext.py
    #     !! static
    #     """
    #     # print( "exif_dt_original {exif_dt_original}")
    #     # print( "exif_dt_offset   {exif_dt_offset}")

    #     # ---- make exif dt timezone aware -- edited to short version
    #     utc_timezone        = datetime.strptime( str( exif_dt_offset ), "%z").tzinfo
    #     #print( f"utc_timezone {utc_timezone}")

    #     #------- now make the date
    #     format         = "%Y:%m:%d %H:%M:%S"
    #     a_datetime     = datetime.strptime( str( exif_dt_original ), format )
    #     # ex_helpers.info_about_datetime( a_datetime, msg = f"dt from {string_date}" )
    #     # ---- add timezone
    #     a_datetime    = a_datetime.astimezone( utc_timezone )


    # # ----------------------------------------
    # def get_exif_string( self, all = False    ):
    #     """
    #     arg all so far does nothing
    #     """
    #     # -----
    #     img             = PIL.Image.open( self.filename )
    #     exif            = { PIL.ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in PIL.ExifTags.TAGS }

    #     if exif is None:
    #         exif = {}

    #     #rint( type(exif) )
    #     ret = "exif values:"
    #     for key, value in exif.items():
    #        #rint( key, value )
    #        ret     = f"{ret}\n{key}: {value}"
    #        #rint( type(what))
    #     #t( ret )
    #     return ret

    # ----------------------------------------
    def get_pil_exif_dict( self, all = False    ):
        """
        this pil method may be archived use exifread
        arg all so far does nothing
        """
        # -----
        print( f"\n\n{self.filename}")

        try:
            img                 = PIL.Image.open( self.filename )
            img_exif            = img._getexif()

        except:
            img_exif            = None

        if img_exif is None:
            img_exif = {}

        exif_dict           = { PIL.ExifTags.TAGS[k]: v for k, v in img_exif.items() if k in PIL.ExifTags.TAGS }

        if exif_dict is None:
            exif_dict = {}

        return exif_dict

    #----------------------------------------------------------------------
    def get_size( self,  ):
        """
        file size
            pathlib is more modern
        """
        stats      = os.stat( self.filename )
        my_size    = stats[stat.ST_SIZE]
        #rint(( "last access",        time.ctime(stats[stat.ST_ATIME]) ))
        #rint(( "last modification",  time.ctime(stats[stat.ST_MTIME]) ))
        #rint(( "last status change", time.ctime(stats[stat.ST_CTIME]) ))
        #rint(( "size ",              os.path.getsize(  file_name ) ))
        #rint(( "size ",              os.stat( file_name ).st_size  ))
        self.size   = my_size
        print( f"get_size {my_size}" )
        return my_size

    # #----------------------------------------------------------------------
    # def get_datetimexx( self,  ):
    #     """
    #     file get_datetime -- or is this jus a time
    #     return
    #         mutates self
    #     """
    #     stats      = os.stat( self.filename )
    #     dt         = time.ctime(stats[stat.ST_MTIME])
    #     #rint(( "last access",        time.ctime(stats[stat.ST_ATIME]) ))
    #     #rint(( "last modification",  time.ctime(stats[stat.ST_MTIME]) ))
    #     #rint(( "last status change", time.ctime(stats[stat.ST_CTIME]) ))
    #     #rint(( "size ",              os.path.getsize(  file_name ) ))
    #     #rint(( "size ",              os.stat( file_name ).st_size  ))
    #     self.datetime   = dt
    #     return dt

    # #----------------------------------------------------------------------
    # def _convert_to_degress( self, value ):
    #     """
    #     Helper function to convert the GPS coordinates stored in the EXIF to degrees in float format
    #     Args:
    #         value angle as a tuple degree, min, seconds
    #     Return
    #         float

    #     """

    #     d = float(value.values[0].num) / float(value.values[0].den)
    #     m = float(value.values[1].num) / float(value.values[1].den)
    #     s = float(value.values[2].num) / float(value.values[2].den)

    #     return d + (m / 60.0) + (s / 3600.0)

    # #----------------------------------------------------------------------
    # def get_location( self, long, lat  ):
    #     """
    #     return

    #     """
    #     geoloc     = Nominatim( user_agent = "GetLoc")
    #     locname    = geoloc.reverse( f"{lat}, {long}")
    #     adr        = locname.address

    #     print ( f"{repr(locname)}")
    #     print( adr )
    #     return adr


    # # ----------------------------------------
    # def _append_request( self, a_request, a_key, a_value ):
    #     """
    #     to aid in building requests


    #     """
    #     if a_value is not None:
    #         a_request = f"{a_request}&{a_key}={a_value}"
    #     return a_request

    # ----------------------------------------
    def get_address( self,   ):
        """
        Purpose:
            get a human readable address
        Returns: an address
        note location has long and lat in int
        this is somewhat expenmsive in terms of time
        """
        #rint( "\nget_address")
        #rint( "self.arg = ", f"{self.lat}, {self.long}", flush = True  )
        if self.lat is None or self.long is None:
            address = "None for self.lat or self.long = None"
        else:
            geoloc     = Nominatim( user_agent = "GetLoc")
            #rint( "arg to reverse", f"{self.lat}, {self.long}" )
            locname    = geoloc.reverse( f"{self.lat}, {self.long}")
            # what is error from this return None?
            if locname is None:
                #rint( "locname is none")
                return "no address found"
            #rint( f"repr(locname) {repr(locname)}")
            #rint( f"type(locname) {type(locname)}")
            address    = locname.address
            #rint( address )   # debug/test
        self.address  = address
        return address

    # -----------------------------------
    def __str__( self,   ):
        """
        usual debug string

        """
        return string_utils.obj_to_str( self )


    # ----------------------------------------
    def explore_locname_xxx( self,   ):
        """
        this is just for testing
        Returns: an address
        note location has long and lat in int
        """
        geoloc     = Nominatim( user_agent = "GetLoc" )
        locname    = geoloc.reverse( f"{self.lat}, {self.long}")
        print( f"repr(locname) {repr(locname)}")
        print( f"type(locname) {type(locname)}")
        address    = locname.address
        print( address )   # debug/test
        print( f"point  = {locname.point}")
        print( f"altitue   {locname.point[2]}"  )
        return address

# ----------------------------------------
class WebMap():
    """

     builds a .png of the map of the location.... as specified in the arguments


     but has someone already done this do not go too far
     center (required if markers not present) defines the center of the map,
     equidistant from all edges of the map. This parameter takes a location
     as either a comma-separated {latitude,longitude} pair
     (e.g. "40.714728,-73.998672") or a string address (e.g. "city hall, new york, ny") identifying a unique location on the face of the earth. For more information, see Locations.

      open file
      build html local
      center (required if markers not present) defines the center of the map, equidistant from all edges of the map.
      This parameter takes a location as either a comma-separated {latitude,longitude}
      pair (e.g. "40.714728,-73.998672") or a string address (e.g. "city hall, new york, ny") identifying a unique location on the face of the earth. For more information, see Locations.


    """
    def __init__( self, api_key, **kwargs ):


        self.reset( api_key,  **kwargs )

    # -----------------------------
    def reset( self, api_key,  **kwargs ):
        """



        """

    #----------------------------------------------------------------------
    def open_web_map_from_ll( self, long, lat, zoom_level = None ):
        """
        open given long, lat and zoom level ( or use instance ??)
        parameters
            ?? filename html
             ?? file name
             ?? open browser flag

        """
        if zoom_level is None:
            zoom_level  = self.zoom_level
        if zoom_level is None:
            zoom_level =  10

        filename_html  = r"d:/temp.html"  # need full path
        gmap       = gmplot.GoogleMapPlotter( lat, long, zoom_level )
        gmap.marker( lat, long, "cornflowerblue" )
        gmap.draw( filename_html )   # a file name for the html
        webbrowser.open( filename_html, new = 2 )        # auto open file above in new tab


# ----------------------------------------
class StaticMap():
    """

     builds a .png of the map of the location.... as specified in the arguments

      open file
      build html local
      center (required if markers not present) defines the center of the map, equidistant from all
      edges of the map. This parameter takes a location as either a comma-separated {latitude,longitude}
      pair (e.g. "40.714728,-73.998672") or a string address (e.g. "city hall, new york, ny")
      identifying a unique location on the face of the earth. For more information, see Locations.

    """
    def __init__( self, api_key, **kwargs ):
        """


        """
        self.reset( api_key,  **kwargs )

    # -----------------------------
    def reset( self, api_key,  **kwargs ):
        """
        see test for args
        static map center as latitude, longitude

        """
        #rint( "in reset" )

        self.api_key          = api_key
        #rint( self.api_key )

        # !! fix rest of them
        self.url        = kwargs.get( "url",  "https://maps.googleapis.com/maps/api/staticmap?" )

        self.sensor     = kwargs.get( "sensor",  None )

        self.size       = kwargs.get( "size", "400x400" )  # may be limit at 640 .. {} )
        #rint( self.size )
        self.zoom       = kwargs.get( "zoom", 5 )
        self.center     = kwargs.get( "center", None )

        # center=-32.3917,115.867 as string??  for lat long
        # self.marker     = kwargs.get( "marker", "cornflowerblue" )
        self.marker     = kwargs.get( "marker", "size:mid%7Ccolor:0x2e3a5c%7Clabel:1%7CAlbany%2C%20NY" )

        #size:mid%7Ccolor:0x2e3a5c%7Clabel:1%7CAlbany%2C%20NY

        # my_request: https://maps.googleapis.com/maps/api/staticmap?
        # &center=41.53993055555556, -71.00936388888888&zoom=15&key=AIzaSyAP6Vp7EvZFOf02PsnzQtR7oimSoTqtKJw&
        #size=600x600
        # &marker=cornflowerblue

        # markers=size:mid%7Ccolor:0x2e3a5c%7Clabel:1%7CAlbany%2C%20NY

        #rint( f"\n\n StaticMap.reset   url {self.url},\n    size {self.size}, ...." )
        return

    # ----------------------------------------
    def _append_request( self, a_request, a_key, a_value ):
        """
        to aid in building requests
        read the code

        """
        if a_value is not None:
            a_request = f"{a_request}&{a_key}={a_value}"

        #rint( a_key )
        #rint( a_value )
        #rint( a_request )

        return a_request

    # ----------------------------------------
    def make_center_marker( self, ):
        """
        add a center marker, center needs to already be in the dict
        blows out any other center
        works for lat long, else may not work
        !! work on this and options
        """
        self.marker    = f"size:mid%7Ccolor:0x2e3a5c%7Clabel:*%7C{self.center}"

    # -----------------------------
    def write_map_file( self, file_name_out ):
        """
        write file after all set up
        return None
               file in file system

               # size            = "600x300"
               # maptype         = "roadmap"
               # file_format     = "png"      # format

               # marker          = "size:mid%7Ccolor:0x2e3a5c%7Clabel:1%7CAlbany%2C%20NY"   #marker

        """
        my_request      = self.url
        my_request      = self._append_request( my_request, "center",  self.center  )
        my_request      = self._append_request( my_request, "zoom",    self.zoom    )
        my_request      = self._append_request( my_request, "key",     self.api_key )
        my_request      = self._append_request( my_request, "size",    self.size    )
        my_request      = self._append_request( my_request, "sensor",  self.sensor  )
        my_request      = self._append_request( my_request, "markers", self.marker  )  # markers !!!!

        #rint( f"my_request: {my_request}" )
        #rint()

        r = requests.get( my_request )

        with open( file_name_out, 'wb') as a_file:
            a_file.write(r.content)

        if len( r.content ) < 5000  :   # generally an error
            print( "len( r.content ) < 5000 perhaps an error look at console")
            #rint( r.content )

# ----------------------------------------
class DistanceFrom():
    """
    set a reference name lat long
    then add places name lat long and compute the distance from the
        reference geopy.Distance
        photo_plus_ext.DistanceFrom( name, from_lat, from_long ) )

    haversine as hs
    pip install haversine
        Latitude is written before longitude. Latitude is written with a number,
        followed by either “north” or “south” depending on whether it is located north or south of the equator.
        Longitude is written with a number, followed by either “east” or “west” depending on
        whether it is located east or west of the Prime Meridian.

    """
    # ----------------------------------------
    def __init__( self, name, from_lat, from_long ):
        """
        """
        # self.MILE       = "mile"
        # self.METER      = "meter"
        # self.KM         = "kilometers"


        self.reset( name, from_lat, from_long, )

    # ----------------------------------------
    def reset( self, name, from_lat, from_long, ):
        """
        units    from Units

        Returns
            None but mutates self

        """
        self.from_lat   = from_lat
        self.from_long  = from_long
        self.from_name  = name

        # unit            = self._normalise_unit( unit )
        # self.unit       = unit   # these are normalized

        self.places       = {}  # dict of dicts


    # # ----------------------------------------
    # def _normalise_unit( self, unit ):
    #     """
    #     unit a string representing the units
    #     very permissive
    #         unit   unit as a string
    #     returns
    #          normalized units -- a string like self.KM
    #     """
    #     unit           = unit.lower()

    #     if unit.startswith( "me"):
    #        n_unit = self.METER

    #     elif unit.startswith( "mi"):
    #         n_unit = self.MILE

    #     elif unit.startswith( "k"):
    #         n_unit = self.KM

    #     else:
    #         pass  # need exception

    #     return n_unit

    # # ----------------------------------------
    # def _convert_to_distance ( self,  a_float, unit  ):
    #     """
    #     a_distance   ,, instance of distance
    #     units a string representing the units

    #     returns
    #         a float


    #     what units
    #     from geopy.units import radians
    #     @property
    #     def feet(self):
    #         return units.feet(kilometers=self.kilometers)

    #     @property
    #     def ft(self):
    #         return self.feet

    #     @property
    #     def kilometers(self):
    #         return self.__kilometers

    #     @property
    #     def km(self):
    #         return self.kilometers

    #     @property
    #     def m(self):
    #         return self.meters

    #     @property
    #     def meters(self):
    #         return units.meters(kilometers=self.kilometers)

    #     @property
    #     def mi(self):
    #         return self.miles

    #     @property
    #     def miles(self):
    #         return units.miles(kilometers=self.kilometers)

    #     @property
    #     def nautical(self):
    #         return units.nautical(kilometers=self.kilometers)

    #     @property
    #     def nm(self):
    #         return self.nautical

    #     """
    #     converted_distance   = None
    #     unit                 = self._normalise_unit( unit )

    #     if unit == self.METER:
    #        converted_distance  = float( a_distance.m )
    #        a_distance          = Distance( meters  = xxx )
    #        a_distance          = Distance( miles   = xxx )

    #                     Distance(kilometers=10)

    #                    Distance(kilometers=10)



    #     elif unit == self.MILE:
    #         converted_distance  = float( a_distance.mi )

    #     elif unit == self.KM:
    #         converted_distance  = float( a_distance.km )

    #     else:
    #         pass  # need exception
    #     return converted_distance

    # ----------------------------------------
    def add_place( self, name, lat, long,  ):
        """
        need to add tests and doc

        returns a place and mutates  self.place

        """
        # # -- using haversign
        # the_distance = hs.haversine( (self.from_lat, self.from_long ), ( lat, long ) )

        # -- using geopy
        a_distance  = geopy.distance.geodesic( ( self.from_lat, self.from_long ), ( lat, long ), )

        a_place     = { "name":     name,
                        "lat":      lat,
                        "long":     long,
                        "distance": a_distance,
                           }
        #a_distance[ "name"]   = name

        self.places[name]  = a_place

        #rint( a_distance )
        #print( self.places )

        return a_place

    # ----------------------------------------
    def shift_longitude( self, delta_km: float ):
    #def shift_longitude_west( self, lat: float, lon: float, delta_km: float ) -> Optional[float]:
        """
        Shifts a point west by a given distance (in km) and returns the new longitude.

        Handles cases where the geodesic crosses the 180th meridian.
        Returns None if the starting point is exactly at a pole (lat = ±90°).

        Args:
            lat: Latitude in signed degrees (North positive).
            lon: Longitude in signed degrees (East positive).
            delta_km: Distance in kilometers to shift west.

        Returns:

            lon_east, lon_west = *( new_lon_east, new_lon_west )
            in signed degrees, or None if operation is not possible.
        """
        # Geodesic calculation fails at the poles due to undefined bearing.
        # may also fail if wraps around earth in which case do from???
        if abs( self.from_lat ) == 90.0:
            return None

        start_point = Point( self.from_lat , self.from_long )

        # ---- west
        # 'distance' is the geodesic distance; 'bearing' is 270° (West).
        destination = geodesic( kilometers = delta_km ).destination( start_point, 270 )
                # The `geodesic()` constructor accepts several named arguments for distance:
                # see stuffdb
        new_lon = destination.longitude

        # Normalize longitude to the range [-180, 180) for consistency.
        if  new_lon >= 180:
            new_lon -= 360

        elif new_lon < -180:
             new_lon += 360

        new_lon_west  = new_lon

        # ---- east
        destination = geodesic( kilometers = delta_km ).destination( start_point, 90 )
                # The `geodesic()` constructor accepts several named arguments for distance:
                # see stuffdb
        new_lon = destination.longitude
        # Normalize longitude to the range [-180, 180) for consistency.
        if new_lon >= 180:
            new_lon -= 360
        elif new_lon < -180:
            new_lon += 360

        new_lon_east  = new_lon

        return ( new_lon_west, new_lon_east,  )  # low to high

    # ----------------------------------------
    def shift_latitude( self, delta_km: float ) -> Optional[Tuple[float, float]]:
    # def shift_latitude_south(lat: float, lon: float, delta_km: float) -> Optional[Tuple[float, float]]:
        """
        Shifts a point south by a given distance (in km) and returns the new latitude.

        If the shift crosses the South Pole, returns the final point after passing the pole.
            I am ignoring crossing the south pole for now

        Returns None if the starting point is exactly at a pole (lat = ±90°).

        Args:
            lat: Latitude in signed degrees (North positive).
            lon: Longitude in signed degrees (East positive).
            delta_km: Distance in kilometers to shift south.

        Returns:
            Tuple of (new_latitude, new_longitude) in signed degrees, or None if operation
            is not possible.

        why would the longitude also change I am going to suppress for now
            but ask later

        """
        # Geodesic calculation fails at the poles due to undefined bearing.
        if abs( self.from_lat ) == 90.0:
            return ( 0., 0., )

        start_point = Point( self.from_lat, self.from_long )

        # 'distance' is the geodesic distance; 'bearing' is 180° (South).
        destination = geodesic( kilometers = delta_km ).destination( start_point, 0 )

        new_lat = destination.latitude
        new_lon = destination.longitude

        # Normalize latitude to the range [-90, 90].
        if  new_lat > 90:
            new_lat = 180 - new_lat
            new_lat += 180

        elif new_lat < -90:
            new_lat = -180 - new_lat
            new_lat += 180

        new_north_lat = new_lat

        # ---- south
        destination = geodesic( kilometers = delta_km ).destination( start_point, 180 )

        new_lat = destination.latitude
        new_lon = destination.longitude

        # Normalize latitude to the range [-90, 90].
        if  new_lat > 90:
            new_lat = 180 - new_lat
            new_lat += 180

        elif new_lat < -90:
            new_lat = -180 - new_lat
            new_lat += 180

        new_south_lat = new_lat

        return ( new_south_lat, new_north_lat, )  # low to high

    # -----------------------------------
    def print_str( self,   ):
        """
        a debug or utility string
        """
        line_begin  ="   "
        a_str = ""
        a_str = f"{a_str}\n>>>>>>>>>>* DistanceFrom Contents ) *<<<<<<<<<<<<"
        a_str = f"{a_str}{line_begin}   from name             {self.from_name}"
        a_str = f"{a_str}{line_begin}   from lat, long        {self.from_lat}, {self.from_long}"
        places  = self.places
        for i_key, i_value in places.items():
            print( f"{i_key}" ) #"     {i_value}" )

            for i_name, i_data in i_value.items():
                print( f"{line_begin}    {i_name}, {i_data}" )
       # _str = f"{a_str}{line_begin}   from location name       {self.lat}, {self.long}"

        #a_str = f"{a_str}{line_begin}   self.distances        {self.distances}"
        #a_str = f"{a_str}\n   units        {self.computername}"
        # a_str = f"{a_str}\n   our_os              {self.our_os}"

        #a_str = f"{a_str}\n   snip_file_fn            {self.snip_file_fn}"
        #a_str = f"{a_str}\n   snippets_fn             {self.snippets_fn}"
        # a_str = f"{a_str}{line_begin}   ex_editor                {self.ex_editor}"

        # a_str = f"{a_str}{line_begin}   --- logging  ---"
        # a_str = f"{a_str}{line_begin}   comm_logging_fn          {self.comm_logging_fn}"


    # -----------------------------------
    def get_str( self,   ):
        """
        a debug or utility string
        """
        line_begin  ="\n"
        a_str = ""
        a_str = f"{a_str}\n>>>>>>>>>>* DistanceFrom Contents ) *<<<<<<<<<<<<"
        a_str = f"{a_str}{line_begin}   from name             {self.from_name}"
        a_str = f"{a_str}{line_begin}   from lat, long        {self.from_lat}, {self.from_long}"
        places  = self.places
        for i_key, i_value in places.items():
            for i_name, i_data in i_value.items():
                a_str = f"{a_str}{line_begin}      {i_name}, {i_value}"
       # _str = f"{a_str}{line_begin}   from location name       {self.lat}, {self.long}"

        #a_str = f"{a_str}{line_begin}   self.distances        {self.distances}"
        #a_str = f"{a_str}\n   units        {self.computername}"
        # a_str = f"{a_str}\n   our_os              {self.our_os}"

        #a_str = f"{a_str}\n   snip_file_fn            {self.snip_file_fn}"
        #a_str = f"{a_str}\n   snippets_fn             {self.snippets_fn}"
        # a_str = f"{a_str}{line_begin}   ex_editor                {self.ex_editor}"

        # a_str = f"{a_str}{line_begin}   --- logging  ---"
        # a_str = f"{a_str}{line_begin}   comm_logging_fn          {self.comm_logging_fn}"


        return a_str

    #-------------------------- import string_utils
    def __str__( self ):
        """universal __str__ """
        return string_utils.obj_to_str( self )



# ---- look for tests in sub_dir test

# ---- eof



