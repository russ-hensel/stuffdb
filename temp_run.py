#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 09:05:42 2025

Executing SQL query: query_exec_model query.executedQuery() =
'SELECT   help_info.id,  help_info.title,  help_info.system, help_info.key_words
FROM help_info  \n    INNER JOIN  help_key_word  ON help_info.id = help_key_word.id  \n
WHERE  key_word IN ( "test" )   \n    GROUP BY   help_info.id,  help_info.title,  help_info.system,
help_info.key_words  \n    HAVING  count(*) >= 1  \n     ORDER BY  lower(help_info.title) ASC  '




 Intelligent Machines podcast









"""


# ---- tof

# ---- imports
#import adjust_path


from PyQt5.QtWidgets import QApplication, QMessageBox
import sys
import py_helpers
app = QApplication(sys.argv)

ret  = py_helpers.confirm_continue( "what follows next ")
print( ret )

# ---- eof