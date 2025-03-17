#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
master place to get the table defining sql as a string

import  code_gen_sql_create
sql   = code_gen_sql_create.sql_dict["help_info"]


INTEGER,    for dates
 VARCHAR(xx),
Decimal

DECIMAL( 5, 2)   for money....


"""


sql_dict     = { }

# each entry is just the defining string needs parsing to be meaningful may have n components per line


# ---- help_info --------------------------------
table_name   = "help_info"
sql = (
"""
    CREATE TABLE  help_info (
    	id    			    INTEGER,         integer
        id_old      	    VARCHAR(15),     string
    	type  			    VARCHAR(15),     string
    	sub_system    	    VARCHAR(15),     string
    	system        		VARCHAR(15),     string
    	key_words     		VARCHAR(70),     string
    	add_ts        		INTEGER,         timestamp
    	edit_ts       		INTEGER,         timestamp
    	table_name    		VARCHAR(40),     string
    	column_name   		VARCHAR(40),      string
    	java_type     		VARCHAR(20),      string
    	java_name     		VARCHAR(175),     string
    	java_package  		VARCHAR(150),     string
    	title 			    VARCHAR(150),     string
    	is_example    		VARCHAR(1),       string
    	can_execute   		VARCHAR(1),       string
    )
"""

)

sql_dict[ table_name ] = sql

# ---- help_text ----------------
# id                     INTEGER PRIMARY KEY  UNIQUE NOT NULL,

table_name   = "help_text"
sql   = """
    CREATE TABLE  help_text    (
         id                     INTEGER,          integer,
    	 id_old      			VARCHAR(15),      string,
    	 text_data      		TEXT,             string,
    )
    """

sql_dict[ table_name ] = sql


# ---- "help_key_word" ----------------
table_name   = "help_key_word"

sql = (
"""
        CREATE TABLE IF NOT EXISTS help_key_word (
            id          INTEGER,      integer,
            key_word    TEXT,          string,
        )
    """)

sql_dict[ table_name ] = sql

# ---- people ----------------------------------------------------------------------------
table_name   = "people"

sql = (
"""CREATE TABLE people   (
	id    			INTEGER,          integer,
	id_old          VARCHAR(15),      string,
	add_kw        	VARCHAR(50),     string,
	descr 			VARCHAR(50),     string,
	type  			VARCHAR(15),     string,
	type_sub      	VARCHAR(15),     string,
	dt_enter      	INTEGER,       timestamp,
	cmnt  			VARCHAR(250),     string,
	status        	VARCHAR(10),     string,
	l_name        	VARCHAR(45),     string,
	f_name        	VARCHAR(35),     string,
	st_adr_1      	VARCHAR(35),     string,
	st_adr_2      	VARCHAR(35),     string,
	st_adr_3      	VARCHAR(35),     string,
	city  			VARCHAR(35),     string,
	state 			VARCHAR(25),     string,
	zip   			VARCHAR(15),     string,
	m_name        	VARCHAR(25),     string,
	dt_item       	INTEGER,         timestamp,
	c_name        	VARCHAR(55),     string,
	title 			VARCHAR(35),     string,
	dddd  			VARCHAR(5),     string,
	department    	VARCHAR(15),     string,
	floor 			VARCHAR(15),     string,
	location      	VARCHAR(40),     string,
	role_text     	VARCHAR(40),     string,
	assoc_msn     	VARCHAR(60),     string,
	bussiness_house   VARCHAR(40),     string,
	country       		VARCHAR(40),     string,
	autodial      		INTEGER,       integer,
)
    """)

sql_dict[ table_name ] = sql

# ---- people_text ----------------
table_name   = "people_text"

sql = (
"""
 CREATE TABLE  people_text   (
     id              INTEGER,
 	 id_old    		 VARCHAR(15),
     text_type       VARCHAR(15),
     text_data       TEXT
 )
