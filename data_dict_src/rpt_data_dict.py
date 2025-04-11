#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 08:51:22 2025
report on code gen and perhaps all code gen
   now code gen maybe in dict_main


import  rpt_data_dict

import  data_dict
data_dict.build_it()
table_name      = "photo_subject"
rpt_data_dict.rpt_sql( table_name  )


"""

# ---- tof
# ---- imports
import data_dict
#import dict_main
import adjust_path
import logging


logger      = logging.getLogger( )


# ---- end imports
# for custom logging level at module
LOG_LEVEL   = 10   # higher is more


#-------------------------------
data_dict.build_it()

# ---------------------
def to_columns( current_str, item_list, format_list = ( "{: <30}", "{:<30}" ), indent = "    "  ):
    """
    this is close to what is in string_util.py
    make a partial to avoid repeat of format list ??
    for __str__  probably always default format_list
    see ColunmFormatter which is supposed to be more elaborate version
    see its __str__
    ex:
        import string_util
        a_str     = string_util.to_columns( a_str, ["column_data",    f"{self.column_data}"  ] )
        a_str     = string_util.to_columns( a_str,
                                            ["column_data",    f"{self.column_data}"  ],
                                            format_list = ( "{: <30}", "{:<30}" )
    """
    #rint ( f"item_list {item_list}.............................................................. " )
    line_out  = ""
    for i_item, i_format in zip( item_list, format_list ):
        a_col  = i_format.format( i_item )
        line_out   = f"{indent}{line_out}{a_col}"
    if current_str == "":
        ret_str  = f"{line_out}"
    else:
        ret_str  = f"{current_str}\n{line_out}"
    return ret_str



# ---- table orineted ---------------------------
def rpt_topic_columns( table_name ):
    """
    Print topic list info for a table

    """
    a_table    = data_dict.DATA_DICT.get_table( table_name )
    columns    = a_table.get_topic_columns()
    for ix, i_column in enumerate( columns ):
        i_type              = i_column.db_type
        i_db_type           = i_column.db_type
        column_name         = i_column.column_name
        i_my_type           = i_column.column_name       # work in progress or error
        i_display_type      = i_column.display_type
        i_form_edit         = i_column.form_edit
        i_is_key_word       = i_column.is_key_word
        i_placeholder       = i_column.placeholder_text
        i_default_func      = i_column.default_func
        i_is_topic          = i_column.is_topic
        col_head_text       = i_column.col_head_text
        col_head_width      = i_column.col_head_width
        col_head_order      = i_column.col_head_order
        topic_colunm_order  = i_column. topic_colunm_order

        debug_msg    = f"rpt_topic_columns {ix} { column_name = } {topic_colunm_order = }  "
        logging.log( LOG_LEVEL,  debug_msg, )

def gen_build_fields( table_name ):
    """
    build   _build_fields( )

    """
    a_table     = data_dict.DATA_DICT.get_table( table_name )

    print( a_table.to_build_form( ) )
    # beware do not change to logging
    # debug_msg   = ( a_table.to_build_form( ) )
    # logging.log( LOG_LEVEL,  debug_msg, )


def gen_build_fieldswhat( table_name ):
    """
    Print list and history list info for a table
    """
    a_table    = data_dict.DATA_DICT.get_table( table_name )
    columns    = a_table.get_list_columns()
    for ix, i_column in enumerate( columns ):
        i_type          = i_column.db_type
        i_db_type       = i_column.db_type
        column_name   = i_column.column_name
        i_my_type       = i_column.column_name       # work in progress or error
        i_display_type  = i_column.display_type
        i_form_edit     = i_column.form_edit
        i_is_key_word   = i_column.is_key_word
        i_placeholder   = i_column.placeholder_text
        i_default_func  = i_column.default_func
        i_is_topic      = i_column.is_topic
        col_head_text       = i_column.col_head_text
        col_head_width      = i_column.col_head_width
        col_head_order      = i_column.col_head_order
        display_order       = i_column.display_order

        msg    = f"{ix} { column_name = } {col_head_order = } {col_head_text = } {col_head_width = }"
        print( msg )


# -----------------------------------
def rpt_key_words( table_name ):
    """
    Print key_words for a table
    """
    print()
    msg        = f"Report on key word columns for {table_name}"
    print( msg )


    a_table    = data_dict.DATA_DICT.get_table( table_name )
    columns    = a_table.columns

    columns.sort( key = lambda i_column: i_column.display_order   )

    for ix, i_column in enumerate( columns ):
        i_type          = i_column.db_type
        i_db_type       = i_column.db_type
        column_name   = i_column.column_name
        i_my_type       = i_column.column_name
        i_display_type  = i_column.display_type
        i_form_edit     = i_column.form_edit
        i_is_key_word   = i_column.is_key_word
        i_placeholder   = i_column.placeholder_text
        i_default_func  = i_column.default_func
        i_is_topic      = i_column.is_topic
        col_head_text       = i_column.col_head_text
        col_head_width      = i_column.col_head_width
        col_head_order      = i_column.col_head_order
        display_order       = i_column.display_order

        if i_is_key_word:
            msg    = f"{ix} { column_name = } {i_is_key_word = }  "
            print( msg )

# -----------------------------------
def rpt_display_order( table_name ):
    """
    Print display order for a table
        this is for code gen
        think this for forms not lists

    """
    rpt_display_order_with_columns( table_name )

# -----------------------------------
def rpt_display_order_old( table_name ):
    """
    Print display order for a table
        this is for code gen
        think this for forms not lists

    """
    a_table    = data_dict.DATA_DICT.get_table( table_name )
    columns    = a_table.columns

    columns.sort( key = lambda i_column: i_column.display_order   )

    for ix, i_column in enumerate( columns ):
        i_type          = i_column.db_type
        i_db_type       = i_column.db_type
        column_name   = i_column.column_name
        i_my_type       = i_column.column_name
        i_display_type  = i_column.display_type
        i_form_edit     = i_column.form_edit
        i_is_key_word   = i_column.is_key_word
        i_placeholder   = i_column.placeholder_text
        i_default_func  = i_column.default_func
        i_is_topic      = i_column.is_topic
        col_head_text       = i_column.col_head_text
        col_head_width      = i_column.col_head_width
        col_head_order          = i_column.col_head_order
        display_order           = i_column.display_order
        form_col_span           = i_column.form_col_span
        form_read_only      = i_column.form_read_only
        is_keep_prior_enabled   = i_column.is_keep_prior_enabled

        msg    = f"{ix} { column_name = } {display_order = } {form_col_span = } {form_read_only = }"
        print( msg )


# -----------------------------------
def rpt_display_order_with_columns( table_name ):
    """
    Print display order for a table
        this is for code gen
        think this for forms not lists

    """
    format_list = ( "{:<4}", "{:<30}", "{:<30}", "{:<30}", "{:<30}", "{:<30}", "{:<30}" )
    indent      = ""
            # ok to have too many i think so


    a_table    = data_dict.DATA_DICT.get_table( table_name )
    columns    = a_table.columns

    columns.sort( key = lambda i_column: i_column.display_order   )

    a_str    =  ""
    column_items    = [ "ix", "column_name", "display_order", "form_col_span","form_read_only" ]
    a_str           = to_columns( a_str, column_items, format_list = format_list, indent = indent )

    for ix, i_column in enumerate( columns ):
        i_type          = i_column.db_type
        i_db_type       = i_column.db_type
        column_name   = i_column.column_name
        i_my_type       = i_column.column_name
        i_display_type  = i_column.display_type
        i_form_edit     = i_column.form_edit
        i_is_key_word   = i_column.is_key_word
        i_placeholder   = i_column.placeholder_text
        i_default_func  = i_column.default_func
        i_is_topic      = i_column.is_topic
        col_head_text       = i_column.col_head_text
        col_head_width      = i_column.col_head_width
        col_head_order          = i_column.col_head_order
        display_order           = i_column.display_order
        form_col_span           = i_column.form_col_span
        form_read_only      = i_column.form_read_only
        is_keep_prior_enabled   = i_column.is_keep_prior_enabled

        # msg    = f"{ix} { column_name = } {display_order = } {form_col_span = } {form_read_only = }"
        # print( msg )

        column_items    = [ f"{ix}", f"{ column_name}", f" {display_order}", f" {form_col_span} ",f" {form_read_only}" ]
        a_str           = to_columns( a_str, column_items, format_list = format_list, indent = indent )



    print( a_str )

# -------------------------------------------
def rpt_list_order( table_name ):
    """
    Print list and history list info for a table

    """
    print()
    msg        = f"Report on list header order rpt_list_order for {table_name}"
    print( msg )

    a_table    = data_dict.DATA_DICT.get_table( table_name )
    columns    = a_table.get_list_columns()
    for ix, i_column in enumerate( columns ):
        i_type          = i_column.db_type
        i_db_type       = i_column.db_type
        column_name   = i_column.column_name
        i_my_type       = i_column.column_name       # work in progress or error
        i_display_type  = i_column.display_type
        i_form_edit     = i_column.form_edit
        i_is_key_word   = i_column.is_key_word
        i_placeholder   = i_column.placeholder_text
        i_default_func  = i_column.default_func
        i_is_topic      = i_column.is_topic
        col_head_text      = i_column.col_head_text
        col_head_width     = i_column.col_head_width
        col_head_order      = i_column.col_head_order

        msg    = f"{ix} { column_name = } {col_head_order = } {col_head_text = } {col_head_width = }"

        print( msg )



# ------------------------------
def rpt_sql( table_name ):
    """
    Print sql create for a table

    """
    a_table    = data_dict.DATA_DICT.get_table( table_name )

    sql        = a_table.to_sql_create()
    msg    = f"{sql} "
    print( msg )

# -----------------------------
def rpt_tables(   ):
    """
    List all tables in the data dictionary

    """

    #a_table    = data_dict.DATA_DICT.get_table( table_name )

    msg    = f"{data_dict.DATA_DICT} "

    print( msg )
# ---- run from here

# uncomment to make sure your table is available
#print( data_dict.DATA_DICT )


# a_table    = data_dict.DATA_DICT.get_table( "photo_key_word" )

# a_table    = data_dict.DATA_DICT.get_table( "plant" )
# a_table    = data_dict.DATA_DICT.get_table( "planting" )
# a_table    = data_dict.DATA_DICT.get_table( "photo" )

# ---- table name

# ---- .... help_info
table_name    = "help_info"
#table_name    = "help_key_word"
#table_name    = "help_text"

#table_name    = "key_gen"

# ---- .... people
# table_name      = "people"
# table_name      = "people_text"
table_name      = "people_phones"


# ---- .... photo
#table_name      = "photo"
# #table_name      = "photo_key_word"
# # table_name      = "photo_text"
#table_name      = "photo_subject"

# ---- .... photoshow
# table_name      = "photoshow"               # album
# #table_name      = "photoshow_text"
# #table_name      = "photoshow_key_word"

# table_name      = "photo_subject"

# table_name      = "plant"

#table_name      = "planting"

#table_name      = "stuff"
#table_name       = "stuff_event"


#table_name      = "persons"


# ----  reports rpt_

# ---- .... rpt_tables
#rpt_tables()
#rpt_topic_columns( "people" )
# ---- .... rpt_display_order
#rpt_display_order( table_name )

# ---- .... gen_build_fields
#gen_build_fields( table_name )


# ---- next only for primay document tables
#rpt_list_order( table_name )

#rpt_key_words( table_name )

# ---- sql for all tables

# ---- rpt_sql
#rpt_sql( table_name  )


#rpt_list_order( table_name )  # uses data_dict.DATA_DICT.get_list_columns( table_name )


# ---- bootstrap   --- now in its own module not here
# ---- eof

