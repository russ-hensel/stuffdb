#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 16:13:31 2024

@author: russ
"""

# ---- imports


import re

import string_util

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

VERBOSE    = False

# ------------------------------------------
class KeyWords(   ):
    """
    in flux, needs better name move testing
    """
    def __init__(self, table_name, db_connect ):
        """
        do some key word processing
            still have to figure out how much
            think can include the db work
        table_name   = "stuff_key_word"
        """
        self.table_name             = table_name   # the key word table name
        self.is_done                = False        # may be ng, if some comp is ok
        self.db                     = db_connect
            # do we hav uuptodate current and old

        self.old_string             = ""
        self.new_string             = ""
        # perhaps all should be sets

        self.new_key_words          = None   # will be a set
        self.old_key_words          = None   # will be a set

        #self.key_word_tn          = None

        self.add_key_words          = None   # will be a set
        self.delete_key_words       = None   # will be a set

        self.key_words_for_delete   = None     # see:
        self.key_words_for_add      = None     # see:

    #----------------------------------
    def string_to_key_words( self,  a_string, caps_split = True ):
        """
        !! change to return a set

        Args:
            a_string (TYPE): DESCRIPTION.
            caps_split  = True   split on caps for indexing

        set   of key words

        split up camel case
        remove and split on dirt   !! durt might remain
        lower case
        remove terminal s on over 2 characters
        make list
        lower
        return
            a set of the key words

        """
        # next not verry efficient
        if caps_split:
            a_string = a_string + " " + a_string.lower() # suppress cap split
        else:
            a_string = a_string.lower() # suppress cap split


        key_word_list    = self.split_on_caps_and_whitespace( a_string )
        key_word_list    = [ a_word.lower( ) for a_word in key_word_list ]

        # try modify in place in list rathere than new list
        new_key_word_set  = set()
        for a_key_word   in key_word_list:
            pass
            # might do lower case here
            if len( a_key_word ) > 3:
                if a_key_word.endswith( "s" ):
                    a_key_word    = a_key_word[ : -1]
            new_key_word_set.add( a_key_word )
        key_word_set  = new_key_word_set

        return key_word_set

    #----------------------------------
    def string_to_old( self, a_string ):
        """
        process a string to key words
        """
        self.is_done            = False
        self.old_string         = a_string
        self.old_key_words      = self.string_to_key_words( a_string )
        debug_key_words         = self.old_key_words

    def move_new_to_old():
        """for use at end of compute and delete """
        1/0

    #----------------------------------
    def string_to_new( self, a_string ):
        """
        process a string to key words
        """
        self.is_done            = False
        self.new_string         = a_string
        self.new_key_words      = self.string_to_key_words( a_string )
        debug_key_words         = self.new_key_words

    #----------------------------------
    def compute_add_delete( self, table_id  ):
        """
        process a string to key words for adds and deletes
        and run the inserts and deletes

        """
        #rint( self )
        self.key_words_for_delete       = self.old_key_words - self.new_key_words
        self.key_words_for_add          = self.new_key_words - self.old_key_words
        # if in new and not in old then add
        #rint(  f"compute_add_delete deleting    { self.key_words_for_delete  =} " )
        self.delete_rows( table_id, self.key_words_for_delete  )

        #rint(  f"compute_add_delete adding    { self.key_words_for_add  =} " )
        self.insert_rows( table_id, self.key_words_for_add     )

        # because of update we have
        self.old_string                 = self.new_string
        self.old_key_words              = self.new_key_words

    # --------------------------------------
    def delete_rows( self, table_id, words ):
        """
        Delete rows from a table where a column matches a value in the list.
        """
        #rint( self )
        query = QSqlQuery( self.db )
        # Prepare the DELETE statement with a placeholder (bind variable)
        query.prepare( f"DELETE FROM {self.table_name} WHERE id = :table_id and key_word = :word" )

        for word in words:
            # Bind the value to the placeholder
            query.bindValue( ":word",     word )
            query.bindValue( ":table_id", table_id )

            # Execute the DELETE statement
            if not query.exec_():
                error = query.lastError()
                print(f"Error deleting word {word}: {error.text()}")
            else:
                if VERBOSE:
                    print(f"Successfully deleted rows where word = {word}")

    # --------------------------------------
    def insert_rows( self, table_id, words ):
        """
        Insert rows into a table where a column matches a value table_id, words
        """
        query = QSqlQuery( self.db )

        sql            = ( f"INSERT INTO {self.table_name}"
                           f"  (id, key_word ) VALUES ( :id, :key_word )")

        msg            = f"insert_rows sql = {sql}"
        print( msg )
        query.prepare( sql )

        # Insert each record
        for i_key_word in words:
            query.bindValue( ":id",        table_id )
            query.bindValue( ":key_word",  i_key_word )

            if not query.exec_():
                print( f"Error inserting record {i_key_word}: {query.lastError().text()}" )
                1/0
            else:
                if VERBOSE:
                    print( f"Record {i_key_word} inserted successfully!" )

    # --------------------------------------
    def split_on_caps_and_whitespace( self, a_string ):
        """
        chat says
            chat_cammel_split.py

        Returns:
            split_words in a list

        """
        # Split based on whitespace
        words = re.split( r'\s+', a_string )

        # Split based on embedded capitest_string capital letters
        split_words = []
        for word in words:
            split_words.extend(re.findall(r'[a-z]+|[A-Z]+(?![a-z])|[A-Z][a-z]*', word))

        return split_words

    # --------------------------------------
    def __str__( self,   ):
        """ """

        a_str   = ""
        a_str   = ">>>>>>>>>>* KeyWords *<<<<<<<<<<<<"

        a_str   = string_util.to_columns( a_str, ["add_key_words",
                                           f"{self.add_key_words}" ] )
        a_str   = string_util.to_columns( a_str, ["db",
                                           f"{self.db}" ] )
        a_str   = string_util.to_columns( a_str, ["delete_key_words",
                                           f"{self.delete_key_words}" ] )
        a_str   = string_util.to_columns( a_str, ["is_done",
                                           f"{self.is_done}" ] )
        a_str   = string_util.to_columns( a_str, ["key_words_for_add",
                                           f"{self.key_words_for_add}" ] )
        a_str   = string_util.to_columns( a_str, ["key_words_for_delete",
                                           f"{self.key_words_for_delete}" ] )
        a_str   = string_util.to_columns( a_str, ["new_key_words",
                                           f"{self.new_key_words}" ] )
        a_str   = string_util.to_columns( a_str, ["new_string",
                                           f"{self.new_string}" ] )
        a_str   = string_util.to_columns( a_str, ["old_key_words",
                                           f"{self.old_key_words}" ] )
        a_str   = string_util.to_columns( a_str, ["old_string",
                                           f"{self.old_string}" ] )
        a_str   = string_util.to_columns( a_str, ["table_name",
                                           f"{self.table_name}" ] )
        return a_str


# a_key_words  = KeyWords()

# a_string  = "This 123 !!  ##  # isATest StringWithSeveral with with withs EmbeddedCaps AndWhiteSpace"

# print( a_string )
# print( a_key_words.string_to_key_words( a_string) )