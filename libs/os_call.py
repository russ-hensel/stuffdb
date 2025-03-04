#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 12:30:09 2024

@author: russ

Extracted from app_glbal


"""
#---- imports
#import abc

import webbrowser
from pathlib import Path
from subprocess import Popen


# ------------------------
class OSCall(  ):
    """
    try to call os based on attempts with different utilities
    in different operating systems
    """
    #------------------------
    def __init__(self, command_list, ):
        """
        command list is the list of utilities to try, a list of strings
        command_aux: like command list but may be a list, a single string, or none, see code

        """
        self.command_list     = []
        self.add_command( command_list )
        self.working_command  = None

    # ----------------------------------------------
    def add_command( self, more_command_list ):
        """
        add a command at the beginning and re init the list
        call internally at init or externally ( parameters ) to add to list
        """
        #rint( f"adding {more_command_list}")
        if more_command_list is None:
            self.command_list        = more_command_list
            # [   r"D:\apps\Notepad++\notepad++.exe", r"gedit", r"xed", r"leafpad"   ]
            # or init from parameters or put best guess first

        else:
            if type( more_command_list ) ==  str:
                more_command_list  = [ more_command_list ]
            # else we expect a list
            self.command_list = more_command_list + self.command_list

        self.ix_command          = -1
        self.working_command     = None
        #rint( f"command list now{self.command_list}")

    # ----------------------------------------------
    def get_next_command( self,  ):
        """
        what it says
        None if cannot find one ( at end of list )
        """
        self.ix_command += 1
        if         self.ix_command >= len( self.command_list ):
            ret =  None
        else:
            ret =         self.command_list[ self.ix_command ]
        #rint( f"command = { self.ix_command} {ret} ", flush = True )
        return ret

    # ----------------------------------------------
    def os_call( self, cmd_arg,  ):
        """
        make an os call trying various utilities until one works
        """
        while True:   # will exit when it works or run out of editors
            a_command    = self.working_command
            if  a_command is None:
                a_command  = self.get_next_command( )

            if a_command is None:
                msg = f"Run out of editors to try >{a_command}< >{cmd_arg}<"

                raise RuntimeError( msg )
                    #break  # think we are already done
            try:
                if cmd_arg is None:
                    proc = Popen( [ a_command,  ] )
                else:
                    proc = Popen( [ a_command, cmd_arg ] )
                self.working_command  = a_command
                break  # do not get here if exception
            except Exception as excpt:
                pass     # this should let us loop -- a bit broad but?


# ---- eof
