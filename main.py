# -*- coding: utf-8 -*-
"""



"""
import os

# Get the directory of the current .py file
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the current working directory to the script's directory
os.chdir(script_dir)
print(os.getcwd())  # Prints the new working directory

import adjust_path
import stuffdb

stuffdb.main()
