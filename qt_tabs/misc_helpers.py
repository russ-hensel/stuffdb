#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
module of helpers for >>py to extend functionality beyond just stuffdb.py ...
"""


# ---- tof

# ---- imports

# ---- end imports


#-------------------------------


from PyQt5.QtWidgets import (  QMessageBox, )

def confirm_continue( msg ):

    msg_box    = QMessageBox()
    msg_box.setIcon( QMessageBox.Information )
    msg_box.setText( msg )
    msg_box.setWindowTitle( "Continue?" )
    msg_box.setStandardButtons(  QMessageBox.Yes | QMessageBox.No )

    msg_box.setDefaultButton( QMessageBox.No  )

    ret    = msg_box.exec_()
    if ret == QMessageBox.No:
        1/0
        return False
    return True

import sys


def  print_sys_path(   ):
    """

    import misc_helpers
    misc_helpers.print_sys_path(   )
    """
    for i_path in sys.path:

        print( f"{i_path}" )


def  insert_path_if_missing( a_path_name ):
    """

    import misc_helpers
    misc_helpers.insert_if_missing( path )
    """
    #print( sys.path )  # is a list
    if not a_path_name in sys.path :
        sys.path.insert( 1, f"{a_path_name}" )
        print( "inserted" )
    else:
        print( "not needed no inserted" )
def  insert_if_missing( a_path_name ):
    """

    import misc_helpers
    misc_helpers.insert_if_missing( path )
    """
    #print( sys.path )  # is a list
    if not a_path_name in sys.path :
        sys.path.insert( 1, f"{a_path_name}" )
        print( "inserted" )
    else:
        print( "not needed no inserted" )

    # if a_path_name
    # sys.path.insert( 1, f"./py_helpers" )   # for installation off dev machines

def  list_to_toc( a_list ):
    """
    see notes >>search list_to_toc

    """
    print( "<details>" )
    print( "<summary>Table of Contents</summary>" )
    print()


    for i_topic in a_list:
        #  - [Find](#Find)
        print( f"- [{i_topic}](#{i_topic})")

    print( )
    print( "<details>" )

    for i_topic in a_list:
        #  - [Find](#Find)
        print( f"## {i_topic}")

    print()

def misc_example( ):
    print( "misc_example  44")

# ---- eof