#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 06:52:49 2025

@author: russ



/mnt/WIN_D/temp_photo/02/Dcp_0778.jpg

SELECT   photo.id,  photo.name,  photo.title,  photo.add_kw, photo.descr    FROM photo

     ORDER BY  dt_enter ASC


SELECT   help_info.id,  help_info.title,  help_info.system, help_info.key_words
      FROM help_info
      ORDER BY  lower(help_info.title) ASC

2025-04-27 09:58:26,149 - DEBUG - Executing SQL query: query_exec_model query.executedQuery() = 'SELECT   help_info.id,  help_info.title,  help_info.system, help_info.key_words    FROM help_info  \n     \n     ORDER BY  lower(help_info.title) ASC  '
2025-04-27 09:58:26,151 - ERROR - Query Execution Error:query_exec_model No query Unable to fetch row
2025-04-27 09:58:26,153 - ERROR - ( SELECT   help_info.id,  help_info.title,  help_info.system, help_info.key_words    FROM help_info

     ORDER BY  lower(help_info.title) ASC
[<data_dict.ColumnDict object at 0x7f409c78a4b0>, <data_dict.ColumnDict object at 0x7f409c78a720>, <data_dict.ColumnDict object at 0x7f409c78a600>, <data_dict.ColumnDict object at 0x7f409c78a630>]
2025-04-27 09:58:26,158 - DEBUG - Executing SQL query: query_exec_model query.executedQuery() = 'SELECT   help_info.id,  help_info.title,  help_info.system, help_info.key_words    FROM help_info  \n     \n     ORDER BY  lower(help_info.title) ASC  '
2025-04-27 09:58:26,161 - ERROR - Query Execution Error:query_exec_model No query Unable to fetch row

2025-04-27 09:58:26,151 - ERROR - Query Execution Error:query_exec_model No query Unable to fetch row
2025-04-27 09:58:26,153 - ERROR - ( SELECT   help_info.id,  help_info.title,  help_info.system, help_info.key_words    FROM help_info

     ORDER BY  lower(help_info.title) ASC

/mnt/WIN_D/temp_photo/00/00july_28.jpg


this works but no results shown
 SELECT   photo.id,  photo.name,  photo.title,  photo.add_kw, photo.descr    FROM photo
    INNER JOIN  photo_key_word  ON photo.id = photo_key_word.id
    WHERE  key_word IN ( "rus" )
    GROUP BY   photo.id,  photo.name,  photo.title,  photo.add_kw, photo.descr
    HAVING  count(*) = 1


SELECT   photo.id,  photo.name,  photo.title,  photo.add_kw, photo.descr    FROM photo
    INNER JOIN  photo_key_word  ON photo.id = photo_key_word.id
    WHERE  key_word IN ( "rus" )
    GROUP BY   photo.id,  photo.name,  photo.title,  photo.add_kw, photo.descr
    HAVING  count(*) = 1
     ORDER BY  id ASC


next not working no error
!continue
2025-04-27 12:31:51,335 - ERROR - Query Execution Error:query_exec_model No query Unable to fetch row
2025-04-27 12:31:51,340 - ERROR - (

    SELECT   photo.id,  photo.name,  photo.title,  photo.add_kw, photo.descr
        FROM photo
    INNER JOIN  photo_key_word
        ON photo.id = photo_key_word.id
    WHERE  key_word IN ( "rus" )
    GROUP BY   photo.id,  photo.name,  photo.title,  photo.add_kw, photo.descr
    HAVING  count(*) = 1
     ORDER BY  id ASC


2025-04-27 12:31:51,344 - DEBUG - StuffTextTab_criteria_select   query.executedQuery() = 'SELECT   photo.id,  photo.name,  photo.title,  photo.add_kw, photo.descr    FROM photo  \n    INNER JOIN  photo_key_word  ON photo.id = photo_key_word.id  \n    WHERE  key_word IN ( "rus" )   \n    GROUP BY   photo.id,  photo.name,  photo.title,  photo.add_kw, photo.descr  \n    HAVING  count(*) = 1  \n     ORDER BY  id ASC  '

from help
 'SELECT   help_info.id,  help_info.title,  help_info.system,   help_info.key_words
     FROM help_info
 INNER JOIN  help_key_word
     ON help_info.id = help_key_word.id
 WHERE  key_word IN ( "rus" )
 GROUP BY   help_info.id,  help_info.title,  help_info.system, help_info.key_words
 HAVING  count(*) >= 1
 ORDER BY  lower(help_info.title) ASC  '




"""


# ---- tof

# ---- imports

# ---- end imports
# >>Py -------- import the database ---- make sure correct db at top of file
# how to do the adjust path??
# import adjust_path
# import sys

# for i_path in sys.path:
#     print( i_path )

# import  misc_helpers

#misc_helpers.insert_if_missing( "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/import_old_sfuff/photo" )


# import adjust_path
# import check_fix
# import stuff_util_sql   as su
# import data_dict

# >>Py ------------ fix up key gen, count records, get max ------------



#>>Py -------- create the tables --------  beware of use_temp --- then go set up key gen
import adjust_path
import check_fix
import stuff_util_sql   as su
import data_dict


db                       = su.create_connection( use_temp = True )
a_db_checker    = check_fix.DbCheck( db )    # just an object create does not really do anything

# next should actually fix the key word index table -- will it create it --- probably not

table          = "help_info"
kw_table   =  "help_key_word"

table          = "photo"
table          = "photoshow"


kw_table   =  table + "_key_word"

a_db_checker.fix_key_word_index(  base_table_name = table,    key_word_table_name = kw_table )


print( "done ")

