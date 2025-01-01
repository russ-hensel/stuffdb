#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 15:34:13 2024

@author: russ


import adjust.path
"""
# ---- imports

import sys

# sys.path.append( r"D:\Russ\0000\python00\python3\_projects\rshlib"  )
# sys.path.append( "../")
sys.path.insert( 1, "../rshlib" )
sys.path.insert( 1, "/mnt/WIN_D/Russ/0000/python00/python3/_projects/qt_by_example" )
sys.path.insert( 1, "/mnt/WIN_D/Russ/0000/python00/python3/_projects/qt_by_example/info_about" )
#sys.path.insert( 1, "/mnt/WIN_D/Russ/0000/python00/python3/_projects/stuffdb" )
#sys.path.insert( 1, "/mnt/WIN_D/Russ/0000/python00/python3/_projects/qt_by_example/ex_qt" )
sys.path.insert( 1, "/mnt/WIN_D/Russ/0000/python00/python3/_projects/rshlib/rshlib_qt/" )
sys.path.insert( 1, "/mnt/WIN_D/Russ/0000/python00/python3/_examples/" )
sys.path.insert( 1, "/mnt/WIN_D/Russ/0000/python00/python3/_examples/qt" )
sys.path.insert( 1, "/mnt/WIN_D/Russ/0000/python00/python3/_projects/stuffdb")
#rom    app_global import AppGlobal

print( "your path has been adjusted for theProf Mint "
       "\n    from /mnt/WIN_D/Russ/0000/python00/python3/_projects/stuffdb/adjust_path.py" )

print( "    path now:" )
for i_path in sys.path:
    print( "        ", i_path )