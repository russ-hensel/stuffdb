#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 15:36:04 2025

@author: russ
"""


# ---- tof
import adjust_path
# ---- imports
import sqlite3
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel
)
from PyQt5.QtCore import QThread, pyqtSignal


from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QMessageBox
)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

import parameters
import parms_temp
import copy_help_table
import  data_dict


# ---- end imports
# --- Database Setup and Core Logic Class ---

class TableCopier:
    """Handles QSqlDatabase connections and the core copy logic.
    """
    def __init__(self, source_db_name='source.db', dest_db_name='destination.db'):
        self.source_db_name = source_db_name
        self.dest_db_name   = dest_db_name
        #self.table_name     = 'help_info'

    def _get_db_connection(self, db_name, connection_name):
        """Helper to establish a Qt SQLite connection."""
        db = QSqlDatabase.addDatabase("QSQLITE", connection_name)
        db.setDatabaseName(db_name)
        if not db.open():
            # QSqlDatabase.lastError().text() provides detailed error info
            raise Exception(f"Failed to open database {db_name}: {db.lastError().text()}")
        return db



    def copy_data(self, db_src_file_name, db_dest_file_name, table_name, columns ):
        """
        Copies data from source to destination using QSqlQuery,
        named bind variables, and a WHERE clause.
        """
        db_src      = db_src_file_name
        db_dst      = db_dest_file_name
        rows_copied = 0

        try:
            # 1. Connect to databases
            db_src      = self._get_db_connection(self.source_db_name, "src_db")
            query_src   = QSqlQuery(db_src)

            db_dst      = self._get_db_connection(self.dest_db_name, "dest_db")
            query_dst = QSqlQuery(db_dst)

            # COLUMNS = [
            #     "id", "id_old", "type", "sub_system", "system", "key_words",
            #     "add_ts", "edit_ts", "table_name", "column_name", "java_type",
            #     "java_name", "java_package", "title", "is_example", "can_execute"
            # ]

            COLUMNS = columns

            # Create the named bind variable placeholders for the INSERT statement
            BIND_VARS = [f":{col}" for col in COLUMNS]
            # 2. SELECT data from source using a named bind variable in the WHERE clause
            select_cols = ", ".join(COLUMNS)
            select_sql = f"""
                SELECT {select_cols}
                FROM {table_name}
                WHERE system = :sys_val
            """

            # 3. Prepare the INSERT statement for the destination
            insert_sql = f"""
                INSERT INTO {table_name} ({select_cols})
                VALUES ({", ".join(BIND_VARS)})
            """

            db_dst.transaction()

            query_src.prepare(select_sql)

            # Bind the value for the WHERE clause
            query_src.bindValue( ":sys_val", "Linux" )

            # Start transaction on destination for performance and atomicity
            if not query_src.exec():
                raise Exception(f"Source SELECT failed: {query_src.lastError().text()}")

            query_dst.prepare(insert_sql)

            # 4. Iterate results and INSERT into destination
            while query_src.next():

                # Retrieve values and bind them to the INSERT query using the column names
                for i, col_name in enumerate(COLUMNS):
                    value = query_src.value(i)
                    # Bind the value using the named placeholder, e.g., ":id"
                    query_dst.bindValue(f":{col_name}", value)

                if not query_dst.exec():
                    db_dst.rollback() # Rollback on error
                    raise Exception(f"Destination INSERT failed (Row {rows_copied + 1}): {query_dst.lastError().text()}")

                rows_copied += 1

            # 5. Commit changes
            db_dst.commit()

            # 6. Verification
            count_query = QSqlQuery(db_dst)
            count_query.exec("SELECT COUNT(*) FROM help_info")
            count_query.next()
            total_rows = count_query.value(0)

            return (
                f"Copy completed successfully! {rows_copied} rows copied.\n"
                f"Destination table 'help_info' now has {total_rows} total rows."
            )

        except Exception as e:
            return f"Operation FAILED: {e}"

        finally:
            # 7. Clean up connections
            if db_src and db_src.isOpen():
                db_src.close()
            if db_dst and db_dst.isOpen():
                db_dst.close()
            # Crucial for managing multiple connections: remove the connection objects
            QSqlDatabase.removeDatabase("src_db")
            QSqlDatabase.removeDatabase("dest_db")


def get_columns( table_name ):
    """

    """

    a_data_dict     = data_dict.build_it()    # returns DATA_DICT

    a_table         = a_data_dict.get_table( table_name  )
    a_result        = a_table.get_list_columns_sql_order()
    print(  a_result  )
    column_names    = [ i_column.column_name for i_column in a_result ]
    print( column_names )
    return column_names

def do_copy(table_name ):

    a_parms_temp            = parms_temp.ParmsTemp()

    src_db_file_name        = parameters.PARAMETERS.db_file_name
    dest_db_file_name       = a_parms_temp.db_file_name

    columns                 = get_columns( table_name )

    a_copier                = copy_help_table.TableCopier( src_db_file_name, dest_db_file_name )
    a_copier.copy_data(src_db_file_name,
                         dest_db_file_name,
                         table_name,
                         columns )


# --------------------
if __name__ == "__main__":

    # table_name     = "help_info"
    # do_copy( table_name )


    # for selection it may be in  WHERE system = :sys_val later may generalize some more
    table_name     = "help_text"
    table_name     = "help_info"
    do_copy( table_name )

# --------------------





