#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 17:41:10 2025

@author: russ
"""


# ---- tof


# ---- imports
import adjust_path
# ---- begin pyqt from import_qt.py

from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel



# # ----QtWidgets big
from PyQt5.QtWidgets import (
    QAction,
    QMenu,
    QApplication,
    QMainWindow,
    QTableView,
    QFrame,
    QMainWindow,
    QMdiArea,
    QMdiSubWindow,
    QMdiArea,
    QMdiSubWindow,
    )



# ---- QtSqlimport pprint
# import sqlite3



import parameters

temp  = parameters.Parameters()
print( parameters.PARAMETERS )


App              = None
DB_CONNECTION    = None

# ---- imports
import qsql_utils
import data_dict



# ---- end imports

#------------
def create_connection(   ):
    """
    Create a SQLite database connection.
    part of setup always use
    """
    global DB_CONNECTION
    if DB_CONNECTION is not None:
        DB_CONNECTION.close()
        DB_CONNECTION    = None  # or delete?

    db_file_name    = parameters.PARAMETERS.db_file_name
    print( f"create_connection for {db_file_name}")


    # if    db_file_name !=  ':memory:':
    #     # delete for a fresh start
    #     delete_db_file( db_file_name )

    # !! may need parameters particurlarry for the db type
    db              = QSqlDatabase.addDatabase( parameters.PARAMETERS.db_type, db_file_name )
    db.setDatabaseName( db_file_name )   # is this really the file name

    # next kills it ?  --- now seems ok may still be issues
    #self.db         = QSqlDatabase.database( "qt_example_db" )
    DB_CONNECTION         = db

    if not db.open():
        print(f"SampleDB Error: Unable to establish a database connection.{db_file_name}")
        1/0
        return None
    return db

# ---- =============================================


#--------------
#def drop_table(   db, table_name   ):
    """
    what it says
    """
    1/0 # !! write this

def create_db( db, table_name_list  ):
    """
    what it says
    """
    for i_table_name in table_name_list:
        create_table(   db, i_table_name   )

    1/0 # finish me

# ----------------------------------
def key_gen_for( db, table_name ):
    """
    what it says
    way more stuff than needed
    return count for table name
    """
    print( f"begin  key_gen_for {table_name}")

    record_count  = 0
    max_ix        = 100000

    query = QSqlQuery( DB_CONNECTION )

    sql = f"""
        SELECT COUNT(*) AS executable_count
            FROM "key_gen"
            WHERE table_name = "{table_name}"
            """    # WHERE can_execute = 'Y';

    print( sql )

    query_ok   =  qsql_utils.query_exec_error_check( query = query, sql = sql, raise_except = True )

    print( "select result" )

    ix          = 0
    while query.next():
        ix              += 1
        field_0        = query.value(0)
        field_1        = query.value(1)
        field_2        = query.value(2)
        field_3        = query.value(3)
        field_4        = query.value(4)
        field_5        = query.value(5)   # index past end, no error just get None

        #print(f"record:{ix} {field_0 = }  {field_1 = }  {field_2 = } {field_3 = } {field_4 = } {field_5 = } ")
        print(f"record count {field_0 = }   <<<<============== ")
        if ix >= max_ix:
            break

    print( f"end   key_gen_for return {field_0} ")
    return field_0


# -----------------------------
def insert_key_gen( db, table_name   ):
    """
    table name is ignored
    junk in code left over but should work
    stuff_util_sql.insert_key_gen( db, table_name   )
    """
    what            = "insert_key_gen"
    print( f"begin {what}")

    # firs make sure key is not present
    records    = key_gen_for( db, table_name )
    if records:
        print( f"key_gen for {table_name} already exists")
        return

    query           = QSqlQuery( db )
    begin_sql       = ( 'INSERT INTO key_gen (  '
                                 'table_name,   key_value )  ' )
    queries = [
       #( f'{begin_sql} VALUES (  "planting",      6060        )' ),
       # ( f'{begin_sql} VALUES (  "people",        7000        )' ),
       ( f'{begin_sql} VALUES (  "{table_name}",        8000     )' ),

    ]

    for sql in queries:
        print( sql )
        if not query.exec_(sql):
            print(f"Query failed: {query.lastError().text()}")
            print(f"Query was: {sql}")
            print(  query.lastError() )
            1/0

    print( f"end {what}")



# -----------------------------
def insert_key_gen_init( db, table_name   ):
    """
    may not want to use this as a lot of hardcode
    table name is ignored
    lots of inserts into the key gen table
    sql is in two parts

    """

    what            = "insert_key_gen_init"
    print( f"begin {what}")

    query           = QSqlQuery( db )
    begin_sql       = ( 'INSERT INTO key_gen (  '
                                 'table_name,   key_value )  ' )
    queries = [
       #( f'{begin_sql} VALUES (  "planting",      6060        )' ),
       # ( f'{begin_sql} VALUES (  "people",        7000        )' ),
       ( f'{begin_sql} VALUES (  "help_info",        8000     )' ),
       ( f'{begin_sql} VALUES (  "picture",        9000     )' ),
    ]

    for sql in queries:
        print( sql )
        if not query.exec_(sql):
            print(f"Query failed: {query.lastError().text()}")
            print(f"Query was: {sql}")
            print(  query.lastError() )
            1/0

    print( f"end {what}")

# ------------
def update_table_key_gen( db, table_name, key_value   ):
    """
    what it says
        not tested yet  --- ready to test

    """
    what   =  "update_table_key_gen"
    print( f"begin {what}"  )

    query           = QSqlQuery( db )
    # query.exec("""
    # UPDATE key_gen
    #     SET key_value = 5000
    #     WHERE   table_name = "stuff";
    #     """ )

    query.exec( f"""
    UPDATE key_gen
        SET key_value = {key_value}
        WHERE   table_name = "{table_name}";
        """ )

    # query.exec("""
    # UPDATE key_gen
    #     SET key_value = 60060
    #     WHERE   table_name = "planting_event";
    #     """ )

    last_error    = query.lastError()
    print( f"{what} {last_error} = " )
    #ia_qt.q_sql_error( query.lastError() )
    db.commit()
    print( f"end {what}"  )

