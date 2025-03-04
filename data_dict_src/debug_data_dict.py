#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 11:18:20 2025

@author: russ
"""




#-------------------------------



# ---- tof
import data_dict
#import dict_main
import adjust_path

# ---- imports

# ---- end imports

#-------------------------------

data_dict.build_it()

table_name    = "help_info"

a_table    = data_dict.DATA_DICT.get_table( table_name )

print( str(a_table))

# ---- eof