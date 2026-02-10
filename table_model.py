#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 09:29:38 2024

table_model.
"""
# ---- tof
# # --------------------
# if __name__ == "__main__":
#     #----- run the full app
#     import main
#     main.main()
# # --------------------


# ---- begin pyqt from import_qt.py

#from   functools import partial
#import collections
import functools
import sqlite3

#import  gui_qt_ext
import   string_utils as string_util
import   string_utils
from app_global import AppGlobal


from qt_compat import QApplication, QAction, exec_app, qt_version
from PyQt.QtWidgets import QMainWindow, QToolBar, QMessageBox
from qt_compat import Qt, DisplayRole, EditRole, CheckStateRole
from qt_compat import Horizontal, Vertical

# ---- QtCore
from PyQt.QtCore import (QAbstractTableModel,
                          QDate,
                          QModelIndex,
                          QRectF,
                          Qt,
                          QTimer,
                          pyqtSlot)
from PyQt.QtGui import (QIntValidator,
                         QPainter,
                         QPixmap,
                         QStandardItem,
                         QStandardItemModel)
# ---- QtSql
from PyQt.QtSql import (QSqlDatabase,
                         QSqlQuery,
                         QSqlQueryModel,
                         QSqlRecord,
                         QSqlRelation,
                         QSqlRelationalDelegate,
                         QSqlRelationalTableModel,
                         QSqlTableModel)

#from PyQt.QtGui import ( QAction, QActionGroup, )

from PyQt.QtWidgets import (
                             QApplication,
                             QButtonGroup,
                             QCheckBox,
                             QComboBox,
                             QDateEdit,
                             QDialog,
                             QDockWidget,
                             QFileDialog,
                             QFrame,
                             QGraphicsPixmapItem,
                             QGraphicsScene,
                             QGraphicsView,
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

import file_browse

# ---- imports local


# -----------------------
def model_dump(  model, msg = "model dump msg" ):
    """
    believe is a debug thing
    what type need models be?
    """
    print( "model_dump begin")

    # ia_qt.q_abstract_table_model( model )
    # ia_qt.q_sql_table_model( model )

    row_count    = model.rowCount()
    column_count = model.columnCount()
    print( f"model_dump begin {row_count = } ")

    for row in range( row_count ):
        row_data = []

        for column in range(column_count):
            # Get the index for the current row and column
            index   = model.index(row, column)
            # Get the data for the current index
            data    = model.data( index )
            row_data.append(data)
            if   column == 2:
                table_name = data
            elif column == 1:
                table_id = data

        print(f"Row {row}: {row_data}")
    print( "model_dump end")

# --------------------------------------
class ModelIndexer( object ):
    """
    so we can do a find inside same sort of model ... later
    make an extension to the model..
    we can index a table model and its instances
    but not all will invalidate the index like the sql models
    """
    #----------- init -----------
    def __init__(self, model, index_tuple   ):
        """
        Usual init see class doc string
            model can be an abstracttablemodel  a TableModel, but what about sql thing
            index_tuple   [0] column_with table_name [1] column with table_id
        so index dict is  key  ( table, table_id )   value is row with the deat
        might want to not default index tuple
        """
        self.model          = model
        self.index_tuple    = index_tuple   # location in model of table, table_id
        # may need to set with model.model_indexer.index_tuple  = ( 21, 22 )

        self.index_dict     = {}
        self.is_valid       = False  # connected to addRow....
        self.refresh_index()

    #--------------------------------------------
    def __str__(self):
        """
        the usual
        """
        a_str   = ">>>>>>>>>>* ModelIndex *<<<<<<<<<<<<"
        a_str   = string_util.to_columns( a_str, ["index_dict",
                                           f"{self.index_dict}" ] )
        a_str   = string_util.to_columns( a_str, ["index_tuple",
                                            f"{self.index_tuple}" ] )
        a_str   = string_util.to_columns( a_str, ["is_valid",
                                           f"{self.is_valid}" ] )
        a_str   = string_util.to_columns( a_str, ["model",
                                           f"{self.model}" ] )
        return a_str

    # -----------------------------------
    def set_is_valid( self, a_bool ):
        """
        is the index valid ... how do we know
        """
        self.is_valid   = a_bool

    # -----------------------------------
    def refresh_index( self, ):
        """
        will not index dups
        """
        model               = self.model
        self.index_dict     = {}   # clear the dict
        row_count           = model.rowCount()
        #column_count = model.columnCount()

        for i_row in range( row_count ):
            row_data = []
            key      = []
            # build key using index_tuple, index itslelf is a tuple
            for i_column in self.index_tuple:
                index   = model.index( i_row, i_column )

                data    = model.data( index )
                key.append( data )

            key                         = tuple( key )
            self.index_dict[ key ]      = i_row         # row with ( table, table_id )
            #rint(f"Row {i_row = }: {key = }")
        self.set_is_valid( True )
        #rint( f"{self.index_dict = }")
        #rint( f"{str( self )  = }")

    # -----------------------------------
    def find( self, key ):
        """
        key is a tuple  matching the columns in .index_tuple
        this is not the row number or none if not found
        return
            row in model, else none
            row_or_none   = model_indexer.find( key )
        """
        if not self.is_valid:
            self.refresh_index()

        row     = self.index_dict.get( key, None )
        return row

# ------------------------
class TableModel( QAbstractTableModel ):
    """
    was TestTableModel -- unclear what it should be
    use a a list of file names from browse
    may be more generally useful
    code derived from chat
    """
    def __init__(self,  headers):
        super().__init__()
        self._data      = []
        self._headers   = headers
        self.indexer    = None
        """
        model.indexer.index_tuple = ( 0, 1 )
        """
    #-------
    def add_indexer (self, index_tuple ):
        """
        what it says read
        index tuple for now pair of column numbers to use as an index to model

        """
        self.indexer    = ModelIndexer( self, index_tuple  )

        return self.indexer   # or not ??

    # -----------------
    def refresh_index( self ):
        self.indexer.refresh_index()

    #-------
    def rowCount(self, index=None ):
        """
        what it says read
        why index = None, drop it
        """
        return len(self._data)

    #--------------------------
    def columnCount(self, index=None):
        return len(self._headers)

# # In qt_compat.py
# DisplayRole = Qt.ItemDataRole.DisplayRole if qt_version == 6 else Qt.DisplayRole
# EditRole    = Qt.ItemDataRole.EditRole    if qt_version == 6 else Qt.EditRole
# CheckStateRole = Qt.ItemDataRole.CheckStateRole if qt_version == 6 else Qt.CheckStateRole


    def data(self, index, role= DisplayRole):
        if role == DisplayRole:
            return self._data[index.row()][index.column()]

    # def data(self, index, role=Qt.DisplayRole):
    #     if role == Qt.DisplayRole:
    #         return self._data[index.row()][index.column()]

    def set_data(self, data ):
        self._data      = data

    # def add_data(self, data ):
    #     pass


    def set_data_at_index(self, index, value, role= EditRole):
        """
        index might be index = model.index(ix_row,  ix_col )  # Row 1, Column 1

        Args:
            index (TYPE): DESCRIPTION.
            value (TYPE): DESCRIPTION.
            role (TYPE, optional): DESCRIPTION. Defaults to Qt.EditRole.

        Returns:
            bool: DESCRIPTION.

        """
        if role == EditRole:
            self._data[index.row()][index.column()] = value  # Update the data
            self.dataChanged.emit(index, index, [DisplayRole])
                # Emit dataChanged signal for this index
            return True
        return False

    def headerData(self, section, orientation, role= DisplayRole):
        if role == DisplayRole:
            if orientation == Horizontal:
                return self._headers[section]
            elif orientation == Vertical:
                return str(section + 1)

    # Method to add a row
    def addRow(self, row_data):
        """
        read
        see tab_table_model_for example
        row_data   a list of the data types ??
        remember to invalidate index if any --- may build in or not
        """
        self.beginInsertRows(self.index(len(self._data), 0), len(self._data), len(self._data))
        self._data.append(row_data)
        self.endInsertRows()

        if self.indexer:   # more efficient to fix index but
            self.indexer.is_valid  = False

    # Optional method to remove a row
    def removeRow(self, row_index):
        """
        what it says, read
        """
        self.beginRemoveRows(self.createIndex(row_index, 0).parent(), row_index, row_index)
        self._data.pop(row_index)
        self.endRemoveRows()

        if self.indexer:  # more efficient to fix index but
            self.indexer.is_valid  = False

        # next may not be needed
        #self.layoutChanged.emit()
        #self.datatChanged.emit()
        #return True

    # ---------------------------
    def get_index_for_row(self, ix_row, column=0):
        """
        what it says, read
        index    = xxxx.get_index_for_row( ix_row )
        """
        return self.createIndex(ix_row, column)

    # ---------------------------
    def clear_data(self):
        """
        what it says, read
        """
        self.beginResetModel()
        self._data.clear()
        self.endResetModel()

        if self.indexer: # more efficient to fix index but
            self.indexer.is_valid  = False

# ---- eof
