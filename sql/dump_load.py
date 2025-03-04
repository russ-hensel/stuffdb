#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 07:58:59 2025

@author: russ
"""


# ---- tof

# ---- imports
import sqlite3
import sys
# ---- end imports


#-------------------------------


def load_table_from_sql( db_name, input_file ):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Read SQL from file
        with open(input_file, 'r', encoding='utf-8') as file:
            sql_script = file.read()

        # Execute SQL script
        cursor.executescript(sql_script)
        conn.commit()

        print(f"Data from '{input_file}' has been imported into the database '{db_name}'.")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if conn:
            conn.close()

# if __name__ == "__main__":
#     if len(sys.argv) != 3:
#         print("Usage: python read_table.py <db_name> <input_file>")
#     else:
#         read_table_from_sql(sys.argv[1], sys.argv[2])



def dump_table_to_sql( db_name, table_name, output_file ):
    """
    from chat, tweaked
    consider a where id > .....
    """
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Check if the table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if not cursor.fetchone():
            print(f"Error: Table '{table_name}' does not exist in the database.")
            return

        with open(output_file, 'w', encoding='utf-8') as file:
            # Dump CREATE TABLE statement
            cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            create_table_sql = cursor.fetchone()[0]
            file.write(f"{create_table_sql};\n\n")

            # Dump INSERT statements
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]

            for row in rows:
                values = ', '.join(f"'{str(value).replace('\'', '\'\'')}'" if value is not None else "NULL" for value in row)
                insert_sql = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({values});"
                file.write(f"{insert_sql}\n")

        print(f"Table '{table_name}' has been dumped to '{output_file}'.")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if conn:
            conn.close()

# if __name__ == "__main__":
#     if len(sys.argv) != 4:
#         print("Usage: python dump_table.py <db_name> <table_name> <output_file>")
#     else:
#         dump_table_to_sql(sys.argv[1], sys.argv[2], sys.argv[3])


# ---- run from here

db_name          =   "test_db.db"
table_name       =   "help_info"
dump_file_name   =  "./db_dump.txt"

dump_table_to_sql( db_name, table_name,  dump_file_name  )

# print( "beware load follows ")

# load_table_from_sql( db_name, dump_file_name )


# ---- eof