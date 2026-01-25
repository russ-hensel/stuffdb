#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 10 14:59:39 2026

@author: russ
"""


# ---- tof


import data_dict

table_name    = "stuff"

INDENT_A      = 10* " "
ATTR_LIST     =  [ "col_head_order",
                    "col_head_text",
                    "col_head_width",
                    "column_name", ]


                    # "create_self",
                    # "db_type",
                    # "default_func",
                    # "detail_edit_class",
                    # "dict_to_edit_cnv",
                    # "display_order" ]


    # #------------------------------------------------
    # def to_upgrade_self(self,    ):
    #     """
    #     upgrade the current dict to a better version of itself
    #     """
    #     #1/0   # now a down grade


#-------------------------------
data_dict.build_it()




# self.getattr(


def  col_to_str( a_str, column ):




        a_str    = ""

        a_str    = f"{a_str}\na_column_dict = data_dict.ColumnDict(\n"



        for ix, i_attribute in enumerate( ATTR_LIST ):
            value        = getattr( column, i_attribute )
            if     value is None:   # none is default so do not include
                continue

            elif type( value ) == int:
                pass
            else:
                value    = f'"{value}"'


            a_str          = f'{a_str}{INDENT_A}self.{i_attribute:<20}    = {value},\n'

        a_str          = f'{a_str}{INDENT_A} )\n'
        a_str          = f'{a_str}a_table_dict.add_column( a_column_dict ) )\n'

        return a_str





# ---- run

a_table     = data_dict.DATA_DICT.get_table( table_name )

print( a_table.to_build_form( ) )

columns     = a_table.get_list_columns_sql_order()

for ix_column, i_column in enumerate( columns ):
    msg     = ( f"{ix_column}  {i_column} ")
    #print( msg )

    a_str     = f"{table_name} ========================================================\n"




    print( col_to_str( a_str, i_column ) )

# ---- eof







