#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  4 16:54:38 2025

@author: russ
"""


# ---- tof

# ---- imports

# ---- end imports


#-------------------------------






# ---- eof

sql  = """

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

sql  = """
CREATE TABLE photo_in_show_key_word  (
id  INTEGER,
key_word  TEXT )

"""