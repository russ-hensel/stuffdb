#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 09:06:57 2024

@author: russ
"""
"""

# ---- create ================================



CREATE TABLE  photo  (
id  INTEGER,
id_old  VARCHAR(15),
name  VARCHAR(150),
add_kw  VARCHAR(50),
descr  VARCHAR(240),
type  VARCHAR(15),
series  VARCHAR(15),
author  VARCHAR(35),
dt_enter  INTEGER,
format  VARCHAR(20),
inv_id  VARCHAR(15),
cmnt  VARCHAR(250),
status  VARCHAR(15)Any,
dt_item  INTEGER,
c_name  VARCHAR(40),
title  VARCHAR(35),
tag  DECIMAL(50),
old_inv_id  VARCHAR(15),
file  VARCHAR(100),
sub_dir  VARCHAR(25),
photo_url  VARCHAR(75),
camera  VARCHAR(20),
lens  VARCHAR(20),
f_stop  DECIMAL(52),
shutter  INTEGER,
copyright  VARCHAR(50) )

# ---- from picture document
"""
SELECT   photo.id,  photo.name,  photo.add_kw,  photo.descr,  photo.file, photo.sub_dir    FROM photo
    WHERE  file IS NOT NULL and  file != ""  AND   dt_item >= :start_date_edit
"""



"""
# ---- dt_item ======================================
# ---- select all --------------------------------
"""  =============== Execution finished without errors.
Result: 12253 rows returned in 70ms

SELECT
               photo.id,
               photo.id_old,
               photo.dt_item

    FROM       photo

    ORDER BY   photo.dt_item;



============== ok
SELECT
               photo.id,
               photo.id_old,
               photo.dt_item

    FROM       photo
    WHERE      photo.dt_item > 3019
    ORDER BY   photo.dt_item;



"""

""" ============= fix "8/15/97"  1997, 8, 15  = 871617600
   ============= Execution finished without errors.
Result: 20 rows returned in 6ms


SELECT
               photo.id,
               photo.id_old,
               photo.dt_item

    FROM       photo
    WHERE      photo.dt_item = "8/15/97"
    ORDER BY   photo.dt_item;


=================  Execution finished without errors.
Result: query executed successfully. Took 2ms, 20 rows affected

UPDATE photo
SET dt_item = 871617600
WHERE photo.dt_item = "8/15/97";


================= Execution finished without errors.
Result: 22 rows returned in 12ms

SELECT
               photo.id,
               photo.id_old,
               photo.dt_item

    FROM       photo
    WHERE      photo.dt_item = "1/1/00"
    ORDER BY   photo.dt_item;

"""
# ---- fix  photo.dt_item = "1/1/00"  1980  1, 1 =  315550800
"""
 ======================= 1980  1, 1 =  315550800
Execution finished without errors.
Result: query executed successfully. Took 1ms, 22 rows affected

UPDATE photo
SET dt_item =  315550800
WHERE photo.dt_item = "1/1/00";



8/1/97

"""

""" =============  ok 0 rows


SELECT
               photo.id,
               photo.id_old,
               photo.dt_item

    FROM       photo
    WHERE      photo.dt_item = ""
    ORDER BY   photo.dt_item;




"""
""" =============    Execution finished without errors.
Result: 2877 rows returned in 33ms


SELECT
               photo.id,
               photo.id_old,
               photo.dt_item

    FROM       photo
    WHERE      photo.dt_item is Null
    ORDER BY   photo.dt_item;



"""
""" ======================= 1980  1, 1 =  315550800
Execution finished without errors.
Result: query executed successfully. Took 4ms, 2877 rows affected
At line 1:

do not qualify the columns with table names



UPDATE photo
SET photo.dt_item = 315550800
WHERE photo.dt_item IS NULL;



"""

from ex_datetime
my birthday  -776528100.0

1980  1, 1 =  315550800


1/1/00






# ---- dt_enter ======================================

# ---- select all --------------------------------
"""  =============== Execution finished without errors.
Result: 12253 rows returned in 70ms
Execution finished without errors.
Result: 12253 rows returned in 39ms

SELECT
               photo.id,
               photo.id_old,
               photo.dt_enter

    FROM       photo

    ORDER BY   photo.dt_enter;

lots of nulls

"""

"""
Execution finished without errors.
Result: 1158 rows returned in 10ms


SELECT
               photo.id,
               photo.id_old,
               photo.dt_enter

    FROM       photo
    WHERE      photo.dt_enter is Null
    ORDER BY   photo.dt_enter;

"""
# ---- fix  photo.dt_enter is Null"  1980  1, 1 =  315550800
"""
 =======================
Execution finished without errors.
Result: query executed successfully. Took 4ms, 1158 rows affected

UPDATE photo
SET dt_enter =  315550800
WHERE photo.dt_enter is Null;


"""
