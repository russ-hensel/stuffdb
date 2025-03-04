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
    #---- table_code

    # ---- photoshow ---------------------------------------------
    a_table_dict   = data_dict.TableDict( "photoshow" )
    a_data_dict.add_table ( a_table_dict )

    # ---- id
    a_column_dict = data_dict.ColumnDict(    column_name    = "id",
                                             db_type        = "INTEGER",
                                             display_type   = "string",
                                             display_order  = 0,
                                             max_len        = None,
                                             default_func   = None,
                                             col_head_text      = "ID",
                                             col_head_width     = 10,
                                             col_head_order     = 1, )
    a_table_dict.add_column( a_column_dict )

    # ---- id_old
    a_column_dict = data_dict.ColumnDict(    column_name    = "id_old",
                                             db_type        = "VARCHAR(15)",
                                             display_order  = 1,
                                             display_type   = "string",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- name
    a_column_dict = data_dict.ColumnDict(    column_name    = "name",
                                             db_type        = "VARCHAR(50)",
                                             display_type   = "string",
                                             display_order  = 10,
                                             max_len        = None,
                                             default_func   = None,
                                             is_key_word    = True,
                                             col_head_text      = "ID",
                                             col_head_width     = 10,
                                             col_head_order     = 1,
                                             )
    a_table_dict.add_column( a_column_dict )

    # ---- cmnt
    a_column_dict = data_dict.ColumnDict(    column_name    = "cmnt",
                                             db_type        = "VARCHAR(100)",
                                             display_type   = "string",
                                             display_order  = 20,
                                             max_len        = None,
                                             default_func   = None,
                                             col_head_text      = "Comment",
                                             col_head_width     = 25,
                                             col_head_order     = 1,
                                           )
    a_table_dict.add_column( a_column_dict )

    # ---- start_date
    a_column_dict = data_dict.ColumnDict(    column_name    = "start_date",
                                             db_type        = "INTEGER",
                                             display_type   = "timestamp",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- end_date
    a_column_dict = data_dict.ColumnDict(    column_name    = "end_date",
                                             db_type        = "INTEGER",
                                             display_type   = "timestamp",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- create_date
    a_column_dict = data_dict.ColumnDict(    column_name    = "create_date",
                                             db_type        = "INTEGER",
                                             display_type   = "timestamp",
                                             max_len        = None,
                                             default_func   = None,   )
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
                                             max_len        = None,
                                             default_func   = None,
                                             is_key_word    = True,
                                             col_head_text      = "Key Words",
                                             col_head_width     = 10,
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
                                             display_type   = "string",
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

    # ---- table_code_end



# --------------------
if __name__ == "__main__":
    #----- run the full app

    build_it()

# ---- eof




