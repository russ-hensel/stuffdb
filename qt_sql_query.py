#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 10:52:28 2024

@author: russ
"""



"""
look in twitter

import sqlite3 as lite


table

have some sort of data dict that draws for sql lite dict and is perhap
enhanced by some aux table or tables


"""

# ---- imports

from  tkinter import messagebox
# import collections
import sqlite3 as lite
import time
import datetime

# ------- local imports
# from   app_global import AppGlobal
# import app_global
# import string_util
#import file_writers
#import pseudo_column
#import sql_writers
import    string_util
from   app_global import AppGlobal


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
    def __init__( self,  qt_query, print_it = True, logger = None, write_gui = None  ):
        # ---- part of interface


        # use these when building so little mutating routines  like add_to_where work

        # self.sql_where        = ""
        # self.sql_having       = ""
        # self.sql_from         = ""
        # self.sql_data         = []    # parameters passed to sql
        # self.row_count        = 0


        self.print_it                = print_it
        self.qt_query                = qt_query
        self.write_gui               = None     # see:
        self.sql_from                = None     # see:
        self.arg_dict                = None     # see:
        self.sql_where               = None     # see:
        self._sql                    = None     # see:
        self.sql_having              = None     # see:
        self.column_list             = None     # see:
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
            mutates self, pretty much forgets everythinb but .....
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
    def col_list_to_sql( self, col_list,      ):
        """

        return
             string like: (  col_aaa, col_bbb, col_ccc, col_ddd, col_eee, col_fff  )    "
         """
        sql_columns    = " "

        for i_name in col_list[ : -1]:
            sql_columns = ( f"{sql_columns} {i_name}, " )
        sql_columns = ( f"{sql_columns} {self.column_list[ -1]}  " )

        return sql_columns


   # ----------------------------------------------
    def prepare_and_bind( self,      ):
        """
        Args:

        Returns:
            mutates self.qt_query

        """
        sql      = self.get_sql()
        self.qt_query.prepare( sql )
        for i_bind_tuple in self.bind_list:
            self.qt_query.bindValue(  *i_bind_tuple )

        if self.print_it:
            print( f"{sql = }")


   # ----------------------------------------------
    def get_sql( self,      ):
        """

        this is select sql features not complete


        """
        #sql        =   f"SELECT *  FROM {self.table_name}  "

        sql_columns          = self.col_list_to_sql( self.column_list )
        self._sql            = f"SELECT {sql_columns}  FROM {self.table_name}  "


        if self.sql_inner_join:
            self._sql        = f"{self._sql}\n{self.sql_inner_join} "

        self._sql            = f"{self._sql } {self.sql_where} "

        if self.sql_order_by:
            self._sql        = f"{self._sql}\n{self.sql_order_by} "

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
                second componnt of tuple is  value of bind var, of appropriate type

        """
        if self.sql_where == "":
            self.sql_where  = "\n WHERE "
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
        a_str   = string_util.to_columns( a_str, ["sql_from",
                                           f"{self.sql_from}" ] )
        a_str   = string_util.to_columns( a_str, ["sql_having",
                                           f"{self.sql_having}" ] )
        a_str   = string_util.to_columns( a_str, ["sql_order_by",
                                           f"{self.sql_order_by}" ] )
        a_str   = string_util.to_columns( a_str, ["sql_where",
                                           f"{self.sql_where}" ] )
        a_str   = string_util.to_columns( a_str, ["table_name",
                                           f"{self.table_name}" ] )
        a_str   = string_util.to_columns( a_str, ["write_gui",
                                           f"{self.write_gui}" ] )
        a_str   = string_util.to_columns( a_str, ["bind_list",
                                           f"{self.bind_list}" ] )

        return a_str


