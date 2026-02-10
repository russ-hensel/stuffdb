#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


not sure of role in stuffdb
    incldes errors which are not called by stuffdb
    not sure what to do with it
    for now just keep


dup of yt_scrape..... but in process of change

from easy db db_objects
lots of junk in it
clean it up


this is just sql lite, no alchemy or qt


"""

import collections
import logging
# ---- imports
#import os
#import sys
import sqlite3 as lite
import time
from subprocess import Popen

import app_global

import string_utils as string_util
import string_utils
from app_global import AppGlobal

# ------------ local
#from   app_global import AppGlobal
#import file_writers
#import file_readers

def line_out( line ):
    """ """
    print( line )

# ----------------------------------------
class SqlRunner(   ):
    """
    run sql output to a SQLWriter


    """
    def __init__( self, db_file_name ):
        # ---- part of interface
        if db_file_name is None:
            line_out( "db_file_name is None:")
            1/0

        self._connection             = None     # see:
        self._cursor                 = None     # see:
        self.db_file_name            = None     # see:
        self.end_time                = None     # see:
        self.ix_batch                = None     # see:
        self.max_ix_batch            = None     # see:
        self.output_append           = None     # see:
        self.output_name             = None     # see:
        self.prior_row               = None     # see:
        self.row_count               = None     # see:
        self.row_to_list             = None     # see:
        self.select_writer           = None     # see:
        self.sql_writer              = None     # see:
        self.start_time              = None     # see:
        self.write_row               = None     # see:

        self.reset( db_file_name )
    #----------        --
    def reset( self, db_file_name = None  ):
        """
        args
            db_file_name
                if None keep old name

        Returns:
            mutates self

        """
        # ---- part of interface
        #self.table_name        = None          # name of table to query

        if db_file_name is not None:
            self.db_file_name        = db_file_name
            # error to use till set with # instance.db_file_name = "somefile.db"

        #AppGlobal.db_object      = self
        self._connection         = None   #  Their main purpose is creating Cursor objects, and Transaction control.
        """
        https://docs.python.org/3/library/sqlite3.html#connection-objects
        commit()

            Commit any pending transaction to the database. If autocommit is True, or there is no open transaction, this method does nothing. If autocommit is False, a new transaction is implicitly opened if a pending transaction was committed by this method.

        rollback()

            Roll back to the start of any pending transaction. If autocommit is True, or there is no open transaction, this method does nothing. If autocommit is False, a new transaction is implicitly opened if a pending transaction was rolled back by this method.

        close()

            Close the database connection. If autocommit is False, any pending transaction is implicitly rolled back. If autocommit is True or LEGACY_TRANSACTION_CONTROL, no implicit transaction control is executed. Make sure to commit() before closing to avoid losing pending changes.

        execute(sql, parameters=(), /)

            Create a new Cursor object and call execute() on it with the given sql and parameters. Return the new cursor object.

        executemany(sql, parameters, /)

    Create a new Cursor object and call executemany() on it with the given sql and parameters. Return the new cursor object.

        """
        self.ix_batch            = 0
        self.max_ix_batch        = 10
        #self.open_connection(   )
        #self.commit( for_sure = True )
        #self.app                 = AppGlobal.app

        self.sql_writer        = None  # part of interface

        self.output_name       = "./sql_output.txt"   # may need to modify based on type
        self.output_append     = "Append"
        # self.file_name              = builder.output_name
        # self.columns_out            = builder.columns_out
        # self.columns_info           = builder.columns_info
        # self.db_name            = ""   #table_info.db_file_name
        self.start_time         = 0    # probably time.time() start of select
        self.end_time           = 0
        self._cursor            = None
        self.select_writer      = None
        """
        https://docs.python.org/3/library/sqlite3.html#cursor-objects

            cursor does not commit
        """

     # ----------------------------------------------
    def commit_connection( self, ):
        """
         connections commit not cursors

        """
        if self._connection:
            self._connection.commit()
            # self._connection         = None

     # ----------------------------------------------
    def close_connection( self, ):
        """
        close everything that might be open

        """
        if self._connection:
            self._connection.commit()
            self._connection.close()
            self._connection         = None

     # ----------------------------------------------
    def open_connection( self, reuse = False ):
        """
        return it but more important set self._connection

        """
        if self._connection:
            # already have connection
            if reuse == False:
                self._connection.close()

        try:
            self._connection   = lite.connect( self.db_file_name )
            #rint( f"open_connection create connection for  {self.db_file_name} {self._connection}" )

        except lite.Error as a_except:
             line_out( type(a_except), '::', a_except )
             line_out( f"open_connection() unable to open: self.db_file_name = {self.db_file_name}")
        #rint( f"return new connection {self._connection}")
        return self._connection

   # ----------------------------------------------
    def get_cursor( self,   ):
        """
        support ram as well as file
        remember to commit ?? close
        close another cursor  self._cursor  ??
        open connection only if needed

        """
        if not self._connection:
            self.open_connection( )
        cur = self._connection.cursor()
        return cur

    # ----------------------------------------------
    def define_table ( self, table_name, sql, allow_drop = False ):
        """
        appears to be valennal SQLite
        table_name
        sql         sql that creates the table
        return
            None
            but may raise some exception -- none
        !! look into indexing this -- and primary key
        """
        cur         = self.get_cursor()

        try:
            if allow_drop:
                cur.execute( f"DROP TABLE IF EXISTS {table_name}" )   # else error if table exists
            cur.execute( sql )

        except lite.Error as a_except:
            #except ( lite.Error, TypeError) as a_except:
            line_out( type(a_except), '::', a_except )
            line_out( f"error define_{table_name} , exception {a_except}" )
            raise
        finally:
            self.commit_connection()
            self.close_connection( )

        line_out( f"define_table   {table_name} " )

    # ----------------------------------------------
    def insert_row( self, sql, a_row ):
        """
        what it says read
        run sql to insert a row of data
        mostly try...
        """
        #rint( f"sql runner insert_row  sql = {sql}")
        #rint( f"insert --> {row_data}" )
        try:
            cur           = self.get_cursor()  # better self.cur
            #cur.executemany( sql, row_data )
            cur.execute( sql,  a_row )

            self.close_connection()
            # sql_con.close()   # with takes care of this ?

        except Exception as a_except:  # !! be more specific
            line_out( "exception in insert_row() {sql}"    )
            line_out( type(a_except), '>>', a_except )
            self.close_connection()

            raise

    # ----------------------------------------------
    # called by str( instance of AppClass )
    def __str__(self):

        a_str   = ""
        a_str   = ">>>>>>>>>>* SqlRunner *<<<<<<<<<<<<"
        a_str   = string_util.to_columns( a_str, ["_connection",
                                           f"{self._connection}" ] )
        a_str   = string_util.to_columns( a_str, ["db_file_name",
                                           f"{self.db_file_name}" ] )
        a_str   = string_util.to_columns( a_str, ["_cursor",
                                           f"{self._cursor}" ] )
        a_str   = string_util.to_columns( a_str, ["end_time",
                                           f"{self.end_time}" ] )
        a_str   = string_util.to_columns( a_str, ["ix_batch",
                                           f"{self.ix_batch}" ] )
        a_str   = string_util.to_columns( a_str, ["max_ix_batch",
                                           f"{self.max_ix_batch}" ] )
        a_str   = string_util.to_columns( a_str, ["output_append",
                                           f"{self.output_append}" ] )
        a_str   = string_util.to_columns( a_str, ["output_name",
                                           f"{self.output_name}" ] )
        a_str   = string_util.to_columns( a_str, ["prior_row",
                                           f"{self.prior_row}" ] )
        a_str   = string_util.to_columns( a_str, ["row_count",
                                           f"{self.row_count}" ] )
        a_str   = string_util.to_columns( a_str, ["row_to_list",
                                           f"{self.row_to_list}" ] )
        a_str   = string_util.to_columns( a_str, ["select_writer",
                                           f"{self.select_writer}" ] )
        a_str   = string_util.to_columns( a_str, ["sql_writer",
                                           f"{self.sql_writer}" ] )
        a_str   = string_util.to_columns( a_str, ["start_time",
                                           f"{self.start_time}" ] )
        a_str   = string_util.to_columns( a_str, ["write_row",
                                           f"{self.write_row}" ] )
        a_str = f"{a_str}\n__________ End SqlRunner __________"
        return a_str

   # ----------------------------------------------
    def confirm_continue( self, info_msg,  a_title, msg, ):   #  help_mode = False
        """
        user interaction:
        display and perhaps throw exception
        app_global.UserCancel
        exceptions: raise app_global.UserCancel if user does not want to continue
        return: zip or exception
        argument in builder  ..... help_mode = True aborts the actual select
        """
        pass

        help_mode    = self.help_mode

        line_out( f"builder confirm_continue {help_mode}")

        AppGlobal.gui.display_info_string( info_msg )

        # if help_mode:
        #     raise app_global.UserCancel( "Mode: Help only, query not run" )

        if AppGlobal.parameters.confirm_selects:   #  !! may still need adjust for msg format

            continue_flag  = messagebox.askokcancel( a_title, msg )

            if continue_flag is not True:
                AppGlobal.gui.display_info_string( "Operation canceled" )
                raise app_global.UserCancel( "user: Operation canceled" )


  # ----------------------------------------------
    def go_xxx( self,  ):
        """
        after all setup is done go and do the select
        arg:  which select in builder to run, later when sub-classed just go
        """
        print( "SQLBuilder builder.go() ")
        AppGlobal.gui.clear_message_area( ) # check this actually works in real time !!
        self.start_time         = 0    # probably time.time() start of select
        self.end_time           = 0
        try:
            self.this_select()          # configured for one of self.  ... with sub-classing always the same
            line_out( f"after this select  {self.get_info_string( ) }"   )

            self.select_and_output()    # help_mode ??

        except app_global.UserCancel as exception:   #  !!this is probably the Right one
        #except Exception as exception:
            pass  # Catch the  exception and swallow as user wants out not an error
            line_out( exception )  # debug only

        msg   = f"Select Done, rows selected: {self.row_count} time = {self.end_time - self.start_time}"
        AppGlobal.gui.display_info_string( msg )
        AppGlobal.logger.debug(  msg  )
        line_out( msg )

    # ----------------------------------------------
    def select( self, sql, sql_data  ):
        """
            new for stuff_db, so far for a single record .
        args

            sql_data is a dict
        """
        self.start_time     = time.time()
        self.row_count      = 0
        self.open_connection()

        with self._connection:
            cur           = self.get_cursor()
            execute_args  = (  sql,   sql_data,  )
            msg           = f"sql_util.select  ; execute_args {execute_args}"
            line_out(  msg )
            # if self.select_writer:
            #     self.select_writer.write_header( )

            #AppGlobal.logger.debug( msg )
            cur.execute( *execute_args )
            # cur.execute( sql )
            while True:
                row   = cur.fetchone()

                self.row_count    += 1

                line_out( f"row {self.row_count}: {row}"  )
                break

        self.commit_connection()
        self.close_connection()
        self.end_time = time.time()

        return row

    # ----------------------------------------------
    def update( self, sql, sql_data  ):
        """
            new for stuff_db, so far for a single record .
        args

            sql_data is a dict
        """
        self.start_time     = time.time()
        self.row_count      = 0
        self.open_connection()

        with self._connection:
            cur           = self.get_cursor()
            execute_args  = (  sql,   sql_data,  )
            msg           = f"sql_util.SqlRunner.update  ; execute_args {execute_args}"
            line_out(  msg )
            # if self.select_writer:
            #     self.select_writer.write_header( )

            #AppGlobal.logger.debug( msg )
            cur.execute( *execute_args )
            # cur.execute( sql )
            # while True:
            #     row   = cur.fetchone()
            #     # self.write_row   = True   # this allows pseudo columns to suppress output
            #     # if row is None: # end of select
            #     #     break

            #     self.row_count    += 1
            #     self.prior_row     = row    # save for later use, perhaps at footer ? -- save after transform is current
            #     #if self.row_to_list:        # !! efficiency tweak ... probably not worth it ... also to make mutable

            #     # if self.select_writer:
            #     #     self.select_writer.write_row( row )
            #     #     #rint( f"select_and_output row {self.row_count}: {row}"  )
            #     # else:
            #     print( f"row {self.row_count}: {row}"  )
            #     break


        self.commit_connection()
        self.close_connection()
        self.end_time = time.time()

        # return row


    # ----------------------------------------------
    def select_and_output( self, sql, sql_data  ):
        """
            this is the new version for yt_scrape
        args
            would sql_query be a better argument ?? !!
            sql_data is a dict
        """
        self.start_time     = time.time()
        self.row_count      = 0
        self.open_connection()

        with self._connection:
            cur           = self.get_cursor()
            execute_args  = (  sql,   sql_data,  )
            msg           = f"select and output; execute_args {execute_args}"
            line_out(  msg )
            if self.select_writer:
                self.select_writer.write_header( )

            #AppGlobal.logger.debug( msg )
            cur.execute( *execute_args )
            # cur.execute( sql )
            while True:
                row   = cur.fetchone()
                # self.write_row   = True   # this allows pseudo columns to suppress output
                if row is None: # end of select
                    break

                self.row_count    += 1
                self.prior_row     = row    # save for later use, perhaps at footer ? -- save after transform is current
                #if self.row_to_list:        # !! efficiency tweak ... probably not worth it ... also to make mutable

                if self.select_writer:
                    self.select_writer.write_row( row )
                    #rint( f"select_and_output row {self.row_count}: {row}"  )
                else:
                    line_out( f"row {self.row_count}: {row}"  )
                #row  = list( row )


                # if self.write_row:   # recently moved up from below so suppressed rows not formatted
                # !! looks like formatting may be done in two places .... no this is transforms
                    # for ix_col, i_col in enumerate( row ):
                    #     # better ?? to put functions in a list to simplify reference
                    #     # indexed double dict lookup


                    #     # i_col_info    = columns_info[ self.columns_out[ ix_col ] ]
                    #     # transform     = i_col_info["transform"]

                    #     transform     = idempotent

                    #     #col_text     = i_col_info["column_head"]
                    #     if transform is not None:
                    #         row[ ix_col ]    = transform( i_col )

                    # self.file_writer.write_row( row )   # here may need to add row count.... breaking stuff what type is row?
                # else row is suppressed

        self.commit_connection()
        self.close_connection()
        self.end_time = time.time()

    # ----------------------------------------------
    def select_and_output_old( self,  ):
        """
        think this is only code in this file still used structured_notes 2024 Mar, transfer it out
        what it says
        now does pseudo cols ....
        !! update for col transforms
        ?? would bringing references local help anything
        ?? flag to see if any transforms used now seems to be automatic based on
        column names
        some mutation and file output in most cases
        """
        self.start_time     = time.time()

        # check transforms to see if we need to convert to list !! for speed, but is it worth it
        # for now force it
        self.row_to_list    = True

        # was for transforms, now use idempotent for all could put back
        #columns_info        = self.columns_info
        #rint( f"columns_info{columns_info}")

        # now made earlier .. injected
        # file_writer         = file_writers.make_file_writer( self  )
        # self.file_writer    = file_writer  # copy for AuxSelect.....


        self.file_writer.write_header( self.table_info )

        msg     = f"Select and output; connect to {self.db_name}"
        line_out( msg )
        sql_con = lite.connect( self.db_name )

        with sql_con:
            cur           = sql_con.cursor()
            execute_args  = ( self.sql,  self.sql_data,  )
            msg           = f"select and output; execute_args {execute_args}"
            #rint(  msg )
            AppGlobal.logger.debug( msg )
            cur.execute( *execute_args )

            while True:  # get rows one at a time in loop
                row   = cur.fetchone()
                self.write_row   = True   # this allows pseudo columns to suppress output
                if row is None: # end of select
                     break

                self.row_count    += 1
                self.prior_row     = row    # save for later use, perhaps at footer ? -- save after transform is current
                if self.row_to_list:        # !! efficiency tweak ... probably not worth it ... also to make mutable
                    #print( "row_to_list"  )
                    row  = list( row )

                for i_function in self.row_functions:
                    i_function( row )   # mutates row
                #rint( f"_>>>>>{row}")

                if self.write_row:   # recently moved up from below so suppressed rows not formatted
                # !! looks like formatting may be done in two places .... no this is transforms
                    for ix_col, i_col in enumerate( row ):
                        # better ?? to put functions in a list to simplify reference
                        # indexed double dict lookup


                        # i_col_info    = columns_info[ self.columns_out[ ix_col ] ]
                        # transform     = i_col_info["transform"]

                        transform     = idempotent

                        #col_text     = i_col_info["column_head"]
                        if transform is not None:
                            row[ ix_col ]    = transform( i_col )

                    self.file_writer.write_row( row )   # here may need to add row count.... breaking stuff what type is row?
                # else row is suppressed

        sql_con.commit()
        sql_con.close()
        self.end_time = time.time()

        # beware this is a mess
        footer_function_info  = ""
        footer_info           = ""
        # pseudo columns and perhaps others

        #rint( f"footer functions are {self.footer_functions}" )

        for i_function in self.footer_functions:
                 #rint( "calling footer function"  )
                 foot_msg                  =   i_function(  )   # returns string
                 footer_function_info     += "\n" + foot_msg

        footer_info    +=  f"Done: >\n"
        footer_info    +=  f"     total number of rows = {self.row_count}"

        msg             =  f"     select and file write took {self.end_time - self.start_time} seconds"
        footer_info  += f"\n{msg}"
        footer_info  += f"\n{footer_function_info}"

        self.file_writer.write_footer( footer_info )

        line_out(  footer_info )
        msg      =  f"select complete with footer info: {footer_info}"
        AppGlobal.logger.debug( msg )
        line_out( msg )

        # os open file for user to view
        #if   self.output_format  == "html":
            #debug = self.output_name
            # debug = file_writer.file_name   # !! shows as error but think injected

            # print( "should the output name be in self. or put the whole function in the writer ")
            # AppGlobal.os_open_html_file( self.output_name )  # or

            # self.file_writer.file_name
        # debug = self.output_name
        # self.file_writer.view_output_file()

            # AppGlobal.os_open_url( self.output_name )

        # elif self.output_format  == "zap":
        #     pass
        # elif self.output_format  == "msg":
        #     pass
        #     # AppGlobal.gui.do_clear_button( "dummy_event")

        #     # with open( self.output_name, "r", encoding = "utf8", errors = 'replace' )  as a_file:
        #     #     lines = a_file.readlines()
        #     #     # print( lines )
        #     #     msg  = "".join( lines )
        #     #     AppGlobal.gui.display_info_string( msg )

        # else:
        #     AppGlobal.os_open_txt_file( self.output_name )



# ---- old old old

# ================= Class =======================
# Define a class is how we crash out
class DBOjectProgramerException( Exception ):
    """
    # make this a hierarchy later -- learn how
    raise if a condition that appears to be a programming exception
    occurs return msg = (  msg_usr, msg_tech,)
    """
    # ----------------------------------------
    def __init__(self, msg_usr, msg_tech ): # queue_item ):
        # testing an idea
        self.msg         = ( msg_usr, msg_tech )

# ================= Class =======================
# Define a class is how we crash out
class DBOjectException( Exception ):
    """
    raise if a condition ( perhaps a bad parameter makes it hard to continue )
    this is for early return to terminate a function usually because of bad
    file name, file contents.... msg should elucidate
    throw back to button press, then catch and put info on
    gui
    """
    # ----------------------------------------
    def __init__(self, msg, ): # queue_item ):
        # call ancestor ??
        # Set some exception information
        # currently pretty much a test
        self.msg         = msg    # string message

#====================================
class TableInfo( object ):
    """
    This holds info about a table so that we can characterize it and its
    columns.  It does not hold any table data, just meta data.  Later this guy
    will get more complicated. Used to describe select statements and to define
    the db in the first place
    How to make:
        init
        then it needs a list of columns that can come from:
            build_from_input file ... then can go on to define a table
            build_from_sql        ... not sure how is useful
            build_from_db file    ... with a table name and database file name

            see init to see a bunch of values it may hold basics are usually
                database_file_name, table_name, and column names and info about the columns

        You can save them, for reuse. -- seems now now a good idea

        Can init with nothing, but then does not do much
        Just set the table_key and name.
        Have setters getters for the dictionary part

        Make from a file:  ?? looks obsolete FileReaderToDataDict.file_to_data_dict()
        Will need a db file name pretty quick

        Note that except for ROWID table names should be lower case... more info in help.txt

    """
    #----------- init -----------
    def __init__(self, ):     # expand the init to set more stuff
        """

        """
        # set items prior to use
        self.__table_data_dict    = None  # info on table level  .table_data_dict
        """

        __table_data_dict  ordered dict normally kept in alpha order by column name
                           contains meta data about the table, key is the column name
                           value is a list of properties, could be dicts but for now indexed list

        """
        #-----------------
        #self.table_data_dict_list_len   = 4   # length of list in the data dict
        #for table_data_dict
        self.ix_data_type               = 0

        self.where_list                 = []    # list of lists [ col_name, where_operator, where_value ]
        self.ix_col_name                = 0
        self.ix_where_operator          = 1
        self.ix_where_value             = 2

        self.order_by_list              = []    # list of lists [ col_name, where_operator, where_value ]
        self.ix_order_by_type           = 1
        #self.ix_sort_type               = 4

        #self.ix_format_order            = 5   # perhaps could default to 0 , 1,2 after sort ?
        self.format_list                = []    # list of lists [ col_name, where_operator, where_value ] see _columns
        self.ix_format_just             = 1
        self.ix_format_len              = 2
#        self.ix_to_db_convert           = 7   # a function using identity for nothing could change to none ?
#        self.ix_from_db_convert         = 8

        # ... fix next # match this to above note defaults
        self.default_list               = [ "TEXT", "", "", -1, "",  -1, "l20", self.identity,  self.identity ]
        #                                    0       1  2    3  4    5   6      7              8
        #------------------
        self.table_key            = "in init not properly set " # should be able to get out of dict  !! we need a way to get
        self.table_name           = None
        #self.db_file_name         = None  #, set as needed -- is it ??
        self.db_file_name         = None    # populated sometimes see code

        self.data_dict_sql        = ""

        self.sql                  = ""      # sql that works with the table
        self.qmarks               = []      # list of question marks used in queries  --- may need qmarks for where and place for var in future

        self.select_table_data_dict      = None    # unless build_select_info_from_file

        #self.dict_file_info       = None # probably should be local
        self.built_select_input_file_name = ""

    # ----------------------------------------
    def __str__( self ):
        lines     = []

        i_line    = 2*"\n" + " --------TableInfo-------- "
        lines.append( i_line )

        i_line    = f"self.table_name {self.table_name}"
        lines.append( i_line )

        i_line    = f"self.table_key {self.table_key }"
        lines.append( i_line )

        lines.append( f"len( self.table_data_dict ) {len( self.table_data_dict )}" )

#        i_line    = f"self.table_data_dict {self.table_data_dict}"
#        lines.append( i_line )

        lines.append( f"self.order_by_list {self.order_by_list}" )
        lines.append( f"self.where_list {self.where_list}" )
        lines.append( f"self.format_list {self.format_list}" )

        ret  = "\n".join( lines )
        ret  += 2*"\n"
        return ret

   #  ----------- getter setter -----------------------
    # two for set and get, note name match
    @property    # lets us get not set
    def table_data_dict( self ):
        #print( " return self.__demo_property getter" )
        return self.__table_data_dict

    # ----------------------------------------
    @table_data_dict.setter
    def table_data_dict(self,  dict_info ):
        """
        use: a_table_info.table_data_dict
        this makes sure it is sorted
        dict_info    not sure what is in this  may just be column_names now but will be more
        """
        pass
        self.__table_data_dict      = collections.OrderedDict()
        col_names                   = list( dict_info )
        col_names.sort( )       # but might want to put key fields first
        # some sort of list comp would be better
        for i_col_name in col_names:
            self.__table_data_dict[ i_col_name ] = dict_info[ i_col_name ]

        #print( " set self.__table_data_dict setter" )
        return

    # ----------------------------------------
    def identity( self, something ):
        """
        Purpose:

        Returns:
        Raises:
        """
        return something

    # ----------------------------------------
    def get_column_names( self, include_rowid ):
        """
        Purpose:
            see name
            should be a function so simple
        Args:
        Returns: list of column names
        Raises:
        """
        column_names     =  self.table_data_dict.keys()
        if not include_rowid:
            column_names.remove( "ROWID" )

        return column_names

    # ----------------------------------------
    def _columns( self, file_line_reader ):
        """
        build select for columns from file_line_reader
        header already processed
        Return: ret_why done change in state
        Raises DBOjectException( msg ) if problem

        """
        msg   = "starting columns - format"
        AppGlobal.print_debug(  msg )
        found_order    = 0   # think lists keep the order as primary index
        while True:     # will the line have a newline... on it yes need to strip off end
            what, column, data = file_line_reader.get_next_line()
            #print( what, column, data )
            if what == "eof":
                return what
            if what == "break":
                return what
            #else:

            if column in self.table_data_dict:      # should be gone select_table_data_dict:
                # ok update data
                pass # pick up after
                if is_in_select_list( column, self.format_list ):
                   msg  =  f"columns() problem on line {file_line_reader.ix_line}: {column} is repeated"
                   AppGlobal.print_debug(  msg )
                   raise DBOjectException( msg )

            else:
                msg  =  f"columns() problem on line {file_line_reader.ix_line}: {column} is not a column name"
                AppGlobal.print_debug(  msg )
                raise DBOjectException( msg )

            if data is None or data == 'null string':
                continue

            data     = data.upper()
            align    = data[0].lower()

            valid_align    = ( "l", "r", "c", )
            if align not in valid_align:
                msg  =  f"columns() alignment problem on line {file_line_reader.ix_line}: {align} not in {valid_align}"
                AppGlobal.print_debug(  msg )
                raise DBOjectException( msg )

            # strip off first character then number if no num then use 0 meaning -- no number
            try:
                if len( data ) > 1:
                    length   = int( data[1:].strip( " " ) )
                else:
                    length   = 0

            except Exception as exception:    # !! should limit this guy
                msg  =  f"columns() length problem on line {file_line_reader.ix_line}: {exception}"
                AppGlobal.print_debug(  msg )
                raise DBOjectException( msg )

            self.format_list.append( [column, align, length ] )
            found_order   += 1

        return "infinity"

    # ----------------------------------------
    def _order_by( self, file_line_reader ):
        """
        order by

        header already processed
        Return: ret_why    change in state
        Raises DBOjectException( msg ) if problem

        """
        msg   = "starting _order_by"
        AppGlobal.print_debug(  msg )
        found_order    = 0   # think lists keep the order as primary index
        while True:     # will the line have a newline... on it yes need to strip off end
            what, column, data = file_line_reader.get_next_line()
            #print( what, column, data )
            if what == "eof":
                return what
            if what == "break":
                return what
            #else:

            if column in self.table_data_dict:      # should be gone select_table_data_dict:

                if is_in_select_list( column, self.order_by_list ):
                   msg  =  f"_order_by() problem on line {file_line_reader.ix_line}: {column} is repeated"
                   AppGlobal.print_debug(  msg )
                   raise DBOjectException( msg )

            else:
                msg  =  f"_order_by() problem on line {file_line_reader.ix_line}: {column} is not a column name"
                AppGlobal.print_debug(  msg )
                raise DBOjectException( msg )

            if data is None or data == 'null string':
                continue

            data   = data.upper()     # consider fix if A... D.... or up down ??
            if data not in ["ASC", "DESC" ]:
                msg     =  f"_order_by() sort direction should be 'ASC' or 'DESC' but is {data}"
                AppGlobal.print_debug( msg )
                raise DBOjectException( msg )

            # ?? still need some tests here

            self.order_by_list.append( [column, data] )
            found_order   += 1

        return "ok"

        # ----------------------------------------
    def _where( self, file_line_reader ):
        """
        build the where info ( not sql ) into self where list
        sql goes in as column sql: and data the sql

        header already processed
        Return: ret_why  ok break eof    and change in state of self
        Raises DBOjectException( msg ) if problem

        """
        msg   = "starting _where"
        AppGlobal.print_debug(  msg )
        found_order    = 0   # think lists keep the order as primary index
        while True:     # will the line have a newline... on it yes need to strip off end
            what, column, data = file_line_reader.get_next_line()
            #print( what, column, data )
            if what == "eof":
                return what
            if what == "break":
                return what
            #else:

            if column in self.table_data_dict:      # should be gone select_table_data_dict:

                if is_in_select_list( column, self.where_list  ):
                   msg  =  f"_where() problem on line {file_line_reader.ix_line}: {column} is repeated"
                   AppGlobal.print_debug(  msg )
                   raise DBOjectException( msg )

            else:
                msg  =  f"self.where_list() problem on line {file_line_reader.ix_line}: {column} is not a column name"
                AppGlobal.print_debug(  msg )
                raise DBOjectException( msg )

            if data is None or data == 'null string':
                continue

             # validate here
#            data   = data.upper()
#            if data not in ["ASC", "DESC" ]:
#                msg     =  f"_order_by() sort direction should be 'ASC' or 'DESC' but is {data}"
#                #print( msg )
#                AppGlobal.logger.debug( msg )
#                raise DBOjectException( msg )

            # ?? still need some tests here

            # break data on space and add quotes ( what if quoted data ) ??
            parts       = data.split( " ", 1 )  # 1 splits into 2 parts

            if len( parts ) < 2:
                msg  =  f"problem where has no value >>{data}<<"
                AppGlobal.print_debug(  msg )
                raise DBOjectException( msg )

            data      = parts[0] + ' "' + parts[1] + '"'

            self.where_list .append( [column, data] )

            found_order   += 1

        return "ok"

    # ----------------------------------------
    def build_delete_sql_from_info( self,   ):
        """
        Purpose:
                see title
                DELETE FROM table_name WHERE condition;
        Returns: sql and qmarks ??
                 change in state
        might access with
                sql      =  self.table_info.sql
                qmarks   =  self.table_info.sql

        """
        msg   = f"build_delete_sql_from_info() "
        AppGlobal.print_debug( msg )

        parts       = []
        sql_select  = " DELETE FROM " + self.table_name

        # order by not needed the where
        if len( self.where_list ) == 0:
            sql_where      = " "
            qmarks         = ""
        else:
            sql_where      = " WHERE "
            qmarks         = []
            parts          = []
            for i_list  in self.where_list:
                parts.append( i_list[0]  + " " + i_list[1] )          # column name
                qmarks.append( "?" )
            sql_where  += ", ".join( parts  )
            qmarks     =  ", ".join( qmarks )

        self.sql       = sql_select + sql_where
        self.qmarks    = qmarks
#        msg   = f"sql_where >>{sql_where}<<>>{qmarks}<<"
#        AppGlobal.print_debug( msg )

        msg   = f"build_delete_sql_from_info self.sql >>{self.sql}<< "
        AppGlobal.print_debug( msg )


    # ----------------------------------------
    def build_select_sql_from_info( self, print_out=False ):
        """
        Purpose:
             info should have been built
        should have all we need in instance var

        """
        msg   = f"build_select_sql_from_info() from self"
        AppGlobal.print_debug( msg )

        table_name        = self.table_name

        # format/select/column section
        #self.qmarks         = []
        parts               = []

        if len( self.format_list ) == 0:
            sql_select      = " SELECT "
            # !! return nothing to do or do all !! still need qmarks
        else:
            sql_select      = " SELECT "
            parts          = []
            for i_list  in self.format_list:
                parts.append( i_list[0]  )          # column name
            sql_select  += ", ".join( parts  )

        sql_select  += " FROM " + self.table_name

        # --------- where
        if len( self.where_list ) == 0:
            sql_where      = " "
            qmarks         = ""
        else:
            sql_where      = " WHERE "
            qmarks         = []
            parts          = []
            for i_list  in self.where_list:
                parts.append( i_list[0]  + " " + i_list[1] )          # column name
                qmarks.append( "?" )
            sql_where  += ", ".join( parts  )
            qmarks     =  ", ".join( qmarks )
            msg   = f"build_select_sql_from_info where  parts >>{parts}<<  qmarks >>{qmarks}<< "
            AppGlobal.print_debug( msg )

        # order by
        if len( self.order_by_list ) == 0:
            sql_order_by      = ""
        else:
            sql_order_by      = " ORDER BY "
            parts          = []
            for i_list  in self.order_by_list:
                parts.append( i_list[0] + " " + i_list[1] )          # column name direction
            sql_order_by  += ", ".join( parts  )

        self.sql       = sql_select + sql_where + sql_order_by
        self.qmarks    = qmarks
#        msg   = f"sql_where >>{sql_where}<<>>{qmarks}<<"
#        AppGlobal.print_debug( msg )

        msg   = f"self.sql >>{self.sql}<< "
        AppGlobal.print_debug( msg )

    # ----------------------------------------
    def build_select_info_from_file( self, db_file_name, input_file_name, print_out=False ):
        """
        Purpose:

        Returns: zip but change in state  populates table_info s
        Raises:  consider this as return

        -- separate
        select
           where
           order_by
           format

        """
        msg   = f"build_select_info_from_file() {input_file_name} for db {db_file_name}"
        AppGlobal.print_debug( msg )

        self.db_file_name    = db_file_name

        if self.built_select_input_file_name == "":
            self.built_select_input_file_name = input_file_name   # just in case use with care
        else:
            msg = f"build_select_info_from_file() select seems to have already been built from {self.built_select_input_file_name}"
            AppGlobal.print_debug( msg )
            return False

        file_line_reader     = file_readers.FileLineReader( input_file_name )

        info_return          = file_line_reader.get_file_info( )   # !! look at return reason  info_return
        required             = [ "purpose", "use_table", "section" ]
        is_ok = file_line_reader.check_for_required_file_info( required )
        if not is_ok:
            msg = f"build_select_info_from_file() required file info missing {required} got file_line_reader"
            AppGlobal.print_debug( msg )
            raise DBOjectException( msg )
            return False

        dict_file_info              = file_line_reader.file_info_dict    # could have gotten dict as return above
        table_name                  = dict_file_info[ "use_table" ]
        self.build_from_db_file( table_name, self.db_file_name,  print_out=False  )

        purpose                     = dict_file_info[ "purpose" ]
        if purpose not in [ "select", "delete" ]:
            msg = f"build_select_info_from_file() purpose should be 'select' or 'delete', instead got {purpose}"
            AppGlobal.print_debug( msg )
            raise DBOjectException( msg )
            return False

        section           = dict_file_info[ "section" ]

        why_done          = ""
        done_order_by     = False
        done_columns      = False
        done_where        = False

        # no protect against repeated sections ??
        while True:
            if   section == "order_by":
                why_done          = self._order_by(  file_line_reader )
                done_order_by     = True
            elif section == "columns":
                why_done          = self._columns(  file_line_reader )
                done_columns      = True
            elif section == "where":    # or where or section
                 why_done          = self._where(  file_line_reader )
                 done_where        = True
            else:
                msg     =  f"build_select_info_from_file() file section >>{section}<< not a valid section"
                AppGlobal.print_debug(  msg )
                raise DBOjectException( msg )

            if why_done == "eof":
                msg     =  f"build_select_info_from_file() why_done = eof"
                AppGlobal.print_debug(  msg )
                break  # or return
            # section break read new purpose

            info_return = file_line_reader.get_file_info( )  #  info_return look at it
            if info_return == "eof":
                msg     =  f"build_select_info_from_file() info return = eof done"
                AppGlobal.print_debug(  msg )
                break

            required             = [ "section" ]
            is_ok = file_line_reader.check_for_required_file_info( required )
            if not is_ok:
                msg = ( f"build_select_info_from_file() required file info missing {required} >> {file_line_reader.file_info_dict}" +
                        f"now read to line  {file_line_reader.ix_line} in file" )
                AppGlobal.print_debug( msg )
                raise DBOjectException( msg )

            dict_file_info           = file_line_reader.file_info_dict
            section                  = dict_file_info[ "section" ]

        if not done_order_by:
            msg   = "no section for order_by"
            AppGlobal.gui_write_progress( msg )

        if not done_columns:
            msg   = "no section for columns, setting defaults"
            AppGlobal.gui_write_progress( msg )

            new_format_list  = []
            column_names     = self.get_column_names( include_rowid = True )
            for i_column in  column_names:
                new_format_list.append( [i_column, "L", 5 ] )

            self.format_list = new_format_list
            msg   = f"default format list {self.format_list}"
            AppGlobal.print_debug( msg )
        else:
            msg   = f"built format list from file {self.format_list}"
            AppGlobal.print_debug( msg )

        if not done_where:
            pass
            msg   = "no section for where"
            AppGlobal.gui_write_progress( msg )
        file_line_reader.close_file()

    # ----------------------------------------
    def build_select_info_all( self, db_file_name, table_name, print_out=False ):
        """
        Purpose:

        Returns: zip but change in state  populates table_info s
        Raises:  consider this as return


        """
        msg   = f"build_select_info_all() for db {db_file_name}"
        AppGlobal.print_debug( msg )

        self.db_file_name    = db_file_name
        self.table_name      = table_name

        self.build_from_db_file( table_name, self.db_file_name,  print_out=False  )

        # set in init, fine just the way it is
        #self.where_list                 = []    # list of lists [ col_name, where_operator, where_value ]

        self.order_by_list              = [ [ "ROWID", "ASC" ]]    # list of lists [ col_name, direction_indicator ]

        new_format_list  = []
        column_names     = self.get_column_names( include_rowid = True )
        for i_column in  column_names:
            new_format_list.append( [i_column, "L", 5 ] )

        self.format_list = new_format_list
        msg   = f"default format list {self.format_list}"
        AppGlobal.print_debug( msg )

    # ----------------------------------------
    def build_from_db_file( self, table_name, db_file_name, print_out=False ):
        """
        Purpose:
            #    def table_to_table_info( self,  table_name, print_out=True ):
            was in table access moved to TableInfo -- could move to a factory??
            !! may return true false for success
            !! make new object for db connection include table list and other meta data??
            main point is to build a self.self.table_info
            internally Returns a list of tuples with column information:
                (id, name, type, notnull, default_value, primary_key)
        Returns: zip but change in state
        Raises:  consider this as return
        """
        self.db_file_name    = db_file_name
        self.table_name      = table_name

        table_list           = get_table_list( self.db_file_name  )

        if table_list is None:
            msg             = f" build_from_db_file() db get_table_list for '{self.db_file_name}' failed, may be that db has no tables or you have the wrong file name "
            self.error_msg  = msg
            AppGlobal.print_debug( msg )
            raise DBOjectException( msg )
            return

        if table_name not in table_list:
            msg   = f"table = '{table_name}' is not in the list of valid tables:{table_list} for '{self.db_file_name}' failed"
            self.error_msg  = msg
            AppGlobal.print_debug( msg )
            raise DBOjectException( msg )
            return

        sql_con   = lite.connect( self.db_file_name )
        cursor    = sql_con.cursor()   # !! close the cursor

        cursor.execute('PRAGMA TABLE_INFO({})'.format(table_name))
        info               = cursor.fetchall()
        # set items prior to use
        #a_table_info       = TableInfo()  # but parts need to be put together
#        self.__table_data_dict    = None  # info on table level  .table_data_dict
        #a_table_info.table_key            = AppGlobal.parameters.default_key    # should get out of dict
        self.table_name           = table_name
        data_dict    = {}

        if print_out:
            print("\nColumn Info:\nID, Name, Type, NotNull, DefaultVal, PrimaryKey")
        for col in info:
            column_id, column_name, column_type, column_not_null, column_not_null, column_primary_key = col
            data_dict[ column_name ]   = self.default_list.copy()
            if print_out:
                print(col)

        cursor.close()       # better to use a context manager

        #try add ROWID  data_dict[ "ROWID" ] = "INTEGER"   # just guessing
        data_dict[ "ROWID" ]                   = self.default_list.copy()
        data_dict[ "ROWID" ][self.ix_data_type ]    = "INTEGER"   # just guessing

        self.table_data_dict  = data_dict
        self.error_msg  = ""

        msg   = f"build_from_db_file( {db_file_name} ) made :\n"   + str( self )
        AppGlobal.print_debug( msg )
        return

    # ----------------------------------------
    def build_from_sql( self, sql_string,  print_out=True ):
        """
        Arg: sql_string containing a select
        Return:
        SELECT cell_phone, date_of_birth, name_first, name_last, name_middle, notes, ROWID FROM people   ORDER BY name_last  ASC
        how to deal with cap issues now only post table name ??? ,
        !! still needs work does not yet make table info
        in an external routine or inside here may want to make another and make sure all columns are valid and or
        get type info
        """
        # clean up
        sql_string = sql_string.lower()
        sql_string = sql_string.strip(" ")
        if not sql_string.startswith( "select " ):
            # error out
            return ( "error", "error", [] )
        # got select
        sql_string = sql_string[ 7: ]
        sql_string = sql_string.strip(" ")

        splits     =  sql_string.split( " from ", 1 )
        if len( splits ) < 2:
            # error out
            return ( "error", "error", [] )
        pre_from, post_from = splits
        col_names   = pre_from.split( "," )
        col_names   = [ i_col_name.strip( " " ) for i_col_name in col_names ]

        post_from   = post_from.strip(" ")
        splits  = post_from.split( "  ", 1 )
        if len( splits ) < 2:
            table_name ,      = splits
            post_table_name   = ""
        else:
            table_name, post_table_name = splits

        return ( table_name, post_table_name, col_names )

    # ----------------------------------------
    def build_from_input_file( self, file_name_to_read,  print_out=True ):
        """
        Arg:
        Return:
        Args:  table_info   -- where table_info will be stored, normally the caller build_from_table_info
        may move to Table Info or a factory
        This can generate all ( or most of ) a blank TableInfo by reading a file.
        result in self.table_info     FileReaderToDataDict.file_to_data_dict()
        ( change name ?? ToTableInfo )
        if it returns true then you can get it from  self.table_info
        data_dict is the beginning of a definition for the file
        right now just gets the field name and defaults type to TEXT
        Return:  change state of self.data_dict   = data_dict
        read all records in file, so or together all column names, discard data for now
        !! output to self.

        file_name_to_read  !! save it for later use
        Return: boolean
        """
        msg   = "TableInfo build_from_input_file()"
        AppGlobal.print_debug( msg )

        file_line_reader     = file_readers.FileLineReader( file_name_to_read )
        info_return = file_line_reader.get_file_info( )    # !! look at it info_return
        is_ok = file_line_reader.check_for_required_file_info( [ "purpose", "use_table"] )
        if not is_ok:
            msg = f"file_to_data_dict  {self.src_file} "
            AppGlobal.print_debug( msg )
            raise DBOjectException( msg )
            return False

        self.dict_file_info  = file_line_reader.file_info_dict
        self.table_name      = self.dict_file_info[ "use_table" ]

        data_dict      = {}
        values_added   = False
        while True:     # will the line have a newline... on it yes need to strip off end
            what, column, data = file_line_reader.get_next_line()
            #print( what, column, data )
            if what == "eof":
                break
            # break is pretty much ignored
            if what == "break":     # and values_added:
                continue
#                    msg = "------ adding record: data -------" + str( row_object )
#                    print( msg )

            else:
                values_added   = True
                is_reserved, the_word = is_reserved_word( column )
                if is_reserved:
                    msg = f"reserved word problem on line {ix_line} = {i_line} word is{the_word}"
                    print( msg )
                    self.error_msg  = msg
                    return False

                #data_val    = "TEXT"    # define all as text for now
                data_val           = self.default_list.copy()     #
                #print( name, parts[1] )
    #            self.data_object.add_value( name, parts[1] )
                if print_out:
                    msg  =  f"adding data column:  {column}:{data_val}"
                    print( msg )
                data_dict[ column ]  = data_val
                        #row_object.add_value( column, data, row_object.ix_new_value )

        msg    = f"build_from_input_file() data_dict = {data_dict}"
        AppGlobal.logger.log( logging.DEBUG, msg  )

        self.table_data_dict   =  data_dict
        #self.table_info.print_info()

        AppGlobal.logger.log( logging.DEBUG,  f"build_from_input_file()  table_info = {self }" )
        self.error_msg  = ""
        return True

    #-----------------------------------------
    def to_sql( self ):
        """
        may be obsolete or at least inconsistent with build from file
        Arg:    state of self.data_dict should first be valid .. can do with file_to_data_dict at least as a first try
        ?? make delete table if already defined ??
        Return: change state of self.data_dict_sql
        was in FileReader to data dict
        Return the sql and in self.data_dict_sql
        """
        sql       = f"CREATE TABLE {self.table_name}( "
#        " key TEXT, bot_name TEXT, common_name_1 TEXT, common_name_2 TEXT, cap_color Text )" )
        table_data_dict      = self.table_data_dict
        col_names            = list( table_data_dict.keys() )
        fields               = [ ]
        for i_col_name in col_names:

            a_field    = i_col_name + " " + table_data_dict[ i_col_name ][ self.ix_data_type ]
            fields.append( a_field )

        all_fields    = ", ".join( fields )
        sql    += all_fields + " )"

        #print( f"proposed sql is: {sql}" )
        self.data_dict_sql   = sql

        return sql

#====================================
class RowObject( object ):
    """
    A struct like thing to access a single (for now)  row in a table, more general stuff in TableAccess
    ?? methods for using that data
    ROWID
    """
    #----------- init -----------
    def __init__(self, table_info ):     # expand the init to set more stuff is this a TableInfo

        self.table_info       = table_info    # info on table level
        self.edit_dict        = None          # holds the row in 2 lists, one for data in db, one for data that is external
                # { column name: [db_value, new_value]  }   ix_db_value, ix_new_value ......... d = collections.OrderedDict()

        # -------------- constants index into list of the edit_dict
        self.ix_db_value      = 0
        self.ix_new_value     = 1

        self.init_data( )

    # -----------------------------------
    def init_data( self,  ):
        """
        continues __init__
        but might be used by itself perhaps
        created an edit dict which has a column name and data ... data is a list, index in init
        """
        table_data_dict   = self.table_info.table_data_dict      # local name may or may not help
        # could just copy and rinit the data but no
        self.edit_dict   = {}
        for i_colum_name in table_data_dict:
            self.edit_dict[ i_colum_name ] =  [None, None]

    # -----------------------------------
    def clear_edit_dict( self,  ):
        """
        Purpose:  clear the data from the edit dict, but keep the column names
        """
        # could just copy and rinit the data but no
        #self.edit_dict   = {}
        for i_colum_name in self.edit_dict:
#            msg = f"clear edit dict for {i_colum_name}"
#            print_debug( msg )
            self.edit_dict[ i_colum_name ]  = [ None, None ]
#        print( self.edit_dict )

    # -----------------------------------
    def column_name_valid( self, column_name,  ):
        """
        Purpose:
            but is this for dup check existence check what
            see name, note that proper cap of column name is required.
            perhaps better in table access !! also check against module reserved words
            !! also need table name valid
        """
        is_valid    = column_name in self.edit_dict
        return is_valid

    # -----------------------------------
    def add_value( self, column_name, column_data, ix_new_old ):
        """
        add a value to the dict item  -- think not table info but more like row object ??
        index points to the new old value
        xxxx will create new items in the dict if not already there !!  -- check valid
        """
        is_ok   = self.column_name_valid( column_name )

        if is_ok:
            i_list                   = self.edit_dict[ column_name ]   # no this can throw error
            i_list[ ix_new_old ]     = column_data
        return is_ok

    # -----------------------------------
    def get_value( self, column_name,  ix_new_old ):
        """
        index points to the new old value

        """
        is_ok   = self.column_name_valid( column_name )   # !! need to manage this
        if is_ok:
            # compress to one line
            i_list                   = self.edit_dict[ column_name ]   # no this can throw error
            column_data              = i_list[ ix_new_old ]
        return column_data

    # -----------------------------------
    def changed_data( self,  ):
        """
        temp compare of old and new, print new
        is this right, why going back to table_access
        !! think not used but if is may need null value check
        """
        data_info     = self.table_access.table_info.table_data_dict   # local name may or may not help

        for i_colum_name in data_info:
            values    = self.edit_dict[ i_colum_name ]       # hope we get a new one each time
            if values[ self.ix_db_value ] == values[ self.ix_new_value ]:
                    print( f"need update on {i_column_name}" )

    # -----------------------------------
    def make_insert_sql( self, ):
        """
        create the sql and data in tuple -- this is insert so skip ROWID
        self.edit_dict

        Returns  ( full_sql, data_list )
        """
        # we now have rowid so need to decrease count by 1 ?? ( or take counts to inside the loop
        sql_begin             = F"INSERT INTO {self.table_info.table_name} "   #"( Id, Name, Price ) VALUES (?, ?, ?)", cars)

        col_names             = list( self.edit_dict.keys() )
        col_names.remove( "ROWID" )

        sql_col_names         = "(" +  ", ".join( col_names ) + " )"

        qmarks                = "( " + "?, " * len( col_names )
        qmarks                = qmarks[ : -2 ] + ")"

        data_list             = []

        for i_col_name in col_names:
#            if i_col_name == "ROWID":
#                continue
            # ?? looks like I contracted several lines to 1 comment out unneeded
            dict_val     = self.edit_dict[ i_col_name ]
            data         = dict_val[ self.ix_new_value ]
            data_list.append( self.edit_dict[ i_col_name ][ self.ix_new_value ] )

        full_sql              = sql_begin + sql_col_names + f" VALUES {qmarks}"

        data_list    = ( tuple( data_list ), )
        #print( data_list )

        # these are not really my attributes !! delete
        self.full_sql    = full_sql
        self.data_list   = data_list

#        print( "====== returning from make insert =========" )
#        print( full_sql,  flush = True )
#        print( data_list, flush = True )

        return ( full_sql, data_list )

    # -----------------------------------
    def make_update_sql( self, ):
        """
        Purpose:
            make update sql tuple from date in self, also need info from self.table_info
        create the sql and data in tuple
        Returns  ( full_sql, data_list )
        """
#        '''UPDATE books SET price = ? WHERE id = ?''', (newPrice, book_id))
        msg  = f"make_update() are we the right row object ??? \n {self}"
        AppGlobal.print_debug( msg )

        sql_begin             = F"UPDATE {self.table_info.table_name} "   #"( Id, Name, Price ) VALUES (?, ?, ?)", cars)

        col_names             = list( self.edit_dict.keys() )
#        sql_col_names         = "(" +  ", ".join( col_names ) + " )"
#
#        qmarks                = "( " + "?, " * len( col_names )
#        qmarks                = qmarks[ : -2 ] + ")"

        update_names          = []
        data_list             = []

        for i_col_name in col_names:
            # ?? looks like I contracted several lines to 1 comment out unneeded
            dict_val     = self.edit_dict[ i_col_name ]
            data         = dict_val[ self.ix_new_value ]
            data         = fix_null( data )
            data_db      = fix_null( dict_val[ self.ix_db_value ] )
            if data == data_db:
                # AppGlobal.print_debug( f"old and new data equal.... {data} == {data_db} " )
                continue   # data unchanged skip
            else:
                AppGlobal.print_debug( "append.... {i_col_name}" )
                update_names.append( i_col_name )
                data_list.append(    data     )

        if len( data_list ) == 0:
            # no sql no data
            full_sql    = ""
            data_list   = tuple( data_list )

        else:
            sets                  = [ f"SET {i_update_names} = ? " for  i_update_names in update_names ]
            sql_sets         = ", ".join( sets )

            sql_where             = f" WHERE {self.table_info.table_key}   = ? "
    #        data_list.append( self.edit_dict[ i_col_name ][ self.ix_new_value ] )

            # old and new values depend on index  self.ix_db_value self.ix_new_value
            key_value_new   = self.edit_dict[ self.table_info.table_key ][ self.ix_new_value ] # this is the new key value should be same as old do a test !!

            key_value_db    = self.edit_dict[ self.table_info.table_key ][ self.ix_db_value ] # this is the new key value should be same as old do a test !!

            if  key_value_new != key_value_db:
                 msg     =  f"edit changed the key column which is a different record and ng original: >>{key_value_db}<< new: >>{key_value_new}<<"
                 #print_debug( debug_msg )
                 print( msg )  # !! send to gui
                 AppGlobal.controller.write_gui( msg  )
                 AppGlobal.logger.debug( msg )
                 raise DBOjectException( msg )

            data_list.append(   key_value_db  )

            full_sql              = sql_begin + sql_sets + sql_where  # + #f" VALUES {qmarks}"
#            data_list             = ( tuple( data_list ), )   # data list still needs primary key -- done ??
            data_list             = tuple( data_list )
            #print( data_list )

        # these are not really my attributes !! delete
        self.full_sql    = full_sql
        self.data_list   = data_list

#        print( "====== returning from make insert =========" )
#        print( full_sql,  flush = True )
#        print( data_list, flush = True )
        msg       = f"( full_sql, data_list )  {( full_sql, data_list )}"
        AppGlobal.print_debug( msg )
        AppGlobal.controller.write_gui( msg  )
        # AppGlobal.logger.debug( msg ) # not required with print debug
        return ( full_sql, data_list )

#    # -----------------------------------
#    def clear_values( self,   ):
#        self.data_in_dict   = {}

#    # -----------------------------------
#    def no_values( self ):
#        return len( self.data_in_dict )

#    # -----------------------------------
#    def print_values( self, ):
#        pass

#    def __repr__(self):
#         return "RowObject __repr__ thats all "

    # -----------------------------------
    def __str__(self):
        """
        mostly for debug, work on as needed
        """
        lines     = []

        i_line    = "============--------RowObject--------====================="
        lines.append( i_line )

        i_line    = f"{self.__class__.__name__ } __str__()"
        lines.append( i_line )

        i_line    = f"edit_dict: {str( self.edit_dict )}"
        lines.append( i_line )

        return "\n".join( lines )

#-------------------------------------
class TableAccess( object ):
    """
    Provide access and debugging for a table described by table_info
        selects  where and order by
        inserts
        updates
        exports  -- kind of select
        deletes


        its info about the table is based on a TableInfo object
        and data may be buffered in a RowObject
        a FileReader may be used to access user data


    Args:

    If you init without a table info you might fix with:

    table_access  = db_objects.TableAccess( db_file_name,  None )
    table_access.table_to_table_info( table_name )  --- function now gone, table info can populate itself

    """
    #----------- init -----------
    def __init__( self, db_file_name, table_info ):
        """
        Args:
            db_file_name     Not None, trouble if does not open correctly
            table_info       describes the file, build outside this object
                             -- can be none then use: init_table_info_from_db which lets
                             you define it using the table name

        """

        self.db_file_name    = db_file_name     # can be set  later a_table_access.db_file_name =
                                                # may be used to build a file_info as in check_file
        self.table_info      = table_info      # can be set  later a_table_access.db_file_name  =

        # -------- other
        self.row_object      = None   # used by edit_one_record_1 .. 2
#        ---------- ?? implement ???
        self.where_operators  = [ "=", "<", ">",  "<=", ">=", "like" ]    # !! still needs work

    # -----------------------------------
    def init_table_info_from_db(self, table_name ):
        """
        """
        self.table_info      = TableInfo( )
        self.table_info.build_from_db_file( table_name, self.db_file_name, print_out=False )

    # -----------------------------------
    def __str__(self):

        lines     = []

        i_line    = "============--------TableAccess as __str__() --------====================="
        lines.append( i_line )

        i_line    = "TableAccess __str__()"
        lines.append( i_line )

#        i_line   = str( self.data_info )
#        lines.append( i_line )

        str_so_far   =  "\n".join( lines )
        str_so_far   +=  self.data_info_to_str()

        return str_so_far

    #--------------------------------
    def new_row_object( self, file_name ):
        """
        !! looks ng, call to row object has a file_name
        """
        self.row_object      = RowObject( self,  file_name )

    # ------------------ select type functions -------------------

    #--------------------------------
    def run_info_sql( self, ):
        """
        Purpose: see name -- may be ok for deletes ....

        Args:
                self.table_info
        Returns: zip
        Raises: none planned but could have bad sql....
        """
        # unless changed we already have table info so that ....
        # self.table_info.build_select_sql_from_file(  self.db_file_name, input_file_name, print_out=False )
        sql      =  self.table_info.sql
        qmarks   =  self.table_info.qmarks

        msg      = f"run_info_sql_with_writer self.table_info  {self.table_info}"
        AppGlobal.print_debug( msg )

#        # sql in table_info so do not need this
#        msg      = f"sql =   {sql}"
#        AppGlobal.print_debug( msg )

        col_names         = [ i_format[0] for i_format in self.table_info.format_list ]

        sql_con = lite.connect( self.db_file_name )
        with sql_con:
            cur    = sql_con.cursor()
            cur.execute( sql )

    #--------------------------------
    def run_info_sql_delete( self,   ):
        """
        Purpose: see name
                same as:  run_info_sql ??
        Args:   select_writer = a file_writer to write the output
                self.table_info
        Returns: zip
        Raises: none planned but could have bad sql....
        """
        sql      =  self.table_info.sql
        qmarks   =  self.table_info.qmarks

        msg      = f"run_info_sql_delete self.table_info  {self.table_info}"
        AppGlobal.print_debug( msg )

        # sql in table_info
        msg      = f"sql =   {sql}"
        AppGlobal.print_debug( msg )

        sql_con = lite.connect( self.db_file_name )
        with sql_con:

            cur    = sql_con.cursor()
            cur.execute( sql )

    #--------------------------------
    def run_info_sql_with_writer( self, select_writer ):
        """
        Purpose: see name

        Args:   select_writer = a file_writer to write the output
                self.table_info
        Returns: zip
        Raises: none planned but could have bad sql....
        """
        # unless changed we already have table info so that ....
        # self.table_info.build_select_sql_from_file(  self.db_file_name, input_file_name, print_out=False )
        sql      =  self.table_info.sql
        qmarks   =  self.table_info.qmarks

        msg      = f"run_info_sql_with_writer self.table_info  {self.table_info}"
        AppGlobal.print_debug( msg )

        # sql in table_info
        msg      = f"sql =   {sql}"
        AppGlobal.print_debug( msg )

        col_names         = [ i_format[0] for i_format in self.table_info.format_list ]

        select_writer.write_header(  )

        row_object     = RowObject( self.table_info )

        sql_con = lite.connect( self.db_file_name )
        with sql_con:
            cur    = sql_con.cursor()
            cur.execute( sql )
            rows   = cur.fetchall()

            for row in rows:
                row_object.clear_edit_dict()

                for ix_col, i_col in enumerate( col_names ):
                    i_data    = fix_null( row[ ix_col ] )
                    row_object.add_value( i_col, i_data, row_object.ix_db_value )
                select_writer.write_row( row_object )

            select_writer.write_footer( None )

    #--------------------------------
    def compare_two( self, id_1, id_2  ):  # output only for fields that have data
        """
        !! implement out to file with default to None
        print down in columns ... will have to figure out wrap text .. maybe even html
        make_select_from_info(
        """
        sql_base    = self.make_select_from_info()
        sql_con     = lite.connect( self.db_file_name )

        #print( "=========== select_all ===========" )
        col_names            = list( self.table_info.table_data_dict.keys() )
        key_column_name      = self.table_info.table_key
        with sql_con:
            # !! fix so key comes from data_infos
            cur       = sql_con.cursor()
            sql       = sql_base  + f" WHERE {key_column_name}=:key"
            print( sql )
            cur.execute( sql, {"key": id_1})
            row_1       = cur.fetchone()

            cur.execute( sql, {"key": id_2})
            row_2       = cur.fetchone()

            print( row_1 )
            print( row_2 )

            print( "fix for null " )

            for ix_col, i_col in enumerate( col_names ):
                i_data_1    = fix_null( row_1[ ix_col ] )
                i_data_2    = fix_null( row_2[ ix_col ] )

                if ( i_data_1 != "" and  i_data_2 != "" ):
                    i_line    = f"{i_col}:{i_data_1}  >>>  {i_data_2}"

                    print( i_line )
                    #fileout.write( i_line   + "\n" )
            #fileout.close()

    #--------------------------------
    def get_one_row( self, key, ):  # output only for fields that have data
        """
        Purpose:
        get on record use key field
        if fails return none or raise and except??
        Returns:  a RowObject
        Raises:
            Side Effects: does not set self.row_object, so later we might have several??

        !! move in with select where ??
        """
        a_row_object   = RowObject( self.table_info )

        sql_base       = self.make_select_from_info()
        sql_con        = lite.connect( self.db_file_name )

        #print( "=========== select_all ===========" )
        col_names            = list( self.table_info.table_data_dict.keys() )
        key_column_name      = self.table_info.table_key
        with sql_con:

            msg       = f"key_column_name = >>{key_column_name}<<"
            print( msg )
            AppGlobal.logger.debug( msg )

            cur       = sql_con.cursor()
            sql       = sql_base  + f" WHERE {key_column_name}='{key}'"

            msg       = sql
            print( msg )
            AppGlobal.logger.debug( msg )

            #cur.execute( sql, { key_column_name: key})   # this may be better form non inject
            cur.execute( sql, )
            row_1       = cur.fetchone()
            msg = f"get_one_row() on key {key} got {row_1}"
            AppGlobal.logger.debug( msg )
            if row_1 is None:
                msg   = msg + " failed to find row"
                print( msg )
                AppGlobal.logger.debug( msg )
                raise DBOjectException( msg )

            AppGlobal.logger.log( logging.DEBUG, msg )
            #print( "fix for null " )
            # !! need error for not found think row_1 comes back None
            for ix_col, i_col in enumerate( col_names ):
                #i_data_1    = fix_null( row_1[ ix_col ] )
                col_value   = row_1[ ix_col ]
                a_row_object.add_value( i_col, col_value,  a_row_object.ix_db_value )

            #fileout.close()
            msg   = f"\nget_one_row() row object= {a_row_object}"
            AppGlobal.print_debug( msg )

            return a_row_object

    #--------------------------------
    def make_table_form( self, output_file_name, ):
        """
        make a blank form in a file for one record
        add fancy self naming for file later
        !! add table name at top
        ?? use file writer or is this simpler
        !! add export select form
        """
        col_names            = list( self.table_info.table_data_dict.keys() )
        key_column_name      = self.table_info.table_key

        fileout = open( output_file_name, "w" )    # a for append  w for write as new?

        fileout.write( f"# 'table form' created for table = {self.table_info.table_name} for the database file = {self.db_file_name}\n" )
        fileout.write( f"use_table:{self.table_info.table_name}\n" )
        fileout.write( "purpose:insert\n" )
        fileout.write( "# next line marks the end of the introductory information and the beginning of the data\n" )

        fileout.write( ":====================\n" )

        for ix_col, i_col in enumerate( col_names ):

            i_line    = f"{i_col}:"
            #print( i_line )
            fileout.write( i_line   + "\n" )

        fileout.write( "# you should have a line marking the end of the data\n" )
        fileout.write( ":====================\n" )
        fileout.close()

    # ------------------ insert/update type functions -------------------
    #-----------------------------------------
    def define_table_from_table_info( self, ):  # db_file_name, table_info )
        """
        pass as arguments or args here ???
        !! need error management throw except
        """
        table_info    = self.table_info
        sql           = table_info.to_sql()
        table_name    = table_info.table_name

        sql_con = lite.connect( self.db_file_name )
        with sql_con:
            cur = sql_con.cursor()
            cur.execute( f"DROP TABLE IF EXISTS {table_name}" )
            print( sql )
            execute_ret =  cur.execute( sql )
            print( execute_ret )
            msg   = f"table {table_name} defined in file {self.db_file_name}"
            print( msg )

    #--------------------------------
    def edit_one_record_1( self, key_value, edit_file_name ):
        """
        retrieve a record, write to file, then read the file and update
        probably needs to be divided into 2 functions
        because of init we do not need db_file_name or table_name
        table_access.edit_one_record_1()
        Args:  ?? record key
                  edit_file_name
                  others

        !! some may be merged or use file_writers and select where   or not
        """
        a_row_object          = self.get_one_row( key_value, )
        self.row_object       = a_row_object    # pass to second phase _2
        self.edit_file_name   = edit_file_name

        AppGlobal.table_access_for_edit = self   #  pass to second phase _2

        lines         = []

        i_line   = f"# program is {AppGlobal.controller.app_name} {AppGlobal.controller.app_version}  "
        lines.append( i_line )

        i_line   = f"purpose:edit"
        lines.append( i_line )

        i_line   = f"use_table:{ self.table_info.table_name }"
        lines.append( i_line )

        i_line   = f"# key is { self.table_info.table_key }, key value is {key_value}"
        lines.append( i_line )

        fileout = open( edit_file_name, "w" )    # a for append  w for write as new?

        i_line    =  "\n".join( lines )
        fileout.write( i_line   + "\n" )

        fileout.write( ":====================\n" )

        edit_dict    = a_row_object.edit_dict
        column_names = ( edit_dict.keys() )
        for i_colum_name in column_names:
            values    = edit_dict[ i_colum_name ]
            value     = values[ a_row_object.ix_db_value ]
            i_line    = f"{i_colum_name}:{value}"
            fileout.write( i_line   + "\n" )
#            print( i_colum_name, value  )

        i_line    =  ":===================="
        fileout.write( i_line   + "\n" )

        fileout.close()

        os_open_text_file( edit_file_name )

    #--------------------------------
#    def edit_one_record_2( self, key_value, edit_file_name ):
    def edit_one_record_2( self,   ):
        """
        retrieve a record, write to file, then read the file and update
        probably needs to be divided into 2 functions
        because of init we do not need db_file_name or table_name
        Args:  ?? record key
                  edit_file_name
                  others
        """
        row_object        = self.row_object  # pass to second phase _2 still contains old data

        print("\n============== edit_one_record_2() ==========================")
        #print( f"row_object.table_access.db_file_name = {row_object.table_access.db_file_name}" )

        #y=1/0  # next line may not be fully implemented
        a_file_reader       = file_readers.FileReader( self.edit_file_name,
                                          self.row_object.table_info.db_file_name,   )

#        msg    = str( a_file_reader )
#        print_debug( msg )
#        AppGlobal.logger.debug( msg )

#        msg  = "edit_one_record_2() self.row_object {self.row_object}"
#        print_debug( msg )
#        AppGlobal.logger.debug( msg )

        #updates the row object not the db
        a_file_reader.update_from_file( self.edit_file_name, self.row_object  )

        # have the row object back here now run the update
        sql, values_where = self.row_object.make_update_sql()

        sql_con = lite.connect( self.db_file_name )
        with sql_con:
#            AppGlobal.logger.debug( sql )
            cur = sql_con.cursor()
            cur.execute( sql, values_where )

        msg = "done edit_one_record_2<<<<"
        AppGlobal.controller.write_gui( msg  )
        AppGlobal.print_debug( msg )

    # -----------------------------------
    def make_insert( self, ):
        """
        an insert
        create the sql and data in tuple
        Returns  ( full_sql, data_list )
        """
        sql_begin           = F"INSERT INTO {self.table_name} "   #"( Id, Name, Price ) VALUES (?, ?, ?)", cars)

        col_names            = list( self.data_in_dict.keys() )

        qmarks                = "( " + "?, " * len( col_names )
        qmarks                = qmarks[ : -2 ] + ")"

        sql_col_names         = "(" +  ", ".join( col_names ) + " )"

        data_list             = []

        for i_col_name in col_names:
            data_list.append( self.data_in_dict[ i_col_name ] )

        full_sql              = sql_begin + sql_col_names + f" VALUES {qmarks}"
        #print( full_sql )

        data_list    = ( tuple( data_list ), )
        #data_list    = tuple( data_list )
        #print( data_list )

        self.full_sql    = full_sql
        self.data_list   = data_list

        return ( full_sql, data_list )

   #--------------------------------
    def insert_with_row_object( self, row_object ):
        """
        replaces  update_with_data_object(
        ?? or use self data object or other way around  == is this used if now why not update_with_row_object
        """
        full_sql, values    = row_object.make_insert_sql()    # think now row_object make insert
        msg                 = f"insert_with_row_object full_sql >>{full_sql}<<>>{values}<<"
        AppGlobal.print_debug( msg )
        sql_con             = lite.connect( self.db_file_name )

        with sql_con:
            cur = sql_con.cursor()
            #cur.execute("CREATE TABLE Cars(Id INT, Name TEXT, Price INT)")
            cur.executemany( full_sql, values )

   #--------------------------------
    def update_with_row_object( self, row_object ):
        """
        update instead of insert above, need to implement
        """
        row_object.changed_data()  # temp for debug

        y=1/0

    # ------------- helper methods ---------------
    #--------------------------------
    def parse_operator( self, operator_data  ):
        """
        !! think obsolete, or move ??
        separate operator from the data -- quote the data ??
        return tuple ( ok, operator, data )   operator may have case shift, data should not
        """
        msg_debug = f"operator_data = {operator_data}"
        AppGlobal.print_debug( msg_debug,   )
        operator_data = operator_data.replace( " ", "" )
        #operator_data_lower = operator_data.lower()
        ok = False
        for i_operator in self.where_operators:
            # print( i_operator )
            if operator_data.lower().startswith( i_operator ):
                #print( i_operator )
                data        = operator_data[ len(i_operator) : ]
                # should check for valid data
                data        = f'"{data}"'
                ok          = True
                operator    = i_operator   # not rely on loop side effect
                break
        if not( ok ):
            operator    = ""
            data        = ""
        ret = ( ok, operator, data )
        #print( f"ret = {ret}", flush = True )
        return ret
# ----------------------------------------
def build_column_info():
    """
    a data dictionary like thing for selects
    right now more or less a literal
    !! still getting developed, and features added

    Returns:  column_info

    column_info  dict of dicts outer key, column name ( and p

# -*- coding: utf-8 -*-


basic database operations and objects
/mnt/WIN_D/Russ/0000/python00/python3/_projects/easy_db/db_objects.py
"""

# ------------------ module functions


#--------------------------------
def fix_null( possible_null  ):  # change various nulls to empty string
    """
    in general my approach to nulls is not thought out
    """
    ret    = possible_null
    if ret == "null string":
        ret = ""
    if ret == "None":
        ret = ""
    if ret is None:
        ret = ""
    return ret


#--------------------------------
def get_table_list( db_filename  ):
    """
    Return:   list of table names None if db connect does not work
    None if a connect fail of some sort, and could be empty list if no tables
    Raise:
    """
    msg       = f"get_table_list: start connect to {db_filename}"
    AppGlobal.print_debug( msg )

    name_list  = []
    try:
        #con       = lite.connect( db_filename )
        con       = lite.connect( db_filename, check_same_thread = False )   # did not fix my problem
        #  check_same_thread is True and only the creating thread may use the connection. If set False,
    except Exception as exception:
        msg       = f"get_table_list: connect exception {exception}"
        AppGlobal.print_debug( msg )

        msg       = f"get_table_list: connect to {db_filename} failed"
        AppGlobal.print_debug( msg )
        return None

    cursor    = con.cursor()
    cursor.execute( "SELECT name FROM sqlite_master WHERE type='table';" )
    # think we get a list of tuples  -- !! try this
    a_list   = cursor.fetchall()
    con.close()
    # cursor.close()
    print( a_list )
    # what looks like simplifying a list of tuples to a list of strings, do with comprehension
    for i_name in a_list:
        AppGlobal.print_debug( i_name )
        a_name, = i_name
        AppGlobal.print_debug( a_name )
        name_list.append( a_name )

    return name_list

def begin_with_alpha( a_word ):
    """
    what it says  !! need implementation
    """

    return True


#-----------------------------------------
def is_reserved_word( a_word ):
    """
    for checking if column names table names  are reserved words do not use for other words ?
    return tuple ( True, the_word )
    the word may differ in case ?? is this what we want
    is_ok, new_word  = db_objects.is_reserved_word( a_word )
    """
    a_word   = a_word.lower()
    reserved_list  = [ "where", "select", "order_by", "from" "order", "by", "like", "delete",
                       "join",  "union" ]
    for i_reserved in reserved_list:
        if i_reserved == a_word:
             return ( True, i_reserved )
    return ( False, "" )

#-----------------------------------------
def is_in_select_list( column_name, where_list ):
    """
    Purpose:
    see code
    """
    for i_where_list in where_list:
        if i_where_list[0] == column_name:
            return True
    return False


# =================================================

# if __name__ == "__main__":
#     #----- run the full app
#     import  easy_db
#     app   = easy_db.App(   )

# =================== eof ==============================
