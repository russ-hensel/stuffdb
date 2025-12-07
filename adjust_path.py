#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


import adjust.path
"""


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
__file__ = '/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/adjust_path.py'
'/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/adjust_path_new.py'
"""

try:
    ix   = cwd.index( "_projects/stuffdb")
    print( ix )

    src_root   = cwd[ : ix - 1 ]
    print( f"in try{src_root = }" )
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
    
     
#comp_root        = "/home/russ/sync_py_3/"
#src_root         = "/home/russ/sync_py_3"


#comp_root        = "/mnt/WIN_D/russ/0000/python00/"
#src_root         = "/mnt/WIN_D/russ/0000/python00/python3"
py3_root            = src_root
proj_root           = f"{py3_root}/_projects"
ex_root             = f"{py3_root}/_examples"


# print( f"{__file__}")

adjust_path_path        = Path( adjust_path_file )
app_dir_path            = adjust_path_path.parent
    # often same as ./
    # directory of the app startup like where main.py is

project_dir_path        = app_dir_path.parent      # ..../_projects
    # one level up where russ keeps all projects
    # probably unique to hei
#rint( f"{hostname              = }")
print( f"{app_dir_path          = }")
print( f"{project_dir_path      = }")



adjust_path_file      = __file__

# # least important at top
# sys.path.insert( 1, f"{proj_root}/rshlib" )adjust_path_file      = __file__
# sys.path.insert( 1, f"{src_root}/_projects/rshlib/test/"  )
#sys.path.insert( 1, f"{src_root}/_projects/rshlib/rshlib_qt/" )
sys.path.insert( 1, f"{src_root}/_projects/rshlib/in_spect" )
sys.path.insert( 1, f"{src_root}/_projects/rshlib" )

#/mnt/8ball1/first6_root/russ/0000/python00/python03/_projects/rshlib/app_services/app_global.py
sys.path.insert( 1, f"{src_root}/_projects/rshlib/app_services" )
sys.path.insert( 1, f"{src_root}/_projects/rshlib/rshlib_qt" )



#sys.path.insert( 1, f"{src_root}/_examples" )
sys.path.insert( 1, f"{src_root}/_projects/stuffdb" )
sys.path.insert( 1, f"{src_root}/_projects/stuffdb/libs" )
sys.path.insert( 1, f"{src_root}/_projects/stuffdb/data_dict_src" )
sys.path.insert( 1, f"{src_root}/_projects/stuffdb/sql" )
sys.path.insert( 1, f"{src_root}/_projects/stuffdb/geo_photo" )
sys.path.insert( 1, f"{src_root}/_projects/stuffdb/sql" )

#sys.path.insert( 1, f"{src_root}/_projects/qt5_by_example" )
#sys.path.insert( 1, f"{src_root}/_projects/clipboard" )

# #sys.path.insert( 1, "../rshlib" )
# sys.path.insert( 1, "./ex_qt" )
# sys.path.insert( 1, "/mnt/WIN_D/Russ/0000/python00/python3/_examples/" )
# sys.path.insert( 1, "/mnt/WIN_D/Russ/0000/python00/python3/_examples/qt" )
# #rom    app_global import AppGlobal


print( "your path has been adjusted fron qt5_by_example on theProf Mint from qt5_by_example" )
for i_path in sys.path:
    print( f"{i_path = }")

print( "end your path has been adjusted " )