# ----------------------------------------
class SQLBuilder_fromstructurednotes(   ):
    """
    from structured notes  may be more classes of interest
    build sql based on criteria ( all should be in reset )
    then pushed in by external methods setting values
    not all criteria used by all methods ?
    always use fully qualified table names

    Build and output
        for output need to know    target... file_name
                                   format or type
                                   append option

    """
    def __init__( self, table_info  ):
        """
        what it says .. for now it seems subclasses should make super call
        """
        print( "init SQLBuilder")
        self.table_info        = table_info
        self.table_name        = self.table_info.table_name
        self.check_title       = "Check Select"
        self.check_run_select  = "Would you like still continue ?"
        # arguments push in ... or ususal args ??

        self.info              = None
        self.file_writer       = None
        self.db_file_name      = None
        self.select_name       = "Default Select Name"
        self.help_mode         = "default help mode"  # means what

        self.output_name       = "./sql_output.txt"   # may need to modify based on type
        self.output_append     = "Append"
        # self.file_name              = builder.output_name
        # self.columns_out            = builder.columns_out
        # self.columns_info           = builder.columns_info
        self.db_name            = table_info.db_file_name

        self.reset()

    # ------ helpers
    # ----------------------------------------------
    def reset( self,  ):
        """
        reset criteria -- not everythong
        try to define most instance var. here to eliminate reporting errors
        Return: mutates self

        think there is a file writer as well

        """
        #self.columns_info       = build_column_info()  # dict of dicts info on each column by fully qualified column name
        # self.db_name            = ""
        self.output_format      = "tablexxx"  #  "html"......
        #self.db_name            = ""
        self.output_name        = None
        self.columns_out        = None     # list of names in order for the column output
        self.help_file          = "./help/build_for_default.txt"  # change to generic

        self.help_mode          = True
        self.a_word             = ""    # word for select criteria, in some cases a string
        self.my_count           = None
        self.is_covid           = ""    # select criteria on tweet
        self.default_order_by   = ""
        self.gui_order_by       = ""
        self.word_type          = "get_error"

        self.tweets_word_select     = ""
        self.words_word_select      = ""
        self.max_count          = 0     # unlimited
        self.begin_dt               = datetime.datetime( 1945, 5, 24, 17, 53, 59 )
        self.end_dt                 = datetime.datetime(   1945, 5, 24, 17, 53, 59 )

        self.select_name        = "A select- name not set "   # user oriented name, same as in dropdown -- can dropdown pass itself with lambda

        self.start_time         = 0    # probably time.time() start of select
        self.end_time           = 0

        self.select_msg         = ""    # a message generated during the select ... ?? may just be an idea

        # list to check may not be present in any given select ... this code will hang around is it too much ?? delete
        # self.pseudo_columns     = [   PseudoColumnRowCount(         self ),
        #                               PseudoColumnTotalWordRank(    self ),
        #                               PseudoColumnRa_Word_Rank(     self ),
        #                               PseudoColumnRa_Word_Length(   self ),
        #                               PseudoColumnRa_Word_Null(     self ),
        #                               PseudoColumnRa_Word_Null(     self ),
        #                               pseudo_column.PseudoColumnSumCountBins(     self ),
        #                           ]

        self.pseudo_columns     = []

        self.row_functions      = []    # called for each row, used with pseudo columns  not currently in structured_notes
        self.footer_functions   = []    # called for the footer

        self.message_function   = None   # set to a function message_function( msg ) for progress messages ?? not implemented

        self.output_append      = None

        self.aux_select         = None   # for now I am thinking used in file_writer write row, but may just be another row_function

        self.reset_sql()

    # ----------------------------------------------
    def reset_sql( self,  ):
        """
        what it says
        return mutate self  --- not sure it should differ from reset
        """
        # use these when building so little mutating routines  like add_to_where work
        self.sql              = ""
        self.sql_where        = ""
        self.sql_having       = ""
        self.sql_from         = ""
        self.sql_data         = []    # parameters passed to sql
        self.row_count        = 0

        self.row_functions    = []    # functions called on each row, producing column dat
        self.prior_row        = None
        self.row_to_list      = False  # convert row to a list for manipulation



   # ----------------------------------------------
    def grouping_row_function( self  ):
        """
        use to suppress rows only letting every nth row thru
        seems to need access to its own instance var,
        should this be in builder in its own object.... is this a good
        place for a partial?  should it be set up sort of like a file writer?
        ?? how will it interact with row count
        or rather than do something new just use a psudo column ... but how to init it
        but this will add a new column
        """
        pass


   # ----------------------------------------------
    def display_help( self  ):
        """
        user interaction:
        display help for this report
        """
        pass
        # AppGlobal.gui.do_clear_button( "dummy_event")
        # with open( self.help_file, "r" ) as a_file:
        #     lines = a_file.readlines()
        #     # print( lines )
        #     msg  = "".join( lines )
        #     AppGlobal.gui.display_info_string( msg )
        # return

    # ----------------------------------------------
    def confirm_continue_0( self,   ):   #  help_mode = False
        """
        adding more common code to confirm_continue, experimenting with factoring

        """
        pass
        # # next is standard this is the refactor ??

        # if self.help_mode or self.output_format != "msg":
        #     self.display_help()
        #     info_msg     =    f"sql is:\n{self.sql}\n"
        #     AppGlobal.gui.display_info_string( info_msg )
        #     info_msg     =    f"sql_data is:\n{self.sql_data}"

        # info_msg     = ""
        # self.confirm_continue( info_msg, self.check_title,   self.check_run_select, )

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

        print( f"builder confirm_continue {help_mode}")

        AppGlobal.gui.display_info_string( info_msg )

        # if help_mode:
        #     raise app_global.UserCancel( "Mode: Help only, query not run" )

        if AppGlobal.parameters.confirm_selects:   #  !! may still need adjust for msg format

            continue_flag  = messagebox.askokcancel( a_title, msg )

            if continue_flag is not True:
                AppGlobal.gui.display_info_string( "Operation canceled" )
                raise app_global.UserCancel( "user: Operation canceled" )

    # ----------------------------------------------
    def select_and_output( self, max_rows = 0 ):
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

        # now made ealier .. injected
        # file_writer         = file_writers.make_file_writer( self  )
        # self.file_writer    = file_writer  # copy for AuxSelect.....


        self.file_writer.write_header( self.table_info )

        msg     = f"Select and output; connect to {self.db_name}"
        print( msg )
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
                self.write_row   = True   # this allows pseodo columns to suppress output
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

        print(  footer_info )
        msg      =  f"select complete with footer info: {footer_info}"
        AppGlobal.logger.debug( msg )

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

  # ----------------------------------------------
    def go( self,  ):
        """
        after all setup is done go and do the select
        arg:  which select in builder to run, later when sub-classed just go
        """
        print( "SQLBuilder builder.go() ")
        AppGlobal.gui.clear_message_area( ) # check this actually works in real time !!
        try:
            self.this_select()          # configured for one of self.  ... with sub-classing always the same
            print( "after this select", self.get_info_string( )    )

            self.select_and_output()    # help_mode ??

        except app_global.UserCancel as exception:   #  !!this is probably the righ one
        #except Exception as exception:
            pass  # Catch the  exception and swallow as user wants out not an error
            print( exception )  # debug only

        msg   = f"Select Done, rows selected: {self.row_count} time = {self.end_time - self.start_time}"
        AppGlobal.gui.display_info_string( msg )
        AppGlobal.logger.debug(  msg  )

   # ----------------------------------------------
    def format_sql_for_user( self  ):
        """
        ?? finish me ... I go back and forth on this, now leaning towards
        mutate self
        """
        self.display_sql   = "not implemented"

   # ----------------------------------------------
    def build_writer( self  ):
        """
        return a sql writer
        """
        pass


