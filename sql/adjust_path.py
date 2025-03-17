#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 15:34:13 2024

@author: russ


import adjust.path
"""
# ---- imports

import sys
import socket

hostname              = socket.gethostname()

print( f"{hostname = }" )

#         # --- environment does not seem too useful but make sure defined
#         cls.environments       = {"what": "not collected"}
# #        cls.environments        = os.environ     # not sure of type, dict like
# "/mnt/WIN_D/russ/0000/python00/python3"
#         host_name              = socket.gethostname()
#         cls.host_name          = host_name

#         # next has failed on raspberry pi us try until better understood
#         try:
#             cls.host_tcpip         = socket.gethostbyname( host_name )
#         except Exception as a_execpt:
#             # no logger at this point
#             print( f"RunningOn.gatherdata() failed to get hostname {a_execpt}" )
#             cls.host_tcpip         = None

if   hostname == "russ-ThinkPad-P72":
    src_root         = "/mnt/WIN_D/russ/0000/python00/python3"
elif hostname == "russ-ThinkPad-P72":
    src_root         = "/mnt/WIN_D/russ/0000/python00/python3"
else:
    src_root         = "/mnt/WIN_D/russ/0000/python00/python3"

sys.path.insert( 1, f"{src_root}/_projects/rshlib" )
sys.path.insert( 1, f"{src_root}/_projects/rshlib/in_spect" )
sys.path.insert( 1, f"{src_root}/_projects/rshlib/rshlib_qt/" )
sys.path.insert( 1, f"{src_root}/_projects/rshlib/app_services/" )

sys.path.insert( 1, f"{src_root}/_projects/stuffdb" )


sys.path.insert( 1, f"{src_root}/_projects/stuffdb/data_dict_src" )


print( "your path has been adjusted for theProf Mint from ...stuffdb/sql" )
print( "=================================================================================== ")

print( "your path has been adjusted for theProf Mint "
       "\n     ...sql" )

if False:
    print( "    path now:" )
    for i_path in sys.path:
        print( "        ", i_path )