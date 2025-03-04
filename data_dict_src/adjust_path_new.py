#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 15:34:13 2024

# ---- imports

import sys
# sys.path.append( r"D:\Russ\0000\python00\python3\_projects\rshlib"  )
# sys.path.append( "../")
src_root         = "/mnt/WIN_D/Russ/0000/python00/python3"
sys.path.insert( 1, f"{src_root}/_projects/rshlib" )
sys.path.insert( 1, f"{src_root}/_examples" )
sys.path.insert( 1, f"{src_root}/_projects/stuffdb" )
sys.path.insert( 1, f"{src_root}/_projects/qt5_by_example" )


import adjust.path
"""
# ---- imports

import sys

src_root         = "/mnt/WIN_D/Russ/0000/python00/python3"
sys.path.insert( 1, f"{src_root}/_projects/rshlib" )
sys.path.insert( 1, f"{src_root}/_projects/rshlib/rshlib_qt/" )
sys.path.insert( 1, f"{src_root}/_projects/rshlib/in_spect" )

sys.path.insert( 1, f"{src_root}/_examples" )

sys.path.insert( 1, f"{src_root}/_projects/stuffdb" )
sys.path.insert( 1, f"{src_root}/_projects/qt5_by_example" )
sys.path.insert( 1, f"{src_root}/_projects/qt5_by_example/info_about_src" )



# # # sys.path.append( r"D:\Russ\0000\python00\python3\_projects\rshlib"  )
# # # sys.path.append( "../")
# # sys.path.insert( 1, "../rshlib" )
# # sys.path.insert( 1, "/mnt/WIN_D/Russ/0000/python00/python3/_projects/qt5_by_example" )
# # sys.path.insert( 1, "/mnt/WIN_D/Russ/0000/python00/python3/_projects/qt5_by_example/info_about_src" )
# #sys.path.insert( 1, "/mnt/WIN_D/Russ/0000/python00/python3/_projects/stuffdb" )
# #sys.path.insert( 1, "/mnt/WIN_D/Russ/0000/python00/python3/_projects/qt_by_example/ex_qt" )
# sys.path.insert( 1, "/mnt/WIN_D/Russ/0000/python00/python3/_projects/rshlib/rshlib_qt/" )
# sys.path.insert( 1, "/mnt/WIN_D/Russ/0000/python00/python3/_projects/rshlib/" )
# sys.path.insert( 1, "/mnt/WIN_D/Russ/0000/python00/python3/_examples/" )
# #sys.path.insert( 1, "/mnt/WIN_D/Russ/0000/python00/python3/_examples/qt" )
# #sys.path.insert( 1, "/mnt/WIN_D/Russ/0000/python00/python3/_projects/stuffdb")
# sys.path.insert( 1, "/mnt/WIN_D/Russ/0000/python00/python3/_projects/stuffdb")
# #rom    app_global import AppGlobal

print( "your path has been adjusted for theProf Mint "
       "\n    from /mnt/WIN_D/Russ/0000/python00/python3/_projects/stuffdb/adjust_path.py" )

# print( "    path now:" )
# for i_path in sys.path:
#     print( "        ", i_path )