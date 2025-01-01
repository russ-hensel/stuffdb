#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
custom versions oa QWidgets

see  qt_by_example for these widgets -- run this deom_custom_widgets.py

"""
# ---- tof

# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main_qt
    #main.main()
# --------------------


from PyQt5 import QtGui
from PyQt5.QtCore import QDate, QDateTime, QModelIndex, Qt, QTimer
from PyQt5.QtGui import QTextCursor, QCursor
# sql
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel

from PyQt5.QtWidgets import (QAction,
                             QApplication,
                             QButtonGroup,
                             QCheckBox,
                             QComboBox,
                             QDateEdit,
                             QGridLayout,
                             QGroupBox,
                             QHBoxLayout,
                             QLabel,
                             QLineEdit,
                             QListWidget,
                             QListWidgetItem,
                             QMainWindow,
                             QMenu,
                             QMessageBox,
                             QPushButton,
                             QRadioButton,
                             QSizePolicy,
                             QTableView,
                             QTableWidget,
                             QTableWidgetItem,
                             QTabWidget,
                             QTextEdit,
                             QVBoxLayout,
                             QWidget)

# ---- imports
import adjust_path

# ---- imports neq qt


# ---- begin pyqt from import_qt.py

#import sqlite3
#from   functools import partial
#import collections
import functools
import pdb
import traceback
#import subprocess
#from   subprocess import run
#from   subprocess import Popen, PIPE, STDOUT
#import datetime
from datetime import datetime
from functools import partial

#import  gui_qt_ext

# ---- QtCore
from PyQt5.QtCore import (QAbstractTableModel,
                          QDate,
                          QModelIndex,
                          QRectF,
                          Qt,
                          QTimer,
                          pyqtSlot)
from PyQt5.QtGui import (QIntValidator,
                         QPainter,
                         QPixmap,
                         QStandardItem,
                         QStandardItemModel)
# ---- QtSql
from PyQt5.QtSql import (QSqlDatabase,
                         QSqlQuery,
                         QSqlQueryModel,
                         QSqlRecord,
                         QSqlRelation,
                         QSqlRelationalDelegate,
                         QSqlRelationalTableModel,
                         QSqlTableModel)
# ---- not in standard imports
# ----QtWidgets Boxes, Dialogs
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

# ---- imports local
import string_util
from app_global import AppGlobal
import wat_inspector
import convert_db_display
#import  picture_viewer
#import  qt_with_logging
import file_browse

#

# # -------------------
# def do_convert_to( in_data, in_type, out_type ):
#     """
#     make everyting universal time

#     types
#         timestamp
#         timestamp_eof
#         timestamp_bod
#         timestamp epd
#         qdate      ....
#         qdate_eof
#             .....


#     """

# """
# I have 2 functions for converting between all combinations
# of qdates, qdatetimes, python datetimes, and timestamps

# could you write a set of tests using pytest for all the combinations?

# The functions are below.  If you see a mistake in the functions
# also let me know, but still create the tests.

# """


# def string_to( a_string, a_type ):
#     """
#     """
#     if  not isinstance( a_string, str ):
#         raise ValueError( f"a_string is not instnace of str  {a_string = } {type(a_string) = }" )

#     if a_type   == "int":
#         a_int  = int( a_string )
#         return a_int

#     else:
#         raise ValueError( f"Unsupported type {a_type = } {a_string = }")



# def int_to(   a_int, a_type  ):
#     """
#     """
#     if  not isinstance( a_int, int ):
#         raise ValueError( f"a_int is not instnace of int  {a_int = } {type(a_int) = }" )


# def datetime_to( a_datetime, a_type ):
#     """
#     convert datetimes to the output type indicated
#     by a_type
#     On errors just divide by 0
#     in mycase a_datetime called by other function must be a datetime but
#     have exception anyway
#     """
#     if  not isinstance( a_datetime, datetime ):
#         raise ValueError( f"a_datetime is not instnace of datetime  {a_datetime = } {type(a_datetime) = }" )

#     if a_type   == "timestamp":
#         timestamp  = int( a_datetime.timestamp() )
#         return timestamp

#     if a_type   == "qdatetime":
#         #qdatetime = QDateTime.fromPyDateTime( a_datetime )
#         qdatetime      = QDateTime(a_datetime.year, a_datetime.month, a_datetime.day,
#                        a_datetime.hour, a_datetime.minute, a_datetime.second)
#         return qdatetime

#     if a_type   == "qdate":
#         q_date = QDate(a_datetime.year, a_datetime.month, a_datetime.day)
#         return q_date

#     raise ValueError( f"Unsupported type {a_type = }")

class ValidationIssue(  Exception ):
    """
    see __init__
    """
    def __init__(self, why, widget   ):
        """
        use:
            raise custom.widgets.ValidationIssue( why, this_control )
            ValidationIssue( msg, this_control )
        try:
            self.load_file( file_name )
        except custom_widgets.ValidationIssue  as an_except:

            ....
            msg  = f"File Load failed, {an_except.why}"
            AppGlobal.gui.display_info_string( msg )
        """
        super( ).__init__(  why  )  # message
        self.control   = widget


# -----------------------
def set_data_to_default_prior_didnotwork( a_self   ):
    """
    function to set the default to the prior value
    uses prior value so should be correct type without
    conversion
    for testing to zzzz
    or could make instance ov base class ?
    """
    a_self.set_preped_data( a_self.prior_value, is_changed = True )
    pass # debug

# -----------------------
def validate_no_z( a_string   ):
    """
    a debug thing
    what type need models be? -- think should throw except
    """
    msg      = None
    if "z" in a_string:
        msg   = "validate_no_z no zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
        print( msg )
    return msg

# -----------------------
def model_dump(  model, msg = "model dump msg" ):
    """
    a debug thing
    what type need models be?
    """
    print( "model_dump begin may want to add back for infomation about  not ia any more ")

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
            data    = model.data(index)
            row_data.append(data)
            if   column == 2:
                table_name = data
            elif column == 1:
                table_id = data

        print(f"Row {row}: {row_data}")
    print( "model_dump end")


