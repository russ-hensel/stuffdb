#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 08:56:37 2025

@author: russ
"""


# ---- tof

# ---- imports

# ---- end imports


import adjust_path
import check_fix


a_db_checker    = check_fix.DbCheck()

a_db_checker.fix_key_word_index(  base_table_name = "help_info",
                                key_word_table_name = "help_key_word" )


print( "and now fix_key_word_index done ")








# ---- eof