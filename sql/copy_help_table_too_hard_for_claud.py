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
from PyQt5.QtSql import QSqlQuery, QSqlDatabase
import traceback

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
    def __init__(self, src_db_name='source.db', dest_db_name='destination.db'):
        self.src_db_name    = src_db_name
        self.dest_db_name   = dest_db_name
        self.db_src         = self.get_db_connection( src_db_name,  "src_db_name" )
        self.db_dest        = self.get_db_connection( dest_db_name, "dest_db_name" )



    def get_db_connection(self, db_name, connection_name):
        """
        Helper to establish a Qt SQLite connection.
        """
        db = QSqlDatabase.addDatabase("QSQLITE", connection_name)
        db.setDatabaseName( db_name )
        if not db.open():
            # QSqlDatabase.lastError().text() provides detailed error info
            raise Exception(f"Failed to open database {db_name}: {db.lastError().text()}")
        return db


    def id_generator( self, table_name, where_clause="", batch_size=1000 ):
        """
        Generator that yields primary key IDs from a table in db_src.

        Args:
            db_src: QSqlDatabase - source database connection
            table_name: str - name of the table
            where_clause: str - optional WHERE clause (without the word WHERE)
            batch_size: int - number of IDs to fetch at once (for performance)

        Yields:
            int - next ID from the table
        """
        db_src    = self.db_src
        if not db_src.isOpen():
            raise ValueError("Source database is not open")

        # Ensure we have a valid table and build the query
        query_str = f"SELECT id FROM {table_name}"
        params = []


        query_str += " WHERE " + where_clause
        query_str += " ORDER BY id"  # Ensures consistent order

        query = QSqlQuery(db_src)

        # Use cursor-based fetching with batching
        offset = 0
        while True:
            batch_query = f"{query_str} LIMIT {batch_size} OFFSET {offset}"

            if not query.exec_(batch_query):
                raise RuntimeError(f"Query failed: {query.lastError().text()}")

            found = False
            while query.next():
                found = True
                yield query.value(0)  # assuming 'id' is the first column

            if not found:
                break  # no more rows

            offset += batch_size

            # Clear the query results to free resources
            query.finish()



    def copy_data_too_fancy_too_bad(self, ref_table_name, src_table_name, where_clause=""):
        """
        Copies data safely with ZERO duplicates and NO parameter mismatch.
        """
        db_src = self.db_src
        db_dst = self.db_dest

        if not db_src.isOpen() or not db_dst.isOpen():
            return "Error: Database not open."

        rows_copied = 0
        batch_commit_size = 1000

        try:
            COLUMNS = get_columns(src_table_name)  # Must return exact order as in table
            if not COLUMNS:
                return f"Error: No columns found for {src_table_name}"

            select_cols = ", ".join(COLUMNS)
            bind_placeholders = ", ".join([f":{col}" for col in COLUMNS])

            select_sql = f"""
                SELECT {select_cols}
                FROM {src_table_name}
                WHERE id = :id_src
            """

            # UPSERT: safe even if re-run
            update_cols = [col for col in COLUMNS if col.lower() != "id"]
            set_clause = ", ".join([f"{col} = excluded.{col}" for col in update_cols])
            insert_sql = f"""
                INSERT INTO {src_table_name} ({select_cols})
                VALUES ({bind_placeholders})
                ON CONFLICT(id) DO UPDATE SET {set_clause}
            """

            query_src = QSqlQuery(db_src)
            query_dst = QSqlQuery(db_dst)

            if not query_src.prepare(select_sql):
                return f"Prepare SELECT failed: {query_src.lastError().text()}"
            if not query_dst.prepare(insert_sql):
                return f"Prepare INSERT failed: {query_dst.lastError().text()}"

            db_dst.transaction()
            print(f"Copying {src_table_name} using IDs from {ref_table_name} | WHERE {where_clause or 'ALL'}")

            for id_val in self.id_generator(ref_table_name, where_clause, batch_size=500):
                print(f"Processing ID: {id_val}", end="")

                query_src.bindValue(":id_src", id_val)
                if not query_src.exec():
                    db_dst.rollback()
                    raise Exception(f"SELECT failed: {query_src.lastError().text()}")

                if not query_src.next():
                    print(" → skipped (not in source)")
                    continue

                # CRITICAL FIX: Use index, not name!
                for i, col_name in enumerate(COLUMNS):
                    value = query_src.value(i)  # ← This is safe and correct
                    query_dst.bindValue(f":{col_name}", value)

                if not query_dst.exec():
                    db_dst.rollback()
                    raise Exception(f"INSERT failed for ID {id_val}: {query_dst.lastError().text()}")

                query_dst.finish()  # Prevents reuse bugs
                rows_copied += 1
                print(f" → COPIED ({rows_copied})")

                if rows_copied % batch_commit_size == 0:
                    db_dst.commit()
                    print(f"   → COMMITTED {rows_copied} rows")
                    db_dst.transaction()

            db_dst.commit()
            print(f"\nCOPY COMPLETED: {rows_copied} rows inserted/updated")

            # Final count
            count_q = QSqlQuery(db_dst)
            count_q.exec(f"SELECT COUNT(*) FROM {src_table_name}")
            total = count_q.next() and count_q.value(0) or "?"
            print(f"Destination table now has {total} rows.")

            return f"SUCCESS: {rows_copied} rows copied."

        except Exception as e:
            db_dst.rollback()
            error = f"COPY FAILED at ID {id_val if 'id_val' in locals() else 'unknown'}:\n{str(e)}"
            print(error)
            return error


    def copy_data_chat_bad(self, ref_table_name, src_table_name, where_clause=""):
        """
        Safely copies rows from source DB to destination DB using ID generator.
        - One row per ID
        - Zero duplicates
        - Proper transactions
        - Full error handling
        - Progress feedback
        """
        db_src = self.db_src
        db_dst = self.db_dest

        if not db_src.isOpen() or not db_dst.isOpen():
            return "Error: One or both databases are not open."

        rows_copied = 0
        batch_commit_size = 1000  # Commit every N rows for speed + safety

        try:
            # Get column names dynamically (you said get_columns() exists)
            COLUMNS = get_columns(src_table_name)
            if not COLUMNS:
                return f"Error: Could not retrieve columns for table '{src_table_name}'"

            # Build SQL templates ONCE
            select_cols = ", ".join(COLUMNS)
            bind_placeholders = ", ".join([f":{col}" for col in COLUMNS])

            select_sql = f"""
                SELECT {select_cols}
                FROM {src_table_name}
                WHERE id = :id_src
            """

            # Use UPSERT to prevent duplicates even if re-run
            set_clause = ", ".join([f"{col} = excluded.{col}" for col in COLUMNS if col != "id"])
            insert_sql = f"""
                INSERT INTO {src_table_name} ({select_cols})
                VALUES ({bind_placeholders})
                ON CONFLICT(id) DO UPDATE SET {set_clause}
            """

            # Prepare queries once (reused safely)
            query_src = QSqlQuery(db_src)
            query_dst = QSqlQuery(db_dst)

            query_src.prepare(select_sql)
            query_dst.prepare(insert_sql)

            # Start transaction
            db_dst.transaction()
            print(f"Starting copy: {src_table_name} ← IDs from {ref_table_name} {where_clause or ''}")

            for id_val in self.id_generator(ref_table_name, where_clause, batch_size=500):
                print(f"Processing ID: {id_val}", end="")

                # Bind ID for SELECT
                query_src.bindValue(":id_src", id_val)

                if not query_src.exec():
                    db_dst.rollback()
                    raise Exception(f"SELECT failed for ID {id_val}: {query_src.lastError().text()}")

                if not query_src.next():
                    print(" → not found in source")
                    continue  # ID exists in ref but not in data table

                # Bind all column values for INSERT
                for col_name in COLUMNS:
                    value = query_src.value(col_name)
                    query_dst.bindValue(f":{col_name}", value)

                # Execute INSERT (exactly once!)
                if not query_dst.exec():
                    db_dst.rollback()
                    raise Exception(f"INSERT failed for ID {id_val}: {query_dst.lastError().text()}")

                # Critical: reset query state
                query_dst.finish()

                rows_copied += 1
                print(f" → copied ({rows_copied})")

                # Commit periodically
                if rows_copied % batch_commit_size == 0:
                    if not db_dst.commit():
                        raise Exception(f"Commit failed: {db_dst.lastError().text()}")
                    print(f"Committed {rows_copied} rows...")
                    db_dst.transaction()  # Restart transaction

            # Final commit
            if not db_dst.commit():
                raise Exception(f"Final commit failed: {db_dst.lastError().text()}")

            # Final count verification
            count_query = QSqlQuery(db_dst)
            count_query.exec(f"SELECT COUNT(*) FROM {src_table_name}")
            if count_query.next():
                total_in_dest = count_query.value(0)
            else:
                total_in_dest = "unknown"

            msg = (
                f"\nCOPY COMPLETED SUCCESSFULLY!\n"
                f"→ Copied: {rows_copied} rows\n"
                f"→ Table '{src_table_name}' now has {total_in_dest} total rows\n"
                f"→ Where clause: {where_clause or 'None'}\n"
            )
            print(msg)
            return msg

        except Exception as e:
            db_dst.rollback()
            error_msg = f"COPY FAILED at ID {id_val if 'id_val' in locals() else 'unknown'}:\n{e}\n{traceback.format_exc()}"
            print(error_msg)
            return error_msg


    def copy_data_buggy(self,  ref_table_name, src_table_name, where_clause  ):
        """
        Copies data from source to destination using QSqlQuery,
        named bind variables, and a WHERE clause.

        ref_table_name,
            get the id's'
        src_table_name
            get the data  and insert the data dest_table, not in code

        where_clause
            ex: "system = 'Linux' "

        """
        db_src      = self.db_src
        db_dst      = self.db_dest
        rows_copied = 0

        try:

            query_src   = QSqlQuery( db_src )
            query_dst   = QSqlQuery( db_dst )

            # COLUMNS = [
            #     "id", "id_old", "type", "sub_system", "system", "key_words",
            #     "add_ts", "edit_ts", "table_name", "column_name", "java_type",
            #     "java_name", "java_package", "title", "is_example", "can_execute"
            # ]

            COLUMNS =   get_columns( src_table_name )

            for id_val in self.id_generator(  ref_table_name, where_clause , batch_size=500 ):
                print(f"Processing user ID: {id_val}")

                # Create the named bind variable placeholders for the INSERT statement
                BIND_VARS = [f":{col}" for col in COLUMNS]
                # 2. SELECT data from source using a named bind variable in the WHERE clause
                select_cols = ", ".join(COLUMNS)
                select_sql = f"""
                    SELECT {select_cols}
                    FROM {src_table_name}
                    WHERE id = :id_src
                """

                # 3. Prepare the INSERT statement for the destination
                insert_sql = f"""
                    INSERT INTO {src_table_name} ({select_cols})
                    VALUES ({", ".join(BIND_VARS)})
                """
                db_dst.transaction()

                query_src.prepare( select_sql  )

                # Bind the value for the WHERE clause
                query_src.bindValue( ":id_src", id_val )

        #     # Start transaction on destination for performance and atomicity
                if not query_src.exec():
                    raise Exception(f"Source SELECT failed: {query_src.lastError().text()}")

                query_dst.prepare( insert_sql )

        #     # 4. Iterate results and INSERT into destination
                while query_src.next():
                    value_list   = []
                    # Retrieve values and bind them to the INSERT query using the column names
                    for i, col_name in enumerate(COLUMNS):
                        value = query_src.value(i)
                        value_list.append( value )

                        # Bind the value using the named placeholder, e.g., ":id"
                        query_dst.bindValue(f":{col_name}", value)

                        if not query_dst.exec():
                            db_dst.rollback() # Rollback on error
                            raise Exception(f"Destination INSERT failed (Row {rows_copied + 1}): {query_dst.lastError().text()}")
                        query_dst.finish()
                    print( value_list )
                    rows_copied += 1


                db_dst.commit()

            # 6. Verification
            count_query = QSqlQuery(db_dst)
            count_query.exec( f"SELECT COUNT(*) FROM {src_table_name}")
            count_query.next()
            total_rows = count_query.value(0)

            msg  = (
                f"Copy completed successfully! {rows_copied} rows copied.\n"
                f"Destination table 'help_info' now has {total_rows} total rows."
            )
            print( msg )
        except Exception as e:
            return f"Operation FAILED: {e}"

        # finally:
        #     # 7. Clean up connections
        #     if db_src and db_src.isOpen():
        #         db_src.close()
        #     if db_dst and db_dst.isOpen():
        #         db_dst.close()
        #     # Crucial for managing multiple connections: remove the connection objects
        #     QSqlDatabase.removeDatabase("src_db")
        #     QSqlDatabase.removeDatabase("dest_db")
        msg    = (f"{rows_copied = }  ")
        print( msg )

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

