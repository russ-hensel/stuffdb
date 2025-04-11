#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 09:05:42 2025

Executing SQL query: query_exec_model query.executedQuery() =
'SELECT   help_info.id,  help_info.title,  help_info.system, help_info.key_words
FROM help_info  \n    INNER JOIN  help_key_word  ON help_info.id = help_key_word.id  \n
WHERE  key_word IN ( "test" )   \n    GROUP BY   help_info.id,  help_info.title,  help_info.system,
help_info.key_words  \n    HAVING  count(*) >= 1  \n     ORDER BY  lower(help_info.title) ASC  '
"""


# ---- tof

# ---- imports
import adjust_path

import  stuff_util_sql as su
import  data_dict

# ---- setup
su.create_connection()
data_dict.build_it()
DB_CONNECTION  = su.DB_CONNECTION
DB             = DB_CONNECTION

table_name   = "stuff"
table_name   = "help_info"
table_name   = "help_key_word"
table_name   = "planting_event"


# ------------ believe this works, will prompt for enter
su.drop_table( DB, table_name )

# ------------ believe this works, fails if table exists?db
su.create_table(   DB, table_name   )




# ---- clean up
DB_CONNECTION.close()
DB_CONNECTION = None

print( "got here, done" )



# ---- eof