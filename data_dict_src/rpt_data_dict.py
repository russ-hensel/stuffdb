#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 08:51:22 2025
report on code gen and perhaps all code gen
   now code gen maybe in dict_main
"""

# ---- tof
import data_dict
#import dict_main
import adjust_path

# ---- imports

# ---- end imports

#-------------------------------

data_dict.build_it()


# ---- table orineted ---------------------------

def rpt_topic_columns( table_name ):
    """
    Print topic list info for a table

    """

    a_table    = data_dict.DATA_DICT.get_table( table_name )
    columns    = a_table.get_topic_columns()
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
        topic_colunm_order  = i_column. topic_colunm_order

        msg    = f"{ix} { column_name = } {topic_colunm_order = }  "

        print( msg )


def gen_build_fields( table_name ):
    """
    build   _build_fields( )

    """
    a_table    = data_dict.DATA_DICT.get_table( table_name )
    print( a_table.to_build_form( ) )

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
        col_head_order      = i_column.col_head_order
        display_order       = i_column.display_order

        msg    = f"{ix} { column_name = } {display_order = }  "

        print( msg )




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

table_name    = "help_info"
#table_name    = "help_key_word"
#table_name    = "help_text"

#table_name    = "key_gen"


# table_name      = "people"
# table_name      = "people_text"

table_name      = "photo"
# #table_name      = "photo_key_word"
# # table_name      = "photo_text"


# table_name      = "photoshow"               # album
# #table_name      = "photoshow_text"
# #table_name      = "photoshow_key_word"

# table_name      = "photo_subject"

# table_name      = "plant"

#table_name      = "planting"

#table_name      = "stuff"

#table_name      = "persons"

#rpt_tables()
#rpt_topic_columns( "people" )
# ----.        rpt_display_order
#rpt_display_order( table_name )

# ----.        gen_build_fields
gen_build_fields( table_name )
# ---- next only for primay document tables
#rpt_list_order( table_name )

#rpt_key_words( table_name )

# ---- sql for all tables


#rpt_sql( table_name  )


#rpt_list_order( table_name )  # uses data_dict.DATA_DICT.get_list_columns( table_name )
# ---- eof

# ---- bootstrap

sql    = """
CREATE TABLE photo_subject  (
id  INTEGER,
photo_id_old  VARCHAR(15),
table_id_old  VARCHAR(15),
table_joined  VARCHAR(30),
photo_id  INTEGER,
table_id  INTEGER )
"""


sql    = """
CREATE TABLE key_gen  (
table_name  VARCHAR(30),
key_value  INTEGER )
"""


sql    = """
CREATE TABLE photo_in_show  (
id  INTEGER,
photo_id_old  VARCHAR(15),
photo_show_id_old  VARCHAR(15),
sequence  INTEGER,
photo_in_show_id_old  VARCHAR(15),
photo_id  INTEGER,
photo_show_id  INTEGER,
photo_in_show_id  INTEGER )
"""

sql    = """
CREATE TABLE photo_subject  (
id  INTEGER,
photo_id_old  VARCHAR(15),
table_id_old  VARCHAR(15),
table_joined  VARCHAR(30),
photo_id  INTEGER,
table_id  INTEGER )
"""

# persons is a qt5_by_example
sql     = """
CREATE TABLE persons (
id   INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
age  INTEGER,
family_relation TEXT,
add_kw TEXT )
"""


#data_dict.create_some_data_dict_from_sql(sql)

