#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 17:59:43 2024

@author: russ

import convert_db_display.py
convert_db_display.convert_from_to( )
"""


from datetime import datetime

from PyQt5 import QtGui
from PyQt5.QtCore import QDate, QDateTime, QModelIndex, Qt, QTimer
from PyQt5.QtGui import QTextCursor
# sql
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
# widgets biger
# widgets -- small
# layouts
from PyQt5.QtWidgets import (QAction,
                             QApplication,
                             QButtonGroup,
                             QCheckBox,
                             QComboBox,
                             QDateEdit,
                             QGridLayout,
                             QGroupBox,
                             QHBoxLayout,
                             QLabel,
                             QLineEdit,
                             QListWidget,
                             QListWidgetItem,
                             QMainWindow,
                             QMenu,
                             QMessageBox,
                             QPushButton,
                             QRadioButton,
                             QSizePolicy,
                             QTableView,
                             QTableWidget,
                             QTableWidgetItem,
                             QTabWidget,
                             QTextEdit,
                             QVBoxLayout,
                             QWidget)

# ---- imports
import adjust_path

# ---- imports neq qt


def string_to( a_string, a_type ):
    """
    """
    if  not isinstance( a_string, str ):
        raise ValueError( f"a_string is not instnace of str  {a_string = } {type(a_string) = }" )

    if a_type  in  ( "int", "integer" ):   # looks like int here was a mistake, change to enum??
        a_int  = int( a_string )
        return a_int

    if a_type   == "string":
        # should this not have been caught earlier >
        return a_string

    else:
        raise ValueError( f"string_to Unsupported type {a_type = } {a_string = }")

# -------------------------------------
def int_to(   a_int, a_type  ):
    """
    """
    if  not isinstance( a_int, int ):
        raise ValueError( f"a_int is not instnace of int  {a_int = } {type(a_int) = }" )

    if   a_type == "string":
        """ convert from a int to a python string """
        if  not isinstance( a_int, int):
            raise ValueError( f"a_int is not instnace of QDate {a_int = } {type(a_int) = }" )

        a_string  = str( a_int )


def to_datetime( data, a_type ):
    """
    return
        a python datetiem
    """
    if   a_type == "qdate":
        """ convert from a qdate to a python datetime """
        if  not isinstance( data, QDate):
            raise ValueError( f"Data is not instnace of QDate {data = } {type(data) = }" )
        qdate        = data
        py_datetime  = datetime( qdate.year(), qdate.month(), qdate.day())

    elif   a_type == "qdatetime":
        """ convert from a qdatetime to a python datetime """
        if  not isinstance( data, QDateTime ):
            raise ValueError( f"Data is not instnace of QDateTime {data = } {type(data) = }")
        qdatetime    = data
        py_datetime  = qdatetime.toPyDateTime()

    elif   a_type in ( "timestamp", "integer" ):
        """ convert from a timestamp to a python datetime
            not sure we should except a "integer" here
        """
        if not isinstance( data, int ):
            raise ValueError( f"Data is not instnace of timestamp {data = } {type(data) = } {a_type = }" )
        py_datetime  = datetime.fromtimestamp( data )

    else:
        # error
        msg    =  f"{data = } {a_type}"
        print(  msg )
        #wat_inspector.go( self, globals() )
        raise Exception( msg )


    return py_datetime


def datetime_to( a_datetime, a_type ):
    """
    convert datetimes to the output type indicated
    by a_type
    On errors just divide by 0
    in mycase a_datetime called by other function must be a datetime but
    have exception anyway
    """
    if  not isinstance( a_datetime, datetime ):
        raise ValueError( f"a_datetime is not instnace of datetime  {a_datetime = } {type(a_datetime) = }" )

    if a_type   == "timestamp":
        timestamp  = int( a_datetime.timestamp() )
        return timestamp

    if a_type   == "qdatetime":
        #qdatetime = QDateTime.fromPyDateTime( a_datetime )
        qdatetime      = QDateTime(a_datetime.year, a_datetime.month, a_datetime.day,
                       a_datetime.hour, a_datetime.minute, a_datetime.second)
        return qdatetime

    if a_type   == "qdate":
        q_date = QDate(a_datetime.year, a_datetime.month, a_datetime.day)
        return q_date

    raise ValueError( f"Unsupported type {a_type = }")


# ---------------------------
def convert_from_to( data, in_type, out_type ):
    """
    convert data from a type indicated by in_type
    to a type indicated by out_type
    if needed use an intermetiate type of python datetime
    but not all go to same intermediate type

    first convert to intermediat type based on out_type

    """
    #rint( f">>>>>>>>>>>>>>>{data = } {in_type = } {out_type = }<<<<<<<<<<<<<<<<<<")
    #if out_type in ( )


    if in_type ==  out_type:
        """but no check on type might want to extract and put above as a bunch of or's """
        return data

    if isinstance( data, ( QDate, QDateTime,  datetime,   )):
        py_datetime   = to_datetime( data, in_type )
        ret_data      = datetime_to( py_datetime, out_type )
        return ret_data

    elif   in_type == "string":
        """ convert from a qdate to a python datetime """
        if  not isinstance( data, str ):
            raise ValueError( f"Data is not instnace of str {data = } {type(data) = }" )

        # could be string, but could be other
        if out_type in ( "qdate", "datetime" ):  # treate as a date intermediary
            py_datetime   = to_datetime( data, in_type )
            ret_data      = datetime_to( py_datetime, out_type )
            return ret_data
        # next use intermediary string, no conver necessary
        ret_data     = string_to( data, out_type )
        return ret_data

    elif   in_type in ( "integer", "timestamp" ):
        """ convert from a timestamp to a python datetime
        may want to get rid of integer and move
        """
        if data == "":
            return None

        if not isinstance( data, int ): # timestamp is an int
            raise ValueError( f"Data is not instnace of int {data = } {type(data) = } {in_type = } {out_type = }" )

        # could be string, but some sort of date
        if out_type in ( "qdate", "datetime", "qdatetime" ):  # treate as a date intermediary
            py_datetime   = to_datetime( data, in_type )
            ret_data      = datetime_to( py_datetime, out_type )
            return ret_data

        # else go to string
        data         = str( data )
        data         = string_to( data, out_type )
        return data

    else:
        raise ValueError( f"Unsupported output type conversion {data = } {in_type = } {out_type = }")

