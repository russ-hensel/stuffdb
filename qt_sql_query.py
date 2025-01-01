#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
this code is not part of the wat_inspector but belongs in stuffdb


"""

# --------------------
if __name__ == "__main__":
    import main
    #main.main()
# --------------------


# ---- imports

import datetime
# import collections
import sqlite3 as lite
import time
from tkinter import messagebox

# ------- local imports
# from   app_global import AppGlobal
# import app_global
# import string_util
#import file_writers
#import pseudo_column
#import sql_writers
import string_util
from app_global import AppGlobal


# ----------------------------------------
class QueryBuilder(    ):
    """
    build a query, currently for a single table

    qt_query     as in query = QSqlQuery()
    interface
        self.table_name        set prior to other functions, may move to init
        self.sql_where         but normally by function
        self.sql_order_by      = None
        self.sql_having        = ""
        self.sql_from          = ""
        self.column_list       = None          # sequence of column names
        self.write_gui         = None       # function one arg to write to gui9

    """
    def __init__( self,  qt_query, print_it = False, logger = None, write_gui = None  ):
        # ---- part of interface


        # use these when building so little mutating routines  like add_to_where work

        # self.sql_where        = ""
        # self.sql_having       = ""
        # self.sql_from         = ""
        # self.sql_data         = []    # parameters passed to sql
        # self.row_count        = 0

        # part of interface populate prior to use
        self.print_it                = print_it
        self.qt_query                = qt_query
        self.write_gui               = None     # see:
        self.sql_from                = None     # see:
        self.arg_dict                = None     # see:
        self.sql_where               = None     # see:
        self._sql                    = None     # see:
        self.sql_having              = None     # interface
        self.column_list             = None     # interface
        self.group_by_c_list         = None     # interface
        self.table_name              = None     # part of interface populate prior to use
        self.sql_data                = None     # see:
        self.sql_order_by            = None     # see:
        self.inner_join              = None

        self.reset( )


    #----------        --
    def reset( self, ):
        """
        reset for reuse, read

        Args:
             (TYPE): DESCRIPTION.

        Returns:
            mutates self, pretty much forgets everything but .....
            f"SELECT name  FROM {CHANNEL_TN} WHERE id = ?"
        """
        # ---- part of interface
        #self.table_name        = None          # name of table to query

        self._sql              = ""

        self.column_list       = []         # interface sequence of column names

        self.sql_where         = ""
        self.sql_order_by      = ""
        self.sql_having        = ""
        self.sql_inner_join    = ""
        self.bind_list         = [] # list of tuples for query.bindValue(":name", "%cad%")
            # might not need to save to end

        # ---- not interface, generally


        # ---- part of interface
        self.table_name        = ""          # name of table to query

        self.sql_from          = ""
                  # sequence of column names
        self.write_gui         = None       # function one arg to write to gui9
        # ---- not interface, generally

   # ----------------------------------------------
    def col_list_to_sql( self, col_list, use_table_name = True     ):
        """

        return
             string like: (  col_aaa, col_bbb, col_ccc, col_ddd, col_eee, col_fff  )    "
         """
        sql_columns     = " "

        prefix          = ""
        if use_table_name:
            prefix    = f"{self.table_name}."

        for i_name in col_list[ : -1]:
            sql_columns = ( f"{sql_columns} {prefix}{i_name}, " )

        sql_columns = ( f"{sql_columns}{prefix}{self.column_list[-1]}  " )

        return sql_columns

   # ----------------------------------------------
    def prepare_and_bind( self,      ):
        """
        Args:

        Returns:
            mutates self.qt_query

        """
        sql      = self.get_sql()
        # msg      = f"prepare_and_bind {sql = }\n watch for bind next {self.bind_list = }"
        # print( msg )
        self.qt_query.prepare( sql )

        for i_bind_tuple in self.bind_list:
            # msg   = f"prepare_and_bind {i_bind_tuple = }"
            self.qt_query.bindValue(  *i_bind_tuple )

        if self.print_it:
            print( self.qt_query.executedQuery()   )
            print( f"{self.print_it = } {sql = }")

   # ----------------------------------------------
    def get_sql( self,      ):
        """

        this is select sql features not complete

        """
        #sql        =   f"SELECT *  FROM {self.table_name}  "

        sql_columns          = self.col_list_to_sql( self.column_list )
        self._sql            = f"SELECT {sql_columns}  FROM {self.table_name}  "

        if self.sql_inner_join:
            self._sql        = f"{self._sql}\n    INNER JOIN {self.sql_inner_join} "
            #rint( self.sql_inner_join  )
            #rint( self._sql )
        # ---- where
        self._sql            = f"{self._sql }\n    {self.sql_where} "
        sql_for_debug        = self._sql

        if self.group_by_c_list:
            group_columns    = self.col_list_to_sql( self.group_by_c_list )
            self._sql        =  f"{self._sql} \n    GROUP BY { group_columns }"


        if self.sql_having:
            self._sql        = f"{self._sql}\n    HAVING {self.sql_having} "

        if self.sql_order_by:
            self._sql        = f"{self._sql}\n    {self.sql_order_by} "

        if self.print_it:
            print( self._sql )

        #sql = self._sql # for debug only

        return self._sql

    # ----------------------------------------------
    def add_to_order_by( self,    column_name, direction,   ):
        """
        arg
            column_name, direction,
            "name", "ASC"      or "DESC"

        """
        if self.sql_order_by  == "":
            self.sql_order_by  = "\n ORDER BY "
        else:
            self.sql_order_by += ", "

        self.sql_order_by  = f"{self.sql_order_by} {column_name} {direction} "

    # ----------------------------------------------
    def add_to_inner_join( self,    sql_inner_join,   ):
        """
        add to empty string only
        arg
            sql_inner_join


        """
        # if self.sql_inner_join  == "":
        #     self.sql_order_by  = "\n ORDER BY "
        # else:
        #     self.sql_order_by += ", "

        self.sql_inner_join  = sql_inner_join

   # ----------- where methods
   # ----------------------------------------------
    def add_to_where( self,    add_where, bind_tuple_list,   ):
        """
        assumes logic is AND
        add on to where clause ok if starts at 0.  assumes and between clauses
        return mutates self -- in particular  self.sql_where self.sql_data

        arg
            add_where

            bind_tuple_list,    a list of tuples  [  ( )... ]
                first component of tuple is  name of the bind variable as a string
                second component of tuple is  value of bind var, of appropriate type

        """
        if self.sql_where == "":
            self.sql_where  = "WHERE "
        else:
            self.sql_where += " AND  "

        self.sql_where   += add_where

        self.bind_list   += bind_tuple_list

        # if add_where is not None:
        #     self.sql_where   +=  add_where
        #     if add_data is not None:
        #         self.sql_data.append( add_data )

    # ----------------------------------------------
    def add_to_where_datesxxx( self, date_column_name, begin_dt, end_dt   ):
    # ----------------------------------------------
    # def add_to_where_dates( self, date_column_name, begin_dt, end_dt   ):
        """
        do we need, not for now
        what it says ....
        args
             date_column_name, begin_dt, end_dt
        return mutates self -- in particular  self.sql_where self.sql_data
        """
        indent   = "   "
        #  -------- dates

        if begin_dt is not None:
            self.add_to_where( add_where = f"\n{indent}{date_column_name}   >= ? ",
                               add_data  = begin_dt  )
            self.sql_data.append( begin_dt )

        #end_dt        =   self.end_dt
        if end_dt is not None:
            self.add_to_where( add_where  =  f"\n{indent}{date_column_name}   <= ? ",
                               add_data   = end_dt  )
            # xxxxassumes at leasxt one not none
            self.sql_data.append( end_dt )
        a_str   = string_util.to_columns( a_str, ["sql_where",
                                           f"{self.sql_where}" ] )

    # -----------------------------------
    def __str__( self,   ):
        """
        the usual
        """
        a_str   = ">>>>>>>>>>* QueryBuilder *<<<<<<<<<<<<"
        a_str   = string_util.to_columns( a_str, ["_sql",
                                           f"{self._sql}" ] )
        a_str   = string_util.to_columns( a_str, ["column_list",
                                           f"{self.column_list}" ] )

        a_str   = string_util.to_columns( a_str, ["group_by_c_list",
                                                   f"{self.group_by_c_list}" ] )
        a_str   = string_util.to_columns( a_str, ["sql_from",
                                           f"{self.sql_from}" ] )
        a_str   = string_util.to_columns( a_str, ["sql_having",
                                           f"{self.sql_having}" ] )
        a_str   = string_util.to_columns( a_str, ["sql_order_by",
                                           f"{self.sql_order_by}" ] )
        a_str   = string_util.to_columns( a_str, ["sql_where",
                                           f"{self.sql_where}" ] )

        a_str   = string_util.to_columns( a_str, ["sql_inner_join",
                                           f"{self.sql_inner_join}" ] )

        a_str   = string_util.to_columns( a_str, ["table_name",
                                           f"{self.table_name}" ] )
        a_str   = string_util.to_columns( a_str, ["write_gui",
                                           f"{self.write_gui}" ] )
        a_str   = string_util.to_columns( a_str, ["bind_list",
                                           f"{self.bind_list}" ] )

        return a_str

# ----------------------------------------

    """
    class SQLBuilder_fromstructurednotes(   ):

    and other material removed below
    from structured notes  may be more classes of interest
    build sql based on criteria ( all should be in reset )
    then pushed in by external methods setting values
    not all criteria used by all methods ?
    always use fully qualified table names

    Build and output
        for output need to know    target... file_name
                                   format or type
                                   append option


        ............................
    """
