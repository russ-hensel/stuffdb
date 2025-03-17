#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 18:17:55 2025

@author: russ
"""
# ---- tof

import data_dict
# ---- build it
def build_it( a_data_dict ):
    """
    build the data_dict for these tables


    """
    # ---- planting ---------------------------------------------
    a_table_dict   = data_dict.TableDict( "planting" )
    a_data_dict.add_table ( a_table_dict )

    # ---- id
    a_column_dict = data_dict.ColumnDict(    column_name    = "id",
                                             db_type        = "INTEGER",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,
                                             col_head_text      = "ID",
                                             col_head_width     = 10,
                                             col_head_order     = 0,
                                             form_col_span      = 1,
                                             form_read_only     = True, )
    a_table_dict.add_column( a_column_dict )

    # ---- id_old
    a_column_dict = data_dict.ColumnDict(    column_name    = "id_old",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,
                                             col_head_text      = "ID Old",
                                              col_head_width     = 10,
                                              col_head_order     = 1,
                                              form_col_span      = 1,
                                              form_read_only     = True, )
    a_table_dict.add_column( a_column_dict )

    # ---- name
    a_column_dict = data_dict.ColumnDict(    column_name    = "name",
                                             db_type        = "VARCHAR(60)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,
                                             is_key_word    = True,
                                             is_keep_prior_enabled  = True,

                                             col_head_text      = "Name",
                                             col_head_width     = 40,
                                             col_head_order     = 10,
                                             form_col_span      = 4,)
    a_table_dict.add_column( a_column_dict )

    # ---- plant_id
    a_column_dict = data_dict.ColumnDict(    column_name    = "plant_id",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- bed_old
    a_column_dict = data_dict.ColumnDict(    column_name    = "bed_old",
                                             db_type        = "VARCHAR(20)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- location
    a_column_dict = data_dict.ColumnDict(    column_name    = "location",
                                             db_type        = "VARCHAR(75)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,
                                             col_head_text      = "Location",
                                             col_head_width     = 20,
                                             col_head_order     = 50, )
    a_table_dict.add_column( a_column_dict )

    # ---- add_kw
    a_column_dict = data_dict.ColumnDict(    column_name    = "add_kw",
                                             db_type        = "VARCHAR(50)",
                                             display_type   = "string",
                                             is_keep_prior_enabled  = True,
                                             is_key_word            = True,
                                             max_len                = None,
                                             default_func           = None , )

    a_table_dict.add_column( a_column_dict )

    # ---- descr
    a_column_dict = data_dict.ColumnDict(    column_name    = "descr",
                                             db_type        = "VARCHAR(250)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func       = None,
                                             is_key_word        = True,
                                             col_head_text      = "Description",
                                             col_head_width     = 30,
                                             col_head_order     = 15, )
    a_table_dict.add_column( a_column_dict )

    # ---- type
    a_column_dict = data_dict.ColumnDict(    column_name    = "type",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- cmnt
    a_column_dict = data_dict.ColumnDict(    column_name    = "cmnt",
                                             db_type        = "VARCHAR(250)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,
                                             is_key_word        = True,)
    a_table_dict.add_column( a_column_dict )

    # ---- lbl
    a_column_dict = data_dict.ColumnDict(    column_name    = "lbl",
                                             db_type        = "VARCHAR(25)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,
                                             col_head_text      = "Label",
                                             col_head_width     = 10,
                                             col_head_order     = 10, )
    a_table_dict.add_column( a_column_dict )

    # ---- bed
    a_column_dict = data_dict.ColumnDict(    column_name    = "bed",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- lbl_name
    a_column_dict = data_dict.ColumnDict(    column_name    = "lbl_name",
                                             db_type        = "VARCHAR(30)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- itag1
    a_column_dict = data_dict.ColumnDict(    column_name    = "itag1",
                                             db_type        = "INTEGER",
                                             display_type   = "integer",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- planting_status
    a_column_dict = data_dict.ColumnDict(    column_name    = "planting_status",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- need_stake
    a_column_dict = data_dict.ColumnDict(    column_name    = "need_stake",
                                             db_type        = "INTEGER",
                                             display_type   = "integer",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- need_label
    a_column_dict = data_dict.ColumnDict(    column_name    = "need_label",
                                             db_type        = "INTEGER",
                                             display_type   = "integer",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- need_work
    a_column_dict = data_dict.ColumnDict(    column_name    = "need_work",
                                             db_type        = "INTEGER",
                                             display_type   = "integer",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- plant_text ---------------------------------------------
    a_table_dict   = data_dict.TableDict( "planting_text" )
    a_data_dict.add_table ( a_table_dict )

    # ---- id
    a_column_dict = data_dict.ColumnDict(    column_name    = "id",
                                             db_type        = "INTEGER",
                                             display_type   = "integer",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- id_old
    a_column_dict = data_dict.ColumnDict(    column_name    = "id_old",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- text_type
    a_column_dict = data_dict.ColumnDict(    column_name    = "text_type",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- text_data
    a_column_dict = data_dict.ColumnDict(    column_name    = "text_data",
                                             db_type        = "TEXT",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )



    # ---- planting_key_word ---------------------------------------------

    a_table_dict   = data_dict.TableDict( "planting_key_word" )
    a_data_dict.add_table ( a_table_dict )

    # ---- id
    a_column_dict = data_dict.ColumnDict(    column_name    = "id",
                                             db_type        = "INTEGER",
                                             display_type   = "integer",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- key_word
    a_column_dict = data_dict.ColumnDict(    column_name    = "key_word",
                                             db_type        = "TEXT",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )