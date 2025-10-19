#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 08:31:23 2023
csv in and out
simple
esp for geo_track
import photo.file_utils
file_utils.
"""

# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    main.main()
# --------------------

import datetime

import photo_ext
from   app_global import AppGlobal


# ---- end imports

def write_photo_points( file_name, photo_points, comment_lines = None ):
    """
    csv_stuff.write_photo_points( file_name, photo_points, comment_lines = None )
    Args:
        file_name (TYPE): DESCRIPTION.
        photo_points (TYPE): DESCRIPTION.photo_ext
        comment_lines (TYPE, optional): DESCRIPTION. Defaults to None.

    Returns:
        None.

    """
    with open( file_name, "w" ) as a_file:
        print( f"write_photo_points {file_name}", flush = True )
        # still need to do comments
        ix = 42
        for ix, i_point in enumerate( photo_points ):
            i_line       = ( f"{i_point.filename}\t{i_point.datetime}\t{i_point.long}\t{i_point.lat}\t" )
            a_file.write( f"{i_line}\n" )

    print( f"write_photo_points done {ix}", flush = True )

# --------------------
def read_photo_points( file_name, ):
    """
    photo_points  = file_utils.read_photo_points( file_name, )
    Args:
        file_name (TYPE): DESCRIPTION.
        photo_points (TYPE): DESCRIPTION.
        comment_lines (TYPE, optional): DESCRIPTION. Defaults to None.

    Returns:
        None.

    """
    photo_points    = []

    with open( file_name, 'r', encoding = "utf8", errors = 'ignore' ) as file_src:
        line_no         = 0
        for i_line in file_src:
            line_no  += 1
            print( f"reading line no {line_no} =  {i_line }")
            i_line    = i_line.rstrip('\n')
            if i_line.startswith( "#" ):  # comments
                print( i_line )
                continue

            a_photo_point           = photo_ext.PhotoPlus(   )
            splits                  = i_line.split( "\t" )

            a_photo_point.filename  = splits[0]

            # a_photo_point.datetime  = datetime.datetime( splits[1] )
            a_photo_point.datetime  = datetime.datetime.strptime( splits[1],  "%Y-%m-%d %H:%M:%S" )

            # may need null check here
            has_long_lat            = True
            try:
                data                =  float( splits[2] )
            except:
                data                = None
                has_long_lat        = False
            a_photo_point.long      = data
            try:
                data                =  float( splits[3] )
            except:
                data                = None
                has_long_lat         = False
            a_photo_point.lat       = data

            a_photo_point.has_lat_long  = has_long_lat

            photo_points.append(  a_photo_point )

        return photo_points

# ------------------------------------------
def write_file_list( file_name, file_list, append_flag = False ):
    """
    what it says -- move to file utils
    args
        implicit from gui
    returns
        may append to file in file system

    """
    # write to defaul file -- !! move to after sort ??
    gui       = AppGlobal.gui

    if append_flag:
        flag        = "a"
    else:
        flag        = "w"

    msg         = f"Writing filelist file {file_name} with flag  {flag}"
    print( msg )
    gui.write_gui( msg )

    with open( file_name, flag, encoding = "utf8", )  as file:

        # i_line and message
        i_line      = f"# Begin _dir_to_filelist adding to file list {len(file_list)} files {datetime.datetime.now()}\n"
        file.write( f"{i_line}\n" )
        gui.write_gui( i_line )
        for i_line in file_list:
            file.write( f"{i_line}\n" )

        i_line      = f"# End _dir_to_filelist adding to file list {len(file_list)} files"
        file.write( f"{i_line}\n" )
        gui.write_gui( i_line )

# ------------------------------------------
def read_flf_to_fl( file_list_fn ):
    """
    what it says -- move to file utils
    args
        implicit from gui
    returns
        a file list

        file_utils.read_flf_to_fl( file_list_fn )
    """
    gui       = AppGlobal.gui

    msg   = f"add read_flf_to_fl    >{file_list_fn}<"
    print( msg   )
    # write to defaul file -- !! move to after sort ??
    with open( file_list_fn, "r" ) as a_file:
        file_list   =[]
        for i_line in a_file:
            # each line will have a \n at the end remove with rstrip()
            i_line   = i_line.rstrip()
            if i_line == "":
                continue
            if i_line.startswith( "#" ):
                continue
            file_list.append( i_line )
            msg   = f"add to file list >{i_line}<"
            print( msg   )
            gui.write_gui( msg )

    return  file_list


# ---- eof