#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof

"""
Created on Fri Jul  5 08:23:13 2024

@author: russ
"""

# --------------------
if __name__ == "__main__":
    import main
    main.main()
# --------------------

# ---- imports
import sqlite3

from app_global import AppGlobal


from qt_compat import QApplication, QAction, exec_app, qt_version
from PyQt.QtWidgets import QMainWindow, QToolBar, QMessageBox
from qt_compat import Qt, DisplayRole, EditRole, CheckStateRole
from qt_compat import TextAlignmentRole





# ---- QtSql
from PyQt.QtSql import (QSqlDatabase,
                         QSqlError,
                         QSqlField,
                         QSqlQuery,
                         QSqlRecord,
                         QSqlTableModel)
# ----QtWidgets
from PyQt.QtWidgets import QWidget


class KeyGenerator:
    def __init__(self, db):
        """
        just connect to db
        """
        self.db = db

    def get_next_key(self, table_name, refresh = False):
        """
        what it says, read
        if refresh is true get the max fom the table first
            but not implemented --- think about it !!
        """
        query = QSqlQuery(self.db)

        self.db.transaction()

        # Fetch the current key value for the table
        query.prepare("SELECT key_value FROM key_gen WHERE table_name = :table_name")
        query.bindValue(":table_name", table_name)
        query.exec()

        if query.next():
            current_key     = query.value(0)
            next_key        = current_key + 1
            update_query = QSqlQuery( self.db )
            update_query.prepare("UPDATE key_gen SET key_value = :next_key WHERE table_name = :table_name")
            update_query.bindValue(":next_key", next_key)
            update_query.bindValue(":table_name", table_name)
            update_query.exec()

        else:
            next_key = 1000
            insert_query = QSqlQuery(self.db)
            insert_query.prepare("INSERT INTO key_gen (table_name, key_value) VALUES (:table_name, :key_value)")
            insert_query.bindValue(":table_name", table_name)
            insert_query.bindValue(":key_value", next_key)
            insert_query.exec()

        self.db.commit()
        #rint( f"key gen {next_key = } for {table_name = } ")
        return next_key

    #---------------------------
    def update_key_for_table(self, table_name, a_key ):
        """
        """
        update_query = QSqlQuery( self.db )
        update_query.prepare("UPDATE key_gen SET key_value = :next_key WHERE table_name = :table_name")
        update_query.bindValue(":next_key",   a_key)
        update_query.bindValue(":table_name", table_name)
        update_query.exec()

    #---------------------------
    def get_max_for_table( self, table_name ):
        """
        what it says, reading should be clear

        """
        query = QSqlQuery( self.db )
        sql   =  f"SELECT MAX(id) FROM  {table_name}"


        if qt_version == 6:
            query.exec( sql )
        else:
            query.exec_( sql )

        if query.next():
            max_id     = query.value(0)

        else:
            max_id     = -9999

        #msg    = f"max id for table {table_name =} is {max_id = }"

        return max_id

# ========================================
class KeyGeneratorWithModel( QWidget ):
    """
    generates primary keys for other recods
    """
    # -------
    def __init__( self ):
        """
        the usual


        """
        super().__init__()
        self.key_dict = {}      # for what

        model               = QSqlTableModel( self, AppGlobal.qsql_db_access.db )
        self.model          = model
        self.table          = "key_gen"
        model.setTable( self.table )

    # -------------------------
    def get_next_key( self, table_name ):
        """
        will get the next key and update anything
        needing it
        !! may want try with a finally then rethow
        Args:
            table_name (TYPE): DESCRIPTION.

        Returns:
            next key an int

        """
        next_key                = None
        # model                   = QSqlTableModel( self, AppGlobal.qsql_db_access.db )
        model                   = self.model

        #ia_qt.q_sql_table_model( model, include_dir= False )

        #model.setFilter( (f"id = {id}") )
        model.select()
        # channel
        ia_qt.q_sql_table_model( model,    msg = "in get_next_key", include_dir= False )
        record_0 = model.record( 0 )

        ia_qt.q_sql_table_model( model,
                                msg = "in get_next_key",
                                include_dir= False )


        print( f"{record_0} = " )
        ia_qt.q_sql_record( record_0,
                                  msg = "in get_next_key",
                                  include_dir= False )

        field_0         = record_0.field( 0 )
        ia_qt.q_sql_field(  field_0,
                                msg = "in get_next_key field_0",
                                include_dir= False  )

        field_1         = record_0.field( 1 )
        ia_qt.q_sql_field(  field_1,
                                msg = "in get_next_key field_1",
                                include_dir= False  )

        # self.yt_id_field.setText(  record.value(    "yt_id"      ))
        # model.submitAll()


    # -------------------------
    def get_next_key_newer ( self, table_name ):
        """
        will get the next key and update anything
        needing it
        !! may want try with a finally then rethow
        Args:
            table_name (TYPE): DESCRIPTION.

        Returns:
            next key an int

        """
        next_key        = None

        #qt_db       = AppGlobal.qsql_db_access    #  QSqlDatabase.database()
        #db          = qt_db.database()()
        #connection  = sqlite3.connect( db.databaseName() )


        connection  =  AppGlobal.qsql_db_access.get_connection()  # must not be closed

        print( ia_qt.q_sql_database( connection,
                                  msg           = "in get_next_key"  ,
                                  include_dir   = True ) )


        cursor      = connection.cursor()

        # cursor.execute("SELECT * FROM records WHERE id = ?", (1,))

        sql             = f'select key_value from key_gen where table_name = "{table_name}";'
        cursor.execute( sql, ( ) )

        result   = cursor.fetchall()  # returns list of tuples
        result   = result[ 0 ]
        key      = result[ 0 ]
        print( key )
        #connection.close()

        #return result  # next_key

        #row             = AppGlobal.sql_runner.select( sql, sql_data  )


        next_key        = key + 1

        sql             = f"""
                                UPDATE key_gen
                                SET key_value = {next_key}
                                WHERE  table_name = "{table_name}";
                                """
        print( sql )
        cursor.execute( sql, ( ) )

        #  AppGlobal.sql_runner.select( sql, {}  )
        # connection.commit()
        # connection.close()
        return next_key

    # -------------------------
    def get_next_key_old( self, table_name ):
        """
        will get the next key and update anything
        needing it

        Args:
            table_name (TYPE): DESCRIPTION.

        Returns:
            next key an int

        """
        next_key        = None

        sql             = f'select key_value from key_gen where table_name = "{table_name}";'
        sql_data        = {}
        print( sql )
        row             = AppGlobal.sql_runner.select( sql, sql_data  )

        print( row )
        next_key        = row[0] + 1

        sql             = f"""
                                UPDATE key_gen
                                SET key_value = {next_key}
                                WHERE  table_name = "{table_name}";
                                """

        AppGlobal.sql_runner.select( sql, {}  )

        # """
        # UPDATE key_gen
        # SET key_value = 55
        # WHERE  table_name = 'channel';

        # """

        return next_key


# ---- eof