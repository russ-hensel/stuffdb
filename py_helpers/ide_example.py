#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

import sys
from platform import python_version

print( sys.prefix )      # the environment's folder

msg     = ( "this is the file idle_example.py" )
print( msg )



print( f"your python version is: {python_version()}"  )
