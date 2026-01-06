#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 15:34:13 2024

@author: russ


import adjust.path
"""
# ---- imports

# ---- imports

import os
import socket
import sys
from   pathlib import Path

# adjust according to where I am -- in progress
hostname              = socket.gethostname()
cwd                   = os.getcwd()
me                    = __file__
adjust_path_file      = __file__




PROJECT   = "not ready yet "
VERBOSE   = 50

if VERBOSE > 20:


    print( f"in {adjust_path_file   = }")
    print( f"{cwd                   = }")
    print( f"{hostname              = }")



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
__file__ = '/mnt/WIN_D/russ/0000/python00/python3/stuffdb/adjust_path.py'
'/mnt/WIN_D/russ/0000/python00/python3/stuffdb/adjust_path_new.py'
"""

try:
    #ix   = cwd.index( "_projects/stuffdb")
    ix   = cwd.index( "/stuffdb" )
    print( ix )

    src_root   = cwd[ : ix   ]
    print( f"in try {src_root = }" )
except ValueError as error:
    # Access the first argument (the message)
    error_message = error.args[0]
    print(f"fallback to hostname")


    if   hostname == "russ-ThinkPad-P72":
        src_root         = "/mnt/WIN_D/russ/0000/python00/python3"

    elif hostname == "smithers":
        src_root         = "/home/russ/sync_py_3"

    elif hostname == 'millhouse-mint':
        src_root         = "/home/russ/sync_py_3"

    elif hostname == 'fattony':
        src_root         = "/media/russ/m_toshiba_silver/sync_on_fattony/python3"

    elif hostname == 'M22ForUv':
        src_root         = "/media/sf_WIN_D/russ/0000/python00/python3"

    elif hostname == 'KingHomer':
        src_root         = "/mnt/8ball1/first6_root/russ/0000/python00/python03"

    else:
        src_root         = "/mnt/WIN_D/russ/0000/python00/python3"




#src_root         = "/mnt/WIN_D/russ/0000/python00/python3"
py3_root            = src_root
proj_root           = f"{py3_root}/_projects"
ex_root             = f"{py3_root}/_examples"


adjust_path_file      = __file__

# # least important at top
# sys.path.insert( 1, f"{proj_root}/rshlib" )adjust_path_file      = __file__
# sys.path.insert( 1, f"{src_root}/rshlib/test/"  )
#sys.path.insert( 1, f"{src_root}/rshlib/rshlib_qt/" )
sys.path.insert( 1, f"{src_root}/rshlib/in_spect" )
sys.path.insert( 1, f"{src_root}/rshlib" )

#/mnt/8ball1/first6_root/russ/0000/python00/python03/rshlib/app_services/app_global.py
sys.path.insert( 1, f"{src_root}/rshlib/app_services" )
sys.path.insert( 1, f"{src_root}/rshlib/rshlib_qt" )
sys.path.insert( 1, f"{src_root}/rshlib/utils" )




#sys.path.insert( 1, f"{src_root}/_examples" )
sys.path.insert( 1, f"{src_root}/stuffdb" )
sys.path.insert( 1, f"{src_root}/stuffdb/libs" )
sys.path.insert( 1, f"{src_root}/stuffdb/data_dict_src" )
sys.path.insert( 1, f"{src_root}/stuffdb/sql" )
sys.path.insert( 1, f"{src_root}/stuffdb/geo_photo" )
sys.path.insert( 1, f"{src_root}/stuffdb/sql" )






# sys.path.insert( 1, f"{src_root}/_projects/rshlib" )
# sys.path.insert( 1, f"{src_root}/_projects/rshlib/app_services" )
# sys.path.insert( 1, f"{src_root}/_projects/rshlib/in_spect" )

# sys.path.insert( 1, f"{src_root}/_examples" )

# sys.path.insert( 1, f"{src_root}/_projects/stuffdb" )

# sys.path.insert( 1, f"{src_root}/_projects/qt5_by_example" )




# # sys.path.append( r"D:\russ\0000\python00\python3\_projects\rshlib"  )
# # sys.path.append( "../")
# #sys.path.insert( 1, "../rshlib" )
# sys.path.insert( 1, "/home/russ/Documents/kw25/russ/0000/python00/python3/_projects/qt5_by_example" )


# sys.path.insert( 1, "/mnt/WIN_D/russ/0000/python00/python3/_projects/qt5_by_example/info_about_src" )
# #sys.path.insert( 1, "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb" )
# #sys.path.insert( 1, "/mnt/WIN_D/russ/0000/python00/python3/_projects/qt_by_example/ex_qt" )
# sys.path.insert( 1, "/mnt/WIN_D/russ/0000/python00/python3/_projects/rshlib/rshlib_qt/" )

# sys.path.insert( 1, "/mnt/WIN_D/russ/0000/python00/python3/_examples/" )
# #sys.path.insert( 1, "/mnt/WIN_D/russ/0000/python00/python3/_examples/qt" )
# #sys.path.insert( 1, "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb")
# sys.path.insert( 1, "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb")
# #rom    app_global import AppGlobal

# print( "your path has been adjusted for theProf Mint "
#        "\n    from /mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/adjust_path.py" )


if VERBOSE > 20:
    print( "    path now:" )
    for i_path in sys.path:
        print( "        ", i_path )



print( "end your path has been adjusted " )