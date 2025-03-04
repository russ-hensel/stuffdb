#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""
Created on Fri Jan 31 12:47:07 2025

@author: russ
"""

# ---- imports
#import adjust_path
import data_dict
# ---- end imports




# ---- build it
def build_it( a_data_dict ):
    """


    """
    #a_data_dict    = data_dict.DATA_DICT

    #---- table_code

    # ---- persons  ---------------------
    a_table_dict   = data_dict.TableDict(  "persons" )
    a_data_dict.add_table ( a_table_dict )

    # ---- "id",
    a_column_dict = data_dict.ColumnDict( column_name  = "id",
                                          db_type      = "INTEGER",
                                          display_type = "error",
                                          max_len        = None,
                                          default_func   = None,
                                          display_order      = 1,
                                          # next is  automatic off db dype
                                          #edit_to_rec   = "edit_to_rec_str_to_int",
                                          #rec_to_edit   = "rec_to_edit_int_to_str",
                                          )
    a_table_dict.add_column( a_column_dict )

    # ---- "name",
    a_column_dict = data_dict.ColumnDict( column_name  = "name",
                                          db_type      = "VARCHAR(150)",
                                          display_type = "error",
                                          max_len        = None,
                                          default_func   = None,
                                          display_order      = 100,)
    a_table_dict.add_column( a_column_dict )

    # ---- "age",
    a_column_dict = data_dict.ColumnDict( column_name  = "age",
                                          db_type      = "VARCHAR(150)",
                                          display_type = "string",
                                          max_len        = None,
                                          default_func   = None,
                                          display_order      = 5,
                                          edit_to_rec   = "edit_to_rec_str_to_int",
                                          rec_to_edit   = "rec_to_edit_int_to_str",
                                                    )
    a_table_dict.add_column( a_column_dict )

    # ---- "family_relation",
    a_column_dict = data_dict.ColumnDict( column_name  = "family_relation",
                                          db_type      = "TEXT",
                                          display_type = "string",
                                          max_len        = None,
                                          default_func   = None,
                                          display_order      = 20,)
    a_table_dict.add_column( a_column_dict )

    # ---- "add_kw",
    a_column_dict = data_dict.ColumnDict( column_name  = "add_kw",
                                          db_type      = "VARCHAR(150)",
                                          display_type = "string",
                                          max_len        = None,
                                          default_func   = None,
                                          display_order      = 12,)
    a_table_dict.add_column( a_column_dict )







# ---- eof