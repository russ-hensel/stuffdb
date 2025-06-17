#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 13:06:44 2025

@author: russ
"""


# ---- tof

# ---- imports


# ---- end imports

def  say_hello():
    from   app_global import AppGlobal
    AppGlobal.q_app.welcome_msg()



def default_startup():
    """
    may be called on startup, sort of forget how
    """

    import parameter_check

    parameter_check.check_parameters()

    # here because of timing issues
    from app_global    import AppGlobal
    from help_document import HelpDocument

    AppGlobal.main_window.add_subwindow( window_class = HelpDocument, instance_ix = 1 )



# ---- eof