#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 08:47:54 2025

@author: russ
"""


# ---- tof

# ---- imports

# ---- end imports


#-------------------------------






# ---- eof


Sql Create for table


            # ---- sql_to_insert_bind ---- code gen

            sql        =   """INSERT INTO    photo (
1             id,
2             id_old,
3             name,
4             add_kw,
5             descr,
6             type,
7             series,
8             author,
9             dt_enter,
10             format,
11             inv_id,
12             cmnt,
13             status,
14             dt_item,
15             c_name,
16             title,
17             tag,
18             old_inv_id,
19             file,
20             sub_dir,
21             photo_url,
22             camera,
23             lens,
24             f_stop,
25             shutter,
26             copyright

            VALUES (
1             :id,
2             :id_old,
3             :name,
4             :add_kw,
5             :descr,
6             :type,
7             :series,
8             :author,
9             :dt_enter,
10             :format,
11             :inv_id,
12             :cmnt,
13             :status,
14             :dt_item,
15             :c_name,
16             :title,
17             :tag,
18             :old_inv_id,
19             :file,
20             :sub_dir,
21             :photo_url,
22             :camera,
23             :lens,
24             :f_stop,
25             :shutter,
26             :copyright
             ) """

            query.prepare( sql )

1             query.bindValue( ":id", id )
2             query.bindValue( ":id_old", id_old )
3             query.bindValue( ":name", name )
4             query.bindValue( ":add_kw", add_kw )
5             query.bindValue( ":descr", descr )
6             query.bindValue( ":type", type )
7             query.bindValue( ":series", series )
8             query.bindValue( ":author", author )
9             query.bindValue( ":dt_enter", dt_enter )
10             query.bindValue( ":format", format )
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
26             query.bindValue( ":copyright", copyright )

            # ---- sql_to_insert_bind ---- code gen ends
CREATE TABLE photo    (
1 CREATE TABLE photo    (
2      id  INTEGER,
3      id_old  VARCHAR(15),
4      name  VARCHAR(150),
5      add_kw  VARCHAR(50),
6      descr  VARCHAR(240),
7      type  VARCHAR(15),
8      series  VARCHAR(15),
9      author  VARCHAR(35),
10      dt_enter  INTEGER,
11      format  VARCHAR(20),
12      inv_id  VARCHAR(15),
13      cmnt  VARCHAR(250),
14      status  VARCHAR(15),
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
27     )
    )