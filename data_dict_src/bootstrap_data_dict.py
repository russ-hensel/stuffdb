#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 08:51:22 2025
report on code gen and perhaps all code gen
   now code gen maybe in dict_main
"""

# ---- tof
import data_dict
#import dict_main
import adjust_path

# ---- imports

# ---- end imports

#-------------------------------

data_dict.build_it()



# ---- bootstrap

sql    = """
CREATE TABLE photo_subject  (
id  INTEGER,
photo_id_old  VARCHAR(15),
table_id_old  VARCHAR(15),
table_joined  VARCHAR(30),
photo_id  INTEGER,
table_id  INTEGER )
"""

#---- key gen
sql    = """
CREATE TABLE key_gen  (
table_name  VARCHAR(30),
key_value  INTEGER )
"""




# persons is a qt5_by_example
sql     = """
CREATE TABLE persons (
id   INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
age  INTEGER,
family_relation TEXT,
add_kw TEXT )
"""



# ---- photo_in_show
sql    = """
CREATE TABLE photo_in_show  (
id  INTEGER,
photo_id_old  VARCHAR(15),
photo_show_id_old  VARCHAR(15),
sequence  INTEGER,
photo_in_show_id_old  VARCHAR(15),
photo_id  INTEGER,
photo_show_id  INTEGER,
photo_in_show_id  INTEGER )

"""

# ---- stuff events   from the import dir unload.sql then change
# REMOVE EXCESS space
xxxxxsql    = """
CREATE TABLE stuff_event (
	id VARCHAR(15),
	stuff_id  VARCHAR(15) ,
	event_dt INTEGER,
	dlr  INTEGER,
	cmnt  VARCHAR(150),
	type  VARCHAR(15)    )
"""

# ---- people_phone
sql    = """
CREATE TABLE people_phone (
	seq_id  VARCAR(10),
	people_id VARCAR(10),
	type VARCAR(10),
	phone_old VARCAR(35),
	cmnt  VARCAR(40),
	phone VARCAR(100),
	autodial INTEGER  )
"""

data_dict.create_some_data_dict_from_sql(sql)





#data_dict.create_some_data_dict_from_sql(sql)

