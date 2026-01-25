#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 11:57:40 2025

DB_NAME:        stuffdb
"""

# ---- tof

"""
# metadata here
# this material is used for selection access to the dict module which


KEY_WORDS:      file directory path dialog
CLASS_NAME:     QFileDialogTab
WIDGETS:        QFileDialog QDirectoryDialog


"""






import data_dict_all


#------------------------
def build_it( a_data_dict_all ):
    """
    build the data dictionary for all tables listed here

    """
    # ---- test_table_text ========================================================-
    a_table_dict   = data_dict_all.TableDict(  "test_table_text" )
    a_data_dict_all.add_table ( a_table_dict )

    a_column_dict = data_dict_all.ColumnDict(
                                             column_name    = "id",
                                             db_type        = "INTEGER",
                                             display_type   = "integer",
                                             max_len        = None,
                                             default_func   = None,
                                       )

    a_table_dict.add_column( a_column_dict )

    a_column_dict = data_dict_all.ColumnDict(    column_name    = "id_old",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None, )

    a_table_dict.add_column( a_column_dict )

    # ---- text_type
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "text_type",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None, )

    # ---- text_data
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "text_data",
                                             db_type        = "TEXT",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None, )

    a_table_dict.add_column( a_column_dict )

    # ---- test_table ================================================================
    a_table_dict   = data_dict_all.TableDict( "test_table" )
    a_data_dict_all.add_table ( a_table_dict )

    # ---- id
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "id",
                                             display_order  =  0,
                                             db_type        = "INTEGER",
                                             form_read_only       = True,
                                             rec_to_edit_cnv      = "cnv_int_to_str",
                                             dict_to_edit_cnv     = "cnv_int_to_str",
                                             edit_to_rec_cnv      = "cnv_str_to_int",
                                             edit_to_dict_cnv     = "cnv_str_to_int",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,
                                             col_head_text      = "ID",
                                             col_head_width     = 10,
                                             col_head_order     = 1,
                                             form_col_span      = 1,
                                             primay_key_ix      = 0,)

    a_table_dict.add_column( a_column_dict )

    # ---- id_old
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "id_old",
                                             display_order  =  1,
                                             db_type        = "VARCHAR(15)",
                                             form_read_only  = True,
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- add_kw
    a_column_dict = data_dict_all.ColumnDict(    column_name        = "add_kw",
                                             db_type            = "VARCHAR(50)",
                                             display_type       = "string",
                                             max_len            = None,
                                             default_func       = None,
                                             is_key_word        = True,
                                             col_head_text      = "Key Words",
                                             col_head_width     = 20,
                                             col_head_order     = 10,
                                             display_order      =  20, )
    a_table_dict.add_column( a_column_dict )

    # ---- descr
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "descr",
                                             db_type        = "VARCHAR(50)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,
                                             is_key_word    = True,
                                             display_order      =  15, )
    a_table_dict.add_column( a_column_dict )




    # ---- dt_enter
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "dt_enter",
                                             db_type        = "INTEGER",

                                            detail_edit_class  = "custom_widgets.CQDateEdit",
                                            form_edit          = "custom_widgets.CQDateEdit",
                                             rec_to_edit_cnv      = "cnv_int_to_qdate",
                                                dict_to_edit_cnv     = "cnv_int_to_qdate",
                                                edit_to_rec_cnv      = "cnv_qdate_to_int",
                                                edit_to_dict_cnv     = "cnv_qdate_to_int",
                                             display_type   = "timestamp",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- cmnt
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "cmnt",
                                             db_type        = "VARCHAR(250)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,
                                             form_col_span      = 4, )
    a_table_dict.add_column( a_column_dict )



    # ---- test_table_key_word -----------------------------------
    a_table_dict   = data_dict_all.TableDict(  "test_table_key_word" )
    a_data_dict_all.add_table ( a_table_dict )

    # ---- id
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "id",
                                             db_type        = "INTEGER",
                                             form_read_only       = True,
                                             rec_to_edit_cnv      = "cnv_int_to_str",
                                             dict_to_edit_cnv     = "cnv_int_to_str",
                                             edit_to_rec_cnv      = "cnv_str_to_int",
                                             edit_to_dict_cnv     = "cnv_str_to_int",
                                             display_type   = "integer",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )


    a_column_dict = data_dict_all.ColumnDict(    column_name    = "key_word",
                                             db_type        = "TEXT",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )




# ---- eof




