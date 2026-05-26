# -*- coding: utf-8 -*-
"""
cannot restart in spyder without a new console
this could be fixed by creating a class and
calling its main.  do I want to do this??

"""

import adjust_path
import os

# Get the directory of the current .py file
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the current working directory to the script's directory
os.chdir(script_dir)
print(os.getcwd())  # Prints the new working directory

# from qt_compat import QApplication, QAction, exec_app, qt_version
# from PyQt.QtWidgets import QMainWindow, QToolBar, QMessageBox


import stuffdb

stuffdb.main()


