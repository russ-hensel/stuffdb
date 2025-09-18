#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
utils for qsql as originally planned no objects, just functions
only coupling to rest of app is
the global logging where using logging should not throw an error
an existing app if message box is called


"""
# ---- tof


APP      = None

import logging

# ---- QtCore
from PyQt5.QtCore import QDate, QModelIndex, Qt, QTimer, pyqtSlot
from PyQt5.QtGui import QIntValidator, QStandardItem, QStandardItemModel
# ---- QtSql
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
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

# ----QtWidgets Boxs, Dialogs
# ----QtWidgets layouts
# ----QtWidgets big
# ----QtWidgets


# from PyQt5.QtWidgets import (QAction,
#                              QActionGroup,
#                              QApplication,
#                              QButtonGroup,
#                              QCheckBox,
#                              QComboBox,
#                              QDateEdit,
#                              QDockWidget,
#                              QFileDialog,
#                              QFrame,
#                              QGridLayout,
#                              QHBoxLayout,
#                              QInputDialog,
#                              QLabel,
#                              QLineEdit,
#                              QListWidget,
#                              QMainWindow,
#                              QMdiArea,
#                              QMdiSubWindow,
#                              QMenu,
#                              QMessageBox,
#                              QPushButton,
#                              QSpinBox,
#                              QTableView,
#                              QTableWidget,
#                              QTableWidgetItem,
#                              QTabWidget,
#                              QTextEdit,
#                              QVBoxLayout,
#                              QWidget)


class SQLError( Exception ):
    """
    raise SQLError( why, errors )
    """
    def __init__(self, why, errors = "not given"):
        """

        I really do not know what I am doing here, works
        but fix in future

        """

        # Call the base class constructor with the parameters it needs
        super( ).__init__(   )
        self.why    = why
        # Now for your custom code...
        self.errors = errors



class DisplaySQLError( QDialog ):
    """
    for display of errors, may move out of here
    and have a callback function
    how does this know abot the parent or qapplication

    """
    # ------------------------------------------
    def __init__(self, *, parent = None, title, msg  ):
        """
        Args:
            need to make sure destroped on close

        Returns:
            None.

        """
        super().__init__( parent )
        self.parent         = parent  # parent may be a function use parent_window
        self.parent_window  = parent

        self.setWindowTitle( title  )

        qt_xpos     = 10
        qt_ypos     = 10
        qt_width    = 1000
        qt_height   = 500
        self.setGeometry(  qt_xpos,
                           qt_ypos ,
                           qt_width,
                           qt_height  )

        self._build_gui( title, msg )

    # ------------------------------------------
    def _build_gui( self, title, msg  ):
        """
        what it says, read?
        """
        layout              = QVBoxLayout( self )
        self.layout         = layout

        # ---- code_gen: edit_fields_for_form  -- end table entries

        # Create QTextEdit widget
        text_edit           = QTextEdit()
        # layout.addWidget(text_edit, 4, 0, 1, 3)  # Row 4, Column 0, RowSpan 1, ColumnSpan 3
        self.text_edit  = text_edit
        layout.addWidget( text_edit )

        cursor = text_edit.textCursor()
        cursor.insertText( msg )

        # # ---- buttons
        # self.setLayout( self.layout )
        #self.button_layout      = QVBoxLayout()
        button_layout           = layout

        a_widget                = QPushButton("OK")
        a_widget.clicked.connect( self.accept )
        button_layout.addWidget( a_widget )

        # # ----
        # self.buttons.setLayout( self.button_layout )

        # self.layout.addRow(self.buttons)

def query_exec_error_check( *, query, sql = None, raise_except = True ):
    """
    !! think about outher args
    make this the standard error checking
    or send result an query as arguments
    from a tab in qt5_by_example
    query may be preloaded with sql or not
    query may have returned rows but that is managed in the caller
    add where called from to get a traceback but we plan to raise a message
    return
        query_ok    True or False, but execpt may be thrown
        query_ok   =  qsql_utils.query_exec_error_check(  query = query, sql = sql, raise_except = True )
    """
    query_ok    = True
    if sql is None:
        result  = query.exec_( )  # sql already in the query
    else:
        result  = query.exec_( sql )

    if not result:
        query_ok        = False
        error_txt       = query.lastError().text()
        loc             = "query_exec_error_check"
        debug_msg       = f"{loc} >>> error sql = { sql } \n lastError = {error_txt = }"
        logging.debug( debug_msg )
        dialog          =  DisplaySQLError( parent = None, title = "SQL Error", msg = debug_msg )
        if dialog.exec_() == QDialog.Accepted:
            pass

        raise SQLError( "sqlerror", debug_msg )

    else:
        pass
        #rint("Query executed successfully.")
    return query_ok

# ------------------------
def ok_message_box(  title = "please a title", msg = "this is a default message " ):
    """
    read it
    qsql_utils.ok_message_box(  title  = " a_title",
                                 msg   = msg  )
    """

    msg_box = QMessageBox()
    msg_box.setIcon( QMessageBox.Information )
    msg_box.setText( msg )  # Set the message text
    msg_box.setWindowTitle( title  )
    msg_box.setStandardButtons( QMessageBox.Ok )

    # Show the message box and wait for the user to close it
    msg_box.exec_()



#--------------
def execute_sql_may_delete_not_used( msg = None, db = None, sql = None  ):
    """
    what it says
    from db_create.py
    this is for sql that has no return result
    but just use above
    """
    print( f"execute_sql: {msg} \n    {sql}")
    db.transaction()
    query = QSqlQuery( db )

    query.exec( sql )

    last_error    = query.lastError ()
    print( f"create_table_help {last_error} = " )
    # ia_qt.q_sql_error( last_error,
    #                    msg =  "now in code at: execute_sql ",
    #                    print_it = True,
    #                    include_dir = False,    # default False
    #                    )
    db.commit()

    print( "execute_sql done")


# ---- tof

# ---- imports

# ---- end imports


#-------------------------------






# ---- eof