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


# ---- imports


import parameters
import qsql_utils
import data_dict
import key_word_indexer
import stuff_util_sql


# ---- end imports

#temp  = parameters.Parameters()
#print( parameters.PARAMETERS )

#data_dict.build_it()
App              = None
DB_CONNECTION    = None

# #------------
# def create_connection(   ):
#     """
#     Create a SQLite database connection.
#     part of setup always use
#     """
#     global DB_CONNECTION
#     if DB_CONNECTION is not None:
#         DB_CONNECTION.close()
#         DB_CONNECTION    = None  # or delete?

#     db_file_name    = parameters.PARAMETERS.db_file_name
#     print( f"create_connection for {db_file_name}")


#     # if    db_file_name !=  ':memory:':
#     #     # delete for a fresh start
#     #     delete_db_file( db_file_name )

#     # !! may need parameters particurlarry for the db type
#     db              = QSqlDatabase.addDatabase( parameters.PARAMETERS.db_type, db_file_name )
#     db.setDatabaseName( db_file_name )   # is this really the file name

#     # next kills it ?  --- now seems ok may still be issues
#     #self.db         = QSqlDatabase.database( "qt_example_db" )
#     DB_CONNECTION         = db

#     if not db.open():
#         print(f"SampleDB Error: Unable to establish a database connection.{db_file_name}")
#         print(f"may need to change to an absolute path for the db for connect to work {1}")
#         1/0
#         return None
#     return db

# def  end_connection_maybe(   ):
#     global  DB_CONNECTION
#     DB_CONNECTION.close( )
#     DB_CONNECTION = None


def line_out( line ):
    """ """
    print( line )


# ------------
def update_table_key_gen_think_in_sql_util( db, table_name, key_value   ):
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
    line_out( f"{what} {last_error} = " )
    #ia_qt.q_sql_error( query.lastError() )
    db.commit()
    line_out( f"end {what}"  )

#--------------
def create_tablexxx(   db, table_name   ):
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






#-------------------------------
def test_queryxxxx( db, table_name = None ):
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
    line_out( "begin  print_record_count ")

    record_count  = 0
    max_ix        = 100000

    query = QSqlQuery( db )

    sql = f"""
        SELECT COUNT(*) AS executable_count
            FROM {table_name}

            """    # WHERE can_execute = 'Y';

    line_out( sql )

    query_ok   =  qsql_utils.query_exec_error_check( query = query, sql = sql, raise_except = True )

    line_out( "select result" )

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
        line_out(f"record count {field_0 = }   <<<<============== ")
        if ix >= max_ix:
            break

    line_out( f"end   print_record_count  ")

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
    line_out( "begin  check_key_words_for_dups ")
    max_ix        = 10044
    # if table_name == None:
    #     table_name = "stuff"

    query = QSqlQuery( db )

    sql         = f"SxxxELECT * FROM {table_name}"

      #     >> find the dups
    sql    = f""" SELECT id, key_word, COUNT(*) AS count
                FROM {table_name} help_key_word
                GROUP BY id, key_word
                HAVING COUNT(*) > 1; """

    line_out( sql )

    query_ok   =  qsql_utils.query_exec_error_check( query = query, sql = sql, raise_except = True )

    line_out( "select result" )

    ix          = 0
    while query.next():
        ix              += 1
        field_0        = query.value(0)
        field_1        = query.value(1)
        field_2        = query.value(2)
        field_3        = query.value(3)
        field_4        = query.value(4)
        field_5        = query.value(5)   # index past end, no error just get None

        line_out(f"record:{ix} {field_0 = }  {field_1 = }  {field_2 = } {field_3 = } {field_4 = } {field_5 = } ")
        if ix >= max_ix:
            break

# ----------------------------------
def tables_check_key_words_for_dups( db,   ):
    """ """
    table_list   = ["help_key_word", "help_key_word"]
    for i_table in table_list:
        check_key_words_for_dups( db, table_name = i_table )


