#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
custom versions of QWidgets
        these have many mods exp to work
        with db records and perhaps the data dict

see  qt_by_example for these widgets -- run this demo_custom_widgets.py

coupling
    to logging
    parameters

"""
# ---- tof

# --------------------
if __name__ == "__main__":
    import main


# --------------------
# ---- imports
#import functools
import logging
import pdb
import traceback
import time
import webbrowser
import textwrap

from datetime  import datetime
from functools import partial
import os
import platform
import subprocess


# ---- Qt
from qt_compat import QApplication, QAction, exec_app, qt_version
from PyQt.QtWidgets import QMainWindow, QToolBar, QMessageBox
from qt_compat import Qt, DisplayRole, EditRole, CheckStateRole
from qt_compat import TextAlignmentRole
from qt_compat import (
    QApplication, QMainWindow, QToolBar, QAction, exec_app,
    DisplayRole, TextAlignmentRole, AlignCenter, WindowMaximized,
    NoInsert, OnManualSubmit
)
from qt_compat import CustomContextMenu   # and look at qt_compat there may be more
from qt_compat import Key_Return, Key_Enter, ShiftModifier, Key_Tab, Key_F, ControlModifier, Key_Backtab  # and look at qt_compat there may be more
#from qt_compat import QTextCursor


from PyQt import QtGui
from PyQt import QtCore
from PyQt.QtCore import Qt, pyqtSignal
from PyQt.QtCore import QDate, QDateTime, QTime, QPoint
from PyQt.QtGui  import QColor, QPalette, QTextCursor, QTextDocument


from PyQt.QtCore import (QAbstractTableModel,
                          QDate,
                          QDateTime,
                          QModelIndex,
                          QRectF,
                          Qt,
                          QTimer,
                          pyqtSlot)

from PyQt.QtGui import (QCursor,
                         QIntValidator,
                         QPainter,
                         QPixmap,
                         QStandardItem,
                         QStandardItemModel,
                         QTextCursor)
from PyQt.QtSql import (QSqlDatabase,
                         QSqlQuery,
                         QSqlQueryModel,
                         QSqlRecord,
                         QSqlRelation,
                         QSqlRelationalDelegate,
                         QSqlRelationalTableModel,
                         QSqlTableModel)

# from PyQt.QtGui import ( QAction, QActionGroup, )

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
                             QGroupBox,
                             QHBoxLayout,
                             QInputDialog,
                             QLabel,
                             QLineEdit,
                             QListWidget,
                             QListWidgetItem,
                             QMainWindow,
                             QMdiArea,
                             QMdiSubWindow,
                             QMenu,
                             QMessageBox,
                             QPushButton,
                             QRadioButton,
                             QSizePolicy,
                             QSpinBox,
                             QTableView,
                             QTableWidget,
                             QTableWidgetItem,
                             QTabWidget,
                             QTextEdit,
                             QVBoxLayout,
                             QWidget)
if qt_version == 6:
    MoveOperation = QTextCursor.MoveOperation
else:
    MoveOperation = QTextCursor


# ---- imports local -- then constants
import string_util
import wat_inspector
from   app_global     import AppGlobal
import exec_qt
import clip_string_utils
import string_list_utils

#import convert_db_display
import mdi_management

EXEC_RUNNER         = None  # setup below -- do we really want to do this
MARKER              = ">>"
LOG_LEVEL           = 1    # higher is more
        # logging.log( LOG_LEVEL,  debug_msg, )
logger              = logging.getLogger( )
SCAN_LINES          = 100

#does order matter
REPLACE_LIST        = [    ( "*>url ",   ">>url " ),   # note deliberate spacemay neee tab as well?
                           ( "*>url0 ",  ">>url " ),
                           ( "*>shell ",  ">>shell " ),
                    ]


# make sure equivalent
QT_DATE_FORMAT         = "yyyy-MM-dd"  # "yyyy-MM-dd"
PY_DATE_FORMAT         = "%Y-%m-%d"   # strftime("%Y-%m-%d")

# DATE_FORMAT         = "yyyy-MM-dd"
# "%Y-%m-%d" )
    # my standard date format

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

#-------------------------------
def move_cursor_to_button( button ):
    """
    likely works with any widget

    """
    # Get the button's rectangle in global coordinates
    button_rect = button.geometry()

    # Get the center point relative to the button's parent (the window)
    center_point = button_rect.center()

    # Convert to global screen coordinates
    global_point = button.mapToGlobal(QPoint(
        button_rect.width() // 2,
        button_rect.height() // 2
    ))

    # Move the cursor
    QCursor.setPos(global_point)

# -----------------------
def validate_no_z( a_string   ):
    """
    a debug thing
    what type need models be? -- think should throw except
    """
    msg      = None
    if "z" in a_string:
        msg   = "validate_no_z no ====================================="
        logging.debug( msg )
    return msg

# -----------------------
def get_rec_data( record, field_name  ):
    """
    get data from the record unless record is the data
    rec = record
    field_name ignored of record is the data
    but to aid in debugging assume rec is the data if not a qrecord
    data      = get_rec_data( record, field_name )
    """
    if  isinstance( record, QSqlRecord ):

        if record.indexOf( field_name ) == -1:
            msg         = ( f"get_rec_data Field {field_name = } "
                            f"does not exist in the record.")
            logging.error( msg )
            raise ValueError( msg )
            #rint( f"set_data_from_record {debug_fn}")
            #data       = record.value( field_name  )
            # msg        =  ( f"set_data_from_record {field_name} {data = }"
            #                 f" {self.db_type = }")
            # logging.debug( msg )
        # still need None !!
    else:
        return record    # take as value field_name does not matter

    # if here have a record with valid field_name
    raw_data        = record.value( field_name  )

    return raw_data

# -----------------------
def set_rec_data( record, field_name, data   ):
    """
    data goes into the record
    but if record is not a record just skip ( debug log ? )
    rec = record
    but to aid in debugging assume record is the data if not a QSqlRecord

    """
    if  not isinstance( record, QSqlRecord ):
        msg         = ( f"set_rec_data Field {field_name} "
                        f"record is not a QSqlRecord Assume testing else ERROR")
        logging.error( msg )
        return


    if record.indexOf( field_name ) == -1:
        msg         = ( f"set_rec_data Field {field_name} "
                        f"does not exist in the record. Assume testing else ERROR ")
        logging.error( msg )
        return
        #raise ValueError( msg )
        #rint( f"set_data_from_record {debug_fn}")
        #data       = record.value( field_name  )
        # msg        =  ( f"set_data_from_record {field_name} {data = }"
        #                 f" {self.db_type = }")
        # logging.debug( msg )
    # still need None !!
    record.setValue( field_name, data )

# -----------------------
def model_dump(  model, msg = "model dump msg" ):
    """
    a debug thing
    what type need models be?
    """
    msg     = ( "model_dump begin may want to add back for information about  not ia any more ")
    logging.debug( msg )
    # ia_qt.q_abstract_table_model( model )
    # ia_qt.q_sql_table_model( model )

    row_count    = model.rowCount()
    column_count = model.columnCount()
    a_str   = ( f"model_dump begin {row_count = } ")

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

    a_str   = ( f"{a_str}\nRow {row}: {row_data}")
    a_str   = ( f"{a_str}\nmodel_dump end")
    logging.debug( a_str )


# --------------------------------------
class ModelIndexer(   ):
    """
    so we can do a find inside same sort of model ... later
    make an extension to the model..
    """
    #----------- init -----------
    def __init__(self, model, index_tuple   ):
        """
        Usual init see class doc string
            model can be an QAbstractTableModel  a TableModel, but what about sql thing
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
        set if the index is valid, if not find will re-index
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
            # build key using index_tuple, index itself is a tuple
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

    def data(self, index, role=DisplayRole):
        """ !! FIX RETURN """
        if role == DisplayRole:
            return self._data[index.row()][index.column()]

    def set_data(self, data ):
        self._data      = data

    # def add_data(self, data ):
    #     pass

    def set_data_at_index(self, index, value, role=EditRole):
        """
        index might be index = model.index(ix_row,  ix_col )  # Row 1, Column 1

        Args:
            index (TYPE): DESCRIPTION.
            value (TYPE): DESCRIPTION.
            role (TYPE, optional): DESCRIPTION. Defaults to EditRole.

        Returns:
            bool: DESCRIPTION.

        """
        if role == EditRole:
            self._data[index.row()][index.column()] = value  # Update the data
            self.dataChanged.emit(index, index, [DisplayRole])
                # Emit dataChanged signal for this index
            return True
        return False

    def headerData(self, section, orientation, role=DisplayRole):
        if role == DisplayRole:
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



class ShellExe( object ):
    """
    for executing shell commands that begin as a list
    this may need refactoring
    based on cmd_assist perhaps should go back there
    should be a singleton for now built by TextEditExt

            used by text editExtMixin
    """
    #----------- init -----------
    def __init__(self,   ):
        pass

    #---------------------------
    def run_code_lines( self, code_lines, ):
        """
        we may be rsripping multimple times like in caller
        """

        code_lines_new     = [i_code_line.strip()
                               for i_code_line in code_lines
                                   if i_code_line.strip() != "" ]

        # works but ugly
        # now combine across \
        code_lines_newer   = []
        got_bs             = False
        for ix, i_code_line in enumerate( code_lines_new ):
            if got_bs:
                len_newer  = len( code_lines_newer )
                code_lines_newer[ len_newer -1 ] += i_code_line
            else:
                code_lines_newer.append( i_code_line )

            # remove trailing \

            last_line   = len(code_lines_newer) - 1
            if code_lines_newer[ last_line ].endswith( "\\" ):
                got_bs             = True
                code_lines_newer[ last_line ] = code_lines_newer[ last_line ].removesuffix( "\\" )
            else:
                got_bs             = False


        code_lines_new   = code_lines_newer
        #rint( f"run_code_lines in shellext    >>shell {code_lines_new =}")
        # line one == 0 is a comment add echo in front and quote
        code_lines_new[ 0 ]    = f"echo '{code_lines_new[ 0 ]}'   "

        #rint( f"run_code_lines in shellext    >>shell {code_lines_new =}")
        code_lines_new      = self.add_echo( code_lines_new )
        debug_msg    = ( f""""run_code_lines in shellext    >>shell {code_lines_new =}""")
        logging.log( LOG_LEVEL,  debug_msg, )

        cmd_str     = ";".join( code_lines_new )
        cmd_str     = f"""gnome-terminal -- bash -c "{cmd_str}; echo 'exec bash' ;exec bash" """

        debug_msg   = ( f"about to os.system {cmd_str = }" )
        logging.log( LOG_LEVEL,  debug_msg, )

        result = os.system( cmd_str  )
        #rint( f"result = os.system >>{result}<<\n\n")

    # ----------------------------------
    def add_echo(self, code_lines ):
        """
        add echo commands except to echo commands
        and for now remove comments from the command part

        """
        new_list      = []
        for i_item in code_lines:
            if i_item.startswith( "echo" ):
                new_list.append( i_item )
            else:
                new_list.append( f"echo '{i_item}'")
                # now look for command part comment
                splits     = i_item.split( "#" )
                i_item     = splits[0]     # combine lines for clean
                new_list.append( i_item )

        return new_list

    # ----------------------------------
    def build_command_1_2xxx( self, add_echo = True, add_newline = False ):
        """
        from command_0 suck dry and delete
        build command from arg1 and arg2
        self.build_command_1_2
        ex:
        return self.build_command_1_2( add_echo = add_echo, add_newline = add_newline )

        ! need a 0 1 2 version and a generalized one see commands 3 for vert which seems to do it
        """
        print( "build_command_1_2" )
        args        = self.get_ddl_args()

        cmd_prefix  = self.build_prefix()

        cmd_list    = cmd_prefix + [ f"{args[1]} {args[2]}",
                                     "exec bash",
                                     ]

        if add_echo:
            cmd_list    = self.build_echo( cmd_list )

        if add_newline:
            cmd_str     = "\n".join( cmd_list )   # may still want to strip exec bash  !!

        else:
            cmd_str     = ";".join( cmd_list )
            cmd_str     = f'gnome-terminal -- bash -c "{cmd_str}"'

        #rint( cmd_str )
        #rint( cmd_list )

        return cmd_str

