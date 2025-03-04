#!/usr/bin/env python3
# -*- coding: utf-8 -*-



"""
this module is intended to be the top module else do not use



"""

# --------------------
if __name__ != "__main__":
    1/0
# --------------------



# ---- imports
import adjust_path
# ---- begin pyqt from import_qt.py

from PyQt5.QtGui import (
    QStandardItemModel,
    QStandardItem,
                        )
# ---- QtCore
from PyQt5.QtCore  import  (
    QDate,
    QModelIndex,
    QTimer,
    Qt,
    pyqtSlot,
                            )

from PyQt5.QtGui import (
    QIntValidator,
    )

# ----QtWidgets
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QAction,
    QTableWidgetItem,
    QTableWidget,
    QDateEdit,
    QMenu,
    QAction,
    QLineEdit,
    QActionGroup,
    QApplication,
    QDockWidget,
    QTabWidget,
    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QSpinBox,
    QMdiSubWindow,
    QTextEdit,
    QButtonGroup,

    )

# ----QtWidgets big
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

# ----QtWidgets layouts
from PyQt5.QtWidgets import (
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    )

# ----QtWidgets Boxs, Dialogs
from PyQt5.QtWidgets import (
    QAction,
    QActionGroup,
    QDockWidget,
    QFileDialog,
    QInputDialog,

    QLabel,
    QListWidget,
    QMenu,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QCheckBox,
    QComboBox,
    )

# ---- QtSql
from PyQt5.QtSql import (
    QSqlDatabase,
    QSqlTableModel,
    QSqlQuery
    )


import pprint
import sqlite3


# ---- Imports
import shutil
import os
import time
import stat
import os
#import datetime
from   datetime import datetime
from   pathlib import Path
import traceback

# import ex_helpers
# import ex_helpers  as ex_h
import db_create
# import code_gen
# import data_dict
# import import_utils


import parameters

temp  = parameters.Parameters()
print( parameters.PARAMETERS )

DB_CONNECTION    = None

"""



"""


# # ---- quasi constants and constants
# DB_FILE_NAME            = "./stuff.db"
# DB_FILE_NAME            = "/tmp/ramdisk/stuff.db"
# DB_FILE_NAME            = "/tmp/ramdisk/photo_subjects.db"
# DB_FILE_NAME            = "/mnt/WIN_D/Russ/0000/python00/python3/_projects/stuffdb/data/appdb.db"
# DB_FILE_NAME            = "/tmp/ramdisk/sept_28.db"

#DB_FILE_NAME       = parameters.PARAMETERS.db_fn

def insert_if(  table_name ):
    """
    insert row into key gen for table name
        if not already there
        will set to 0
    """

    query = QSqlQuery( DB_CONNECTION )

    # Step 1: Check if "sue" already exists
    check_sql = "SELECT COUNT(*) FROM key_gen WHERE table_name = :table_name"
    query.prepare(check_sql)
    query.bindValue(":table_name",  table_name  )

    if not query.exec_():
        print(f"Query failed: {query.lastError().text()}")
    else:
        if query.next():
            count = query.value(0)
            if count == 0:

                insert_sql = "INSERT INTO key_gen (table_name, key_value) VALUES (:table_name, :key_value)"
                query.prepare(insert_sql)
                query.bindValue(":table_name", table_name  )
                query.bindValue(":key_value", 0 )  # Set key_value as appropriate, using 0 as an example

                if not query.exec_():
                    print(f"Insert query failed: {query.lastError().text()}")
                else:
                    print( f"Row for {table_name = } added successfully")
            else:
                print( f"{table_name = } already exists in the table")

#---------------------------------------------
def update_tables(   ):
    """
    update key gen for a list of tables
    """
    table_list    = [
                        "stuff",
                        "photo",
                        "planting",
                        "help_info",
                        "photoshow",
                        "people",
        ]

    for i_table in table_list:
        update_a_table( i_table )

