# -*- coding: utf-8 -*-
"""
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

import os
# ---- imports
#import collections
import stat
import sys
import time
import traceback
import webbrowser
from datetime import datetime, timedelta, timezone
from pathlib import Path

import exifread
#import dis
import geopy
import geopy.distance
import gmplot
# import haversine as hs
import PIL.ExifTags
import PIL.Image
# import datetime  -- this messes up above
import pytz
import requests
from dateutil import tz
from geopy.geocoders import Nominatim
from gmplot import gmplot

# import Units

# ---- local imports
sys.path.append( r"D:\Russ\0000\python00\python3\_projects\rsh"  )
import data
from app_global import AppGlobal
import app_exceptions

# FileInfo     = collections.namedtuple( "FileInfo" , "lat long elav date", defaults=( None, None ) )
# or could make a photo plus for each
# GeoInfo      =  collections.namedtuple( "GeoInfo" ,
                                       # "lat long elav date file_name speed address",
                                       #  defaults=( None, None, None, None, None, None, None  )
                                       # )
DATETIME_FORMAT         = "%Y:%m:%d %H:%M:%S"

# ------------------------------------------
def make_file_list( path_name  = None, suffixes = None ):
    """
    Purpose:
        given a file name, scan the directory it is in
        and make a file list in this object for it
        not sure if is recusife uses glob
        was geo_track.py def _dir_to_filelist_old( self, filename  = None ):
    arguments
        path_name -- for dir to search -- may be file or dir
    returns:
        file_list
    """
    if suffixes is None:
        suffixes        = ["jpg","png", ]
    file_list     = []
    # apparently we also need to check for empty file name

    path_name  = path_name.strip()
    if path_name == "":
        msg   = (f"File, {path_name}, is empty; operation terminated")
        print( msg )
        raise app_exceptions.ReturnToGui( msg )

    path_name   = Path( path_name )
    if not path_name.exists():
        msg   = (f"File, {path_name}, does not exist; operation terminated")
        print( msg )
        raise app_exceptions.ReturnToGui( msg )

    if path_name.is_file():
        path_name    = path_name.parent

    file_list       = [ str(path.absolute() )
                        for i in suffixes for path in path_name.glob("*."+i)]

    return file_list


# ---- grok say, russ mods

def dms_to_decimal( degrees, minutes, seconds, ref ):
    """Convert DMS (degrees, minutes, seconds) to decimal degrees."""
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal

def get_gps_coordinates( gps_info ): # exif['GPSInfo']
        """ """


        #gps_info = exif['GPSInfo']
        # Map GPS sub-tags to names
        gps_tags = {PIL.ExifTags.GPSTAGS.get(tag, tag): value for tag, value in gps_info.items()}

        # Extract latitude and longitude
        if 'GPSLatitude' in gps_tags and 'GPSLatitudeRef' in gps_tags:
            lat_dms = gps_tags['GPSLatitude']
            lat_ref = gps_tags['GPSLatitudeRef']
            latitude = dms_to_decimal(
                lat_dms[0].numerator / lat_dms[0].denominator,
                lat_dms[1].numerator / lat_dms[1].denominator,
                lat_dms[2].numerator / lat_dms[2].denominator,
                lat_ref
            )
        else:
            latitude = None

        if 'GPSLongitude' in gps_tags and 'GPSLongitudeRef' in gps_tags:
            lon_dms = gps_tags['GPSLongitude']
            lon_ref = gps_tags['GPSLongitudeRef']
            longitude = dms_to_decimal(
                lon_dms[0].numerator / lon_dms[0].denominator,
                lon_dms[1].numerator / lon_dms[1].denominator,
                lon_dms[2].numerator / lon_dms[2].denominator,
                lon_ref
            )
        else:
            longitude = None

        return latitude, longitude

def exif_date_to_timestamp( date_str ):
    """
    Grok say, and seems to work
    read it
    """
    try:
        dt = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
        return int(dt.timestamp())
    except ValueError:
        return None


# ----------------------------------------
class PhotoPlus():
    """
    !!add size date.....

    get and use exif data from phots
    status    works, barely, missing any help with errors
              work on it  test in ./test/...

    photo_plus   = photo_ext.PhotoPlus( i_file )  # i_file = None if not reading file
    photo_plus.get_data()
    lat   = photo_plus.lat
    long  = photo_plus.long

    """
    # ----------------------------------------
    def __init__(self, file_name = None, timezone_missing = None   ):
        """
        file_name     name of a photo that hopefully contains exif data
        file_name     is for now assumed to be full path... probably !!
        should convert if not

        file_name is none will suppress read of file
        then manually populate


        """
        self.reset( file_name, timezone_missing )

    # -----------------------------
    def reset( self, file_name = None, timezone_missing = None ):
        """
        reset data, mostly to None, but
        if file_name is not None
        fetch the data from the file
        reset the file name for reuse of the instance

        better if these were @properties

        file_name     name of a photo that hopefully contains exif data
                    may use a None, then push in variables as in ..,,,
                    read_photo_points
        return
            mutates instance
        """
        #rint( "in reset" )
        self.file_name           = file_name   # work  with path ??
        self.timezone_missing   = timezone_missing
                                    # timezone to use if missing in photo, or falsy
        # self.ok                 = 1  # negative numbers for failure !! not implemented yet
        # # self.geo_info.file_name  = file_name
        # self.lat                = None       # latitude as a 40
        # self.long               = None       # longitude as a -70.0

        self.address            = None
        # self.size               = None       # size of file in bytes
        self.datetime           = None       # some datetime... the one we use may have zone or not
                                             # make utc if possible
        self.datetime_nz_str    = ""         # datetime with no zone info as a string
        self.timezone_str       = ""         # timezone as a string  also flag if zone is present use truthiness
        # self.datetime_str       = None       # datetime as a string
        self.timestamp          = None       # from exif
        self.speed              = None       # !! unit conversion not yet done
        # self.has_lat_long       = False
        # self.geo_info           = GeoInfo( )
        # or put in one dict
        self.exif_dict_from_pil = { }
        self.os_dict            = { }


    #----------------------------------------------------------------------
    def set_lat_long_from_str( self, lat_decimal_str, long_decimal_str ):
        """
        set from two strings

        accepts blank "" strings then lat long is set to ?
            datetime_nz_string     datetime in format: DATETIME_FORMAT            = "%Y:%m:%d %H:%M:%S"
            timezone_str
        return
            mutate self

        """
        self.has_lat_long   = True

        if lat_decimal_str and lat_decimal_str != "None":
            self.lat             = float( lat_decimal_str )
        else:
            self.lat             = None
            self.has_lat_long    = False

        if long_decimal_str and long_decimal_str != "None":
            self.long             = float( long_decimal_str )
        else:
            self.long             = None
            self.has_lat_long     = False

    #----------------------------------------------------------------------
    def utc_datetime_from_str( self, datetime_nz_str, timezone_str, default_timezone_str, msg = None ):
        """
        using strings get a utc datetime
        args:
            read the code
        return
            utc_datetime
        raises
            will raise exception if errors

        """
        if timezone_str == "None":
            timezone_str    = default_timezone_str

        try:

            if   timezone_str.startswith( "UTC" ):
                a_timezone = tz.gettz( timezone_str  )

            elif timezone_str.startswith( "+" ) or timezone_str.startswith( "-" ):
                timezone_str    = f"UTC{timezone_str}"
                a_timezone      = tz.gettz( timezone_str  )

            else:
                a_timezone   = pytz.timezone( timezone_str )

            a_datetime   = datetime.strptime( datetime_nz_str, DATETIME_FORMAT  )
            # apply zone
            a_datetime   = a_datetime.replace( tzinfo = a_timezone )
            # to utc
            a_datetime   = a_datetime.astimezone( timezone.utc )
            # print( repr( a_datetime ))

            #self.set_datetime_from_str(   datetime_nz_str, timezone_str   )

        except Exception as an_except:

            msg     = f"a_except         >>{an_except}<<  type  >>{type( an_except)}<<"
            print( msg )
            AppGlobal.logger.debug( msg )


            msg     = ( f"during processing for >>{msg}<< and "
                        f"\n    default_timezone_str = {default_timezone_str} and"
                        f"\n    timezone_str         = {timezone_str} " )
            print( msg )
            AppGlobal.logger.debug( msg )

            s_trace = traceback.format_exc()
            msg     = f"format-exc       >>{s_trace}<<"
            print( msg )
            AppGlobal.logger.error( msg )   #    AppGlobal.logger.debug( msg )

            raise

        debug_stop   = 1

        return a_datetime

    #----------------------------------------------------------------------
    def set_datetime_from_strxxxx( self, datetime_nz_str, timezone_str ):
        """
        set from two strings that are also saved in self.
            datetime_nz_string     datetime in format: DATETIME_FORMAT            = "%Y:%m:%d %H:%M:%S"
            timezone_str
        return
            mutate self

        """
        self.datetime_nz_str  = datetime_nz_str
        self.timezone_str     = timezone_str

        cont   = False    # b!! move to truthyness
        if datetime_nz_str:
            if timezone_str:
                cont = True

        # if datetime_nz_str and timezone_str:
        if cont:
            # we should be able to make timezone aware datetime
            #a_datetime_with_zone  = self.make_dt_with_zone( datetime_nz_str, timezone_str  )

            # ------------------------------
            # make_dt_with_zonexxx( self, exif_dt_original, exif_dt_offset  ):
            # ---- make exif dt timezone aware -- edited to short version
            utc_timezone        = datetime.strptime( timezone_str, "%z").tzinfo
            #print( f"utc_timezone {utc_timezone}")

            #------- now make the date
            a_datetime     = datetime.strptime( datetime_nz_str, DATETIME_FORMAT )
            # ex_helpers.info_about_datetime( a_datetime, msg = f"dt from {string_date}" )
            # ---- add timezone
            a_datetime    = a_datetime.astimezone( utc_timezone )

            self.datetime  = a_datetime
            # self.datetime_nz_str  = datetime_nz_str
            # self.timezone_str     = timezone_str
            # self.datetime         = a_datetime_with_zone

        else:
            #------- now make the date not aware
            try:
                msg     = str( datetime_nz_str )
                print( msg )
                self.datetime     = datetime.datetime.strptime( datetime_nz_str, DATETIME_FORMAT )
            except ValueError as an_except:
                self.datetime     = None

    #----------------------------------------------------------------------
    def get_name( self, ):
        """
        return
            the short name of the file
            no dir structure at all
            for None return ""
        """
        if self.file_name is None:
            return ""
        else:
            return Path( self.file_name ).name

    #----------------------------------------------------------------------
    def exif_from_exifreadxxxx( self,  ):
        """
        this is old, puts values into self
        seems to required a lot of work compared to tet_exif_dict_from_pil

        get the exif data we use that is quick
        see code for details
        return
            mutate:  self
                ???
                    self.datetime           = None       # some datetime... the one we use may have zone or not
                    self.datetime_nz_str    = None       # datetime with no zone info
                    self.timezone_str       = None       # timezone as a string
                    self.datetime_str       = None       # datetime as a string
        """
        # ret   = None, None
        #file_name_debug   = self.file_name
       # print( f"for debug, fast_data for {file_name_debug}")
        timezone_missing_debug   = self.timezone_missing
        with open( self.file_name, 'rb' ) as f:
            tags            = exifread.process_file( f )
            latitude        = tags.get('GPS GPSLatitude'     )
            latitude_ref    = tags.get('GPS GPSLatitudeRef'  )
            longitude       = tags.get('GPS GPSLongitude'    )
            longitude_ref   = tags.get('GPS GPSLongitudeRef' )


            if latitude and longitude:
                self.has_lat_long = True
                lat_value = self._convert_to_degress( latitude )
                if latitude_ref.values != 'N':
                    lat_value = -lat_value

                lon_value  = self._convert_to_degress(longitude)
                if longitude_ref.values != 'E':
                    lon_value = -lon_value

                #ret =  ( lat_value, lon_value, )
            else:
                lat_value   = None
                lon_value   = None

            # self.geo_info.lat       = lat_value
            # self.geo_info.long      = long_value

            self.lat                = lat_value
            self.long               = lon_value

            self.address            = "not set or fetched"

            elevation_value         = tags.get( 'GPS GPSAltitude' )  # and ref
            # self.geo_info.long = long_value

            timestamp               = tags.get( "GPS GPSTimeStamp" )  # is a constant better than a literal test in ex_timing
            # self.geo_info.timestampn = long_value
            self.timstamp           = timestamp               # need type


           # 0x882a 	TimeZoneOffset 	int16s[n] 	ExifIFD 	(1 or 2 values:
           #    1. The time zone offset of DateTimeOriginal from GMT in hours,
           #    2. If present, the time zone offset of ModifyDate)

            speed_ref               = tags.get( "GPS GPSSpeedRef" )    # 	'K' = km/h 'M' = mph  'N' = knots

            speed                   = tags.get( "GPS GPSSpeed" )
            # self.geo_info.speed     = speed
            self.speed              = speed

            size                    = os.path.getsize( self.file_name  )
            self.size               = size
            stats                   = os.stat( self.file_name )
            # self.datetime           = datetime.datetime.fromtimestamp( stats[stat.ST_MTIME] )

            # ---- datetime is all that is left may be None
            tag          =  tags.get( "EXIF DateTimeOriginal"   )
            if tag:
                datetime_nz_str = str( tag )
            else:
                datetime_nz_str = ""
                #print( f"datatime string not found for {self.file_name}")

                # else:
                self.datetime    = None
                msg     =  f"for file {self.file_name} there was no datetime info "
                print( msg )
                AppGlobal.logger.log( 10, msg )

                return

            # there are 3 zone tags try them all
            tag            =  tags.get( "EXIF OffsetTimeOriginal" )  # may not be valid?
            tag            =  tags.get( "EXIF OffsetTime" )


            self.datetime             = self.utc_datetime_from_str(
                datetime_nz_str       = datetime_nz_str,
                timezone_str          = str( tag ),
                default_timezone_str  = self.timezone_missing,
                msg                   = f"for >>{self.file_name}<<" )

            debug_stop   = 1

    # ----------------------------------
    def make_dt_with_zonexxx( self, exif_dt_original, exif_dt_offset  ):
        """
        args are strings or string like
        change ?? to with zone or not depending on exif_dt_offset
        use exif data to make a timezone aware dt
        in ex_exif_tags.py ex_dates_and_times_with_zone  and photo_ext.py
        !! static
        """
        # print( "exif_dt_original {exif_dt_original}")
        # print( "exif_dt_offset   {exif_dt_offset}")

        # ---- make exif dt timezone aware -- edited to short version
        utc_timezone        = datetime.datetime.strptime( str( exif_dt_offset ), "%z").tzinfo
        #print( f"utc_timezone {utc_timezone}")

        #------- now make the date
        format         = "%Y:%m:%d %H:%M:%S"
        a_datetime     =  datetime.datetime.strptime( str( exif_dt_original ), format )
        # ex_helpers.info_about_datetime( a_datetime, msg = f"dt from {string_date}" )
        # ---- add timezone
        a_datetime    = a_datetime.astimezone( utc_timezone )

        return a_datetime

    # ----------------------------------------
    def exif_stringxxx( self, all = False    ):
        """

        depricate --- a dict is better
        """
        # -----
        img             = PIL.Image.open( self.file_name )
        exif            = { PIL.ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in PIL.ExifTags.TAGS }
        #rint( type(exif) )
        ret = "exif values:"
        for key, value in exif.items():
            #rint( key, value )
            ret     = f"{ret}\n{key}: {value}"
            #rint( type(what))
        #t( ret )
        return ret

    #from PIL import Image, ExifTags
    # ----------------------------------------
    def get_exif_dict_from_pil( self,   ):
        """
        get data into a dict or None
        read it
        new 2025
        """
        exif_dict   = self.exif_dict
        image       = PIL.Image.open( self.file_name )
        exif_data   = image._getexif()

        if exif_data:
            exif_dict = {PIL.ExifTags.TAGS.get(tag, tag): value for tag, value in exif_data.items()}

        else:
            return exif_dict

        # geo data is in its own dict
        exif_geo_dict    = exif_dict.get( "GPSInfo", None )
        if exif_geo_dict is not None:
            msg    = (f" processing ----------- {exif_geo_dict = }")
            print( msg )
            latitude, longitude         = get_gps_coordinates( exif_geo_dict )
            exif_dict[ "Latitude" ]     = latitude
            exif_dict[ "Longitude" ]    = longitude
            # else will be missing

        # make_model     = ( f "{exif_dict.get( 'DateTime', 'none'  )}/
        #                    {}  " )

        dt_original_ts  =  exif_date_to_timestamp(
                              exif_dict.get( "DateTime", None  ) )

        exif_dict[ "dt_original_ts" ]    = dt_original_ts

        # msg     = ( f"exif_dict_from_pil {exif}" )
        # print( msg )

        return exif_dict  # but mutated

    #----------------------------------------------------------------------
    def get_os_dict( self,  ):
        """
        file size
        exif_dict[ "dt_original_ts" ]    = dt_original_ts
        """
        os_dict    = self.os_dict   # and mutate

        stats      = os.stat( self.file_name )
        my_size    = stats[stat.ST_SIZE]
        #rint(( "last access",        time.ctime(stats[stat.ST_ATIME]) ))
        #rint(( "last modification",  time.ctime(stats[stat.ST_MTIME]) ))
        #rint(( "last status change", time.ctime(stats[stat.ST_CTIME]) ))
        #rint(( "size ",              os.path.getsize(  file_name ) ))
        #rint(( "size ",              os.stat( file_name ).st_size  ))


        os_dict[ "size" ]     = my_size

        return os_dict

    #----------------------------------------------------------------------
    def get_datetimexx( self,  ):
        """
        file get_datetime -- or is this just a time
        return
            mutates self
        """
        stats      = os.stat( self.file_name )
        dt         = time.ctime(stats[stat.ST_MTIME])
        #rint(( "last access",        time.ctime(stats[stat.ST_ATIME]) ))
        #rint(( "last modification",  time.ctime(stats[stat.ST_MTIME]) ))
        #rint(( "last status change", time.ctime(stats[stat.ST_CTIME]) ))
        #rint(( "size ",              os.path.getsize(  file_name ) ))
        #rint(( "size ",              os.stat( file_name ).st_size  ))
        self.datetime   = dt
        return dt

    #----------------------------------------------------------------------
    def _convert_to_degress( self, value ):
        """
        Helper function to convert the GPS coordinates stored in the EXIF to degrees in float format
        Args:
            value angle as a tuple degree, min, seconds
        Return
            float

        """
        d = float(value.values[0].num) / float(value.values[0].den)
        m = float(value.values[1].num) / float(value.values[1].den)
        s = float(value.values[2].num) / float(value.values[2].den)

        return d + (m / 60.0) + (s / 3600.0)


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
        this is somewhat expensive in terms of time
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
            more formatting might be nice
        """
        a_str =  ">>>>>>>>>>* PhotoPlus instance var (some) *<<<<<<<<<<<<"
        a_str = f"{a_str}\n   file_name          {self.file_name}         {type(self.file_name)}"

        a_str = f"{a_str}\n   lat               {self.lat}              {type(self.lat)}"
        a_str = f"{a_str}\n   long              {self.long}             {type(self.long)}"
        a_str = f"{a_str}\n   has_lat_long      {self.has_lat_long}     {type(self.has_lat_long)}"
        a_str = f"{a_str}\n   datetime          {self.datetime}         {type(self.datetime)}"
        a_str = f"{a_str}\n   datetime_nz_str   {self.datetime_nz_str}  {type(self.datetime_nz_str)}"
        a_str = f"{a_str}\n   timezone_str      {self.timezone_str}     {type(self.timezone_str)}"
        a_str = f"{a_str}\n   timezone_missing  {self.timezone_missing} {type(self.timezone_missing)}"
        a_str = f"{a_str}\n   address           {self.address}          {type(self.address)}"
        a_str = f"{a_str}\n   size              {self.size}             {type(self.size)}"

        return a_str

    # ----------------------------------------
    def explore_locname_xxx( self,   ):
        """
        this is just for testing
        Returns: an address
        note location has long and lat in int
        """
        geoloc     = Nominatim( user_agent = "GetLoc")
        locname    = geoloc.reverse( f"{self.lat}, {self.long}")
        print( f"repr(locname) {repr(locname)}")
        print( f"type(locname) {type(locname)}")
        address    = locname.address
        print( address )   # debug/test
        print( f"point  = {locname.point}")
        print( f"altitude   {locname.point[2]}"  )
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
            ?? file_name html
             ?? file name
             ?? open browser flag

        """
        if zoom_level is None:
            zoom_level  = self.zoom_level
        if zoom_level is None:
            zoom_level =  10

        file_name_html  = r"d:/temp.html"  # need full path
        gmap       = gmplot.GoogleMapPlotter( lat, long, zoom_level )
        gmap.marker( lat, long, "cornflowerblue" )
        gmap.draw( file_name_html )   # a file name for the html
        webbrowser.open( file_name_html, new = 2 )        # auto open file above in new tab


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
    haversine as hs
    pip install haversine
    Latitude is written before longitude. Latitude is written with a number,
    followed by either “north” or “south” depending on whether it is located north or south of the equator.
    Longitude is written with a number, followed by either “east” or “west” depending on
    whether it is located east or west of the Prime Meridian.

    """
    # ----------------------------------------
    def __init__(self, name, from_lat, from_long, unit  ):
        """
        """
        self.MILE       = "mile"
        self.METER      = "meter"
        self.KM         = "kilometers"

        self.reset(  name, from_lat, from_long, unit  )

    # ----------------------------------------
    def reset( self, name, from_lat, from_long, unit ):
        """
        units    from Units

        Returns
            None but mutates self

        """
        self.from_lat  = from_lat
        self.from_long = from_long
        self.from_name = name

        unit          = self._normalise_unit( unit )
        self.unit     = unit

        self.distances = []  # named tuples ThreeParts   = collections.namedtuple( 'ThereParts', "index_1 index_2, index_3" )
        #self.distances = {}
        # # change to dict
        #self.Distance  = collections.namedtuple( "Distance", "a_comment lat long distance" )

    # ----------------------------------------
    def _normalise_unit( self,    unit  ):
        """
        unit a string representing the units

        returns
             normalized units
        """
        unit           = unit.lower()
        if unit.startswith( "me"):
            n_unit = self.METER

        elif unit.startswith( "mi"):
            n_unit = self.MILE

        elif unit.startswith( "k"):
            n_unit = self.KM
        else:
            pass  # need exception
        return n_unit

    # ----------------------------------------
    def _convert_distance_units( self,  a_distance, unit  ):
        """
        a_distance   ,, instance of distance
        units a string representing the units

        returns
            a float


        what units
        from geopy.units import radians
        @property
        def feet(self):
            return units.feet(kilometers=self.kilometers)

        @property
        def ft(self):
            return self.feet

        @property
        def kilometers(self):
            return self.__kilometers

        @property
        def km(self):
            return self.kilometers

        @property
        def m(self):
            return self.meters

        @property
        def meters(self):
            return units.meters(kilometers=self.kilometers)

        @property
        def mi(self):
            return self.miles

        @property
        def miles(self):
            return units.miles(kilometers=self.kilometers)

        @property
        def nautical(self):
            return units.nautical(kilometers=self.kilometers)

        @property
        def nm(self):
            return self.nautical

        """
        converted_distance   = None
        unit                 = self._normalise_unit( unit )

        if unit == self.METER:
            converted_distance  = float( a_distance.m )

        elif unit == self.MILE:
            converted_distance  = float( a_distance.mi )

        elif unit == self.KM:
            converted_distance  = float( a_distance.km )

        else:
            pass  # need exception
        return converted_distance

    # ----------------------------------------
    def add_to_long_lat( self,  name, lat, long,  ):
        """


        """
        # # -- using haversine
        # the_distance = hs.haversine( (self.from_lat, self.from_long ), ( lat, long ) )

        # -- using geopy
        distances      = geopy.distance.geodesic( ( self.from_lat, self.from_long ), ( lat, long ),   )

        the_distance   = self._convert_distance_units( distances, self.unit  )

        # old stuck in km
        # the_distance   = distances.km

        #rint( f"type distances {type( distances) }" )  # geopy.distance.geodesic
        #rint( f"distances {distances}" )

        #rint( f"type the_distance {type( the_distance) }" )   # float
        #rint( f"the_distance {the_distance}" )

        #rint( f"float the_distance {float( the_distance)}" )  # is ok but already a float

        ## when named tuple
        #a_distance   = self.Distance( name, long, lat, the_distance   )
        a_distance    = {  "name": name,
                           "long": long,
                           "distance": the_distance,
                           }
        #a_distance[ "name"]   = name

        self.distances.append( a_distance )

        #rint( a_distance )
        #rint( self.distances )

        return the_distance

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

       # _str = f"{a_str}{line_begin}   from location name       {self.lat}, {self.long}"
        a_str = f"{a_str}{line_begin}   unit                  {self.unit}"
        a_str = f"{a_str}{line_begin}   self.distances        {self.distances}"
        #a_str = f"{a_str}\n   units        {self.computername}"
        # a_str = f"{a_str}\n   our_os              {self.our_os}"

        #a_str = f"{a_str}\n   snip_file_fn            {self.snip_file_fn}"
        #a_str = f"{a_str}\n   snippets_fn             {self.snippets_fn}"
        # a_str = f"{a_str}{line_begin}   ex_editor                {self.ex_editor}"

        # a_str = f"{a_str}{line_begin}   --- logging  ---"
        # a_str = f"{a_str}{line_begin}   comm_logging_fn          {self.comm_logging_fn}"


        return a_str