# -----------------------------------
class CQGridLayout( QGridLayout ):
    """
    !! to do --- whold thing make go across only -- at least for now

    to do
    add column span row span -- keep delta ? delta is span in direction, but may need both ?
    add setup for stickyness ??
    tested through my use, works in my apps, but may nt even be used

    placer    = gui_qt_ext.PlaceInGrid( 99,  central_widget = a_widget, by_rows = False )
    placer.place(  a_widget, columnspan = None,   rowspan = None, sticky = None )

    Interface
        tried to use _xxx for non interface functions and var
        debug_id

    """
    def __init__( self,  central_widget, a_max = 0, by_rows = True  ):
        """
        and see class doc.... combine
        uses  layout a QGridLayout()
        placer = gui_qt_ext.PlaceInGrid( parent_widget, a_max, by_rows = False)
        Args:
               parent_widget  container for the widges that this will place
                a_max, may want to change to by name and default to 0 which is unlimited
                by_rows  --- require name ?? default

        """
        # if central_widget:
        #     self.central_widget = central_widget
        # else:
        #     print( "creating central widget " )
        #     self.central_widget = QWidget()

        # a_window.setCentralWidget( self.central_widget )

        # self.window   = a_window   # for later ref

        # if layout:
        #     self.layout   = layout
        # else:
        #     print( "creating layout" )
        #     self.layout   = QGridLayout()

        self.central_widget = central_widget
        self.layout         = QGridLayout()
        if  isinstance(  central_widget,  QVBoxLayout ):  # should be more here
            self.central_widget.addLayout( self.layout )
        else:
            self.central_widget.setLayout( self.layout )

        #rint( f"PlaceInGrid __init__ central_widget.layout(){ central_widget.layout()} " )
        self.debug_id       = "default_id"  # use as part of interface
        self.max            = a_max
        self.ix_row         = 0
        self.ix_col         = 0     # ix_col   += 1 to move across one
        self.ix_col_max     = 0 # may be used by filler
        self.by_rows        = by_rows
        self.indent         = 0    # interface and set by new_row
        if by_rows:
            self.function =  self._place_down_row_
        else:
            self.function =  self._place_across_col_

    # -----------------------------------
    def addWidget( self,
               a_widget,
               columnspan   = None,
               rowspan      = None,
               sticky       = None
               ):
        """
        to work like QLayouts
        """
        self.place(
               a_widget     = a_widget,
               columnspan   = columnspan,
               rowspan      = rowspan,
               sticky       = sticky
               )

    # -----------------------------------
    def place( self,
               a_widget,
               columnspan   = None,
               rowspan      = None,
               sticky       = None
               ):
        """

        move row or column by delta grid spacings after pacing control
        what is row span vs deltac
        args:
            widget     -> the widget being placed
            columnspan -> the column span               left over from tk not implemented
            rowspan    -> the rowspan                    left over from tk not implemented
            sticky     -> temporary override of sticky via argument   left over from tk not implemented
        """
        if columnspan is None:
            columnspan = 1

        if rowspan is None:
            rowspan    = 1

        #app_global.print_debug( f"row,co = {self.ix_row}, {self.ix_col}" )
        self.function( a_widget,  columnspan = columnspan, rowspan = rowspan, sticky = sticky )

    # -----------------------------------
    def place_filler( self,  stretch   = 1, widget = None  ):
        """
        place a filler widget that will streach
        filler is layed out in the central_widget layout ?
        need to fix for widget = None
        """
        #rint( f"&&&&&&&&&& place_filler {self}")

        widget          = QWidget()
        widget          = QGroupBox( f"filler {self.debug_id}" )   # just for debugging

        # which of next ??
        ix_col_stretch  = self.ix_col_max + 1
        ix_col_stretch  = self.ix_col + 1

        self.layout.setColumnStretch( ix_col_stretch, stretch )
        print( f"-------- end place filler  ----- col >{ix_col_stretch}<  row >{self.ix_row}< ---- {stretch}-----")
        # seems keywords not allowed in addWidget, just by position
        self.layout.addWidget(  widget,
                                self.ix_row,
                                ix_col_stretch ,
                                # column_span,       # columnSpan -1, then the widget will extend to the
                                                    #     bottom and/or right edge, respectively.
                                # row_span,          # rowSpan

                                #1,    #Alignment or flag  Qt.Alignment()]]])     # is it a list ? The alignment is specified by alignment .
                                                    #The default alignment is 0, which means that the widget fills the entire cell.
                                )

    # -----------------------------------
    def _place_down_row_( self, a_widget, columnspan, rowspan, sticky = None ):
        """
        one of the value intended for self.function
        does its name
        not much tested
        need to add sticky
        """
        # if sticky is None:
        #     sticky = self.sticky

        #rint( f"_place_down_row_ row = {self.ix_row} col = {self.ix_col}"  )
        # a_widget.grid( row          = self.ix_row,
        #               column        = self.ix_col,
        #               rowspan       = rowspan,
        #               sticky        = sticky,  )
        1/0

        self.layout.addWidget( a_widget,
                               self.ix_row,
                               self.ix_col ,
                               columnSpan     = columnspan,
                               rowSpan        = rowspan,    )

        self.ix_row += rowspan
        if ( self.max > 0  ) and ( self.ix_row >= self.max ):
            #rint( f"{self.debug_id} hit max row {self.max}"  )
            self.ix_col += 1
            self.ix_row  = 0

    # -----------------------------------
#    delta_row_col( delta_row, delta_col )
#    add a span argument
    # -----------------------------------
    def new_column( self, delta = 1,  ):
        """
        start a new column in row 0
        for going down columns not aacross

        """
        self.ix_row     = 0
        self.ix_col     += delta

    # -----------------------------------
    def new_row( self, delta_row = 1, indent = None ):
        """
        start a new row in col 0
        !! also for col
        """
        if indent is None:
            indent = self.indent    # or vise versa
        else:
            self.indent = indent
        self.ix_row     += delta_row
        self.ix_col      = indent

        # -----------------------------------
    def dwn_and_back( self,  delta_row = 1 ):
        """
        just an idea
        for now just us direct manipulation of ix_row, ix_col
        go dwn row and back column
        to set up directly below last placement
        delta_row = 1 !! add this
        set up for next placer, then will need a self.ix_row     -= 1
        """
        self.ix_row     += 1
        self.ix_col     -= 1

    # -----------------------------------
    def set_row( self, row,  ):
        """
        what if beyond max
        """
        self.ix_row = row

    # -----------------------------------
    def set_col( self,  col ):
        """
        what it says, why not just the property

        """
        self.ix_col = col

    # -----------------------------------
    def _place_across_col_( self, a_widget, *, columnspan,  rowspan, sticky, ):
        """
        # layout.addWidget(text_edit, 4, 0, 1, 3)  # Row 4, Column 0, RowSpan 1, ColumnSpan 3
        what it says
        one of the value intended for self.function
        args:
            widget     -> the widget being placed
            columnspan -> the column span
            rowspan    -> the rowspan
            sticky     -> temporary override of sticky via argument
        """
        #rint( f"_place_across_col_ row = {self.ix_row} col = {self.ix_col}"  )
        # defaulting should be done in place
        # if columnspan is None:
        #     columnspan = 1

        # if rowspan is None:
        #     rowspan = 1

        # probably wrong but not using sticky
        if sticky is None:
            self.sticky = sticky

        #rint( f"_place_across_col_ ({self.ix_col}, {self.ix_row})"
        #                               f"columnspan = {columnspan}" )
        #rint( f"for {self.debug_id} placing   {a_widget}  at {self.ix_col}, row {self.ix_row}")
        #	addWidget(QWidget *widget, int stretch = 0, Qt::Alignment alignment = Qt::Alignment())

        self.layout.addWidget( a_widget,
                               self.ix_row,
                               self.ix_col,
                               rowspan,
                               columnspan,
                               )
        # ---- code that may be useful?
        # self.gridLayout.addWidget(textEdit1, 0, 0)
        # self.gridLayout.addWidget(textEdit2, 1, 1)
        # self.gridLayout.addWidget(textEdit3, 0, 1)
        # self.gridLayout.setColumnStretch(0, 1)
        # self.gridLayout.setColumnStretch(1, 3)
        # self.gridLayout.setRowStretch(0, 3)
        # self.gridLayout.setRowStretch(1, 1)



        # self.layout.addWidget( a_widget,
        #                        self.ix_row,
        #                        self.ix_col,
        #                        rowspan,              # streah
        #                        # sticky,  #  Qt.AlignCenter,       # allignment ??    Qt.AlignCenter works but makes a mess
        #                        )

        self.ix_col         += columnspan
        self.ix_col_max      = max( self.ix_col_max, self.ix_col )
        if ( self.max > 0  ) and ( self.ix_col >= self.max ):
            #rint( f"hit max row {self.max}"  )
            self.new_row()

        #rint("_place_across_col_",  self.ix_row, self.ix_col  )
        #rint( f"end placing   self = {self}  ") 2023-08-03 10:18:53

    # -----------------------------------
    def __str__( self,   ):
        """
        what is says, read, for debugging

        """
        a_str = f"/n>>>>>>>>>>* __str__ for PlaceInGrid  debug id =  {self.debug_id} * <<<<<<<<<<<<"
        a_str = f"{a_str}\n   ix_row                 {self.ix_row }"
        a_str = f"{a_str}\n   ix_col                 {self.ix_col }"

        a_str = f"{a_str}\n   ix_col_max             {self.ix_col_max}"

        #a_str = f"{a_str}\n   function               {self.function}"
        # a_str = f"{a_str}\n   xxx        {self.xxx}"
        return a_str

