#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 13:54:05 2024

@author: russ
"""

to_chat = """

please write the sql to join these two tables on

photo_in_show.photo_id   = photo.id

return  photo_show_id, photo.file and photo.sub_dir


CREATE TABLE  photo_in_show  (
id  INTEGER,
photo_id_old  VARCHAR(15),
photo_show_id_old  VARCHAR(15),
sequence  INTEGER,
photo_in_show_id_old  VARCHAR(15),
photo_id  INTEGER,
photo_show_id  INTEGER,
photo_in_show_id  INTEGER )

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
status  VARCHAR(15),
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


"""
chat_says = """
sql

SELECT
    photo_in_show.photo_show_id,
    photo.file,
    photo.sub_dir
FROM
    photo_in_show
INNER JOIN
    photo
ON
    photo_in_show.photo_id = photo.id;

works in db bever  and so does



SELECT
    photo_in_show.photo_show_id,
    photo.file,
    photo.sub_dir
FROM
    photo_in_show
INNER JOIN
    photo
ON
    photo_in_show.photo_id = photo.id

WHERE photo_in_show.photo_show_id  = 10078



"""




!next
Query Execution Error: Parameter count mismatch

!next
Executing SQL query:  query.executedQuery() = '\n        SELECT\n            photo.id,\n            photo.name,\n            photo.photo_fn\n        FROM\n            photo_subject\n        JOIN\n            photo\n        ON\n            photo_subject.photo_id = photo.id\n        WHERE\n            photo_subject.table_joined = :table_joined\n        AND\n            photo_subject.table_id     = :table_id;\n        '

!next

!next

        SELECT
            photo.id,
            photo.name,
            photo.photo_fn
        FROM
            photo_subject
        JOIN
            photo
        ON
            photo_subject.photo_id = photo.id
        WHERE
            photo_subject.table_joined = :table_joined
        AND
            photo_subject.table_id     = :table_id;

	file  			VARCHAR(100),    string,
	sub_dir       	VARCHAR(25),    string,

this works except for id

       SELECT
           photo.id,
           photo.name,
           photo.file,
           photo.sub_dir
       FROM
           photo_subject
       JOIN
           photo
       ON
           photo_subject.photo_id = photo.id
       WHERE
           photo_subject.table_joined = "planting"
       AND
           photo_subject.table_id     = 10178;

Execution finished without errors.
Result: 5 rows returned in 33ms
At line 1:
SELECT
           photo.id,
           photo.name,
           photo.file,
           photo.sub_dir
       FROM
           photo_subject
       JOIN
           photo
       ON
           photo_subject.photo_id = photo.id
       WHERE
           photo_subject.table_joined = "planting"
       AND
           photo_subject.table_id     = 10178;

above is one of few that selects, then not the right items but
click on row not found does not 404 and does not transfer to the picuter tab

3281	Sarah''s Climbing Rose (s)	60212_09.jpg
3282	Sahara''s Climbing Rose (s)	60212_10.jpg
3283	Sahara''s Climbing Rose (s)	60212_11.jpg


seems like it should join

photo
3281	brsh381	Sarah''s Climbing Rose (s)
id


planting                        photo_id   table id
1598	brsh381	27	planting	3281	   10178
1599	brsh382	27	planting	3282	   10178
1600	brsh383	27	planting	3283	   10178
1744	rsh55177	27	planting	9999	10178
1751	rsh55185	27	planting	9999	10178

10178	27	Sarah''s Climbing Rose (s) on Fence	76	Fence to M&P (Front)

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


this is in code does it work
        SELECT
           photo.id,
           photo.name,
           photo.file,
           photo.sub_dir
        FROM
            photo_subject
        JOIN
            photo
        ON
            photo_subject.photo_id = photo.id
        WHERE
            photo_subject.table_joined = :table_joined
        AND
            photo_subject.table_id     = :table_id;


SELECT
           photo.id,
           photo.name,
           photo.file,
           photo.sub_dir
       FROM
           photo_subject
       JOIN
           photo
       ON
           photo_subject.photo_id = photo.id
       WHERE
           photo_subject.table_joined = "planting"
       AND
           photo_subject.table_id     = 10178;