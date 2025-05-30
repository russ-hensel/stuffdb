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

# adjust according to where I am -- in progress
hostname              = socket.gethostname()
cwd                   = os.getcwd()
adjust_path_file      = __file__

VERBOSE   = 5

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

print( f"{__name__ = } ")
print( f"{__file__ = }   ")
__name__ = 'adjust_path'
__file__ = '/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/adjust_path.py'

"""


# print( f"{__file__}")

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


# ---- ./ path

if on_russ_dev:
    sys.path.insert( 1, f"{src_root}/_projects/stuffdb" )


sys.path.insert( 1, f"./libs" )   # for installation off dev machines
sys.path.insert( 1, f"./data_dict_src" )   # for installation off dev machines
sys.path.insert( 1, f"./sql" )   # for installation off dev machines
sys.path.insert( 1, f"./py_helpers" )   # for installation off dev machines

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
        print( "        ", i_path )