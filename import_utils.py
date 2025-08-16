# -*- coding: utf-8 -*-
#>>>>>python example for file read write -- and some file info
# snipfile_ok>> python example file operations  ex_file.py

"""
What:

utilities that suppor the  imports


"""
# ---- search --------------
"""


Search for the following in the code below:


"""

# ---- Imports


import os
import pprint
import shutil

import stat
import time
import traceback
#import datetime
from datetime import datetime
from pathlib import Path




"""



"""

# ---- constants
SINGLE_QUOTE            = "'"
DOUBLE_QUOTE            = '"'
DOUBLE_SINGLE_QUOTE     = DOUBLE_QUOTE + SINGLE_QUOTE
SINGLE_DOUBLE_QUOTE     = SINGLE_QUOTE + DOUBLE_QUOTE
# TO_SPACES               = ""
TAB                     = "\t"
COMMA                   = ","

#------------------------------
def string_to_int( num_string ):
    """
     because of blanks
     import_utils.string_to_int(    )
    """
    if ( num_string == "") or num_string is None:
        return 0
    else:
        return int( num_string )


def string_to_ts_tenths( date_string, ):
        """
        have tenths of sec think can go even farther
        string to fraction
        """
        return string_to_timestamp( date_string, "%Y/%m/%d %H:%M:%S.%f" )

def string_to_ts_sec( date_string, ):
        """
        just to seconds
        """
        return string_to_timestamp( date_string, "%Y/%m/%d %H:%M:%S" )

def string_to_ts_min( date_string, ):
        """
        just to minutes
        """
        return string_to_timestamp( date_string, "%Y/%m/%d %H:%M" )

#------------------------------
def string_to_timestamp( date_string, date_format ):
    """
    chat told me how
        Using python how can i convert a string like "1997/02/13 14:05:51.370000" to a
        linux time ( an integer )
        may except
    """
    # return time.time  # if problem on None
    if  ( date_string == "" ) or date_string is None:
        return None   # for binding to Null
    try:

        # The datetime string
        #date_string = "1997/02/13 14:05:51.370000"

        # Define the format of the string
        # date_format     = "%Y/%m/%d %H:%M:%S.%f"

        # Convert the string into a datetime object
        dt_object       = datetime.strptime(date_string, date_format)

        # Convert the datetime object to a Unix timestamp
        unix_timestamp = int(dt_object.timestamp())

        #rint("string_to_timestamp", unix_timestamp)

    except Exception as an_except:   #  or( E1, E2 )

        msg     = f"string_to_timestamp a_except    >>{date_string = }<<"
        print( msg )

        msg     = f"a_except         >>{an_except}<<  type  >>{type( an_except)}<<"
        print( msg )

        msg     = f"an_except.args   >>{an_except.args}<<"
        print( msg )

        s_trace = traceback.format_exc()
        msg     = f"format-exc       >>{s_trace}<<"
        print( msg )

        raise

    # finally:
    #     msg     = f"in finally  {1}"
    #     print( msg )


    return unix_timestamp

#------------------------------
def no_quotes( a_string ):
    """
    remove undesired leading and trailing quotes
    """
    if   a_string.startswith( DOUBLE_SINGLE_QUOTE  ):
        a_string    = a_string[ 2: ]
    elif  a_string.startswith(  SINGLE_QUOTE ) or  a_string.startswith(  DOUBLE_QUOTE )  :
        a_string    = a_string[ 1: ]

    if   a_string.endswith( DOUBLE_SINGLE_QUOTE  ):
        a_string    = a_string[ : -2 ]
    elif  a_string.endswith(  SINGLE_QUOTE ) or  a_string.endswith(  DOUBLE_QUOTE )  :
        a_string    = a_string[ : -1 ]

    a_string  = a_string.strip( )

    return a_string

#------------------------------
def remove_escape( a_string ):
    """
    chat told me how
    remove ' at ends?? as well  -- remove trailing blanks '
    """
    converted_string = a_string.encode().decode('unicode_escape')
    return converted_string

