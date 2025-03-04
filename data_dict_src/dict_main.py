#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""
Created on Thu Jan  2 17:21:25 2025

@author: russ
/mnt/WIN_D/Russ/0000/python00/python3/_projects/stuffdb/data_dict_src/ data_dict help .py
"""

import adjust_path

# DATA_DICT  = None

import data_dict
#import data_dict_stuff
#import data_dict_photo


def  build_it():
    """may be dup in data_dict  """
    # global DATA_DICT
    if data_dict.DATA_DICT:
        return data_dict.DATA_DICT

    # data_dict.build_it_old( "stuffdb")

    # return

    import data_dict_help
    data_dict_help.build_it( data_dict.DATA_DICT )

    # import data_dict_people
    # data_dict_people.build_it( data_dict.DATA_DICT )

    import data_dict_photo     # missing photo_subject
    data_dict_photo.build_it( data_dict.DATA_DICT )

    import data_dict_plant
    data_dict_plant.build_it( data_dict.DATA_DICT )

    import data_dict_planting
    data_dict_planting.build_it( data_dict.DATA_DICT )

    import data_dict_people
    data_dict_people.build_it( data_dict.DATA_DICT )

    import data_dict_stuff
    data_dict_stuff.build_it( data_dict.DATA_DICT )

    import data_dict_photoshow
    data_dict_photoshow.build_it( data_dict.DATA_DICT )

    #rint( f"{data_dict.DATA_DICT}" )
    print( "DATA_DICT created ")
    return data_dict.DATA_DICT


    # data_dict.DATA_DICT.print_table( "photo" )


    # a_table    = data_dict.DATA_DICT.get_table( "photo_key_word" )
    # # sql         = a_table.to_sql_create ()
    # # print( sql )

    # print( f"{a_table}" )
    # print( a_table.to_build_form() )


def code_gen():

    # ---- pick table  -- alpha please
    # a_table    = data_dict.DATA_DICT.get_table( "photo_key_word" )
    # a_table    = data_dict.DATA_DICT.get_table( "help_info" )
    #a_table    = data_dict.DATA_DICT.get_table( "help_text" )
    a_table    = data_dict.DATA_DICT.get_table( "people" )
    a_table    = data_dict.DATA_DICT.get_table( "photoshow" )
    # a_table    = data_dict.DATA_DICT.get_table( "plant" )
    # a_table    = data_dict.DATA_DICT.get_table( "planting" )
    # a_table    = data_dict.DATA_DICT.get_table( "photo" )
#    a_table    = data_dict.DATA_DICT.get_table( "stuff_text" )

    # ---- action

    # sql         = a_table.to_sql_create ()
    # print( sql )

    # print( f"{a_table}" )

    print( a_table.to_build_form()     )
    #print( a_table.to_history_list()   )

    #print( a_table    )

    # # ---- or now in rpt_data_dict
    # table_name   = "help_info"
    # table_name   = "people"
    # column_list    = data_dict.DATA_DICT.get_history_columns( table_name )
    # for i_column in column_list:
    #     print( f"    {i_column.column_name}")


# -------------------- a_data_dict
if __name__ == "__main__":
    #----- run the full app


    build_it()
    code_gen()

# ---- eof