class IdleExe( ):
    """
    for executing shell commands that begin as a list
    this may need refactoring
    based on cmd_assist perhaps should go back there
    should be a singleton for now built by TextEditExt
    """
    def __init__( self ):
        """ """
        self.venv               = "py_12_misc"  # !! change to parameter
        self.file_name_temp_py  = "temp_py.py"
        self.file_name_temp_sh  = "temp_sh.sh"

    #--------
    def write_file_py( self, code_lines, file_name = None ):
        """ """
        file_name    = self.file_name_temp_py

        with open( file_name, 'w' ) as a_file:
                # wa will append so file should be deleted time to time w will overwrite
            a_file.writelines(f"{line}\n" if not line.endswith("\n") else line for line in code_lines )

    #--------
    def write_file_sh( self, sh_lines, file_name = None ):
        """ """
        file_name    = self.file_name_temp_sh

        with open( file_name, 'w' ) as a_file:    # wa will append so file should be deleted time to time w will overwrite
            a_file.writelines(f"{line}\n" if not line.endswith("\n") else line for line in sh_lines )


    def idle_on_temp_file( self, code_lines ):
        """ """
        code_lines[0]   =  f"# -- {code_lines[0]}"
        self.write_file_py( code_lines, )
        sh_lines        = [ f"conda activate {self.venv}", f"idle  {self.file_name_temp_py}" ]
        self.write_file_sh( sh_lines )

        #subprocess.run(  ["bash", self.file_name_temp_sh ] )
        #    # blocking
        subprocess.Popen(["bash", self.file_name_temp_sh] )
            # non blocking --- see help


    def idle_file( self, file_name ):
        """
        open idle in a conda venv for file_name

        think links to idle_file   filename
        """

        sh_lines        = [ f"conda activate {self.venv}", f"idle  {file_name}" ]
        self.write_file_sh( sh_lines )

        # next seems to be blocking
        #subprocess.run(["bash", self.file_name_temp_sh ])

        # should be non blocking
        subprocess.Popen([ "bash", self.file_name_temp_sh])


        # next is wrong because we need the environment set up
        #subprocess.run([ "idle", file_name ])

# -------------------------------
class TextEditExtMixin(  ):
    """
    new extension to text edits with stuffdb support optional

    """
    def __init__(self,
                 parent             = None, ):

        self.up_button              = None
        self.dn_button              = None
        self.search_text_widget     = None
        self.last_position          = 0
        self.set_custom_context_menu( )

        # ---- external optional services
        self.stuffdb                = None
        self.stuffdb_app_global     = None
        self.ext_logger             = None
        #self.stuff_text_ext         = None
        # self.prior_text             = ""

        # ---- additional services
        self.idle_exe               = IdleExe()
        self.shell_exe              = ShellExe()

    #-------------------------------------------
    def set_stuffdb( self, stuffdb ):
        """
        get functions..... from stuffdb for stuffdb integration

        ?? migrate to property  """
        self.stuffdb                = stuffdb

        self.stuffdb_app_global     = stuffdb.app_global
        self.ext_logger             = stuffdb.app_global.logger
        #self.stuff_text_ext         = self.stuffdb.get_stuff_text_edit_ext( self )

     #-----------------------------------------
    def log( self, *, level = LOG_LEVEL, msg ):
        """
        self.log( msg = msg )
        self.log( level = logging.DEBUG, msg = msg  )
        """
        if self.ext_logger:
            #self.ext_logger( msg )
            self.ext_logger.log( level, msg  )
        else:
            print( f"self.log {msg}")

    # beware may be used multiple places
    def keyPressEvent(self, event):
        """
        capture all the key presses
        """
        # breakpoint()
        # ---- is next block indent
        if event.key() == Key_Tab:
            self.indent_selected_text()
            return

        elif event.key() == Key_Backtab or (event.key() == Key_Tab and event.modifiers() & ShiftModifier):
            self.unindent_selected_text()
            return

        if event.modifiers() == ControlModifier and event.key() == Key_F:
            self.ctrl_f_search_down()
            return

        #super().keyPressEvent( event )
        self.keyPressEvent( event )

    #------------------------------
    def fooxxx(self):
        print("Ctrl+F pressed!")
        self.append("foo() executed!")

    def make_search_widgets( self, ):
        """
        search_text_widget,  up_button,  dn_button  =  text_edit.make_search_wigets(  )
        ⇑ Up Double Arrow (U+21D1)
        ⇓ Down Double Arrow (U+21D3)
        """
        widget      = QPushButton( "⇑ Up ⇑")
        self.up_button  = widget
        widget.clicked.connect(  self.search_up  )

        widget      = QPushButton( "⇓ Down ⇓")
        self.dn_button  = widget
        widget.clicked.connect( self.search_down )

        widget      = QLineEdit()
        self.search_text_widget   = widget

        return self.search_text_widget, self.up_button, self.dn_button

    # ---------------------
    def ctrl_f_search_down( self,   ):
        """

        """
        selected_text    = self.capture_selected_text()
        #self.append( f"ctrl_f_search_down {selected_text = }")
        self.search_text_widget.setText( selected_text )
        # do not do the firs search

    # ---------------------
    def search_down( self,   ):
        """
        search for text see search up
            case insensitive
        """
        text_edit   = self
        search_text = self.search_text_widget.text()
        if search_text:
            cursor = text_edit.textCursor()
            cursor.setPosition( self.last_position )
            found = text_edit.find( search_text )

            if found:
                self.last_position = text_edit.textCursor().position()
                text_edit.ensureCursorVisible()  # Scroll to the found text

            else:
                # grok code
                self.last_position = 0
                cursor.setPosition(self.last_position)
                text_edit.setTextCursor(cursor)
                text_edit.ensureCursorVisible()  # Optional: Scroll to top if reset

    # ---------------------
    def search_up( self,  ):
        """case insensitive
        for an text edit search for a string
        the line_edit contains the string that is the target
        direction of search is up
        case insensitive
        may need to protect against trying to start beyond end !!
        as user may have deleted some text

        """
        text_edit   = self
        search_text = self.search_text_widget.text()
        if search_text:
            cursor = text_edit.textCursor()
            cursor.setPosition( self.last_position )

            if qt_version == 6:
                found = text_edit.find( search_text,  QTextDocument.FindFlag.FindBackward )
                    # ← Qt6 uses FindFlag, not FindBackward directly
            else:
                found = text_edit.find( search_text,   QTextDocument.FindBackward )


            if found:
                self.last_position = text_edit.textCursor().position()
                text_edit.ensureCursorVisible()  # Scroll to the found text

            else:
                # not found make another try or message ??
                #self.last_position = text_edit.document().characterCount()
                    # ng
                self.last_position = len( text_edit.toPlainText() )
                cursor.setPosition( self.last_position )
                text_edit.setTextCursor(cursor)
                text_edit.ensureCursorVisible()

    #----------------------------
    def set_custom_context_menu( self, ):
        """
        what it says
            call in the init of the final widget ?
        """
        #self.setContextMenuPolicy( QtCore.Qt.CustomContextMenu)
        self.setContextMenuPolicy( CustomContextMenu)   # 5 6 compat

        self.customContextMenuRequested.connect( self.show_context_menu )

        # widget.setContextMenuPolicy( QtCore.Qt.CustomContextMenu )
        # widget.customContextMenuRequested.connect( self.show_context_menu )
        #self.context_widget   = widget # for later use in menu

    # ---------------------------------------
    def show_context_menu( self, pos ):
        """
        this is really just for the text edit
        so is !! wrong in some way
        refactor please !! just use action
           ?? extend further

        """
        widget      = self
        menu        = QMenu( widget )

        # Enable/disable actions based on context
        cursor = widget.textCursor()
        has_selection   = cursor.hasSelection()
        can_undo        = widget.document().isUndoAvailable()
        can_paste       = QApplication.clipboard().text() != ""


        # cut_action.setEnabled(has_selection)
        # copy_action.setEnabled(has_selection)
        # paste_action.setEnabled(can_paste)
        # foo_action.setEnabled(can_paste)

        # Add standard actions
        undo_action = menu.addAction("Undo")
        undo_action.triggered.connect(widget.undo)
        undo_action.setEnabled(can_undo)

        menu.addSeparator()

        cut_action = menu.addAction("Cut")
        cut_action.triggered.connect(widget.cut)
        cut_action.setEnabled(has_selection)

        copy_action = menu.addAction("Copy")
        copy_action.triggered.connect( widget.copy )
        copy_action.setEnabled(has_selection)

        paste_action = menu.addAction("Paste")
        paste_action.triggered.connect( widget.paste )
        paste_action.setEnabled(can_paste)
        #menu.addSeparator()

        # ---- "Smart Paste"
        foo_action = menu.addAction("Smart Paste")
        foo_action.triggered.connect(self.smart_paste_clipboard )
        foo_action.setEnabled(can_paste)

        menu.addSeparator()

        # ---- "Smarten"
        foo_action = menu.addAction("Smarten")
        foo_action.triggered.connect( self.smarten  )
        foo_action.setEnabled(has_selection)

        # ---- "Search Selected"
        foo_action = menu.addAction("Search Selected")
        foo_action.triggered.connect( self.search_selected  )
        foo_action.setEnabled(has_selection)

        menu.addSeparator()

        # ---- "coyp all "
        foo_action = menu.addAction("Copy All")
        foo_action.triggered.connect(self.copy_all )
        menu.addSeparator()

        # ---- "0_sreen_dirt"
        foo_action = menu.addAction("0_sreen_dirt")
        processing_function     = partial( clip_string_utils.list_to_list_remove_dirt, screen_dirt = AppGlobal.parameters.screen_dirt )
        foo                     = partial( self.process_selected,  processing_function = processing_function )
        foo_action.triggered.connect( foo )
        foo_action.setEnabled( has_selection )

        menu.addSeparator()

        # ---- submenu
        submenu                 = menu.addMenu("Max Lines ...")

        # Add actions to the submenu -- but for now these might not connet to anything
        # pdf_action              = submenu.addAction("Export to PDF")
        # csv_action              = submenu.addAction("Export to CSV")
        # json_action             = submenu.addAction("Export to JSON")



        # ---- "Max 0 Blank Lines"
        foo_action              = submenu.addAction( "Max 0 Blank Lines" )
        processing_function     = partial( string_list_utils.list_to_list_max_n_blank,  max_blank = 0 )
        foo                     = partial( self.process_selected,  processing_function = processing_function )
        foo_action.triggered.connect( foo )
        foo_action.setEnabled(has_selection)

        # ----  "Max 1 Blank Lines"
        foo_action              = submenu.addAction( "Max 1 Blank Lines" )
        processing_function     = partial( string_list_utils.list_to_list_max_n_blank,  max_blank = 1 )
        foo                     = partial( self.process_selected,  processing_function = processing_function )
        foo_action.triggered.connect( foo )
        foo_action.setEnabled(has_selection)

        # ---- "max_2_blank_lines"
        foo_action              = submenu.addAction("Max 2 Blank Lines")
        processing_function     = partial( string_list_utils.list_to_list_max_n_blank,  max_blank = 2 )
        foo                     = partial( self.process_selected,  processing_function = processing_function )
        foo_action.triggered.connect( foo )
        foo_action.setEnabled( has_selection )

        menu.addSeparator()

        # ---- "Sort/Del Dups for Line Pairs"
        foo_action              = menu.addAction( "Sort/Del Dups for Line Pairs" )
        processing_function     = partial( string_list_utils.alt_line_sort,  which_line = 0, del_dups = True   )
        foo                     = partial( self.process_selected,  processing_function = processing_function )
        foo_action.triggered.connect( foo )
        foo_action.setEnabled( has_selection )


        # ---- "Strip Trail in Sel"
        foo_action = menu.addAction("Strip Trail in Sel")
        foo        = partial( self.strip_selected,  keep_leading = True )
        foo_action.triggered.connect( foo )
        foo_action.setEnabled(has_selection)

        # ---- "Strip Lead and Trail in Sel"
        foo_action = menu.addAction( "Strip Lead and Trail in Sel" )
        foo        = partial( self.strip_selected,  keep_leading = False )
        foo_action.triggered.connect( foo )
        foo_action.setEnabled(has_selection)
        #foo_action.triggered.connect( self.strip_eol_lines_in_selection )
        #menu.addSeparator()

        # ---- ""Update Markup""
        foo_action = menu.addAction("Update Markup")
        foo_action.triggered.connect( self.update_markup )
        foo_action.setEnabled(has_selection)
        menu.addSeparator()

        # ---- "Open Urls"
        foo_action = menu.addAction("Open Urls")
        foo_action.triggered.connect( self.goto_urls_in_selection )
        foo_action.setEnabled(has_selection)
        menu.addSeparator()

        select_all_action = menu.addAction("Select All")
        select_all_action.triggered.connect(widget.selectAll)

        # ---- >>   go
        menu_action = menu.addAction(">> Go ...")
        menu_action.triggered.connect( self.cmd_exec )
        menu.addSeparator()

        # Show it
        if qt_version == 6:  # 5 6 compat
            menu.exec(widget.mapToGlobal(pos))
        else:
            menu.exec_(widget.mapToGlobal(pos))

    # ----------------------------------
    def capture_selected_text( self ):
        """

        Capture the currently highlighted (selected) text
        is this worth a function
        selected_text    = self.capture_selected_text()
        """
        cursor        = self.textCursor()
        selected_text = cursor.selectedText()

        if selected_text:
            print(f"Captured highlighted text: '{selected_text}'")
            # Call your function with the captured text
            #self.foo(selected_text)
        else:
            print("No text is currently highlighted/selected")

        return selected_text

    # ------------------------
    def cmd_exec( self   ):
        """
        execute command parsed out of text
        probably should be refactored to use
        a disptach dict

          read the code find on cmd ==
                py
                sh
                url
                shell
                text
                idle
                copy
                find_dn
        """
        text_edit        = self
        # ---- do some parsing
        code_lines       = self.get_snippet_lines( text_edit  )
        debug_msg        = ( f"code lines >>{code_lines}<<" )
        #self.logging( debug_msg )
        self.log(  msg = debug_msg  )
        # logging.debug( debug_msg )
        # self.app_global         = AppGlobal
        #stuff_db_app_global.logger( )

        code_lines       = self.undent_lines(code_lines)
        splits           = code_lines[0].split()
        splits_1         = code_lines[0].split( " ", 1 )
        if len( splits_1 ) > 1:
            arg_1 = splits_1[1].strip()   # ?? follow by remove of nl

        if len( splits) == 0:
            return

        if splits[0] == MARKER:
            splits = splits[1:]        # toss the >>

        if splits[0].startswith( MARKER ):
            splits[0]  = splits[0][ 2: ]  # again toss the >>

        cmd         = splits[0].lower()
        cmd_args    = splits[ 1:]

        debug_msg   = ( f"cmd_exec {cmd = } \n {cmd_args = }")
        # need to fic
        #self.logging.log( LOG_LEVEL,  debug_msg, )
        self.log( msg = debug_msg )

        # ---- py
        if   cmd == "py":
            code    = "\n".join( code_lines[ 1:] )  # title in line 0 !!
            msg     = " ".join( cmd_args )
            if msg == "":
                msg  = "execute some python code"
            # !! fix me
            # #rint( code )
            global   EXEC_RUNNER
            if EXEC_RUNNER is None:
                EXEC_RUNNER      = exec_qt.ExecRunner( AppGlobal.q_app  )

            EXEC_RUNNER.create_window(
                        code       = code,
                        a_locals   = locals(),
                        a_globals  = globals(),
                        msg        = msg,
                        autorun    = True )

        elif cmd == "copy":
            #rint( "you need to implement >>idle")
            QApplication.clipboard().setText( " ".join( cmd_args )   )

        # ---- snippet
        elif cmd == "snippet":
            code    = "\n".join( code_lines[ 1:] )  # title in line 0 !!
            msg     = " ".join( cmd_args )

            QApplication.clipboard().setText( code )

        # ---- idle and idle file
        elif cmd == "idle":   # want a one line and may line
            msg     = ( "  >>idle in process ................................")
            self.log( msg = msg, )
            self.idle_exe.idle_on_temp_file( code_lines )

        elif cmd == "idle_file":   # want a one line and may line
            file_name     = cmd_args[0]
            self.idle_exe.idle_file( file_name  )
            pass  # debug

        # ---- text
        elif cmd == "text":
            # we might be able to do without support from stuff
            file_name     = cmd_args[0]
            if self.stuffdb_app_global:
                self.stuffdb_app_global.os_open_txt_file( file_name )

        elif cmd == "url":
            filename     = cmd_args[0]
            webbrowser.open( filename, new = 0, autoraise = True )

        # ---- bash  >>bash
        elif cmd == "bash":
            #rint( f"you need to implement >>shell {code_lines}")
            print(f"need to fix bash{code_lines} how comments " )
            code_lines   = [i_line.rstrip() for i_line in code_lines ]
            #code_lines   = code_lines.rstrip() ng it is a list
            if self.shell_exe:
                self.shell_exe.run_code_lines( code_lines )

        # ---- shell
        elif cmd == "shell":
            #file_name     = cmd_args[0]  # older change to next t
            file_name     = arg_1
            self.shell_file( file_name )
    \
        # ---- search  !! should not have in this object move to stuff db
        # as a plugin of some source
        elif cmd.startswith( "search" ):
            # msg   = ( "implementing >>search")
            # logging.debug( msg )
            #breakpoint( )


            # reject if >>search not on line clicked -- will dake a bigger fix
            # if len( code_lines ) > 1:
            #     return

            if  self.stuffdb  is None:
                msg   = ( f"cannot do search as STUFF_DB  = none  ")
                #self.logging.error( msg )
                self.log( msg = msg, )
                # !! put up dialog
                return

            else:
                self.stuffdb_app_global.mdi_management.do_db_search( cmd,  cmd_args )


            #     # msg   = ( f"you need to implement >>search {STUFF_DB  = }  ")
            #     # logging.debug( msg )
            #     new_args =  []  # drop after #
            #     for i_arg in cmd_args:
            #         if i_arg.startswith( "#" ):
            #             break
            #         new_args.append( i_arg )
            #         key_words   = " ".join( new_args )
            #     self.search_stuffdb( cmd,do_db_search
            # " ".join( new_args ))
            #     #STUFF_DB.main_window.search_me( " ".join( new_args ) )  # cmd_args rest of line
            # # = None  # may be monkey patched in
            # #                     # this wold be the app
            # #                     # STUFF_DB.main_window may be what you want
            # #                     # go_active_sub_window_func

        # ---- find_dn
        elif cmd == "find_dn":
            # code lines >>       find_dn exe
            parse_0 = code_lines[0][2:].strip()  #  strip >> and spaces
            parse_1 = parse_0[ 7: ]              # strip find_dn
            parse_2 = parse_1.split( "#" )[0]    # remove comments
            parse_3 = parse_2.strip()            # strip lead and trail spaces
            selected_text         =  parse_3     # could clean up code
            # selected_text    = self.capture_selected_text()
            #self.append( f"ctrl_f_search_down {selected_text = }")
            self.search_text_widget.setText( selected_text )
            # self.dn_button.setFocus()
            move_cursor_to_button( self.dn_button )
            self.search_down()

        elif cmd == "xxx":
            pass
        else:
            msg   = ( f"{cmd = } \n {cmd_args = }" )
            print( msg )
            #logging.error( msg )
        # next case based on command cmd
    # ------------------------
    def get_snippet_lines( self, do_undent = True  ):
        """ """
        if qt_version == 6:
             lines  = self.get_snippet_lines_6( do_undent = do_undent )
        else:
             lines  = self.get_snippet_lines_5( do_undent = do_undent )

        return lines


    # ------------------------
    def get_snippet_lines_5( self, do_undent = True  ):
        """
        !! for some uses need to know which line or content
              of the first line for single line commands
        title is line 0
        often for code
        assume cursor in the body
        but there is a built in find function

        # ---- top of text
        >beginmarker    anything else on line

        >>py this is a title
        print( 1 )
        for ix in range( 10, 15 ):
            print( ix )

        >beginmarker    anything else on line

        # ---- end  of text

        start scanning up:
            stop if hit begin marker or top ( or blank lines?

        now scan down and collect lines ( rstripped, no spaces no \n )

            stop if  n_blank lines
            marker
            or end of text
        """
        lines                   = []
        cursor                  = self.textCursor()
        consective_blank_lines  = 0
        original_position       = cursor.position()
        cursor.movePosition( cursor.StartOfLine )
        prior_start_of_line     = cursor.position()

        # ---- upward scan
        for ix in range( SCAN_LINES ):

            cursor.movePosition( QTextCursor.StartOfLine )
            cursor.movePosition(cursor.EndOfLine, cursor.KeepAnchor )
            selected_text = cursor.selectedText()

            selected_text   = selected_text.rstrip()
            if   selected_text == "":
                consective_blank_lines  += 1

            else:
                consective_blank_lines  = 0

            if selected_text.strip().lower().startswith( MARKER ):
                #rint( f"hit the top of marked text {ix =}")
                break # leave curor at begin of marker line

            # lines.append( selected_text  )

            cursor.movePosition( cursor.Up )
            cursor.movePosition( QTextCursor.StartOfLine )
            position       = cursor.position()
            if position == prior_start_of_line:
                debug_msg = ( f"is error !! hit the top of all text {ix =}")
                # self.logging.log( LOG_LEVEL,  debug_msg, )
                self.log( msg = debug_msg, )
                break
            else:
                prior_start_of_line  = position

        # now at top of text
        #rint( f"found the top of  text {ix =}")

        # ---- start down collecting lines
        consective_blank_lines  = 0
        on_top_line             = True
        for ix in range( SCAN_LINES ):
            cursor.movePosition( cursor.EndOfLine, cursor.KeepAnchor )
            selected_text   = cursor.selectedText()
            selected_text   = selected_text.rstrip()

            if   selected_text == "":
                consective_blank_lines  += 1

            else:
                 consective_blank_lines  = 0

            if consective_blank_lines  > 3:
                #msg = f"scan down blank line limit {consective_blank_lines}"
                #rint( msg )
                break

            # hot on firs line down
            if not on_top_line and selected_text.strip().lower().startswith( MARKER ):
                #rint( f"hit the next line of marked text {ix =}")
                break # leave curor at begin of marker line
            else:
                on_top_line = False

            lines.append( selected_text  )

            # Move to the start of the next line 2 steps
            cursor.movePosition(cursor.Down)
            cursor.movePosition(QTextCursor.StartOfLine)
            position       = cursor.position()

            if position == prior_start_of_line:
                #rint( f"hit the end of text {ix =} ")
                break

            else:
                prior_start_of_line  = position

        if do_undent:
            lines   = self.undent_lines( lines )

        return lines



