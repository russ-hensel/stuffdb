#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 11:57:40 2025

@author: russ
"""

# ---- tof

import data_dict


# ---- build it
def build_it( a_data_dict ):
    """
    build the data dictionary for all tables listed here

    """
    # ---- people_text ========================================================-
    a_table_dict   = data_dict.TableDict(  "people_text" )
    a_data_dict.add_table ( a_table_dict )

    a_column_dict = data_dict.ColumnDict(    column_name    = "id",
                                             db_type        = "INTEGER",
                                             display_type   = "integer",
                                             max_len        = None,
                                             default_func   = None,   )

    a_table_dict.add_column( a_column_dict )

    a_column_dict = data_dict.ColumnDict(    column_name    = "id_old",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None, )

    a_table_dict.add_column( a_column_dict )

    # ---- text_type
    a_column_dict = data_dict.ColumnDict(    column_name    = "text_type",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None, )

    # ---- text_data
    a_column_dict = data_dict.ColumnDict(    column_name    = "text_data",
                                             db_type        = "TEXT",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None, )

    a_table_dict.add_column( a_column_dict )

    # ---- people ================================================================
    a_table_dict   = data_dict.TableDict( "people" )
    a_data_dict.add_table ( a_table_dict )

    # ---- id
    a_column_dict = data_dict.ColumnDict(    column_name    = "id",
                                             display_order  =  0,
                                             db_type        = "INTEGER",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,
                                             col_head_text      = "ID",
                                             col_head_width     = 10,
                                             col_head_order     = 1,
                                             form_col_span      = 1,
                                             form_read_only     = True, )
    a_table_dict.add_column( a_column_dict )

    # ---- id_old
    a_column_dict = data_dict.ColumnDict(    column_name    = "id_old",
                                             display_order  =  1,
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- add_kw
    a_column_dict = data_dict.ColumnDict(    column_name        = "add_kw",
                                             db_type            = "VARCHAR(50)",
                                             display_type       = "string",
                                             max_len            = None,
                                             default_func       = None,
                                             is_key_word        = True,
                                             col_head_text      = "Key Words",
                                             col_head_width     = 10,
                                             col_head_order     = 10,
                                             display_order      =  20, )
    a_table_dict.add_column( a_column_dict )

    # ---- descr
    a_column_dict = data_dict.ColumnDict(    column_name    = "descr",
                                             db_type        = "VARCHAR(50)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,
                                             is_key_word    = True,
                                             display_order      =  15, )
    a_table_dict.add_column( a_column_dict )

    # ---- type
    a_column_dict = data_dict.ColumnDict(    column_name    = "type",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- type_sub
    a_column_dict = data_dict.ColumnDict(    column_name    = "type_sub",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- dt_enter
    a_column_dict = data_dict.ColumnDict(    column_name    = "dt_enter",
                                             db_type        = "INTEGER",
                                             display_type   = "timestamp",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- cmnt
    a_column_dict = data_dict.ColumnDict(    column_name    = "cmnt",
                                             db_type        = "VARCHAR(250)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,
                                             form_col_span      = 4, )
    a_table_dict.add_column( a_column_dict )

    # ---- status
    a_column_dict = data_dict.ColumnDict(    column_name    = "status",
                                             db_type        = "VARCHAR(10)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- l_name
    a_column_dict = data_dict.ColumnDict(    column_name    = "l_name",
                                             display_order  =  25,
                                             db_type        = "VARCHAR(45)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,
                                             is_key_word    = True,
                                             col_head_text      = "Last Name",
                                             col_head_width     = 20,
                                             col_head_order     = 5,
                                             topic_colunm_order = 2,
                                             form_col_span      = 4, )

    a_table_dict.add_column( a_column_dict )

    # ---- f_name
    a_column_dict = data_dict.ColumnDict(    column_name    = "f_name",
                                             display_order  =  23,
                                             db_type        = "VARCHAR(35)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,
                                             is_key_word    = True,
                                             col_head_text      = "First Name",
                                             col_head_width     = 20,
                                             col_head_order     = 4,
                                             topic_colunm_order = 1,
                                             form_col_span      = 4, )

    a_table_dict.add_column( a_column_dict )

    # ---- st_adr_1
    a_column_dict = data_dict.ColumnDict(    column_name    = "st_adr_1",
                                             display_order  =  60,
                                             db_type        = "VARCHAR(35)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- st_adr_2
    a_column_dict = data_dict.ColumnDict(    column_name    = "st_adr_2",
                                             display_order  =  61,
                                             db_type        = "VARCHAR(35)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- st_adr_3
    a_column_dict = data_dict.ColumnDict(    column_name    = "st_adr_3",
                                             display_order  =  62,
                                             db_type        = "VARCHAR(35)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- city
    a_column_dict = data_dict.ColumnDict(    column_name    = "city",
                                             display_order  =  70,
                                             db_type        = "VARCHAR(35)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- state
    a_column_dict = data_dict.ColumnDict(    column_name    = "state",
                                             display_order  =  72,
                                             db_type        = "VARCHAR(25)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- zip
    a_column_dict = data_dict.ColumnDict(    column_name    = "zip",
                                             display_order  =  74,
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- m_name
    a_column_dict = data_dict.ColumnDict(    column_name    = "m_name",
                                             display_order  = 24,
                                             db_type        = "VARCHAR(25)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,
                                             is_key_word    = True,)
    a_table_dict.add_column( a_column_dict )

    # ---- dt_item
    a_column_dict = data_dict.ColumnDict(    column_name    = "dt_item",
                                             db_type        = "INTEGER",
                                             display_type   = "timestamp",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- c_name
    a_column_dict = data_dict.ColumnDict(    column_name    = "c_name",
                                             db_type        = "VARCHAR(55)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,
                                             is_key_word        = True,
                                             col_head_text      = "Company",
                                             col_head_width     = 20,
                                             col_head_order     = 8,
                                           )
    a_table_dict.add_column( a_column_dict )

    # ---- title
    a_column_dict = data_dict.ColumnDict(    column_name    = "title",
                                             db_type        = "VARCHAR(35)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- dddd
    a_column_dict = data_dict.ColumnDict(    column_name    = "dddd",
                                             db_type        = "VARCHAR(5)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- department
    a_column_dict = data_dict.ColumnDict(    column_name    = "department",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- floor
    a_column_dict = data_dict.ColumnDict(    column_name    = "floor",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- location
    a_column_dict = data_dict.ColumnDict(    column_name    = "location",
                                             db_type        = "VARCHAR(40)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- role_text
    a_column_dict = data_dict.ColumnDict(    column_name    = "role_text",
                                             db_type        = "VARCHAR(40)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- assoc_msn
    a_column_dict = data_dict.ColumnDict(    column_name    = "assoc_msn",
                                             db_type        = "VARCHAR(60)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- bussiness_house
    a_column_dict = data_dict.ColumnDict(    column_name    = "bussiness_house",
                                             db_type        = "VARCHAR(40)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- country
    a_column_dict = data_dict.ColumnDict(    column_name    = "country",
                                             db_type        = "VARCHAR(40)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- autodial
    a_column_dict = data_dict.ColumnDict(    column_name    = "autodial",
                                             db_type        = "INTEGER",
                                             display_type   = "integer",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- people_key_word -----------------------------------
    a_table_dict   = data_dict.TableDict(  "people_key_word" )
    a_data_dict.add_table ( a_table_dict )

    # ---- id
    a_column_dict = data_dict.ColumnDict(    column_name    = "id",
                                             db_type        = "INTEGER",
                                             display_type   = "integer",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )


    a_column_dict = data_dict.ColumnDict(    column_name    = "key_word",
                                             db_type        = "TEXT",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- people_phone  ---------------------
    a_table_dict   = data_dict.TableDict(  "people_phone" )
    a_data_dict.add_table ( a_table_dict )

    # ---- "seq_id",
    a_column_dict = data_dict.ColumnDict( column_name  = "seq_id",
                                          db_type      = "VARCAR(10)",
                                          display_type = "error",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- "people_id",
    a_column_dict = data_dict.ColumnDict( column_name  = "people_id",
                                          db_type      = "VARCAR(10)",
                                          display_type = "error",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- "type",
    a_column_dict = data_dict.ColumnDict( column_name  = "type",
                                          db_type      = "VARCAR(10)",
                                          display_type = "error",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- "phone_old",
    a_column_dict = data_dict.ColumnDict( column_name  = "phone_old",
                                          db_type      = "VARCAR(35)",
                                          display_type = "error",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- "cmnt",
    a_column_dict = data_dict.ColumnDict( column_name  = "cmnt",
                                          db_type      = "VARCAR(40)",
                                          display_type = "error",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- "phone",
    a_column_dict = data_dict.ColumnDict( column_name  = "phone",
                                          db_type      = "VARCAR(100)",
                                          display_type = "error",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- "autodial",
    a_column_dict = data_dict.ColumnDict( column_name  = "autodial",
                                          db_type      = "INTEGER",
                                          display_type = "integer",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )


# ---- eof




