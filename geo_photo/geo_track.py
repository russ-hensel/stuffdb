# -*- coding: utf-8 -*-
#! /usr/bin/python3
#!python3

"""
this is the controller module for the geotracker app

/media/russ/j_sg_bigcase/sync_py_3

"""
# ------------------------------------------
if __name__ == "__main__":
    import main
    main.main()
# ------------------------------------------

# ---- import

import os
#import logging
import importlib
from   subprocess import Popen   #, PIPE  #
import time
import datetime
import gpxpy
import gpxpy.gpx
import pathlib
from   functools import partial
from   pathlib   import Path
import folium
import pytz
# from folium.plugins import HeatMap
import webbrowser
import simplekml



# #----- local imports
# import app_abc
# import parameters
# import clipper
# import gui
# import photo_ext
import app_exceptions
# import file_filters
# import dir_tree_explore
# import photo_file_utils
from   app_global import AppGlobal

# ---- end imports

# FileInfo     = collections.namedtuple( "FileInfo" , "lat long elav date", defaults=( None, None ) )
#data_point   =  FileInfo( lat  = lat, long = long,   )
#an_example   = ThreeParts( index_1  = "aaa", index_2 = "bbb", index_3 = "ccc" )
"""
from collections import namedtuple
>>> fields = ('val', 'left', 'right')
>>> Node = namedtuple('Node', fields, defaults=(None,) * len(fields))
>>> Node()
Node(val=None, left=None, right=None)
"""