#--------------
def create_table(   db, table_name   ):
    """
    what it says
    """
    print( f"db_create create_table: {table_name}")

    query       = QSqlQuery( db )

    a_table     = data_dict.DATA_DICT.get_table( table_name )

    sql         = a_table.to_sql_create()
    msg         = f"{sql} "
    print( msg )


    query_ok   =  qsql_utils.query_exec_error_check( query = query, sql = sql, raise_except = True )

    print( "table created, check it " )
    db.commit()

    print( "create_table done")


#--------------
# def delete_table( db, table_name ):
def drop_table(   db, table_name   ):
    """
    delete or drop a table
    """
    query       = QSqlQuery( db )

    sql         = f"DROP TABLE IF EXISTS {table_name}"
    print( sql )

    user_input = input( "Enter something to continue: ")

    query.prepare( sql )

    query_ok    =  qsql_utils.query_exec_error_check( query = query, sql = sql, raise_except = True )


    db.commit()

    print( "delete_table done")



    # -------------------------------------

    # db.transaction()
    # query = QSqlQuery( db )

    # query.exec( sql )

    # last_error    = query.lastError ()
    # print( f"create_table_help {last_error} = " )
    # # ia_qt.q_sql_error( last_error,
    # #                    msg          =  "now in code at: create_table ",
    # #                    print_it     = True,
    # #                    include_dir  = False,    # default False
    # #                    )
    # db.commit()

    # print( "create_table done")


#-------------------------------
def test_query( db, table_name = None ):
    """
    use to test just to see if things are working

    """
    max_ix        = 10
    if table_name == None:
        100/0
        table_name = "stuff"

    query = QSqlQuery( DB_CONNECTION )

    sql         = f"SELECT * FROM {table_name}"
    print( sql )

    query_ok   =  qsql_utils.query_exec_error_check( query = query, sql = sql, raise_except = True )

    print( "select result" )

    ix          = 0
    while query.next():
        ix              += 1
        field_0        = query.value(0)
        field_1        = query.value(1)
        field_2        = query.value(2)
        field_3        = query.value(3)
        field_4        = query.value(4)
        field_5        = query.value(5)   # index past end, no error just get None

        print(f"record:{ix} {field_0 = }  {field_1 = }  {field_2 = } {field_3 = } {field_4 = } {field_5 = } ")
        if ix >= max_ix:
            break

