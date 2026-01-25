#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""
photo
photo_text
photo_key_words

DB_NAME:        stuffdb

"""

#import adjust_path
import data_dict_all


# ---- build it
def build_it( a_data_dict_all ):
    """
    actual build of the data dict

    """

    # ---- photo ---------------------------------------------
    a_table_dict   = data_dict_all.TableDict( "photo" )
    a_data_dict_all.add_table ( a_table_dict )

    # ---- id
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "id",
                                             db_type        = "INTEGER",
                                             form_read_only       = True,
                                             rec_to_edit_cnv      = "cnv_int_to_str",
                                             dict_to_edit_cnv     = "cnv_int_to_str",
                                             edit_to_rec_cnv      = "cnv_str_to_int",
                                             edit_to_dict_cnv     = "cnv_str_to_int",
                                             form_make_ref   = True,
                                             display_type   = "integer",
                                             max_len        = None,
                                             default_func   = None,
                                             col_head_text      = "ID",
                                             col_head_width     = 10,
                                             col_head_order     = 1,
                                             display_order      = 0,
                                             form_col_span      = 1,  )
    a_table_dict.add_column( a_column_dict )

    # ---- id_old
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "id_old",
                                             db_type        = "VARCHAR(15)",
                                             form_read_only = True,
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,
                                             display_order      = 2,
                                             form_col_span      = 1,  )
    a_table_dict.add_column( a_column_dict )

    # ---- name
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "name",
                                             db_type        = "VARCHAR(150)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,
                                             is_key_word        = True,
                                             form_make_ref      = True,
                                             is_keep_prior_enabled = True,
                                             col_head_text      = "Name",
                                             col_head_width     = 40,
                                             col_head_order     = 10,
                                             display_order      = 10,
                                             form_col_span      = 4,  )

    a_table_dict.add_column( a_column_dict )

    # ---- add_kw
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "add_kw",
                                             db_type        = "VARCHAR(50)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func       = None,
                                             is_key_word        = True,
                                             is_keep_prior_enabled = True,
                                             col_head_text      = "Key Words",
                                             col_head_width     = 40,
                                             col_head_order     = 15,
                                             display_order      = 35,
                                             form_col_span      = 4,  )

    a_table_dict.add_column( a_column_dict )

    # ---- descr
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "descr",
                                             db_type        = "VARCHAR(240)",
                                             display_type   = "string",
                                             max_len            = None,
                                             default_func       = None,
                                             is_key_word        = True,
                                             is_keep_prior_enabled = True,
                                             col_head_text      = "Descr.",
                                             col_head_width     = 40,
                                             col_head_order     = 20,
                                             display_order      = 30,
                                             form_col_span      = 4,  )

    a_table_dict.add_column( a_column_dict )

    # ---- type
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "type",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- series
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "series",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- author
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "author",
                                             db_type        = "VARCHAR(35)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,
                                             is_key_word    = True,)
    a_table_dict.add_column( a_column_dict )

    # ---- dt_enter
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "dt_enter",
                                             db_type        = "INTEGER",
                                             detail_edit_class    = "cw.CQDateEdit",
                                             form_edit            = "cw.CQDateEdit",
                                             rec_to_edit_cnv      = "cnv_int_to_qdate",
                                             dict_to_edit_cnv     = "cnv_int_to_qdate",
                                             edit_to_rec_cnv      = "cnv_qdate_to_int",
                                             edit_to_dict_cnv     = "cnv_qdate_to_int",

                                             display_type   = "timestamp",
                                             max_len        = None,
                                             default_func   = None,
                                             display_order      = 200,
                                             form_read_only     = True,

                                             #form_col_span      = 2,
                                              )
    a_table_dict.add_column( a_column_dict )

    # ---- format
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "format",
                                             db_type        = "VARCHAR(20)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- inv_id
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "inv_id",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- cmnt
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "cmnt",
                                             db_type        = "VARCHAR(250)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,
                                             display_order      = 38,
                                             form_col_span      = 4,

                                              )
    a_table_dict.add_column( a_column_dict )

    # ---- status
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "status",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- dt_item
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "dt_item",
                                              db_type        = "INTEGER",
                                              display_type   = "timestamp",
                                              form_col_span      = 1,


                                             rec_to_edit_cnv      = "cnv_int_to_qdate",
                                             dict_to_edit_cnv     = "cnv_int_to_qdate",
                                             edit_to_rec_cnv      = "cnv_qdate_to_int",
                                             edit_to_dict_cnv     = "cnv_qdate_to_int",

                                             detail_edit_class  = "custom_widgets.CQDateEdit",
                                             form_edit          = "custom_widgets.CQDateEdit",


                                              max_len        = None,
                                              default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- c_name
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "c_name",
                                             db_type        = "VARCHAR(40)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- title
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "title",
                                             db_type        = "VARCHAR(35)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,
                                             is_key_word    = True,
                                             is_keep_prior_enabled = True,
                                             col_head_text      = "Title",
                                             col_head_width     = 40,
                                             col_head_order     = 12,
                                             display_order      = 25,
                                             form_col_span      = 4,
                                             form_make_ref   = True)
    a_table_dict.add_column( a_column_dict )

    # ---- tag
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "tag",
                                             db_type        = "DECIMAL(50)",
                                             display_type   = "skip",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- old_inv_id
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "old_inv_id",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- file
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "file",
                                             db_type        = "VARCHAR(100)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,
                                             display_order      = 42,
                                             form_col_span      = 4,
                                             form_make_ref   = True )
    a_table_dict.add_column( a_column_dict )

    # ---- sub_dir
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "sub_dir",
                                             db_type        = "VARCHAR(25)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,
                                             display_order         = 40,
                                             is_keep_prior_enabled = True,
                                             form_col_span      = 2,
                                             form_make_ref   = True )
    a_table_dict.add_column( a_column_dict )

    # ---- photo_url
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "photo_url",
                                             db_type        = "VARCHAR(75)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- camera
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "camera",
                                             db_type        = "VARCHAR(20)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,
                                             display_order      = 90,
                                             # form_col_span      = 2,
                                             )
    a_table_dict.add_column( a_column_dict )

    # ---- lens
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "lens",
                                             db_type        = "VARCHAR(20)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,
                                             display_order      = 92,
                                             # form_col_span      = 2,
                                             )
    a_table_dict.add_column( a_column_dict )

    # ---- f_stop
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "f_stop",
                                             db_type        = "DECIMAL(52)",
                                             display_type   = "skip",
                                             max_len        = None,
                                             default_func= None,
                                             display_order      = 94,
                                             # form_col_span      = 2,
                                             )
    a_table_dict.add_column( a_column_dict )

    # ---- shutter
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "shutter",
                                             db_type        = "INTEGER",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,
                                             display_order      = 96,
                                             # form_col_span      = 2,
                                             )
    a_table_dict.add_column( a_column_dict )

    # ---- copyright
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "copyright",
                                             db_type        = "VARCHAR(50)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    #print( a_table_dict )

    # ---- photo_text not in earlier stuff  ---------------------
    a_table_dict   = data_dict_all.TableDict(  "photo_text" )
    a_data_dict_all.add_table ( a_table_dict )

    a_column_dict = data_dict_all.ColumnDict(    column_name    = "id",
                                   db_type        = "INTEGER",

                                    form_read_only       = True,
                                    rec_to_edit_cnv      = "cnv_int_to_str",
                                    dict_to_edit_cnv     = "cnv_int_to_str",
                                    edit_to_rec_cnv      = "cnv_str_to_int",
                                    edit_to_dict_cnv     = "cnv_str_to_int",
                                   display_type   = "integer",
                                   max_len        = None,
                                   default_func= None,   )

    a_table_dict.add_column( a_column_dict )


    a_column_dict = data_dict_all.ColumnDict(    column_name    = "id_old_is_none",
                                   db_type        = "VARCHAR(15)",
                                   display_type   = "string",
                                   max_len        = None,
                                   default_func= None, )

    a_table_dict.add_column( a_column_dict )

    # ---- text_data -
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "text_data",
                                  db_type        = "TEXT",
                                  display_type   = "string",
                                  max_len        = None,
                                  default_func= None,
                                  placeholder_text   =
                                  "this is a long text\\nfield\\ncan hold many lines",)

    a_table_dict.add_column( a_column_dict )

    #rint( a_table_dict.to_sql() )



    # ---- photo_key_word ---------------------------------------------
    a_table_dict   = data_dict_all.TableDict( "photo_key_word" )
    a_data_dict_all.add_table ( a_table_dict )

    # ---- id
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "id",
                                             db_type        = "INTEGER",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- key_word
    a_column_dict = data_dict_all.ColumnDict(    column_name    = "key_word",
                                             db_type        = "TEXT",
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func= None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- table_code_end

    # ---- photo_subject  ---------------------
    a_table_dict   = data_dict_all.TableDict(  "photo_subject" )
    a_data_dict_all.add_table ( a_table_dict )

    a_column_dict = data_dict_all.ColumnDict( column_name  = "id",
                                          db_type      = "INTEGER",
                                          display_type = "integer",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    a_column_dict = data_dict_all.ColumnDict( column_name  = "photo_id_old",
                                          db_type      = "VARCHAR(15)",
                                          display_type = "error",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    a_column_dict = data_dict_all.ColumnDict( column_name  = "table_id_old",
                                          db_type      = "VARCHAR(15)",
                                          display_type = "error",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    a_column_dict = data_dict_all.ColumnDict( column_name  = "table_joined",
                                          db_type      = "VARCHAR(30)",
                                          display_type = "error",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    a_column_dict = data_dict_all.ColumnDict( column_name  = "photo_id",
                                          db_type      = "INTEGER",
                                          display_type = "integer",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    a_column_dict = data_dict_all.ColumnDict( column_name  = "table_id",
                                          db_type      = "INTEGER",
                                          display_type = "integer",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- photo_in_show   ---------------------
    a_table_dict   = data_dict_all.TableDict(  "photo_in_show" )
    a_data_dict_all.add_table ( a_table_dict )

    a_column_dict = data_dict_all.ColumnDict( column_name  = "id",
                                          db_type      = "INTEGER",
                                          display_type = "integer",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    a_column_dict = data_dict_all.ColumnDict( column_name  = "photo_id_old",
                                          db_type      = "VARCHAR(15)",
                                          display_type = "error",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    a_column_dict = data_dict_all.ColumnDict( column_name  = "photo_show_id_old",
                                          db_type      = "VARCHAR(15)",
                                          display_type = "error",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    a_column_dict = data_dict_all.ColumnDict( column_name  = "sequence",
                                          db_type      = "INTEGER",
                                          display_type = "integer",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    a_column_dict = data_dict_all.ColumnDict( column_name  = "photo_in_show_id_old",
                                          db_type      = "VARCHAR(15)",
                                          display_type = "error",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    a_column_dict = data_dict_all.ColumnDict( column_name  = "photo_id",
                                          db_type      = "INTEGER",
                                          display_type = "integer",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    a_column_dict = data_dict_all.ColumnDict( column_name  = "photo_show_id",
                                          db_type      = "INTEGER",
                                          display_type = "integer",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    a_column_dict = data_dict_all.ColumnDict( column_name  = "photo_in_show_id",
                                          db_type      = "INTEGER",
                                          display_type = "integer",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )



# --------------------
# if __name__ == "__main__":
#     #----- run the full app

#     build_it()

# # ---- eof

