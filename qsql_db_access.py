#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 16:41:23 2024

@author: russ
"""
# ---- imports
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
my reference list of qt imports comes from import_qt.py

PyQt5.QtSql.QSqlError

qsql_db_access.QsqlDbAcess()

"""

# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    main.main()
# --------------------


import sqlite3

# ---- imports local
from app_global import AppGlobal
# ---- QtCore
from PyQt5.QtCore import QDate, QModelIndex, Qt, QTimer, pyqtSlot
# ---- begin pyqt from import_qt.py
# ---- QtGui
from PyQt5.QtGui import QIcon, QIntValidator, QStandardItem, QStandardItemModel
# ---- QtSql
from PyQt5.QtSql import QSqlDatabase, QSqlError, QSqlQuery, QSqlTableModel
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
                             QTabWidget,
                             QTextEdit,
                             QToolBar,
                             QVBoxLayout,
                             QWidget)


# ----------------------------------------
class QsqlDbAccess(   ):
    """

    """
    def __init__( self,   ):
        """


        """
        self.connection   = None
        self.db           = None   # use as interface

        self.init_db()

        print( "")


    # --------------------------------
    def init_db( self, ):
        """
        why not just get_connection

        print( "Channel Subwindow init_db" )
        self.db = QSqlDatabase.addDatabase( AppGlobal.parameters.db_type )
        self.db.setDatabaseName(            AppGlobal.parameters.db_fn )
        if not self.db.open():
            QMessageBox.critical( None, "Database Error", self.db.lastError().text())

        db = AppGlobal.qsql_db_access.db
        xxxAppGlobal.db    = self.db   # globla avail
        db appears to be the connection
        russ is still confused try using AppGlobal.qsql_db_access.db   = a_qsql_db_access.db
        """
        print( "QsqlDbAccess  init_db()" )
        self.db = QSqlDatabase.addDatabase( AppGlobal.parameters.db_type  )
        self.db.setDatabaseName(            AppGlobal.parameters.db_fn   )

        if not self.db.open():
            msg    = "Database Error: {self.db.lastError().databaseText()}"
            QMessageBox.critical(
                None,
                "databasenot open - Error!", msg
                                )
        connection_name = self.db.connectionName()
        print( "{connection_name = }")

        # Use the sqlite3 module to connect to the same database
        sqlite_conn = sqlite3.connect( AppGlobal.parameters.db_fn )

        # this is a chat lie
        #assert sqlite_conn == self.db.nativeHandle(), "Connections are not the same!"

        # Set the trace callback
        #sqlite_conn.set_trace_callback(log_sql_callback)

        # this is for usual callback in python api
        # Register the callback function with sqlite3_trace()
        sqlite_conn.set_trace_callback( self.log_sql_callback )


        """
        # Define a callback function to log SQL statements
        def log_sql_callback(statement):
            print("Executing SQL statement:", statement)

        # Create a SQLite database connection
        conn = sqlite3.connect('example.db')

        # Register the callback function with sqlite3_trace()
        conn.set_trace_callback(log_sql_callback)

        """

        # # ia_qt.q_sql_database( self.db,
        #                               msg           = "in init_db()",
        #                               include_dir    = False) )

    # --------------------------------
    def log_sql_callback( self, statement ):
        msg      = f"log_sql_callback {statement}"
        print( msg )

    # --------------------------------
    def get_connectionxxx( self, ):
        """
        consider in an object of its own
        is this how we connect it is unclear how this works, just a stab in dark
        uncleare where this needs to be located ...
        """
        if  self.connection:
            return self.connection

        else:
            # db_type    =  ..... ??
            self.connection = QSqlDatabase.addDatabase( AppGlobal.parameters.db_type  )
            self.connection.setDatabaseName( AppGlobal.parameters.db_fn   )

        if not self.connection.open():
            QMessageBox.critical(
                None,
                "Connection not open - Error!",
                "Database Error: %s" % self.connection.lastError().databaseText(),
            )

        msg      = f"get_connection for { AppGlobal.parameters.db_fn}"
        print( msg )
        AppGlobal.logger.debug( msg )

        return self.connection



    # -------------------------------------------
    def query_exec_model(self, query, model,  msg = None ):
        """
        exec queries with some error checking
        return ok   = True if now error

        is_ok  = AppGlobal.qsql_db_access.query_exec_model( query,
                                                  model,
                                                  msg = None )
        """
        msg      = f"Executing SQL query:  {query.executedQuery() = }"
        AppGlobal.logger.debug( msg )

        if query.exec():
            model.setQuery( query )
            if model.lastError().isValid():
                msg     = f"Query Error: {model.lastError().text() = }"
                print(  msg )
                AppGlobal.logger.error( msg )
                return False

        else:
            print( "Query Execution Error:", query.lastError().text())
            print(  msg )
            AppGlobal.logger.error( msg )
            print( query.executedQuery()   )
            return False

        return True

# ---- eof
