#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 11:57:55 2024

@author: russ
"""
see update_old

ask for some sql to fill in default values is missing --- still to do

i have a table table_one with

the creation sql   = """ CREATE TABLE  table_one (
	id    			    INTEGER, integer,
	id_old    			VARCHAR(15),   string,
	text_type  			VARCHAR(15),   string,
	text_data       TEXT,          string,
)
    """)

and table_two with
the creation sql   = """ CREATE TABLE  table_two (
	id    			    INTEGER, integer,
	id_old    			VARCHAR(15),   string,
	text_stuff  			VARCHAR(15),   string,
	text_info      TEXT,          string,
)
    """)

Both tables are populated.
I would like to update table_two so that table_two.id = table_one.id if the
tables join on the id_old field.  Some items in table_two may be missing, I do not want to create them.



UPDATE table_two
SET table_two.id = table_one.id
FROM table_one
WHERE table_two.id_old = table_one.id_old;

However, SQLite does not natively support the FROM clause in an UPDATE statement. You can work around this by using a subquery instead:

UPDATE table_two
SET id = (
    SELECT table_one.id
    FROM table_one
    WHERE table_one.id_old = table_two.id_old
)
WHERE EXISTS (
    SELECT 1
    FROM table_one
    WHERE table_one.id_old = table_two.id_old
);
================================
so russ adjust for plant / plant_text



---- do these in combo  id=0 at the end is for failed matches
UPDATE plant_text
SET id = 0;


UPDATE plant_text
SET id = (
    SELECT plant.id
    FROM plant
    WHERE plant.id_old = plant_text.id_old
)
WHERE EXISTS (
    SELECT 1
    FROM plant
    WHERE plant.id_old = plant_text.id_old
);

================== for photosubject on one of columns
UPDATE photo_subject
SET photo_id = 0;

--- works but seems wrong
UPDATE photo_subject
SET photo_id = (
    SELECT photo.id
    FROM photo
    WHERE photo.id_old = photo_subject.photo_id_old
)
WHERE EXISTS (
    SELECT 1
    FROM photo
    WHERE photo.id_old = photo_subject.photo_id_old
    );


chat corrects to

UPDATE photo_subject
SET photo_id = (
    SELECT photo.id
    FROM photo
    WHERE photo.id_old = photo_subject.photo_id_old
)
WHERE EXISTS (
    SELECT 1
    FROM photo
    WHERE photo.id_old = photo_subject.photo_id_old
);


UPDATE photo_subject
SET photo_id = (
    SELECT photo.id
    FROM photo
    WHERE photo.id_old = photo_subject.photo_id_old
)
WHERE EXISTS (
    SELECT 1
    FROM photo
    WHERE photo.id_old = photo_subject.photo_id_old
    WHERE photo.id_old = photo_subject.photo_id_old
);