# ----------------------------------
def print_record_count( db, table_name ):
    """
    what it says
    will only return one record
    """
    print( "begin  print_record_count ")

    record_count  = 0
    max_ix        = 100000

    query = QSqlQuery( db )

    sql = f"""
        SELECT COUNT(*) AS executable_count
            FROM {table_name}

            """    # WHERE can_execute = 'Y';

    print( sql )

    query_ok   =  qsql_utils.query_exec_error_check( query = query, sql = sql, raise_except = True )

    print( "select result" )

    ix          = 0
    while query.next():
        ix              += 1
        field_0        = query.value(0)
        field_1        = query.value(1)
        field_2        = query.value(2)
        field_3        = query.value(3)
        field_4        = query.value(4)
        field_5        = query.value(5)   # index past end, no error just get None

        #print(f"record:{ix} {field_0 = }  {field_1 = }  {field_2 = } {field_3 = } {field_4 = } {field_5 = } ")
        print(f"record count {field_0 = }   <<<<============== ")
        if ix >= max_ix:
            break

    print( f"end   print_record_count  ")

# ----------------------------------
def add_missing_text( db, table_name ):
    """
    what it says
        fix up db on temp basis
    """
    chat = """
    i hava a table defined by
            CREATE TABLE help_info  (
            id  INTEGER,
            type  VARCHAR(15),
            can_execute  VARCHAR(1) )

    and another defined by

        CREATE TABLE help_text  (
            id  INTEGER,
            text_data  TEXT )

    I would like to find add text_data = "no text data for now"
    to all the records missing in the help_text table.

    Can you give me the sql for sqllite ?

    """
    if  table_name == "stuff":
        sql = """
            INSERT INTO stuff_text (id, text_data)
            SELECT id, 'no text data for now \in this stuff'
            FROM stuff
            WHERE id NOT IN (SELECT id FROM stuff_text);

            """

    elif  table_name == "help_info":

        sql  =  """
            INSERT INTO help_text (id, text_data)
            SELECT id, 'no text data for now'
            FROM help_info
            WHERE id NOT IN (SELECT id FROM help_text);
            """


    elif  table_name in [ "people", "people_text" ] :

        sql  =  """
            INSERT INTO people_text (id, text_data)
            SELECT id, 'no text data for now\nfor people this is a default'
            FROM people
            WHERE id NOT IN (SELECT id FROM people_text);
            """

    elif  table_name == "planzzzzzzt":
        # sql = """
        #     SELECT stuff.*
        #     FROM stuff
        #     LEFT JOIN stuff_text  ON stuff.id = stuff_text.id
        #     WHERE stuff_text.id IS NULL;
        #     """
        sql = """
            SELECT plant.*
            FROM plant
            LEFT JOIN plant_text ON plant.id = plant_text.id
            WHERE plant_text.id IS NULL; """


    else:
        # no sql for that
        1/0



    print( sql )

    record_count  = 0
    max_ix        = 100000

    query = QSqlQuery( DB_CONNECTION )


    query_ok   =  qsql_utils.query_exec_error_check( query = query, sql = sql, raise_except = True )

    print( "sql done" )

# ----------------------------------
def print_missing_text( db, table_name ):
    """
    what it says
    """
    print( "begin  print_missing_help_text ")


    chat = """
    i hava a table defined by
            CREATE TABLE help_info  (
            id  INTEGER,
            type  VARCHAR(15),
            can_execute  VARCHAR(1) )

    and another defined by

        CREATE TABLE help_text  (
            id  INTEGER,
            text_data  TEXT )

    I would like to find all the records in help_info

    where there is no corresponding record in help_text

    can you give me a query that will list these records?

    """


    if  table_name == "help_info":
        sql = """
            SELECT help_info.*
            FROM help_info
            LEFT JOIN help_text  ON help_info.id = help_text.id
            WHERE help_text.id IS NULL;
            """

    elif  table_name == "stuff":
        sql = """
            SELECT stuff.*
            FROM stuff
            LEFT JOIN stuff_text  ON stuff.id = stuff_text.id
            WHERE stuff_text.id IS NULL;
            """
        sql = """
            SELECT stuff.*
            FROM stuff
            LEFT JOIN stuff_text ON stuff.id = stuff_text.id
            WHERE stuff_text.id IS NULL; """

    elif  table_name == "plant":
        # sql = """
        #     SELECT stuff.*
        #     FROM stuff
        #     LEFT JOIN stuff_text  ON stuff.id = stuff_text.id
        #     WHERE stuff_text.id IS NULL;
        #     """
        sql = """
            SELECT plant.*
            FROM plant
            LEFT JOIN plant_text ON plant.id = plant_text.id
            WHERE plant_text.id IS NULL; """


    else:
        # no sql for that
        1/0

    print( sql )

    record_count  = 0
    max_ix        = 100000

    query = QSqlQuery( DB_CONNECTION )

    query_ok   =  qsql_utils.query_exec_error_check( query = query, sql = sql, raise_except = True )

    print( "select result" )

    ix          = 0
    while query.next():
        ix              += 1
        field_0        = query.value(0)
        field_1        = query.value(1)
        field_2        = query.value(2)
        field_3        = query.value(3)
        field_4        = query.value(4)
        field_5        = query.value(5)   # index past end, no error just get None

        print(f"record:{ix} {field_0 = }  {field_1 = }  {field_2 = } {field_3 = } {field_4 = } {field_5 = } ")
        if ix >= max_ix:
            break

    print( f"end   print_missing_help_text {ix = }")

