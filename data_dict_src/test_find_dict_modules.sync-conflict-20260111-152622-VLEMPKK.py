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

import find_dict_modules


#--------------------------------------
def test_get_schema_dict( verbose  ):
    """
    work towards getting a SchemaDict for a schema_name
    """
    schema_name     = "stuffdb"
    dir_list        = [ "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/stuffdb/data_dict_src" ]
    a_schema_dict   = find_dict_modules.build_schema_dict( schema_name, dir_list )

    # for i_module in module_list:
    #      print( i_module )

    #      a_module = importlib.import_module( i_module  )
    #      print( a_module )

    # for i_module in module_list:
    #      print( i_module )

    #      a_module = importlib.import_module( i_module  )
    #      a_module.build_it( a_schema_dict )
    if   verbose >20:
        print( a_schema_dict )
        a_table_dict     = a_schema_dict.get_table( "stuff" )
        print( a_table_dict )

    return a_schema_dict

# --------------------
if __name__ == "__main__":
    #----- run the full app

    test_get_schema_dict( verbose = 30  )

# --------------------
