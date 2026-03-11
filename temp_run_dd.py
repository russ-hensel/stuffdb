#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 20:18:19 2025

@author: russ
"""


# ---- tof

# ---- imports

# ---- end imports


#-------------------------------

import adjust_path

import data_dict


LOG_LEVEL   = 10   # higher is more


#-------------------------------
data_dict.build_it()
table_name      = "stuff"
#table_name      = "help_info"
table_name      = "photoshow"
table_name      = "people"
table_name      = "planting"
table_name      = "plant"
table_name      = "photo"


a_table     = data_dict.DATA_DICT.get_table( table_name )

# print( a_table.to_build_form( ) )
print( a_table.to_upgrade_self( ) )


# ---- eof