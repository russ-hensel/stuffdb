#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 08:28:33 2025

@author: russ
"""


# ---- tof

# ---- imports
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
# ---- end imports


#-------------------------------

# ----------------------------------------
class KeyGen(   ):
    """
    runs sql when passed a dict -- no under construction

    outpur to ?? a file
    """
    def __init__(self, db_file_name ):
        """
        the usual
            will assume sql lite for now



        """
        self.db_file_name    = db_file_name


# ---- eof



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

        # debug_msg   = ( "QsqlDbAccess  init_db()" )
        # logging.log( LOG_LEVEL,  debug_msg, )

        db_file_name    = self.db_file_name
        db_type         = "QSQLITE"
        self.db         = QSqlDatabase.addDatabase( db_type  )
        self.db.setDatabaseName( db_file_name   )

        if not self.db.open():
            msg    = f"Database Error: {self.db.lastError().databaseText()} {db_file_name =} "
            print( msg, )
            # QMessageBox.critical(
            #     None,
            #     "databasenot open - Error!", msg
            #     )

        connection_name = self.db.connectionName()
        debug_msg     = ( f"{connection_name = }")
        print(  debug_msg, )

        #
        """
        self.optimize_1()
        # # ia_qt.q_sql_database( self.db,
        #                               msg           = "in init_db()",
        #                               include_dir    = False) )
        """


        sql     = """INSERT INTO book_club (
                name,
                frequency  )
                VALUES (?, ? )
            """

            query.prepare( sql )
            query.addBindValue( name )
            query.addBindValue( frequency )

        # !! do we ever execute

    #-----------------------------------------------
    def delete_data( self ):
        """

        """
        print_func_header( "delete_data()  not implemented" )
        self.append_msg( tab_base.DONE_MSG )






# ----------------------------------------
class RunSql(   ):
    """
    runs sql when passed a dict

    outpur to ?? a file
    """
    def __init__(self, sql_dict ):
        """
        the usual


        sql_dict

        sql_dict["sql_type"]        = "select"
        sql_dict["db_file_name"]    =  ":memory:"
        sql_dict["db_file_name"]    = "/tmp/ramdisk/qt_sql.db"
        sql_dict["sql"]             = "select"
        sql_dict["db_type"]             = "QSQLITE"

        """

        self.sql_dict   = sql_dict

        if sql_dict["sql_type"] == "select":
            pass
            #self.run_sql_select   = RunSqlSelect( sql_dict )

        print( "all done ")
# ---- eof



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

        # debug_msg   = ( "QsqlDbAccess  init_db()" )
        # logging.log( LOG_LEVEL,  debug_msg, )

        db_file_name    = self.sql_dict["db_file_name"]
        db_type         = self.sql_dict["db_type"]
        self.db         = QSqlDatabase.addDatabase( db_type  )
        self.db.setDatabaseName( db_file_name   )

        if not self.db.open():
            msg    = f"Database Error: {self.db.lastError().databaseText()} {db_file_name =} "
            print( msg, )
            # QMessageBox.critical(
            #     None,
            #     "databasenot open - Error!", msg
            #     )

        connection_name = self.db.connectionName()
        debug_msg     = ( f"{connection_name = }")
        print(  debug_msg, )

        #
        """
        self.optimize_1()
        # # ia_qt.q_sql_database( self.db,
        #                               msg           = "in init_db()",
        #                               include_dir    = False) )
        """

    #-----------------------------------------------
    def insert_data( self ):
        """
        also see the tab_qsql_database.py  populate_book_club_table
        this uses bind variables, probably the safeest way to execute sql
        """
        print_func_header( "insert_data()" )

        query = QSqlQuery(  global_vars.EX_DB  )

        table_data = [
            ("History",      "weekly"    ),
            ("Adventure",    "weekly"    ),
            ("Easterns",      "monthly"   ),
            ("Physics",      "daily"     ),
        ]

        for name, frequency in table_data:
            # this only one way to bind
            sql     = """INSERT INTO book_club (
                name,
                frequency  )
                VALUES (?, ? )
            """

            query.prepare( sql )
            query.addBindValue( name )
            query.addBindValue( frequency )

        # !! do we ever execute

    #-----------------------------------------------
    def delete_data( self ):
        """

        """
        print_func_header( "delete_data()  not implemented" )
        self.append_msg( tab_base.DONE_MSG )



class RunSqlSelect():
    def __init__(self, run_sql ):
        """
        the usual
        """
        self.run_sql   = run_sql
        #self.sql_dict   = sql_dict




    #-----------------------------------------------
    def select_and_output( self ):
        """
        select data then loop through with a print
        test qsql_utils
        """

        sql         =  self.sql_dict["sql"]

        query      = QSqlQuery(  self.run_sql.db )

        query_ok   =  query_exec_error_check( query = query, sql = sql, raise_except = True )

        msg      = ("query = {sql }")
        output( msg )

        while query.next():
            # a_id        = query.value(0)
            # name        = query.value(1)
            # frequency   = query.value(2)

            msg      = (f"ID: {query.value(0)}  {query.value(0)}  {query.value(0) }  ")
            output( msg )



def output( a_string ):
    """ """
    print( a_string )



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
        error_txt       =  query.lastError().text()
        loc             = "query_exec_error_check"
        debug_msg        = f"{loc} >>> error sql = { sql } \n lastError = {error_txt = }"
        logging.debug( debug_msg )
        dialog          =  DisplaySQLError( parent = None, title = "SQL Error", msg = debug_msg )
        if dialog.exec_() == QDialog.Accepted:
            pass

        raise SQLError( "sqlerror", debug_msg )

    else:
        pass
        #rint("Query executed successfully.")
    return query_ok