#---------------------------------------------
def update_a_table( table_name ):
    """
    update key gen for a single table
    """
    # ex_name  = "update_a_table"
    # print( f"{ex_helpers.begin_example( ex_name )}"
    #         "\n    "
    # )

    insert_if( table_name )

    db_create.DB_FILE_NAME  = DB_FILE_NAME
    db_create.create_connection(  )

    query = QSqlQuery( db_create.DB_CONNECTION )

    sql = f"SELECT MAX(id) FROM {table_name}"

    query.prepare(sql)

    if not query.exec_():
        print(f"Query failed: {query.lastError().text()}")
    else:
        if query.next():
            max_id = query.value(0)  # Get the max value from the result set
            print(f"The maximum id value is: {max_id}")
        else:
            print("No rows found")

    new_key_value   = max_id + 200

    # ---- update
    sql = "UPDATE key_gen SET key_value = :new_value WHERE table_name = :table_name"

    query.prepare(sql)

    query.bindValue(":new_value",  new_key_value)
    query.bindValue(":table_name", table_name)

    if not query.exec_():
        print(f"Query failed: {query.lastError().text()}")
    else:
        print("Key value updated successfully")

#---------------------------------------------
def update_a_table_key_gen( table_name, new_value ):
    """
    update key gen for a single table
    """
    # ex_name  = "update_a_table"
    # print( f"{ex_helpers.begin_example( ex_name )}"
    #         "\n    "
    # )

    insert_if( table_name )   # now we have the file

    # db_create.DB_FILE_NAME  = DB_FILE_NAME
    # db_create.create_connection(  )

    #query = QSqlQuery( db_create.DB_CONNECTION )

    # sql = f"SELECT MAX(id) FROM {table_name}"

    # query.prepare(sql)

    # if not query.exec_():
    #     print(f"Query failed: {query.lastError().text()}")
    # else:
    #     if query.next():
    #         max_id = query.value(0)  # Get the max value from the result set
    #         print(f"The maximum id value is: {max_id}")
    #     else:
    #         print("No rows found")

    # new_key_value   = max_id + 200

    # ---- update

    query = QSqlQuery( DB_CONNECTION )

    sql = "UPDATE key_gen SET key_value = :new_value WHERE table_name = :table_name"

    query.prepare( sql )

    query.bindValue(":new_value",  new_value )
    query.bindValue(":table_name", table_name )

    if not query.exec_():
        print(f"Query failed: {query.lastError().text()}")
    else:
        print("Key value updated successfully")


#----------------------------------
def create_tablexxxxseebelow ():
    """
    create the key_gen table
    """
    # ex_name  = "create_table"
    # print( f"{ex_helpers.begin_example( ex_name )}"
    #         "\n    "
    # )
    key_gen_table           = "key_gen"
    db_create.DB_FILE_NAME  = DB_FILE_NAME
    db_create.create_connection(  )
    sql         = data_dict.sql_dict[ key_gen_table ]

    msg   = f"CREATE TABLE  {key_gen_table} "
    db_create.create_table( msg = msg , db = db_create.DB_CONNECTION, sql = sql  )

    # ex_helpers.end_example( ex_name )


# ------------------------------------------------------
def create_connect_for_module(   ):
    """
    what it says
        create global module

    """
    db_connection   =  db_create.create_connection( parameters.PARAMETERS.db_fn )
    global   DB_CONNECTION
    DB_CONNECTION   = db_connection
    print( f"create_connect_for_module  {DB_CONNECTION = }"  )

# # ------------------------------------------------------
# def test_get_connect(   ):
#     """


#     """
#     #db_create.DB_FILE_NAME  = DB_FILE_NAME
#     db_create.create_connection( parameters.PARAMETERS.db_fn )
#     print( f"{db_create.DB_CONNECTION = }"  )

#     query = QSqlQuery( db_create.DB_CONNECTION )





# ---- run from here, be careful


#test_get_connect()

# do this befor all others
create_connect_for_module()
update_a_table_key_gen( "help_info", 100_000 )
# --------------------
#db_create.create_connection( parameters.PARAMETERS.db_fn )
# print( f"{db_create.DB_CONNECTION = }"  )
# update_a_table_key_gen( db_create.DB_CONNECTION, help_info, 100_000 )


# ---- drop
#db_create.drop_table_by_name(  DB_FILE_NAME, "key_gen"   )


#db_create.create_table_by_table_name( DB_FILE_NAME, "key_gen" )

#update_tables()



#insert_if( "jones")
#update_a_table( table_name    = "photo")
#update_tables()


# ---- eof -----------------------------------------------