# --------------------------------------
class ModelIndexer( object ):
    """
    so we can do a find inside same sort of model ... later
    make an extension to the model..
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
        self.is_valid       = False

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
        not clear why using a set
        set if the index is valid, if not find will reindex
        """
        self.is_valid   = a_bool

    # -----------------------------------
    def create_index( self, ):
        """
        will not index dups
        """
        model        = self.model
        row_count    = model.rowCount()

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
        return
            row in model, else none
            row_or_none   = model_indexer.find( key )
        """
        if not self.is_valid:
            self.create_index()

        row     = self.index_dict.get( key, None )
        return row

# ------------------------
class TableModel( QAbstractTableModel ):
    """
    for a table display
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

    #-------
    def rowCount(self, index=None):
        """
        what it says read
        why index = None, drop it
        """
        return len(self._data)

    def columnCount(self, index=None):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def set_data(self, data ):
        self._data      = data

    # def add_data(self, data ):
    #     pass

    def set_data_at_index(self, index, value, role=Qt.EditRole):
        """
        index might be index = model.index(ix_row,  ix_col )  # Row 1, Column 1

        Args:
            index (TYPE): DESCRIPTION.
            value (TYPE): DESCRIPTION.
            role (TYPE, optional): DESCRIPTION. Defaults to Qt.EditRole.

        Returns:
            bool: DESCRIPTION.

        """
        if role == Qt.EditRole:
            self._data[index.row()][index.column()] = value  # Update the data
            self.dataChanged.emit(index, index, [Qt.DisplayRole])
                # Emit dataChanged signal for this index
            return True
        return False

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]
            elif orientation == Qt.Vertical:
                return str(section + 1)

    # Method to add a row
    def addRow(self, row_data):
        """
        read
        row_data   a list of the data types ??
        remember to invalidate index if any --- may build in or not
        """
        self.beginInsertRows(self.index(len(self._data), 0), len(self._data), len(self._data))
        self._data.append(row_data)
        self.endInsertRows()

    # Optional method to remove a row
    def removeRow(self, row_index):
        """
        what it says, read
        """
        self.beginRemoveRows(self.index(row_index, 0), row_index, row_index)
        self._data.pop(row_index)
        self.endRemoveRows()

    # ---------------------------
    def clear_data(self):
        """
        what it says, read
        """
        self.beginResetModel()
        self._data.clear()
        self.endResetModel()

#-------------------------------
class CQComboBoxEditCriteria( QComboBox ):
    """
    read it
    custom_widgets.CQLineEditCriteria( get_type = "string", set_type = "string")
    """
    def __init__(self,
                 parent             = None,
                 #data_field_name    = None,
                 get_type       = "string",
                 set_type       = "string" ):
        """
        read it
        in   -- into the widget
        out  -- out to the record

        work to do
            check context menu

            document formatting


        """
        super(   ).__init__( parent  )
        # if not data_field_name:
        #     1/0
        # self.data_field_name       = data_field_name
        self.get_type             = get_type
        self.set_type             = set_type

        self.default_type          = "value"    # value will be a string
        self.default_value         = ""

        self.default_type          = "index"    # value will be an Int
        self.default_value         = 0
        self.criteria_name         = "not set"

    #-----------------------------
    def get_data( self ):
        """
        read it
        later will have type conversion
        """
        data     = self.currentText()
        # if self.data_out_type == "integer":
        #     ret    = int( data )
        #     return ret

        ret    = data
        return ret

    #--------------------------------
    def build_criteria( self, a_dict ):
        """mutate the dict for criterial  """
        print( f"CQComboBoxEditCriteria {self.get_data()}")
        a_dict[ self.critera_name ] = self.get_data()

    #-----------------------------
    def set_data( self, data ):
        """
        read it
        not checking in_type for now only string
        for now convert to string
        """
        #if self.r_type == "integer":
        data    = str( data )
        self.setCurrentText( data )

    # #-----------------------------
    # def set_data_default( self, data = None ):
    #     """
    #     read it
    #     """
    #     if data is None:
    #         data = ""
    #     self.setText( data )

    # @property
    # def data_value( self ):
    #     #rint( "@property datagetter" )
    #     ret   = self.get_data_out()
    #     #rint( ret )
    #     return ret
    #     #return "joe"

    # # ---------------------------------
    # @data_value.setter
    # def data_value(self,  arg ):
    #     #rint( "@data.setter" )
    #     self.set_data_in( arg )

    #----------------------------
    def set_data_default( self ):
        """
        might want to route thru set_data
        """
        if   self.default_type  == "index":
             self.setCurrentIndex( self.default_value )

        elif self.default_type  == "value":
            self.setText( self.default_value )
            #self.default_value

        else:
            msg    = f"CQLineEditCriteria  this_is_an_exception_message {self.default_type = }"

            print( msg )
            AppGlobal.logger.error( msg )    # debug info warning, error critical
            raise ValueError( msg, )


#-------------------------------
class CQLineEditCriteria( QLineEdit ):
    """
    read it
    custom_widgets.CQLineEditCriteria( get_type = "string", set_type = "string")
    """
    def __init__(self,
                 parent             = None,
                 #data_field_name    = None,
                 get_type      = "string",
                 set_type       = "string" ):
        """
        read it
        in   -- into the widget
        out  -- out to the record

        work to do
            check context menu
            on date change remove ignore date
            document formatting

        """
        super(   ).__init__( parent  )
        # if not data_field_name:
        #     1/0
        # self.data_field_name       = data_field_name
        self.get_type              = get_type
        self.set_type              = set_type
        self.default_type              = "value"    # value will be a string
        self.default_value         = ""

    #-----------------------------
    def get_data( self ):
        """
        read it
        later will have type conversion
        """
        data     = self.text()
        # if self.data_out_type == "integer":
        #     ret    = int( data )
        #     return ret

        ret    = data
        return ret

    #--------------------------------
    def build_criteria( self, a_dict ):
        """mutate the dict for criterial  """
        a_dict[ self.critera_name ] = self.get_data()
    #-----------------------------
    def set_data( self, data ):
        """
        read it
        not checking in_type for now only string
        for now convert to string
        """
        #if self.r_type == "integer":
        data    = str( data )
        self.setText( data )

    # #-----------------------------
    # def set_data_default( self, data = None ):
    #     """
    #     read it
    #     """
    #     if data is None:
    #         data = ""
    #     self.setText( data )

    # @property
    # def data_value( self ):
    #     #rint( "@property datagetter" )
    #     ret   = self.get_data_out()
    #     #rint( ret )
    #     return ret
    #     #return "joe"

    # # ---------------------------------
    # @data_value.setter
    # def data_value(self,  arg ):
    #     #rint( "@data.setter" )
    #     self.set_data_in( arg )

    #----------------------------
    def set_data_default( self ):
        """
        """

        if   self.default_type  == "xxxx":
             self.setDate(QDate.currentDate() )

        elif self.default_type  == "value":
            self.setText( self.default_value )
            #self.default_value

        else:
            msg    = f"CQLineEditCriteria  this_is_an_exception_message {self.default_type = }"

            print( msg )
            AppGlobal.logger.error( msg )    # debug info warning, error critical
            raise ValueError( msg, )