# ---------------------------
def date_criteria_from_to( data, in_type, out_type ):
    """

    qdate     = convert_db_display.date_criteria_from_to( data, in_type, out_type )
    timestamp = convert_db_display.date_criteria_from_to( data, "", "timestamp" )




    convert data from a type indicated by in_type
    to a type indicated by out_type
    if needed use an intermetiate type of python datetime
    but not all go to same intermediate type

    first convert to intermediat type based on out_type
    in_type    --- always a qdate
    out_type   --- always a timestamp vaiant _eof bod    end of day begining of day....
                which is a type of int
    intermediate type will be datetime


    for now now time zone issues but !! later
        in qdate
           datetime

         out qdate
            "ts_eod"
            ......
    """
    if in_type == "qdate":   # this is for out settings
        if not isinstance( data, QDate ): # is it what it says
            1/0
        if out_type == "qdate": # optimization to skip conversions
            return data

        dt  = datetime( data.year(), data.month(), data.day())  # from qdate

    if in_type == "datetime":
        if not isinstance( data, datetime ): # is it what it says
            1/0

    # in any case a datetime


    if  out_type == "ts_bod":
        dt  =  dt.replace(hour=0, minute=0, second=0, microsecond=0)  # to beginning of day

    elif out_type == "ts_eod":
        dt  = dt.replace(hour=23, minute=59, second=59, microsecond=999999)

    elif out_type == "ts_noon":
        dt  = dt.replace(hour=12, minute=0, second=0, microsecond=0 )

    # elif out_type == "dt_noon":
    #     dt  = dt.replace(hour=12, minute=0, second=0, microsecond=0)

    else:
        1/0

    timestamp    =  int( dt.timestamp() )
    return timestamp

def some_tests():
    print( "sometests =======================================")

    # Sample datetime for testing
    sample_datetime = datetime(2023, 10, 11, 12, 30, 45)  # Year, Month, Day, Hour, Minute, Second
    timestamp    = int( sample_datetime.timestamp() ) # Expected Unix timestamp\

    a_datetime   = sample_datetime
    qdate        = QDate(a_datetime.year, a_datetime.month, a_datetime.day)

    #qdatetime      = QDateTime.fromPyDateTime(sample_datetime)

    py_datetime    = sample_datetime
    qdatetime      = QDateTime(py_datetime.year, py_datetime.month, py_datetime.day,
                           py_datetime.hour, py_datetime.minute, py_datetime.second)



    timestamp_from_qdate    =  convert_from_to( qdate,     "qdate",     "timestamp" )
        # should convert to qdate

    qdate_from_qdatetime    =  convert_from_to( qdatetime, "qdatetime", "qdate"     )
        # should convert to qdatetime

    qdatetime_from_qdate    =  convert_from_to( qdate, "qdate", "qdatetime")


    # ------------------------- tests
    # print( datetime_to( sample_datetime, "timestamp") == timestamp )

    # print( datetime_to( None, "timestamp" ) )   # will raise error

    # print( f"{qdate}, {timestamp = }" )
    # new_timestamp    = convert_from_to( qdate, "qdate", "timestamp" )
    # print( f"{qdate}, {new_timestamp = }" )

    # new_qdate        = convert_from_to( new_timestamp, "timestamp",  "qdate" )
    # print( f"{new_qdate}, {new_timestamp = }" )


    # print( f"\n\n{convert_from_to(qdate, "qdate", "timestamp") = }")

    # print( convert_from_to(qdate, "qdate", "timestamp") == timestamp )
    # print( convert_from_to(qdate, "qdate", "qdatetime") == qdatetime )

    back_to_qdatetime    = convert_from_to( qdate_from_qdatetime, "qdate", "qdatetime" )
    print( f"{qdate = }" )
    print( f"{qdate_from_qdatetime = }" )
    print( f"{qdatetime = }" )
    print( f"{qdate = }" )
    print( f"{back_to_qdatetime = }" )


# --------------------
if __name__ == "__main__":
    #----- run the full app
    some_tests()

# ---- eof -------------
