#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

#import adjust_path
import data_dict


# ---- build it
def build_it( a_data_dict ):
    """


    """
    # ---- photoshow ---------------------------------------------
    a_table_dict   = data_dict.TableDict( "photoshow" )
    a_data_dict.add_table ( a_table_dict )

    # ---- id
    a_column_dict = data_dict.ColumnDict(    column_name    = "id",
                                             db_type        = "INTEGER",

                                             form_read_only       = True,
                                             rec_to_edit_cnv      = "cnv_int_to_str",
                                             dict_to_edit_cnv     = "cnv_int_to_str",
                                             edit_to_rec_cnv      = "cnv_str_to_int",
                                             edit_to_dict_cnv     = "cnv_str_to_int",



                                             display_type   = "string",
                                             display_order  = 0,
                                             max_len        = None,
                                             default_func   = None,
                                             col_head_text      = "ID",
                                             col_head_width     = 10,
                                             col_head_order     = 1,
                                             form_col_span      = 1,

                                             edit_to_rec        = "edit_to_rec_str_to_int",
                                             rec_to_edit        = "rec_to_edit_int_to_str",
                                             )


    a_table_dict.add_column( a_column_dict )

    # ---- id_old
    a_column_dict = data_dict.ColumnDict(    column_name    = "id_old",
                                             db_type        = "VARCHAR(15)",
                                             form_read_only       = True,
                                             display_order  = 1,
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,
                                             form_col_span          = 1,

                                             edit_to_rec        = "edit_to_rec_str_to_int",
                                             rec_to_edit        = "rec_to_edit_int_to_str",
                                             )
    a_table_dict.add_column( a_column_dict )

    # ---- name
    a_column_dict = data_dict.ColumnDict(    column_name    = "name",
                                             db_type        = "VARCHAR(50)",
                                             display_type   = "string",
                                             display_order  = 10,
                                             max_len            = None,
                                             default_func       = None,
                                             is_key_word        = True,
                                             col_head_text      = "Name",
                                             col_head_width     = 50,
                                             col_head_order     = 1,
                                             form_col_span       = 4,
                                            )

    a_table_dict.add_column( a_column_dict )

    # ---- cmnt
    a_column_dict = data_dict.ColumnDict(    column_name    = "cmnt",
                                             db_type        = "VARCHAR(100)",
                                             display_type   = "string",
                                             display_order  = 20,
                                             max_len        = None,
                                             default_func   = None,
                                             is_key_word    = True,
                                             col_head_text      = "Comment",
                                             col_head_width     = 50,
                                             col_head_order     = 1,
                                             form_col_span       = 4,
                                            )
    a_table_dict.add_column( a_column_dict )

    # ---- start_date
    a_column_dict = data_dict.ColumnDict(    column_name    = "start_date",
                                             db_type        = "INTEGER",
                                             #form_read_only       = True,
                                             rec_to_edit_cnv      = "cnv_int_to_qdate",
                                             dict_to_edit_cnv     = "cnv_int_to_qdate",
                                             edit_to_rec_cnv      = "cnv_qdate_to_int",
                                             edit_to_dict_cnv     = "cnv_qdate_to_int",


                                             display_type   = "timestamp",
                                             max_len        = None,
                                             default_func   = None,
                                             display_order  = 122,
                                             # next dups for now
                                             detail_edit_class  = "custom_widgets.CQDateEdit",
                                             form_edit          = "custom_widgets.CQDateEdit",)
    a_table_dict.add_column( a_column_dict )

    # ---- end_date
    a_column_dict = data_dict.ColumnDict(    column_name    = "end_date",
                                             db_type        = "INTEGER",
                                             #form_read_only       = True,
                                             rec_to_edit_cnv      = "cnv_int_to_qdate",
                                             dict_to_edit_cnv     = "cnv_int_to_qdate",
                                             edit_to_rec_cnv      = "cnv_qdate_to_int",
                                             edit_to_dict_cnv     = "cnv_qdate_to_int",


                                             display_type   = "timestamp",
                                             max_len        = None,
                                             default_func   = None,
                                             display_order  = 124,
                                             # next dups for now
                                             detail_edit_class  = "custom_widgets.CQDateEdit",
                                             form_edit          = "custom_widgets.CQDateEdit",)
    a_table_dict.add_column( a_column_dict )

    # ---- create_date
    a_column_dict = data_dict.ColumnDict(    column_name    = "create_date",
                                             db_type        = "INTEGER",
                                             #form_read_only       = True,
                                             rec_to_edit_cnv      = "cnv_int_to_qdate",
                                             dict_to_edit_cnv     = "cnv_int_to_qdate",
                                             edit_to_rec_cnv      = "cnv_qdate_to_int",
                                             edit_to_dict_cnv     = "cnv_qdate_to_int",



                                             display_type   = "timestamp",
                                             max_len        = None,
                                             default_func   = None,
                                             display_order  = 120,
                                             # next dups for now
                                             detail_edit_class  = "custom_widgets.CQDateEdit",
                                             form_edit          = "custom_widgets.CQDateEdit",)
    a_table_dict.add_column( a_column_dict )

    # ---- type
    a_column_dict = data_dict.ColumnDict(    column_name    = "type",
                                             db_type        = "VARCHAR(20)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- add_kw
    a_column_dict = data_dict.ColumnDict(    column_name    = "add_kw",
                                             db_type        = "VARCHAR(50)",
                                             display_type   = "string",
                                             display_order  = 30,
                                             form_col_span  = 4,
                                             max_len        = None,
                                             default_func   = None,
                                             is_key_word    = True,
                                             col_head_text      = "Key Words",
                                             col_head_width     = 50,
                                             col_head_order     = 1,
                                             )
    a_table_dict.add_column( a_column_dict )

    # ---- web_site_dir
    a_column_dict = data_dict.ColumnDict(    column_name    = "web_site_dir",
                                             db_type        = "VARCHAR(240)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- photoshow_text ---------------------
    a_table_dict   = data_dict.TableDict(  "photoshow_text" )
    a_data_dict.add_table ( a_table_dict )

    # ---- id
    a_column_dict = data_dict.ColumnDict(    column_name    = "id",
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


    a_column_dict = data_dict.ColumnDict(    column_name    = "id_old",
                                             db_type        = "VARCHAR(15)",
                                             form_read_only  = True,
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None, )

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
                                             default_func   = None, )

    a_table_dict.add_column( a_column_dict )

    #rint( a_table_dict.to_sql_create() )


    # ---- photoshow_key_word ---------------------------------------------
    a_table_dict   = data_dict.TableDict( "photoshow_key_word" )
    a_data_dict.add_table ( a_table_dict )

    # ---- id
    a_column_dict = data_dict.ColumnDict(    column_name    = "id",
                                             db_type        = "INTEGER",
                                             form_read_only       = True,
                                             rec_to_edit_cnv      = "cnv_int_to_str",
                                             dict_to_edit_cnv     = "cnv_int_to_str",
                                             edit_to_rec_cnv      = "cnv_str_to_int",
                                             edit_to_dict_cnv     = "cnv_str_to_int",


                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- key_word
    a_column_dict = data_dict.ColumnDict(    column_name    = "key_word",
                                             db_type        = "TEXT",
                                             form_read_only       = True,
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,
                                             form_col_span       = 4, )
    a_table_dict.add_column( a_column_dict )


    # ---- photo_subject  ---------------------
    a_table_dict   = data_dict.TableDict(  "photo_subject" )
    a_data_dict.add_table ( a_table_dict )

    # ---- "id",
    a_column_dict = data_dict.ColumnDict( column_name  = "id",
                                          db_type      = "INTEGER",
                                             form_read_only       = True,
                                             rec_to_edit_cnv      = "cnv_int_to_str",
                                             dict_to_edit_cnv     = "cnv_int_to_str",
                                             edit_to_rec_cnv      = "cnv_str_to_int",
                                             edit_to_dict_cnv     = "cnv_str_to_int",


                                          display_type = "integer",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- "photo_id_old",
    a_column_dict = data_dict.ColumnDict( column_name  = "photo_id_old",
                                          db_type      = "VARCHAR(15)",
                                          display_type = "error",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- "table_id_old",
    a_column_dict = data_dict.ColumnDict( column_name  = "table_id_old",
                                          db_type      = "VARCHAR(15)",
                                          display_type = "error",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- "table_joined",
    a_column_dict = data_dict.ColumnDict( column_name  = "table_joined",
                                          db_type      = "VARCHAR(30)",
                                          display_type = "error",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- "photo_id",
    a_column_dict = data_dict.ColumnDict( column_name  = "photo_id",
                                          db_type      = "INTEGER",
                                          display_type = "integer",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- "table_id",
    a_column_dict = data_dict.ColumnDict( column_name  = "table_id",
                                          db_type      = "INTEGER",
                                          display_type = "integer",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )


    # ---- photo_in_show  ---------------------
    a_table_dict   = data_dict.TableDict(  "photo_in_show" )
    a_data_dict.add_table ( a_table_dict )

    # ---- "id",
    a_column_dict = data_dict.ColumnDict( column_name  = "id",
                                          db_type      = "INTEGER",

                                             form_read_only       = True,
                                             rec_to_edit_cnv      = "cnv_int_to_str",
                                             dict_to_edit_cnv     = "cnv_int_to_str",
                                             edit_to_rec_cnv      = "cnv_str_to_int",
                                             edit_to_dict_cnv     = "cnv_str_to_int",


                                          display_type = "integer",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- "photo_id_old",
    a_column_dict = data_dict.ColumnDict( column_name  = "photo_id_old",
                                          db_type      = "VARCHAR(15)",
                                          display_type = "error",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- "photo_show_id_old",
    a_column_dict = data_dict.ColumnDict( column_name  = "photo_show_id_old",
                                          db_type      = "VARCHAR(15)",
                                          display_type = "error",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- "sequence",
    a_column_dict = data_dict.ColumnDict( column_name  = "sequence",
                                          db_type      = "INTEGER",
                                          display_type = "integer",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- "photo_in_show_id_old",
    a_column_dict = data_dict.ColumnDict( column_name  = "photo_in_show_id_old",
                                          db_type      = "VARCHAR(15)",
                                          display_type = "error",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- "photo_id",
    a_column_dict = data_dict.ColumnDict( column_name  = "photo_id",
                                          db_type      = "INTEGER",
                                             form_read_only       = True,
                                             rec_to_edit_cnv      = "cnv_int_to_str",
                                             dict_to_edit_cnv     = "cnv_int_to_str",
                                             edit_to_rec_cnv      = "cnv_str_to_int",
                                             edit_to_dict_cnv     = "cnv_str_to_int",
                                          display_type = "integer",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- "photo_show_id",
    a_column_dict = data_dict.ColumnDict( column_name  = "photo_show_id",
                                          db_type      = "INTEGER",
                                             form_read_only       = True,
                                          display_type = "integer",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- "photo_in_show_id",
    a_column_dict = data_dict.ColumnDict( column_name  = "photo_in_show_id",
                                          db_type      = "INTEGER",
                                          display_type = "integer",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )


# --------------------
if __name__ == "__main__":
    #----- run the full app

    build_it()

# ---- eof




