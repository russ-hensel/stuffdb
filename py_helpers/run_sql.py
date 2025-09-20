#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 08:28:33 2025

@author: russ
"""


# ---- tof

# ---- tof
# --------------------
if __name__ == "__main__":
    import main
    #main.main()
# ----------------



# ---- imports
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
# ---- end imports

from stuffdb import STUFFDB_CONNECTION_NAME
import parameters

#-------------------------------

# ----------------------------------------
class KeyGenxxx(   ):
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

        db_file_name        = self.db_file_name
        db_type             = "QSQLITE"
        self.db             = QSqlDatabase.addDatabase( db_type  )
        self.connect_name   = "temp_connect_db"  # not the file name

        self.is_existing    = False

        if QSqlDatabase.contains( self.connect_name ):
            self.db             = QSqlDatabase.database( self.connect_name )
            self.is_existing    = True
        else:
            self.db             = QSqlDatabase.addDatabase( self.db_type, self.connection_name )
            self.db.setDatabaseName( self.db_file_name)

        if not self.db.open():
            msg    = f"Database Error: {self.db.lastError().databaseText()} {db_file_name =} "
            print( msg, )
            # QMessageBox.critical(
            #     None,
            #     "databasenot open - Error!", msg
            #     )

        connection_name = self.db.connectionName()
        debug_msg     = ( f"init_db {connection_name = }")
        print(  debug_msg, )



    #-----------------------------------------------
    def delete_data( self ):
        """

        """
        # print_func_header( "delete_data()  not implemented" )
        # self.append_msg( tab_base.DONE_MSG )


# ----------------------------------------
class RunSql(   ):
    """
    runs sql when passed a dict

    outpur to ?? a file
    print goes back to gui
    if run from >>py
    """

    def __init__(self, sql_dict ):
        """
        the usual


        sql_dict

        sql_dict["sql_type"]        = "select"
        sql_dict["db_file_name"]    =  ":memory:"
        sql_dict["db_file_name"]    = "/tmp/ramdisk/qt_sql.db"
        sql_dict["sql"]             = "select"
        sql_dict["db_type"]         = "QSQLITE"

        might want a column list for select or can we parse?

        """
        self.sql_dict       = sql_dict
        self.connect_name   = None
        try:
            self.go()


        except Exception as error:

            error_message = str(error)
            msg  = (f"Caught an erro in __init__: {error_message}")
            print( msg )

            # msg_box_msg    = "this is a message"
            # msg_box             = QMessageBox()
            # msg_box.setIcon( QMessageBox.Information )
            # msg_box.setText(  msg_box_msg  )
            # msg_box.setWindowTitle( "Sorry that is a No Go " )
            # msg_box.setStandardButtons( QMessageBox.Ok )

        finally:
            self.finalize_db()
            self.close_file_out()


    def go(self,   ):
        """


        """
        self.is_existing = False

        key             = "output_type"
        get_item        = self.sql_dict.get( key, None )
        if not get_item:
            self.sql_dict[ key ] = None
        else:
            self.sql_dict[ key ] = get_item.lower()

        key             = "output_file_name"
        get_item        = self.sql_dict.get( key, None )
        if not get_item:
            self.sql_dict[ key ] = None
        else:
            self.sql_dict[ key ] = get_item


        # output_type  = sql_dict["output_type"].lower( )
        # output_file  = sql_dict["output_file_name"]

        self.columns    = None
        self.file_out   = None   # changes if file is opened


        sql_type   = self.sql_dict["sql_type"].lower( )
        if  sql_type == "select":
            pass
            self.select_data()
            #self.run_sql_select   = RunSqlSelect( sql_dict )

        elif sql_type ==  "delete":
            pass
            self.delete_data()

        self.close_file_out()

        print( "__init__ all done ")


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



        # connection_name = "my_connection"
        # if QSqlDatabase.contains(connection_name):
        #     self.db = QSqlDatabase.database(connection_name)
        # else:
        #     self.db = QSqlDatabase.addDatabase(db_type, connection_name)
        #     self.db.setDatabaseName(db_file_name)


        # for now use name run_sql later perhaps see if there is a dup?
        self.db         = QSqlDatabase.addDatabase( db_type, "run_sql"  )
        self.db.setDatabaseName( db_file_name )

        if not self.db.open():
            msg    = f"Database Error: {self.db.lastError().databaseText()} {db_file_name =} "
            print( msg, )
            # ore except
            return
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
    # --------------------------------
    def finalize_db( self, ):
        """
        use if doing something useful
        see qsql_db_access.py
        seems to get rid of db inless pre-existing
        """
        if not self.is_existing and self.connect_name :
            QSqlDatabase.removeDatabase( self.connect_name )


    #-----------------------------------------------
    def select_data( self ):
        """
        also see the tab_qsql_database.py  populate_book_club_table
        this uses bind variables, probably the safeest way to execute sql
        """
        sql         = self.sql_dict["sql"]
        self.init_db()
        self.open_file_output()

        msg         =  f"for file output see {self.file_out_full_name} "
        print( msg )
        self.output_to_file( msg )


        self.parse_column_list()



        col_width        = self.sql_dict.get( "col_width", None )
        if col_width is None:
            col_widths  = [30] * len( self.columns )
        else:
            if type(col_width) == list:  # !! use is instance
                pass
                # assume width of columns as ints
            else:
                # should just be a number
                col_widths  = [col_width] * len( self.columns )

        query       = QSqlQuery( self.db  )

        query_ok    = True

        result      = query.exec_( sql )

        if not result:
            query_ok        = False
            error_txt       = query.lastError().text()
            loc             = "query_exec_error_check"
            debug_msg       = f"{loc} >>> error sql = { sql } \n lastError = {error_txt = }"
            #logging.debug( debug_msg )
            print( debug_msg )
            # dialog          =  DisplaySQLError( parent = None, title = "SQL Error", msg = debug_msg )
            # if dialog.exec_() == QDialog.Accepted:
            #     pass

            raise Exception( "sqlerror", debug_msg )

        else:
            pass
            #rint("Query executed successfully.")

        ix_line    = 0
        while query.next():
            # a_id        = query.value(0)
            # name        = query.value(1)
            # frequency   = query.value(1)
            ix_line     += 1
            msg         = f"{ix_line:<5} "
            for ix, i_column in enumerate( self.columns):
                msg   = f"{msg}{str(query.value(ix)):{col_widths[ix]}} "
            # msg      = (f"row: {query.value(0) = }  { query.value(1) = }  {query.value(1)} ")

            print( msg )
            self.output_to_file( msg )


        self.finalize_db()

        msg         =  "number of lines {ix_line} "
        print( msg )
        self.output_to_file( msg )

        msg         =  f"for file output see {self.file_out_full_name} "
        print( msg )
        self.output_to_file( msg )

        print( "-------------- all done ---------------------")

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

    #-----------------------------------------------
    def parse_column_list( self ):
        """
        call from select_data
        for the select
        words should be in upper or lower case but not mixed
        require FROM in upper?
        mutates
            self.columns    to contain the column names of the select
        """
        sql      = self.sql_dict["sql"].strip()

        sql      = sql.replace( "from ",   "FROM " )
        sql      = sql.replace( "select ", "SELECT " )

        sql_split   = sql.split( "FROM" )
        sql_select  = sql_split[0]
        #                         1234567
        if sql_select.startswith( "SELECT "):
            pass
        else:
            return
        sql_columns     = sql_select[ 7: ]
        sql_columns     = sql_columns.replace( ",", " ")
        columns         = sql_columns.split( " " )
        # remove empty
        columns         = [i_column for i_column in columns if i_column != ""]


        self.columns    = columns


        # !! do we ever execute

    #-----------------------------------------------
    def delete_data( self ):
        """
        no output to file but return no of deleted

        """
        # print_func_header( "delete_data()  not implemented" )
        # self.append_msg( tab_base.DONE_MSG )
        sql         = self.sql_dict["sql"]
        self.init_db()
        # self.open_file_output()

        # self.parse_column_list()

        query       = QSqlQuery( self.db  )

        query_ok    = True

        result      = query.exec_( sql )

        if not result:
            query_ok        = False
            error_txt       = query.lastError().text()
            loc             = "query_exec_error_check"
            debug_msg       = f"{loc} >>> error sql = { sql } \n lastError = {error_txt = }"
            #logging.debug( debug_msg )
            print( debug_msg )
            # dialog          =  DisplaySQLError( parent = None, title = "SQL Error", msg = debug_msg )
            # if dialog.exec_() == QDialog.Accepted:
            #     pass

            raise Exception( "sqlerror", debug_msg )

        else:
            pass
            #rint("Query executed successfully.")
            rows_deleted = query.numRowsAffected()
            msg          = f"Rows deleted: {rows_deleted}"
            print( msg )


        # while query.next():
        #     # a_id        = query.value(0)
        #     # name        = query.value(1)
        #     # frequency   = query.value(1)

        #     msg      = (f"row: {query.value(0) = }  { query.value(1) = }  {query.value(1)} ")
        #     print( msg )
        #     self.output_to_file( msg )


        self.finalize_db()
        print( "-------------- all done ---------------------")


    #-----------------------------------------------
    def update_data( self ):
        """
        basically the same as delete in how we manage it

        """
        #-----------------------------------------------
        self.delete_data(   )















    #-----------------------------------------------
    def open_file_output( self ):
        """
        args in self.sql_dict
        """
        # print_func_header( "delete_data()  not implemented" )
        # self.append_msg( tab_base.DONE_MSG )
        output_type         = self.sql_dict["output_type"].lower( )
        output_file_name    = self.sql_dict["output_file_name"]


        # lets put it under output
        output_file_name    = parameters.PARAMETERS.output_dir + "/" + output_file_name
        output_file_name    = output_file_name.replace( "//", "/" )
        output_file_name    = output_file_name.replace( "//", "/" )  # super sure


        self.file_out_full_name = output_file_name

        self.file_out       = open( output_file_name,
                                    'w',
                                    encoding  = "utf8",
                                    errors    = 'ignore' )

    # --------------------------------
    def output_to_file( self, msg ):
        """
        self.parent_window.output_to_file( msg )


        """
        if self.file_out:
            self.file_out.write( msg + "\n" )
        #print( msg )

    # --------------------------------
    def close_file_out( self,  ):
        """

        """
        if self.file_out:
            self.file_out.close()
        self.file_out = None




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