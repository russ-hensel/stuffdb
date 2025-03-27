#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
custom versions oa QWidgets

see  qt_by_example for these widgets -- run this deom_custom_widgets.py

coupling
    to logging


"""
# ---- tof change next depending on project

# --------------------
if __name__ == "__main__":
    import main
    main.main()
# --------------------


# # --------------------
# if __name__ == "__main__":
#     #----- run the full app
#     import main_qt

#     #main.main()



# --------------------
# ---- imports
import functools
import logging
import pdb
import traceback
#import subprocess
#from   subprocess import run
#from   subprocess import Popen, PIPE, STDOUT
#import datetime
from datetime import datetime
from functools import partial


import string_util
import wat_inspector
from app_global import AppGlobal
from PyQt5 import QtGui
# ---- Qt
from PyQt5.QtCore import QDate, QDateTime, QTime



from PyQt5.QtCore import (QAbstractTableModel,
                          QDate,
                          QDateTime,
                          QModelIndex,
                          QRectF,
                          Qt,
                          QTimer,
                          pyqtSlot)
from PyQt5.QtGui import (QCursor,
                         QIntValidator,
                         QPainter,
                         QPixmap,
                         QStandardItem,
                         QStandardItemModel,
                         QTextCursor)
from PyQt5.QtSql import (QSqlDatabase,
                         QSqlQuery,
                         QSqlQueryModel,
                         QSqlRecord,
                         QSqlRelation,
                         QSqlRelationalDelegate,
                         QSqlRelationalTableModel,
                         QSqlTableModel)
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
# ---- imports local
#import convert_db_display
import mdi_management


LOG_LEVEL   = 20    # higher is more

logger      = logging.getLogger( )


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
def validate_no_z( a_string   ):
    """
    a debug thing
    what type need models be? -- think should throw except
    """
    msg      = None
    if "z" in a_string:
        msg   = "validate_no_z no zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
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

    def data(self, index, role=Qt.DisplayRole):
        """ !! FIX RETURN """
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
class CQComboBoxEditCriteria2xxx( QComboBox ):
    """
    make this like a line edit with a memory
    based on what chat suggested
    lots of junk from old edit criteria
        try to clean up
    read it
    custom_widgets.CQLineEditCriteria( get_type = "string", set_type = "string")

    custom_widgets.CQLineEditCriteria( get_type = "string", set_type = "string")
    custom_widgets.CQComboBoxEditCriteria2( )

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
        max_items    = 10
        self.setEditable( True )  # Allow user input
        self.max_items = max_items  # Set max item limit

        # Connect signals
        self.editTextChanged.connect(self.handle_edit_text)
        self.activated.connect(self.add_current_text)
        self.focusOutEvent = self.create_focus_out_event()

        # if not data_field_name:
        #     1/0
        # self.data_field_name       = data_field_name

        print( "CQComboBoxEditCriteria2 next look like junk ")
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
        """
        mutate the dict for criteria
        think this is how we build criteria for criteria select
        """
        msg   = ( f"CQComboBoxEditCriteria {self.get_data()}")
        logging.debug( msg )

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

            logging.error( msg )
            raise ValueError( msg, )

    def handle_edit_text(self, text):
        """Handles when user types into the box"""
        self.current_text = text

    def add_current_text(self):
        """Adds the current text to the list with max_items limit"""
        text = self.currentText().strip()
        if text and text not in [self.itemText(i) for i in range(self.count())]:  # Avoid duplicates
            self.addItem(text)

            # Keep only the last 'max_items' items
            if self.count() > self.max_items:
                self.removeItem(0)  # Remove the oldest entry

    #---------------------------
    def keyPressEvent(self, event):
        """Capture Enter key to add item"""
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.add_current_text()
        super().keyPressEvent(event)

    #----------------------
    def create_focus_out_event(self):
        """Handles when focus leaves the widget"""
        def focus_out_event(event):
            self.add_current_text()
            super(CQComboBoxEditCriteria2, self).focusOutEvent(event)
        return focus_out_event