# --------------------------------
class CQDateCriteria( QWidget,  ):
    """
    custom_widget.pb   as CQDateEdit
    custom_widgets.CQDateEdit()
    """
    def __init__(self,
                 parent             = None,
                 # data_field_name    = None,
                 set_type           = "qdate",
                 get_type           = "ts_bod" ):   # dt_bod .....
        """
        read it
        """
        super(   ).__init__( parent  )
        self.parent            = parent

        self.get_type          = get_type    # type comming out from qdate
        self.set_type          = set_type    # type comming in to set qdate
        self.ignore_cb_widget  = None
        self.default_type      = None
        self._build_gui()

    #---------------------------
    def __getattr__(self, name):
        """
        this is the magic that calls the date control functions
        from this object
        priority goes to this object then QDateEdit

        """
        if name in self.__dict__:
            return self[name]

        try:
            return getattr(self.date_edit_widget, name)

        except AttributeError:
            raise AttributeError(
                "'{}' object has no attribute '{}'".format(
                    self.__class__.__name__, name
                )
            )

    # ------------------------------------------
    def _build_gui( self,   ):
        """
        what it says
        """
        layout                  = QHBoxLayout( self )

        widget                  = QCheckBox( "Ignore\nDate")
        self.ignore_cb_widget   = widget
        layout.addWidget( widget,  stretch = 0 )

        widget                  = QDateEdit()
        self.date_edit_widget   = widget
        self.setCalendarPopup( True )
        layout.addWidget( widget,  stretch = 2 )

        widget.setCalendarPopup( True )

        widget.setDate(QDate.currentDate())

    # ----------------------------
    def set_date( self, date, set_type =  None  ):
        """
        set the date, if Non checked ignore
              and set the dates to !! ??
        else uncheck and set the date to the correct type
        this guy is not finished
        """
        if not set_type:
            set_type  = self.set_type

        if date is None:
            self.ignore_cb_widget.setChecked( True )
            print( "CQDateCriteria set_date still need self.setsomething" )
            return

        try:
            qdate = convert_db_display.date_criteria_from_to( date, set_type, "qdate" )

        except Exception as an_except:   #  or( E1, E2 )

            msg     = f"a_except         >>{an_except}<<  type  >>{type( an_except)}<<"
            print( msg )
            AppGlobal.logger.error( msg )

            msg     = f"an_except.args   >>{an_except.args}<<  {self.field_name = } "
            print( msg )
            AppGlobal.logger.error( msg )

            s_trace = traceback.format_exc()
            msg     = f"format-exc       >>{s_trace}<<"
            print( msg )
            AppGlobal.logger.error( msg )

            raise

        self.setDate( qdate )

        self.ignore_cb_widget.setChecked( False )
        print( "CQDateCriteria set_date still need self.setsomething" )

    # ----------------------------
    def get_date( self, get_type = None   ):
        """
        return None if ignore is checked else the propre conversion
        of the date
        valid types are qdate and various timestamps as ints
        """
        if self.ignore_cb_widget.isChecked():
            return None

        if not get_type:
            get_type = self.get_type

        qdate   = self.date()

        try:    # can we factor all into our parent?
            data    = convert_db_display.date_criteria_from_to( qdate, "qdate", get_type )


        except Exception as an_except:   #  or( E1, E2 )

            msg     = f"a_except         >>{an_except}<<  type  >>{type( an_except)}<<"
            print( msg )
            AppGlobal.logger.error( msg )

            msg     = f"an_except.args   >>{an_except.args}<<  {self.field_name = } "
            print( msg )
            AppGlobal.logger.error( msg )

            s_trace = traceback.format_exc()
            msg     = f"format-exc       >>{s_trace}<<"
            print( msg )
            AppGlobal.logger.error( msg )

            raise



        #rint( "get_date alway a timestamp untill fixed ")
        # data   = self.get_data_as_timestamp()

        return data

    #--------------------------------
    def build_criteria( self, a_dict ):
        """mutate the dict for criterial  """
        print( "CQDateCriteria build_criteria dates not yet right " )
        a_dict[ self.critera_name ] = self.get_date()


    # --------------------------------
    def contextMenuEvent(self, event):
        # Create the context menu
        context_menu = QMenu(self)

        # Add custom actions
        clear_action = QAction("Clear Date", self)
        today_action = QAction("Set to Today", self)

        # Connect actions to methods
        clear_action.triggered.connect(self.clear_date)
        today_action.triggered.connect(self.set_to_today)

        # Add actions to the menu
        context_menu.addAction(clear_action)
        context_menu.addAction(today_action)

        # Show the context menu
        context_menu.exec_(event.globalPos())

    def clear_date(self):
        """
        probally not right set to date None
        """
        self.clear()  # Clears the QDateEdit

    def set_data_default( self ):
        """
        data not date to agree with other criteria widgets
        """
        print( "date_criteria  set_data_default need more")
        #self.set_date( None )
        self.ignore_cb_widget.setChecked( True )

    def set_date_today(self):
        """
        no conversion necessary as all qdate


        """
        self.date_edit_widget.setDate(QDate.currentDate())  # Sets date to today

    # # --------------------------------
    # @property
    # def data_value( self ):
    #     """
    #     beware4 date is a function of the widget
    #     """
    #     #rint( "@property datagetter" )
    #     ret   = self.get_date()
    #     #rint( ret )
    #     return ret

    # # ---------------------------------
    # @date_value.setter
    # def data_value(self,  arg ):
    #     """
    #     beware4 date is a function of the widget
    #     """
    #     #rint( "@data.setter" )
    #     self.set_date( arg )


# ---- Edits not Critria ------------------------------------