# ----------- where methods
   # ----------------------------------------------
    def add_to_where( self,    add_where = None, add_data = None,   ):
        """
        add on to where clause ok if starts at 0.  assumes and between clauses
        return mutates self -- in particular  self.sql_where self.sql_data
        """
        if self.sql_where == "":
            self.sql_where  = "\n WHERE "
        else:
            self.sql_where += " AND  "

        if add_where is not None:
            self.sql_where   +=  add_where
            if add_data is not None:
                self.sql_data.append( add_data )

    # ----------------------------------------------
    def add_to_where_dates( self,   ):
        """
        what it says ....
        return mutates self -- in particular  self.sql_where self.sql_data
        """
        #  -------- dates
        begin_dt      =   self.begin_dt
        if begin_dt is not None:
            self.add_to_where( add_where = f"\n{indent}tweets.tweet_datetime  >= ? ",
                               add_data  = begin_dt  )

        end_dt        =   self.end_dt
        if end_dt is not None:
            self.add_to_where( add_where  = f"\n{indent}tweets.tweet_datetime <= ? ",
                               add_data   = end_dt  )

    # ----------------------------------------------
    def get_info_string( self,   ):
        """
        migrate to __str__ see below
        what it says ....
        for debug gathers instance var for select ... into a string
        return string
        """
        # add more as needed, setup in setup init to avoid errors
        msg     =  "builder vars for SQLBuilder( self.x ):\n"
        msg    += f"     db_name:                   {self.db_file_name}\n"
        msg    += f"     table_name:                {self.table_name}\n"
        msg    += f"     sql:                       {self.sql}\n"
        msg    += f"     file_writer:               {self.file_writer}\n"

        msg    += f"     select_name:               {self.select_name}\n"
        msg    += f"     output_format:             {self.output_format}\n"

        msg    += f"     columns_out:               {self.columns_out}\n"

        # ---- tweets selects
        msg    += f"     begin_dt:                  {self.begin_dt}\n"
        msg    += f"     end_dt:                    {self.end_dt}\n"

        # msg    += f"     tweet_type:                {self.tweet_type}\n"
        msg    += f"     max_count:                 {self.max_count}\n"
        msg    += f"     word_type:                 {self.word_type}\n"


        # msg    += f"     tweets_word_select         {self.tweets_word_select}\n"
        # msg    += f"     is_covid:                  {self.is_covid}\n"


        # msg    += f"     a_word:                    {self.a_word}\n"

        # # ---- concord selects
        # msg    += f"     concord_word_select:       {self.concord_word_select}\n"
        # msg    += f"     is_ascii:                  {self.is_ascii}\n"

        # # ---- words selects
        # msg    += f"     words_word_select          {self.words_word_select}\n"
        # msg    += f"     min_group_by_count         {self.min_group_by_count}\n"
        # msg    += f"     words_is_word_null         {self.words_is_word_null}\n"

       #  # ---- end selcts
       #  msg    += f"     default_order_by:          {self.default_order_by}\n"
       #  msg    += f"     gui_order_by:              {self.gui_order_by}\n"
       # # msg    += f"     sort_order:        {self.sort_order}\n"   # why both of them is this default set where

       #  msg    += f"     my_count:                  {self.my_count}\n"

       #  msg    += f"     sql:                       {self.sql}\n"
       #  msg    += f"     sql_where:                 {self.sql_where}\n"
       #  msg    += f"     sql_having:                {self.sql_having}\n"
       #  msg    += f"     sql_data:                  {self.sql_data}\n"

       #  msg    += f"     row_functions:             {self.row_functions}\n"
       #  msg    += f"     footer_functions:          {self.footer_functions}\n"

       #  msg    += f"     output_append:             {self.output_append}\n"
        msg    += f"\n\n"

        return msg




    # -----------------------------------
    def __str__( self,   ):
        """
        this is informal, just for debugging
        sometimes it is hard to see where values have come out this may help if printed.
        not complete, add as needed -- compare across applications
        this copied from smart_terminal, commented out items might be good to use here or not
        """

        a_str   = ""
        a_str   = f"{a_str}>>>>>>>>>>* SQLBuilder *<<<<<<<<<<<<"
        a_str   = string_util.to_columns( a_str, ["db_name",        f"{self.db_name}" ] )
        a_str   = string_util.to_columns( a_str, ["table_name",     f"{self.table_name}" ] )
        a_str   = string_util.to_columns( a_str, ["sql",            f"{self.sql}" ] )
        # a_str   = string_util.to_columns( a_str, ["logging_level", f"{self.logging_level}" ] )
        # a_str   = string_util.to_columns( a_str, ["pylogging_fn",    f"{self.pylogging_fn}" ] )
        # a_str   = string_util.to_columns( a_str, ["gui_text_log_fn", f"{self.confirm_selects}" ] )


   # # ----------------------------------------------
   #  def add_to_where_is_covid( self  ):
   #      """
   #      return mutates self -- in particular  self.sql_where self.sql_data
   #      """
   #      #  --------tweets is_covid
   #      is_covid   = self.is_covid
   #      if is_covid is not None:

   #          if is_covid:
   #              self.add_to_where( add_where = f"\n{indent}tweets.is_covid   ",
   #                                 add_data = None )

   #          else:
   #              self.add_to_where( add_where = f"\n{indent}NOT tweets.is_covid   ",
   #                                 add_data = None )

   # # ----------------------------------------------
   #  def add_to_where_is_ascii( self  ):
   #      """
   #      return mutates self -- in particular  self.sql_where self.sql_data
   #      """
   #      #  --------concord is_ascii-- ok
   #      is_ascii   = self.is_ascii
   #      if is_ascii is not None:

   #          if is_ascii:
   #              self.add_to_where( add_where = f"\n{indent}concord.is_ascii   ",
   #                                 add_data = None )

   #          else:
   #              self.add_to_where( add_where = f"\n{indent}NOT concord.is_ascii   ",
   #                                 add_data = None )

   # # ----------------------------------------------
   #  def add_to_where_word_like( self  ):
   #      """
   #      return mutates self -- in particular  self.sql_where self.sql_data
   #      """
   #      # --------- word  ... consider auto adding of wild char at both ends
   #      # --------- tweets.word   consider auto adding of wild char at both ends
   #      a_word    = self.tweets_word_select
   #      if a_word != "":
   #          a_word    = a_word.lower()
   #          self.add_to_where( add_where  = f'\n{indent}lower( tweets.tweet )  LIKE  "%{a_word}%"',     # sql inject
   #                             add_data   = None  )

   # # ----------------------------------------------
   #  def add_to_where_tweet_type( self  ):
   #      """
   #      return mutates self -- in particular  self.sql_where self.sql_data
   #      """
   #      # ----- tweet_type
   #      tweet_type      =   self.tweet_type
   #      if tweet_type is not None:
   #           self.add_to_where( add_where = f"\n{indent}tweets.tweet_type = ? ",
   #                             add_data = tweet_type  )

   # # ----------------------------------------------
   #  def add_to_where_concord_word_like( self  ):
   #      """
   #      return mutates self -- in particular  self.sql_where self.sql_data
   #      """
   #      # --------- word  ... consider auto adding of wild char at both ends
   #      # --------- tweets.word   consider auto adding of wild char at both ends
   #      a_word    = self.concord_word_select
   #      if a_word != "":
   #          self.add_to_where( add_where  = f'\n{indent}concord.word  LIKE  "{a_word}"  ',     # sql inject
   #                             add_data   = None  )
   # # ----------------------------------------------
   #  def add_to_where_concord_word_type( self  ):
   #      """
   #      return mutates self -- in particular  self.sql_where self.sql_data
   #      """
   #      # ----- concord word_type
   #      word_type      =   self.concord_word_type_select
   #      if word_type is not None:
   #           self.add_to_where( add_where = f"\n{indent}concord.word_type = ? ",
   #                             add_data = word_type  )

   # # ----------------------------------------------
   #  def add_to_where_words_word( self  ):
   #      """
   #      return mutates self -- in particular  self.sql_where self.sql_data
   #      """
   #      a_word    = self.words_word_select
   #      if a_word != "":
   #          a_word    = a_word.lower()
   #          self.add_to_where( add_where  = f'\n{indent}words.word LIKE  ? ',
   #                             add_data   = a_word  )

   # # ----------------------------------------------
   #  def add_to_where_words_word_null( self  ):
   #      """
   #      return mutates self -- in particular  self.sql_where self.sql_data
   #      """
   #      is_null     = self.words_is_word_null
   #      if is_null is None:
   #          return
   #      if is_null:
   #          self.add_to_where( add_where  = f'\n{indent}words.word IS NULL ',
   #                             add_data   = None )
   #      else:
   #          self.add_to_where( add_where  = f'\n{indent}words.word IS NOT NULL ',
   #                             add_data   = None )



