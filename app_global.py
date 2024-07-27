# -*- coding: utf-8 -*-

"""
Purpose:
    part of my ( rsh ) library of reusable code
    a library module for multiple applications
	allows any module access to a set of application global values and functions
	typical use:
	from app_global import AppGlobal

    watch out this often uses injected values
    	self.parameters    = AppGlobal.parameters

        app_db    AppDB



"""

# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    main.main()
# --------------------


# import sys
# import webbrowser
# from   subprocess import Popen
# from   pathlib    import Path
# import os
# import psutil
# #from   tkinter    import messagebox
# import logging


# import sys

# next change used by russ in development
#sys.path.insert( 1, "../rshlib" )
# sys.path.insert( 1,  "/media/sf_0000/python00/python3/_projects/rshlib" )
# sys.path.insert( 1, r"D:\Russ\0000\python00\python3\_projects\rshlib"   )

# print( "Note: main.py may have changed the system path in a way not needed by your installation" )

# def main( ):
#     import clip_board
#     clip_board.main()

# # --------------------
# if __name__ == "__main__":
#     # #----- run the full app
#     main( )



# ------ local imports
import app_global_abc

# ------------------------------------------
class AppGlobal( app_global_abc.AppGlobalABC ):
    """
    use at class level ( do not _init_ ) for application globals,
    similar to but different from parameters
    some global functions
    """
    # class var supress liner messages and better anyway
    snipper             = None      # populated by ...
    cmd_processor       = None      # populated by ...
    commands            = None      # populated by ...
    double_buttons      = None      # populated by ...
    do_transforms       = None      # populated by ...
    snippeter           = None      # populated by ...  !! dup name or what


    # ----------------------------------------------
    def __init__(self,  controller  ):

        yyyyy  = 1/0    # this guy should not be created and this stops it



# ======================== eof ======================