# ---------------------------------
class CQEditBase(   ):
    """
    second parent for QT edit child controls

    do we need both?  what is the differance
    set_to_default
    clear_data

    """
    def __init__(self,
                 parent             = None,
                 field_name         = None,
                 display_type       = "qdate",
                 db_type            = "timestamp" ):
        """
        read it
        timestammp is an int
        in   -- into the widget
        out  -- out to the record
        """
        # print( "        begin init CQEditBase")
        # super(   ).__init__(   )  no parent
        self.context_menu        = None  # override if one is added
        if not field_name:
            pass
            #rint( "!! CQEditBase need except here ??")
            # 1/0
        # can be used as interface
        self.field_name            = field_name
        self.db_type               = db_type
        self.display_type          = display_type   #
            # for this control I think dispaly type must alsway be qdate
            # for edit I think must alsways be string
        #self.is_constant           = False
        is_editable                 = True  #  --- by the user   may be built in
                                        # will nee a configur for it
        self.validate               = self.validate_all_ok


        # ---- these are private change to _
        # prior value, prior_type -- likely already in edit
        self.prior_value           = None     # value last set from a record ot to record
                                                # set to something balid for edit in its init
            # in db_type

        self.is_changed             = False    # by user or default

        # next probably in closure for the function
        self.default_value                = "value_of_self_default_value"  # may or may not be used
        self.clear_value                  = "value_of_self_clear_value"    # may or may not be used
        # Set an initial date (optional)
        #self.setDate( QDate.currentDate() )

        # next should be done in descandant
        # self.default_type          = "today"   # need begin of day, endo of day ??
        # self.default_value         = None     # if used make a qdate

        # print( "        end init CQEditBase")


    #----------------------------
    def show_context_menu(self, global_pos):
        """ chat code, modified a bit """
        self.context_menu.exec( global_pos )

    #----------------------------
    def handle_right_click(self, event):
        """ chat code, modified a bit """
        if event.button() == Qt.RightButton:
            self.show_context_menu(event.globalPos())
        # else:
        #     # Call the parent class method for other events
        #     super(QLineEdit, self.line_edit).mousePressEvent(event)

    #----------------------------
    def set_data( self, in_data, in_type ):
        """
        what it says read
            takes the in_data in the type in_type and puts it
            into the field
            also recording prior_data ??

                !! still need prior_data
        we will set the in_data, but need to know the type
        do not need diaplay_type we know it
        will be some sort of qdate always for this widget
        * will reset prior value
        import convert_db_display.py
        convert_db_display.convert_from_to( )

        .set_data( 22, "integer" )
        """
        # out data is output of coversion, needs to be put into the display field

        debug_display_type    = self.display_type
        debug_field_name      = self.field_name
        # !! not sure this should be in in long term
        if self.field_name == "id":
            msg   = f"set_data {id = } {self.is_changed = }"
            print( msg )
            # breakpoint( )
            pass

        try:
            out_data   = convert_db_display.convert_from_to( in_data, in_type, self.display_type )
            # all display types for this control are some kind of qdate

        except Exception as an_except:   #  or( E1, E2 )

            msg     = f"a_except         >>{an_except}<<  type  >>{type( an_except)}<<"
            print( msg )
            AppGlobal.logger.error( msg )

            msg     = f"an_except.args   >>{an_except.args}<<  {self.field_name = } "
            print( msg )
            AppGlobal.logger.error( msg )

            s_trace = traceback.format_exc()
            msg     = f"format-exc       >>{s_trace}<<"
            print( msg )
            AppGlobal.logger.error( msg )

            raise

        # all for prior value
        if in_type == self.db_type:
            # the convert might be ok as would set to nothing
            self.prior_value = in_data

        else:
            try:
                self.prior_value = convert_db_display.convert_from_to( in_data, in_type, self.db_type )

            except Exception as an_except:   #  or( E1, E2 )

                msg     = f"a_except         >>{an_except}<<  type  >>{type( an_except)}<<"
                print( msg )
                AppGlobal.logger.error( msg )

                msg     = f"an_except.args   >>{an_except.args}<<  {self.field_name = } "
                print( msg )
                AppGlobal.logger.error( msg )

                s_trace = traceback.format_exc()
                msg     = f"format-exc       >>{s_trace}<<"
                print( msg )
                AppGlobal.logger.error( msg )

                raise

        if out_data is None:
            self.is_changed = False
            print( f"CQEditBase set_data  is_changed set to false {self.field_name}")
            return
        self.is_changed      = True
        self.set_preped_data( out_data  )
        # doe we set is_changed here

    #----------------------------
    def set_preped_data( self, data,   ):
        """'
        final step from set_data should alway be qdate for a date edit....
        is it generally overriden?
        """
        1/0  # should be in descandant
        # ex:
        self.setDate( data  )

    #----------------------------
    def get_raw_data( self, ):
        """'
        may be intended to get data in typed format
        comment is wrong  -- final step from set_data should alway be qdate
        """
        1/0 # should be in descandant
        qdate   = self.date()
        return qdate

    #-----------------------------
    def set_data_to_defaultxxxx( self,   ):
        """
        prior value will be reset
        is_change will be true
        data will be in display
        record is not changed

        looks like it is being overriden in all descandnts
        why is ther date stuff here
        """
        print( "CQEditBase set_data_to_default should override in child")
        return


        # if from_prior_value:
        #     # !! what if none
        #     #self.clear()  # Clears the QDateEdit
        #     self.set_data( self.prior_value, self.db_type )

        # elif   self.default_type  == "today":
        #      value   = QDate.currentDate()
        #      self.set_data( value, "qdate" )

        # elif self.default_type  == "qdate":
        #     # sets a fixed qdate stored in default value
        #     self.set_data( self.default_value, "qdate"  )

        # else:
        #     1/0

        # self.is_changed   = True

    # -----------------------
    def set_data_to_prior( self   ):
        """
        often replaced with ... set_data_to_prior_value( self   )
        but could be clear or default or pass
        """
        1/0
        self.set_preped_data( self.prior_value, is_changed = True )
        pass # debug

    # -----------------------
    def set_data_to_clear( self   ):
        """
        often replaced with ... set_data_to_prior_value( self   )
        but could be clear or default or pass
        """
        print( "set_data_to_clear should have been overridden " )
        pass # debug

    # ---- do_data_to are implenentations for some of the sets, see comments
    # -----------------------
    def do_data_to_keep_prior_what( self   ):
        """
        often replaced with ... set_data_to_prior_value( self   )
        but could be clear or default or pass
        for default just indicate that it is changed
        """
        self.on_data_changed()
        pass # debug

    # -----------------------
    def do_data_to_prior_value( self   ):
        """
        function to set the default to the prior value
        uses prior value so should be correct type without
        conversion
        for testing to zzzz
        or could make instance ov base class ?
        """
        self.set_preped_data( self.prior_value, is_changed = True )
        pass # debug


    # -----------------------
    def do_data_to_default_value( self, default_value  ):
        """
        complete this code:
            set_data_to_default    = partial( set_data_to_default, "")
        function to set the default to a value
        should be correct type without  conversion

        """
        print( "set_data_to_default_value" )
        self.set_preped_data( default_value, is_changed = True )
        pass # debug

    # -----------------------
    def do_data_to_self_default( self   ):
        """
        depricte
        function to set the default to the prior value
        uses prior value so should be correct type without
        conversion
        for testing to zzzz
        or could make instance ov base class ?
        set_data_default
        better to keep value in a closure
        """
        self.set_preped_data( self.default_value, is_changed = True )
        pass # debug


    # -----------------------
    def set_data_to_default( self   ):
        """
        function to set the default to the prior value
        uses prior value so should be correct type without
        conversion
        for testing to zzzz
        or could make instance ov base class ?
        set_data_default
        better to keep value in a closure
        """
        print( "set_data_to_default should be replaced ")
        1/0
        #self.set_preped_data( self.default_value, is_changed = True )
        pass # debug


    # -----------------------
    def set_data_to_pass( self   ):
        """
        a nop function for other set datas
        but   sets is_changed
        """
        pass
        self.is_changed   = True


    # def set_data_to_default( self   ):
    #     """slot for a function to be plugged in else does nothing
    #     which is probably wrong"""
    #     print( "set_data_to_default" )

    #-----------------------------
    def set_data_from_record( self, record ):
        """
        read it
        !! need prior_data -- done in set_data
        !! utc?
        """
        debug_fn   =  self.field_name
        #rint( f"set_data_from_record {debug_fn}")
        data       = record.value(  self.field_name  )
        #rint( f"{data = } {self.db_type = }")

        if data is None:
            self.is_changed    = False
            print( f"CQEditBase set_data_from_record None in display think this is ok {self.field_name}")
            return

        self.set_data( data, self.db_type, )
        # qdate     =self. do_convert_to( data, self.db_type, self.display_type )
        #     # should alway get some kind of qdate
        # self.setDate( qdate )
        # self.prior_value   = data
        self.is_changed    = False
        if self.field_name == "id":
            print( f"CQEditBase set_data_from_record 2    {self.field_name}")

    # #-----------------------------
    # def raise_validate_issue( self, msg ):
    #     """
    #     ??
    #     """
    #     raise ValidationIssue( msg , self )
    #-----------------------------
    def validate_all_ok( self ):
        """
        pretty much a no op, just do not throw an exception
        default for the base class
        """
        return

    #-----------------------------
    def validate_is_int( self ):
        """
        could make class an argument to the function
        may raise exception
        """
        data   = self.get_raw_data().strip()
        if data == "":
            return
        # just thro for now
        int_maybe   = int( data )

    #-----------------------------
    def validate_max_int( self, max_int ):
        """
        could make class an argument to the function
        may raise exception
        """
        # self.validate_is_int( )
        data   = self.get_raw_data().strip()
        if data == "":
            return
        # just thro for now
        int_maybe   = int( data )
        if int_maybe > max_int:
            raise ValueError( "int too big ")

    #-----------------------------
    def validate_max_length( self, max_len ):
        """
        may only work on string types
        use as partial:
            self.validate    = partial( validate_max_len, max_len = 2 )
        may raise exception
        """
        data   = self.get_raw_data()
        if len( data ) > max_len:
            msg     = f"validate_max_length need a good message {max_len = }"
            raise ValueError( msg )

    #-----------------------------
    def validate( self ):
        """
        need to return a message could be thru and exception or just
        a return value for now None or "" means ok else
        contain an error message
        this needs work for now just checking it it called
        !! look in descendant
        plug in this function
        """
        1/0   # in descendant -- or move here ??
        print( f"CQEditBase get_data_for_record {self.field_name = }")

        if self.field_name == "add_kw":
             pdb.set_trace()

        if self.validate_function:
            return self.validate_function( self.get_raw_data )
        return None  #

    #-----------------------------
    def get_data_for_record( self, record, record_state ):
        """
        read it
        self.id_field.set_r_type(    record.value(    "id"       ))
        record.setValue( "add_kw",     self.add_kw_field.text())
        """
        # --- do we need othr status checks
        # --- do we need othr status checks

        #rint( f"get_data_for_record {self.field_name = }")
        if self.field_name == "id":
            #breakpoint( )
            debug_is_changed   = self.is_changed
            pass

        #debug_break   = 1

        if not self.is_changed:
            # we just do not bring anyting back
            return

        raw_data    = self.get_raw_data( )
        #qdate       = self.date()
        debug_var   = ( raw_data, self.display_type, self.db_type )

        try:
            data        = convert_db_display.convert_from_to( raw_data, self.display_type, self.db_type )

        except Exception as an_except:   #  or( E1, E2 )

            msg     = f"a_except         >>{an_except}<<  type  >>{type( an_except)}<<"
            print( msg )
            AppGlobal.logger.error( msg )

            msg     = f"an_except.args   >>{an_except.args}<<  {self.field_name = } "
            print( msg )
            AppGlobal.logger.error( msg )

            s_trace = traceback.format_exc()
            msg     = f"format-exc       >>{s_trace}<<"
            print( msg )
            AppGlobal.logger.error( msg )

            raise

        # conversions here or in get_data_out   --- save prior value
        record.setValue( self.field_name, data )
        self.prior_value  = data
        self.is_changed   = False
        if self.field_name == "id":
            print( f"CQEditBase get_data_for_record     {self.field_name}")

    # ------------------------------------
    def on_data_changed( self, ): # new_text):
        """
        on_data_changed( self, new_text):  xxx no new_text sent for text changed
        data may be sent for textEdited
        !! make sure is hooked to control --- may be missing from some
        """
        self.is_changed   = True

    # ------------------------------------
    def clear_data( self, to_prior ):
        """
        may be edited or messed with
        on data change for each drop the new data
        think the set_data_to_clear is what should be used
        """
        1/0
        print( "need implementation zzzz clear_data ")

    # ------------------------------------
    def print_str( self,   ):
        """
        may be edited or messed with
        on data change for each drop the new data
        """
        print( self )

    def __str__( self ):
        a_str   = ""
        a_str   = ">>>>>>>>>>* CQEditBase *<<<<<<<<<<<<"

        a_str   = string_util.to_columns( a_str, ["clear_value",
                                           f"{self.clear_value}" ] )
        a_str   = string_util.to_columns( a_str, ["context_menu",
                                           f"{self.context_menu}" ] )
        a_str   = string_util.to_columns( a_str, ["db_type",
                                           f"{self.db_type}" ] )
        a_str   = string_util.to_columns( a_str, ["default_type",
                                           f"{self.default_type}" ] )
        a_str   = string_util.to_columns( a_str, ["default_value",
                                           f"{self.default_value}" ] )
        a_str   = string_util.to_columns( a_str, ["display_type",
                                           f"{self.display_type}" ] )
        a_str   = string_util.to_columns( a_str, ["field_name",
                                           f"{self.field_name}" ] )
        a_str   = string_util.to_columns( a_str, ["is_changed",
                                           f"{self.is_changed}" ] )
        a_str   = string_util.to_columns( a_str, ["prior_value",
                                           f"{self.prior_value}" ] )
        a_str   = string_util.to_columns( a_str, ["set_data_to_default",
                                           f"{self.set_data_to_default}" ] )
        a_str   = string_util.to_columns( a_str, ["set_data_to_prior",
                                           f"{self.set_data_to_prior}" ] )
        a_str   = string_util.to_columns( a_str, ["validate",
                                           f"{self.validate}" ] )
        return a_str