#------------------------------
def get_new_key ( query, sql, id_old ):
    """
    chat told me how
        query with conncectin see comment
         return new key or None

    query     =  QSqlQuery( db_create.DB_CONNECTION )
    sql       =   "SELECT id FROM help_info WHERE id_old = :id_old"
    id_old    = "joe"
    import_utils.get_new_key( query = query, sql = sql, id_old = id_old )
            query           =  QSqlQuery( db_create.DB_CONNECTION )
            sql             = "SELECT id FROM planting WHERE id_old = :id_old"

            planting_id     = import_utils.get_new_key( query = query, sql = sql, id_old = planting_id_old )



    """


    # Assuming db_create.DB_CONNECTION is your database connection
    #query = QSqlQuery( db_create.DB_CONNECTION )

    # Prepare the SQL statement
    # sql = "SELECT id FROM help_info WHERE id_old = :id_old"

    query.prepare( sql )
    #ia_qt.q_sql_query( query )

    # Bind the id_old value (replace 'some_old_id' with the actual id_old you're looking for)
    #old_id  = 'old_id'
    query.bindValue(":id_old", id_old )
    #print( "fix ia_qt.q_sql_query( query )" )
    # Execute the query
    if not query.exec_():
        print(f"Query failed: {query.lastError().text()}")
        1/0
    else:
        # Check if there are any results
        if query.next():
            # Get the value of the 'id' column
            id_value = query.value(0)
            print(f"ID corresponding to id_old '{id_old}': {id_value}")
        else:
            print(f"No record found with id_old = {id_old}")
            id_value  = None

    return id_value

#------------------------------------------
def split_line( a_string ):
    """
    so we can easily set se split_dat_line

    """
    return a_string.split(  ","  )

#------------------------------------------
def split_dat_line( a_string ):
    """
    similar version in ex_csv, may need to add some tests here
    another idea that may be equ is to change ", " into ": "
            parsed_list.append(  pending )
     import_utils.split_dat_line

    """
    parsed_list    = []
    the_rest       = a_string
    pending        = ""
    while len( the_rest ) > 0:

        splits    = the_rest.split( ",", 1 )
        if len( splits ) <  2:
            print( "len <2")
            parsed_list.append(  pending )
            break
        #print( splits )
        #if len( splits ) == 0
        the_rest        = splits[1]
        if the_rest.startswith( SINGLE_QUOTE ) or the_rest.startswith( "," ) :

            pending      = pending + splits[0]
            parsed_list.append(  pending )
            pending      = ""
            #parsed_list.append( splits[1])

        elif the_rest.startswith( " "):

            pending  = splits[0]

        else:
            pending      = pending + splits[0]
            parsed_list.append(  pending )
            pending      = ""
            #parsed_list.append( splits[1])


        if len( parsed_list ) > 16 :
            print( f"{len( parsed_list) =}")
            break

    return parsed_list

#====================================
class ComaToTab(  ):
    """
    read in comma sep file write out a tab sep file, perhaps a bit of conversion
    """
    #----------- init -----------
    def __init__(self, file_name_src, file_name_dest  ):     # expand the init to set more stuff is this a TableInfo
        file_src        = open( file_name_src,    'r', encoding = "utf8", errors = 'ignore' )
        file_dest       = open( file_name_dest, 'w', encoding = "utf8", errors = 'ignore' )

        for ix_line, i_line in enumerate( file_src ) :
            i_input_line     = i_line
            i_line_issue     = i_line
            ix_line_issue    = ix_line
            try:
                # print( f"importing line >>>>>{ix_line}")
                #i_line     = i_line.rstrip('\n')
                i_line     = i_line.replace( "\96", "'" )  # grave aacent
                i_line     = i_line.replace( "\92", "/" )  #  backslash
                i_line     = i_line.replace( COMMA, TAB  )  #
                file_dest.write( i_line )
            except:
                msg    = ( f"exception at line {ix_line}")
                print( msg )
                msg    = ( f"\n{i_input_line}\n\n")
                print( msg )
        msg     = ( f"line count {ix_line =}")
        print( msg )
        msg     = ( ">>>>>>>>>>>>>>all done<<<<<<<<<<<<<<<<<<")
        print( msg )

# ---- run standalone from here
# --------------------
if __name__ == "__main__":
    file_name_src     = "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/import_old_sfuff/help_info/help_info.dat"
    file_name_dest    = "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/import_old_sfuff/help_info/help_info_tab.csv"
    a_comma_to_tab    = ComaToTab( file_name_src, file_name_dest )




# ---- eof -----------------------------------------------