#-------------------------------
class CQComboBoxEditCriteriaxxx( QComboBox ):
    """
    read it
    custom_widgets.CQLineEditCriteria( get_type = "string", set_type = "string")
    custom_widgets.CQComboBoxEditCriteria( )

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
        """
        mutate the dict for criteria
        think this is how we build criteria for criteria select
        """
        msg   = ( f"CQComboBoxEditCriteria {self.get_data()}")
        logging.debug( msg )

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

            logging.error( msg )
            raise ValueError( msg, )

#-------------------------------
class CQLineEditCriteriaxxx( QLineEdit ):
    """
    read it
    custom_widgets.CQLineEditCriteria( get_type = "string", set_type = "string")
    """
    def __init__(self,
                 parent         = None,
                 #data_field_name    = None,
                 get_type       = "string",
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
        self.default_type          = "value"    # value will be a string
        self.default_value         = ""
        self.functon_on_return     = None
        self.returnPressed.connect( self.on_return_pressed )

    #-----------------------------
    def on_return_pressed( self ):
        """
        read it

        """
        if self.functon_on_return is not None:
            self.functon_on_return( )   # consider passing the edit

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
        """mutate the dict for criteria  """
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
            logging.error( msg )

            raise ValueError( msg, )

# --------------------------------
class CQDateCriteria_keep_for_a_bit( QWidget,  ):
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

        self.get_type          = get_type    # type coming out from qdate
        self.set_type          = set_type    # type coming in to set qdate
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
            msg     = ( "CQDateCriteria set_date still need self.setsomething" )
            logging.error( msg )
            return

        try:
            qdate = convert_db_display.date_criteria_from_to( date, set_type, "qdate" )

        except Exception as an_except:
            msg     = f"a_except         >>{an_except}<<  type  >>{type( an_except)}<<"
            logging.error( msg )

            msg     = f"an_except.args   >>{an_except.args}<<  {self.field_name = } "
            logging.error( msg )

            s_trace = traceback.format_exc()
            msg     = f"format-exc       >>{s_trace}<<"
            logging.error( msg )

            raise

        self.setDate( qdate )

        self.ignore_cb_widget.setChecked( False )
        msg      = ( "CQDateCriteria set_date still need self.setsomething" )
        logging.debug( msg )

    # ----------------------------
    def get_date( self, get_type = None   ):
        """
        return None if ignore is checked else the proper conversion
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
            logging.error( msg )

            msg     = f"an_except.args   >>{an_except.args}<<  {self.field_name = } "
            logging.error( msg )

            s_trace = traceback.format_exc()
            msg     = f"format-exc       >>{s_trace}<<"
            logging.error( msg )

            raise

        return data

    #--------------------------------
    def build_criteria( self, a_dict ):
        """mutate the dict for criteria  """
        msg    = ( "CQDateCriteria build_criteria dates not yet right " )
        logging.debug( msg )

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
        probably not right set to date None
        """
        self.clear()  # Clears the QDateEdit

    def set_data_default( self ):
        """
        data not date to agree with other criteria widgets
        """
        msg     = ( "date_criteria  set_data_default need more")
        logging.debug( msg )
        #self.set_date( None )
        self.ignore_cb_widget.setChecked( True )

    def set_date_today(self):
        """
        no conversion necessary as all qdate
        """
        self.date_edit_widget.setDate(QDate.currentDate())  # Sets date to today

# ---- Edits not Criteria ------------------------------------
# ---------------------------------
class CQEditBase(   ):
    """
    second parent for QT edit child controls

    do we need both?  what is the difference
    set_to_default
    clear_data

    do not need prior value it is just sitting in the control


    --- default, prior
            reset
            change_to
            * ct_default   ct_prior
            clear
            new
    ---
            set
            set_data
            set_to
            make
            * do_ct    do_ct_value   do_ct_today   do_ct_prior
            do_data_to_

    get rid of is_changed
                prior_data
                events for above

    """
    def __init__(self,
                 parent             = None,
                 field_name         = None,
                 display_type       = "qdate",
                 db_type            = "timestamp",
                 is_keep_prior_enabled = False):
        """
        read it
        timestamp is an int
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
            # for this control I think display type must always be qdate
            # for edit I think must always be string
        #self.is_constant           = False

        self.is_keep_prior_enabled  = is_keep_prior_enabled

        self.null_surogate          = None   # find a value to use as null surrogate

        # ---- these are private change to _
        # prior value, prior_type -- likely already in edit
        self.prior_value            = None     # value last set from a record ot to record
                                                # set to something valid for edit in its init
            # in db_type
        self.is_field_valid         = self.validate_all_ok

        self.debug_format           = "not_set"

        # looks like a bad idea, when is reset
        self.is_changed             = False    # by user or default -- is this !! useful or a problem

        # next probably in closure for the function
        self.default_valuexxx          = "value_of_self_default_value"  # may or may not be used
        self.clear_valuexxx        = "value_of_self_clear_value"    # may or may not be used
        self.default_typexxx           = None
        # Set an initial date (optional)
        #self.setDate( QDate.currentDate() )

        # next should be done in descendant
        # self.default_type          = "today"   # need begin of day, end of day ??
        # self.default_value         = None     # if used make a qdate

        # print( "        end init CQEditBase")
        # next is to deal with issues of bad inheritance for the date Edit
        self.bad_calls              = 0
        # self.extra_dict             = None
            # for the CQDictComboBox  if needed

        # or just let be a direct call !! --- will not work for all types
        #self.returnPressed.connect( self.on_return_pressed )

        if self.ct_prior is None:
            msg     = f"__init__ Error {self.ct_default = } { self.ct_prior = }"
            logging.error( msg )

        # msg     = f"__init__ {self.ct_default = } { self.ct_prior = }"
        # logging.debug( msg )

    #----------------------------
    def rec_to_edit( self, record, format = None ):
        """
        convert from record format to edit format
        this is more or less a prototype
        note that I know my own field_name
        """
        self.debug_format   = format   # unhide the closure
        converted_data      = None
        msg                 = f"rec_to_edit This function is not implemented yet. \n {str( self ) = }"
        logging.error( msg )
        raise NotImplementedError( msg )

        return converted_data

    #----------------------------
    def edit_to_rec( self, record, format = None ):
        """
        convert from edit format to record format
        this is more or less a prototype
        will use field name, if record is not a record skip placing in
        record for debug
        """
        self.debug_format    = format
        converted_data       = None
        msg         = f"edit_to_rec This function is not implemented yet. \n {str( self ) = }"
        logging.error( msg )
        raise NotImplementedError( msg )

        return converted_data

    #--------------------------------
    def build_criteria( self, a_dict ):
        """
        mutate the dict for criteria
        think this is how we build criteria for criteria select
        """
        msg   = ( f"CQEditBase {self.field_name} {self.get_raw_data()}")
        logging.debug( msg )

        a_dict[ self.field_name ] = self.get_raw_data()

    #----------------------------
    def set_preped_data( self, data, is_changed = None ):
        """'
        final step from set_data should always be qdate for a date edit....
        is it generally overridden?\
        no think should be ok here too
        """
        msg         = f"get_raw_data This function is not implemented yet. \n {str( self ) = }"
        logging.error( msg )

        raise NotImplementedError( msg )

    #----------------------------
    def set_data( self, data, is_changed = None ):
        """ """
        self.set_preped_data( data, is_changed = is_changed )

    #-----------------------------
    def on_return_pressed( self ):
        """
        read it
        widget.function_on_return   = function_to_do_something
        if function does not have return_pressed functionality you can set to anything
        makes the api uniform
        """
        if self.function_on_return is not None:
            self.function_on_return( )   # consider passing the edit

    #----------------------------
    def function_on_return( self ):
        """
        Replacable function should be replaced  unless default this pass
        some functions do not have the event so leave alone or set to anything
        it will never be called
        """
        pass

    #-----------------------------
    def on_value_changed( self ):
        """
        read it
        different widgets have different events for this
        they will be dircted here for a uniform interface
        useful in particular by criteris

        makes the api uniform


        """
        if self.function_on_return is not None:
            self.function_on_changed( )   # consider passing the edit

    #----------------------------
    def function_on_changed( self ):
        """
        Replacable function should be replaced  unless default this pass
        some functions do not have the event so leave alone or set to anything
        it will never be called

        widget.function_on_changed   = something_to_do_function
        """
        pass




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

    # -----------------------
    def ct_default( self   ):
        """
        should be replaced
        set_data_to_prior_value( self   )
        but could be clear or default or pass
        often replaced with

            a_partial           = partial( self.do_ct_value, "" )


        really want three variations, clear, clear_default ( if a default value ) clear_or_prior, clear_or_default clear  all from clear_or
        """
        msg         = f"ct_default  is not implemented yet. \n self = {self}"
        logging.error( msg )
        raise NotImplementedError( msg )

    # -----------------------
    def ct_prior( self   ):
        """
        should be replaced  ... set_data_to_prior_value( self   )
        but could be clear or default or pass
        might be replaced with
            a_partial           = partial( self.do_ct_value, "" )

        """
        msg         = f"ct_prior  is not implemented yet. \n self = {self}"
        logging.error( msg )
        raise NotImplementedError( msg )

        return
        # now moved to do
        msg         = f"ct_prior in test {self.is_keep_prior_enabled = }"
        logging.debug( msg )

        if self.is_keep_prior_enabled:
            pass # leave the value there
        else:
            self.ct_default()

    # -----------------------
    def do_ct_prior( self,  ):
        """
        complete this code:
            set_data_to_default    = partial( set_data_to_default, "" )
        function to set the default to a value
        should be correct type without  conversion

        """
        #self.on_data_changed()
        if self.is_keep_prior_enabled:
            pass # leave the value there
        else:
            self.ct_default()

    # -----------------------
    def do_ct_value( self, a_value  ):
        """
        complete this code:
            set_data_to_default    = partial( set_data_to_default, "" )
        function to set the default to a value
        should be correct type without  conversion
        look for
             a_partial           = partial( self.do_ct_value, "" )

        """
        #rint( "set_data_to_default_value {a_value = }" )
        self.set_preped_data( a_value, is_changed = True )
        print( f"do_ct_value {self.field_name}")

        pass # debug


    #-----------------------------
    def is_field_valid( self ):   # seems to help keep and test
        """
        change validate to is_field_valid
        need to return a message could be thru and exception or just
        a return value for now None or "" means ok else
        contain an error message
        this needs work for now just checking it it called
        !! look in descendant
        plug in this function
        """
        msg         = f"is_field_valid not implemented yet. \n self = {self }"
        logging.error( msg )
        raise NotImplementedError( msg )
        return

    # ---- validate implementations -----------------------
    #-----------------------------
    def validate_all_ok( self, arg_ng_1 =  "arg_ng_1",   arg_ng_2 = "arg_ng_2" ):
        """
        pretty much a no op, just do not throw an exception
        default for the base class
        getting called instead of setDate by the date edit hence a bunch of work arounds
        what should CQDateEdit.setDate( ) return It updates the displayed date but does not return anything.
            after TypeError: invalid result from CQDateEdit.validate_all_ok()
        """
        if not arg_ng_1 ==  "arg_ng_1":
            self.bad_calls              += 1
            msg  =  (    f"validate_all_ok seems to be called incorrectly "
                         f" {arg_ng_1 =} {self.bad_calls = } {self.field_name = }" )
            logging.error( msg )
            #breakpoint( )
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

    # ---- replacable functions for edit to rec and vise virsa
    #----------------------------
    def edit_to_rec_str_to_str( self, record, format = None  ):
        """
        pretty much nothing format just ignored
        self.edit_to_rec    =self.edit_to_record_str_str             # partial to set format
        if record is not record it is data
        could have special for None
        """
        # raw_data    = self.get_raw_data()
        # set_rec_data( record, raw_data )
        raw_data            = self.get_raw_data()
        converted_data      = raw_data

        # might want conditions for formatting, but for now now support
        if format is not None:
            msg         = ( f"rec_to_edit_int_to_str Field {self.field_name} "
                            f"format other than None not supported ")
            logging.error( msg )
            raise ValueError( msg )

        set_rec_data( record, self.field_name, converted_data )

        return converted_data # for debug

    #----------------------------
    def edit_to_rec_str_to_int( self, record, format = None  ):
        """
        pretty much nothing format just ignored
        self.edit_to_rec    =self.edit_to_record_str_str             # partial to set format
        if record is not record it is data
        could have special for None
        """
        raw_data            = self.get_raw_data()
        raw_data            = raw_data.rstrip( )
        if raw_data ==  "":
            msg   = ( f"!!edit_to_rec_str_to_int consider empty to Null/None {self.field_name =}")
            logging.error( msg )
            converted_data      = None # is this valid or do i need to use some special value
        else:
            converted_data      = int( raw_data )

        # might want conditions for formatting, but for now now support
        if format is not None:
            msg         = ( f"rec_to_edit_int_to_str Field {self.field_name} "
                            f"format other than None not supported ")
            logging.error( msg )
            raise ValueError( msg )

        set_rec_data( record, self.field_name, converted_data )

        return converted_data # for debug

    #---------------------------
    def edit_to_rec_qdate_to_int( self, record, format = None  ):
        """
        date is a qdate -- change name of function, int is a timestamp
        note that our timestamps are ints

        """
        qdate        = self.get_raw_data()

        # could check for qdate
        py_datetime  = datetime( qdate.year(), qdate.month(), qdate.day())
        timestamp    = int( py_datetime.timestamp() )

        if format is not None:
            msg         = ( f"rec_to_edit_int_to_str Field {self.field_name} "
                            f"format other than None not supported ")
            logging.error( msg )
            raise ValueError( msg )

        set_rec_data( record, self.field_name, timestamp )

        return timestamp

    #----------------------------
    def rec_to_edit_str_to_str( self, record, format = None ):
        """
        special case
            None   -> ""

        else:

        """
        self.debug_format   = format   # unhide the closure
        field_name          = self.field_name

        raw_data            = get_rec_data( record, field_name )
        converted_data      = raw_data

        if converted_data is None:
            converted_data      = ""

        # conditional break
        # if field_name == "text_data":
        #     pass
        #     #breakpoint( )


        # might want conditions for formatting, but for now now support
        if format is not None:
            msg         = ( f"rec_to_edit_str_to_str Field {field_name} "
                            f"format other than None not supported ")
            logging.error( msg )
            raise ValueError( msg )

         # put in record

        self.set_preped_data( converted_data   )
        return converted_data  # return for test data has been set

    #----------------------------
    def rec_to_edit_int_to_str( self, record, format = None ):
        """
        special case
            None   -> ""
        for debug or testing do test on isinstance of record

            # msg = record.value( field_name )
            data        = record.value( field_name  )
            # msg         = (  f"set_data_from_record Value for "
            #                  f"{field_name}: {data}" )
            # logger.log( logging.DEBUG, msg )
        else:

        """
        self.debug_format   = format   # unhide the closure
        field_name          = self.field_name
        # conditional break
        # if field_name == "text_data":
        #     pass
        #     #breakpoint( )

        self.debug_format   = format   # unhide the closure
        field_name          = self.field_name

        raw_data            = get_rec_data( record, field_name  ) # may raise...

        if raw_data is None:
            converted_data  = ""
        else:
            # for now assume correct type
            converted_data  = str( raw_data )

        # might want conditions for formatting, but for now now support
        if format is not None:
            msg         = ( f"rec_to_edit_int_to_str Field {field_name} "
                            f"format other than None not supported ")
            logging.error( msg )
            raise ValueError( msg )

        self.set_preped_data( converted_data  )

        return converted_data  # return for test data has been set

    #----------------------------
    def rec_to_edit_int_to_qdate( self, record, format = None ):
        """
        special case
            None   -> see code

        """
        self.debug_format   = format   # unhide the closure
        field_name          = self.field_name
        # conditional break
        # if field_name == "text_data":
        #     pass
        #     #breakpoint( )

        raw_data            = get_rec_data( record, field_name  ) # may raise...

        if raw_data is None:
            converted_data  = QDate( 1900, 1, 1 ) # surrogate for None
            msg         = ( f"rec_to_edit_int_to_qdate Field {field_name} "
                            f"got data of None used surrogate None ")

            raise ValueError( msg )

        else:
            if not isinstance( raw_data, int ):
                msg   = ( f"Data is not instance of int = timestamp {raw_data = } {type(raw_data) = }  " )
                logging.error( msg )
                raise ValueError( msg )

            a_datetime          = datetime.fromtimestamp( raw_data )

            converted_data      = QDate( a_datetime.year, a_datetime.month, a_datetime.day )

        # might want conditions for formatting, but for now now support
        if format is not None:
            msg         = ( f"rec_to_edit_int_to_qdate Field {field_name} "
                            f"format other than None not supported ")
            logging.error( msg )
            raise ValueError( msg )

        self.set_preped_data( converted_data  )

        return converted_data  # return for test data has been set

    #----------------------------
    def rec_to_dict_cb( self, record, format = None ):
        """
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
    # ------------------------------------
    def print_str( self,   ):
        """
        for debug
        """
        print( self )
        #logging.debug( msg )

    def __str__( self ):
        a_str   = ""
        a_str   = ">>>>>>>>>>* CQEditBase *<<<<<<<<<<<<"

        # a_str   = string_util.to_columns( a_str, ["clear_value",
        #                                    f"{self.clear_value}" ] )
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

        self.default_type          = "string"          # deprecate
        #self.default_value         = "default-value"     # deprecate
        self.prior_value           = ""  # something of a valid type
        #self.textEdited.connect(self.on_text_changed )  #  text is sent new_text
        #self.textChanged.connect(self.on_text_changed)
        #-----------------------------
        self.null_surogate          = ""
        # ---- set functions
        #a_partial           = partial( self.do_ct_value, "do_ct_value!!" )
        a_partial           = partial( self.do_ct_value, "" )
        self.ct_default     = a_partial

        self.ct_prior       = self.do_ct_prior
        self.validate       = self.validate_all_ok

        # in out conversion
        self.rec_to_edit    =  self.rec_to_edit_str_to_str
        self.edit_to_rec    =  self.edit_to_rec_str_to_str

        self.returnPressed.connect( self.on_return_pressed )

        self.textChanged.connect( self.on_value_changed  )

            # call in all edits where it applies
        self.setPlaceholderText( self.field_name )
        self._build_context_menu()

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
            msg = f"set_preped_data error a_string, not a string {self.field_name = }  return for now inspect then break"
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

    # ---- crud cycle -------------------------------
    # -----------------------
    def set_data_to_clear( self   ):
        """
        often replaced with ... set_data_to_....
        but could be clear or default or pass
        """
        self.set_preped_data( "", is_changed = True )
        pass # debug

    # ------------------------------------
    def on_text_changedxxxxx( self, new_data ):
        """
        !! probably phase out
        may be edited or messed with
        on data change for each drop the new data
        this is probably a bit messed up but also not needed??
        """
        #self.is_changed  = True
        self.on_data_changed( )
        self.prior_value   = new_data
        #rint(f"line edit on_data_changed: {new_data} saved to prior_value ")  !!

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

#-------------------------------
class CQComboBox( QComboBox, CQEditBase ):
    """
    read it
    custom_widgets.CQComboBoxEdit
        from the line edit
        lets see what we can get rid of
        start with non editable
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
                        parent             = None,
                        field_name         = field_name,
                        display_type       = None,
                        db_type            = None )

        self.default_typexxx          = "string"          # deprecate
        #self.default_value         = "default-value"     # deprecate
        self.prior_value           = ""  # something of a valid type
        #self.textEdited.connect(self.on_text_changed )  #  text is sent new_text
        #self.textChanged.connect(self.on_text_changed)
            #-----------------------------
        self.null_surogatexxx          = ""
        # ---- set functions
        #a_partial           = partial( self.do_ct_value, "do_ct_value!!" )
        a_partial           = partial( self.do_ct_value, "" )
        self.ct_default     = a_partial

        self.ct_prior       = self.do_ct_prior
        self.validate       = self.validate_all_ok

        # in out conversion
        self.rec_to_edit    =  self.rec_to_edit_str_to_str
        self.edit_to_rec    =  self.edit_to_rec_str_to_str

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
            msg = f"set_preped_data error a_string, not a string {self.field_name = }  return for now inspect then break"
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


