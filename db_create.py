#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 08:38:46 2024

@author: russ


import db_create
db_create.create_table_stuff( db )
/mnt/WIN_D/Russ/0000/python00/python3/_projects/stuff_db_qt/db_create.py

see in backup
      /mnt/WIN_D/Russ/0000/python00/python3/_projects/stuff_db_qt/stuffdb_def.py


In process of modifying to use externally and call from other contexts

import db_create
    db_create.create_connection()
    #   db-create.DB_CONNECTION

"""

# ---- to main

# # --------------------
# if __name__ == "__main__":
#     import main
#     main.main()
# # --------------------

# ---- imports


import sqlite3

import ex_helpers
#import ia_qt
# ---- QtCore
from PyQt5.QtCore import QDate, QModelIndex, Qt, QTimer, pyqtSlot
from PyQt5.QtGui import QIntValidator, QStandardItem, QStandardItemModel
# ---- QtSql
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
# ----QtWidgets Boxs, Dialogs
# ----QtWidgets layouts
# ----QtWidgets big
# ----QtWidgets
from PyQt5.QtWidgets import (QAction,
                             QActionGroup,
                             QApplication,
                             QButtonGroup,
                             QCheckBox,
                             QComboBox,
                             QDateEdit,
                             QDockWidget,
                             QFileDialog,
                             QFrame,
                             QGridLayout,
                             QHBoxLayout,
                             QInputDialog,
                             QLabel,
                             QLineEdit,
                             QListWidget,
                             QMainWindow,
                             QMdiArea,
                             QMdiSubWindow,
                             QMenu,
                             QMessageBox,
                             QPushButton,
                             QSpinBox,
                             QTableView,
                             QTableWidget,
                             QTableWidgetItem,
                             QTabWidget,
                             QTextEdit,
                             QVBoxLayout,
                             QWidget)

import adjust_path
import code_gen
import data_dict

# ---- begin pyqt from import_qt.py












DB_CONNECTION    = None

DB_FILE_NAME     = "./data/appdb.db"  # normally used for run manual
DB_FILE_NAME     = "/tmp/ramdisk/sept_26.db"



print( DB_FILE_NAME )



# ---- general purpose -------------------------------------
def create_connection( db_fn = None ):
    """
    shoudl only be called on manual run
    Returns:
        TYPE: DESCRIPTION.

    """
    global  DB_CONNECTION

    if db_fn is None:
        db_fn = DB_FILE_NAME
    print( f"using {db_fn =}" )

    db = QSqlDatabase.addDatabase("QSQLITE")  # or another appropriate database driver
    db.setDatabaseName(db_fn )

    if not db.open():
        print("Unable to open database")
        1/0
        return False
    DB_CONNECTION   = db
    return db

#--------------
def execute_sql( msg = None, db = None, sql = None  ):
    """
    what it says

    """
    print( f"execute_sql: {msg} \n    {sql}")
    db.transaction()
    query = QSqlQuery( db )

    query.exec( sql )

    last_error    = query.lastError ()
    print( f"create_table_help {last_error} = " )
    ia_qt.q_sql_error( last_error,
                       msg =  "now in code at: execute_sql ",
                       print_it = True,
                       include_dir = False,    # default False
                       )
    db.commit()

    print( "execute_sql done")


#--------------
def create_table( msg = None, db = None, sql = None  ):
    """
    what it says

    """
    print( f"db_create create_table: {msg}")
    db.transaction()
    query = QSqlQuery( db )

    query.exec( sql )

    last_error    = query.lastError ()
    print( f"create_table_help {last_error} = " )
    ia_qt.q_sql_error( last_error,
                       msg          =  "now in code at: create_table ",
                       print_it     = True,
                       include_dir  = False,    # default False
                       )
    db.commit()

    print( "create_table done")

#--------------------------------
def querry_ok( what, query, db ):
    """

    Args:
        what (TYPE): DESCRIPTION.
        query (TYPE): DESCRIPTION.
        db (TYPE): DESCRIPTION.

    Returns:
        None.

    """
    if query.lastError().isValid():
        ok = False
        print("Error:", query.lastError().text())
        ia_qt.q_sql_error( query.lastError() )
    else:
        ok = False
        print("Table created successfully")

    db.commit()

    print(  f"{what} table created??" )
    return ok

#--------------
def delete_table( db, table_name ):
    """
    """
    query = QSqlQuery( db )
    query.prepare( f"DROP TABLE IF EXISTS {table_name}" )

    # Execute the query
    if not query.exec_():
        print( f"Error dropping table {table_name}:", query.lastError().text())
    else:
        print( f"Table {table_name} dropped successfully!")


#----------------------------------
def drop_table_by_name(  db_file_name, table_name   ):
    ex_name  = "drop_table"
    print( f"{ex_helpers.begin_example( ex_name )}"
            "\n    "
    )
    """
    db_create.drop_table_by_name(  db_file_name, table_name   )
    """

    global DB_FILE_NAME
    DB_FILE_NAME  = db_file_name
    create_connection(  )


    #sql         = data_dict.sql_dict[ TABLE_NAME ]

    sql          = f"DROP TABLE IF EXISTS {table_name}"

    msg   = "a message"
    execute_sql( msg = msg , db =  DB_CONNECTION, sql = sql  )

    ex_helpers.end_example( ex_name )



# ---- key gen -------------------------------------
def create_table_key_genxxx( db ):
    """
    """
    msg   = "create_table_key_gen"
    sql    = """
        CREATE TABLE IF NOT EXISTS key_gen (
            table_name VARCHAR(30) PRIMARY KEY UNIQUE NOT NULL,
            key_value INTEGER
        )
    """

    create_table( msg = None, db = db, sql = sql  )

# # ---- key gen
# def create_table_key_gen( db ):
#     """
#     """
#     query = QSqlQuery()
#     # Create the key_gen table if it doesn't exist
#     query.exec("""
#         CREATE TABLE IF NOT EXISTS key_gen (
#             table_name VARCHAR(30) PRIMARY KEY UNIQUE NOT NULL,
#             key_value INTEGER
#         )
#     """)