""")
sql_dict[ table_name ] = sql

# ---- people_key_word ----------------
table_name   = "people_key_word"

sql = (
"""
        CREATE TABLE IF NOT EXISTS people_key_word (
            id          INTEGER,   integer,
            key_word    TEXT,       string,
        )
    """)

sql_dict[ table_name ] = sql


# ---- photo ----------------------------------------------------
table_name   = "photo"

# splits on whitespace
# consider move to tab sep file


sql = (
""" CREATE TABLE  photo   (
	id              INTEGER,         integer,
    id_old    		VARCHAR(15),     string,
	name  			VARCHAR(150),    string,
	add_kw        	VARCHAR(50),     string,
	descr 			VARCHAR(240),    string,
	type  			VARCHAR(15),    string,
	series        	VARCHAR(15),    string,
	author        	VARCHAR(35),    string,
	dt_enter      	INTEGER,      timestamp,
	format        	VARCHAR(20),    string,
	inv_id        	VARCHAR(15),    string,
	cmnt  			VARCHAR(250),    string,
	status        	VARCHAR(15),    string,
	dt_item       	INTEGER,    timestamp,
	c_name        	VARCHAR(40),    string,
	title 			VARCHAR(35),    string,
	tag   			DECIMAL(5,0),    skip,
	old_inv_id    	VARCHAR(15),    string,
	file  			VARCHAR(100),    string,
	sub_dir       	VARCHAR(25),    string,
	photo_url     	VARCHAR(75),    string,
	camera        	VARCHAR(20),    string,
	lens  			VARCHAR(20),    string,
	f_stop        	DECIMAL(5,2),    skip,
	shutter         INTEGER,        string,
	copyright     	VARCHAR(50),    string,
    )
    """)

sql_dict[ table_name ] = sql

# ---- photo_key_word ----------------
table_name   = "photo_key_word"

sql = (
"""CREATE TABLE IF NOT EXISTS photo_key_word (
            id          INTEGER,    integer,
            key_word    TEXT,       string,
        )
    """)

sql_dict[ table_name ] = sql


# ---- photo_subject ----------------
table_name   = "photo_subject"

sql = (
""" CREATE TABLE photo_subject (
    id                     INTEGER,    integer,
	photo_id_old      		VARCHAR(15),  string,
	table_id_old      		VARCHAR(15),   string,
	table_joined  		VARCHAR(30),     string,
    photo_id           INTEGER,        integer,
    table_id              INTEGER,       integer,
     )
    """)

sql_dict[ table_name ] = sql



# ---- photoshow ----------------
table_name   = "photoshow"

sql = (
""" CREATE TABLE  photoshow  (
	id    			INTEGER,      integer,
    id_old          VARCHAR(15),  string,
	name  			VARCHAR(50),  string,
	cmnt  			VARCHAR(100),  string,
	start_date    	INTEGER,       timestamp,
	end_date      	INTEGER,       timestamp,
	create_date   	INTEGER,       timestamp,
	type  			VARCHAR(20),  string,
	add_kw        	VARCHAR(50),  string,
	web_site_dir  	VARCHAR(240),  string,
    )
    """)

sql_dict[ table_name ] = sql

# ---- photoshow_key_word ----------------
table_name   = "photoshow_key_word"

sql = (
"""CREATE TABLE IF NOT EXISTS photoshow_key_word (
            id          INTEGER,    integer,
            key_word    TEXT,       string,
        )
    """)

sql_dict[ table_name ] = sql

# ---- photo in show ----------------
table_name   = "photo_in_show"

# PRIMARY KEY ("photo_in_show_id") WITH HASH SIZE 10  not sure needed or used

sql = (
""" CREATE TABLE  photo_in_show  (
    id                      INTEGER,      integer,
	photo_id_old      		VARCHAR(15),  string,
	photo_show_id_old 		VARCHAR(15),  string,
	sequence      		    INTEGER,     integer,
	photo_in_show_id_old    VARCHAR(15),  string,
	photo_id      		    INTEGER,     integer,
	photo_show_id		    INTEGER,     integer,
	photo_in_show_id        INTEGER,      integer,
    )
    """)

sql_dict[ table_name ] = sql

# ---- photo_key_word ----------------
table_name   = "photo_in_show_key_word"

sql = (
"""CREATE TABLE IF NOT EXISTS photo_in_show_key_word (
            id          INTEGER,    integer,
            key_word    TEXT,       string,
        )
    """)

sql_dict[ table_name ] = sql


# ---- key_gen ----------------------------------------------------
table_name   = "key_gen"
# PRIMARY KEY UNIQUE NOT NULL,
sql = (
""" CREATE TABLE key_gen (
            table_name      VARCHAR(30),  string,
            key_value       INTEGER       integer,
        )
    """)

sql_dict[ table_name ] = sql

# ---- plant ----------------------------------------------------
table_name   = "plant"

sql = (
""" CREATE TABLE  plant  (
    id                    INTEGER,       integer,
	id_old    			  VARCHAR(15),     string,
	name  			      VARCHAR(75),     string,
	latin_name    		  VARCHAR(75),     string,
	add_kw        	      VARCHAR(40),     string,
	descr 		    	   VARCHAR(250),     string,
	plant_type  			      VARCHAR(25),     string,
	type_sub      		  VARCHAR(15),     string,
	cmnt  			     VARCHAR(250),     string,
	life  			     VARCHAR(20),     string,
	water 			     VARCHAR(20),     string,
	sun_min       		   VARCHAR(20),     string,
	sun_max       		   VARCHAR(20),     string,
	zone_min      	      VARCHAR(2),     string,
	zone_max      		  VARCHAR(2),     string,
	height          	   	INTEGER,     int7-2,
	form  		    	 VARCHAR(20),     string,
	color 		    	 VARCHAR(30),     string,
	pref_unit     		   VARCHAR(10),     string,
	hybridizer    		    VARCHAR(50),     string,
	hybridizer_year       	   INTEGER,     integer,
	color2        		    VARCHAR(30),     string,
	color3        		   VARCHAR(30),     string,
	life2 			  VARCHAR(20),     string,
	tag1  			   VARCHAR(15),     string,
	chromosome    	   VARCHAR(15),     string,
	bloom_time    		   VARCHAR(15),     string,
	bloom_dia     	     INTEGER,     int5-2,
	fragrance     		   VARCHAR(15),     string,
	rebloom       		   VARCHAR(15),     string,
	itag1 			   INTEGER,     integer,
	extended      		  VARCHAR(1),     string,
	plant_class 			  VARCHAR(15),     string,
	source_type   	  VARCHAR(15),     string,
	source_detail 		   VARCHAR(60),     string,
	spider        	   VARCHAR(10),     string,
	spider_ratio  		 INTEGER,     int5-2,
	double        		   VARCHAR(1),     string,
)
    """)

sql_dict[ table_name ] = sql


# ---- stuff_key_word ----------------
table_name   = "plant_key_word"

sql = (
"""
        CREATE TABLE IF NOT EXISTS  plant_key_word (
            id          INTEGER,    integer,
            key_word    TEXT,       string,
        )
    """)

sql_dict[ table_name ] = sql




# ---- plant_text ----------------------------------------------------
table_name   = "plant_text"

sql = (
""" CREATE TABLE  plant_text (
	id    			INTEGER, integer,
	id_old    			VARCHAR(15),   string,
	text_type  			VARCHAR(15),   string,
	text_data       TEXT,          string,
)
    """)

sql_dict[ table_name ] = sql



# ---- planting ----------------------------------------------------
table_name   = "planting"

sql = (
""" CREATE TABLE   planting   (
    id                   INTEGER,       integer,
	id_old   			 VARCHAR(15),      string,
	name  			     VARCHAR(60),       string,
	plant_id      		 VARCHAR(15),     string,
	bed_old       		 VARCHAR(20),      string,
	location      		 VARCHAR(75),      string,
	add_kw        		 VARCHAR(50),      string,
	descr 			     VARCHAR(250),      string,
	type  			     VARCHAR(15),    string,
	cmnt  			     VARCHAR(250),    string,
	lbl   			     VARCHAR(25),    string,
	bed   			     VARCHAR(15),    string,
	lbl_name      		 VARCHAR(30),    string,
	itag1 			     INTEGER,        integer,
	planting_status      VARCHAR(15),    string,
	need_stake    		 INTEGER,       integer,
	need_label    		 INTEGER,      integer,
	need_work     		 INTEGER,     integer,
)
    """)

sql_dict[ table_name ] = sql

# ---- planting_key_word ----------------
table_name   = "planting_key_word"

sql = (
"""
        CREATE TABLE IF NOT EXISTS  planting_key_word (
            id          INTEGER,    integer,
            key_word    TEXT,       string,
        )
    """)

sql_dict[ table_name ] = sql


# ---- planting_event ----------------
table_name   = "planting_event"
# put new at end planting_id as an integer
sql = (
""" CREATE TABLE planting_event    (
    id                      INTEGER,
	id_old   			    VARCHAR(15),,    string,
	planting_id_old   		VARCHAR(15),,    string,
	event_dt      		    INTEGER,    string,
	dlr   			        DECIMAL( 7,2),     integer,
	cmnt  			        VARCHAR(250),    string,
	type  			        VARCHAR(15),    string,
	dt_mo 			        DECIMAL(  11,0),    string,
	dt_day        	        DECIMAL(  11,0),
	day_of_year   	        INTEGER,
	planting_id             INTEGER
)
    """)

sql_dict[ table_name ] = sql




# ---- stuff ----------------------------------------------------
table_name   = "stuff"

sql = (
"""
 CREATE TABLE  stuff   (
    id              INTEGER,      integer,
 	id_old    		VARCHAR(15),  string,
 	add_kw        	VARCHAR(50),  string,
 	descr 			VARCHAR(50),  string,
 	type  			VARCHAR(15),  string,
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

sql_dict[ table_name ] = sql


# ---- stuff text ----------------
table_name   = "stuff_text"

sql = (
"""
 CREATE TABLE  stuff_text   (
     id              INTEGER,         integer,
 	 id_old    		 VARCHAR(15),   string,
     text_type       VARCHAR(15),  string,
     text_data       TEXT,           string,
 )
""")

sql_dict[ table_name ] = sql


# ---- stuff_key_word ----------------
table_name   = "stuff_key_word"

sql = (
"""
        CREATE TABLE IF NOT EXISTS  stuff_key_word (
            id          INTEGER,    integer,
            key_word    TEXT,       string,
        )
    """)

sql_dict[ table_name ] = sql