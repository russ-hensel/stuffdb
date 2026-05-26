#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 13:32:32 2026

@author: russ
"""

# ---- tof



# ---------------------------------
class MixinBase(   ):
    """

    """
    def __init__( self,  ):
        """ """

    # ---------------------------------
    def replacement_1( self ):
        msg   = "replacement_1"
        print( msg )

# ---------------------------------
class Mixin( MixinBase   ):
    """
    second parent for QT edit child controls

    do not need prior value it is just sitting in the control

    get rid of is_changed ??
                prior_data
                events for above
    """
    def __init__( self,  ):
        """ """

    # ---------------------------------
    def replace_me( self ):
        msg   = "replace_me"
        print( msg )

# --------------------
if __name__ == "__main__":
    a_mixin  = Mixin()

    #a_mixin.replace_me    = MixinBase.replacement_1
        # ng TypeError: MixinBase.replacement_1() missing 1 required positional argument: 'self'

    a_mixin.replace_me    = a_mixin.replacement_1
        # works

    a_mixin.replace_me()





# ---- eof ---------------------------