def do_copyxxx(table_name ):

    a_parms_temp            = parms_temp.ParmsTemp()

    src_db_file_name        = parameters.PARAMETERS.db_file_name
    dest_db_file_name       = a_parms_temp.db_file_name

    columns                 = get_columns( table_name )

    a_copier                = copy_help_table.TableCopier( src_db_file_name, dest_db_file_name )
    a_copier.copy_data(src_db_file_name,
                         dest_db_file_name,
                         table_name,
                         columns )



def test_copy_text():
    """
    table needs to exist
        /mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/sql/create_help_db.py


    """

    a_parms_temp            = parms_temp.ParmsTemp()
    src_db_file_name        = parameters.PARAMETERS.db_file_name
    dest_db_file_name       = a_parms_temp.db_file_name
    ref_table_name          = "help_info"
    src_table_name          = "help_text"
    where_clause            = "system = 'Linux' "


    a_table_copier      = TableCopier( src_db_name= src_db_file_name, dest_db_name=dest_db_file_name )
    a_table_copier.copy_data( ref_table_name = ref_table_name, src_table_name = src_table_name, where_clause = where_clause )


def test_copy_info():
    """
    table needs to exist
        /mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/sql/create_help_db.py


    """

    a_parms_temp            = parms_temp.ParmsTemp()
    src_db_file_name        = parameters.PARAMETERS.db_file_name
    dest_db_file_name       = a_parms_temp.db_file_name
    ref_table_name          = "help_info"
    src_table_name          = "help_info"
    where_clause            = "system = 'Linux' "


    a_table_copier      = TableCopier( src_db_name= src_db_file_name, dest_db_name=dest_db_file_name )
    a_table_copier.copy_data( ref_table_name = ref_table_name, src_table_name = src_table_name, where_clause = where_clause )



def test_gen():
    """just test the generator function  """

    a_parms_temp            = parms_temp.ParmsTemp()
    src_db_file_name        = parameters.PARAMETERS.db_file_name
    dest_db_file_name       = a_parms_temp.db_file_name
    table_name              = "help_info"


    a_table_copier      = TableCopier( src_db_name= src_db_file_name, dest_db_name=dest_db_file_name )

    ix_count   = 0
    for id_val in a_table_copier.id_generator(  "help_info", "system = 'Linux' " , batch_size=500 ):
        print(f"test_gen user ID: {id_val}")
        # Do something with the ID using db_dest if needed
        ix_count += 1
    print( f"{ix_count = }" )

# ---- if name
# --------------------
if __name__ == "__main__":

    # table_name     = "help_info"
    # do_copy( table_name )


    # # for selection it may be in  WHERE system = :sys_val later may generalize some more
    # table_name     = "help_text"
    # table_name     = "help_info"
    #test_gen()

    test_copy_info()
    #test_copy_text()
# --------------------





