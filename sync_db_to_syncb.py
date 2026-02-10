#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  7 09:42:26 2026

@author: russ
"""

from app_global import AppGlobal
from  pathlib import Path

print( AppGlobal.parameters.db_file_name )
print( AppGlobal.parameters.db_lock_file_name )
print( AppGlobal.parameters )
print( AppGlobal.parameters )



from  pathlib import Path
text   = AppGlobal.parameters.db_lock_file_name
print( f"a_python_template { text = }" )
print( AppGlobal.parameters.db_file_name )
print( AppGlobal.parameters.db_lock_file_name )
db_path_name   = Path(  AppGlobal.parameters.db_file_name  )

print( db_path_name )
db_path_name   =  db_path_name.resolve()
print( db_path_name )