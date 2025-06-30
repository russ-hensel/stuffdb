

import    adjust_path

import  data_dict


table_name      = "stuff_event"
table_name      = "photo_subject"
table_name      = "photo_subject"
table_name      = "photo_subject"
table_name      = "people"
table_name      = "people_phone"

data_dict.build_it()
a_table          = data_dict.DATA_DICT.get_table( table_name )

msg       = "did your uncomment something"
msg        = a_table.to_sql_create()
msg        = a_table.sql_to_insert_bind()
#msg        = a_table.sql_to_insert_bind()
msg        = a_table.splits_to_bind()

print( msg )



#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 11:58:42 2025

@author: russ
"""


# ---- tof

# ---- imports

# ---- end imports


#-------------------------------






# ---- eof



Query was: INSERT INTO    help_info (
               id,
               id_old,
               type,
               sub_system,
               system,
               key_words,
               add_ts,
               edit_ts,
               table_name,
               column_name,
               java_type,
               java_name,
               java_package,
               title,
               is_example,
               can_execute )
                VALUES (
               :id,
               :id_old,
               :type,
               :sub_system,
               :system,
               :key_words,
               :add_ts,
               :edit_ts,
               :table_name,
               :column_name,
               :java_type,
               :java_name,
               :java_package,
               :title,
               :is_example,
               :can_execute )



1 id,
2                id_old,
3                type,
4                sub_system,
5                system,
6                key_words,
7                add_ts,
8                edit_ts,
9                table_name,
10                column_name,
11                java_type,
12                java_name,
13                java_package,
14                title,
15                is_example,
16                can_execute )

1 :id,
2                :id_old,
3                :type,
4                :sub_system,
5                :system,
6                :key_words,
7                :add_ts,
8                :edit_ts,
9                :table_name,
10                :column_name,
11                :java_type,
12                :java_name,
13                :java_package,
14                :title,
15                :is_example,
16                :can_execute )

 1            id_old           = splits[0].strip( "'" )
2             id               = ix_line + KEY_OFFSET             #id_old           = splits[0]
3             a_type           = no_quotes( splits[1] )  # column name is tpe
4             sub_system       = no_quotes( splits[2] )
5             system           = no_quotes( splits[3] )
6             key_words        = no_quotes( splits[4] )
7             add_ts           = string_to_timestamp( splits[5] )
8             edit_ts          = string_to_timestamp( splits[6] )
9             table_name       = no_quotes( splits[7] )
10             column_name      = no_quotes( splits[8] )
11             java_type        = no_quotes( splits[9] )
12             java_name        = no_quotes( splits[10] )
13             java_package     = no_quotes( splits[11] )
14             title            = no_quotes( splits[12] )
15             is_example       = no_quotes( splits[13] )
16             can_execute      = no_quotes( splits[14] )


1             query.bindValue( ":id_old",         id_old  )
2             query.bindValue( ":id",             id   )
3             query.bindValue( ":type",           a_type   )
4             query.bindValue( ":sub_system",     sub_system   )
5             query.bindValue( ":system",         system   )
6             query.bindValue( ":key_words",      key_words   )
7             query.bindValue( ":add_ts",         add_ts   )
8             query.bindValue( ":edit_ts",        edit_ts   )
9             query.bindValue( ":table_name",     table_name   )
10             query.bindValue( ":column_name",    column_name   )
11             query.bindValue( ":java_type",      java_type   )
12             query.bindValue( ":java_name",      java_name   )
13             query.bindValue( ":java_package",   java_package   )
14             query.bindValue( ":title",          title   )
15             query.bindValue( ":is_example",     is_example   )
16             query.bindValue( ":can_execute",    can_execute   )


I have modified it a bit to:

   for ix_line, i_line in enumerate( file_src ) :

       i_line_issue     = i_line
       ix_line_issue    = ix_line
       try:
           print( f"importing line >>>>>{ix_line}")
           i_line           = i_line.rstrip('\n')

           splits           = i_line.split( ","   )
           #rint( f"{len(splits) = }")

           # we should get n splits
           if len( splits ) != MAX_SPLITS:
               raise Exception( f"wrong len of splits {len( splits ) = }  {MAX_SPLITS = }")

           id_old           = splits[0].strip( "'" )
           a_id               = ix_line + KEY_OFFSET
           #id_old           = splits[0]
           a_type           = no_quotes( splits[1] )  # column name is tpe
           sub_system       = no_quotes( splits[2] )
           system           = no_quotes( splits[3] )
           key_words        = no_quotes( splits[4] )
           add_ts           = string_to_timestamp( splits[5] )
           edit_ts          = string_to_timestamp( splits[6] )
           table_name       = no_quotes( splits[7] )
           column_name      = no_quotes( splits[8] )
           java_type        = no_quotes( splits[9] )
           java_name        = no_quotes( splits[10] )
           java_package     = no_quotes( splits[11] )
           title            = no_quotes( splits[12] )
           is_example       = no_quotes( splits[13] )
           can_execute      = no_quotes( splits[14] )

           #data        = splits[1].strip( "'" )
           #pprint.pprint( splits )

           print( f">>>>>{type}<   >{sub_system}<   >{system}< >{add_ts}<>{table_name}<>{column_name}" )

           # #data        = data.encode().decode('unicode_escape')
           # #print( f"\n\n\nreading/inserting line no {ix_line} =  \n{id_old} \n{data}"

           query = QSqlQuery( db_create.DB_CONNECTION )

           sql        = """INSERT INTO    help_info (
              id,
              id_old,
              type,
              sub_system,
              system,
              key_words,
              add_ts,
              edit_ts,
              table_name,
              column_name,
              java_type,
              java_name,
              java_package,
              title,
              is_example,
              can_execute )
               VALUES (
              :id,
              :id_old,
              :type,
              :sub_system,
              :system,
              :key_words,
              :add_ts,
              :edit_ts,
              :table_name,
              :column_name,
              :java_type,
              :java_name,
              :java_package,
              :title,
              :is_example,
              :can_execute ) """

           query.prepare( sql )

           # query.bindValue( ":ix_line",  ix_line  )
           query.bindValue( ":id_old",         id_old  )
           query.bindValue( ":id",             a_id   )
           query.bindValue( ":type",           a_type   )
           query.bindValue( ":sub_system",     sub_system   )
           query.bindValue( ":system",         system   )
           query.bindValue( ":key_words",      key_words   )
           query.bindValue( ":add_ts",         add_ts   )
           query.bindValue( ":edit_ts",        edit_ts   )
           query.bindValue( ":table_name",     table_name   )
           query.bindValue( ":column_name",    column_name   )
           query.bindValue( ":java_type",      java_type   )
           query.bindValue( ":java_name",      java_name   )
           query.bindValue( ":java_package",   java_package   )
           query.bindValue( ":title",          title   )
           query.bindValue( ":is_example",     is_example   )
           query.bindValue( ":can_execute",    can_execute   )

           # print( f"{sql = }")

           if not query.exec_( ):
               # nice to have logging here
               msg         = f"Query failed (may break or except ): {ix_line = } {query.lastError().text()} "
               print( msg )
               print(f"Query was: {sql}")
               raise Exception( "msg" )  # should be caught and continue

it still fails, the failure is in the sql part not in the rest of the code.

try again to find the error

I have checked the db definition and it seems correct, of course i could be wrong


CREATE TABLE help_info    (
     id  INTEGER,
     id_old  VARCHAR(15),
     type  VARCHAR(15),
     sub_system  VARCHAR(15),
     system  VARCHAR(15),
     key_words  VARCHAR(70),
     add_ts  INTEGER,
     edit_ts  INTEGER,
     table_name  VARCHAR(40),
     column_name  VARCHAR(40),
     java_type  VARCHAR(20),
     java_name  VARCHAR(175),
     java_package  VARCHAR(150),
     title  VARCHAR(150),
     is_example  VARCHAR(1)
    )

1      id  INTEGER,
2      id_old  VARCHAR(15),
3      type  VARCHAR(15),
4      sub_system  VARCHAR(15),
5      system  VARCHAR(15),
6      key_words  VARCHAR(70),
7      add_ts  INTEGER,
8      edit_ts  INTEGER,
9      table_name  VARCHAR(40),
10      column_name  VARCHAR(40),
11      java_type  VARCHAR(20),
12      java_name  VARCHAR(175),
13      java_package  VARCHAR(150),
14      title  VARCHAR(150),
15      is_example  VARCHAR(1)