class DbCheck(   ):

    """set up to run externally  """
    def __init__( self, db ):
        """ """
        #db     = su.create_connection()
        # should be done externally data_dict.build_it()
        self.db     = db

    # -------------------
    def tables_check_key_words_for_dups( self ):
        """ """
        table_list   = ["help_key_word", "help_key_word"]
        for i_table in table_list:
            check_key_words_for_dups( self.db, table_name = i_table )

    # -------------------
    def fetch_duplicate_rows( self, table_name ):

        query = QSqlQuery( self.db )

        # Query to fetch rows where id is duplicated
        sql = f"""
        SELECT * FROM {table_name}
        WHERE id IN (
            SELECT id FROM {table_name}
            GROUP BY id
            HAVING COUNT(id) > 1
        );
        """

        if not query.exec(sql):
            print("Query execution failed:", query.lastError().text())
            return

        # Process results
        print( f"\nDuplicate rows in {table_name}")

        ix   = -1
        while query.next():
            ix   += 1
            row_data = [query.value(i) for i in range(query.record().count())]
            print(f"{ix} row_data = {row_data} " )

    # -------------------------------------
    def tables_fetch_duplicate_rows( self, ):
        table_list   = [ "photo", "stuff", "planting" ]
        for i_table in table_list:
            self.fetch_duplicate_rows( self.db, table_name = i_table )



    def find_missing_ids( self, table_name_a, table_name_b ):
        """ """
        query = QSqlQuery()

        sql = f"""
        SELECT {table_name_a}.id
        FROM {table_name_a}
        LEFT JOIN {table_name_b} ON {table_name_a}.id = {table_name_b}.id
        WHERE {table_name_b}.id IS NULL;
        """

        print( f"sql = {sql}")
        if not query.exec(sql):
            print("Query execution failed:", query.lastError().text())
            return

        missing_ids = []
        while query.next():
            missing_ids.append(query.value(0))  # Get the id from table_a

        if missing_ids:
            print("Missing IDs in table_b:", missing_ids)
        else:
            print("No missing IDs found!")

    # -------------------------
    def find_missing_ids_both_ways( self, table_name_a, table_name_b ):
        """ """
        self.find_missing_ids(   table_name_a, table_name_b )
        self.find_missing_ids(   table_name_b, table_name_a )

    # -------------------------------------
    def tables_find_missing_ids_both_ways( self, ):
        table_list   = [ ("stuff",      "stuff_text" ),
                         ( "people",    "people_text" ), ]


        for i_table_name_a, i_table_name_b in table_list:
             self.find_missing_ids_both_ways( i_table_name_a, i_table_name_b )


    # ------------------------
    def fix_key_word_index( self, *, base_table_name, key_word_table_name ):
        """
        drop a key_word_table_name and then reindex
        relies a lot on key_word_indexer

        fix_key_word_index( base_table_name = "help_info",  key_word_table_name = "help_key_word" )
        """
        warn   = ( "\nkey word field may still be manual and not from data dict check "
                  " +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++" )

        print( warn )
        stuff_util_sql.drop_table(   self.db, table_name = key_word_table_name )
        stuff_util_sql.create_table( self.db, table_name = key_word_table_name )

        a_key_word_indexer    = key_word_indexer.KeyWordIndexer(  self.db,
                                              base_table_name,
                                              key_word_table_name  )

        a_key_word_indexer.loop_thru( )
        stuff_util_sql.end_connection( )

        print( warn )


# ====================================================================

def  do_it_left_over_nomoreuse ():
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

    # ---- .... people
    table_name      = "people"
    #table_name      = "people_text"
    #table_name      = "people_key_word"
    table_name      = "people_phone"

    # ---- .... plant
    # table_name      = "plant"
    # table_name      = "plant_text"
    # table_name      = "plant_key_word"

    #table_name      = "planting"
    #table_name      = "planting_text"
    #table_name      = "planting_key_word"

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
    #table_name      = "photo_subject"
    #table_name      = "photo_in_show"
    # ---- .... stuff
    table_name      = "stuff"
    table_name      = "stuff_key_word"
    # table_name      = "stuff_event"
    #table_name      = "xxx"

    # ---- run command


    # drop_table(   DB_CONNECTION, table_name = table_name )
    # create_table( DB_CONNECTION, table_name = table_name )
    # check_key_words_for_dups( DB_CONNECTION, table_name = table_name )


    #test_query( DB_CONNECTION, table_name = table_name )
    #print_missing_text( DB_CONNECTION, table_name = table_name )
    #print_record_count( DB_CONNECTION, table_name = table_name )
    #add_missing_text( DB_CONNECTION, table_name = table_name )
    #test_query( DB_CONNECTION, table_name = table_name )

    #key_gen_for( DB_CONNECTION, table_name = table_name )
    #insert_key_gen( DB_CONNECTION, table_name  )

    # ---- no table name required
    tables_check_key_words_for_dups( DB_CONNECTION )


    # ---- clean up
    DB_CONNECTION.close()
    #print( "done")

# # --------------------
# if __name__ == "__main__":

#     do_it()


# # --------------------
# if __name__ == "__main__":
#     #----- run the full app
#     import qt_sql_widgets
#     qt_sql_widgets.main()
# # --------------------



# ---- eof