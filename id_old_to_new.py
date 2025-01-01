#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 14:23:51 2024

@author: russ
"""
# -*- coding: utf-8 -*-
#>>>>>python example for file read write -- and some file info
# snipfile_ok>> python example file operations  ex_file.py

"""
What:

Status:
    draft,
Refs:

"""
# ---- search --------------
"""
Search for the following in the code below:



"""
import os
import pprint
import shutil
import sqlite3
import stat
import time
import traceback
#import datetime
from datetime import datetime
from pathlib import Path

import ex_helpers
import ex_helpers as ex_h
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

# ---- imports
import adjust_path
import code_gen
import db_create
import import_utils

# ---- begin pyqt from import_qt.py












# ---- Imports




"""



"""


# ---- quasi constants and constants

DB_FILE_NAME            = "./stuff.db"
DB_FILE_NAME            = "/tmp/ramdisk/stuff.db"
DB_FILE_NAME            = "/tmp/ramdisk/photo_subjects.db"
DB_FILE_NAME            = "/tmp/ramdisk/sept_26.db"
DB_FILE_NAME            = "/tmp/ramdisk/sept_28.db"

#KEY_OFFSET              = 1000

#TABLE_NAME              = "photo_subject"


MAX_LINES               = 100_000
#MAX_LINES               = 100

no_not_found            = 0
no_found                = 0

# SELECT
#            photo.id,
#            photo.id_old

#        FROM
#            photo

#        WHERE
#            photo.id_old = "rsh68417";



# select   something one at a TimeoutError

#         get old id
#             look up new id

#             update something id with the new id





def do_update( table_id, new_id ):
    """
    this may be derived from id_old_to_new.py
    please generate the python qt5 code to update
    table photo_subject for its id photo_subject.id  = photo_subject_id
    photo_subject.photo_id = new_id  where photo_subject.photo_id is
    a column in photo_subject?

    update_sql for some table
    table_id
    old_id   to update into
    new_id


    """
    # Assuming you've already established a database connection
    query = QSqlQuery()

    # Prepare your SQL statement with placeholders
    query.prepare("""
        UPDATE photo_subject
        SET photo_id = :photo_id
        WHERE id = :id
    """)

    # Bind values to the placeholders
    query.bindValue(":photo_id", new_id)
    query.bindValue(":id", table_id )


    # Execute the query and check for success
    if query.exec():
        print("Update successful")
    else:
        print("Update failed:", query.lastError().text())





def lookup_photo_by_id( id_old_lookup ):
    """
    return  the new_id or none
    master location for this is in
    id_old_to_new


    """
    global no_not_found
    global no_found


    # Step 2: Prepare the query to select based on id_old
    query = QSqlQuery( db_create.DB_CONNECTION )
    query.prepare("SELECT id, id_old, name FROM photo WHERE id_old = :id_lookup")
    query.bindValue(":id_lookup", id_old_lookup )

    # Step 3: Execute the query
    if not query.exec_():
        print("Failed to execute query")
        return

    # Step 4: Fetch the results and count rows
    rows = 0
    results = []
    while query.next():
        rows += 1
        # Fetch each field's value
        id       = query.value(0)        # id (INTEGER)
        id_old   = query.value(1)    # id_old (VARCHAR)
        name     = query.value(2)      # name (VARCHAR)

        results.append( (id, id_old, name ))

    # Step 5: Display the number of rows and data
    if rows == 0:
        print("No rows found.")
        no_not_found  += 1
        ret     = None
    elif rows == 1:
        print(f"One row found: {results[0]}")
        no_found  += 1
        ret     = id
    else:
        print(f"{rows} rows found.")
        for result in results:
            print(f"ID: {result[0]}, ID Old: {result[1]}, Name: {result[2]}")
        ret     = None
    return ret


# ------------------------------------------
def update_photo_subject_data(   ):
    """
    this only does one part tho import
        may do some more  read it
    look in id_old_to_new --  note need different versions for dirrent table

    """

    db_create.DB_FILE_NAME  = DB_FILE_NAME
    db_create.create_connection(  )

    # if not db.open():
    #     print("Failed to open the database")
    #     return

    # Step 2: Define the query
    query = QSqlQuery(  db_create.DB_CONNECTION   )
    query.prepare( "SELECT id, photo_id_old, table_id_old, "
                   "table_joined, photo_id, table_id FROM photo_subject")

    if not query.exec_():
        print("Failed to execute query")
        return

    # Step 3: Loop through the result set
    ix    = 0
    while query.next():
        ix += 1
        # Fetch each field's value
        a_id                = query.value(0)               # id (INTEGER)
        photo_subject_id    = query.value(0)
        photo_id_old        = query.value(1)      # photo_id_old (VARCHAR)
        table_id_old        = query.value(2)      # table_id_old (VARCHAR)
        table_joined        = query.value(3)      # table_joined (VARCHAR)
        photo_id            = query.value(4)      # photo_id (INTEGER)
        table_joined_id     = query.value(5)       # table_id (INTEGER)


        #print(f"{ix = } ID: {id}, Photo ID Old: {photo_id_old}, Table ID Old: {table_id_old}, Table Joined: {table_joined}, Photo ID: {photo_id}, Table ID: {table_id}")
        print(f"{ix = } ID: {id}, Photo ID Old: {photo_id_old},  " )

        photo_id    = lookup_photo_by_id( photo_id_old )

        if photo_id is not None:
            pass
            do_update( a_id, photo_id )

        # next incase they are flipp1ed
        # lookup_photo_by_id( table_id_old )  # seem worse
        # if ix > 500:
        #     break

    print( f"{no_not_found = }   {no_found = }   " )
    # Close the database connection when done
    # db.close()

# Call the function


def do_update_with_sql(  table_id, new_id, sql = "", ):
    """
    this may be derived from id_old_to_new.py
    please generate the python qt5 code to update
    table photo_subject for its id photo_subject.id  = photo_subject_id
    photo_subject.photo_id = new_id  where photo_subject.photo_id is
    a column in photo_subject?

    update_sql for some table
    table_id
    old_id   to update into
    new_id


    """
    # Assuming you've already established a database connection
    query = QSqlQuery()

    # Prepare your SQL statement with placeholders

    sql   = (
        """
        UPDATE photo_in_show
        SET    photo_show_id = :new_id
        WHERE id = :table_id
        """)


    query.prepare( sql )
    # Bind values to the placeholders
    query.bindValue(":new_id", new_id)
    query.bindValue(":table_id",     table_id )


    # Execute the query and check for success
    if query.exec():
        print("Update successful")
    else:
        print("Update failed:", query.lastError().text())


# ---- looks ok for photo_subject, photo -- need to extend for others

def lookup_photoshow_by_old_id( id_old_lookup ):
    """
    return  the new_id or none
    master location for this is in
    id_old_to_new


    """
    global no_not_found
    global no_found


    # Step 2: Prepare the query to select based on id_old
    query = QSqlQuery( db_create.DB_CONNECTION )
    query.prepare("SELECT id, id_old FROM photoshow WHERE id_old = :id_old_lookup")
    query.bindValue(":id_old_lookup", id_old_lookup )

    # Step 3: Execute the query
    if not query.exec_():
        print("Failed to execute query")
        return

    rows        = 0
    results     = []
    while query.next():
        rows += 1
        # Fetch each field's value
        id       = query.value(0)        # id (INTEGER)
        id_old   = query.value(1)    # id_old (VARCHAR)
        #name     = query.value(2)      # name (VARCHAR)

        results.append( (id, id_old, ))  # name ))


    if rows == 0:
        print("No rows found.")
        no_not_found  += 1
        ret     = None
    elif rows == 1:
        print(f"One row found: {results[0]}")
        no_found  += 1
        ret     = id
    else:
        print(f"{rows} rows found.")
        for result in results:
            print(f"ID: {result[0]}, ID Old: {result[1]} ")
        ret     = None
    return ret


# ------------------------------------------
def update_photo_in_show_data(   ):
    """
    this will update the show id from the old to the
    new
    the photoshow must alredy be imported
    need to query photo_in_show then update it

        id                      INTEGER,      integer,
    	photo_id_old      		VARCHAR(15),  string,
    	photo_show_id_old 		VARCHAR(15),  string,
    	sequence      		    INTEGER,     integer,
    	photo_in_show_id_old    VARCHAR(15),  string,
    	photo_id      		    INTEGER,     integer,
    	photo_show_id		    INTEGER,     integer,
    	photo_in_show_id        INTEGER,      integer,
        )

    """

    db_create.DB_FILE_NAME  = DB_FILE_NAME
    db_create.create_connection(  )

    # if not db.open():
    #     print("Failed to open the database")
    #     return

    # Step 2: Define the query
    query = QSqlQuery(  db_create.DB_CONNECTION   )
    query.prepare( "SELECT id, photo_show_id_old from photo_in_show" )

    if not query.exec_():
        print("Failed to execute query")
        return

    # Step 3: Loop through the result set
    ix    = 0
    while query.next():
        ix += 1
        # Fetch each field's value
        a_id                 = query.value(0)               # id (INTEGER)
        photo_show_id_old    = query.value(1)


        #print(f"{ix = } ID: {id}, Photo ID Old: {photo_id_old}, Table ID Old: {table_id_old}, Table Joined: {table_joined}, Photo ID: {photo_id}, Table ID: {table_id}")
        print(f"{ix = } ID: {a_id},  {photo_show_id_old =},  " )
        new_id   = lookup_photoshow_by_old_id( photo_show_id_old )

        if new_id is not None:
            do_update_with_sql( a_id, new_id )

        # photo_id    = lookup_photo_by_id( photo_id_old )

        # if photo_id is not None:
        #     pass
        #     do_update( a_id, photo_id )

        # next incase they are flipp1ed
        # lookup_photo_by_id( table_id_old )  # seem worse
        # if ix > 500:
        #     break

    print( f"{no_not_found = }   {no_found = }   " )
    # Close the database connection when done
    # db.close()

# Call the function


# ---- looks ok for photo_subject, photo -- need to extend for others



# ---- be careful what you run
#update_photo_subject_data()

# update_photo_in_show_data()