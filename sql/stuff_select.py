#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 11:07:49 2024

@author: russ
"""

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

import sqlite3


#from   functools import partial
import collections
import functools
import time

# import winsound windows only


# ---- imports local

#from    app_global import AppGlobal

import  gui_qt_ext
import  string_util
import  qt_sql_query

import  ia_qt
import qt_sql_query
import key_words

# ---- "stuff_criteria_key_words"

kw_table_name   = "stuff_criteria_key_words"

a_key_word_processor        = key_words.KeyWords( kw_table_name )


criteria   = { "criteria_key_words": "one two three"}

# get criteria
qt_query            = QSqlQuery( )

query_builder       = qt_sql_query.QueryBuilder( qt_query, print_it = True, logger = None, write_gui = None  )


print( "\n\n=======================================")


criteria_key_words           = criteria[ "criteria_key_words" ]
criteria_key_words           = a_key_word_processor.string_to_key_words( criteria_key_words )
key_word_count                  = len(  criteria_key_words )
        # now have aset
criteria_key_words              = ", ".join( [ f'"{i_word}"' for i_word in criteria_key_words ] )
criteria_key_words              = f'( {criteria_key_words} ) '    # ( "one", "two" )

# ----- build query
query_builder.reset()
query_builder.table_name        = "stuff"

column_list                     = [ 'add_kw', 'descr' ]

query_builder.column_list       = column_list

query_builder.group_by_c_list   = column_list
query_builder.sql_inner_join    = " stuff_key_word  ON stuff.id = stuff_key_word.id "
query_builder.sql_having        = f" count(*) = {key_word_count} "

query_builder.add_to_where( f" key_word IN {criteria_key_words}" , [] )

#rint( criteria_key_words )


sql     = query_builder.get_sql()
#print( sql )


# ---- "help ----------------------------------------------
print( "\n\n=======================================")

kw_table_name           = "help_key_words"

a_key_word_processor    = key_words.KeyWords( kw_table_name )


criteria   = { "key_words": "the code"}
criteria   = { "key_words": "" }

# get criteria
qt_query                        = QSqlQuery( )

query_builder                   = qt_sql_query.QueryBuilder( qt_query, print_it = True, logger = None, write_gui = None  )



criteria_key_words              = criteria[ "key_words" ]
criteria_key_words              = a_key_word_processor.string_to_key_words( criteria_key_words )
key_word_count                  = len(  criteria_key_words )
        # now have aset
criteria_key_words              = ", ".join( [ f'"{i_word}"' for i_word in criteria_key_words ] )
criteria_key_words              = f'( {criteria_key_words} ) '    # ( "one", "two" )

# ----- build query
query_builder.reset()
query_builder.table_name        = "help_info"

column_list                     = [ 'title', 'system' ]

query_builder.column_list       = column_list

if key_word_count > 0:

    query_builder.group_by_c_list   = column_list
    query_builder.sql_inner_join    = " help_key_word  ON help_info.id = help_key_word.id "
    query_builder.sql_having        = f" count(*) = {key_word_count} "

    query_builder.add_to_where( f" key_word IN {criteria_key_words}" , [] )

query_builder.add_to_where( f'  title LIKE  "%t%"  ' , [] )


sql     = query_builder.get_sql()
#print( sql )

# ---- generated sql that worked
"""
SELECT   help_info.title, help_info.system    FROM help_info
    INNER JOIN  help_key_word  ON help_info.id = help_key_word.id
    WHERE  key_word IN ( "code", "the" )  AND    title LIKE  "t"
    GROUP BY   help_info.title, help_info.system
    HAVING  count(*) = 2





"""

