#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Index the key words for all of a table

deletes all the old entries



"""
# ---- tof
import logging

from PyQt5 import QtGui
from PyQt5.QtCore import (QDate,
                          QModelIndex,
                          QSize,
                          QSortFilterProxyModel,
                          Qt,
                          QTimer)
# sql
from PyQt5.QtSql import (QSqlDatabase,
                         QSqlQuery,
                         QSqlQueryModel,
                         QSqlRelation,
                         QSqlRelationalDelegate,
                         QSqlRelationalTableModel,
                         QSqlTableModel)
from PyQt5.QtWidgets import (QAbstractItemView,
                             QAction,
                             QApplication,
                             QButtonGroup,
                             QCheckBox,
                             QComboBox,
                             QDataWidgetMapper,
                             QDateEdit,
                             QDialog,
                             QDoubleSpinBox,
                             QFormLayout,
                             QGridLayout,
                             QGroupBox,
                             QHBoxLayout,
                             QHeaderView,
                             QLabel,
                             QLineEdit,
                             QListWidget,
                             QListWidgetItem,
                             QMainWindow,
                             QMenu,
                             QMessageBox,
                             QPushButton,
                             QRadioButton,
                             QSpinBox,
                             QStyledItemDelegate,
                             QTableView,
                             QTableWidget,
                             QTableWidgetItem,
                             QTabWidget,
                             QTextEdit,
                             QVBoxLayout,
                             QWidget)

#import adjust_path
#import db_create
import key_words

# ---- end imports
LOG_LEVEL  = 20

# ------------------------------------------
class KeyWordIndexer(   ):
    """
    in flux, needs better name move testing
    """
    def __init__(self, db, table_name, kw_table_name  ):
        """
        """
        self.db                     = db
        self.table_name             = table_name
        self.kw_table_name          = kw_table_name
        self.sql                    = ""
        a_key_word_processor        = key_words.KeyWords( self.kw_table_name, self.db )
        self.akwp                   = a_key_word_processor
        #rint( "!! bad names")

    # ---------------------------
    def set_sql( self,  sql   ):
        """
        phase out of get_sql to somewhere else

        set_sql( sql   = SELECT  # but add quotes
            id,
            d_kw,
            scr,
            tle,
            me,
            nufact
            FROM    stuff    )

        """
        self.sql   = sql

    # ---------------------------
    def get_sql( self, table_name  ):
        """
        !! change this so column names passe in as part of setup
        sql select to get the key word string, then
        made into key words
        id needs to be first
        others strings
        """
        # next for compat with old code before ripped out
        if not self.sql == "":
            return self.sql

        # ---- stuff
        if   table_name == "stuff":
            sql        = """SELECT
            id,
         	add_kw,
         	descr,
         	title,
         	name,
         	manufact
            FROM    stuff  """

        # ---- help_info
        elif table_name == "help_info":
            sql        = """SELECT
            id,
            sub_system,
            system,
            key_words,
            table_name,
            column_name,
            title

            FROM    help_info  """

        elif table_name == "photo":
            sql        = """SELECT
            id,
           	name,
           	add_kw ,
           	descr
            FROM    photo  """

        elif table_name == "people":
            sql        = """SELECT
            id,
           	f_name,
           	l_name,
            c_name,
           	add_kw ,
           	descr
            FROM    people  """

        elif table_name == "planting":
            sql        = """SELECT
            id,
           	name,
           	add_kw ,
           	lbl
            FROM    planting  """

        elif table_name == "plant":
            sql        = """SELECT
            id,
           	name,
           	add_kw ,
            latin_name
            FROM    plant """
        # ---- photoshow  = album
        elif table_name == "photoshow":  # album
            sql        = """SELECT
            id,
           	name,
           	cmnt
            FROM    photoshow """

        # ---- tabs
        elif table_name == "tabs":
            sql        = """SELECT
            id,
           	doc_file_name,
           	tab_title,
            widgets,
            key_words
            FROM    tabs """

        else:
            print( f"not set up for {table_name = }")
            1/0

        #rint( f"KeyWordIndexer sql for key words {sql}")
        return sql

    # ---------------------------
    def get_key_words( self, table_name, row_data  ):
        """
        pull out the fields needed for a specific table
        needs to be specialized
        currently may be all fields
        adjust sql to only get the fields to indes
        """
        key_words     = None
        key_words     = " ".join( row_data )
        debug_msg     = f"get_key_words just got key words {key_words = }"
        logging.log( LOG_LEVEL,  debug_msg, )
        return key_words

    # ---------------------------
    def loop_thru( self ):
        """
        """
        sql  = self.get_sql( self.table_name )

        #print( f"loop_thru    {sql = } ")
        query       = QSqlQuery( self.db )

        if not query.exec_( sql ):
            error = query.lastError()
            print( f"Error executing query: {error.text()}")
            print( f"Driver error: {error.driverText()}")
            print( f"Database error: {error.databaseText()}")

        ix    = 0
        #rint( "query loop ")
        while query.next():
            ix   += 1

            row_data = [ str( query.value(i) ) for i in range(query.record().count())]

            #print(row_data)
            table_id          = int( row_data[ 0 ] )
            old_kw_string     = ""
            new_kw_string     = self.get_key_words( self.table_name, row_data[ 1: ]  )
                # split off id an int
            #rint( f">>>>>>> {new_kw_string = }<<<" )
            #a_key_word_processor
            akwp          = self.akwp
            #ret           = akwp.string_to_key_words( new_kw_string  )
            #print( ret )

            # will delete everything
            akwp.string_to_old(    new_kw_string  )
            akwp.string_to_new(    ""  )

            # will create everything
            akwp.string_to_old(    ""  )
            akwp.string_to_new(    new_kw_string  )

            akwp.compute_add_delete( table_id  )


# #--------------------------
# def run_indexer_on_help( ):
#     """
#     --- now in seperater file/dir
#     seems to work
#     """
#     1/0 # phase out use from some other file
#     db_fn       = "/tmp/ramdisk/help_info.db"
#     db          =  db_create.create_connection( db_fn )
#     db_create.delete_table_help_key_word( db )
#     db_create.create_table_help_key_word( db )
#     a_kwi     = KeyWordIndexer( db = db, table_name =  "help_info", kw_table_name = "help_key_word"   )
#     a_kwi.loop_thru()

# # ---------------------
# def run_indexer_on_stuff( ):
#     """
#     close to working but not quite  --- now in seperater file/dir
#     """
#     1/0 # phase out use from some other file
#     db_fn       = ""
#     1/0
#     db          =  db_create.create_connection( db_fn )
#     db_create.delete_table_stuff_key_word( db )
#     db_create.create_table_stuff_key_word( db )
#     a_kwi     = KeyWordIndexer( db = db, table_name =  "stuff"   )
#     a_kwi.loop_thru()

# --------------------
if __name__ == "__main__":
    #run_indexer_on_help()

    # ---- run manually  no see table_key woprd indexer --------------------------

    print( "running manually ---------- disconnect other stuff please  ---------")



# ---- eof -----------------------------------------