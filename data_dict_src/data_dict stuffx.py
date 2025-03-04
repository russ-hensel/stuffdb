#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 11:50:38 2025

@author: russ
"""

import data_dict




def build_it():
    """


    """
    import data_main
    a_data_dict    = data_main.DATA_DICT

    sql = (
    """
     CREATE TABLE  stuff_text   (

         text_type       VARCHAR(15),  string,
         text_data       TEXT,           string,
     )
    """)


    # ---- stuff_text ---------------------
    a_table_dict   = data_dict.TableDict(  "stuff_text" )
    a_data_dict.add_table ( a_table_dict )

    a_column_dict = data_dict.ColumnDict(    column_name    = "id",
                                             db_type        = "INTEGER",
                                             display_type   = "integer",
                                             max_len        = None,
                                             default        = None,   )

    a_table_dict.add_column( a_column_dict )


    a_column_dict = data_dict.ColumnDict(    column_name    = "id_old",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )

    a_table_dict.add_column( a_column_dict )

    # ---- text_data
    a_column_dict = data_dict.ColumnDict(    column_name    = "text_type",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )



    # ---- text_data
    a_column_dict = data_dict.ColumnDict(    column_name    = "text_data",
                                             db_type        = "TEXT",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )

    a_table_dict.add_column( a_column_dict )

    print( a_table_dict.to_sql() )

    # ---- stuff -------------------------------

    sql = (
    """
 CREATE TABLE  stuff   (


 	type_sub      	VARCHAR(15),  string,
 	author        	VARCHAR(50),  string,
 	publish       	VARCHAR(50),  string,
 	model 			VARCHAR(35),  string,
 	serial_no     	VARCHAR(35),  string,
 	value 			INTEGER,        integer,
 	project       	VARCHAR(20),  string,
 	file  			VARCHAR(40),  string,
 	owner 			VARCHAR(35),  string,
 	dt_enter      	INTEGER,   timestamp,
 	start_ix      	VARCHAR(10),  string,
 	end_ix        	VARCHAR(10),  string,
 	sign_out      	VARCHAR(35),  string,
 	format        	VARCHAR(20),  string,
 	inv_id        	VARCHAR(15),  string,
 	cmnt  			VARCHAR(250),  string,
 	status        	VARCHAR(10),  string,
 	id_in_old		VARCHAR(15),  string,
 	dt_item       	INTEGER,   timestamp,
 	c_name        	VARCHAR(35),  string,
 	performer     	VARCHAR(35),  string,
 	cont_type     	VARCHAR(15),  string,
 	url   			VARCHAR(150),  string,
 	author_f      	VARCHAR(50),  string,
 	title 			VARCHAR(150),  string,
 	name  			VARCHAR(150),  string,
 	loc_add_info  	VARCHAR(150),  string,
 	manufact      	VARCHAR(100),  string,
 )
