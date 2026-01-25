#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 11 10:01:04 2026


"""
# ---- tof
# ---- imports
from   pathlib import Path
import importlib


import adjust_path
import data_dict_all


#------------
def build_schema_dict( schema_name, dir_list  ):
    """
    return schema_dict
    """
    module_list    = find_dict_modules( dir_list, schema_name )
    a_schema_dict  = data_dict_all.SchemaDict( schema_name )

    # this builds in the data
    for i_module in module_list:
         a_module = importlib.import_module( i_module  )
         a_module.build_it( a_schema_dict )



    # for i_module in module_list:
    #      print( i_module )

    #      a_module = importlib.import_module( i_module  )
    #      a_module.build_it( a_schema_dict )

    # print( a_schema_dict )
    # a_table_dict     = a_schema_dict.get_table( "stuff" )
    # print( a_table_dict )
    return a_schema_dict

#------------
def find_dict_modules( dir_list, schema_name  ):
    """
    find the object files and make a list
       may later need to use .name or .stem
    dir_list, list of strings or perhaps paths pointing to dirs
    returns file list, canicates for inclusion
    """
    dir_list            = list( set( dir_list ))  # de dup
    file_list           = []
    module_list         = []

    for i_directory in dir_list:
        i_directory     = Path( i_directory )
        i_file_list     = [file  for file in i_directory.glob('*dict*.py')  ]
                # not .stem or .name which may be needed later
        for i_file in i_file_list:
            if is_dict_module( i_file, schema_name ):
                # if so strip to module name
                i_path   = Path( i_file )
                i_module = i_path.stem

                module_list.append( i_module )


    # msg         = "index_and_search.py find_doc_files this is the file list"
    # logging.debug( msg )
    # for ix, i_file in enumerate( file_list ):
    #     msg    = f" {ix }ix, {i_file} "
    #     logging.debug( msg )


    return module_list

#------------
def is_dict_module( file_name, schema_name ):
    """
    return boolean

    """
    file_data  = get_file_data( file_name )
    # if str( i_doc ) == "tab_box_layout.py":
    module_db_name      = file_data.get( "db_name", None )
    return ( module_db_name == schema_name )

#------------
def get_file_data( file_name ):
    """
    look down 35 or so lines
    """

    file_data   = {}

    a_file      = open( file_name, 'r', encoding = "utf8", errors = 'ignore' )

    for ix, i_line in enumerate( a_file ):

        # looks like a loop woruld do all this
        i_line    = i_line.rstrip('\n')   # this i think is the best way --- think is arg to have python strip
        i_line    = i_line.strip()
        #rint( f"reading line no {ix} =  {i_line }")


        if i_line.startswith( "DB_NAME:"):
            i_line    = i_line[ 10: ].strip()
            file_data[ "db_name" ] =  i_line

        # if i_line.startswith( "MODULE:"):
        #         i_line    = i_line[ len("MODULE:" ): ].strip()
        #         doc_data[ "module" ] = doc_data[ "module" ] + " " + i_line


        if ix > 35:   # line limit
            #rint( "break on ix .....")
            break

    a_file.close()

    #rint( f"{file_data = }")

    return file_data

#--------------------------------------
def test_it(   ):
    """
    work towards getting a SchemaDict for a schema_name
    """
    schema_name     = "stuffdb"
    dir_list        = [ "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/stuffdb/data_dict_src" ]
    a_schema_dict   = build_schema_dict( schema_name, dir_list )

    # for i_module in module_list:
    #      print( i_module )

    #      a_module = importlib.import_module( i_module  )
    #      print( a_module )




    # for i_module in module_list:
    #      print( i_module )

    #      a_module = importlib.import_module( i_module  )
    #      a_module.build_it( a_schema_dict )

    print( a_schema_dict )
    a_table_dict     = a_schema_dict.get_table( "stuff" )
    print( a_table_dict )

# --------------------
if __name__ == "__main__":
    #----- run the full app

    test_it()

# --------------------