# ============================================
class WasApp(   ):
    """
    was ... now stripping doen
    this class is the "main" or controller for the whole app
    to run see end of this file
    it is the controller of an mvc app

    !! need super call here
    """
    def __init__( self  ):
        """
        usual init for main app
        splash not working as desired, disabled
        splash screen which is of not help unless we sleep the init
        """
        # self.app_name          = "GeoTrack"
        # self.version           = "Ver 10: 2024 02 25.01"
        # self.app_version       = self.version
        #     # get rid of dupe at some point... app_version in gui_ext
        # self.app_url           = "www.where"
        # # clean out dead
        # AppGlobal.controller   = self
        # self.gui               = None

        # self.q_to_splash       = q_to_splash
        # self.polling_delta     = None     # actually set from parameters may want to move location
        # self.starting_dir      = ""       # defined later but maybe move to ... -- !! delete in parameters
        # # self.polling_pause     = False  # to make polling pause, set from main thread  move to gui
        # self.restart( )
        # self.file_name          = None
        # self.gpx                = None   # a gpx object, lat built ... good idea ?
        #self.url                = "./map_url.html"
        self.last_photo_fn      = None     # name of the last photo file that has be read ....
        self.last_gpx_fn        = None
        self.max_min_lat_long   = None     # !! not a great way of managing




    # ----------------------------------
    def _finish_gui(self ):
        """
        after building a gui do this
        looks like stuff could be combined
        """
        msg       = ( "Error messages may be in log file, check it if problems"
                       " -- check parameters.py for logging level "
                       )
        #rint( msg )
        AppGlobal.print_debug( msg )
        self.logger.log( AppGlobal.fll, msg )
        self.polling_delta  = self.parameters.poll_delta_t

        self.starting_dir   = os.getcwd()

        # if   self.parameters.gui_module  == "gui_with_tabs":

    # ----------------------------------
    def _polling_task( self,  ):
        """
        poll for clipboard change and process them
        this is only for the auto commands, for
        the button push ones see:  controller.button_switcher
        protect with a try so polling does not crash the entire application -- "no matter what"
        """
        return
        # msg       = "+."
        #rint( msg, end = ""  )   # showing polling is alive


    # ------------------------------------------
    def test2( self, ):
        """
        some test, for when I need to experiment
        """
        self._get_output_options(  )

    # ---- Input ------------------------------------------
    def input_and_go( self,  ):
        """
        get input first from ddl and then dispatch the right
        stuff, see readme or whatever

        """
        option  = self.gui.get_input_option()


        gui          = AppGlobal.gui
        start_time   = time.time()
        AppGlobal.gui.clear_message_area()

        google_out   = gui.get_output_google()
        msg          = f"get google output {google_out} "
        print( msg )

        folium_out   = gui.get_output_folium()
        msg          = f"get folium_out {folium_out} "
        print( msg )

        try:
            # ---- "DirScan"
            option  = self.gui.get_input_option()
            if option ==   "DirScan" :
                self._input_dir_scan()

            # ---- "GPXfile"
            elif option ==   "GPXfile" :
                # old
                #self.gui_make_map_from_gpx_file()
                # new wilt be   _input_gpx_file
                self._input_gpx_file()

            # ---- "FileList"
            elif option ==   "FileList" :
                self._input_file_list()
                # self.gui_make_map_from_filelist()

            # ---- "PhotoPoints"
            elif option == "PhotoPoints":
                self._input_photo_points()

            else:
                print( f"input_and_go unrecognized option {option }")

        except app_exceptions.ReturnToGui  as an_except:
            msg  = f"Operation failed, {an_except.why}"
            AppGlobal.gui.write_gui( msg )

        except app_exceptions.ApplicationError  as an_except:
            msg  = f"Operation failed, {an_except.why}"
            AppGlobal.gui.write_gui( msg )

        end_time    = time.time()
        run_time    = round( end_time - start_time, 2 )
        msg         = f"End of Operation ... run time {run_time} sec"
        gui.write_gui( msg )

   # ---- For each input type ------------------------
    def _input_dir_scan( self,  ):
        """
        process when the input is a dir scan

        """
        #gui             = AppGlobal.gui
        google_out      = self.gui.get_output_google()
        msg             = f"get google output {google_out} "
        print( msg )

        folium_out      = self.gui.get_output_folium()
        msg             = f"get folium_out {folium_out} "
        print( msg )

        file_name       = self.gui.get_browse()
        msg     = f"Make map from a directory using file >{file_name}<"
        self.gui.write_gui( msg )
        file_list        = self._dir_to_fl( file_name )
        # what do do with file_list, write to file probably
        photo_points     = self._fl_to_pp( file_list )
        print( f"_input_dir_scan len(photo_points) {len(photo_points)} ")

        photo_points    = self._pp_to_filtered_pp( photo_points )

        photo_points    = self._pp_to_sorted_pp( photo_points )

        gpx             = self._pp_to_gpx( photo_points )

        if folium_out:
            xxx         = self._gpx_to_map( gpx )

        if google_out:
            self._pp_to_kmz( photo_points )

        msg   = "done DirScan"
        self.gui.write_gui( msg )
        print( msg )

   # --------------------------
    def _input_file_list( self,  ):
        """
        process when the input is a file list

        """
        gui          = AppGlobal.gui
        google_out   = gui.get_output_google()
        msg          = f"get google output {google_out} "
        print( msg )

        folium_out   = gui.get_output_folium()
        msg          = f"get folium_out {folium_out} "
        print( msg )

        file_name       = gui.get_browse()
        a_path          = Path( file_name )
        if  a_path.suffix != ".txt":
            msg   = ( f"Your file for the filelist, {a_path}, is not a .txt file, "
                        "which is required. Operation terminated." )
            self.gui.write_gui( msg )
            raise app_exceptions.ReturnToGui( msg )

        file_list       = photo_file_utils.read_flf_to_fl( file_name )

        msg     = f"Read file list: file list len = {len(file_list)}"
        AppGlobal.gui.write_gui( msg )

        photo_points    = self._fl_to_pp( file_list )
        print( f"_input_file_list len(photo_points) {len(photo_points)} ")

        photo_points    = self._pp_to_filtered_pp( photo_points )

        photo_points    = self._pp_to_sorted_pp( photo_points )

        gpx             = self._pp_to_gpx( photo_points )

        if folium_out:
            xxx             = self._gpx_to_map( gpx )

        if google_out:
            # msg   = "Google earth not yet supported for a FileList -- but will give a try"
            # gui.write_gui( msg )
            # gpx          = self._make_gpx_from_data( gpx_data )

            self._pp_to_kmz( photo_points )
            # gpx_data     = self._sort_filter_gpx_data( gpx_data )

        msg    = "done FileList"
        gui.write_gui( msg )
        print( msg )

    # ------------------------------------------
    def _input_gpx_file( self,  ):
        """
        in this version we are going to make photo_plus points with no file name
        so sorts.... filter can work this replaces old gui_make_map_from_gpx_file()

        """
        gui          = AppGlobal.gui
        google_out   = gui.get_output_google()
        msg          = f"get google output {google_out} "
        print( msg )

        folium_out   = gui.get_output_folium()
        msg          = f"get folium_out {folium_out} "
        print( msg )


        file_name    = self.gui.get_browse()
        msg     = f"Make map from *.GPX file using file {file_name}"
        AppGlobal.gui.write_gui( msg )

        try:
            # gpx          = self._gpx_from_gpxfile( file_name )
            # self._gpx_to_map( gpx )
            photo_points    = self.gpx_to_pp( file_name )
            print( f"_input_gpx_file len(photo_points) {len(photo_points)} ")

            photo_points    = self._pp_to_filtered_pp( photo_points )
            photo_points    = self._pp_to_sorted_pp( photo_points )

            gpx             = self._pp_to_gpx( photo_points )

            if folium_out:
                xxx             = self._gpx_to_map( gpx )

            if google_out:
                # msg   = "Google earth not yet supported for a FileList -- but will give a try"
                # gui.write_gui( msg )
                # gpx          = self._make_gpx_from_data( gpx_data )

                self._pp_to_kmz( photo_points )
                # gpx_data     = self._sort_filter_gpx_data( gpx_data )

            msg    = "done FileList"
            gui.write_gui( msg )
            print( msg )

        except app_exceptions.ReturnToGui  as an_except:
            msg  = f"File Load failed, {an_except.why}"
            print( msg )
            AppGlobal.gui.write_gui( msg )

        except app_exceptions.ApplicationError  as an_except:
            msg  = f"File Load failed, {an_except.why}"
            print( msg )
            AppGlobal.gui.write_gui( msg )

        # check next in caller
        # end_time    = time.time()
        # run_time    = round( end_time - start_time, 2 )
        # msg         = f"End of Make Map from GPX file... run time {run_time} sec"
        # print( msg )
        # AppGlobal.gui.write_gui( msg )

        # 1/0    # until finished




    # ------------------------------------------
    def _input_photo_points( self,  ):
        """
        get input first from ddl and then dispatch the right
        stuff, see readme or whatever

        """
        gui        = AppGlobal.gui
        file_name  = gui.get_browse()

        photo_points  = photo_file_utils.read_photo_points( file_name, )
        print( f"PhotoPoints len(photo_points) {len(photo_points)} ")

        photo_points    = self._pp_to_filtered_pp( photo_points )

        photo_points    = self._pp_to_sorted_pp( photo_points )

        gpx             = self._pp_to_gpx( photo_points )
        self._gpx_to_map( gpx )

    # ---- New Gui Transforms  --------------------------------------
    def _dir_to_fl( self, file_in_dir_fn ):
        """
        pretty much _dir_to_filelist
        consider a move of the code


        Purpose:
            given a file name, scan the directory it is in
            and make a file list in this object for it

        arguments
            filename -- for dir to search
        returns:
            mutate      self.file_list
        """
        # validation could be a function
        filename  = file_in_dir_fn   #!! fix this

        filename  = filename.strip()
        if filename == "":
            msg   =  f"File, {filename}, is empty; operation terminated"
            self.gui.write_gui( msg )
            raise app_exceptions.ReturnToGui( msg )

        a_file_path   = pathlib.Path( filename )
        if not a_file_path.exists():
            msg   = (f"File, {filename}, does not exist; operation terminated")
            self.gui.write_gui( msg )
            raise app_exceptions.ReturnToGui( msg )

        if a_file_path.is_file():
            a_file_path    = a_file_path.parent

        #--------- directory
        recur_limit         = self.gui.get_recur_limit( )
        dir_filter_obj      = file_filters.DFAll()
        print( dir_filter_obj .demo_filter )

        #-------- file
        file_filter_obj     = file_filters.FFExtList( ["jpg", "pnp", ],
                                                     include_true = True,
                                                     use_lower    = True )

        dir_tree_explorer                   = dir_tree_explore.DirTreeExplorer()
        dir_tree_explorer.file_filter       = file_filter_obj
        dir_tree_explorer.directory_filter  = dir_filter_obj
        dir_tree_explorer.max_dir_depth     = recur_limit
        dir_tree_explorer.gui_write         = self.gui.write_gui

        dir_tree_explorer.explore_dir( a_file_path )
        file_list    = dir_tree_explorer.file_list

        self.write_todffl( file_list )

        return file_list

    # ------------------------------------------
    def _fl_to_flf( self, file_name ):
        """
        from a file- list    --> make a flist file = flf

        Purpose:
            get a list of files from a file
            consider sort... or sort after have data??
            consider that files in file list exist??
        Return
             file_list   a list of files
        Except:
            app_exceptions.ReturnToGui

        """
        file_list   = []

        # check  none
        if file_name is None:
            msg   = "File name is None, so cannot be processed to make a gpx"
            self.gui.write_gui( msg )
            raise app_exceptions.ReturnToGui( msg )

        # check extension
        file_path    = pathlib.Path( file_name )

        if file_path.suffix != ".txt":  # consider lower
            msg   = f"File name {file_name} is a not txt file, so cannot be processed"
            self.gui.write_gui( msg )
            raise app_exceptions.ReturnToGui( msg )

        # check exist
        if not file_path.exists():
            msg   = f"File name {file_name} is not a file that exists, so cannot be processed."
            self.gui.write_gui( msg )
            raise app_exceptions.ReturnToGui( msg )

        dffl_fn         = AppGlobal.parameters.default_filelist_fn
        add_to_dffl     = AppGlobal.gui.get_add_to_dffl()
        dffl            = None    # use this as file and flag
        if add_to_dffl:
            msg         = f"Adding to default file filelist {dffl_fn}"
            print( msg )
            self.gui.write_gui( msg )
            dffl        = open( dffl_fn,"a")

        line_no = 0   # enumerate instead
        with open( file_path, 'r' ) as file:
            for i_line in file:
                line_no  += 1
                if dffl:
                    dffl.write( i_line )
                i_line    = i_line.rstrip('\n')
                #rint( f"reading line no {line_no} =  {i_line }")
                file_list.append( i_line )
        if dffl:
            dffl.close()

        msg    = f"Made file list from {file_name} number of photos = {line_no}"
        print( msg )
        self.gui.write_gui( msg )

        return file_list
    # ------------------------------------------
    def  gpx_to_pp( self, file_name ):
        """
        from a gph file   --> list of photo points
        to do ..... write out photo points
        Purpose:
            make a gpx_data ( list of photo plus item ) from the gpx file
            for now we are just using the tracks in the file and their
            segments, see code
        Arguments
            file_name   name of a gpx file

        Return
            photo_points     .... points to build a gpx file
        """
        # next might be a function ??
        # chdek none
        if file_name is None:
            msg   = "File name is None, so cannot be processed to make a gpx"
            self.gui.write_gui( msg )
            raise app_exceptions.ReturnToGui( msg )

        # check extension
        file_path    = pathlib.Path( file_name )

        if file_path.suffix != ".gpx":  # consider lower
            msg   = f"File name {file_name} is a not gpx file, so cannot be processed to make a gpx"
            self.gui.write_gui( msg )
            raise app_exceptions.ReturnToGui( msg )

        # check exist
        if not file_path.exists():
            msg   = ( f"File name {file_name} is not a file that exists, "
                     "so cannot be processed to make a gpx" )
            self.gui.write_gui( msg )
            raise app_exceptions.ReturnToGui( msg )

        with open( file_path, 'r' ) as readFile:
            gpx = gpxpy.parse( readFile )
            # now we need to use gpxpy to get list of points which
            # may be what is in the gpx object or not
            photo_points  = []

            # extracts the latitude and longitude coordinates of each point in each track segment, appending them to separate lists called lats and longs
            for track in gpx.tracks: # iterable that contains all of the tracks in the GPX file  self.tracks: List[GPXTrack] = []
                for segment in track.segments: # each track is composed of one or more track segments, which are represented by the track.segments iterable
                    for point in segment.points: # each track segment consists of a series of GPS points that make up the track
                                                 # self.segments: List[GPXTrackSegment] = []
                                                 # points: Optional[List[GPXTrackPoint]]
                                                  # for points: __slots__ = ('latitude', 'longitude', 'elevation', 'time', 'course',
                                                              # 'speed', 'magnetic_variation', 'geoid_height', 'name',
                                                              # 'comment', 'description', 'source', 'link', 'link_text',
                                                              # 'symbol', 'type', 'type_of_gpx_fix', 'satellites',
                                                              # 'horizontal_dilution', 'vertical_dilution',
                                                              # 'position_dilution', 'age_of_dgps_data', 'dgps_id',
                                                              # 'link_type', 'extensions')
                        a_pp     = photo_ext.PhotoPlus( None )
                        # !! check for None in next  -- or make sure gpx is clean
                        a_pp.long       = point.longitude
                        a_pp.lat        = point.latitude
                        a_pp.datetime   = point.time           # seems to be a datetime
                        a_pp.latitude   = True

                        photo_points.append( a_pp )

        msg    = f"Made photo_points from {file_name} len = len( photo_points ) "
        print( msg )
        self.gui.write_gui( msg )
        AppGlobal.logger.debug( msg )

        return photo_points


    # ------------------------------------------
    def _fl_to_pp( self, file_list ):  # return photo_points
        """
        from a file- list    --> list of photo points
        to do ..... write out photo points
        Purpose:
            make a gpx_data ( list of photo plus item ) from the file
            a file list
            * allow comment after file name -- no spaces in file name
            * may add line to default file list -- option
        Arguments
            file_list    list of file names, or perhaps pathlib.paths
        Return
            photo_points     .... points to build a gpx file
        """
        a_timezone      = AppGlobal.gui.get_timezone()
        #rint( self.file_list )
        photo_points    = []  #  photo plus instances in list
        # next is not fast may want to see what is slowing it down
        for ix, i_file in enumerate( file_list ):
            # i_file is a line in the file list file and should be a file name or a comment

            if i_file.startswith( "#"):
                print( i_file )
                continue

            if not os.path.exists( i_file ):
                msg   = f"File Name {i_file} references a file that seems not to exist"
                self.gui.write_gui( msg )
                AppGlobal.logger.log( 10 ,  msg )  # how do I get the right levels ?? document
                print( msg )
                continue

            i_file       = i_file.split(  maxsplit = 1  )[0] #allow content after filename ( control with gui or parameters )
            photo_plus   = photo_ext.PhotoPlus( i_file, a_timezone )
            if photo_plus.has_lat_long:
                photo_points.append( photo_plus )
            #msg   = f" lat = {data_point.lat}   long =  {data_point.long}"
            #rint( msg )
            #AppGlobal.gui.write_gui( msg )
        # msg    = "done"
        # print( msg )
        #AppGlobal.gui.write_gui( msg )

        photo_points_fn     = AppGlobal.parameters.default_photo_points_fn
        msg    = f"Write out photo points to file {photo_points_fn}"
        print( msg )
        AppGlobal.logger.log( 10 ,  msg )
        AppGlobal.gui.write_gui( msg )

        photo_file_utils.write_photo_points(
            file_name      = photo_points_fn,
            photo_points   = photo_points,
            comments       = None )

        return photo_points

    # --------------------------------------
    def _pp_to_kmz( self, photo_points ):
        """
        photo points are turned into a kmz file, read the code
        return  None ?? open google earth
        """
        file_name     = AppGlobal.parameters.default_kmz_fn
        # Create a KML object
        kml = simplekml.Kml()

        coordinates = []   # may not need this intermediary
        for i_photo_plus in photo_points:

            if i_photo_plus.lat is None or i_photo_plus.long is None:
                continue
            # append a tuple
            coordinates.append( (   i_photo_plus.lat,        i_photo_plus.long, ) )

        # Create a KML LineString with tessellate set to True
        linestring = kml.newlinestring( name = "My Path" )
        linestring.tessellate = 1  # Set tessellate to 1 to create a tessellated line

        # Add coordinates to the LineString
        for lat, lon in coordinates:
            linestring.coords.addcoordinates([(lon, lat, 0)])
                # Note the order: (longitude, latitude, altitude)

        # Set altitude mode to clampToGround to ensure the path follows the Earth's surface
        linestring.altitudemode = simplekml.AltitudeMode.clamptoground

        # Save the KML file to disk
        kml.save( file_name
 )
        msg    = f"in _pp_to_kmz KML file {file_name} has been created."
        print( msg )

        # might want to make file_name absolute first !!
        # os.popen( f"./{file_name}" )
        # os.popen(  file_name  )   # ok windows, not linux
        proc = Popen( [ "/usr/bin/google-earth-pro",
          "/mnt/WIN_D/Russ/0000/python00/python3/_projects/geo_track/default_kmz.kmz" ] )
          # Opens google earth in linux and perhaps windows

    # --------------------------------------
    def _pp_to_gpx( self, photo_points ):
        """
        photo points are turned into a gpx object which is , read the code
        return gpx object
        """
        msg     = f"_pp_gpx make gpx object from photo_points  list {len( photo_points )} "
        AppGlobal.gui.write_gui( msg )
        # Create a GPX object
        gpx = gpxpy.gpx.GPX()

        # Create a track
        track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append( track )

        track_point_list        = []
        max_min_lat_long        = MaxMinLatLong()

        for photo_point in photo_points:
            #rint( f"adding phot_point {photo_point}")
            if photo_point.lat is None or photo_point.long is None:
                continue    # !! apply as a filter earlier

            max_min_lat_long.add_lat_long( photo_point.lat, photo_point.long)
            # Create some track points with made-up data
            a_track_point           = gpxpy.gpx.GPXTrackPoint(
                                         latitude  = photo_point.lat,
                                         longitude = photo_point.long,
                                             )
            #  !! change to use data in photo_point
            a_track_point.time      = datetime.datetime( 2023, 10, 26, 10, 0, 0 )   # !! fix me have data
            a_track_point.elevation = 100
            # a_track_point.speed     = 5  # meters per second
            track_point_list.append( a_track_point )

        # Add track points to the track -- out dent here
        track.segments.append( gpxpy.gpx.GPXTrackSegment( track_point_list ))
        self.max_min_lat_long = max_min_lat_long   # not good !! forgot why
        # Serialize the GPX data to a string..... for what now out!!
        #gpx_data = gpx.to_xml()
        #rint(gpx_data)

        msg     = f"_pp_gpx done track_point_list len = {len(track_point_list)}" # {gpx_data}
        AppGlobal.gui.write_gui( msg )
        return  gpx

    # ------------------------------------------
    def _gpx_to_map( self, gpx ):
        """
        Purpose:
            use a gpx object to make and open a html map
        arguments
           implied:  self.gpx
        returns:
           a new file  url       = 'map.html'
        """
        startTime = time.time()  # run time start

        max_min_lat_long   = MaxMinLatLong()

        msg   = f"Starting _gpx_to_map... {'unknown'} points"
        print( msg )
        AppGlobal.logger.debug( msg )

        # variables are later used to calculate the center coordinates
        #    of all the GPX files so the map can be centered at that location
        latCenter = 0
        lngCenter = 0

        # count how many trips we are adding to the map; files = trips
        print( "Adding coords to the map..." )

        # start counter of points added to the map
        countCoords = 0
        # ---- calculate center of the map --- #
        # loop through the GPX files
        if True:

            # extract the latitude and longitude data from the GPX file
            lats, lngs = [], []
            msg   = f"gpx.tracks len  = {len(gpx.tracks)}"
            AppGlobal.logger.debug( msg )
            # extracts the latitude and longitude coordinates of each point in each
            # track segment, appending them to separate lists called lats and longs
            for track in gpx.tracks: # iterable that contains all of the tracks in the GPX file
                msg   = f"len(track.segments)  = {len(track.segments)}"
                AppGlobal.logger.debug( msg )
                for segment in track.segments: # each track is composed of one or more track segments,
                    # which are represented by the track.segments iterable
                    msg   = f"segment.points  = {len(segment.points)}"
                    AppGlobal.logger.debug( msg )
                    for point in segment.points:
                        # each track segment consists of a series of
                        # GPS points that make up the track

                        # !! check for None in next  -- or make sure gpx is clean
                        lats.append( point.latitude )
                        lngs.append( point.longitude )
                        max_min_lat_long.add_lat_long( point.latitude, point.longitude )

                        countCoords += 1
                        #msg    = f"countCoords = {countCoords}"
                        #rint(  msg  )
                        #AppGlobal.logger.debug( msg )

            # calculates the sum of all latitudes and longitudes, and then
            # divides them by the total number of points in the GPX files to get the average
            # latitude and longitude of all the points
            # !! russ look into this seems just for multiple tracks
            if ( len(lats) != 0  ) and ( len(lngs) != 0 ):

                latCenter += sum(lats)/len(lats)
                lngCenter += sum(lngs)/len(lngs)

        default_zoom   =  max_min_lat_long.get_zoom()
        foliumMap      = folium.Map(location=[latCenter, lngCenter], zoom_start = default_zoom )

        # ------- add a polyline to map ------ #
        lats, lngs = [], []

        # extracts the latitude and longitude coordinates of each point
        # in each track segment, appending them to separate lists called lats and longs

        msg    =  f"add a polyline to map len( gpx.tracks )  {len( gpx.tracks )}"
        print( msg )


        msg    =  ( f"_gpx_to_map lats {lats} "
                    f"lngs {lngs} "  )
        print( msg )

        AppGlobal.logger.debug( msg )

        for track in gpx.tracks: # iterable that contains all of the tracks in the GPX file
            for segment in track.segments: # each track is composed of one or more track segments, which are represented by the track.segments iterable
                for point in segment.points:
                    # each track segment consists of a series of
                    # GPS points that make up the track
                    # NOTE: map
                    lats.append( point.latitude  ) # extract and add to the list
                    lngs.append( point.longitude ) # extract and add to the list

                    # NOTE: heatmap data.append([point.latitude, point.longitude])

        # NOTE: map# add a PolyLine to the map using the latitude and longitude data of the GPX file
        folium.PolyLine(locations = list(zip(lats, lngs))).add_to(foliumMap)

        msg =  f"Added {countCoords} coords to the map."
        print( msg )

        #rint("Saving map...") # status
        url       = 'map.html'

        url       = AppGlobal.parameters.default_html_fn
        foliumMap.save( url)
        print("Map saved.")

        webbrowser.open( url, new = 0, autoraise = True )

        # ------------- run time ------------- #
        endTime      = time.time()  # run time end
        totalRunTime = round( endTime-startTime, 2 ) # round to 0.xx
        #rint(f"gpx_to_map run time: {totalRunTime} seconds. That's {round(totalRunTime/60,2)} minutes.") # status

    # ------------------------------------------
    def _get_output_options( self,  ):
        """
        may not be used, for test??
        """
        gui          = self.gui

        google_out   = gui.get_output_google()
        msg          = f"get google output {google_out} "
        print( msg )

        folium_out   = gui.get_output_folium()
        msg          = f"get folium_out {folium_out} "
        print( msg )


    # ---- New Filters ------------------------------------------
    def _pp_to_filtered_pp( self, photo_points ):
        """
        filter the photo points according to the gui
        raise except if none left

        """
        gui   = self.gui
        if gui.get_use_dates(    ):
            a_filter_function  = self.get_date_filter_function ()
            photo_points       = self._pp_filter_on_fun( photo_points ,
                                                   a_filter_function )

            if len( photo_points ) == 0:
                msg  = "After filtering on dates no points left to map"
                gui.write_gui( msg )

                raise app_exceptions.ReturnToGui( msg )

            msg    = f"Filtered photo_points on dates: len = {len( photo_points)}"
            print( msg )
            self.gui.write_gui( msg )
            AppGlobal.logger.debug( msg )

        # ---- long lat
        need_filter, filter_function    = self._get_long_lat_filter_function()
        if need_filter:
            photo_points    =  [ a_point for a_point in photo_points if filter_function(a_point ) ]

            if len( photo_points ) == 0:
                msg  = "After filtering on long lat no points left to map"
                gui.write_gui( msg )

                raise app_exceptions.ReturnToGui( msg )

            msg    = f"Filtered photo_points on long lat: len = {len( photo_points)}"
            print( msg )
            self.gui.write_gui( msg )
            AppGlobal.logger.debug( msg )

        return photo_points

    # ---------------------------
    def get_date_filter_function( self,  ):
        """
        """
        timezone     = self.gui.get_timezone()
        timezone     = pytz.timezone( timezone  )
        start_date   = self.gui.get_start_date()
        end_date     = self.gui.get_end_date()
        msg          = "get_date_filter_function  need to error check start and end date here "
        print( msg )
        # may need to make the next a functinns !!
        start_datetime    = datetime.datetime.combine( start_date, datetime.datetime.max.time() )
        start_datetime    = timezone.localize( start_datetime )

        end_datetime      = datetime.datetime.combine( end_date,   datetime.datetime.max.time() )
        end_datetime      = timezone.localize( end_datetime )


        msg               = f"filter on dates  {start_datetime}     to  {end_datetime} "
        print( msg )
        AppGlobal.gui.write_gui( msg )

        def a_function(  a_photo_plus ):
            #rint( "a_function")
            ok     =  ( ( a_photo_plus.datetime >= start_datetime ) and
                        ( a_photo_plus.datetime <= end_datetime   ) )
            return ok

        return a_function

    # -----------------------------------------
    def _get_long_lat_filter_function( self,  ):
        """
        what it says read, still in test only max lat
        need_filter, filter_function    = self._get_long_lat_filter_function()
        """
        gui          = AppGlobal.gui
        need_filter  = False

        # ---- long
        min_long      = gui.get_min_long()
        if min_long:
            need_filter  = True
            def min_long_function(  a_photo_plus ):
                #rint( "a_function")
                ok     =  ( a_photo_plus.long >= min_long )
                return ok
        else:    #rint( "a_function")
            def min_long_function(  a_photo_plus ):
                return True

        max_long      = gui.get_max_long()
        if max_long:
            need_filter  = True
            def max_long_function(  a_photo_plus ):
                ok     =  ( a_photo_plus.long <= max_long )
                return ok
        else:    #rint( "a_function")
            def max_long_function(  a_photo_plus ):
                return True

        msg               = f"filter on min_long {min_long} max_long  {max_long}    "
        print( msg )
        gui.write_gui( msg )

        # ---- lat
        min_lat      = gui.get_min_lat()
        if min_lat:
            need_filter  = True
            def min_lat_function(  a_photo_plus ):
                ok     =  ( a_photo_plus.lat >= min_lat )
                return ok
        else:
            def min_lat_function(  a_photo_plus ):
                return True

        max_lat      = gui.get_max_lat()
        if max_lat:
            need_filter  = True
            def max_lat_function(  a_photo_plus ):
                #rint( "a_function")
                ok     =  ( a_photo_plus.lat <= max_lat )
                return ok
        else:    #rint( "a_function")
            def max_lat_function(  a_photo_plus ):
                return True

        msg               = f"filter on min_lat {min_lat} max_lat  {max_lat}    "
        print( msg )
        gui.write_gui( msg )

        def long_lat_filter_function( a_photo_plus ):
            ok       = ( min_lat_function( a_photo_plus )  and max_lat_function( a_photo_plus ) and
                         min_long_function( a_photo_plus ) and max_long_function( a_photo_plus ) )
            return ok

        # def a_function(  a_photo_plus ):
        #    #rint( "a_function")
        #    ok     =  ( a_photo_plus.datetime >= start_datetime ) and ( a_photo_plus.datetime <= end_datetime )
        #    return ok

        return need_filter,  long_lat_filter_function

    # -----------------------------------------
    def _pp_filter_on_fun( self, photo_points, filter_fun   ):
        """
        for filtering gpx data --
             use with partial may need to make thru a partial to include gui data
        arguments
            photo_points     list of photo plus or photo_points
            filter_fun   function that filters return true or false
             !! might generalize some more
        Return
            new list
            writes to gui

            photo_points      = _pp_filter_on_fun( photo_points , a_filter_function )

        """
        msg    = f"Filter on dates now starting with {len( photo_points )} points"
        AppGlobal.gui.write_gui( msg )

        new_photo_points    = [ a_pp for a_pp in photo_points if filter_fun( a_pp ) ]

        msg    = f"Filter on dates now {len( new_photo_points )} points"
        AppGlobal.gui.write_gui( msg )

        return new_photo_points

    # ---- Sort --------------------------------------
    def _pp_to_sorted_pp( self, photo_points ):
        """
        sort as requested in gui, this mutates
        but could create new so use return

        """
        sort_fun    = self._get_gpx_sort_fun(   )
        if sort_fun:
            photo_points.sort(  key = sort_fun )   # sort in place


        msg    = f"Sorted photo_points now len = {len( photo_points)}"
        print( msg )
        self.gui.write_gui( msg )
        AppGlobal.logger.debug( msg )

        return photo_points


    # ------------------------
    def _gpx_sort_fun( self, data ):
        """
        for sorting gpx data
        this returns a key
        """
        key    = data.lat
        return key

    # ------------------------------------------
    def _get_gpx_sort_fun( self,   ):
        """
        Arguments
            implied self.gui
        return
            a sort function for gpx_data
            perhaps a lambda ... but then one liners
            could do from dict if get many
            output to gui
            !! consider change to dict base
        """
        gui        = AppGlobal.gui
        sort       = gui.get_sort_rb_index()

        if   sort == gui.NO_SORT:
            msg   = "No sorting of points"
            fun   = None     # flag value for no sort

        elif sort == gui.DATETIME_SORT:
            msg   = "Sort points on date"
            fun   = self._photo_plus_sort_key_on_datetime

        elif sort == gui.FN_SORT:
            msg   = "Sort points on filename"
            fun   = self._photo_plus_sort_key_on_filename

        else:
            msg   = "Not a valid sort from gui, No sorting of points"
            fun   = None     # flag value for no sort

        gui.write_gui( msg )
        return fun

    # ------------------------------------------
    def _sort_gpx_dataxxx( self, gpx_data, sort_fun  ):
        """
        not worth a function
        working on what it says
        should i get sort from gui ?? probably in get_gpx_sort fun
        return
            mutates gpx_data
        """
        # if sort_fun is None:
        #     sort_fun = self._gpx_sort_fun
        gpx_data.sort(  key = sort_fun )   # sort in place
        return gpx_data     # but this is same as what was passed in

    # ---- Filter ------------------------------------------
    def _gpx_filter_on_filedates( self, gpx_data, filter_fun   ):
        """
        for filtering gpx data --
             use with partial may need to make thru a partial to include gui data
        arguments
            gpx_data     list of photo plus
            filter_fun   function that filters return true or false
             !! might generalize some more
        Return
            new list
            writes to gui

        """
        msg    = f"Filter on dates now starting with {len( gpx_data )} points"
        AppGlobal.gui.write_gui( msg )

        new_gpx_data    = [ a_pp for a_pp in gpx_data if filter_fun( a_pp ) ]

        msg    = f"Filter on dates now {len( new_gpx_data )} points"
        AppGlobal.gui.write_gui( msg )

        return new_gpx_data

    # ------------------------------------------
    def _photo_plus_sort_key_on_filename( self, a_photo_plus, ):
        """
        we just want the extension which for now is in in a_photo plus
        but lets put it in via a get_ perhaps later a @property

        -- consider full path and lower casing

        """
        key     =  a_photo_plus.get_name( )
        return key

    # ------------------------------------------
    def _photo_plus_sort_key_on_datetime( self, a_photo_plus, ):
        """
        for sorting gpx data -- elements are _photo_plus items
        may need to make thru a partial to include gui data
        perhaps this is a _ppartial_photo_plus_date_filter

        """
        key     =  a_photo_plus.datetime
        return key

    # ------------------------------------------
    def _photo_plus_date_filter( self, a_photo_plus, start_datetime, end_datetime ):
        """
        for filtering gpx data
        may need to make thru a partial to include gui data
        perhaps this is a _ppartial_photo_plus_date_filter
        perhaps move to photo plus ... with other filters ??

        """
        ok     =  ( a_photo_plus.datetime >= start_datetime   and
                    a_photo_plus.datetime <= end_datetime )
        return ok

    # ------------------------------------------
    def _filter_gpx_dataxxx( self, gpx_data, filter_fun = None ):
        """
        working on what it says -- but looks like this is a sort function ???
        return
            mutates gpx_data
        """
        1/0
        if filter_fun is None:
            sort_fun = self._gpx_sort_fun()
        gpx_data.sort(  key = self._gpx_sort_fun )   # sort in place

    # ------------------------------------------
    def _kml_file_from_data( self, gpx_data, file_name = "path_rsh.kml" ):
        """
            file_name
            gpx_data     .... points to build a kml file
        """
        # Create a KML object
        kml = simplekml.Kml()

        # Define some coordinate points (latitude, longitude)
        # coordinates = [
        #     (37.7749, -122.4194),  # San Francisco, CA
        #     (34.0522, -118.2437),  # Los Angeles, CA
        #     (40.7128, -74.0060),   # New York City, NY
        # ]

        coordinates = []   # may not need this intermediary
        for i_photo_plus in gpx_data:

            if i_photo_plus.lat is None or i_photo_plus.long is None:
                continue
            # append a tuple
            coordinates.append( (   i_photo_plus.lat,        i_photo_plus.long, ) )

        # Create a KML LineString with tessellate set to True
        linestring = kml.newlinestring( name = "My Path" )
        linestring.tessellate = 1  # Set tessellate to 1 to create a tessellated line

        # Add coordinates to the LineString
        for lat, lon in coordinates:
            linestring.coords.addcoordinates([(lon, lat, 0)])  # Note the order: (longitude, latitude, altitude)

        # Set altitude mode to clampToGround to ensure the path follows the Earth's surface
        linestring.altitudemode = simplekml.AltitudeMode.clamptoground

        # Save the KML file to disk
        kml.save( file_name  )

        msg    = f"KML file {file_name} has been created."
        print( msg )

        # might want to make file_name absolute first !!
        os.popen( file_name )

    # ------------------------------------------
    def _make_gpx_from_data( self, gpx_data ):
        """
        Purpose
            from self.gpx_data make
            self.gpx     a gpx object


        Arg
            gpx_data -- photo plus objects
        Return
             gpx object
        Notes:
            reject data point if lat or long missing
        """
        msg     = "make_gpx_from_data..."
        AppGlobal.gui.write_gui( msg )
        # Create a GPX object
        gpx = gpxpy.gpx.GPX()

        # Create a track
        track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(track)

        track_point_list        = []
        max_min_lat_long        = MaxMinLatLong()  # move to

        # for i_lat_long in self.gpx_data:

        #     # Create some track points with made-up data
        #     a_track_point           = gpxpy.gpx.GPXTrackPoint(
        #                                  latitude  = i_lat_long[0],
        #                                  longitude = i_lat_long[1] )

        for data_point in gpx_data:

            if data_point.lat is None or data_point.long is None:
                continue

            max_min_lat_long.add_lat_long( data_point.lat, data_point.long)
            # Create some track points with made-up data
            a_track_point           = gpxpy.gpx.GPXTrackPoint(
                                         latitude  = data_point.lat,
                                         longitude = data_point.long,
                                             )

            a_track_point.time      = datetime.datetime( 2023, 10, 26, 10, 0, 0 )
            a_track_point.elevation = 100
            # a_track_point.speed     = 5  # meters per second
            track_point_list.append( a_track_point )

            # a_track_point = gpxpy.gpx.GPXTrackPoint(latitude=37.234567, longitude=-122.876543)
            # # a_track_point.time      = datetime.datetime(2023, 10, 26, 10, 15, 0)
            # # a_track_point.elevation = 110
            # # a_track_point.speed     = 4.5  # meters per second
            # track_point_list.append( a_track_point )

        # Add track points to the track
        track.segments.append(gpxpy.gpx.GPXTrackSegment( track_point_list ))
        self.max_min_lat_long = max_min_lat_long   # not good
        # Serialize the GPX data to a string  ... !! not sure why her seems not to be used
        print( "alright to comment out ")
        #gpx_data = gpx.to_xml()

        #rint(gpx_data)
        msg     = "make_gpx_from_data done" #" {gpx_data}"
        AppGlobal.gui.write_gui( msg )
        return  gpx

    # ------------------------------------------
    def _gpx_data_from_file_file_list( self, file_list ):
        """
        Purpose:
            make a gpx_data ( list of photo plus item ) from the file
            a file list
            * allow comment after file name -- no spaces in file name
            * may add line to default file list -- option
        Arguments
            file_list    list of file names, or perhaps pathlib.paths
        Return
            gpx_data     .... points to build a gpx file
        """
        #rint( self.file_list )
        gpx_data    = []  #  photo plus instances in list
        # next is not fast may want to see what is slowing it down
        for i_file in file_list:

            if i_file.startswith( "#"):
                print( i_file )
                continue

            i_file       = i_file.split(  maxsplit = 1  )[0]
                #allow content after filename ( control with gui or parameters )
            photo_plus   = photo_ext.PhotoPlus( i_file )
            if photo_plus.has_lat_long:
                gpx_data.append( photo_plus )
            #msg   = f" lat = {data_point.lat}   long =  {data_point.long}"
            #rint( msg )
            #AppGlobal.gui.write_gui( msg )
        # msg    = "done"
        # print( msg )
        #AppGlobal.gui.write_gui( msg )

        return gpx_data

    # ------------------------------------------
    def _get_file_list_from_file( self, file_name ):
        """
        Purpose:
            get a list of files from a file
            consider sort... or sort after have data??
            consider that files in file list exist??
        Return
             file_list   a list of files
        Except:
            app_exceptions.ReturnToGui

        """
        file_list   = []

        # chdek none
        if file_name is None:
            msg   = "File name is None, so cannot be processed to make a gpx"
            self.gui.write_gui( msg )
            raise app_exceptions.ReturnToGui( msg )

        # check extension
        file_path    = pathlib.Path( file_name )

        if file_path.suffix != ".txt":  # consider lower
            msg   = f"File name {file_name} is a not txt file, so cannot be processed"
            self.gui.write_gui( msg )
            raise app_exceptions.ReturnToGui( msg )

        # check exist
        if not file_path.exists():
            msg   = f"File name {file_name} is not a file that exists, so cannot be processed."
            self.gui.write_gui( msg )
            raise app_exceptions.ReturnToGui( msg )

        dffl_fn         = AppGlobal.parameters.default_filelist_fn
        add_to_dffl     = AppGlobal.gui.get_add_to_dffl()
        dffl            = None    # use this as file and flag
        if add_to_dffl:
            msg         = f"Adding to default file filelist {dffl_fn}"
            print( msg )
            self.gui.write_gui( msg )
            dffl        = open( dffl_fn,"a")

        line_no = 0   # enumerate instead
        with open( file_path, 'r' ) as file:
            for i_line in file:
                line_no  += 1
                if dffl:
                    dffl.write( i_line )
                i_line    = i_line.rstrip('\n')
                #rint( f"reading line no {line_no} =  {i_line }")
                file_list.append( i_line )
        if dffl:
            dffl.close()

        msg    = f"Made file list from {file_name} number of photos = {line_no}"
        print( msg )
        self.gui.write_gui( msg )

        return file_list

    # ------------------------------------------
    def _dir_to_filelist( self, filename  = None ):
        """
        Purpose:
            given a file name, scan the directory it is in
        """
        #return self._dir_to_filelist_old( filename  )
        return self._dir_to_filelist_new( filename  )

    # ------------------------------------------
    def _dir_to_filelist_new( self, filename  = None ):
        """
        Purpose:
            given a file name, scan the directory it is in
            and make a file list in this object for it

        arguments
            filename -- for dir to search
        returns:
            mutate      self.file_list
        """
        # validation could be a function
        filename  = filename.strip()
        if filename == "":
            msg   = (f"File, {filename}, is empty; operation terminated")
            self.gui.write_gui( msg )
            raise app_exceptions.ReturnToGui( msg )

        a_file_path   = pathlib.Path( filename )
        if not a_file_path.exists():
            msg   = (f"File, {filename}, does not exist; operation terminated")
            self.gui.write_gui( msg )
            raise app_exceptions.ReturnToGui( msg )

        if a_file_path.is_file():
            a_file_path    = a_file_path.parent

        #--------- directory
        recur_limit         = self.gui.get_recur_limit( )
        dir_filter_obj      = file_filters.DFAll()
        print( dir_filter_obj .demo_filter )

        #-------- file
        file_filter_obj     = file_filters.FFExtList( ["jpg", "pnp", ],
                                                     include_true = True,
                                                     use_lower    = True )

        dir_tree_explorer                   = dir_tree_explore.DirTreeExplorer()
        dir_tree_explorer.file_filter       = file_filter_obj
        dir_tree_explorer.directory_filter  = dir_filter_obj
        dir_tree_explorer.max_dir_depth     = recur_limit
        dir_tree_explorer.gui_write         = self.gui.write_gui

        dir_tree_explorer.explore_dir( a_file_path )
        file_list    = dir_tree_explorer.file_list

        self.write_todffl( file_list )

        return file_list

    # ------------------------------------------
    def _dir_to_filelist_old( self, filename  = None ):
        """
        Purpose:
            given a file name, scan the directory it is in
            and make a file list in this object for it

        arguments
            filename -- for dir to search
        returns:
            mutate      self.file_list
        """

        file_list     = []
        # apparently we also need to check for empty file name

        filename  = filename.strip()
        if filename == "":
            msg   = (f"File, {filename}, is empty; operation terminated")

            self.gui.write_gui( msg )
            raise app_exceptions.ReturnToGui( msg )

        a_file_path   = pathlib.Path( filename )
        if not a_file_path.exists():
            msg   = (f"File, {filename}, does not exist; operation terminated")
            self.gui.write_gui( msg )
            raise app_exceptions.ReturnToGui( msg )

        if a_file_path.is_file():
            a_file_path    = a_file_path.parent

        suffixes        = ["jpg","png", ]
        file_list       = [ str(path.absolute() )
                            for i in suffixes for path in a_file_path.glob("*."+i)]

        self.write_todffl(file_list)

        return file_list

    # ------------------------------------------
    def write_todffl( self, file_list ):
        """
        what it says -- move to file utils  -- see  ?
        args
            implicit from gui
        returns
            may append to file in file system... always does for now
        """
        # write to default file -- !! move to after sort ??
        dffl_fn         = AppGlobal.parameters.default_filelist_fn
        add_to_dffl     = AppGlobal.gui.get_add_to_dffl()
        dffl            = None    # use this as file and flag
        if True:
            msg         = f"Adding to default file filelist {dffl_fn}!!"
            print( msg )
            # !! change to with
            self.gui.write_gui( msg )
            dffl        = open( dffl_fn,"a")

            # i_line and message
            i_line      = f"# Begin _dir_to_filelist adding to file list {len(file_list)} files {datetime.datetime.now()}\n"
            dffl.write( f"{i_line}\n" )
            self.gui.write_gui( i_line )
            for i_line in file_list:
                dffl.write( f"{i_line}\n" )

            i_line      = f"# End _dir_to_filelist adding to file list {len(file_list)} files"
            dffl.write( f"{i_line}\n" )
            self.gui.write_gui( i_line )

            dffl.close()

        return

    # ---- gui_ functions -------------------
    # ------------------------------
    def gui_make_map_from_filelistxxxx( self, ):
        """
        Purpose
           what it says

        Arg
            file name comes from gui
        """
        gui        = AppGlobal.gui
        start_time = time.time()
        AppGlobal.gui.clear_message_area()
        file_name    = self.gui.get_browse()
        msg     = f"Make map from a filelist file using file {file_name}"
        AppGlobal.gui.write_gui( msg )

        try:
            file_list    = self._get_file_list_from_file( file_name )
            gpx_data     = self._gpx_data_from_file_file_list( file_list )

            gpx_data     = self._sort_filter_gpx_data( gpx_data )
            if len( gpx_data ) > 0:

                gpx          = self._make_gpx_from_data( gpx_data )
                self._gpx_to_map( gpx )
            else:
                msg  = "After filtering no points left to map"
                gui.write_gui( msg )

        except app_exceptions.ReturnToGui  as an_except:
            msg  = f"File Load failed, {an_except.why}"
            print( msg )
            gui.write_gui( msg )

        except app_exceptions.ApplicationError  as an_except:
            msg  = f"File Load failed, {an_except.why}"
            print( msg )
            AppGlobal.gui.write_gui( msg )

        end_time    = time.time()
        run_time    = round( end_time - start_time, 2 )
        msg         = f"End of Make Map from FileList... run time {run_time} sec"
        print( msg )
        AppGlobal.gui.write_gui( msg )

    # ------------------------------
    def _sort_filter_gpx_data( self, gpx_data ):
        """
        Purpose
           what it says -- consider rename
           !! is this still used
        Arg
            sort and filter criteria from gui
            gpx_data   list of photo_plus
            datetimes will be converted to utc ...
            !! may want to adjust with an offset or not ??
        """
        function_name   = "_sort_filter_gpx_data"

        #----- date filter
        #partial_fun      = None
        use_dates        = self.gui.get_use_dates()
        if use_dates:
            start_date   = self.gui.get_start_date()
            end_date     = self.gui.get_end_date()
            msg          = "need to error check start and end date here "
            print( msg )
            timezone     = self.gui.get_timezone
            timezone     = pytz.timezone( timezone  )
            start_datetime    = datetime.datetime.combine(
                                   start_date, datetime.datetime.min.time() )
            # now apply timezone
            start_datetime    = timezone.localize( start_datetime )
            start_datetime    = start_datetime.astimezone( timezone.utc )
            print( "_sort_filter_gpx_data !! not finished ")


            end_datetime      = datetime.datetime.combine(
                                   end_date,   datetime.datetime.max.time() )
            # now apply timezone
            end_datetime    = timezone.localize( end_datetime )
            end_datetime    = end_datetime.astimezone( timezone.utc )

            partial_fun       = partial( self._photo_plus_date_filter,
                                         start_datetime  = start_datetime,
                                         end_datetime    = end_datetime )
            msg     = f"Filter on  {start_datetime} to  {end_datetime} starting with {len( gpx_data)} points"
            AppGlobal.gui.write_gui( msg )

            gpx_data = [ i_gpx_point for i_gpx_point in gpx_data if partial_fun( i_gpx_point ) ]

            msg     = f"After Filterfiltered {len( gpx_data)} points"
            AppGlobal.gui.write_gui( msg )

        # if for next filter ( unless combine filters, faster but harder )
        else:
            msg     = f"No filter on {len( gpx_data)} points"
            AppGlobal.gui.write_gui( msg )

        # ----- sort
        #       keep after filter ( more efficient else seems to not matter)
        sort_function     = self._get_gpx_sort_fun()
        if not sort_function:
            # msg     = f"_sort_filter_gpx_data no sort"
            # AppGlobal.gui.write_gui( msg )
            pass

        else:
            # gpx_data = self._sort_gpx_data( gpx_data, sort_function )
            gpx_data.sort(  key = sort_function )   # sort in place

            msg     = "Data sorted"
            AppGlobal.gui.write_gui( msg )

        return gpx_data

    # ------------------------------
    def gui_open_dffl ( self, ):
        """
        Purpose
           what it says
        Arg
            file name comes from parameters
        """
        file_name   = AppGlobal.parameters.default_filelist_fn
        AppGlobal.os_open_txt_file( file_name )

    # ------------------------------
    def gui_make_kmz_from_filelistxxxxx ( self, ):
        """
        Purpose
           what it says
        Arg
            file name comes from gui

        """
        start_time = time.time()
        AppGlobal.gui.clear_message_area()
        file_name    = self.gui.get_browse()
        msg     = f"Make KMZ from a filelist file using file {file_name}"
        AppGlobal.gui.write_gui( msg )

        try:
            file_list    = self._get_file_list_from_file( file_name )
            gpx_data     = self._gpx_data_from_file_file_list( file_list )

            gpx_data     = self._sort_filter_gpx_data( gpx_data )
            if len( gpx_data ) > 0:

                gpx          = self._make_gpx_from_data( gpx_data )
                self._gpx_to_map( gpx )
            else:
                msg  = "After filtering no points left to map"
                gui.write_gui( msg )

            self._kml_file_from_data( gpx_data )

        except app_exceptions.ReturnToGui  as an_except:
            msg  = f"File Load for KMZ failed, {an_except.why}"
            print( msg )
            AppGlobal.gui.write_gui( msg )

        except app_exceptions.ApplicationError  as an_except:
            msg  = f"File Load for KMZ failed, {an_except.why}"
            print( msg )
            AppGlobal.gui.write_gui( msg )

        end_time    = time.time()
        run_time    = round( end_time - start_time, 2 )
        msg         = f"End of Make KMZ from FileList... run time {run_time} sec"
        print( msg )
        AppGlobal.gui.write_gui( msg )

    # ------------------------------
    def gui_make_map_from_dirxxxx( self, ):
        """
        Purpose
            what is says

        Arg
            use file_name from gui for directory
            and other gui stuff see code

        """
        gui          = AppGlobal.gui
        start_time   = time.time()
        AppGlobal.gui.clear_message_area()

        file_name    = self.gui.get_browse()
        msg     = f"Make map from a directory using file >{file_name}<"
        AppGlobal.gui.write_gui( msg )

        #default_filelist_fn
        #add_to_dffl   = AppGlobal.gui.get_add_to_dffl()

        try:
            file_list    = self._dir_to_filelist( file_name )
            #file_list    = self._get_file_list_from_file( file_name )
            gpx_data     = self._gpx_data_from_file_file_list( file_list )

            gpx_data     = self._sort_filter_gpx_data( gpx_data )
            if len( gpx_data ) > 0:
                gpx          = self._make_gpx_from_data( gpx_data )
                self._gpx_to_map( gpx )

            else:
                msg  = "After filtering no points left to map"
                gui.write_gui( msg )

        except app_exceptions.ReturnToGui  as an_except:
            msg  = f"File Load failed, {an_except.why}"
            AppGlobal.gui.write_gui( msg )

        except app_exceptions.ApplicationError  as an_except:
            msg  = f"File Load failed, {an_except.why}"
            AppGlobal.gui.write_gui( msg )

        end_time    = time.time()
        run_time    = round( end_time - start_time, 2 )
        msg         = f"End of Make Map from Directory... run time {run_time} sec"
        gui.write_gui( msg )

    # ------------------------------
    def gui_make_kmz_from_dirxxxx ( self, ):
        """
        Purpose
            what is says
        Arg
            use file_name from gui for directory
            and other gui stuff see code
        """
        start_time   = time.time()
        AppGlobal.gui.clear_message_area()

        file_name    = self.gui.get_browse()
        msg     = f"Make kKMZ file from a directory using file >{file_name}<"
        AppGlobal.gui.write_gui( msg )

        try:
            file_list    = self._dir_to_filelist( file_name )

            gpx_data     = self._gpx_data_from_file_file_list( file_list )

            gpx_data     = self._sort_filter_gpx_data( gpx_data )

            if len( gpx_data ) > 0:
                gpx          = self._make_gpx_from_data( gpx_data )
                self._kml_file_from_data( gpx_data )

            else:
                msg  = "After filtering no points left to map"
                gui.write_gui( msg )


            # a_filter_fun = self._get_gpx_filter_fun()  # so far just for dates
            # if a_filter_fun is None:
            #     msg = "No date filtering for this data"
            #     AppGlobal.gui.write_gui( msg )
            # else:
            #     gpx_data = self._gpx_filter_on_filedates(gpx_data, a_filter_fun )

        except app_exceptions.ReturnToGui  as an_except:
            msg  = f"KMZ file creation failed, {an_except.why}"
            print( msg )
            AppGlobal.gui.write_gui( msg )

        except app_exceptions.ApplicationError  as an_except:
            msg  = f"KMZ file creation failed, {an_except.why}"
            print( msg )
            AppGlobal.gui.write_gui( msg )

        end_time    = time.time()
        run_time    = round( end_time - start_time, 2 )
        msg         = f"End of KMZ file creation, from Directory... run time {run_time} sec"
        print( msg )
        AppGlobal.gui.write_gui( msg )

    # ------------------------------
    def gui_open_irfanviewxxxxx( self, ):
        """
        Purpose
            what is says

        Arg
            use file_name from gui for directory

        """
        file_name      = AppGlobal.parameters.irfanview_fn
        AppGlobal.os_popen_file( file_name )

    # ------------------------------
    def gui_make_map_from_gpx_file ( self, ):
        """
        Purpose
            what is says
            this is old version which does not make photoPlus points

        Arg
            use file_name from gui for directory

        """
        start_time = time.time()
        AppGlobal.gui.clear_message_area()
        file_name    = self.gui.get_browse()
        msg     = f"Make map from *.GPX file using file {file_name}"
        AppGlobal.gui.write_gui( msg )

        try:
            gpx          = self._gpx_from_gpxfile( file_name )
            self._gpx_to_map( gpx )

        except app_exceptions.ReturnToGui  as an_except:
            msg  = f"File Load failed, {an_except.why}"
            print( msg )
            AppGlobal.gui.write_gui( msg )

        except app_exceptions.ApplicationError  as an_except:
            msg  = f"File Load failed, {an_except.why}"
            print( msg )
            AppGlobal.gui.write_gui( msg )

        end_time    = time.time()
        run_time    = round( end_time - start_time, 2 )
        msg         = f"End of Make Map from GPX file... run time {run_time} sec"
        print( msg )
        AppGlobal.gui.write_gui( msg )

    # ------------------------------------------
    def makeup_gpx( self, ):
        """
        just makeup a gpx file ... this is a test
        debug only , move to ex_file
        """
        msg     = f"makeup_gpx{0}"
        AppGlobal.gui.write_gui( msg )
        # Create a GPX object
        gpx = gpxpy.gpx.GPX()

        # Create a track
        track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(track)

        track_point_list        = []
        # Create some track points with made-up data
        a_track_point           = gpxpy.gpx.GPXTrackPoint(latitude=37.123456, longitude=-122.987654)
        a_track_point.time      = datetime.datetime(2023, 10, 26, 10, 0, 0)
        a_track_point.elevation = 100
        a_track_point.speed     = 5  # meters per second
        track_point_list.append( a_track_point )

        a_track_point = gpxpy.gpx.GPXTrackPoint(latitude=37.234567, longitude=-122.876543)
        # a_track_point.time      = datetime.datetime(2023, 10, 26, 10, 15, 0)
        # a_track_point.elevation = 110
        # a_track_point.speed     = 4.5  # meters per second
        track_point_list.append( a_track_point )

        # Add track points to the track
        track.segments.append( gpxpy.gpx.GPXTrackSegment( track_point_list ) )

        # Serialize the GPX data to a string
        #gpx_data = gpx.to_xml()


        #rint(gpx_data)
        msg     = "makeup_gpx done" # {gpx_data}"
        AppGlobal.gui.write_gui( msg )

        self.gpx = gpx

    # ------------------------------------------
    def xxxx( self, file_name ):
        """
        self.file_name          = None
        self.gpx                = None
        self.url                = "./map_url.html"

        mutates
            self.gpx
        """
        pass

    # ------------------------------------------
    def _gpx_from_gpxfile( self,  file_name ):
        """
        required in vers 2023 12 03.01
            file_name needs to be a *.gpx file name
        returns
            gpx
        """
        # next might be a function ??
        # chdek none
        if file_name is None:
            msg   = "File name is None, so cannot be processed to make a gpx"
            self.gui.write_gui( msg )
            raise app_exceptions.ReturnToGui( msg )

        # check extension
        file_path    = pathlib.Path( file_name )

        if file_path.suffix != ".gpx":  # consider lower
            msg   = f"File name {file_name} is a not gpx file, so cannot be processed to make a gpx"
            self.gui.write_gui( msg )
            raise app_exceptions.ReturnToGui( msg )

        # check exist
        if not file_path.exists():
            msg   = f"File name {file_name} is not a file that exists, so cannot be processed to make a gpx"
            self.gui.write_gui( msg )
            raise app_exceptions.ReturnToGui( msg )

        with open( file_path, 'r' ) as readFile:
            gpx = gpxpy.parse( readFile )

        msg    = f"Made gpx object from {file_name}"
        print( msg )
        self.gui.write_gui( msg )

        return gpx

    # ------------------------------------------
    def scan_dir_to_filexxxx( self, ):
        """
        scan a directory to make a file listing files in dor

        next junk?
            self.file_name          = None
            self.gpx                = None
            self.url                = "./map_url.html"

            mutates
                a file
        """
        1/0   # still used
        scan_dir        = "D:/Russ/0000/python00/python3/_projects/rshlib"
        file_name_out   = "./file_list.txt"

        with open( file_name_out, 'w') as fno:

            path_dir = pathlib.Path( scan_dir )
            for i_path in path_dir.iterdir():
                # info = path.stat()
                ext    = i_path.suffix
                if ext == ".jpg":
                    pass
                else:
                    continue
                line = str( i_path.absolute() ) + "\n"
                fno.write( line )

    # ---- edits
    # ------------------------------------------
    def edit_map( self, ):
        """
        Purpose: what it says
        Arguments:
            none, read
        """
        AppGlobal.os_open_txt_file( AppGlobal.parameters.default_html_fn )

    # ------------------------------------------
    def edit_kmz( self, ):
        """
        Purpose: what it says
        Arguments:
            none, read
        """
        AppGlobal.os_open_txt_file( AppGlobal.parameters.default_kmz_fn )

    # ------------------------------------------
    def edit_photo_points( self, ):
        """
        Purpose: what it says
        Arguments:
            none, read
        """
        file_name     = AppGlobal.parameters.default_photo_points_fn
        AppGlobal.os_open_txt_file( file_name )

    # ------------------------------------------
    def edit_filelist( self, ):
        """
        Purpose: what it says
        Arguments:
            none, read
        """
        file_name     = AppGlobal.parameters.default_filelist_fn
        #rint( f"gui_open_browse_file look at type for {file_name}" )
        AppGlobal.os_open_txt_file( file_name )

    # ------------------------------------------
    def gui_open_browse_file( self, ):
        """
        Purpose:
        Arguments:
            use gui for input
        """
        gui           = AppGlobal.gui
        file_name     = gui.get_browse()
        print( f"gui_open_browse_file look at type for {file_name}" )

        AppGlobal.os_open_txt_file( file_name )

