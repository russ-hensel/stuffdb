#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 18:17:55 2025

@author: russ

DB_NAME:        stuffdb


"""

import data_dict_all


# ---- build it
def build_it( a_data_dict_all ):
    """
    build then data dictionary for a table or two

    """

    # ---- stuff_text ---------------------
    a_table_dict   = data_dict_all.TableDict(  "key_gen" )
    a_data_dict_all.add_table ( a_table_dict )


    a_column_dict = data_dict_all.ColumnDict( column_name  = "table_name",
                                          db_type      = "VARCHAR(30)",
                                          display_type = "error",
                                          max_len        = None,
                                          default_func   = None,
                                          primay_key_ix  = 0,)
    a_table_dict.add_column( a_column_dict )

    a_column_dict = data_dict_all.ColumnDict( column_name  = "key_value",
                                          db_type      = "INTEGER",
                                          display_type = "integer",
                                          max_len        = None,
                                          default_func   = None,   )
    a_table_dict.add_column( a_column_dict )



# # --------------------
# if __name__ == "__main__":
#     #----- run the full app

#     test()
# # --------------------
