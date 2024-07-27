#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 08:38:46 2024

@author: russ


import db_create
db_create.create_table_stuff( db )
/mnt/WIN_D/Russ/0000/python00/python3/_projects/stuff_db_qt/db_create.py

see in backup
      /mnt/WIN_D/Russ/0000/python00/python3/_projects/stuff_db_qt/stuffdb_def.py

"""

# ---- to main

# # --------------------
# if __name__ == "__main__":
#     import main
#     main.main()
# # --------------------



# ---- imports
import sys
sys.path.insert( 1, "../rshlib" )
sys.path.insert( 1, "./ex_qt" )
sys.path.insert( 1, ".//mnt/WIN_D/Russ/0000/python00/python3/_examples/" )
sys.path.insert( 1, ".//mnt/WIN_D/Russ/0000/python00/python3/_examples/qt" )


from PyQt5.QtSql import QSqlDatabase, QSqlQuery

import ia_qt


def create_connection():
    """

    Returns:
        TYPE: DESCRIPTION.

    """
    db_fn           = "/mnt/WIN_D/Russ/0000/python00/python3/_projects/stuff_db_qt/data/appdb.db"
    print( f"using {db_fn =}" )

    db = QSqlDatabase.addDatabase("QSQLITE")  # or another appropriate database driver
    db.setDatabaseName(db_fn )

    if not db.open():
        print("Unable to open database")
        1/0
        return False
    return db

def querry_ok( what, query, db ):
    """

    Args:
        what (TYPE): DESCRIPTION.
        query (TYPE): DESCRIPTION.
        db (TYPE): DESCRIPTION.

    Returns:
        None.

    """

    if query.lastError().isValid():
        ok = False
        print("Error:", query.lastError().text())
    else:
        ok = False
        print("Table created successfully")

    db.commit()

    print(  f"{what} table created??" )
    return ok

def create_table_key_gen( db ):


    query = QSqlQuery()
    # Create the key_gen table if it doesn't exist
    query.exec("""
        CREATE TABLE IF NOT EXISTS key_gen (
            table_name VARCHAR(30) PRIMARY KEY UNIQUE NOT NULL,
            key_value INTEGER
        )
    """)

# ---- stuff --------------------------
def create_table_stuff( db ):
    """
    what it says
    seems not to work but sql ok in browser

    Args:
        db (TYPE): DESCRIPTION.

    Returns:
        None.

    """
    print( "create_table_stuff add transaction ?? **")
    db.transaction()
    query = QSqlQuery( db )

    query.exec("""
        CREATE TABLE IF NOT EXISTS stuff (
            id          INTEGER PRIMARY KEY  UNIQUE NOT NULL,
            add_kw      VARCHAR(50),
            descr       VARCHAR(60),
            type        VARCHAR(20),
            type_sub    VARCHAR(20),
            author      VARCHAR(40),
            publish     VARCHAR(40),
            model       VARCHAR(40),
            serial_no   VARCHAR(40),
            value       DECMIAL,
            project     VARCHAR(40),
            file        VARCHAR(40),
            owner       VARCHAR(40),
            start_ix     VARCHAR(20),
            end_ix      VARCHAR(20),
            sign_out     VARCHAR(40),
            format     VARCHAR(40),
            inv_id     VARCHAR(40),
            cmnt        VARCHAR(250),
            status     VARCHAR(15),
            in_id       VARCHAR(15),
            dt_item     VARCHAR(40),
            # c_name
            # preformer
            # cont_type
            # url
            # author_f
            # title
            # name
            # loc_add_info
            manafuct    VARCHAR(40),
            add_ts      INTEGER,
            edit_ts      INTEGER

        )
    """)

    last_error    = query.lastError()
    print( f"create_table_stuff {last_error} = " )

    db.commit()

    print( "stuff table created??")

#--------------
def create_table_stuff_text( db ):
    """
    what it says
    seems not to work but sql ok in browser

    Args:
        db (TYPE): DESCRIPTION.

    Returns:
        None.

        Note that numeric arguments in parentheses that following the type name (ex: "VARCHAR(255)")

    """
    print( "create_table_stuff add transaction ?? **")
    db.transaction()
    query = QSqlQuery( db )

    query.exec("""
        CREATE TABLE IF NOT EXISTS stuff_text (
            id          INTEGER PRIMARY KEY  UNIQUE NOT NULL,
            text_data   TEXT

        )
    """)

    last_error    = query.lastError ()
    print( f"create_table_stuff_text {last_error} = " )
    ia_qt.q_sql_error( last_error,
                       msg =  "now in code at: create_table_stuff_text ",

                       print_it = True,
                       include_dir = False,    # default False
                       )
    db.commit()

    print( "stuf_textf table created??")

# -------------------------------
def insert_stuff_text( db  ):
    query = QSqlQuery()
    queries = [
        # recheck match to stuff
        'INSERT INTO stuff_text  VALUES (  27,   "text for id  =27 and some more \ntext on next line "   )',
        'INSERT INTO stuff_text  VALUES (   28,   "text for id  =28 and some more \ntext on next line "   )',
        'INSERT INTO stuff_text  VALUES (   29,   "text for id  =28 and some more \ntext on next line "   )',
        'INSERT INTO stuff_text  VALUES (   30,   "text for id  =28 and some more \ntext on next line "   )',
        # 'INSERT INTO photo_text  VALUES (  49,   "text for id  =2*29 and some more \ntext on next line "   )',
        # 'INSERT INTO photo_text  VALUES (  999,   "text for id  =999 and some more \ntext on next line "   )',

        # 'INSERT INTO stuff_event  VALUES (  2001, 28, "comment for 2001", 80000, -99, "test", 0 )',
        # 'INSERT INTO stuff_event  VALUES (  2002, 28, "comment for 2002",80000,  -99, "test", 0 )',
        # 'INSERT INTO stuff_event  VALUES (  2003, 28, "comment for 2003",80000,  -99, "test", 0 )',
        # 'INSERT INTO stuff_event  VALUES (  2004, 28, "comment for 2004", 80000, -99, "test", 0 )',

    ]
    for sql in queries:
        if not query.exec_(sql):
            print(f"Query failed: {query.lastError().text()}")
            print(f"Query was: {sql}")


# -------------------------------
def insert_stuff_events( db  ):
    query = QSqlQuery()
    queries = [

        'INSERT INTO stuff_event  VALUES (  2001, 28, "comment for 2001", 80000, -99, "test", 0 )',
        'INSERT INTO stuff_event  VALUES (  2002, 28, "comment for 2002",80000,  -99, "test", 0 )',
        'INSERT INTO stuff_event  VALUES (  2003, 28, "comment for 2003",80000,  -99, "test", 0 )',
        'INSERT INTO stuff_event  VALUES (  2004, 28, "comment for 2004", 80000, -99, "test", 0 )',

    ]
    for sql in queries:
        if not query.exec_(sql):
            print(f"Query failed: {query.lastError().text()}")
            print(f"Query was: {sql}")

# ---- help -------------------------------
"""
CREATE TABLE help_info (
            id              INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            title           VARCHAR( 150 ),
            key_words       VARCHAR( 100 )
        )
