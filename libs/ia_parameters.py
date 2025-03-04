#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 16:09:47 2024

@author: russ
"""



global PARAMETERS
PARAMETERS   = None


# ========================================
class Parameters( ):
    """
    manages parameter values: use it like an ini file but it is code
    """


    # -------
    def __init__( self, ):
        """
        Init for instance, usually not modified, except perhaps debug stuff
        ( if any )... but use plus_test_mode()
        may be down in listing because it should not be messed with.
        """
        self.mode_default()

    # -------
    def choose_mode( self ):
        """
        typically choose one mode
            and if you wish add the plus_test_mode
            if you comment all out all modes you get the default mode which should
            run, perhaps not in the way you want
        """
        #self.mode_russ_on_theprof()

    # ------->> default mode, always call
    def mode_default( self ):
        """
        sets up pretty much all settings
        documents the meaning of the modes
        call first, then override as necessary
        good chance these settings will at least let the app run
        """
        self.mode              = "mode_default"
        self.dir_for_search    = [ "/mnt/WIN_D/russ/0000/python00/python3/_projects/rshlib/in_spect/" ]
            # where we seareh for inofmation about modules

if PARAMETERS is None:
    PARAMETERS  = Parameters()


# ---- eof