#-------------------------------
class CQLineEdit( QLineEdit, CQEditBase ):
    """
    read it
    custom_widgets.CQLineEdit
    """
    def __init__(self,
                 parent             = None,
                 field_name         = None,
                 display_type       = "string",
                 db_type            = "string" ):

        """
        read it
        in   -- into the widget
        out  -- out to the record
        """
        #super(   ).__init__(   )   # seems to go to CQEditBase ???

        QLineEdit.__init__( self, None  )     # need arg ?

        CQEditBase.__init__( self,
                        parent             = parent,
                        field_name         = field_name,
                        display_type       = display_type,
                        db_type            = db_type )


        self.default_type          = "string"          # depricate
        self.default_value         = "default-value"     # depricate
        self.prior_value           = ""  # something of a valid type
        self.textEdited.connect(self.on_text_changed )  #  text is sent new_text
        #self.textChanged.connect(self.on_text_changed)
            #-----------------------------

        # should have default, prior ....

        a_partial                    = partial( self.do_data_to_default_value, "to default" )
        self.set_data_to_default     = a_partial

        self.set_data_to_prior       = self.set_data_to_prior

        self._build_context_menu()

    # -------------------------
    def _build_context_menu( self ):
        """ """

        context_menu        = QMenu(self)
        self.context_menu   = context_menu

        # Add actions for common operations
        undo_action     = context_menu.addAction("Undo")
        undo_action.triggered.connect(self.undo)

        redo_action     = context_menu.addAction("Redoxx")
        context_menu.addSeparator()
        cut_action = context_menu.addAction("Cutxx")
        copy_action = context_menu.addAction("Copy")
        paste_action = context_menu.addAction("Paste")
        context_menu.addSeparator()
        select_all_action = context_menu.addAction("Select All")
        select_all_action.triggered.connect(self.selectAll)

        select_all_action = context_menu.addAction("PrintStr")
        select_all_action.triggered.connect(self.print_str )

        # Connect actions to QLineEdit methods

        redo_action.triggered.connect(self.redo)
        cut_action.triggered.connect(self.cut)
        copy_action.triggered.connect(self.copy)
        paste_action.triggered.connect(self.paste)


        # Show the context menu at the cursor position
        # context_menu.exec(QCursor.pos())

        self.mousePressEvent = self.handle_right_click
        # Disable the default context menu
        self.setContextMenuPolicy(Qt.NoContextMenu)

    #----------------------------
    def get_raw_data( self, ):
        """'
        final step from set_data should alway be a string for
        this edit
        """
        data  = self.text()
        return data

    #----------------------------
    def set_preped_data( self, a_string,   is_changed = None ):
        """
        specialize for this edit
        what about prior value

        a prepped data is data in the format for the edit and
        formatted and ready for the edit.

        arg
            is_changed     None      leave is_changed as it was
                           True        is_changed set to True
                           False        is_changed set to False
                           other       undefined behaviour
        mutates

            changes contents of edit
            may change self.is_changed
            self.prior_value  -- so far unchanged, this is probably wrong


        """
        # next !! debug

        if not isinstance( a_string, str ):
            self_field_name   = self.field_name
            msg = f"set_preped_data a_string, not a string {self.field_name = }  return for now inspect then break"
            return
            wat_inspector.go(
                msg            = msg,
                # inspect_me     = self.people_model,
                a_locals       = locals(),
                a_globals      = globals(), )
            breakpoint()

        self.setText( a_string  )   #
            # with prior there ? depending on is_changed ??
        self.prior_value  = a_string
        if is_changed is not None:
            self.is_changed = is_changed
    # ---- crud cycle -------------------------------
    #-----------------------------
    def set_data_to_defaultzzz( self,  ):
        """
        read it
        should it not set the prior value as well
        """
        print( "should be replace by function from base ")
        return
        # if data is None:
        #     data = ""
        # if from_prior_value:
        #     # !! what if none
        #     #self.clear()  # Clears the QDateEdit
        #     self.set_data( self.prior_value, self.db_type )

        # if self.default_type  == "string":
        #     # clear will be empty string
        #     self.set_data( self.default_value, "string"  )

        # else:
        #     1/0

        # self.is_changed   = True
    # -----------------------
    def set_data_to_clear( self   ):
        """
        often replaced with ... set_data_to_....
        but could be clear or default or pass
        """
        self.set_preped_data( "", is_changed = True )
        pass # debug

    #-----------------------------
    def validate( self ):
        """
        this is dead will be over written by

            validate       = widget.some_validate_function see init
        need to return a message could be thru and exception or just
        a return value for now None or "" means ok else
        contain an error message -- possibly promotable??

        """
        #rint( f"CQLineEdit validate get_data_for_record {self.field_name = }")

        # # custom debug
        # if self.field_name == "add_kw":
        #      pdb.set_trace()

        if self.validate_function:
            validate_issue   =  self.validate_function( self.get_raw_data() )
            if validate_issue:

                raise ValidationIssue( validate_issue , self )

        return None

    # ------------------------------------
    def clear_data( self, to_prior ):
        """
        what cleare data is depends on function plugged in here
        """
        #rint( f"need implementation o  !! { to_prior =} ")
        self.set_preped_data( "" )

    # ------------------------------------
    def on_text_changed( self, new_data ):
        """
        may be edited or messed with
        on data change for each drop the new data
        this is probably a bit messed up but also not needed??
        """
        #self.is_changed  = True
        self.on_data_changed( )
        self.prior_value   = new_data
        #rint(f"line edit on_data_changed: {new_data} saved to prior_value ")  !!

    # -------------------------------
    def __str__( self ):

        a_str   = ""
        a_str   = ">>>>>>>>>>* CQLineEdit *<<<<<<<<<<<<"
        a_str   = string_util.to_columns( a_str, ["default_type",
                                           f"{self.default_type}" ] )
        # a_str   = string_util.to_columns( a_str, ["default_value",
        #                                    f"{self.default_value}" ] )
        a_str   = string_util.to_columns( a_str, ["is_changed",
                                           f"{self.is_changed}" ] )
        a_str   = string_util.to_columns( a_str, ["prior_value",
                                           f"{self.prior_value}" ] )
        a_str   = string_util.to_columns( a_str, ["get_raw_data()",
                                           f"{self.get_raw_data()}" ] )

        more    = CQEditBase.__str__( self, )
        a_str   = f"{a_str}\n{more}"
        return a_str

    # @property
    # def data_value( self ):
    #     #rint( "@property datagetter" )
    #     ret   = self.get_data_out()
    #     #rint( ret )
    #     return ret


    # # ---------------------------------
    # @data_value.setter
    # def data_value(self,  arg ):
    #     #rint( "@data.setter" )
    #     self.set_data_in( arg )
