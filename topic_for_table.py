#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  2 07:34:28 2025

so this needs to be in a global place, lets put in midi management ??
/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/topic_for_table.py

"""


# ---- tof

# ---- imports

from    PyQt5.QtSql import QSqlQuery, QSqlError

from collections import defaultdict
# --------------------
if __name__ == "__main__":   # for testing
    import adjust_path


import  data_dict

# ---- end imports

class TopicDict():


    def __init__( self, db,   ):
        """
        this caches what is in the data dict
        should only need one per table

        """
        self.db                      = db
        self.topic_for_table_dict    = defaultdict( lambda: None )

    def get_topic_string( self, table_name, a_id ):
        """
        what it says, read

        """
        a_topic_for_table     = self.topic_for_table_dict[ table_name ]
        if not a_topic_for_table:
            a_topic_for_table     = TopicForTable( self.db, table_name )
            self.topic_for_table_dict[ table_name ] = a_topic_for_table


        topic_string = a_topic_for_table.get_topic_string( a_id )

        return topic_string


#-------------------------------
class TopicForTable():

    def __init__( self, db, table_name ):
        """


        """
        # data_dict.build_it() should have been built by now
        self.db     = db
        a_table     = data_dict.DATA_DICT.get_table( table_name )

        # msg        = a_table.to_sql_create()
        self.table_name     = table_name

        # msg        = a_table.sql_to_insert_bind()
        self.topic_columns  = a_table.get_topic_columns()
        #msg        = a_table.get_key_word_columns()

        column_str      = ", ".join( self.topic_columns )
        self.sql        = f"SELECT {column_str} FROM {self.table_name} WHERE id = :id"


    def get_topic_string( self, a_id ):
        """
        in a python object
        i hava a table name

        """
        query   = QSqlQuery( self.db )
        if not query.prepare( self.sql ):
            raise RuntimeError(f"Failed to prepare query: {query.lastError().text()}")

        # Bind the id value
        query.bindValue(":id", a_id)

        # Execute
        if not query.exec():
            raise RuntimeError(f"Query execution failed: {query.lastError().text()}")

        # Fetch result
        if not query.next():
            return None  # No row found for that id

        # Extract values in order of column_list
        values = {}
        for ix, col in enumerate( self.topic_columns ):
            values[col]  = query.value(ix)
        topic_string   = " ".join( values.values() )

        return topic_string

# --------------------
if __name__ == "__main__":

    import adjust_path
    import stuff_util_sql as su

    # ---- get ready
    db        = su.create_connection( use_temp = True  )
    data_dict.build_it()


    # ---- with TopicForTable
    a_tft     = TopicForTable( db, "stuff"  )


    a_id      = 3096 # kabota
    topic_string           = a_tft.get_topic_string( a_id )
    # topic_list      = [ i_value for i_value in topic.values()]
    # topic_string    = " ".join( topic_list )
    # print( topic )
    print( topic_string )

    # ---- with a topic dict
    a_topic_dict    = TopicDict( db )
    topic_string    = a_topic_dict.get_topic_string( "stuff", a_id )
    print( topic_string )

    topic_string    = a_topic_dict.get_topic_string( "stuff", a_id )
    print( topic_string )

# ---- eof