# ----------------------------------
def check_key_words_for_dups( db, table_name ):
    """
    what it says
    """
    print( "begin  check_key_words_for_dups ")
    max_ix        = 10044
    if table_name == None:
        table_name = "stuff"

    query = QSqlQuery( DB_CONNECTION )

    sql         = f"SxxxELECT * FROM {table_name}"

      #     >> find the dups
    sql    = f""" SELECT id, key_word, COUNT(*) AS count
                FROM {table_name} help_key_word
                GROUP BY id, key_word
                HAVING COUNT(*) > 1; """

    print( sql )

    query_ok   =  qsql_utils.query_exec_error_check( query = query, sql = sql, raise_except = True )

    print( "select result" )

    ix          = 0
    while query.next():
        ix              += 1
        field_0        = query.value(0)
        field_1        = query.value(1)
        field_2        = query.value(2)
        field_3        = query.value(3)
        field_4        = query.value(4)
        field_5        = query.value(5)   # index past end, no error just get None

        print(f"record:{ix} {field_0 = }  {field_1 = }  {field_2 = } {field_3 = } {field_4 = } {field_5 = } ")
        if ix >= max_ix:
            break



# ====================================================================

def  do_it():
    # ---- run from here =====================================
    create_connection()
    data_dict.build_it()
    app                 = QApplication( [] )
    qsql_utils.APP      = app

    # ---- table_name

    # table_name    = "help_info"
    #table_name    = "help_key_word"
    #table_name    = "help_text"

    #table_name    = "key_gen"

    # table_name      = "plant"

    # table_name      = "people"
    # table_name      = "people_text"
    #table_name       = "persons"   # for qt by example

    #table_name      = "photo"
    #table_name      = "photo_text"     # not in old stuff may not use
    #table_name      = "photo_key_word"


    # table_name      = "photo_subject"
    # table_name      = "photo_in_show"


    #table_name      = "photoshow"
    #table_name      = "photoshow_key_word"
    # table_name      = "photo_text"     # not yet

    #table_name      = "stuff"
    table_name      = "stuff_key_word"

    #table_name      = "xxx"

    # ---- run command


    # drop_table(   DB_CONNECTION, table_name = table_name )
    # create_table( DB_CONNECTION, table_name = table_name )



    #test_query( DB_CONNECTION, table_name = table_name )
    #print_missing_text( DB_CONNECTION, table_name = table_name )
    #print_record_count( DB_CONNECTION, table_name = table_name )
    #add_missing_text( DB_CONNECTION, table_name = table_name )
    #test_query( DB_CONNECTION, table_name = table_name )
    drop_table( DB_CONNECTION, table_name = table_name )
    create_table( DB_CONNECTION, table_name = table_name )
    #key_gen_for( DB_CONNECTION, table_name = table_name )
    #insert_key_gen( DB_CONNECTION, table_name  )

    # ========================== beware ==============================

    # table_name_list     = [ "help_ifno", "help_text", "help_key_words" ]
    # create_db ---- not finished

    # ---- clean up
    DB_CONNECTION.close()
    #print( "done")

# --------------------
if __name__ == "__main__":

    do_it()


# # --------------------
# if __name__ == "__main__":
#     #----- run the full app
#     import qt_sql_widgets
#     qt_sql_widgets.main()
# # --------------------



# ---- eof