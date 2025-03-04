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


    """

    # ---- plant ---------------------------------------------
    a_table_dict   = data_dict.TableDict( "plant" )
    a_data_dict.add_table ( a_table_dict )

    # ---- id
    a_column_dict = data_dict.ColumnDict(    column_name    = "id",
                                             db_type        = "INTEGER",
                                             display_order  =  0,
                                             display_type   = "integer",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- id_old
    a_column_dict = data_dict.ColumnDict(    column_name    = "id_old",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             display_order  =  4,
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- name
    a_column_dict = data_dict.ColumnDict(    column_name    = "name",
                                             db_type        = "VARCHAR(75)",
                                             display_type   = "string",
                                             display_order  =  10,
                                             max_len        = None,
                                             default_func   = None,
                                             is_key_word    = True,
                                             col_head_text      = "Name",
                                             col_head_width     = 25,
                                             col_head_order     = 10, )
    a_table_dict.add_column( a_column_dict )

    # ---- latin_name
    a_column_dict = data_dict.ColumnDict(    column_name    = "latin_name",
                                             db_type        = "VARCHAR(75)",
                                             display_type   = "string",
                                             display_order  = 12,
                                             max_len        = None,
                                             default_func   = None,
                                             is_key_word    = True,
                                             col_head_text      = "Latin",
                                             col_head_width     = 20,
                                             col_head_order     = 10, )

    a_table_dict.add_column( a_column_dict )

    # ---- add_kw
    a_column_dict = data_dict.ColumnDict(    column_name    = "add_kw",
                                             db_type        = "VARCHAR(40)",
                                             display_type   = "string",
                                             display_order  = 30,
                                             max_len        = None,
                                             default_func   = None,
                                             is_key_word    = True,
                                             col_head_text      = "Key Words",
                                             col_head_width     = 20,
                                             col_head_order     = 50, )
    a_table_dict.add_column( a_column_dict )

    # ---- descr
    a_column_dict = data_dict.ColumnDict(    column_name    = "descr",
                                             db_type        = "VARCHAR(250)",
                                             display_type   = "string",
                                             display_order  = 34,
                                             max_len        = None,
                                             default_func   = None,
                                             is_key_word    = True,
                                             col_head_text      = "Description",
                                             col_head_width     = 20,
                                             col_head_order     = 60, )

    a_table_dict.add_column( a_column_dict )

    # ---- plant_type
    a_column_dict = data_dict.ColumnDict(    column_name    = "plant_type",
                                             db_type        = "VARCHAR(25)",
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

    # ---- cmnt
    a_column_dict = data_dict.ColumnDict(    column_name    = "cmnt",
                                             db_type        = "VARCHAR(250)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,
                                             is_key_word    = True,)
    a_table_dict.add_column( a_column_dict )

    # ---- life
    a_column_dict = data_dict.ColumnDict(    column_name    = "life",
                                             db_type        = "VARCHAR(20)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- water
    a_column_dict = data_dict.ColumnDict(    column_name    = "water",
                                             db_type        = "VARCHAR(20)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- sun_min
    a_column_dict = data_dict.ColumnDict(    column_name    = "sun_min",
                                             db_type        = "VARCHAR(20)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- sun_max
    a_column_dict = data_dict.ColumnDict(    column_name    = "sun_max",
                                             db_type        = "VARCHAR(20)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- zone_min
    a_column_dict = data_dict.ColumnDict(    column_name    = "zone_min",
                                             db_type        = "VARCHAR(2)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- zone_max
    a_column_dict = data_dict.ColumnDict(    column_name    = "zone_max",
                                             db_type        = "VARCHAR(2)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- height
    a_column_dict = data_dict.ColumnDict(    column_name    = "height",
                                             db_type        = "INTEGER",
                                             display_type   = "int7-2",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- form
    a_column_dict = data_dict.ColumnDict(    column_name    = "form",
                                             db_type        = "VARCHAR(20)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- color
    a_column_dict = data_dict.ColumnDict(    column_name    = "color",
                                             db_type        = "VARCHAR(30)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- pref_unit
    a_column_dict = data_dict.ColumnDict(    column_name    = "pref_unit",
                                             db_type        = "VARCHAR(10)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- hybridizer
    a_column_dict = data_dict.ColumnDict(    column_name    = "hybridizer",
                                             db_type        = "VARCHAR(50)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- hybridizer_year
    a_column_dict = data_dict.ColumnDict(    column_name    = "hybridizer_year",
                                             db_type        = "INTEGER",
                                             display_type   = "integer",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- color2
    a_column_dict = data_dict.ColumnDict(    column_name    = "color2",
                                             db_type        = "VARCHAR(30)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- color3
    a_column_dict = data_dict.ColumnDict(    column_name    = "color3",
                                             db_type        = "VARCHAR(30)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- life2
    a_column_dict = data_dict.ColumnDict(    column_name    = "life2",
                                             db_type        = "VARCHAR(20)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- tag1
    a_column_dict = data_dict.ColumnDict(    column_name    = "tag1",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- chromosome
    a_column_dict = data_dict.ColumnDict(    column_name    = "chromosome",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- bloom_time
    a_column_dict = data_dict.ColumnDict(    column_name    = "bloom_time",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- bloom_dia
    a_column_dict = data_dict.ColumnDict(    column_name    = "bloom_dia",
                                             db_type        = "INTEGER",
                                             display_type   = "int5-2",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- fragrance
    a_column_dict = data_dict.ColumnDict(    column_name    = "fragrance",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- rebloom
    a_column_dict = data_dict.ColumnDict(    column_name    = "rebloom",
                                             db_type        = "VARCHAR(15)",
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

    # ---- extended
    a_column_dict = data_dict.ColumnDict(    column_name    = "extended",
                                             db_type        = "VARCHAR(1)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- plant_class
    a_column_dict = data_dict.ColumnDict(    column_name    = "plant_class",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- source_type
    a_column_dict = data_dict.ColumnDict(    column_name    = "source_type",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- source_detail
    a_column_dict = data_dict.ColumnDict(    column_name    = "source_detail",
                                             db_type        = "VARCHAR(60)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- spider
    a_column_dict = data_dict.ColumnDict(    column_name    = "spider",
                                             db_type        = "VARCHAR(10)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- spider_ratio
    a_column_dict = data_dict.ColumnDict(    column_name    = "spider_ratio",
                                             db_type        = "INTEGER",
                                             display_type   = "int5-2",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- double
    a_column_dict = data_dict.ColumnDict(    column_name    = "double",
                                             db_type        = "VARCHAR(1)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )



    # ---- plant_key_word ---------------------------------------------

    a_table_dict   = data_dict.TableDict( "plant_key_word" )
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

    # ---- plant_text ---------------------------------------------
    a_table_dict   = data_dict.TableDict( "plant_text" )
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



# ---- more needed
# ---- eof