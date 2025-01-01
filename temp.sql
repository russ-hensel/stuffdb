#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 08:48:54 2024

@author: russ
"""
could you please join these two tabls ( give me the sql
            CREATE TABLE people (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                name            TEXT NOT NULL,
                age             INTEGER,
                family_relation TEXT


            CREATE TABLE people_phones (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id       INTEGER,
                phone_number    TEXT,
                FOREIGN KEY(person_id) REFERENCES people(id) ON DELETE CASCADE
            )

I notice there's a small syntax error in your table definitions - the first CREATE TABLE statement is missing its closing parenthesis. I'll help you join these tables with SQL, assuming the fixed schema.



```sql
-- Basic join to get all people and their phone numbers
SELECT
    p.id,
    p.name,
    p.age,
    p.family_relation,
    pp.phone_number
FROM people p
LEFT JOIN people_phones pp ON p.id = pp.person_id;

-- Alternative version with column aliases and formatting
SELECT
    p.id AS person_id,
    p.name AS full_name,
    p.age,
    p.family_relation AS relation,
    COALESCE(pp.phone_number, 'No phone') AS contact_number
FROM people p
LEFT JOIN people_phones pp ON p.id = pp.person_id
ORDER BY p.name;

```

I've provided two queries:

1. A basic LEFT JOIN that will show all people and their phone numbers (if they have any)
2. An enhanced version that:
   - Uses better column aliases
   - Handles NULL phone numbers by showing 'No phone' instead
   - Sorts the results by name

I used a LEFT JOIN instead of an INNER JOIN to ensure we see all people, even those without phone numbers. Would you like me to explain any part of the query or show different join variations?



```sql
-- Basic join to get all people and their phone numbers
SELECT
    people.id,
    people.name,
    people.age,
    people.family_relation,
    people_phones.phone_number
FROM people
LEFT JOIN people_phones ON people.id = people_phones.person_id
SELECT
    people.id,
    people.name,
    people.age,
    people.family_relation,
    people_phones.phone_number
FROM people
LEFT JOIN people_phones ON people.id = people_phones.person_id

WHERE peopli.id = 2;


-- Alternative version with NULL handling
SELECT
    people.id,
    people.name,
    people.age,
    people.family_relation,
    COALESCE(people_phones.phone_number, 'No phone') AS phone_number
FROM people
LEFT JOIN people_phones ON people.id = people_phones.person_id
ORDER BY people.name;

```

I've removed all the table aliases (p and pp) and used the full table names instead.
The queries will work exactly the same way, they're just more explicit now. Which version do you prefer?


SELECT
    people.id,
    people.name,
    people.age,
    people.family_relation,
    people_phones.phone_number
FROM people
LEFT JOIN people_phones ON people.id = people_phones.person_id

WHERE peopli.id = 2;

The explicit version is indeed clearer, especially for maintainability. Here's the final query we'll go with:

```sql
SELECT
    people.id,
    people.name,
    people.age,
    people.family_relation,
    COALESCE(people_phones.phone_number, 'No phone') AS phone_number
FROM people
LEFT JOIN people_phones ON people.id = people_phones.person_id
ORDER BY people.name;

```

This query will:
1. Show all people from the 'people' table
2. Include their phone numbers from 'people_phones' if they exist
3. Show 'No phone' for people without phone numbers
4. Sort everyone by name

The explicit table names make it immediately clear which table each column comes from.