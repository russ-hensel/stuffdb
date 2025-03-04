#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 11:20:01 2024

chat

('Germany', 'France', 'UK');

"""
from PyQt5.QtSql import QSqlQuery

# Create a QSqlQuery object
query = QSqlQuery()

# List of values to match (for example, a list of IDs or names)
values = [1, 3, 5]

# Create a string of placeholders for the 'IN' clause (one '?' per value)
placeholders = ','.join(['?'] * len(values))

# Prepare the SQL query using the 'IN' clause with placeholders
query.prepare(f"SELECT * FROM people WHERE id IN ({placeholders})")

# Bind the values to the placeholders
for i, value in enumerate(values):
    query.bindValue(i, value)

# Execute the query
if query.exec_():
    while query.next():
        # Assuming the 'people' table has columns 'id' and 'name'
        id_ = query.value(0)  # The first column (id)
        name = query.value(1)  # The second column (name)
        print(f"ID: {id_}, Name: {name}")
else:
    print("Error executing query:", query.lastError().text())




" and kw_stuff.stuff_id = a.id "

SELECT ~"a~".~"id~",              ~"a~".~"name~",
        ~"a~".~"descr~",              ~"a~".~"type~",
        ~"a~".~"type_sub~",              ~"a~".~"author~",
          ~"a~".~"publish~",              ~"a~".~"dt_enter~",
          ~"a~".~"id_in~",              ~"a~".~"inv_id~",
          ~"a~".~"cmnt~",              ~"a~".~"status~",
          ~"a~".~"add_kw~",              ~"a~".~"c_name~",
          ~"a~".~"cont_type~",              ~"a~".~"manufact~"
          FROM ~"stuff~" ~"a~", kw_stuff  WHERE
          key_word in (  'one', 'three', 'two')
          and kw_stuff.stuff_id = a.id  GROUP BY ~"a~".~"id~",
          ~"a~".~"name~",              ~"a~".~"descr~",
          ~"a~".~"type~",              ~"a~".~"type_sub~",
          ~"a~".~"author~",              ~"a~".~"publish~",
          ~"a~".~"dt_enter~",              ~"a~".~"id_in~",
          ~"a~".~"inv_id~",              ~"a~".~"cmnt~",
          ~"a~".~"status~",              ~"a~".~"add_kw~",
          ~"a~".~"c_name~",              ~"a~".~"cont_type~",
          ~"a~".~"manufact~" HAVING  count(*) = 3



------------ works

SELECT   stuff.add_kw,  stuff.descr
    FROM stuff
    INNER JOIN stuff_key_word
    ON stuff.id = stuff_key_word.id
     WHERE  key_word IN ( "two", "three", "one")

     GROUP BY   stuff.add_kw,  stuff.descr
     HAVING  count(*) = 3;


------- runs


SELECT   stuff.add_kw,  stuff.descr
    FROM stuff
    INNER JOIN stuff_key_word
    ON stuff.id = stuff_key_word.id
     WHERE  key_word IN ( "word", "add"  )

     GROUP BY   stuff.add_kw,  stuff.descr
     HAVING  count(*) = 2;