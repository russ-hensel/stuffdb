#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 23 10:46:12 2025

just run it --- but make sure db setup is right first
"""


# ---- tof

# ---- imports
import  stuff_util_sql as su
import  data_dict
# ---- end imports

#

# ---- setup
su.create_connection( use_temp = True )
        # if use_temp =True it will take the db parmaters from parms_temp
data_dict.build_it()
DB_CONNECTION  = su.DB_CONNECTION
DB             = DB_CONNECTION

table_name   = "help_info"
#table_name   = "help_key_word"

#table_name   = "planting_text"
#table_name   = "planting_event"
#table_name   = "stuff_text"
#table_name   = "stuff_event"
#table_name   = "stuff"


#table_name   = "key_gen"

# ------------ believe this works, will prompt for enter
su.drop_table( DB, table_name )

# ------------ believe this works, fails if table exists?db
su.create_table(   DB, table_name   )

# ---- the helps or notes
# ---- table_name   = "help_info"
table_name   = "help_info"
su.drop_table( DB, table_name )
su.create_table(   DB, table_name   )

# ---- table_name   = "help_text"
table_name   = "help_text"
su.drop_table( DB, table_name )
su.create_table(   DB, table_name   )

# ---- table_name   = "help_key_word"
table_name   = "help_key_word"
su.drop_table( DB, table_name )
su.create_table(   DB, table_name   )


# ---- clean up
DB_CONNECTION.close()
DB_CONNECTION = None



# ---- eof