#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search for ia objects to create

just started is it a good idea
this should make less setup code -- not sure if any implemented


"""

# ---- tof

# # --------------------
# if __name__ == "__main__":
#     #----- run the full app
#     import main
#     # import qt_search
#     # qt_search.main()
# # --------------------

import inspect
import os
import sqlite3 as lite
import subprocess
import sys
from functools import partial
from pathlib import Path
from platform import python_version
from subprocess import PIPE, STDOUT, Popen, run

#import global_vars
import ia_parameters

#port wat_inspector

VERBOSE    = False
# ---- ---- local imports
#print_func_header  = uft.print_func_header

LINE_LIMIT   = 25   # or move to parameters

# -------------------------------------
class IaSearch():
    """
    this will create
    """
    #-------------------
    def __init__( self ):
        """
        The usual
        """
        # self.db    = None
        # self.reset()

        # global_vars.set_tab_db( self.db  )
        # global_vars.set_tab_db_builder( self  )

        if  VERBOSE is True:
            print( "ia_search.IaSearch find_ia_files now know as info_about, not yet updated ")

            print( "loop thru files")

            print( "    finding file data")
            print( "    save file data")

        self.file_path_list    = self.find_ia_files()
        self.inspect_files( self.file_path_list )


    #------------
    def find_ia_files( self, ):
        """
        find the object files and make a list
            these are file_paths, not file_names
            may later need to use .name or .stem
        """
        directory_list      = ia_parameters.PARAMETERS.dir_for_search
        file_path_list      = []
        #i_directory    = Path( "./" )
        for i_directory in directory_list:
            i_directory = Path( i_directory )

            i_file_path_list    = [file  for file in i_directory.glob('info_about*.py')  ]
                    # not .stem or .name whic may be needed later path not string

            file_path_list      = file_path_list + i_file_path_list
        msg      =  f"find_ia_files {VERBOSE = }"
        print( msg )
        for ix, i_file_path in enumerate( file_path_list ):
            if  VERBOSE is True:
               print( ix, i_file_path)

        return file_path_list

    # ----- helper key function
    def get_key( self, item ):
        """
        replace with lambda
        given an item, returns a key for sorting purposes
        these functions are often done as lambda functions
        but that can be confusing if you are not used to lambda
        """
        # choose a way of computing
        #key   = 1/item

        key   = item[ "sort_order:" ]
        key   = -int( key )
        #print( f"IaSearch get_key {key = }" )
        return key

    #------------
    def inspect_files( self, file_path_list ):
        """
        inspect the files and build
            self.file_data_list    = file_data_list
        """
        file_data_list    = []
        for i_file in file_path_list:
            file_data    = self.get_file_data( i_file )
            if file_data is not None:
                file_data_list.append( file_data )

        file_data_list.sort(  key = self.get_key )

        #rint( file_data_list )
        self.file_data_list    = file_data_list

    #------------
    def get_file_data( self, file_path ):
        """
        beware file_name really file_name_path
        read the doc data into a dict strings?
        file_name think string or path
        change to with
        """
        #rint( f"get_doc_data {file_name = }")
        #rint( "could make a loop to do this maybe a comp !!")

        # APPLICATION:    information_about
        # KEY_WORDS:      sql query of a single table crud select insert update delete
        # does next need orderign -- require InforAbout  ObjectName
        # CLASS_NAMES:    InfoAboutQSqlRecord InfoAboutQSqlField

        file_data_items       = [ "application:",
                                  "class_names:",
                                  "sort_order:"
                                 ] # omit module and module_file_name

        file_data    = {}
        file_data[ "file_path:"  ]  =  file_path
        file_data[ "module:"  ]     =  file_path.stem

        # inti to empty -- so will exist if not found
        for i_file_data_item in file_data_items:
            file_data[ i_file_data_item ] = ""

        # file_data[ "doc_file_name" ] = file_name

        a_file  = open( file_path, 'r', encoding = "utf8", errors = 'ignore' )

        for ix, i_line in enumerate( a_file ):

            i_line          = i_line.strip()
            i_line_lower    = i_line.lower()



            # if i_line_lower.startswith( item ):
            #         i_line    = i_line[ len( item ) + 1 : ].strip()
            #         file_data[ i_file_data_item ] = file_data[ i_file_data_item ] + " " + i_line
            # i_line          = i_line.rstrip('\n')   # this i think is the best way --- think is arg to have python strip
            # i_line          = i_line.strip()
            # i_line_lower    = i_line.lower()
            # #rint( f"reading line no {ix} =  {i_line }")

            # # this loop is great be seem to be too many special items
            # for i_file_data_item in file_data_items:
            #     if i_line_lower.startswith( i_file_data_item ):
            #         i_line    = i_line[ len(i_file_data_item) + 1 : ].strip()
            #         file_data[ i_file_data_item ] = file_data[ i_file_data_item ] + " " + i_line
                        # should get rid of id

            # slightly different processing eware
            item       =  "application:"
            if i_line_lower.startswith( item ):
                    i_line    = i_line[ len( item ) + 1 : ].strip()
                    file_data[ item ] =  i_line


            item       = "sort_order:"
            if i_line_lower.startswith( item ):
                    i_line    = i_line[ len( item ) + 1 : ].strip()
                    file_data[ item ] =  i_line


            item       =  "class_names:"  # can be multiple
            if i_line_lower.startswith( item ):
                    i_line    = i_line[ len( item ) + 1 : ].strip()
                    file_data[ item ] = file_data[ item ] + " " + i_line





            # if i_line.startswith
            #         i_line    = i_line[ 10: ].strip()
            #         file_data[ "application" ] = file_data[ "application" ] + " " + i_line

            # # next could be a loop if we had many

            # key         = "class_names"
            # if i_line.startswith(  f"{key.upper()}:"):
            #         i_line    = i_line[ len(key) + 1 : ].strip()
            #         file_data[ key ] = file_data[ key ] + " " + i_line


            if ix > LINE_LIMIT:   # line limit
                #rint( "break on ix .....")
                break

        a_file.close()

        #rint( f"{file_data = }")
        if file_data[ "application:"] != "info_about":
            return None

        return file_data


# ---- eof