"""
# -------------------------------
def insert_help_info( db  ):
    query = QSqlQuery()
    queries = [
        # recheck match to stuff
        'INSERT  INTO help_info  VALUES (   5000,   "this is a title 5000 ", "5000 key words"   )',
        'INSERT  INTO help_info  VALUES (   5001,   "this is a title 5001 ", "5001 key words"   )',
        'INSERT  INTO help_info  VALUES (   5002,   "this is a title 5002 ", "5002 key words"   )',
    ]
    for sql in queries:
        if not query.exec_(sql):
            print(f"Query failed: {query.lastError().text()}")
            print(f"Query was: {sql}")



#--------------
def create_table_help_text( db ):
    """
    what it says


    """
    print( "create_table_help_text add transaction ?? **")
    db.transaction()
    query = QSqlQuery( db )

    query.exec("""
        CREATE TABLE IF NOT EXISTS help_text (
            id          INTEGER PRIMARY KEY  UNIQUE NOT NULL,
            text_data   TEXT

        )
    """)

    last_error    = query.lastError ()
    print( f"create_table_help_text {last_error} = " )
    ia_qt.q_sql_error( last_error,
                       msg =  "now in code at: create_table_stuff_text ",

                       print_it = True,
                       include_dir = False,    # default False
                       )
    db.commit()

    print( "create_table_help_text table created??")

# -------------------------------
def insert_help_text( db  ):
    query = QSqlQuery()
    queries = [
        # recheck match to stuff

        'INSERT INTO help_text  VALUES (   5000,   "text for id  =5 000 and some more \ntext on next line "   )',
        'INSERT INTO help_text  VALUES (   5001,   "text for id  =5 000 and some more \ntext on next line "   )',
        'INSERT INTO help_text  VALUES (   5002,   "text for id  =5 000 and some more \ntext on next line "   )',
        # 'INSERT INTO photo_text  VALUES (  49,   "text for id  =2*29 and some more \ntext on next line "   )',
        # 'INSERT INTO photo_text  VALUES (  999,   "text for id  =999 and some more \ntext on next line "   )',

        # 'INSERT INTO stuff_event  VALUES (  2001, 28, "comment for 2001", 80000, -99, "test", 0 )',
        # 'INSERT INTO stuff_event  VALUES (  2002, 28, "comment for 2002",80000,  -99, "test", 0 )',
        # 'INSERT INTO stuff_event  VALUES (  2003, 28, "comment for 2003",80000,  -99, "test", 0 )',
        # 'INSERT INTO stuff_event  VALUES (  2004, 28, "comment for 2004", 80000, -99, "test", 0 )',

    ]
    for sql in queries:
        if not query.exec_(sql):
            print(f"Query failed: {query.lastError().text()}")
            print(f"Query was: {sql}")






# -------------------------------
def create_table_photo( db ):
    """
    what it says

    Args:
        db (TYPE): DESCRIPTION.

    """
    print( "create_table_photo  ")
    what    = "create_table_photo"
    db.transaction()
    query = QSqlQuery( db )

    query.exec("""
        CREATE TABLE IF NOT EXISTS photo (
            id          INTEGER PRIMARY KEY  UNIQUE NOT NULL,
            add_kw      VARCHAR(50),
            name        VARCHAR(60),
            descr       VARCHAR(60),
            photo_fn    VARCHAR(60),
            photo_ts    INTEGER,
            url         VARCHAR(60),
            title       VARCHAR(60),
            camera      VARCHAR(40),
            add_ts      INTEGER,
            edit_ts     INTEGER,
            no_comma    INTEGER

        )
    """)

    last_error    = query.lastError()
    print( f"{what} {last_error} = " )

    db.commit()

    print(  f"{what} table created??" )

def create_table_photo_text( db ):
    """
    what it says

        Note that numeric arguments in parentheses that following the type name (ex: "VARCHAR(255)")

    """
    what    = "create_table_photo_text"
    print( "create_table_photo_text add transaction ?? **")
    db.transaction()
    query = QSqlQuery( db )

    query.exec("""
        CREATE TABLE IF NOT EXISTS photo_text (
            id          INTEGER PRIMARY KEY  UNIQUE NOT NULL,
            text_data   TEXT

        )
    """)

    last_error    = query.lastError ()
    print( f"create_table_photo_text {last_error} = " )
    ia_qt.q_sql_error( last_error,
                       msg =  "now in code at: create_table_photo_text ",

                       print_it    = True,
                       include_dir = False,    # default False
                       )
    db.commit()

    print(  f"{what} table created??" )


# -------------------------------
def insert_photo_text( db  ):
    query = QSqlQuery()
    queries = [

        'INSERT INTO photo_text  VALUES (  29,   "text for id  =29 and some more \ntext on next line "   )',
         'INSERT INTO photo_text  VALUES (  39,   "text for id  =39 and some more \ntext on next line "   )',
         'INSERT INTO photo_text  VALUES (  49,   "text for id  =2*29 and some more \ntext on next line "   )',
         'INSERT INTO photo_text  VALUES (  999,   "text for id  =999 and some more \ntext on next line "   )',


    ]
    for sql in queries:
        if not query.exec_(sql):
            print(f"Query failed: {query.lastError().text()}")
            print(f"Query was: {sql}")





def create_table_photoshow( db ):
    """
    what it says

    Args:
        db (TYPE): DESCRIPTION.

    """

    what    = "create_table_photoshow"
    print(  f"{what = }")
    db.transaction()
    query = QSqlQuery( db )

    query.exec("""
        CREATE TABLE IF NOT EXISTS photoshow (
            id          INTEGER PRIMARY KEY  UNIQUE NOT NULL,
            name        VARCHAR(60),
            cmnt        VARCHAR(60),
            add_kw      VARCHAR(60),
            start_ts    INTEGER,
            end_ts      INTEGER,
            descr       VARCHAR(60),
            add_ts      INTEGER,
            edit_ts     INTEGER,
            no_comma    INTEGER

        )
    """)

    last_error    = query.lastError()
    print( f"{what} {last_error} = " )

    if query.lastError().isValid():
           print("Error:", query.lastError().text())
    else:
           print("Table created successfully")

    db.commit()

    print(  f"{what} table created??" )


def create_table_photoshow_photo( db ):
    """
    what it says

    Args:
        db (TYPE): DESCRIPTION.

    """

    what    = "create_table_photoshow_photo"
    print(  f"{what = }")
    db.transaction()
    query = QSqlQuery( db )

    query.exec("""
        CREATE TABLE IF NOT EXISTS photoshow_photo (
            id              INTEGER PRIMARY KEY  UNIQUE NOT NULL,
            photoshow_id    INTEGER,
            photo_id        INTEGER,
            seq_no          INTEGER,
            no_comma        INTEGER

        )
    """)

    # last_error    = query.lastError()
    # print( f"{what} {last_error} = " )

    if query.lastError().isValid():
           print("Error:", query.lastError().text())
    else:
           print("Table created successfully")

    db.commit()

    print(  f"{what} table created??" )

# -------------------------------
def create_table_stuff_event( db ):
    """
    what it says

    Args:
        db (TYPE): DESCRIPTION.

    """
    what    = "create_stuff_event"
    print(  f"{what = }")
    db.transaction()
    query = QSqlQuery( db )

    query.exec("""
        CREATE TABLE IF NOT EXISTS stuff_event (
            id              INTEGER PRIMARY KEY  UNIQUE NOT NULL,
            stuff_id        INTEGER,
            cmnt            VARCHAR(100),
            event_ts        INTEGER,
            dlr             INTEGER,
            type            VARCHAR(20),
            no_comma        INTEGER

        )
    """)

    querry_ok( what, query, db )



def setup_databasexxx(self):
    query = QSqlQuery()
    queries = [
        """CREATE TABLE photo (
            id INTEGER PRIMARY KEY,
            name TEXT,
            photo_fn TEXT
        )""",
        """CREATE TABLE photoshow (
            id INTEGER PRIMARY KEY,
            name TEXT
        )""",
        """CREATE TABLE photoshow_photo (
            photoshow_id INTEGER,
            photo_id INTEGER,
            FOREIGN KEY(photoshow_id) REFERENCES photoshow(id),
            FOREIGN KEY(photo_id) REFERENCES photo(id)
        )""",
        "INSERT INTO photo VALUES (1, 'Photo 1', 'photo1.jpg')",
        "INSERT INTO photo VALUES (2, 'Photo 2', 'photo2.jpg')",
        "INSERT INTO photoshow VALUES (1, 'Show 1')",
        "INSERT INTO photoshow_photo VALUES (1, 1)",
        "INSERT INTO photoshow_photo VALUES (1, 2)"
    ]
    for sql in queries:
        if not query.exec_(sql):
            print(f"Query failed: {query.lastError().text()}")
            print(f"Query was: {sql}")

# ---- run manually --------------------------

print( "running manually ---------- disconnect other stuff please  ---------")

#create_table_photo_text( db = create_connection() )
#create_table_photo( db = create_connection() )
# insert_photo_text( db = create_connection()  )

#create_table_photoshow( db = create_connection() )
#create_table_photoshow_photo( db = create_connection() )


# create_table_stuff_event( db = create_connection() )
# insert_stuff_events( db = create_connection()  )
#insert_stuff_text( db = create_connection()  )

# ---- help
# insert_help_info( db = create_connection()  )

# create_table_help_text( db = create_connection()  )

insert_help_text( db = create_connection()  )




print( "ran manually -------------------------------------------------")