# ----------------------------------------
def test_classPhotoPlus():

    print( "\n test_classPhotoPlus =====================")
    file_name        = r"D:\Russ\0000\python00\python3\_examples\wedge.jpg"

    # ---- PhotoPlus
    a_photo_plus    = PhotoPlus( file_name )

    # # ---- lat long
    # lat_long  = a_photo_plus.get_lat_long()
    #rint( lat_long )

    # # ---- adr
    # adr  = a_photo_plus.get_address(   )
    #rint( adr )

    # ---- file size
    file_size    = a_photo_plus.get_size()
    print( f"file_size {file_size}")

    # ---- exif string
    exif_string   = a_photo_plus.exif_string()
    print( exif_string )

    #exif_string


    # # ------
    # address  = a_photo_plus.get_address()
    #rint( address )

    # ex_helpers.print_double_bar_sep()

    # ex_helpers.end_example( ex_name )  # not part of example, marks end

# test_classPhotoPlus()



# ----------------------------------------
def test_static_map_class ():
    # ex_name  = "ex_static_map_class"   # end with >>    ex_helpers.end_example( ex_name )  # not part of example, marks end
    #rint( f"""{ex_helpers.begin_example( ex_name )}
    #        Python | Get a google map image of specified location using Google Static Maps API - GeeksforGeeks
    #                *>url  https://www.geeksforgeeks.org/python-get-google-map-image-specified-location-using-google-static-maps-api/

    #       """ )
    print( "\n test_static_map_class =====================")
    zoom_world      = 1
    zoom_landmass   = 5
    zoom_city       = 10
    zoom_street     = 15
    zoom_building   = 20

    url             = None
    zoom            = None        # zoom defines the zoom  level of the map
    center          = None
    size            = "400x400"   # may be limit at 640 ...
    size            = "600x600"   # may be limit at 640 ...
    #size            = None  # just do not pass
    marker          = None        # values "cornflowerblue" ??
    sensor          = None        # don't know
    api_key         = None        # sign up for one


    fn_out          = "ex_static_map.png"

    # ---- actual values -- but see dict setup where may be overwritten
    #api_key         = ex_helpers.get_data( "google_api_key_gmp" )
    api_key         = data.get_data( "google_api_key_gmp" )  # you will need to get you own key


    # url variable store url
    url             = "https://maps.googleapis.com/maps/api/staticmap?"

    # center defines the center of the map,
    # equidistant from all edges of the map.
    center          = "Dehradun"
    center          = "Williamsburg,Brooklyn,NY"
    center          = "77, 45"
    center          = "45, 77"
    zoom            = 10
    zoom            = zoom_street
    marker          = "cornflowerblue"
    marker          = "size:mid%7Ccolor:0x2e3a5c%7Clabel:1%7CAlbany%2C%20NY"

    # # # from google example
    # center          = "Albany%2C+NY"

    # zoom            = "9"

    # scale           = "2"
    # size            = "600x300"
    # maptype         = "roadmap"
    # file_format     = "png"      # format
    # #key
    # marker          = "size:mid%7Ccolor:0x2e3a5c%7Clabel:1%7CAlbany%2C%20NY"   #markers

    """
    https://maps.googleapis.com/maps/api/staticmap?
    center=Albany%2C+NY
    &zoom=9
    &scale=2
    &size=600x300
    &maptype=roadmap
    &format=png
    &key=AIzaSyAP6Vp7EvZFOf02PsnzQtR7oimSoTqtKJw
    &markers=size:mid%7Ccolor:0x2e3a5c%7Clabel:1%7CAlbany%2C%20NY
    """

    # ---- at farm with marker
    # center here because twice
    center  = "41.53993055555556, -71.00936388888888"   # farm
    a_staticmap_dict    = {    "url":       url,
                               "api_key":   api_key,
                               "size":      size,
                               #"zoom":      5,     # east coast
                               "zoom":      15,     # east coast
                               #"center":    "45, 77",
                               #"center":    "77, 45",   # off England
                               #"center":    "-77, 45",  # Antarctica
                               "center":    center,


                               # "marker":    "size:mid%7Ccolor:0x2e3a5c%7Clabel:1%7CAlbany%2C%20NY",
                               # next works
                               # "marker":    "size:mid%7Ccolor:0x2e3a5c%7Clabel:1%7C41.53993055555556, -71.00936388888888",
                               # "marker":    f"size:mid%7Ccolor:0x2e3a5c%7Clabel:1%7C{center}",  # this marker placed at center
                               "sensor":    sensor,
                        }

    #rint( a_staticmap_dict )
    # return

    # # google example
    # a_staticmap_dict    = {    "url":       url,
    #                            "api_key":   api_key,
    #                            "size":      "600x300",
    #                            "zoom":      "9",
    #                            "center":    "Albany%2C+NY",
    #                            "marker":    "size:mid%7Ccolor:0x2e3a5c%7Clabel:1%7CAlbany%2C%20NY",
    #                            "sensor":    sensor,
    #                     }



    # a_staticmap_dict    = {    "url":       url,
    #                            "api_key":   api_key,
    #                            "size":      size,
    #                            "zoom":      zoom,
    #                            "center":    "540 Horseneck Rd, Dartmouth, Ma, USA",
    #                            "marker":    marker,
    #                            "sensor":    sensor,
    #                     }

    a_static_map    = StaticMap( **a_staticmap_dict )
    a_static_map.make_center_marker()
    a_static_map.write_map_file( fn_out )

    # a_dict          = a_static_map.read_exif_2(  r"D:\PhotosRaw\2022\Phone\PXL_20220914_193543215.jpg"  )

    # # if a_dict: !!
    # lat      = a_dict[  'latitude' ]
    # long      = a_dict[ 'longitude' ]

    # a_static_map.open_web_map( long, lat, zoom_city  )


    # shell out to see
    ret   = os.system( fn_out )

    # ex_helpers.print_double_bar_sep()

    # ex_helpers.end_example( ex_name )

