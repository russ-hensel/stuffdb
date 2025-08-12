#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 15:34:13 2024

@author: russ


import adjust.path
"""
# ---- imports

import os
import socket
import sys
from pathlib import Path

# adjust according to where I am -- in progress
hostname              = socket.gethostname()
cwd                   = os.getcwd()
adjust_path_file      = __file__

VERBOSE   = 50

if VERBOSE > 20:

    print( "in adust_path")
    print( f"{adjust_path_file = }")
    print( f"{cwd                    = }")
    print( f"{hostname          = }")

# if   hostname == "russ-ThinkPad-P72":
#     src_root         = "/mnt/WIN_D/russ/0000/python00/python3"
# elif hostname == "russ-ThinkPad-P72":
#     src_root         = "/mnt/WIN_D/russ/0000/python00/python3"
# else:
#     src_root         = "/mnt/WIN_D/russ/0000/python00/python3"


"""
can we assume that we are using from cwd
lets say no do we want to change directory lets say no



simplest to do just off of hostname
project_root       is this the same as ./  we assume not
python3_root       .. this may only be on rh machine
adjust_path_root  =


hostname          = 'russ-ThinkPad-P72'
derive
print( f"{__name__ = } ")
print( f"{__file__ = }   ")
__name__ = 'adjust_path'
__file__ = '/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/adjust_path.py'
'/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/adjust_path_new.py'
"""


# print( f"{__file__}")

adjust_path_path        = Path( adjust_path_file )
ap_dir_path             = adjust_path_path.parent  # often same as ./

project_dir_path        = ap_dir_path.parent

print( f"{project_dir_path = }")


if hostname  == "russ-ThinkPad-P72":
    sys.path.insert( 1, f"{ap_dir_path}/libs" )
    sys.path.insert( 1, f"{ap_dir_path}/data_dict_src" )
    sys.path.insert( 1, f"{ap_dir_path}/sql" )
    sys.path.insert( 1, f"{ap_dir_path}/py_helpers" )

    sys.path.insert( 1, f"{project_dir_path}/rshlib" )
    sys.path.insert( 1, f"{project_dir_path}/rshlib/app_services" )
    sys.path.insert( 1, f"{project_dir_path}/rshlib/rshlib_qt/" )
    sys.path.insert( 1, f"{project_dir_path}/rshlib/in_spect" )

else:
    # minimun change




    src_root        = __file__
    on_russ_dev     = True
    ix              = src_root.find( '_projects/stuffdb' )
    if ix < 0:
        pass
        #on_russ_dev = False

    else:
        src_root        = src_root[ :ix ]
        print( src_root )

        # may want to mess with test phrase
        if   "0000/python00/python3/" in src_root:
            print( "running in russ dev env")
            on_russ_dev     = True
        else:
            on_russ_dev     = True
            print( "not -------------------------------" )


#let try to automate this
# src_root         = "/mnt/WIN_D/russ/0000/python00/python3"


# ---- ./ path
on_russ_dev  = False
if on_russ_dev:
    sys.path.insert( 1, f"{src_root}/_projects/stuffdb" )


    sys.path.insert( 1, f"./libs" )   # for installation off dev machines
    sys.path.insert( 1, f"./data_dict_src" )   # for installation off dev machines
    sys.path.insert( 1, f"./sql" )   # for installation off dev machines
    sys.path.insert( 1, f"./py_helpers" )   # for installation off dev machines


# fix this for linux derive from file
src_root   =  r"D:\russ\0000\python00\python3"


if on_russ_dev:
# ---- only on russ's computers
    sys.path.insert( 1, f"{src_root}/_projects/rshlib" )

    sys.path.insert( 1, f"{src_root}/_projects/rshlib/app_services" )
    sys.path.insert( 1, f"{src_root}/_projects/rshlib/rshlib_qt/" )
    sys.path.insert( 1, f"{src_root}/_projects/rshlib/in_spect" )

    sys.path.insert( 1, f"{src_root}/_examples" )

    sys.path.insert( 1, f"{src_root}/_projects/stuffdb" )
    sys.path.insert( 1, f"{src_root}/_projects/stuffdb/py_helpers" )
    sys.path.insert( 1, f"{src_root}/_projects/stuffdb/data_dict_src" )
    sys.path.insert( 1, f"{src_root}/_projects/stuffdb/sql" )

    sys.path.insert( 1, f"{src_root}/_projects/qt5_by_example" )
    sys.path.insert( 1, f"{src_root}/_projects/qt5_by_example/info_about_src" )

    sys.path.insert( 1, f"{src_root}/_projects/stuffdb" )




#rom    app_global import AppGlobal


if VERBOSE >= 20:
    print( "your path has been adjusted for theProf Mint "
           "\n    from /mnt/WIN_D/Russ/0000/python00/python3/_projects/stuffdb/adjust_path.py" )

if VERBOSE >= 20:
    print( "    path now:" )
    for i_path in sys.path:
        print( f"         >{i_path}<" )