# ----------------------------------------
class MaxMinLatLong( ):
    """
    keep track of min and max lat long
    and return some useful info

    """
    # ----------------------------------------
    def __init__( self ):

        self.max_lat   = None
        self.max_long  = None
        self.min_lat   = None
        self.min_long  = None
        #self.max_span_to_zoom but max_span is a float...

    # ----------------------------------------
    def add_lat_long( self, lat, long ):
        """
        Purpose:
            read it

        """
        if lat is not None:
            if self.max_lat is None:
                self.max_lat = lat
            else:
                if lat > self.max_lat:
                    self.max_lat = lat

        if long is not None:
            if self.max_long is None:
                self.max_long = long
            else:
                if long > self.max_long:
                    self.max_long = long

        if lat is not None:
            if self.min_lat is None:
                self.min_lat = lat
            else:
                if lat < self.min_lat:
                    self.min_lat = lat

        if long is not None:
            if self.min_long is None:
                self.min_long = long
            else:
                if long < self.min_long:
                    self.min_long = long

    # ----------------------------------------
    def get_span( self,   ):
        """
        Purpose:
          get the span of max lat and long
          protect against none value

        """
        lat_span = None
        if self.max_lat and self.min_lat:
            lat_span = self.max_lat - self.min_lat

        long_span = None
        if self.max_long and self.min_long:
            long_span = self.max_long - self.min_long

        return ( lat_span, long_span )

    # ----------------------------------------
    def get_zoom ( self,   ):
        """
        Purpose:
          get the zoom for a map

        """
        max_span              = None
        zoom                  = 14
        span_lat, span_long   = self.get_span()
        msg    = f"span_lat  = {span_lat}    span_long = {span_long}"
        print( msg )

        if span_lat and span_long:
            max_span = max( span_lat, span_long )
            # perhaps a dict instead .... when maintain dict on float ng
            # unless round to nearest 10 or divide and use int ....
            if max_span > 2:
                zoom = 14
            if max_span  > 5:
                zoom = 5
        print( f"got zoom {zoom} for a max_span of {max_span}")
        return zoom


# ---- eof