# ----------------------------------------
class SQLBuilderfromtwitteranal(   ):
    """
    fromtwitteranal
    build sql based on criteria ( all should be in reset )
    then pushed in by external methods setting values
    not all criteria used by all methods ?
    always use fully qualified table names
    """
    def __init__( self,  ):
        """
        what it says .. for now it seems subclasses should make super call
        """
        print( "init SQLBuilder")
        self.reset()
        self.check_title       = "Check Select"
        self.check_run_select  = "Would you like still continue ?"

    # ------ helpers
    # ----------------------------------------------
    def reset( self,  ):
        """
        reset criteria
        try to define most instance var. here to eliminate reporting errors
        Return: mutates self
        """
        self.columns_info       = build_column_info()  # dict of dicts info on each column by fully qualified column name
        self.db_name            = ""
        self.output_format      = "tablexxx"  #  "html"......
        self.db_name            = ""
        self.output_name        = None
        self.columns_out        = None     # list of names in order for the column output
        self.help_file          = "./help/build_for_default.txt"  # change to generic

        self.help_mode          = True
        self.a_word             = ""    # word for select criteria, in some cases a string
        self.my_count           = None
        self.is_covid           = ""    # select criteria on tweet
        self.default_order_by   = ""
        self.gui_order_by       = ""
        self.word_type          = "get_error"

        self.tweets_word_select     = ""
        self.words_word_select      = ""

        self.begin_dt               = datetime.datetime( 1945, 5, 24, 17, 53, 59 )
        self.end_dt                 = datetime.datetime(   1945, 5, 24, 17, 53, 59 )

        self.select_name        = "A select- name not set "   # user oriented name, same as in dropdown -- can dropdown pass itself with lambda

        self.start_time         = 0    # probably time.time() start of select
        self.end_time           = 0

        self.select_msg         = ""    # a message generated during the select ... ?? may just be an idea

        # list to check may not be present in any given select ... this code will hang around is it too much ?? delete
        self.pseudo_columns     = [   PseudoColumnRowCount(         self ),
                                      PseudoColumnTotalWordRank(    self ),
                                      PseudoColumnRa_Word_Rank(     self ),
                                      PseudoColumnRa_Word_Length(   self ),
                                      PseudoColumnRa_Word_Null(     self ),
                                      PseudoColumnRa_Word_Null(     self ),
                                      pseudo_column.PseudoColumnSumCountBins(     self ),
                                  ]

        self.row_functions      = []    # called for each row, used with pseudo columns
        self.footer_functions   = []    # called for the footer

        self.message_function   = None   # set to a function message_function( msg ) for progress messages ?? not implemented

        self.output_append      = None

        self.aux_select         = None   # for now I am thinking used in file_writer write row, but may just be another row_function

        self.reset_sql()

    # ----------------------------------------------
    def reset_sql( self,  ):
        """
        what it says
        return mutate self  --- not sure it should differ from reset
        """
        # use these when building so little mutating routines  like add_to_where work
        self.sql              = ""
        self.sql_where        = ""
        self.sql_having       = ""
        self.sql_from         = ""
        self.sql_data         = []    # parameters passed to sql
        self.row_count        = 0

        self.row_functions    = []    # functions called on each row, producing column dat
        self.prior_row        = None
        self.row_to_list      = False  # convert row to a list for manipulation

    # ----------------------------------------------
    def builder_vars_as_str( self,   ):
        """
        what it says ....
        for debug gathers instance var for select ... into a string
        return string
        """
        # add more as needed, setup in setup init to avoid errors
        msg     =  "builder vars for SQLBuilder( self.x ):\n"
        msg    += f"     db_name:                   {self.db_name}\n"
        msg    += f"     select_name:               {self.select_name}\n"
        msg    += f"     output_format:             {self.output_format}\n"

        msg    += f"     columns_out:               {self.columns_out}\n"

        # ---- tweets selects
        msg    += f"     begin_dt:                  {self.begin_dt}\n"
        msg    += f"     end_dt:                    {self.end_dt}\n"

        msg    += f"     tweet_type:                {self.tweet_type}\n"
        msg    += f"     max_count:                 {self.max_count}\n"
        msg    += f"     word_type:                 {self.word_type}\n"


        msg    += f"     tweets_word_select         {self.tweets_word_select}\n"
        msg    += f"     is_covid:                  {self.is_covid}\n"


        msg    += f"     a_word:                    {self.a_word}\n"

        # ---- concord selects
        msg    += f"     concord_word_select:       {self.concord_word_select}\n"
        msg    += f"     is_ascii:                  {self.is_ascii}\n"

        # ---- words selects
        msg    += f"     words_word_select          {self.words_word_select}\n"
        msg    += f"     min_group_by_count         {self.min_group_by_count}\n"
        msg    += f"     words_is_word_null         {self.words_is_word_null}\n"

        # ---- end selcts
        msg    += f"     default_order_by:          {self.default_order_by}\n"
        msg    += f"     gui_order_by:              {self.gui_order_by}\n"
       # msg    += f"     sort_order:        {self.sort_order}\n"   # why both of them is this default set where

        msg    += f"     my_count:                  {self.my_count}\n"

        msg    += f"     sql:                       {self.sql}\n"
        msg    += f"     sql_where:                 {self.sql_where}\n"
        msg    += f"     sql_having:                {self.sql_having}\n"
        msg    += f"     sql_data:                  {self.sql_data}\n"

        msg    += f"     row_functions:             {self.row_functions}\n"
        msg    += f"     footer_functions:          {self.footer_functions}\n"

        msg    += f"     output_append:             {self.output_append}\n"
        msg    += f"\n\n"

        return msg

   # ----------------------------------------------
    def grouping_row_function( self  ):
        """
        use to suppress rows only letting every nth row thru
        seems to need access to its own instance var,
        should this be in builder in its own object.... is this a good
        place for a partial?  should it be set up sort of like a file writer?
        ?? how will it interact with row count
        or rather than do something new just use a psudo column ... but how to init it
        but this will add a new column
        """
        pass


   # ----------------------------------------------
    def display_help( self  ):
        """
        user interaction:
        display help for this report
        """
        AppGlobal.gui.do_clear_button( "dummy_event")
        with open( self.help_file, "r" ) as a_file:
            lines = a_file.readlines()
            # print( lines )
            msg  = "".join( lines )
            AppGlobal.gui.display_info_string( msg )
        return

    # ----------------------------------------------
    def confirm_continue_0( self,   ):   #  help_mode = False
        """
        adding more common code to confirm_continue, experimenting with factoring

        """
        # next is standard this is the refactor ??

        if self.help_mode or self.output_format != "msg":
            self.display_help()
            info_msg     =    f"sql is:\n{self.sql}\n"
            AppGlobal.gui.display_info_string( info_msg )
            info_msg     =    f"sql_data is:\n{self.sql_data}"

        info_msg     = ""
        self.confirm_continue( info_msg, self.check_title,   self.check_run_select, )

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
        help_mode    = self.help_mode

        print( f"builder confirm_continue {help_mode}")

        AppGlobal.gui.display_info_string( info_msg )

        if help_mode:
            raise app_global.UserCancel( "Mode: Help only, query not run" )

        if AppGlobal.parameters.confirm_selects:   #  !! may still need adjust for msg format

            continue_flag  = messagebox.askokcancel( a_title, msg )

            if continue_flag is not True:
                AppGlobal.gui.display_info_string( "Operation canceled" )
                raise app_global.UserCancel( "user: Operation canceled" )

    # ----------------------------------------------
    def select_and_output( self,  ):
        """
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

        columns_info        = self.columns_info
        #rint( f"columns_info{columns_info}")

        file_writer         = file_writers.make_file_writer( self  )
        self.file_writer    = file_writer  # copy for AuxSelect.....
        file_writer.write_header()

        #msg     = f"Select and output; connect to {self.db_name}"
        #rint( msg )
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
                self.write_row   = True   # this allows pseodo columns to suppress output
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
                        i_col_info    = columns_info[ self.columns_out[ ix_col ] ]
                        transform     = i_col_info["transform"]
                        #col_text     = i_col_info["column_head"]
                        if transform is not None:
                            row[ ix_col ]    = transform( i_col )

                        file_writer.write_row( row )   # here may need to add row count.... breaking stuff what type is row?
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

        file_writer.write_footer( footer_info )

        print(  footer_info )
        msg      =  f"select complete with footer info: {footer_info}"
        AppGlobal.logger.debug( msg )

        # os open file for user to view
        if   self.output_format  == "html":
            AppGlobal.os_open_html_file( self.output_name )

        elif self.output_format  == "zap":
            pass
        elif self.output_format  == "msg":
            pass
            # AppGlobal.gui.do_clear_button( "dummy_event")

            # with open( self.output_name, "r", encoding = "utf8", errors = 'replace' )  as a_file:
            #     lines = a_file.readlines()
            #     # print( lines )
            #     msg  = "".join( lines )
            #     AppGlobal.gui.display_info_string( msg )

        else:
            AppGlobal.os_open_txt_file(  self.output_name )

  # ----------------------------------------------
    def go( self,  ):
        """
        after all setup is done go and do the select
        arg:  which select in builder to run, later when sub-classed just go
        """
        AppGlobal.gui.do_clear_button( "ignored" ) # check this actually works in real time !!
        try:
            self.this_select()          # configured for one of self.  ... with sub-classing always the same
            self.select_and_output()    # help_mode ??

        except app_global.UserCancel as exception:   #

            pass  # Catch the  exception and swallow as user wants out not an error
            #rint( exception )

        msg   = f"Select Done, rows selected: {self.row_count} time = {self.end_time - self.start_time}"
        AppGlobal.gui.display_info_string( msg )
        AppGlobal.logger.debug(  msg  )

   # ----------------------------------------------
    def format_sql_for_user( self  ):
        """
        ?? finish me ... I go back and forth on this, now leaning towards
        mutate self
        """
        self.display_sql   = "not implemented"

# ----------- where methods
   # ----------------------------------------------
    def add_to_where( self,    add_where = None, add_data = None,   ):
        """
        add on to where clause ok if starts at 0.  assumes and between clauses
        return mutates self -- in particular  self.sql_where self.sql_data
        """
        if self.sql_where == "":
            self.sql_where  = "\n WHERE "
        else:
            self.sql_where += " AND  "

        if add_where is not None:
            self.sql_where   +=  add_where
            if add_data is not None:
                self.sql_data.append( add_data )

    # ----------------------------------------------
    def add_to_where_dates( self,   ):
        """
        what it says ....
        return mutates self -- in particular  self.sql_where self.sql_data
        """
        #  -------- dates
        begin_dt      =   self.begin_dt
        if begin_dt is not None:
            self.add_to_where( add_where = f"\n{indent}tweets.tweet_datetime  >= ? ",
                               add_data  = begin_dt  )

        end_dt        =   self.end_dt
        if end_dt is not None:
            self.add_to_where( add_where  = f"\n{indent}tweets.tweet_datetime <= ? ",
                               add_data   = end_dt  )

   # ----------------------------------------------
    def add_to_where_is_covid( self  ):
        """
        return mutates self -- in particular  self.sql_where self.sql_data
        """
        #  --------tweets is_covid
        is_covid   = self.is_covid
        if is_covid is not None:

            if is_covid:
                self.add_to_where( add_where = f"\n{indent}tweets.is_covid   ",
                                   add_data = None )

            else:
                self.add_to_where( add_where = f"\n{indent}NOT tweets.is_covid   ",
                                   add_data = None )

   # ----------------------------------------------
    def add_to_where_is_ascii( self  ):
        """
        return mutates self -- in particular  self.sql_where self.sql_data
        """
        #  --------concord is_ascii-- ok
        is_ascii   = self.is_ascii
        if is_ascii is not None:

            if is_ascii:
                self.add_to_where( add_where = f"\n{indent}concord.is_ascii   ",
                                   add_data = None )

            else:
                self.add_to_where( add_where = f"\n{indent}NOT concord.is_ascii   ",
                                   add_data = None )

   # ----------------------------------------------
    def add_to_where_word_like( self  ):
        """
        return mutates self -- in particular  self.sql_where self.sql_data
        """
        # --------- word  ... consider auto adding of wild char at both ends
        # --------- tweets.word   consider auto adding of wild char at both ends
        a_word    = self.tweets_word_select
        if a_word != "":
            a_word    = a_word.lower()
            self.add_to_where( add_where  = f'\n{indent}lower( tweets.tweet )  LIKE  "%{a_word}%"',     # sql inject
                               add_data   = None  )

   # ----------------------------------------------
    def add_to_where_tweet_type( self  ):
        """
        return mutates self -- in particular  self.sql_where self.sql_data
        """
        # ----- tweet_type
        tweet_type      =   self.tweet_type
        if tweet_type is not None:
             self.add_to_where( add_where = f"\n{indent}tweets.tweet_type = ? ",
                               add_data = tweet_type  )

   # ----------------------------------------------
    def add_to_where_concord_word_like( self  ):
        """
        return mutates self -- in particular  self.sql_where self.sql_data
        """
        # --------- word  ... consider auto adding of wild char at both ends
        # --------- tweets.word   consider auto adding of wild char at both ends
        a_word    = self.concord_word_select
        if a_word != "":
            self.add_to_where( add_where  = f'\n{indent}concord.word  LIKE  "{a_word}"  ',     # sql inject
                               add_data   = None  )
   # ----------------------------------------------
    def add_to_where_concord_word_type( self  ):
        """
        return mutates self -- in particular  self.sql_where self.sql_data
        """
        # ----- concord word_type
        word_type      =   self.concord_word_type_select
        if word_type is not None:
             self.add_to_where( add_where = f"\n{indent}concord.word_type = ? ",
                               add_data = word_type  )

   # ----------------------------------------------
    def add_to_where_words_word( self  ):
        """
        return mutates self -- in particular  self.sql_where self.sql_data
        """
        a_word    = self.words_word_select
        if a_word != "":
            a_word    = a_word.lower()
            self.add_to_where( add_where  = f'\n{indent}words.word LIKE  ? ',
                               add_data   = a_word  )

   # ----------------------------------------------
    def add_to_where_words_word_null( self  ):
        """
        return mutates self -- in particular  self.sql_where self.sql_data
        """
        is_null     = self.words_is_word_null
        if is_null is None:
            return
        if is_null:
            self.add_to_where( add_where  = f'\n{indent}words.word IS NULL ',
                               add_data   = None )
        else:
            self.add_to_where( add_where  = f'\n{indent}words.word IS NOT NULL ',
                               add_data   = None )