#-------------------------------
# -------------------------------
class CQTextEdit(QTextEdit, CQEditBase):
    """
    Custom QTextEdit subclass with CQEditBase integration
    """
    def __init__(self, parent=None, field_name=None, display_type="string", db_type="string"):
        """
        Initialization for CQTextEdit
        """
        #rint("begin init CQTextEdit")

        # Initialize QTextEdit properly
        QTextEdit.__init__(self, parent)  # Call QTextEdit constructor with parent

        # Initialize CQEditBase properly
        CQEditBase.__init__(self, parent, field_name, display_type, db_type)

        #rint("finish init CQTextEdit")
        self.default_type           = "string"

        # # !! this is wrong
        # self.default_value          = "this is my default_value CQTextEdit"
        # self.set_data_to_default    = self.set_data_to_self_default

        a_partial                    = partial( self.do_data_to_default_value, "text default" )
        self.set_data_to_default     = a_partial


        #print( "!! change this default soon ")
        # a_partial                    = partial( self.set_data_to_default_value, "" )
        # self.set_data_to_default     = a_partial

        # this also needs fixing
        self.set_data_to_prior       = self.do_data_to_prior_value




        # Connect the textEdited signal to on_data_changed method -- not here for line edit
        self.textChanged.connect( self.on_data_changed )  # no argument sent
        #self.textEdited.connect(self.on_text_changed )  # no data sent
        # cursor        = self.textCursor()
        # debug_cursor  = self.textCursor()

    def on_data_changedxxxxx(self):
        print("Text has been changed should is_changed be set ")


    #----------------------------
    def get_raw_data( self, ):
        """'
        final step from set_data should alway be a string for
        this edit type
        """
        data  = self.toPlainText()
        return data

    #----------------------------
    def set_preped_data( self, a_string, is_changed = None ):
        """ specialize for this edit
        might hav second argument for is changed
        add to rest of group
        """
        # next !! debug

        if not isinstance( a_string, str ):
            debug    = self.field_name
            msg      = f"set_preped_data error a_string, not a string {self.field_name = }"
            wat_inspector.go( self, globals( ), msg = msg )
        self.setText( a_string  )
        self.prior_value  = a_string
        if is_changed is not None:
            self.is_changed = is_changed

    # ---- crud cycle -------------------------------
    #-----------------------------
    def set_data_to_default_comment_out( self, from_prior_value = False ):
        """
        read it
        """

        return
        # if data is None:
        #     data = ""
        if from_prior_value:
            # !! what if none
            #self.clear()  # Clears the QDateEdit
            self.set_data( self.prior_value, self.db_type )

        if self.default_type  == "string":
            # clear will be empty string
            self.set_data( self.default_value, "string"  )

        else:
            1/0

        self.is_changed   = True

    #-----------------------------
    def validate( self ):
        """
        need to return a message could be thru and exception or just
        a return value for now None or "" means ok else
        contain an error message -- possibly promotable??

        """
        #rint( f"CQLineEdit validate get_data_for_record {self.field_name = }")

        # # custom debug
        # if self.field_name == "add_kw":
        #      pdb.set_trace()

        if self.validate_function:
            validate_issue   =  self.validate_function( self.get_raw_data() )
            if validate_issue:
                raise ValidationIssue( validate_issue , self )

        return None

    # ------------------------------------
    def clear_data( self, to_prior ):
        """
        may be edited or messed with
        on data change for each drop the new data
        """
        print( "need implementation of { to_prior =} ")
        self.set_preped_data( "" )


    # ------------------------------------
    def on_text_changed( self,   ):
        """
        may be edited or messed with
        no data sent by QTextEdit object.
        """
        #self.is_changed  = True
        self.on_data_changed( )
        self.prior_value   = self.toPlainText()
        print(f"text edit on_text_changed ")


    # --------------------------------------------------
    def __str__( self ):

        a_str   = ""
        a_str   = ">>>>>>>>>>* QTextEdit *<<<<<<<<<<<<"
        a_str   = string_util.to_columns( a_str, ["default_type",
                                           f"{self.default_type}" ] )
        a_str   = string_util.to_columns( a_str, ["default_value",
                                           f"{self.default_value}" ] )
        a_str   = string_util.to_columns( a_str, ["is_changed",
                                           f"{self.is_changed}" ] )
        a_str   = string_util.to_columns( a_str, ["prior_value",
                                           f"{self.prior_value}" ] )
        more    = CQEditBase.__str__( self, )
        a_str   = f"{a_str}\n{more}"
        return a_str

    # @property
    # def data_value( self ):
    #     #rint( "@property datagetter" )
    #     ret   = self.get_data_out()
    #     #rint( ret )
    #     return ret


    # # ---------------------------------
    # @data_value.setter
    # def data_value(self,  arg ):
    #     #rint( "@data.setter" )
    #     self.set_data_in( arg )

