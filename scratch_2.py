#!/usr/bin/env python3
# -*- coding: utf-8 -*-



 Handling Large .db-wal Files:

    Why large?: Frequent writes or uncommitted transactions can cause growth.
    Fix:
        Run

PRAGMA wal_checkpoint(FULL);
    did on test db size did not change -- do a change


to force a full checkpoint.
        Check for stuck transactions or unclosed connections in your application.
        Vacuum the database (VACUUM;) to optimize if needed.

Deleting .db-wal Files:

    Caution: Do not manually delete .db-wal files while the database is in use, as this can corrupt the database or cause data loss.
    Only delete if:
        All database connections are closed.
        You’re sure no transactions are pending.
        You’ve backed up the database.




1. Check for any remaining connections:

# On Linux/Mac, check if any process is using the database -- add this a linux command ??
lsof your_database.db*

# Or check for SQLite processes  - add this a linux command ??
ps aux | grep sqlite



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



class AClass():

    def __init__( self ):
        pass
        self.x=2
        self.y=3
    def __str__( self ):
        a_str     = " \n".join(  f"{k} = {v!r}"        for         k, v        in self.__dict__.items() )
        return a_str
a_class = AClass()

print( a_class )