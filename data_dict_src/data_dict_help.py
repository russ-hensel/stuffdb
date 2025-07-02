#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 11:50:38 2025

@author: russ
"""

import data_dict

#print( data_dict.DATA_DICT )


def build_it( a_data_dict ):
    """

    """
    #a_data_dict    = data_dict.DATA_DICT
    #rint( a_table_dict.to_sql() )
    sql = """

    CREATE TABLE  help_info (


    	system        		VARCHAR(15),     string
    	key_words     		VARCHAR(70),     string
    	add_ts        		INTEGER,         timestamp
    	edit_ts       		INTEGER,         timestamp
    	table_name    		VARCHAR(40),     string
    	column_name   		VARCHAR(40),      string
    	java_type     		VARCHAR(20),      string
    	java_name     		VARCHAR(175),     string
    	java_package  		VARCHAR(150),     string
    	title 			    VARCHAR(150),     string
    	is_example    		VARCHAR(1),       string
    	can_execute   		VARCHAR(1),       string
    )
"""
    # ---- help_info -------------------------------
    a_table_dict   = data_dict.TableDict(  "help_info" )
    a_data_dict.add_table ( a_table_dict )

    # ---- id
    a_column_dict = data_dict.ColumnDict(    column_name    = "id",
                                   db_type              = "INTEGER",
                                             form_read_only       = True,
                                             rec_to_edit_cnv      = "cnv_int_to_str",
                                             dict_to_edit_cnv     = "cnv_int_to_str",
                                             edit_to_rec_cnv      = "cnv_str_to_int",
                                             edit_to_dict_cnv     = "cnv_str_to_int",

                                   max_len            = None,
                                   default_func       = None,
                                   col_head_text      = "ID",
                                   col_head_width     = 10,
                                   col_head_order     = 1,
                                   display_order      = 0,
                                   form_col_span      = 1,
                                   )

    a_table_dict.add_column( a_column_dict )



    # ----id_old
    a_column_dict = data_dict.ColumnDict(    column_name    = "id_old",
                                             db_type        = "VARCHAR(15)",

                                             form_read_only       = True,


                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,
                                             col_head_order  = 1,
                                             display_order      = 2,
                                             form_col_span      = 1,
                                                               )


    a_table_dict.add_column( a_column_dict )

    # ---- type
    a_column_dict = data_dict.ColumnDict(    column_name    = "type",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None, )

    a_table_dict.add_column( a_column_dict )

    # ---- sub_system
    a_column_dict = data_dict.ColumnDict(    column_name    = "sub_system",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             detail_edit_class  = "custom_widgets.CQComboBox",
                                             form_edit          = "custom_widgets.CQComboBox",
                                             set_editable        = True,


                                             max_len        = None,
                                             default_func   = None,
                                             col_head_text      = "Sub System",
                                             col_head_width     = 15,
                                             col_head_order     = 35,
                                             display_order     = 18, )

    a_table_dict.add_column( a_column_dict )


    # ---- system
    a_column_dict = data_dict.ColumnDict(    column_name    = "system",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             detail_edit_class  = "custom_widgets.CQComboBox",
                                             form_edit          = "custom_widgets.CQComboBox",
                                             set_editable        = True,
                                             max_len        = None,
                                             default_func   = None,
                                             is_key_word        = True,
                                             col_head_text      = "System",
                                             col_head_width     = 15,
                                             col_head_order     = 30,
                                             display_order     = 15,
                                             form_col_span      = 1,)

    a_table_dict.add_column( a_column_dict )

    # ----key_words
    a_column_dict = data_dict.ColumnDict(    column_name        = "key_words",
                                             db_type            = "VARCHAR(70)",
                                             display_type       = "string",
                                             max_len            = None,
                                             default_func       = None,
                                             is_key_word        = True,
                                             is_keep_prior_enabled = True,
                                             col_head_text      = "Key Words",
                                             col_head_width     = 40,
                                             col_head_order     = 38,
                                             display_order      = 12,
                                             form_col_span      = 4,)
    a_table_dict.add_column( a_column_dict )

    # ---- add_ts   --- may not exist ?? -- was missing fixed
    a_column_dict = data_dict.ColumnDict(    column_name    = "add_ts",
                                             db_type        = "INTEGER",
                                             display_type   = "timestamp",
                                             max_len        = None,
                                             default_func   = None,
                                             detail_edit_class  = "custom_widgets.CQDateEdit",
                                             form_edit          = "custom_widgets.CQDateEdit",
                                             form_read_only     = True,
                                             display_order      = 120,
                                             form_col_span      = 1,)
    a_table_dict.add_column( a_column_dict )

    # ---- edit_ts
    a_column_dict = data_dict.ColumnDict(    column_name    = "edit_ts",
                                             db_type        = "INTEGER",
                                             display_type   = "timestamp",
                                             max_len        = None,
                                             default_func   = None,
                                             detail_edit_class  = "custom_widgets.CQDateEdit",
                                             form_edit          = "custom_widgets.CQDateEdit",
                                             form_read_only     = True,
                                             display_order      = 120,
                                             form_col_span      = 1,)
    a_table_dict.add_column( a_column_dict )


    # ---- table_name
    a_column_dict = data_dict.ColumnDict(    column_name    = "table_name",
                                             db_type        = "VARCHAR(40)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,
                                             is_key_word    = True,
                                             display_order   = 80 )
    a_table_dict.add_column( a_column_dict )


    # ---- column_name
    a_column_dict = data_dict.ColumnDict(    column_name    = "column_name",
                                             db_type        = "VARCHAR(40)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,
                                             display_order   = 82 )
    a_table_dict.add_column( a_column_dict )

    # ---- java_type
    a_column_dict = data_dict.ColumnDict(    column_name    = "java_type",
                                             db_type        = "VARCHAR(20)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,
                                             display_order  = 32, )
    a_table_dict.add_column( a_column_dict )

    # ---- java_name
    a_column_dict = data_dict.ColumnDict(    column_name    = "java_name",
                                             db_type        = "VARCHAR(175)",
                                             display_type   = "string",
                                             is_keep_prior_enabled = True,
                                             max_len        = None,
                                             default_func   = None,
                                             display_order  = 34, )
    a_table_dict.add_column( a_column_dict )

    # ---- java_package
    a_column_dict = data_dict.ColumnDict(    column_name    = "java_package",
                                             db_type        = "VARCHAR(150)",
                                             display_type   = "string",
                                             is_keep_prior_enabled = True,
                                             max_len        = None,
                                             default_func   = None,
                                             display_order  = 30, )

    a_table_dict.add_column( a_column_dict )

    # ---- title
    a_column_dict = data_dict.ColumnDict(    column_name    = "title",
                                             db_type        = "VARCHAR(150)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,
                                             is_key_word            = True,
                                             is_keep_prior_enabled  = True,
                                             col_head_text      = "Title",
                                             col_head_width     = 60,
                                             col_head_order     = 5,
                                             display_order    = 10,
                                             form_col_span      = 4,)

    a_table_dict.add_column( a_column_dict )

    # ---- is_example
    a_column_dict = data_dict.ColumnDict(    column_name    = "is_example",
                                             db_type        = "VARCHAR(1)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None, )
    a_table_dict.add_column( a_column_dict )

    # ---- can_execute
    a_column_dict = data_dict.ColumnDict(    column_name    = "can_execute",
                                             db_type        = "VARCHAR(1)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None, )
    a_table_dict.add_column( a_column_dict )

    # ---- help_text ---------------------
    a_table_dict   = data_dict.TableDict(  "help_text" )
    a_data_dict.add_table ( a_table_dict )

    a_column_dict = data_dict.ColumnDict(    column_name    = "id",
                                   db_type              = "INTEGER",
                                             form_read_only       = True,
                                             rec_to_edit_cnv      = "cnv_int_to_str",
                                             dict_to_edit_cnv     = "cnv_int_to_str",
                                             edit_to_rec_cnv      = "cnv_str_to_int",
                                             edit_to_dict_cnv     = "cnv_str_to_int",
                                   display_type         = "integer",
                                   max_len              = None,
                                   default_func         = None,
                                   placeholder_text     = "id",
                                   form_col_span        = 1,  )

    a_table_dict.add_column( a_column_dict )


    a_column_dict = data_dict.ColumnDict(    column_name    = "id_old",
                                   db_type        = "VARCHAR(15)",
                                             form_read_only       = True,

                                   display_type   = "string",
                                   max_len        = None,
                                   default_func= None,
                                   form_col_span  = 1,  )

    a_table_dict.add_column( a_column_dict )

    # ---- text_data
    a_column_dict = data_dict.ColumnDict(    column_name    = "text_data",
                                   db_type        = "TEXT",
                                   display_type   = "string",
                                   max_len        = None,
                                   default_func= None,
                                   placeholder_text   = "this is a long text\\nfield\\ncan hold many lines",)

    a_table_dict.add_column( a_column_dict )




    #rint( a_table_dict.to_sql() )

    # ---- help_key_word -------------------------------
    a_table_dict   = data_dict.TableDict(  "help_key_word" )
    a_data_dict.add_table ( a_table_dict )

    # ---- id
    a_column_dict = data_dict.ColumnDict(    column_name    = "id",
                                             db_type        = "INTEGER",
                                             display_type   = "integer",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- key_word
    a_column_dict = data_dict.ColumnDict(    column_name    = "key_word",
                                             db_type        = "TEXT",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )



# # --------------------
# if __name__ == "__main__":
#     #----- run the full app

#     test()
# # --------------------
