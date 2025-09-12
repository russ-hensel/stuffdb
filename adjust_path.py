#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 15:34:13 2024

@author: russ


import adjust.path

still a bit of a mess


"""
# ---- imports

import os
import socket
import sys
from   pathlib import Path

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
app_dir_path            = adjust_path_path.parent
    # often same as ./
    # directory of the app startup like where main.py is

project_dir_path        = app_dir_path.parent      # ..../_projects
    # one level up where russ keeps all projects
    # probably unique to hei

print( f"{app_dir_path     = }")
print( f"{project_dir_path = }")


if hostname  in [ "russ-ThinkPad-P72", 'millhouse-mint', 'fattony' ]:
    sys.path.insert( 1, f"{app_dir_path}/libs" )
    sys.path.insert( 1, f"{app_dir_path}/data_dict_src" )
    sys.path.insert( 1, f"{app_dir_path}/sql" )
    sys.path.insert( 1, f"{app_dir_path}/py_helpers" )

    sys.path.insert( 1, f"{project_dir_path}/rshlib" )
    sys.path.insert( 1, f"{project_dir_path}/rshlib/app_services" )
    sys.path.insert( 1, f"{project_dir_path}/rshlib/rshlib_qt/" )
    sys.path.insert( 1, f"{project_dir_path}/rshlib/in_spect" )

else:
    sys.path.insert( 1, f"{app_dir_path}/libs" )
    sys.path.insert( 1, f"{app_dir_path}/data_dict_src" )
    sys.path.insert( 1, f"{app_dir_path}/sql" )
    sys.path.insert( 1, f"{app_dir_path}/py_helpers" )



# what is this??
src_root        = __file__
on_russ_dev     = False
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




# ---- only on russ's computers
    # sys.path.insert( 1, f"{src_root}/_projects/rshlib" )

    # sys.path.insert( 1, f"{src_root}/_projects/rshlib/app_services" )
    # sys.path.insert( 1, f"{src_root}/_projects/rshlib/rshlib_qt/" )
    # sys.path.insert( 1, f"{src_root}/_projects/rshlib/in_spect" )

    # sys.path.insert( 1, f"{src_root}/_examples" )

    # sys.path.insert( 1, f"{src_root}/_projects/stuffdb" )
    # sys.path.insert( 1, f"{src_root}/_projects/stuffdb/py_helpers" )
    # sys.path.insert( 1, f"{src_root}/_projects/stuffdb/data_dict_src" )
    # sys.path.insert( 1, f"{src_root}/_projects/stuffdb/sql" )

    # sys.path.insert( 1, f"{src_root}/_projects/qt5_by_example" )
    # sys.path.insert( 1, f"{src_root}/_projects/qt5_by_example/info_about_src" )

    # sys.path.insert( 1, f"{src_root}/_projects/stuffdb" )




#rom    app_global import AppGlobal


if VERBOSE >= 20:
    print( "your path has been adjusted for theProf Mint "
           f"\n    from {__file__}" )

if VERBOSE >= 20:
    print( "    path now:" )
    for i_path in sys.path:
        print( f"         >{i_path}<" )