# test_static_map_class()


# ----------------------------------------
def test_DistanceFrom_class ():
    # ex_name  = "ex_static_map_class"   # end with >>    ex_helpers.end_example( ex_name )  # not part of example, marks end
    #rint( f"""{ex_helpers.begin_example( ex_name )}
    #        Python | Get a google map image of specified location using Google Static Maps API - GeeksforGeeks
    #                *>url  https://www.geeksforgeeks.org/python-get-google-map-image-specified-location-using-google-static-maps-api/

    #       """ )
    print( "\n test_DistanceFrom_class =====================")

    #a_df       = DistanceFrom( "base at:", 22, 33 , geopy.units.meters )
    a_df       = DistanceFrom( "base at:", 22, 33 , "km" )
    a_df       = DistanceFrom( "base at:", 22, 33 , "meter" )
    a_df       = DistanceFrom( "base at:", 22, 33 , "miles" )
    a_df.add_to_long_lat( "test 1",  22, 33 )
    a_df.add_to_long_lat( "test 2",  22, 33 )
    a_df.add_to_long_lat( "test 3",  23, 33 )

    print( a_df.get_str() )

    print( "nice to make a map with all plotted ")

#test_DistanceFrom_class()








# ----------------------------------------
def test_multipls_class ():
    # ex_name  = "ex_static_map_class"   # end with >>    ex_helpers.end_example( ex_name )  # not part of example, marks end
    #rint( f"""{ex_helpers.begin_example( ex_name )}
    #        Python | Get a google map image of specified location using Google Static Maps API - GeeksforGeeks
    #                *>url  https://www.geeksforgeeks.org/python-get-google-map-image-specified-location-using-google-static-maps-api/

    #       """ )
    """

    lets take a list of photos and get the distance in meters from the firs photo
    """
    print("=============== test_multiple_class =======================")
    photo_list   = [
        r"D:\PhotosRaw\2022\Phone\sept\PXL_20220910_174726196.jpg",
        r"D:\PhotosRaw\2022\Phone\sept\PXL_20220910_174640945.MP.jpg",
        r"D:\PhotosRaw\2022\Phone\sept\PXL_20220910_174406430.jpg",
        r"D:\PhotosRaw\2022\Phone\sept\PXL_20220910_174029046.jpg",
        r"D:\PhotosRaw\2022\Phone\sept\PXL_20220910_174023607.jpg",
        r"D:\PhotosRaw\2022\Phone\sept\PXL_20220910_174019528.jpg",
        r"D:\PhotosRaw\2022\Phone\sept\PXL_20220910_174009498.jpg",
        #r"D:\PhotosRaw\2022\Phone\sept\PXL_20220910_151637932.mp4",
        r"D:\PhotosRaw\2022\Phone\sept\PXL_20220910_150846541.jpg",
        r"D:\PhotosRaw\2022\Phone\sept\PXL_20220910_145710158.jpg",
        r"D:\PhotosRaw\2022\Phone\sept\PXL_20220910_144750549.jpg",
        r"D:\PhotosRaw\2022\Phone\sept\PXL_20220910_144137079.MP.jpg",
        r"D:\PhotosRaw\2022\Phone\sept\PXL_20220910_142915439.MP.jpg",
        r"D:\PhotosRaw\2022\Phone\sept\PXL_20220910_142657446.jpg",
        r"D:\PhotosRaw\2022\Phone\sept\PXL_20220909_232510944.jpg",
        r"D:\PhotosRaw\2022\Phone\sept\PXL_20220909_232452220.jpg",
        r"D:\PhotosRaw\2022\Phone\sept\PXL_20220909_232449638.jpg",
        r"D:\PhotosRaw\2022\Phone\sept\PXL_20220909_232321042.MP.jpg",
        r"D:\PhotosRaw\2022\Phone\sept\PXL_20220909_232323587.jpg",
        r"D:\PhotosRaw\2022\Phone\sept\PXL_20220909_232306170.jpg",
        r"D:\PhotosRaw\2022\Phone\sept\PXL_20220909_232301832.jpg",
        r"D:\PhotosRaw\2022\Phone\sept\PXL_20220831_202342440.jpg",
        r"D:\PhotosRaw\2022\Phone\sept\PXL_20220831_202337117.jpg",
        r"D:\PhotosRaw\2022\Phone\sept\PXL_20220817_155336214.jpg",
        r"D:\PhotosRaw\2022\Phone\sept\PXL_20220817_155335384.jpg",
        r"D:\PhotosRaw\2022\Phone\sept\PXL_20220731_203859679.jpg",

        ]

    a_photo       = photo_list[0]
    a_photo_plus  = PhotoPlus( a_photo )
    lat_long      = a_photo_plus.get_lat_long()

    distance_from   = DistanceFrom( a_photo, *lat_long, geopy.units.meters )
    print( distance_from.get_str( ) )

    for a_photo in photo_list:
        a_photo_plus  = PhotoPlus( a_photo )
        lat_long      = a_photo_plus.get_lat_long()
        distance_from.add_to_long_lat( a_photo, *lat_long )

    print( distance_from.get_str( ) )

    print( "========= all done ==============")

    #= DistanceFrom( 22, 33 , geopy.units.m )
    # a_df.add_to_long_lat( "test",  22, 33 )
    # a_df.add_to_long_lat( "test",  22, 33 )


# test_multipls_class()   put at bottom


# ==============================================
if __name__ == '__main__':
    """
    run the app here for convenience of launching

    """
#    x
    print( "" )
    print( " ==========   ==============" )

    #test_DistanceFrom_class()
    #test_multipls_class ()
    #test_classPhotoPlus()
    test_static_map_class()