# # -----------------------------
# def insert_key_gen( db, table_name, key_value  ):
#     """ """

#     what    = "insert_key_gen"
#     print( f"begin {what}")

#     sql     = ( 'INSERT INTO key_gen (  '
#                                  f'{table_name},   {key_value} )  ' )
#     queries = [
#        #( f'{begin_sql} VALUES (  "planting",      6060        )' ),
#        ( f'{begin_sql} VALUES (  "people",        7000        )' ),



# -----------------------------
def insert_key_gen( db  ):
    """ """

    what    = "insert_key_gen"
    print( f"begin {what}")
    query = QSqlQuery()
    begin_sql     = ( 'INSERT INTO key_gen (  '
                                 'table_name,   key_value )  ' )
    queries = [
       #( f'{begin_sql} VALUES (  "planting",      6060        )' ),
       ( f'{begin_sql} VALUES (  "people",        7000        )' ),

    ]

    for sql in queries:
        print( sql )
        if not query.exec_(sql):
            print(f"Query failed: {query.lastError().text()}")
            print(f"Query was: {sql}")
            ia_qt.q_sql_error( query.lastError() )

    print( f"end {what}")

# ------------
def update_table_key_gen( db ):
    """
    what it says


    """
    what   =  "update_table_key_gen"
    print( f"begin {what}"  )
    db.transaction()
    query = QSqlQuery( db )

    # query.exec("""
    # UPDATE key_gen
    #     SET key_value = 5000
    #     WHERE   table_name = "stuff";
    #     """ )

    query.exec("""
    UPDATE key_gen
        SET key_value = 6060
        WHERE   table_name = "planting";
        """ )

    # query.exec("""
    # UPDATE key_gen
    #     SET key_value = 60060
    #     WHERE   table_name = "planting_event";
    #     """ )

    last_error    = query.lastError()
    print( f"{what} {last_error} = " )
    ia_qt.q_sql_error( query.lastError() )
    db.commit()
    print( f"end {what}"  )


#--------------


#--------------
def delete_table_help_key_word( db ):
    # Prepare the SQL command to drop a table
    table_name     = "help_key_word"
    delete_table( db, table_name )

#--------------
def delete_table_photo_key_word( db ):
    # Prepare the SQL command to drop a table
    table_name     = "photo_key_word"
    delete_table( db, table_name )

#--------------
def create_table_parm_key_word( db, table_name ):
    """
    what it says
    on way to replacing all create____
    """
    #what   = "create_table_stuff_key_word"
    what   = f"create_{table_name = } "
    print( f"{what}")

    db.transaction()
    query     = QSqlQuery( db )

    # sql    = data_dict.sql_dict[ table_name ]
    sql    = code_gen.to_sql_create( table_name )

    query.exec( sql )

    last_error    = query.lastError ()
    print( f"{what} {last_error} = " )
    ia_qt.q_sql_error( last_error,
                       msg       =  f"now in code at: {what}",
                       print_it = True,
                       include_dir = False,    # default False
                       )
    db.commit()

    print( f"{what} table created??")