#-------------------------------
class CQDictComboBox(QComboBox, CQEditBase ):
    """
    starting code from chat
    may need to run a select for values not in dd

    """
    def __init__(self,
                 parent             = None,
                 field_name         = None,
                 display_type       = "string",
                 db_type            = "string" ):
        """ """

        # init both parents
        QLineEdit.__init__( self, None  )     # need arg ?

        CQEditBase.__init__( self,
                        parent             = parent,
                        field_name         = field_name,
                        display_type       = display_type,
                        db_type            = db_type )

        print( "say give each its own copy of index_to_key ... but could centralized ")

        self.index_valid     = False   # false while in process of building
        self.index_to_key    = {}   # needs to be shared with one in mdi
                                    # anyway some issues

        # self.dict_data       = {}   # pointer to one in mdi

        # others do this it might work for us with None
        a_partial           = partial( self.do_ct_value, None )
        self.ct_default     = a_partial
        self.ct_prior       = self.do_ct_prior

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
        set_preped_data
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
            # fic it
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
            self.db_value       = self.get_value_by_index()   # probably same sa  get_raw_data()
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
        print( "get the value, save in temp, reset the combo and reset")
        print( "not necessary if we always add at the end ????")
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

        # self.label.setText("Key not found")


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

        # ---- set functions
        a_partial           = partial( self.do_ct_value, "\n\nnew default text" )
        self.ct_default     = a_partial                  # interface, clear text default --- set for python code
        self.ct_prior       = self.do_ct_prior
        self.validate       = self.validate_all_ok      # interface, a function for validation
        self.null_surogate  = ""
        self.tab_width      = 4                         # also for interface

        # in out conversion
        self.rec_to_edit      =  self.rec_to_edit_str_to_str
        self.edit_to_rec      =  self.edit_to_rec_str_to_str

        self.text_edit_ext_obj  = None # may be set externally

        # Connect the textEdited signal to on_data_changed method -- not here for line edit
        #self.textChanged.connect( self.on_data_changed )  # no argument sent
        #self.textEdited.connect(self.on_text_changed )  # no data sent
        # cursor        = self.textCursor()
        # debug_cursor  = self.textCursor()

    # def on_data_changedxxxxx(self):
    #     print("Text has been changed should is_changed be set ")

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
            msg      = f"set_preped_data error a_string, not a string {self.field_name = }"
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


    def keyPressEvent(self, event):   # automatically called? no setup
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
        """from a chatbot is it ok?? """
        self.insertPlainText(source.text())  #  removes formatting


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
                 parent             = None,
                 field_name         = None,
                 display_type       = None,
                 db_type            = None ):
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

        # ---- set functions
        # a_partial           = partial( self.do_ct_value, "do_ct_value!!" )
        # self.ct_default     = a_partial

        a_partial           = partial( self.do_ct_value, QDate() ) # invalid date
        #self.ct_default     = a_partial


        # probably wrong but hope do not blow
        self.ct_default     = a_partial
        self.ct_prior       = a_partial

        self.rec_to_edit    =  self.rec_to_edit_ts_qdate
        self.edit_to_rec    =  self.edit_to_rec_qdate_ts

        #self.is_valid       = self.validate_all_ok
        #self.null_surogate  = QDate( 1980, 1, 1 )

        #self.default_type          = "today"   # need begin of day, end of day ??
        #self.default_value         = None     # if used make a qdate
        self.config_calender_popup( True )
        # prior value, prior_type
        self.is_editable            = True  #  --- by the user   may be built in
                                        # will nee a configure for it

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
        #     qdate   = self.null_surogate
        #     msg        = f"date edit using null_surrogate for {self.field_name}"
        #     logging.debug( msg )

        # elif not isinstance( qdate,  QDate ):
        #     self_field_name   = self.field_name
        #     msg = f"set_preped_data error qdate, not a QDate {self.field_name = }  return ??for now inspect then break"
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
            #qdate         = None   # manage the null in set preped
            qdate         = QDate()   # says chat

        else:

        #timestamp = 1710432000  # Example Unix timestamp in seconds
            qdate         = QDateTime.fromSecsSinceEpoch( raw_data ).date()

        self.set_preped_data( qdate   )
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


