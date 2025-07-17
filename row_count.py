#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 08:28:17 2025

@author: russ
"""


# ---- tof

# ---- imports

# ---- end imports


#-------------------------------






# ---- eof



    for ix_line, i_line in enumerate( file_src ) :

        i_line_issue     = i_line
        ix_line_issue    = ix_line
        try:
            if VERBOSE:
                print( f"importing line >>>>>{ix_line}")
            i_line           = i_line.rstrip( '\n' )
            splits           = i_line.split( TAB   )
            #rint( f"{len(splits) = }")

            # since source was checked we should not care
            # we should get n splits  id not in file does not count  !! this should be above split code
            # if len( splits ) != 25:
            #     pass
            #     msg     =  ( f"wrong len of splits at line {ix_line} {len( splits ) = } {i_line}")
            #     #rint( msg )
            #     raise Exception( msg )   # will be caught below

            # ---- to_import_splits len(name_list)-1 = 25

1             a_id            = ix_line + KEY_OFFSET
2             id_old          = import_utils.no_quotes( splits[2 ] )
3             name            = import_utils.no_quotes( splits[1 + 2 ] )
4             add_kw          = import_utils.no_quotes( splits[2  + 2 ] )
5             descr           = import_utils.no_quotes( splits[3 + 2  ] )
6             a_type          = import_utils.no_quotes( splits[4  + 2 ] )
7             series          = import_utils.no_quotes( splits[5  + 2 ] )
8             author          = import_utils.no_quotes( splits[6  + 2 ] )
9             dt_enter        = import_utils.string_to_ts_min( splits[7  + 2   ] )
10             a_format        = import_utils.no_quotes( splits[8  + 2   ] )
11             inv_id          = import_utils.no_quotes( splits[9  + 2  ] )
12             cmnt            = import_utils.no_quotes( splits[10  + 2  ] )
13             status          = import_utils.no_quotes( splits[11  + 2  ] )
14             dt_item         = import_utils.string_to_ts_min( splits[12  + 2  ] )
15             c_name          = import_utils.no_quotes( splits[13  + 2  ] )
16             title           = import_utils.no_quotes( splits[14   + 2 ] )
17             tag             = import_utils.no_quotes( splits[15  + 2  ] )
18             old_inv_id      = import_utils.no_quotes( splits[16  + 2 ] )
19             file            = import_utils.no_quotes( splits[17  + 2  ] ).lower()
20             sub_dir         = import_utils.no_quotes( splits[18  + 2 ] ).lower()
21             photo_url       = import_utils.no_quotes( splits[19  + 2 ] )
22             camera          = import_utils.no_quotes( splits[20  + 2 ] )
23             lens            = import_utils.no_quotes( splits[21  + 2  ] )
24             f_stop          = import_utils.no_quotes( splits[22  + 2  ] )
25             shutter         = import_utils.string_to_int( import_utils.no_quotes( splits[23 + 2  ] ) )
26             a_copyright     = import_utils.no_quotes( splits[24  + 2  ] )


            # ---- code gen most of this
            # ---- code_gen: sql_to_insert_bind  -- begin


            # ---- import sql
            sql        = """INSERT INTO    photo (
1                 id,
2                 id_old,
3                 name,
4                 add_kw,
5                 descr,
6                 type,
7                 series,
8                 author,
9                 dt_enter,
10                 format,
11                 inv_id,
12                 cmnt,
13                 status,
14                 dt_item,
15                 c_name,
16                 title,
17                 tag,
18                 old_inv_id,
19                 file,
20                 sub_dir,
21                 photo_url,
22                 camera,
23                 lens,
24                 f_stop,
25                 shutter,
26                 copyright )

                 VALUES (
1                 :a_id,
2                 :id_old,
3                 :name,
4                 :add_kw,
5                 :descr,
6                 :type,
7                 :series,
8                 :author,
9                 :dt_enter,
10                 :format,
11                 :inv_id,
12                 :cmnt,
13                 :status,
14                 :dt_item,
15                 :c_name,
16                 :title,
17                 :tag,
18                 :old_inv_id,
19                 :file,
20                 :sub_dir,
21                 :photo_url,
22                 :camera,
23                 :lens,
24                 :f_stop,
25                 :shutter,
26                 :copyright ) """

            if VERBOSE:
                print( f"{name = } {dt_enter = } {dt_item = } { splits[7 ] = }")

            query = QSqlQuery( db )

            query.prepare( sql )

1             query.bindValue( ":a_id", a_id )
2             query.bindValue( ":id_old", id_old )
3             query.bindValue( ":name", name )
4             query.bindValue( ":add_kw", add_kw )
5             query.bindValue( ":descr", descr )
6             query.bindValue( ":type", a_type )
7             query.bindValue( ":series", series )
8             query.bindValue( ":author", author )
9             query.bindValue( ":dt_enter", dt_enter )
10             query.bindValue( ":format", a_format )
11             query.bindValue( ":inv_id", inv_id )
12             query.bindValue( ":cmnt", cmnt )
13             query.bindValue( ":status", status )
14             query.bindValue( ":dt_item", dt_item )
15             query.bindValue( ":c_name", c_name )
16             query.bindValue( ":title", title )
17             query.bindValue( ":tag", tag )
18             query.bindValue( ":old_inv_id", old_inv_id )
19             query.bindValue( ":file", file )
20             query.bindValue( ":sub_dir", sub_dir )
21             query.bindValue( ":photo_url", photo_url )
22             query.bindValue( ":camera", camera )
23             query.bindValue( ":lens", lens )
24             query.bindValue( ":f_stop", f_stop )
25             query.bindValue( ":shutter", shutter )
26             query.bindValue( ":copyright", a_copyright )

        # ---- code_gen: sql_to_insert_bind  -- end table entries

            # ---- code_gen: sql_to_insert_bind  -- end table entries

            if not query.exec_( ):


for table table_name = 'photo'
CREATE TABLE  photo    (
1      id  INTEGER,
2      id_old  VARCHAR(15),
3      name  VARCHAR(150),
4      add_kw  VARCHAR(50),
5      descr  VARCHAR(240),
6      type  VARCHAR(15),
7      series  VARCHAR(15),
8      author  VARCHAR(35),
9      dt_enter  INTEGER,
10      format  VARCHAR(20),
11      inv_id  VARCHAR(15),
12      cmnt  VARCHAR(250),
13      status  VARCHAR(15),
14      dt_item  INTEGER,
15      c_name  VARCHAR(40),
16      title  VARCHAR(35),
17      tag  DECIMAL(50),
18      old_inv_id  VARCHAR(15),
19      file  VARCHAR(100),
20      sub_dir  VARCHAR(25),
21      photo_url  VARCHAR(75),
22      camera  VARCHAR(20),
23      lens  VARCHAR(20),
24      f_stop  DECIMAL(52),
25      shutter  INTEGER,
26      copyright  VARCHAR(50)
    )


CREATE TABLE photo    (
1      id  INTEGER,
2      id_old  VARCHAR(15),
3      name  VARCHAR(150),
4      add_kw  VARCHAR(50),
5      descr  VARCHAR(240),
6      type  VARCHAR(15),
7      series  VARCHAR(15),
8      author  VARCHAR(35),
9      dt_enter  INTEGER,
10      format  VARCHAR(20),
11      inv_id  VARCHAR(15),
12      cmnt  VARCHAR(250),
13      status  VARCHAR(15),
14      c_name  VARCHAR(40),
15      title  VARCHAR(35),
16      tag  DECIMAL(50),
17      old_inv_id  VARCHAR(15),
18      file  VARCHAR(100),
19      sub_dir  VARCHAR(25),
20      photo_url  VARCHAR(75),
21      camera  VARCHAR(20),
22      lens  VARCHAR(20),
23      f_stop  DECIMAL(52),
24      shutter  INTEGER,
25      copyright  VARCHAR(50)
    )

seems one short why
from pb
1 	"id"    			char(15) NOT NULL,
2 	"name"  			char(150) NULL,
3 	"add_kw"        		char(35) NULL,
4 	"descr" 			char(240) NULL,
5 	"type"  			char(15) NULL,
6 	"series"        		char(15) NULL,
7 	"author"        		char(35) NULL,
8 	"dt_enter"      		date NULL,
9 	"format"        		char(20) NULL,
10 	"inv_id"        		char(15) NULL,
11 	"cmnt"  			char(250) NULL,
12 	"status"        		char(10) NULL,
13 	"dt_item"       		date NULL,
14 	"c_name"        		char(35) NULL,
15 	"title" 			char(35) NULL,
16 	"tag"   			numeric(5,0) NULL,
17 	"old_inv_id"    		char(15) NULL,
18 	"file"  			char(60) NULL,
19 	"sub_dir"       		char(25) NULL,
20 	"photo_url"     		varchar(75) NULL,
21 	"camera"        		varchar(20) NULL,
22 	"lens"  			varchar(20) NULL,
23 	"f_stop"        		numeric(5,2) NULL,
24 	"shutter"       		integer NULL,
25 	"copyright"     		varchar(50) NULL,