# ---------------------------------
class CQDateEdit( QDateEdit,  CQEditBase ):
    """
    move a version to stuffdb
    custom_widget.pb   as CQDateEdit
    custom_widgets.CQDateEdit()

    often timestamp to qdate

    """
    def __init__(self,
                 parent             = None,
                 field_name         = None,
                 display_type       = "qdate",
                 db_type            = "timestamp" ):
        """
        read it
        timestammp is an int
        in   -- into the widget
        out  -- out to the record
        """
        #super(   ).__init__(   )
        QDateEdit.__init__( self, parent  )     # mimic LineEdit try parent int there parent of None
        CQEditBase.__init__( self,
                        parent             = parent,
                        field_name         = field_name,
                        display_type       = display_type,
                        db_type            = db_type )

        self.default_type          = "today"   # need begin of day, endo of day ??
        self.default_value         = None     # if used make a qdate
        self.config_calender_popup( True )
        # prior value, prior_type
        is_editable                 = True  #  --- by the user   may be built in
                                        # will nee a configur for it
    # -------------------
    def config_calender_popup( self, is_popup ):
        """ """
        self.setCalendarPopup( is_popup )

    # -------------------
    def contextMenuEvent(self, event):
        """
        magic name for override
        """
        # Create the context menu
        context_menu = QMenu( self )

        # # Add custom actions
        # clear_action = QAction("Clear Date",   self)
        # clear_action.triggered.connect(self.clear_date)
        # context_menu.addAction(clear_action)

        today_action = QAction("Set to Today", self)
        today_action.triggered.connect(self.set_data_today)
        context_menu.addAction(today_action)

        # Show the context menu
        context_menu.exec_(event.globalPos())

    #----------------------------
    def set_data_today(self):
        """
        we need in in or out datatpe
        """
        qdate       = QDate.currentDate()
        self.set_data( qdate, "qdate" )

    #----------------------------
    def get_raw_data( self, ):
        """'
        final step from set_data should alway be qdate
        """
        qdate   = self.date()
        return qdate

    #----------------------------
    def set_preped_data( self, qdate, is_changed = True  ):
        """'
        final step from set_data should alway be qdate
        specialized by name of function call
        """
        # self.setDate( qdate  )  # was going to validate next seems to fix
        super( QDateEdit, self).setDate(qdate )  # Ensure QDateEdit.setDate() is called

    #-----------------------------
    def set_data_to_default_comment_out( self, is_changei = False ):
        """
        return
            mutate
            prior value will be reset
            is_change will be true
            data will be in display
            record is not changed
        """
        if from_prior_value:
            # !! what if none
            #self.clear()  # Clears the QDateEdit
            self.set_data( self.prior_value, self.db_type )

        elif   self.default_type  == "today":
             value   = QDate.currentDate()
             self.set_data( value, "qdate" )

        elif self.default_type  == "qdate":
            # sets a fixed qdate stored in default value
            self.set_data( self.default_value, "qdate"  )

        else:
            1/0

        self.is_changed   = True


    #-----------------------------
    def validate( self, ignore_for_debug_1 = None , ignore_for_debug_2 = None ):
        """
        need to return a message could be thru and exception or just
        a return value for now None or "" means ok else
        contain an error message
        getting called from
        """
        if False:
            msg   = "should not happen 22222"
            raise ValidationIssue( msg , self )
        return None



    # # ---- do we want the next, why, for debug or...
    # # -------------------------------- noe sure we need these
    # @property
    # def data_value( self ):
    #     #rint( "@property datagetter" )
    #     ret   = self.get_date()
    #     #rint( ret )
    #     return ret


    # # ---------------------------------
    # @date.setter
    # def data_value(self,  arg ):
    #     #rint( "@data.setter" )
    #     self.set_date( arg )


# ---- EOF ----------------------------