# ---------------------------------
class CQDateEditOld( QDateEdit,  CQEditBase ):
# class CQDateEdit( CQEditBase, QDateEdit,   ):  # reverse does not help
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

        # ---- set functions
        # a_partial           = partial( self.do_ct_value, "do_ct_value!!" )
        # self.ct_default     = a_partial
        self.ct_default     = self.do_ct_prior
        self.ct_prior       = self.do_ct_prior
        #self.is_valid       = self.validate_all_ok
        self.null_surogate  = QDate( 1980, 1, 1 )


        self.default_type          = "today"   # need begin of day, end of day ??
        self.default_value         = None     # if used make a qdate
        self.config_calender_popup( True )
        # prior value, prior_type
        self.is_editable            = True  #  --- by the user   may be built in
                                        # will nee a configure for it


        raw_data      = self.get_raw_data()
        msg      = ( f"raw_data = {raw_data}")    # PyQt5.QtCore.QDate(2000, 1, 1)
        logging.debug( msg )


        try:
            msg   = ( "__init__ start try")
            logging.debug( msg )

            self.set_preped_data( None )
            # output has start and stop but still this in output
            # TypeError: invalid result from CQDateEdit.validate_all_ok()
            msg   = ( "__init__stop try")
            logging.debug( msg )
        except:
            msg   = ( "__init__pass on except")
            logging.error( msg )
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
        final step from set_data should always be qdate
        """
        qdate   = self.date()
        return qdate

    #----------------------------
    def set_preped_data( self, qdate, is_changed = True  ):
        """'
        final step from set_data should always be qdate
        specialized by name of function call
        """
        if qdate == None:
            qdate   = self.null_surogate
            msg        = f"date edit using null_surrogate for {self.field_name}"
            logging.debug( msg )

        elif not isinstance( qdate,  QDate ):
            self_field_name   = self.field_name
            msg = f"set_preped_data error qdate, not a QDate {self.field_name = }  return ??for now inspect then break"
            logging.error( msg )
            return
            wat_inspector.go(
                msg            = msg,
                # inspect_me     = self.people_model,
                a_locals       = locals(),
                a_globals      = globals(), )
            breakpoint()


        # self.setDate( qdate  )  # was going to validate next seems to fix
        #super( QDateEdit, self).setDate( qdate )  # Ensure QDateEdit.setDate() is called
            # above still going to to self.validate sometimes
        xxx= """
        i am in a control that inherits from QDateEdit as well as others.
        i want to call the method setDate in the control, but it seems to
        be going thew wrong place.  any fixes for this?
        here is another try at it
        """
        QDateEdit.setDate( self, qdate )

    # -------------------------------
    def __str__( self ):

        a_str   = ""

        a_str   = f"{a_str}{CQEditBase.__str__( self, )    }"

        a_str   = f"{a_str}\n>>>>>>>>>>* CQDateEdit ( nothing so far ) *<<<<<<<<<<<<"

        # a_str   = string_util.to_columns( a_str, ["default_type",
        #                                    f"{self.default_type}" ] )
        # # a_str   = string_util.to_columns( a_str, ["default_value",
        # #                                    f"{self.default_value}" ] )
        # a_str   = string_util.to_columns( a_str, ["is_changed",
        #                                    f"{self.is_changed}" ] )


        # more    = CQEditBase.__str__( self, )
        # a_str   = f"{a_str}\n{more}"
        return a_str



# ---- EOF ----------------------------