""")



    a_table_dict   = data_dict.TableDict(  "stuff" )
    a_data_dict.add_table ( a_table_dict )

    # ---- id
    a_column_dict = data_dict.ColumnDict(    column_name    = "id",
                                             db_type        = "INTEGER",
                                             display_type   = "integer",
                                             max_len        = None,
                                             default        = None,   )
    a_table_dict.add_column( a_column_dict )

    # ---- id_old
    a_column_dict = data_dict.ColumnDict(    column_name    = "id_old",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )

    # ---- add_kw
    a_column_dict = data_dict.ColumnDict(    column_name    = "add_kw",
                                             db_type        = "VARCHAR(50)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )

    # ---- descr
    a_column_dict = data_dict.ColumnDict(    column_name    = "descr",
                                             db_type        = "VARCHAR(50)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )

    # ---- type
    a_column_dict = data_dict.ColumnDict(    column_name    = "type",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )

    a_table_dict.add_column( a_column_dict )

    # ----type_sub
    a_column_dict = data_dict.ColumnDict(    column_name    = "type_sub",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )

    # ----author
    a_column_dict = data_dict.ColumnDict(    column_name    = "author",
                                             db_type        = "VARCHAR(50)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )

    # ----publish
    a_column_dict = data_dict.ColumnDict(    column_name    = "publish",
                                             db_type        = "VARCHAR(50)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )

    # ---- model
    a_column_dict = data_dict.ColumnDict(    column_name    = "model",
                                             db_type        = "VARCHAR(35)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )

    # ----serial_no
    a_column_dict = data_dict.ColumnDict(    column_name    = "serial_no",
                                             db_type        = "VARCHAR(35)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )

    # ---- value
    a_column_dict = data_dict.ColumnDict(    column_name    = "value",
                                             db_type        = "INTEGER",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )

    # ---- 	project
    a_column_dict = data_dict.ColumnDict(    column_name    = "project",
                                             db_type        = "VARCHAR(20)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )


    # ---- file
    a_column_dict = data_dict.ColumnDict(    column_name    = "file",
                                             db_type        = "VARCHAR(40)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )

    # ---- owner
    a_column_dict = data_dict.ColumnDict(    column_name    = "owner",
                                             db_type        = "VARCHAR(32)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )

    # ---- dt_enter
    a_column_dict = data_dict.ColumnDict(    column_name    = "dt_enter",
                                             db_type        = "INTEGER",
                                             display_type   = "timestamp",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )

    # ---- start_ix
    a_column_dict = data_dict.ColumnDict(    column_name    = "start_ix",
                                             db_type        = "VARCHAR(10)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )

    # ---- end_ix
    a_column_dict = data_dict.ColumnDict(    column_name    = "end_ix",
                                             db_type        = "VARCHAR(10)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )

    # ---- sign_out
    a_column_dict = data_dict.ColumnDict(    column_name    = "sign_out",
                                             db_type        = "VARCHAR(35)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )

    # ---- format
    a_column_dict = data_dict.ColumnDict(    column_name    = "format",
                                             db_type        = "VARCHAR(20)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )

    # ---- inv_id
    a_column_dict = data_dict.ColumnDict(    column_name    = "inv_id",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )

    # ---- cmnt
    a_column_dict = data_dict.ColumnDict(    column_name    = "cmnt",
                                             db_type        = "VARCHAR(10)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )

    # ---- status
    a_column_dict = data_dict.ColumnDict(    column_name    = "status",
                                             db_type        = "VARCHAR(250)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )

    # ---- id_in_old
    a_column_dict = data_dict.ColumnDict(    column_name    = "id_in_old",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )

    # ---- dt_item
    a_column_dict = data_dict.ColumnDict(    column_name    = "dt_item",
                                             db_type        = "INTEGER",
                                             display_type   = "timestamp",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )

    # ---- c_name
    a_column_dict = data_dict.ColumnDict(    column_name    = "c_name",
                                             db_type        = "VARCHAR(35)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )

    # ---- performer
    a_column_dict = data_dict.ColumnDict(    column_name    = "performer",
                                             db_type        = "VARCHAR(35)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )

    # ---- cont_type
    a_column_dict = data_dict.ColumnDict(    column_name    = "cont_type",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )

    # ---- url
    a_column_dict = data_dict.ColumnDict(    column_name    = "url",
                                             db_type        = "VARCHAR(150)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )

    # ---- author_f
    a_column_dict = data_dict.ColumnDict(    column_name    = "author_f",
                                             db_type        = "VARCHAR(50)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )


    # ---- title
    a_column_dict = data_dict.ColumnDict(    column_name    = "title",
                                             db_type        = "VARCHAR(150)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )


    # ---- name
    a_column_dict = data_dict.ColumnDict(    column_name    = "name",
                                             db_type        = "VARCHAR(150)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )


    # ---- loc_add_info
    a_column_dict = data_dict.ColumnDict(    column_name    = "loc_add_info",
                                             db_type        = "VARCHAR(150)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )

    # ---- manufact
    a_column_dict = data_dict.ColumnDict(    column_name    = "manufact",
                                             db_type        = "VARCHAR(100)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )

    print( a_table_dict.to_sql() )

    # ---- stuff_key_word -----------------------------------
    a_table_dict   = data_dict.TableDict(  "stuff_key_word" )
    a_data_dict.add_table ( a_table_dict )

    a_column_dict = data_dict.ColumnDict(    column_name    = "key_word",
                                             db_type        = "TEXT",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None,   )
    a_table_dict.add_column( a_column_dict )

    print( a_table_dict.to_sql() )

    print( a_data_dict )

build_dd()


# --------------------
if __name__ == "__main__":
    #----- run the full app

    test()
# --------------------