# SCAN_LINES = 500
# MARKER = ">"


    #----------------------------------
    def get_snippet_lines_6(self, do_undent=True):
        """
        qt6 version I hope
        :param do_undent: DESCRIPTION, defaults to True
        :type do_undent: TYPE, optional
        :return: DESCRIPTION
        :rtype: TYPE

        """

        lines = []
        cursor = self.textCursor()

        consecutive_blank = 0
        original_position = cursor.position()

        # Move to start of current line (Qt6 uses StartOfBlock)
        cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
        prior_start = cursor.position()

        # -------------------------
        # UPWARD SCAN
        # -------------------------
        for ix in range(SCAN_LINES):

            # Select whole line
            cursor.movePosition(
                QTextCursor.MoveOperation.StartOfBlock
            )
            cursor.movePosition(
                QTextCursor.MoveOperation.EndOfBlock,
                QTextCursor.MoveMode.KeepAnchor
            )

            selected = cursor.selectedText().rstrip()

            if selected == "":
                consecutive_blank += 1
            else:
                consecutive_blank = 0

            # Stop at begin marker
            if selected.strip().lower().startswith(MARKER):
                break

            # Move up
            cursor.movePosition(QTextCursor.MoveOperation.Up)
            cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
            position = cursor.position()

            # Hit top of document
            if position == prior_start:
                self.log(msg=f"hit top of text {ix=}")
                break
            else:
                prior_start = position

        # -------------------------
        # DOWNWARD SCAN: collect lines
        # -------------------------
        consecutive_blank = 0
        on_top_line = True

        for ix in range(SCAN_LINES):

            cursor.movePosition(
                QTextCursor.MoveOperation.EndOfBlock,
                QTextCursor.MoveMode.KeepAnchor
            )

            selected = cursor.selectedText().rstrip()

            if selected == "":
                consecutive_blank += 1
            else:
                consecutive_blank = 0

            if consecutive_blank > 3:
                break

            # Stop if we hit the next bottom marker
            if not on_top_line and selected.strip().lower().startswith(MARKER):
                break
            else:
                on_top_line = False

            lines.append(selected)

            # Move to next line
            cursor.movePosition(QTextCursor.MoveOperation.Down)
            cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
            position = cursor.position()

            # End of document
            if position == prior_start:
                break
            else:
                prior_start = position

        if do_undent:
            lines = self.undent_lines(lines)

        return lines

    #------------------------------------
    def update_markup(self, ):
        """
        update from old stuff markup to new markup
        !! change to use process_selected
        """
        text_edit       = self
        # Get the selected text
        cursor          = text_edit.textCursor()
        selected_text   = cursor.selectedText()

        # Check if there's any selected text
        if not selected_text:
            return None

        # Split into lines and strip each line
        # Note: QTextEdit uses Unicode paragraph separators (U+2029) for line breaks in selectedText()
        lines           = selected_text.split('\u2029')
        updated_lines   = [self.do_line_replacements(line) for line in lines]

        processed_text  = '\n'.join(updated_lines)

        cursor.insertText( processed_text )

        return processed_text

    # -----------------------------
    def do_line_replacements( self, line ):
        """

        may want to strip eol while at it ??
        may have tab or space, we do not want tabs at all in text
        so replace with 2 spaces
        """
        # print( "do_line_replacements {line =}" )
        #breakpoint()
        line    = line.replace( "\t", "  " )
        for old, new in REPLACE_LIST:
                line   = line.replace( old, new )

        return line

    # ---- static functions

    # ------------------------
    def undent_lines( self, lines ):
        """
        static
        ?? perhaps a util
        delete leading spaces ( as per code )
        then return as a multiline string  that is a list of strings
            lines   is a list of lines

        """
        new_lines            = []
        if len( lines ) == 0:
            return new_lines

        num_leading_spaces   = len( lines[0] ) - len( lines[0].lstrip(' ') )
        #rint( f"{num_leading_spaces = }")
        leading_spaces       = " " * num_leading_spaces

        for i_line in lines:
            if i_line.startswith( leading_spaces ):
                i_line   = i_line[ num_leading_spaces : ]
            new_lines.append( i_line )

        return new_lines

    #-----------------------------------
    def process_selected( self, processing_function  ):
        """
        generallized routine for extracting selected text, processing and return it
        processing_function   = a function takes a list returns a list
            may want to use partial
        """
        # Get the current cursor and selection

        text_edit   = self
        cursor      = text_edit.textCursor()
        if not cursor.hasSelection():
            return

        # Get selected text
        selected_text = cursor.selectedText()

        # Split into lines
        lines = selected_text.split('\u2029')  # QTextEdit uses Unicode paragraph separator

        processed_lines     = processing_function( lines )
        processed_text      = "\n".join( processed_lines )

        # Store selection positions
        selection_start = cursor.selectionStart()
        selection_end   = cursor.selectionEnd()

        # Replace selected text
        cursor.insertText( processed_text )

        # Restore selection
        cursor.setPosition(selection_start)
        cursor.setPosition(selection_end, cursor.KeepAnchor)
        text_edit.setTextCursor(cursor)

    #-----------------------------------
    def remove_blank_linexxxxxs( self,   ):
        """
        because of call from menu no options could use partial there
        """
        processing_function     = partial( clip_string_utils.clean_string_list_to_list,
                                          delete_tailing_spaces  = True,
                                          delete_blank_lines     = True,   )

        self.process_selected( processing_function = processing_function )

        # new_lines  = clip_string_utils. clean_string_to_list( in_text,
        #                       delete_tailing_spaces  = True,
        #                       delete_comments        = False,
        #                       delete_blank_lines     = False,   )
        # # Get the current cursor and selection

        # # text_edit   = self
        # # cursor      = text_edit.textCursor()
        # if not cursor.hasSelection():
        #     return

        # # Get selected text
        # selected_text = cursor.selectedText()

        # # Split into lines and remove trailing spaces
        # lines = selected_text.split('\u2029')  # QTextEdit uses Unicode paragraph separator

        # if keep_leading:
        #     trimmed_lines = [line.rstrip() for line in lines]
        # else:
        #     trimmed_lines = [line.strip() for line in lines]

        # trimmed_text = '\n'.join(trimmed_lines)

        # # Store selection positions
        # selection_start = cursor.selectionStart()
        # selection_end   = cursor.selectionEnd()

        # # Replace selected text
        # cursor.insertText(trimmed_text)

        # # Restore selection
        # cursor.setPosition(selection_start)
        # cursor.setPosition(selection_end, cursor.KeepAnchor)
        # text_edit.setTextCursor(cursor)

    # ------------------------
    def remove_blank_lines_zz( self, lines ):
        """
        static
        ?? perhaps a util
        delete leading spaces ( as per code )
        then return as a multiline string  that is a list of strings
            lines   is a list of lines

        """
        pass
        # new_lines  = clip_string_utils. clean_string_to_list( in_text,
        #                       delete_tailing_spaces  = True,
        #                       delete_comments        = False,
        #                       delete_blank_lines     = False,   )

    #-----------------------------
    def shell_file( self, file_name ):
        """ """
        if platform.system() == 'Windows':
            os.startfile(file_name)

        elif platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', file_name))

        else:  # Linux
            subprocess.call(('xdg-open', file_name ) )

    #-----------------------------------
    def paste_clipboard( self, ):
        """
        what it says
        """
        text    = QApplication.clipboard().text( )
        self.insert_text_at_cursor( text )

    #-----------------------------------
    def copy_all( self, ):
        """
        what it says
        """
        QApplication.clipboard().setText(self.toPlainText())

    #-----------------------------------
    def search_selected( self, keep_leading = True ):
        """
        default not working from menu ??
        """
        text_edit   = self
        cursor      = text_edit.textCursor()
        if not cursor.hasSelection():
            return

        # Get selected text
        selected_text = cursor.selectedText()

        # Split into lines and remove trailing spaces
        lines = selected_text.split('\u2029')  # QTextEdit uses Unicode paragraph separator

        if keep_leading:
            trimmed_lines = [line.rstrip() for line in lines]
        else:
            trimmed_lines = [line.strip() for line in lines]

        trimmed_text = '\n'.join(trimmed_lines)

        # Store selection positions
        selection_start = cursor.selectionStart()
        selection_end   = cursor.selectionEnd()

        # ---- search here
        self.stuffdb_app_global.mdi_management.do_db_search( "search",  [ trimmed_text ] )

        # Restore selection
        cursor.setPosition(selection_start)
        cursor.setPosition(selection_end, cursor.KeepAnchor)
        text_edit.setTextCursor(cursor)

    #-----------------------------------
    def strip_selected( self, keep_leading = True ):
        """
        default not working from menu ??
        """
        # Get the current cursor and selection
        text_edit   = self
        cursor      = text_edit.textCursor()
        if not cursor.hasSelection():
            return

        # Get selected text
        selected_text = cursor.selectedText()

        # Split into lines and remove trailing spaces
        lines = selected_text.split('\u2029')  # QTextEdit uses Unicode paragraph separator

        if keep_leading:
            trimmed_lines = [line.rstrip() for line in lines]
        else:
            trimmed_lines = [line.strip() for line in lines]

        trimmed_text = '\n'.join(trimmed_lines)

        # Store selection positions
        selection_start = cursor.selectionStart()
        selection_end   = cursor.selectionEnd()

        # Replace selected text
        cursor.insertText(trimmed_text)

        # Restore selection
        cursor.setPosition(selection_start)
        cursor.setPosition(selection_end, cursor.KeepAnchor)
        text_edit.setTextCursor(cursor)


    #-----------------------------------
    def smarten( self, ):
        """
        like smart paste but copy then smart paste

        text_edit       = self
        cursor          = text_edit.textCursor()
        selected_text   = cursor.selectedText()

        later do withot going thru the clipboard

        see capture selected text -- how differnt thena copy

        """
        self.copy()
        self.smart_paste_clipboard()

    #-----------------------------------
    def smart_paste_clipboard( self, ):
        """
        what it says

            consider strip out tabs....
            detect line contentns and prefix with >> ...
            string_util.begins_with_url( a_string )

            may want to make more advanced, look at file extension
            .txt  .py????

            /home/russ/anaconda.sh
             ~/russ/anaconda.sh

        """
        text            = QApplication.clipboard().text( )
        splits          = text.split( "\n" )
        new_lines       = []

        for i_line in splits:
            ii_line      = i_line

            if string_util.begins_with_url( i_line ):
                ii_line  = f">>url   {i_line}"

            elif string_util.begins_with_file_name( i_line ):
                ii_line  = f">>shell   {i_line}\n>copy     {i_line}"

            new_lines.append( ii_line )

        # !! integrate the next if a multiline
        #new_lines.append( "the end")
        new_text = "\n".join( new_lines )

        self.insert_text_at_cursor( new_text )
        self.insert_text_at_cursor( "" )       # extra line at end

    #------------------------------------
    def goto_urls_in_selection(self, ):
        """
        what it says

            and/or look in clipboard utils
        """
        text_edit       = self
        cursor          = text_edit.textCursor()
        selected_text   = cursor.selectedText()

        if not selected_text:
            return None

        lines           = selected_text.split('\u2029')
        stripped_lines  = [line.strip() for line in lines]
        for i_line in stripped_lines:
            j_line    = i_line.lower()
            if j_line.startswith( ">>url" ):
                i_line = i_line[ 5: ]

            # i_line.replace( ">>url", "") # what about caps -- do better
            i_line    = i_line.strip( )
            if string_util.begins_with_url( i_line ):
                # msg    = f" webbrowser.open {i_line = }"
                # print( msg )
                splits = i_line.split( " " )
                i_line = splits[0]
                webbrowser.open( i_line, new = 0, autoraise = True )

    # ------------------------
    def insert_text_at_cursor( self, text ):
        """
        insert text at the cursor position
        """
        text_edit       = self
        cursor          = text_edit.textCursor()
        cursor.insertText( text )

    # ---- new stuff for block indent from claude check and debug

    def indent_selected_text(self):
        """Indent selected text to the next tab stop."""
        cursor = self.textCursor()

        # If no selection, insert spaces to next tab stop at cursor position
        if not cursor.hasSelection():
            self._indent_at_cursor(cursor)
            return

        # Get selection boundaries
        start_pos = cursor.selectionStart()
        end_pos = cursor.selectionEnd()

        # Move cursor to start of selection to get line information
        cursor.setPosition(start_pos)
        start_block = cursor.block()

        # Move cursor to end of selection
        cursor.setPosition(end_pos)
        end_block = cursor.block()

        # Calculate indentation needed
        indent_spaces = self._calculate_indent_spaces(start_block)
        if indent_spaces <= 0:
            return  # No indentation needed or error occurred

        # Store original selection for restoration
        original_start = start_pos
        original_end = end_pos

        # Begin editing operation
        cursor.beginEditBlock()

        try:
            # Indent all lines in selection
            current_block = start_block
            position_offset = 0

            while current_block.isValid() and current_block.blockNumber() <= end_block.blockNumber():
                # Move cursor to beginning of current line
                cursor.setPosition(current_block.position())

                # Insert spaces at the beginning of the line
                spaces_to_add = ' ' * indent_spaces
                cursor.insertText(spaces_to_add)

                # Update position offset for selection restoration
                position_offset += indent_spaces

                # Move to next block
                current_block = current_block.next()

            # Restore selection with adjusted positions
            new_start = original_start + indent_spaces
            new_end = original_end + position_offset

            cursor.setPosition(new_start)
            cursor.setPosition(new_end, QTextCursor.KeepAnchor)

        except Exception as e:
            print(f"Error during indentation: {e}")
        finally:
            cursor.endEditBlock()
            self.setTextCursor(cursor)

    def unindent_selected_text(self):
        """
        !! think this can use process_selectde instad
        Remove indentation (Shift+Tab functionality).
        """
        cursor = self.textCursor()

        if not cursor.hasSelection():
            return

        # Get selection boundaries
        start_pos = cursor.selectionStart()
        end_pos = cursor.selectionEnd()

        cursor.setPosition(start_pos)
        start_block = cursor.block()

        cursor.setPosition(end_pos)
        end_block = cursor.block()

        # Begin editing operation
        cursor.beginEditBlock()

        try:
            current_block = start_block
            total_removed = 0

            while current_block.isValid() and current_block.blockNumber() <= end_block.blockNumber():
                line_text = current_block.text()

                # Calculate how many spaces to remove (up to tab_width)
                spaces_to_remove = 0
                for char in line_text[:self.tab_width]:
                    if char == ' ':
                        spaces_to_remove += 1
                    else:
                        break

                if spaces_to_remove > 0:
                    # Remove spaces from beginning of line
                    cursor.setPosition(current_block.position())
                    cursor.setPosition(current_block.position() + spaces_to_remove, QTextCursor.KeepAnchor)
                    cursor.removeSelectedText()
                    total_removed += spaces_to_remove

                current_block = current_block.next()

            # Restore selection with adjusted positions
            spaces_removed_from_start = min(self.tab_width, len(start_block.text()) - len(start_block.text().lstrip(' ')))
            new_start = max(start_pos - spaces_removed_from_start, start_block.position())
            new_end = end_pos - total_removed

            cursor.setPosition(new_start)
            cursor.setPosition(new_end, QTextCursor.KeepAnchor)

        except Exception as e:
            print(f"Error during unindentation: {e}")
        finally:
            cursor.endEditBlock()
            self.setTextCursor(cursor)

    #-----------------------------------
    def _indent_at_cursor(self, cursor):
        """Handle tab when there's no selection - insert spaces to next tab stop.

        """
        try:
            # Get current line and cursor position within the line
            current_block = cursor.block()
            cursor_pos_in_block = cursor.positionInBlock()

            # Calculate spaces needed to reach next tab stop
            spaces_to_next_tab = self.tab_width - (cursor_pos_in_block % self.tab_width)

            # Insert spaces
            cursor.insertText(' ' * spaces_to_next_tab)

        except Exception as e:
            print(f"Error during cursor indentation: {e}")

    def _calculate_indent_spaces(self, start_block):
        """Calculate how many spaces to add based on the first non-blank line."""
        try:
            current_block = start_block

            # Find the first non-blank line
            while current_block.isValid():
                line_text = current_block.text()
                stripped_text = line_text.lstrip(' \t')

                if stripped_text:  # Found non-blank line
                    # Count leading spaces (convert tabs to spaces for calculation)
                    leading_spaces = 0
                    for char in line_text:
                        if char == ' ':
                            leading_spaces += 1
                        elif char == '\t':
                            leading_spaces += self.tab_width
                        else:
                            break

                    # Calculate spaces needed to reach next tab stop
                    next_tab_stop = ((leading_spaces // self.tab_width) + 1) * self.tab_width
                    return next_tab_stop - leading_spaces

                current_block = current_block.next()

            # If no non-blank lines found, default to tab_width spaces
            return self.tab_width

        except Exception as e:
            print(f"Error calculating indent spaces: {e}")
            return 0




# ---- Edits are also for criteria
# ---------------------------------
class CQEditBase(   ):
    """
    second parent for QT edit child controls

    do not need prior value it is just sitting in the control

    get rid of is_changed ??
                prior_data
                events for above

    """
    def __init__( self,
                 parent                 = None        ,
                 field_name             = None      ,
                 is_keep_prior_enabled  = None   ):  # perhaps last should be false or is it defaulted later
        """
        read it
        appears to be a mixin as it is only used to add methods to other classes

        should always be called by descendants all args required
        but having trouble with inherit so added defaults
        may check some for none and except
        """
        # print( "        begin init CQEditBase")
        # super(   ).__init__(   )  no parent
        self.context_menu           = None  # override if one is added
        if not field_name:
            pass
            #rint( "!! CQEditBase need except here ??")
            # 1/0
        # can be used as interface
        self.field_name             = field_name

        self.is_keep_prior_enabled  = is_keep_prior_enabled

        # ---- keep for now but may be dead
        self.null_surogate          = None
            # find a value to use as null surrogate
            # can be used in interface, not sure if this should be "" or None

        # ---- these are private change to _
        # prior value, prior_type -- likely already in edit
        self.prior_value            = None     # value last set from a record ot to record
                                                # set to something valid for edit in its init

        # self.is_field_valid         =  not set makes all ok
        self.debug_format           = "not_set"

        self.cnv_str_to_str_strip   = None    # replacable function for stripping


        # next noet here as only appropriate for some edits
        # self.returnPressed.connect( self.on_return_pressed )

    # ---- dict oriented ----------------
    #----------------
    def edit_to_dict( self, a_dict, format = None ):
        """
        new
        from edit to a dict with conversion
        """
        data   = self.get_raw_data( )
        data   = self.edit_to_dict_cnv( data,  )
        a_dict[ self.field_name ] = data

    #----------------
    def edit_to_dict_cnv( self, data, format = None ):
        """
        new
        replaceable function for data_edit_to_dict
        widget.data_edit_to_dict   = self.....
        format should be used with closures
        """
        msg    = f"edit_to_dict_cnv should have been replaced for {self.field_name = }"
        logging.error( msg )
        raise NotImplementedError( msg )

    #----------------
    def dict_to_edit( self, a_dict, ):
        """
        new
        from dict to edit with conversion
        """
        data   = a_dict[ self.field_name ]
        data   = self.dict_to_edit_cnv( data, )
        self.set_preped_data( data )

    #----------------
    def dict_to_edit_cnv( self, data, format = None ):
        """
        new
        replaceable function for data_edit_to_dict
        widget.data_edit_to_dict   = self.....
        """
        msg    = f"dict_to_edit_cnv should have been replaced for {self.field_name = }"
        logging.error( msg )
        raise NotImplementedError( msg )
        return data

    # ---- record oriented ----------------
    #----------------------------
    def rec_to_edit( self, record, ):
        """
        convert from record format to edit format
        this is more or less a prototype
        note that I know my own field_name
        """
        self.debug_format   = format   # unhide the closure
        field_name          = self.field_name

        raw_data            = get_rec_data( record, field_name )
        converted_data      = self.rec_to_edit_cnv( raw_data, )
        self.set_preped_data( converted_data )

    #----------------
    def rec_to_edit_cnv( self, data, format = None ):
        """
        new
        replaceable function for data_edit_to_dict
        widget.data_edit_to_dict   = self.....
        """
        msg    = f"rec_to_edit_cnv should have been replaced for {self.field_name = }"
        logging.error( msg )
        raise NotImplementedError( msg )
        return data

    #----------------------------
    def edit_to_rec( self, record, ):
        """

        """
        raw_data            = self.get_raw_data()
        converted_data      = self.edit_to_rec_cnv( raw_data )
        set_rec_data( record, self.field_name, converted_data )

    #----------------
    def edit_to_rec_cnv( self, data ):
        """
        new
        replaceable function for data_edit_to_dict
        widget.data_edit_to_dict   = self.....
        """
        msg    = f"edit_to_rec_cnv should have been replaced for {self.field_name = }"
        logging.error( msg )
        raise NotImplementedError( msg )
        return data

    #--------------------------------
    def build_criteria( self, a_dict ):
        """
        mutate the dict for criteria
        think this is how we build criteria for criteria select
        note we always get raw data
        generally not replaceable
        """
        # msg   = ( f"CQEditBase {self.field_name} {self.get_raw_data()}")
        # logging.debug( msg )

        a_dict[ self.field_name ] = self.get_raw_data()

    # ---- low level no conversion get/set
    #----------------------------
    def get_raw_data( self, ):
        """'
        implemented in child
        may be intended to get data in typed format
        comment is wrong  -- final step from set_data should always be qdate
        because getting data depends on type of underlying edit
        """
        msg         = f"get_raw_data This function is not implemented yet. \n {str( self ) = }"
        raise NotImplementedError( msg )

    #----------------------------
    def set_preped_data( self, data, is_changed = None ):
        """'
        final step from set_data should always be qdate for a date edit....
        is it generally overridden?\
        no think should be ok here too
        """
        msg    = f"set_prepped_data should have been replaced for {self.field_name = }"
        logging.error( msg )
        raise NotImplementedError( msg )

    #----------------------------
    def set_data( self, data, is_changed = None ):
        """
        seem same as set_prepped_data so drop ??
        """
        self.set_preped_data( data, is_changed = is_changed )

    # ---- set clear default prior -------------------------
    # -----------------------
    def set_clear( self   ):
        """
        can be replaced with pretty much anything that does
        self.set_prepped_data( data ) or pass at the end


        really want three variations, clear, clear_default ( if a default value )
            clear_or_prior, clear_or_default clear  all from clear_or
        """
        msg         = f"set_clear should have been replaced for {self.field_name = }"
        logging.error( msg )
        raise NotImplementedError( msg )

    # -----------------------
    def set_default( self   ):
        """
        can be replaced with pretty much anything that does
        self.set_prepped_data( data ) or pass at the end

        really want three variations, clear, clear_default ( if a default value ) clear_or_prior, clear_or_default clear  all from clear_or
        """
        msg         = f"set_default should have been replaced for {self.field_name = }"
        logging.error( msg )
        raise NotImplementedError( msg )

    # -----------------------
    def set_prior( self   ):
        """
        can be replaced with pretty much anything that does
        self.set_prepped_data( data ) or pass at the end
        pass for it to do nothing else may want to use one of above functions

        really want three variations, clear, clear_default ( if a default value ) clear_or_prior, clear_or_default clear  all from clear_or
        """
        msg         = f"set_prior should have been replaced for {self.field_name = }"
        logging.error( msg )
        raise NotImplementedError( msg )

    # -----------------------
    def set_value( self, a_value  ):
        """
        complete this code:
            set_data_to_default    = partial( set_data_to_default, "" )
        function to set the default to a value
        should be correct type without  conversion
        look for
             a_partial           = partial( self.do_ct_value, "" )

        """
        # # for conditional debug
        # if self.field_name == "sub_dir":
        #     breakpoint()
        #rint( "set_data_to_default_value {a_value = }" )
        self.set_preped_data( a_value, is_changed = True )
        # debug_msg   = ( f"do_ct_value {self.field_name}")
        # logging.log( LOG_LEVEL,  debug_msg, )

        pass # debug

    def set_pass( self, ):
        """
        set to prior by passing
        """
        pass

    # ---- validate  implementations -----------------------
    #-----------------------------
    def is_field_valid( self, option = None ):   # seems to help keep and test
        """
        replaceable, else all valid
        change validate to is_field_valid
        need to return a message could be thru and exception or just
        a return value for now None or "" means ok else
        contain an error message
        this needs work for now just checking it it called
        !! look in descendant
        plug in this function
        """
        pass
        # msg         = f"is_field_valid not implemented yet. \n self = {self }"
        # logging.error( msg )
        # raise NotImplementedError( msg )
        # return


    #-----------------------------

    #-----------------------------
    def validate_is_int( self ):
        """
        could make class an argument to the function
        may raise exception

        """
        data   = self.get_raw_data().strip()
        if data == "":
            return
        # just throw for now
        try:
            int_maybe   = int( data )

        except Exception as an_except:   #  or( E1, E2 )

            msg     = f"a_except         >>{an_except}<<  type  >>{type( an_except)}<<"
            logging.error( msg )   # logger.log  ERROR  DEBUG  logging.debug  .error

            msg     = f"an_except.args   >>{an_except.args}<<"
            logging.error( msg )   # logger.log  ERROR  DEBUG  logging.debug  .error

            msg     = f"self = {self}"
            logging.error( msg )   # logger.log  ERROR  DEBUG  logging.debug  .error

            s_trace = traceback.format_exc()
            msg     = f"format-exc       >>{s_trace}<<"
            logging.error( msg )   # logger.log  ERROR  DEBUG  logging.debug  .error
            #AppGlobal.logger.error( msg )   #    AppGlobal.logger.debug( msg )
            raise
        #     #raise  # to re-raise same
        # finally:
        #     msg     = f"in finally  {1}"
        #     print( msg )
        return

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

        # just throw for now
        self.validate_is_int()
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

    #------------
    # ---- events  not clear if all implemented ------------
    def call_on_return_pressed( self, ):
        self.on_return_pressed()

    #-----------------------------
    def on_return_pressed( self ):
        """
        read it
        widget.function_on_return   = function_to_do_something
        if function does not have return_pressed functionality you can set to anything
        makes the api uniform
        may be replaced else just a pass -- the replacement doe not seem to work
        so will try more indirect -- think if I had used a lambda to set up
        direct call world be ok
        """
        pass
        # print( f"{self.on_return_pressed = }")
        # print( f"{self.on_return_pressed  = }")

    #-----------------------------
    def on_value_changed( self ):
        """
        read it
        may be replaced
        different widgets have different events for this
        they will be directed here for a uniform interface
        useful in particular by criteria

        makes the api uniform

        """
        pass

    #----------------------------
    def show_context_menu_seemed_wrong(self, global_pos):
        """ chat code, modified a bit
        code for this in TextEditExtMixin or for each edit

        """
        pass
        # self.context_menu.exec( global_pos )
        # lets see if   self.context_menu  is just self
        self.exec( global_pos )

    #----------------------------
    def handle_right_click(self, event):
        """ chat code, modified a bit
            may be dead code
        """
        if event.button() == Qt.RightButton:
            self.show_context_menu(event.globalPos())
        # else:
        #     # Call the parent class method for other events
        #     super(QLineEdit, self.line_edit).mousePressEvent(event)

    # ---- replaceable functions
    #----------------------------
    def cnv_str_to_str( self, data ):
        """
        perhaps the easiest conversion
        """
        if self.cnv_str_to_str_strip:
            data    = self.cnv_str_to_str_strip( data )


        return data

    #----------------------------
    def cnv_str_to_str_strip_eol( self, data ):
        """
        for now from a multiline edit later expand
        """
        processed_lines = [line.rstrip() for line in data.splitlines()]

        final_text      = "\n".join( processed_lines )


        return final_text



    #----------------------------
    def cnv_str_to_int( self, data ):
        """
        read
        may need null management adj
        could strip ??
        """
        if data in [ None, ""]:
            converted_data      = None

        else:
            converted_data      = int( data )

        return converted_data

    #----------------------------
    def cnv_int_to_str( self, data  ):
        """
        convert dictionary data to a new data type
        here new = old string to string
        perhaps the easiest conversion
        """
        if data is None:
            converted_data      = ""

        else:
            converted_data      = str( data )

        return converted_data

    #----------------------------
    def cnv_qdate_to_int( self, qdate ):
        """
        int is a timestamp
        convert dictionary data to a new data type
        should be ts timestamp not int
        """
        py_datetime  = datetime( qdate.year(), qdate.month(), qdate.day())
        timestamp    = int( py_datetime.timestamp() )
        return timestamp

        # pass   # debug
        # if data in [ None, "" ]:
        #     qdate         = QDate()   # says chat invalid

        # else:
        #     #timestamp = 1710432000  # Example Unix timestamp in seconds
        #     qdate         = QDateTime.fromSecsSinceEpoch( data ).date()

        # return qdate

    #----------------------------
    def cnv_str_to_qdate( self, data ):
        """
        converted_data  is QDate
        """
        #date_string = "2019-08-10"
        try:
            converted_data  = QDate.fromString( data, QT_DATE_FORMAT )

        except ValueError as error:
            error_message   = str(error)
            msg             = (f"Caught an error: for {self.field_name = } {error_message}")
            logging.error( msg )

        return converted_data

    #----------------------------
    def cnv_qdate_to_str( self, data ):
        """
        data is a qdate we assume
        """
        try:
            converted_data = data.toString( QT_DATE_FORMAT )

        except ValueError as error:
            error_message   = str(error)
            msg             = ( f"Caught an error: for {self.field_name = } {error_message}" )
            logging.error( msg )

        return converted_data

    #----------------------------
    def cnv_int_to_qdate( self, data ):
        """
        convert dictionary data to a new data type

        """
        #if data is None:
        if data in [ None, "" ]:  # how do we get string here
            converted_data  = QDate( 1900, 1, 1 ) # surrogate for None
            # msg         = ( f"cnv_dict_int_to_qdate Fieintld {self.field_name} "
            #                 f"got data of None used surrogate None ")

            # raise ValueError( msg )

        else:
            # may need something for floats
            if isinstance( data, float ):
                data = int( data )

            if not isinstance( data, int ):
                msg   = ( f"Data {self.field_name} is not instance of int = timestamp {data = } {type(data) = }  " )
                logging.error( msg )

                raise ValueError( msg )  # or should we continue
                return   QDate( 1901, 1, 1 ) # surrogate for None but after raise
            data    = int( data )   # assume this works from float
            a_datetime          = datetime.fromtimestamp( data )

            converted_data      = QDate( a_datetime.year, a_datetime.month, a_datetime.day )

        return converted_data

    #----------------------------
    def rec_to_dict_cb( self, record, format = None ):
        """
        not new may need revision
        from a record to a dict type combo Boxes
        will only work on dict based edits

        record to dictionary based combo box
        """
        # self.debug_format   = format   # unhide the closure
        field_name          = self.field_name

        raw_data            = get_rec_data( record, field_name )
            # should be key in dict

        # converted_data      = raw_data

        # if converted_data is None:
        #     converted_data      = ""

        # is raw_data a valid key in the dict
        if  self.is_key_in_dict( raw_data ):
            pass
            """got the data in the dict ok to go"""

        else:
            #stuff_document reference -- may not have use ModuleNotFoundError

            info_ignored   = self.get_info_for_id( raw_data )
                # will fix the dict

    #----------------------------
    def dict_cb_to_rec( self, record, format = None  ):
        """
        inverse of rec_to_dict_cb
        """
        # raw_data    = self.get_raw_data()
        # set_rec_data( record, raw_data )
        raw_data            = self.get_raw_data()
        # raw and converted should be the same

        set_rec_data( record, self.field_name, raw_data )

        return raw_data # for debug
        # get_selected_key( raw_data )   --- good chance this is wrong

    # ---- debug ------------------------


    def __str__( self ):
        a_str   = ""
        a_str   = ">>>>>>>>>>* CQEditBase *<<<<<<<<<<<<"

        # a_str   = string_util.to_columns( a_str, ["clear_value",
        #                                    f"{self.clear_value}" ] )
        a_str   = string_util.to_columns( a_str, ["context_menu",
                                           f"{self.context_menu}" ] )


        a_str   = string_util.to_columns( a_str, ["field_name",
                                           f"{self.field_name}" ] )


        a_str   = string_util.to_columns( a_str, ["get_raw_data()",
                                           f"{str(self.get_raw_data()) } " ] )

        return a_str

#-------------------------------
class CQLineEdit( QLineEdit, CQEditBase ):
    """
    read it
    custom_widgets.CQLineEdit
    """
    def __init__(self,
                 parent                 = None,
                 field_name             = None,
                 is_keep_prior_enabled  = False):
        """
        read it
        in   -- into the widget
        out  -- out to the record
        """
        #super(   ).__init__(   )   # seems to go to CQEditBase ???

        QLineEdit.__init__( self, None  )

        CQEditBase.__init__( self,
                 parent                 = parent,
                 field_name             = field_name,
                 is_keep_prior_enabled  = is_keep_prior_enabled )

        # ---- keep for now but may be dead
        self.null_surogate          = None
            # find a value to use as null surrogate
            # can be used in interface, not sure if this should be "" or None


        # ---- set functions by default
        #a_partial           = partial( self.do_ct_value, "do_ct_value!!" )
        a_partial               = partial( self.set_value, a_value = "" )
        self.set_clear          = a_partial
        self.set_default        = a_partial
        if self.is_keep_prior_enabled:
            self.set_prior      = self.set_pass
        else:
            self.set_prior      = a_partial

        #self.is_field_valid     = # default is all pass

        # ---- in out conversion
        self.rec_to_edit_cnv    = self.cnv_str_to_str
        self.edit_to_rec_cnv    = self.cnv_str_to_str

        self.dict_to_edit_cnv   = self.cnv_str_to_str
        self.edit_to_dict_cnv   = self.cnv_str_to_str

       #  self.is_field_valid     = if not set all valid a pass

        # issue of when evaluated this may be at compile vs lambda later
        self.returnPressed.connect( self.call_on_return_pressed )

        # self.textChanged.connect( self.on_value_changed  )
        self.textChanged.connect( lambda: self.on_value_changed() )
        #lambda: self.criteria_changed( True )

            # call in all edits where it applies
        self.setPlaceholderText( self.field_name )
        #self._build_context_menu()

    # ---- required implementations
    #----------------------------
    def set_preped_data( self, a_string, is_changed = None ):
        """
        specialize for this edit
        what about prior value

        a prepped data is data in the format for the edit and
        formatted and ready for the edit.

        arg
            is_changed     None      leave is_changed as it was
                           True        is_changed set to True
                           False        is_changed set to False
                           other       undefined behavior
        mutates

            changes contents of edit
            may change self.is_changed
            self.prior_value  -- so far unchanged, this is probably wrong
        """
        # next !! debug
        if a_string == None:
            a_string   = self.null_surogate
            msg        = f"line edit using null_surrogate for {self.field_name}"
            logging.debug( msg )

        elif not isinstance( a_string, str ):
            self_field_name   = self.field_name
            msg = f"set_prepped_data error a_string, not a string {self.field_name = }  return for now inspect then break"
            logging.debug( msg )
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

        if self.field_name == "text_data":
            pass   # conditional breakpoint

        if is_changed is not None:
            self.is_changed = is_changed

    #----------------------------
    def get_raw_data( self, ):
        """'
        make get edit data in future
        final step from set_data should always be a string for
        this edit
        """
        data  = self.text()
        return data

    #----------------------------
    def set_custom_context_menu( self, ):
        """
        what it says
            call in the init of the final widget ?
        """
        # self.setContextMenuPolicy( QtCore.Qt.CustomContextMenu)
        self.setContextMenuPolicy( CustomContextMenu)  # 5 6 compat


        self.customContextMenuRequested.connect( self.show_context_menu )

    # ---------------------------------------
    def show_context_menu( self, pos ):
        """
        from text edit mixin

        """
        widget      = self
        menu        = QMenu( widget )

        # Enable/disable actions based on context
        #cursor = widget.textCursor()
       # has_selection   = cursor.hasSelection()
        #can_undo        = widget.document().isUndoAvailable()
        #can_paste       = QApplication.clipboard().text() != ""


        # cut_action.setEnabled(has_selection)
        # copy_action.setEnabled(has_selection)
        # paste_action.setEnabled(can_paste)
        # foo_action.setEnabled(can_paste)

        # Add standard actions
        undo_action = menu.addAction("Undo_just_test")
        #undo_action.triggered.connect(widget.undo)
        undo_action.setEnabled( False )
        menu.addSeparator()

    # ---------------------------------------
    def show_context_menu_old_ng( self, pos ):
        """

        chat thinks this is way to go
        get code from text edit and model on it
        """
        widget      = self
        # self.my_special_function(event) for context

        # Call the base implementation (shows default context menu)
        super( CQLineEdit, self).contextMenuEvent( event )



    # ---- crud cycle -------------------------------
    # # -----------------------
    # def set_data_to_clear( self   ):
    #     """
    #     often replaced with ... set_data_to_....
    #     but could be clear or default or pass
    #     """
    #     self.set_prepped_data( "", is_changed = True )
    #     pass # debug

    # # ------------------------------------
    # def on_text_changedxxxxx( self, new_data ):
    #     """
    #     !! probably phase out
    #     may be edited or messed with
    #     on data change for each drop the new data
    #     this is probably a bit messed up but also not needed??
    #     """
    #     #self.is_changed  = True
    #     self.on_data_changed( )
    #     self.prior_value   = new_data
    #     #rint(f"line edit on_data_changed: {new_data} saved to prior_value ")  !!

    # -------------------------
    def _build_context_menu_is_used_correct ( self ):
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

        # select_all_action = context_menu.addAction("PrintStr")
        # select_all_action.triggered.connect(self.print_str )

        # Connect actions to QLineEdit methods

        redo_action.triggered.connect(self.redo)
        cut_action.triggered.connect(self.cut)
        copy_action.triggered.connect(self.copy)
        paste_action.triggered.connect(self.paste)


        # Show the context menu at the cursor position
        # context_menu.exec(QCursor.pos())

        #self.mousePressEvent = self.handle_right_click
        # !! disable as we do not have yet
        # Disable the default context menu
        #self.setContextMenuPolicy(Qt.NoContextMenu)

    # -------------------------------
    def __str__( self ):

        a_str   = ""

        a_str   = f"{a_str}{CQEditBase.__str__( self, )    }"

        a_str   = f"{a_str}\n>>>>>>>>>>* CQLineEdit *<<<<<<<<<<<<"


        # a_str   = string_util.to_columns( a_str, ["default_value",
        #                                    f"{self.default_value}" ] )
        # a_str   = string_util.to_columns( a_str, ["is_changed",
        #                                    f"{self.is_changed}" ] )
        a_str   = string_util.to_columns( a_str, ["field_name",
                                           f"{self.field_name}" ] )
        # a_str   = string_util.to_columns( a_str, ["prior_value",
        #                                    f"{self.prior_value}" ] )
        a_str   = string_util.to_columns( a_str, ["get_raw_data()",
                                           f"{self.get_raw_data()}" ] )

        # more    = CQEditBase.__str__( self, )
        # a_str   = f"{a_str}\n{more}"
        return a_str

#-------------------------------
class CQComboBox( QComboBox, CQEditBase ):
    """
    read it
    custom_widgets.CQComboBoxEdit
        from the line edit
        lets see what we can get rid of
        start with non editable

    try         self.setEditable(True)
    """
    def __init__(self,
                 parent                 = None,
                 field_name             = None,
                 is_keep_prior_enabled  = False):

        """
        read it
        in   -- into the widget
        out  -- out to the record
        """
        #super(   ).__init__(   )   # seems to go to CQEditBase ???

        QLineEdit.__init__( self, None  )     # need arg ?

        CQEditBase.__init__( self,
                        parent             = None,
                        field_name         = field_name,
                               )

        # self.setEditable(True)  # !! may need to be at top debug make ...
        self.default_typexxx          = "string"          # deprecate
        #self.default_value         = "default-value"     # deprecate
        self.prior_value           = ""  # something of a valid type
        #self.textEdited.connect(self.on_text_changed )  #  text is sent new_text
        #self.textChanged.connect(self.on_text_changed)
            #-----------------------------
        self.null_surogatexxx          = ""
        # ---- set functions
        #a_partial           = partial( self.do_ct_value, "do_ct_value!!" )
        a_partial           = partial( self.set_value, "" )
        self.set_default    = a_partial

        self.set_prior      = self.set_pass
        #self.validate       = self.validate_all_ok

        # in out conversion need same for dict
        self.rec_to_edit_cnv    =  self.cnv_str_to_str
        self.edit_to_rec_cnv    =  self.cnv_str_to_str

        self.setPlaceholderText( self.field_name )   # can we set on combo
        #self.addItems( [ "", "atest", "bbbbbb", "cccccc", ] )

    # currentIndexChanged( int index )
    # self.combo_box.currentIndexChanged.connect(self.on_index_changed)

        self.currentIndexChanged.connect( self.on_value_changed )

    # ---- required implementations
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
                           other       undefined behavior
        mutates

            changes contents of edit
            may change self.is_changed
            self.prior_value  -- so far unchanged, this is probably wrong

        """
        # next !! debug
        if a_string == None:
            a_string   = self.null_surogate
            msg        = f"line edit using null_surrogate for {self.field_name}"

            logging.debug( msg )
        elif not isinstance( a_string, str ):
            self_field_name   = self.field_name
            msg = f"set_prepped_data error a_string, not a string {self.field_name = }  return for now inspect then break"
            logging.debug( msg )
            return
            wat_inspector.go(
                msg            = msg,
                # inspect_me     = self.people_model,
                a_locals       = locals(),
                a_globals      = globals(), )
            breakpoint()

        # self.setText( a_string  )   #
        self.setCurrentText( a_string )
            # with prior there ? depending on is_changed ??
        self.prior_value  = a_string
        if is_changed is not None:
            self.is_changed = is_changed

    #----------------------------
    def get_raw_data( self, ):
        """'
        make get edit data in future
        final step from set_data should always be a string for
        this edit
        """
        #data  = self.text()
        data  = self.currentText()
        return data

    #----------------------------
    def add_items( self, a_list ):
        """'
        probably use addItems directly
        a_list is a list of strings
        """
        self.addItems( a_list  )

    # -------------------------
    def _build_context_menu_hide_no_delete( self ):
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

        # select_all_action = context_menu.addAction("PrintStr")
        # select_all_action.triggered.connect(self.print_str )

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

    # --------------------------
    def setPlaceholderText( self, ignoered ):
        """so we can call without harm """
        pass

    # --------------------------
    def returnPressed( self ):
        """so we can call without harm """
        pass

    # -------------------------------
    def __str__( self ):

        a_str   = ""

        a_str   = f"{a_str}{CQEditBase.__str__( self, )    }"

        a_str   = f"{a_str}\n>>>>>>>>>>* CQLineEdit *<<<<<<<<<<<<"

        a_str   = string_util.to_columns( a_str, ["default_type",
                                           f"{self.default_type}" ] )
        # a_str   = string_util.to_columns( a_str, ["default_value",
        #                                    f"{self.default_value}" ] )
        a_str   = string_util.to_columns( a_str, ["is_changed",
                                           f"{self.is_changed}" ] )
        a_str   = string_util.to_columns( a_str, ["field_name",
                                           f"{self.field_name}" ] )
        a_str   = string_util.to_columns( a_str, ["prior_value",
                                           f"{self.prior_value}" ] )
        a_str   = string_util.to_columns( a_str, ["get_raw_data()",
                                           f"{self.get_raw_data()}" ] )

        # more    = CQEditBase.__str__( self, )
        # a_str   = f"{a_str}\n{more}"
        return a_str


class CQHistoryComboBox( QComboBox, CQEditBase ):
    """
    Claud got me started
    A QComboBox subclass that allows text entry and maintains a history of entered text.
    The history is presented as dropdown options when the user clicks the dropdown arrow.

    """

    textSubmitted = pyqtSignal(str)  # Signal emitted when text is submitted

    def __init__(self,
                 parent                 = None,
                 field_name             = None,
                 is_keep_prior_enabled  = False):

        """
        read it
        in   -- into the widget
        out  -- out to the record
        """
        #super(   ).__init__(   )   # seems to go to CQEditBase ???

        QLineEdit.__init__( self, None  )     # need arg ?  # parent

        CQEditBase.__init__( self,
                        parent             = None,  # parent
                        field_name         = field_name,
                               )


    # def __init__(self, parent=None, max_history=10):
    #     """
    #     Initialize the HistoryComboBox.

    #     Args:
    #         parent: Parent widget
    #         max_history: Maximum number of history items to store
    #     """
        # super().__init__(parent)

        # Enable editing
        self.setEditable(True)

        # Set insert policy to not add duplicates automatically
        # self.setInsertPolicy(QComboBox.NoInsert)
        self.setInsertPolicy( NoInsert )  # 5 6 compat I hope
        # Store maximum history size
        self.max_history = 10

        # Connect signals
        self.lineEdit().returnPressed.connect(self.add_current_text_to_history)


        #self.default_value         = "default-value"     # deprecate
        self.prior_value           = ""  # something of a valid type
        #self.textEdited.connect(self.on_text_changed )  #  text is sent new_text
        #self.textChanged.connect(self.on_text_changed)
            #-----------------------------
        self.null_surogatexxx          = ""
        # ---- set functions
        #a_partial           = partial( self.do_ct_value, "do_ct_value!!" )
        a_partial           = partial( self.set_value, "" )
        self.set_default    = a_partial

        self.set_prior      = self.set_pass
        #self.validate       = self.validate_all_ok

        # in out conversion need same for dict
        self.rec_to_edit_cnv    =  self.cnv_str_to_str
        self.edit_to_rec_cnv    =  self.cnv_str_to_str

        self.setPlaceholderText( self.field_name )   # can we set on combo
        #self.addItems( [ "", "atest", "bbbbbb", "cccccc", ] )

    def add_current_text_to_history(self):
        """Add the current text to the history if not empty and not a duplicate."""
        text = self.currentText().strip()

        if not text:
            return

        # Check if the text is already in the history
        index = self.findText(text)

        if index >= 0:
            # If it exists, remove it so we can add it to the top
            self.removeItem(index)

        # Insert at the beginning
        self.insertItem(0, text)

        # If we've exceeded the maximum history size, remove the oldest item
        if self.count() > self.max_history:
            self.removeItem(self.count() - 1)

        # Keep the current text instead of clearing it
        # Set the current index to -1 to ensure the text remains visible
        self.setCurrentIndex(-1)
        self.setCurrentText(text)

        # Emit signal with the submitted text
        self.textSubmitted.emit(text)

    def keyPressEvent(self, event):
        """
        Handle key press events to add text to history when Enter is pressed.
        """
        #if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
        if event.key() == Key_Return or event.key() == Key_Enter:   # 5 6 compat


            #self.add_current_text_to_history()
            self.call_on_return_pressed()

        # Pass the event to the parent class
        super().keyPressEvent(event)

    def get_history(self):
        """Get the current history as a list of strings."""
        return [self.itemText(i) for i in range(self.count())]

    def set_history(self, history_list):
        """Set the history from a list of strings."""
        self.clear()
        for item in reversed(history_list):
            if item.strip():
                self.addItem(item)

    def clear_history(self):
        """Clear the history."""
        self.clear()

    def get_text(self):
        """Get the current text in the edit field."""
        return self.currentText()

    def set_text(self, text, add_to_history=True):
        """
        Set the text in the edit field.

        Args:
            text: Text to set
            add_to_history: If True, also adds the text to history
        """
        if add_to_history and text.strip():
            # Temporarily store the text
            stored_text = text.strip()

            # Check if the text is already in the history
            index = self.findText(stored_text)

            if index >= 0:
                # If it exists, remove it so we can add it to the top
                self.removeItem(index)

            # Insert at the beginning
            self.insertItem(0, stored_text)

            # If we've exceeded the maximum history size, remove the oldest item
            if self.count() > self.max_history:
                self.removeItem(self.count() - 1)

            # Set the current index to -1 to show the text in the edit field
            # without selecting an item from the dropdown
            self.setCurrentIndex(-1)

            # Make sure the text is set correctly
            self.setCurrentText(stored_text)
        else:
            # Just set the text without adding to history
            self.setCurrentText(text)

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
                           other       undefined behavior
        mutates

            changes contents of edit
            may change self.is_changed
            self.prior_value  -- so far unchanged, this is probably wrong


        """
        # next !! debug
        if a_string == None:
            a_string   = self.null_surogate
            msg        = f"line edit using null_surrogate for {self.field_name}"

            logging.debug( msg )
        elif not isinstance( a_string, str ):
            self_field_name   = self.field_name
            msg = f"set_prepped_data error a_string, not a string {self.field_name = }  return for now inspect then break"
            logging.debug( msg )
            return
            wat_inspector.go(
                msg            = msg,
                # inspect_me     = self.people_model,
                a_locals       = locals(),
                a_globals      = globals(), )
            breakpoint()

        # self.setText( a_string  )   #
        #self.setCurrentText( a_string )
        self.set_text(  a_string, add_to_history =True)

            # with prior there ? depending on is_changed ??
        self.prior_value  = a_string
        if is_changed is not None:
            self.is_changed = is_changed

    #----------------------------
    def get_raw_data( self, ):
        """'
        make get edit data in future
        final step from set_data should always be a string for
        this edit
        """
        #data  = self.text()
        data  = self.currentText()
        self.add_current_text_to_history(   )
        return data

    # --------------------------
    def setPlaceholderText( self, ignoered ):
        """
        so we can call without harm
        this widget cannot have placholder text
        """
        pass


#-------------------------------
class CQDictComboBox(QComboBox, CQEditBase ):
    """
    starting code from chat
    may need to run a select for values not in dd

    """
    def __init__(self,
                 parent                 = None,
                 field_name             = None,
                  is_keep_prior_enabled = None ):
        """ """

        # init both parents
        QLineEdit.__init__( self, None  )     # need arg ?

        CQEditBase.__init__( self,
                        parent                  = parent,
                        field_name              = field_name,
                        is_keep_prior_enabled   = is_keep_prior_enabled )

        debug_msg    = ( "say give each its own copy of index_to_key ... but could centralized ")
        logging.log( LOG_LEVEL,  debug_msg, )

        self.index_valid     = False   # false while in process of building
        self.index_to_key    = {}   # needs to be shared with one in mdi
                                    # anyway some issues

        # self.dict_data       = {}   # pointer to one in mdi

        # # others do this it might work for us with None
        # a_partial           = partial( self.do_ct_value, None )
        # self.ct_default     = a_partial
        # self.ct_prior       = self.do_ct_prior
        # may instead index to 0 or ...
        a_partial               = partial( self.set_value, a_value = "" )
        self.set_clear          = a_partial
        self.set_default        = a_partial
        if self.is_keep_prior_enabled:
            self.set_prior      = self.set_pass
        else:
            self.set_prior      = a_partial


        self.db_value       = None
            # value from the db, used in debugging

        # these should be the only functions we need
        self.rec_to_edit    = self.rec_to_dict_edit
        self.edit_to_rec    = self.dict_edit_to_rec

        #self.mdi_manager    = None
            # needs to be set, necessary but coupling loose
        self.widget_ext      = None  # set it or forget it it will not work

    #----------------------------
    def rec_to_dict_edit( self, record, format = None ):
        """
        convert from record format to edit format
        this is more or less a prototype
        note that I know my own field_name
        set_prepped_data
        """
        self.debug_format   = format   # unhide the closure

        raw_data            = get_rec_data( record, self.field_name )
        converted_data      = raw_data
        self.set_preped_data( converted_data )

        msg                 = f"rec_to_dict_edit set value {self.field_name =} {raw_data = }"
        logging.debug( msg )

        return converted_data

    #----------------------------
    def dict_edit_to_rec( self, record, format = None ):
        """
        convert from edit format to record format
        this is more or less a prototype
        will use field name, if record is not a record skip placing in
        record for debug
        """
        self.debug_format    = format  # should not be used for this type
        converted_data       = self.get_raw_data()

        msg         = f"dict_edit_to_rec {self.field_name = } {converted_data = }"
        logging.debug( msg )

        set_rec_data( record, self.field_name, converted_data )

        return converted_data # debug only set above

    #----------------------------
    def set_preped_data( self, a_key,   is_changed = None ):
        """
        specialize in extension
        what about prior value
            if we are fetching a value and the
            key is not present we will have a invalid
            index
        """
        # do i have the key?
        if not a_key in self.widget_ext.combo_dict:
            # fix it
            self.index_valid    = False
            self.db_value       = a_key
            value_not_used      = self.widget_ext.get_info_for_id( a_key )
                # old comments may be some truth
                    # this will update the dictionary and  call all the
                    # tabs to refresh using some function
                    # but this may need to know the ddl is invalid
                    # which set in warning
                    # update will be called later

        else:
            self.set_selection_by_key( a_key )

    #----------------------------
    def get_raw_data( self, ):
        """'
        key should be correct type
        this actually should be the data to go back to the db
        """
        #data  = self.db_value   # old for debug may block update
        data  = self.get_key_by_index()
        #data  = self.get_selected_key()   # eliminate call after testing
        return data

    #---------------------------
    def update_dictionary( self, just_warning = True ):
        """
        2 events, a warning to save the id and
        then telling the dict has change --
        but the index may not be valid -- as for
        a new record in the fetch process  -- how do we detect that
        """
        if just_warning:
            self.db_value       = self.get_value_by_index()   # probably same as  get_raw_data()
            self.index_valid    = False
        else:
            self.load_combo_box()
            self.index_valid    = True
            self.set_selection_by_key( self.db_value )

    # --------------------------
    def load_combo_box( self ):
        """
        assumes dict is in place
            builds the index and loads the drop down
        """
        debug_msg  =  ( "load_combo_box get the value, save in temp, reset the combo and reset")
        logging.log( LOG_LEVEL,  debug_msg, )
        debug_msg  = ( "load_combo_box not necessary if we always add at the end ????")
        logging.log( LOG_LEVEL,  debug_msg, )
        self.index_to_key    = {}
        self.clear()
        for index, (key, value) in enumerate( self.widget_ext.combo_dict.items() ):
            self.addItem(str(value))
            self.index_to_key[index] = key
        pass # debug

    # --------------------------
    def get_value_by_index(self):
        """
        but if index is invalid get our backup copy
        """
        if self.index_valid:
            index   = self.currentIndex()
            key     = self.index_to_key.get(index)
            value   = self.widget_ext.combo_dict.get(key)

        else:
            value   = self.db_value

        return value

    # --------------------------
    def get_key_by_index(self):
        """
        that is by the current index
        """
        index     = self.currentIndex()
        key       = self.index_to_key.get(index)
        #value = self.dict_data.get(key)
        debug_msg   = (f"get_key_by_index Selected key: {key}")
        logging.log( LOG_LEVEL,  debug_msg, )
        return key

    # --------------------------
    def set_selection_by_key(self, key):
        """ """

        for index, stored_key in self.index_to_key.items():
            if stored_key == key:
                self.setCurrentIndex(index)
                # self.label.setText(f"Selection Set to: {self.dict_data[key]}")

    # --------------------------
    def setPlaceholderText( self, ignoered ):
        """so we can call without harm """
        pass

# -------------------------------
class CQTextEdit( QTextEdit,  CQEditBase, TextEditExtMixin,   ):
    """
    Custom QTextEdit subclass with CQEditBase integration

    truble with ctrl-f change order form below
    CQTextEdit(QTextEdit, CQEditBase, TextEditExtMixin ):
        to
            (QTextEdit, TextEditExtMixin, CQEditBase,   ):
                does it work better
                could change init order or not
            did not help

    """
    def __init__(self,
                 parent                 = None,
                 field_name             = None,
                 is_keep_prior_enabled  = False):
        """
        Initialization for CQTextEdit
        """
        #rint("begin init CQTextEdit")

        # Initialize QTextEdit properly
        QTextEdit.__init__( self, parent )  # Call QTextEdit constructor with parent

        # Initialize CQEditBase properly
        CQEditBase.__init__( self, parent,
                            field_name,
                            is_keep_prior_enabled  = is_keep_prior_enabled )

        TextEditExtMixin.__init__( self, )

        # ---- set functions

        # think about how to get to parametes with minimun coupling
        # monkey patch into module on first import
        note_default_text  = AppGlobal.parameters.note_default_text

        a_partial               = partial( self.set_value, note_default_text )
        self.set_clear          = a_partial
        self.set_default        = a_partial

        # special is_prior_text_enabled tor text '

        self.is_prior_text_enabled   = False
            #
        self.prior_text      = ""

        if self.is_keep_prior_enabled:
            self.set_prior      = self.set_pass
        else:
            self.set_prior      = a_partial

        self.null_surogate  = ""
        self.tab_width      = 4                         # also for interface

        # ---- in out conversion
        # in out conversion
        self.rec_to_edit_cnv    = self.cnv_str_to_str
        self.edit_to_rec_cnv    = self.cnv_str_to_str

        self.dict_to_edit_cnv   = self.cnv_str_to_str
        self.edit_to_dict_cnv   = self.cnv_str_to_str

        self.cnv_str_to_str_strip   = self.cnv_str_to_str_strip_eol

        self.text_edit_ext_obj  = None # may be set externally

        # self.do_paste_cache     = True # !! change to fallse and
            # make gui turn on -- used in data maager

        # Connect the textEdited signal to on_data_changed method -- not here for line edit
        #self.textChanged.connect( self.on_data_changed )  # no argument sent
        #self.textEdited.connect(self.on_text_changed )  # no data sent
        # cursor        = self.textCursor()
        # debug_cursor  = self.textCursor()

        # self.set_custom_context_menu()

    def keyPressEvent_delete_me (self, event):
        """
        capture all the key presses
        """
        breakpoint()


    #----------------------------
    def set_preped_data( self, a_string, is_changed = None ):
        """ specialize for this edit
        might have second argument for is changed
        add to rest of group
        """
        # next !! debug
        if a_string == None:
            a_string   = self.null_surogate
            msg        = f"text edit using null_surrogate for {self.field_name}"
            logging.debug( msg )

        elif not isinstance( a_string, str ):
            debug    = self.field_name
            msg      = f"set_prepped_data error a_string, not a string {self.field_name = }"
            wat_inspector.go( self, globals( ), msg = msg )

        self.setText( a_string  )
        self.prior_value  = a_string
        if is_changed is not None:
            self.is_changed = is_changed

    #----------------------------
    def get_raw_data( self, ):
        """'
        final step from set_data should always be a string for
        this edit type
        """
        data  = self.toPlainText()
        return data

    #-----------------------------
    def get_data_for_record_debug( self, record, record_state ):
        """a debug trick to try other than that consider an if  """
        msg    = ( "get_data_for_record_debug this for debug only ")
        logging.debug( msg )
        CQEditBase.get_data_for_record( self, record, record_state )

    #-----------------------------
    def cache_current_text( self ):
        """
        save contents of the text in one level deep buffer
        probably trigger before select or add
        this code would go
            maybe move to the QCText... or pull paste_up from there
        """
        text_edit   = self
        cursor      = text_edit.textCursor()  # Save the current cursor position

        self.prior_text     = text_edit.toPlainText()  # Get all text as a string

        text_edit.setTextCursor(cursor)

    #-----------------------------
    def paste_cache_text( self ):
        """
        save contents of the text in one level deep buffer
        """
        pass   # some confusion with added mixin _cache may have been bad choice here
        #self.insert_text_at_cursor( self.prior_text )
        self.insert_text_at_cursor( self.prior_text )
        pass # debug

    def keyPressEvent_for_tab(self, event):   # automatically called? no setup

        """ what wyh is this, --- a tab inser perhaps """
        if event.key() == 0x01000001:  # Qt.Key_Tab
            cursor = self.textCursor()
            cursor.insertText( ' ' * self.tab_width )
        else:
            super().keyPressEvent(event)


    # ------------------------------------
    def on_text_changed( self,   ):
        """
        may be edited or messed with
        no data sent by QTextEdit object.
        """
        #self.is_changed  = True
        self.on_data_changed( )
        self.prior_value   = self.toPlainText()
        msg        = (f"CQTextEdit text edit on_text_changed ")
        logging.debug( msg )

    # ------------------------------------
    def insertFromMimeData(self, source):
        """from a ChatBot is it ok?? """
        self.insertPlainText(source.text())  #  removes formatting

    # ------------------------------------
    def scroll_to_top(self, ):
        """

        """
        # cursor = self.textCursor()
        # cursor.movePosition(cursor.Start)
        # self.setTextCursor(cursor)
        # self.ensureCursorVisible()

        # ----------------- new grok
        self.moveCursor( MoveOperation.Start )
        self.ensureCursorVisible()   # or just text_edit.verticalScrollBar().setValue(0)

    # ------------------------------------
    def scroll_to_bottom(self, ):
        """

        """
        #text_edit    = self

        # cursor = self.textCursor()
        # cursor.movePosition(cursor.End)
        # self.setTextCursor(cursor)
        # self.ensureCursorVisible()

        # ----------------- new grok
        self.moveCursor( MoveOperation.End )  # qt_compat
        self.ensureCursorVisible()          # this does the scroll

    # --------------------------------------------------
    def __str__( self ):

        a_str   = ""
        a_str   = ">>>>>>>>>>* QTextEdit *<<<<<<<<<<<<"
        # a_str   = string_util.to_columns( a_str, ["default_type",
        #                                    f"{self.default_type}" ] )
        # a_str   = string_util.to_columns( a_str, ["default_value",
        #                                    f"{self.default_value}" ] )
        # a_str   = string_util.to_columns( a_str, ["is_changed",
        #                                    f"{self.is_changed}" ] )
        # a_str   = string_util.to_columns( a_str, ["prior_value",
        #                                    f"{self.prior_value}" ] )
        more    = CQEditBase.__str__( self, )
        a_str   = f"{a_str}\n{more}"
        return a_str

# ---------------------------------
class CQDateEdit( QDateEdit,  CQEditBase ):
# class CQDateEdit( CQEditBase, QDateEdit,   ):  # reverse does not help
    """
    move a version to stuffdb
    custom_widget.pb   as CQDateEdit
    custom_widgets.CQDateEdit()

    often timestamp to qdate

    """
    def __init__(self,
                 parent                 = None,
                 field_name             = None,
                 is_keep_prior_enabled  = False):
        """
        read it
        timestammp is an int
        in   -- into the widget
        out  -- out to the record
        """
        #super(   ).__init__(   )
        QDateEdit.__init__( self, parent  )     # mimic LineEdit try parent int there parent of None
        CQEditBase.__init__( self,
                        parent                  = parent,
                        field_name              = field_name,
                        is_keep_prior_enabled   = False)

        # ---- set functions
        # a_partial           = partial( self.do_ct_value, "do_ct_value!!" )
        # self.ct_default     = a_partial
        today                   = QDate.currentDate()
        a_partial               = partial( self.set_value, today ) # invalid date
        #self.ct_default     = a_partial

        self.set_clear          = a_partial
        self.set_default        = a_partial

        if self.is_keep_prior_enabled:
            self.set_prior      = self.set_pass

        else:
            self.set_prior      = a_partial

        # ---- in out conversion
        self.rec_to_edit_cnv    = self.cnv_int_to_qdate
        self.edit_to_rec_cnv    = self.cnv_qdate_to_int

        self.dict_to_edit_cnv   = self.cnv_int_to_qdate
        self.edit_to_dict_cnv   = self.cnv_qdate_to_int


        #self.default_type          = "today"   # need begin of day, end of day ??
        #self.default_value         = None     # if used make a qdate
        self.config_calender_popup( True )
        # prior value, prior_type
        self.is_editable            = True  #  --- by the user   may be built in
                                        # will nee a configure for it

        self.setDisplayFormat( QT_DATE_FORMAT )

    # --------------------------
    def setPlaceholderText( self, ignoered ):
        """
        so we can call without harm
        """
        pass


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


        if qt_version == 6:  # 5 6 compat
            context_menu.exec(event.globalPos())
        else:
            context_menu.exec_(event.globalPos())


    #----------------------------
    def set_data_today(self):
        """
        needs rename
        we need in in or out datatype
        """
        qdate       = QDate.currentDate()
        self.set_data( qdate, "qdate" )

    #----------------------------
    def get_raw_data( self, ):
        """
        final step from set_data should always be qdate
        """
        qdate   = self.date()

        # need or not ??  right or not
        # if  qdate.date().isValid():
        #     pass
        #     #print("The date is invalid (NULL equivalent).")
        # else:
        #     qdate  = None   # cannot pass on invalid date
        #     print("The date is valid:", date_edit.date().toString())

        return qdate

    #----------------------------
    def set_preped_data( self, qdate, is_changed = True  ):
        """'
        final step from set_data should always be qdate
        specialized by name of function call
        """
        # if qdate == None:
        #     qdate   = self.null_surrogate
        #     msg        = f"date edit using null_surrogate for {self.field_name}"
        #     logging.debug( msg )

        # elif not isinstance( qdate,  QDate ):
        #     self_field_name   = self.field_name
        #     msg = f"set_prepped_data error qdate, not a QDate {self.field_name = }  return ??for now inspect then break"
        #     logging.error( msg )
        #     return
        #     wat_inspector.go(
        #         msg            = msg,
        #         # inspect_me     = self.people_model,
        #         a_locals       = locals(),
        #         a_globals      = globals(), )
        #     breakpoint()


        # self.setDate( qdate  )  # was going to validate next seems to fix
        #super( QDateEdit, self).setDate( qdate )  # Ensure QDateEdit.setDate() is called
            # above still going to to self.validate sometimes
        # xxx= """
        # i am in a control that inherits from QDateEdit as well as others.
        # i want to call the method setDate in the control, but it seems to
        # be going thew wrong place.  any fixes for this?
        # here is another try at it
        # """
        QDateEdit.setDate( self, qdate )

        # # std way
        # pass
        # self.setDate( qdate )
        # pass

    #----------------------------
    def rec_to_edit_ts_qdate( self, record, format = None ):
        """
        timestamp is converted to qdate
        this seems to be the default
        """
        # self.debug_format   = format   # unhide the closure
        # converted_data      = None
        # msg                 = f"rec_to_edit This function is not implemented yet. \n {str( self ) = }"
        # logging.error( msg )
        # raise NotImplementedError( msg )

        field_name          = self.field_name
        raw_data            = get_rec_data( record, field_name  )

        if ( raw_data is None ) or ( raw_data == "" ):  # null may come as empty string
            # qdate       = QDate( 1900, 1, 1 ) # surrogate for None
            # msg         = ( f"rec_to_edit_ts_qdate Field {field_name} "
            #                 f"got data of None used ....  maybe")
            # logging.error( msg )
            # or
            #raise ValueError( msg )
            #qdate         = None   # manage the null in set prepped
            qdate         = QDate()   # says chat invalid

        else:
            #timestamp = 1710432000  # Example Unix timestamp in seconds

            qdate         = QDateTime.fromSecsSinceEpoch( int( raw_data ) ).date()

        self.set_preped_data( qdate )
        return qdate

    #----------------------------
    def edit_to_rec_qdate_ts( self, record, format = None ):
        """
        qdate is converted to a timestamp
        """
        raw_data            = self.get_raw_data()

        if not raw_data.isValid():
            raw_data     = None

        if raw_data is None:
            a_timestamp  = None

        else:
            noon_time   = QTime(12, 0, 0)
            # Create QDateTime with the specified date and time
            qdatetime   = QDateTime( raw_data, noon_time )
            # Get the Unix timestamp in seconds
            a_timestamp = qdatetime.toSecsSinceEpoch()

        set_rec_data( record, self.field_name, a_timestamp )

        return a_timestamp  # just debug or what

    #----------------------------
    def edit_to_rec_now( self, record, format = None ):
        """
        always return the current time !! are we used?
        """
        a_timestamp         = time.time( )  # zz
        set_rec_data( record, self.field_name, a_timestamp )
        return a_timestamp  # just debug or what

    # -------------------------------
    def __str__( self ):

        a_str   = ""

        a_str   = f"{a_str}{CQEditBase.__str__( self, )    }"

        a_str   = f"{a_str}\n>>>>>>>>>>* CQDateEdit ( nothing so far ) *<<<<<<<<<<<<"

        a_str   = string_util.to_columns( a_str, ["getDate",
                                            f"{str(self.date() )}" ] )
        # # a_str   = string_util.to_columns( a_str, ["default_value",
        # #                                    f"{self.default_value}" ] )
        # a_str   = string_util.to_columns( a_str, ["is_changed",
        #                                    f"{self.is_changed}" ] )


        # more    = CQEditBase.__str__( self, )
        # a_str   = f"{a_str}\n{more}"
        return a_str

# ---- eof ----------------------------