#--------------
def drop_table_by_table_name( db_file_name, table_name ):
    """
    what it says
    on way to replacing all create___-- will now delete this is version 46 _
    also delete the inserts as we are using exported data now
    db_create.drop_table_by_table_name( db_file_name, table_name )

    """
    global DB_FILE_NAME
    DB_FILE_NAME  = db_file_name
    create_connection(  )

    sql          = f"DROP TABLE IF EXISTS {table_name}";

    msg   = "drop_table_by_table_name a message {db_file_name = }  {table_name = }"
    execute_sql( msg = msg , db = DB_CONNECTION, sql = sql  )

    print( "drop_table_by_table_name done")
    #ex_helpers.end_example( ex_name )

#--------------
def create_table_by_table_name( db_file_name, table_name ):
    """
    what it says
    on way to replacing all create___-- will now delete this is version 46 _
    also delete the inserts as we are using exported data now

    people may be tmplat for use


    """
    what   = f"create_{table_name = } {db_file_name} "
    print( f"{what}")

    #DB_FILE_NAME  = DB_FILE_NAME
    db             = create_connection( db_file_name )

    db.transaction()
    query     = QSqlQuery( db )

    # sql    = data_dict.sql_dict[ table_name ]
    sql    = code_gen.to_sql_create( table_name )

    query.exec( sql )

    last_error    = query.lastError ()
    print( f"{what} {last_error} = " )
    ia_qt.q_sql_error( last_error,
                       msg          =  f"now in code at: {what}",
                       print_it     = True,
                       include_dir  = False,    # default False
                       )
    db.commit()

    print( f"{what} table created??")

# -------------------------------
def insert_query_list( db, query_list  ):
    query = QSqlQuery()

    for sql in query_list:
        if not query.exec_(sql):
            print(f"Query failed: {query.lastError().text()}")
            print(f"Query was: {sql}")

# --------------------
if __name__ == "__main__":
    """
    """

    # ---- run manually --------------------------
    # nire at tio
    PARM            = "X"
    TABLE_NAME      = ""
    FUNCTION        = None

    print( "!!still needs work" )
    print( "running manually ---------- disconnect other stuff please  ---------")

    #create_table_photo_text( db = create_connection() )
    #create_table_photo( db = create_connection() )
    # insert_photo_text( db = create_connection()  )

    #create_table_photoshow( db = create_connection() )
    #create_table_photoshow_photo( db = create_connection() )
    # ---- stuff

    #insert_stuff( db = create_connection()  )
    # create_table_stuff_event( db = create_connection() )
    # insert_stuff_events( db = create_connection()  )
    #insert_stuff_text( db = create_connection()  )


    #create_table_stuff_key_word( db = create_connection() )
    # ---- help
    # insert_help_info( db = create_connection()  )

    # create_table_help_text( db = create_connection()  )stuff
    # insert_help_text( db = create_connection()  )

    # ---- people
    #create_people( db = create_connection() )
    #insert_people( db = create_connection() )

    #create_people_text( db = create_connection() )
    #insert_people_text( db = create_connection() )

    #create_people_contact( db = create_connection() )
    #insert_people_contact( db = create_connection() )


    #create_people( db = create_connection() )
    #insert_stuff( db = create_connection()  )
    # create_table_stuff_event( db = create_connection() )
    # insert_stuff_events( db = create_connection()  )
    #insert_stuff_text( db = create_connection()  )


    # ---- photo
    # create_table_photo_subject( db = create_connection()  )
    #insert_photo_subject( db = create_connection()  )

    #update_table_key_gen( db = create_connection()  )

    #insert_photo( db = create_connection()  )
    #insert_photo_text( db = create_connection()  )

    #insert_photo_subject( db = create_connection()  )

    #create_table_photo_key_word( db = create_connection()  )

    # ---- planting
    # edit next two first -- should need only one
    #insert_key_gen( db = create_connection()  )
    #update_table_key_gen(  db = create_connection()  )

    #create_planting( db = create_connection()  )
    #insert_planting( db = create_connection()  )

    #create_planting_text( db = create_connection()  )
    #insert_planting_text( db = create_connection()  )

    #create_planting_event( db = create_connection()  )
    #insert_planting_event( db = create_connection()  )

    #insert_photo_planting_subject( db = create_connection()  )

    print( "ran manually -------------------------------------------------")


