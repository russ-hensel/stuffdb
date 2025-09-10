#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""
Created on Mon Jul  8 16:41:23 2024



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


import logging
import sqlite3

import time

from PyQt5.QtCore import QDate, QModelIndex, Qt, QTimer, pyqtSlot
from PyQt5.QtGui import QIcon, QIntValidator, QStandardItem, QStandardItemModel
from PyQt5.QtSql import QSqlDatabase, QSqlError, QSqlQuery, QSqlTableModel
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

LOG_LEVEL   =   10

# ---- imports local
from app_global import AppGlobal


# ----------------------------------------
class QsqlDbAccess(   ):
    """
    for connections to the db
    """
    def __init__( self, connection_name  ):
        """
        usual
        """
        self.connection         = None
        self.db                 = None   # use as interface
        self.connection_name    = connection_name
        self.init_db()

        #rint( "")

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

        debug_msg   = ( "QsqlDbAccess  init_db()" )
        logging.log( LOG_LEVEL,  debug_msg, )

        db_file_name    = AppGlobal.parameters.db_file_name
        self.db         = QSqlDatabase.addDatabase( AppGlobal.parameters.db_type, self.connection_name  )
                # make this name unique -- from utils....
        self.db.setDatabaseName( db_file_name )

        if not self.db.open():
            msg    = f"Database Error: {self.db.lastError().databaseText()} {db_file_name =} "
            logging.error( msg, )
            QMessageBox.critical(
                None,
                "databasenot open - Error!", msg
                )

        connection_name = self.db.connectionName()
        debug_msg     = ( f"{connection_name = }")
        logging.log( LOG_LEVEL,  debug_msg, )

        # Use the sqlite3 module to connect to the same database
        sqlite_conn         = sqlite3.connect( db_file_name )
        self.sqlite_conn    = sqlite_conn

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
        self.optimize_1()
        # # ia_qt.q_sql_database( self.db,
        #                               msg           = "in init_db()",
        #                               include_dir    = False) )

    # --------------------------------
    def log_sql_callback( self, statement ):
        msg      = f"log_sql_callback {statement}"
        logging.log( LOG_LEVEL,  msg, )

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
                # not the name the file_name

        if not self.connection.open():
            QMessageBox.critical(
                None,
                "Connection not open - Error!",
                "Database Error: %s" % self.connection.lastError().databaseText(),
            )

        msg      = f"get_connection for { AppGlobal.parameters.db_fn}"
        logging.debug( msg )

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
        # debug_msg      = f"Executing SQL query: query_exec_model {query.executedQuery() = }"
        # logging.log( LOG_LEVEL,  debug_msg, )

        if query.exec():
            model.setQuery( query )
            if model.lastError().isValid():
                msg     = f"Query Error: query_exec_model {model.lastError().text() = }"
                logging.error( msg, )

                return False

        else:  # fail
            msg    =  ( f"Query Execution Error:query_exec_model {query.lastError().text()}" )
            logging.error( msg, )

            msg    =  ( f"( {query.executedQuery()} "  )
            logging.error( msg, )

            return False

        return True


    # --------------------------------
    def optimize_1( self, ):
        """
        from grok edited

        Optimize SQLite database settings for performance.

        """
        # Connect to the database
        conn        = self.sqlite_conn
        cursor      = conn.cursor()

        # Apply PRAGMA settings for performance
        try:
            # Set synchronous mode to NORMAL for a balance of speed and safety
            cursor.execute("PRAGMA synchronous = NORMAL;")

            # Enable Write-Ahead Logging for better concurrency --
            #    currently I do not have transaction management for this.
            #cursor.execute("PRAGMA journal_mode = WAL;")

            # # Increase cache size to ~100 MB (assuming 4 KB page size)
            # cursor.execute("PRAGMA cache_size = 25000;")  # 25,000 pages

            # # Store temporary tables in memory
            # cursor.execute("PRAGMA temp_store = MEMORY;")

            # # Set exclusive locking mode for single-user applications
            # cursor.execute("PRAGMA locking_mode = EXCLUSIVE;")

            # # Set busy timeout to 5 seconds to handle contention
            # cursor.execute("PRAGMA busy_timeout = 5000;")

            # # Set page size to 8192 (must be set before creating tables or use VACUUM)
            # cursor.execute("PRAGMA page_size = 8192;")

            # # Apply the new page size by running VACUUM (rebuilds the database)
            # cursor.execute("VACUUM;")

            # Optimize query planning (run periodically)
            cursor.execute("PRAGMA optimize;")

            # Commit PRAGMA changes
            conn.commit()

        except sqlite3.Error as e:
            print(f"Error applying PRAGMA settings: {e}")
            conn.rollback()
            return

        finally:
            conn.commit()

        # # Example: Create a table and index
        # try:
        #     # Create a sample table
        #     cursor.execute("""
        #         CREATE TABLE IF NOT EXISTS users (
        #             id INTEGER PRIMARY KEY,
        #             name TEXT,
        #             email TEXT
        #         );
        #     """)

        #     # Create an index on the email column for faster queries
        #     cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON users(email);")

        #     # Example: Batch insert with a transaction
        #     start_time = time.time()
        #     cursor.execute("BEGIN TRANSACTION;")
        #     # Insert multiple rows in a single statement
        #     rows = [(i, f"User {i}", f"user{i}@example.com") for i in range(1, 1001)]
        #     cursor.executemany("INSERT INTO users (id, name, email) VALUES (?, ?, ?);", rows)
        #     cursor.execute("COMMIT;")
        #     print(f"Inserted 1000 rows in {time.time() - start_time:.2f} seconds")

        #     # Example: Query with index
        #     cursor.execute("SELECT * FROM users WHERE email = ?;", ("user500@example.com",))
        #     result = cursor.fetchone()
        #     print(f"Query result: {result}")

        #     # Example: Analyze query plan
        #     cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM users WHERE email = ?;",
        #                   ("user500@example.com",))
        #     query_plan = cursor.fetchall()
        #     print("Query Plan:", query_plan)

        # except sqlite3.Error as e:
        #     print(f"Error during table operations: {e}")
        #     conn.rollback()

        # finally:
        #     # Close the connection
        #     conn.close()


# ---- eof
