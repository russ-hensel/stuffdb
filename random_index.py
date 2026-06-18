#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=E221,E201,E202,C0325,E0611,W0201,W0612
# ---- tof
"""

Created on Fri Oct 15 16:18:43 2021

@author: russ



firest implementation, random dist over a range with a bias,
later have different methods


idea is to move ahaed in list, but in a semi-randoem way

"""

# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main   # noqa  stops auto removal by pycln

# --------------------

# ---- imports



import random
import string_utils


class PureRandomIndex(   ):
    """
    About this class.....

    """
    #----------- init -----------
    def __init__( self, length, start = 0, width = 20, bias = 5  ):
        """
        See class doc
        only length is used
        andom_index.RandomIndex( len( file_as_list ), self.parameter.spicture_ran_width, self.parameter.picture_ran_bias  )
        """
        # this is the constructor run when you create
        # like  app = AppClass( 55 )
        self.length              = length
        self.ix_now              = start
        self.width               = 10       # width around current item
        self.bias                = 2        # direction we tend to move
        self.last                = 0        # index of the last item from get_next  a lot like sef.now_ix



    #--------------------------
    def __str__( self ):
        """
        universal __str__
        """
        return string_utils.obj_to_str( self )

    # -----------------------------------
    def get_next(self):
        """
        what it says, read

        """
        ix_now          = random.randrange( 0, self.length )
        self.ix_now     = ix_now

        self.last       = ix_now

        return self.ix_now

# -----------------------------------
class SequentialIndex(   ):
    """
    just advance in order
    """
    #----------- init -----------
    def __init__( self, length, start = 0, width = 20, bias = 5  ):
        """
        See class doc
        andom_index.RandomIndex( len( file_as_list ), self.parameter.spicture_ran_width, self.parameter.picture_ran_bias  )
        """
        # this is the constructor run when you create
        # like  app = AppClass( 55 )
        self.length              = length
        self.ix_now              = 0
        # self.width               = 10       # width around current item
        # self.bias                = 2        # direction we tend to move
        # self.last                = 0        # index of the last item from get_next  a lot like sef.now_ix

    # -----------------------------------
    def get_next(self):
        """
        what it says, read
        ?? very inefficient
        """

        self.ix_now     = self.ix_now + 1
        self.ix_now     = self.ix_now % self.length
            # wrap around length both ways
        self.last       = self.ix_now
        return self.ix_now

    #--------------------------
    def __str__( self ):
        """
        universal __str__
        """
        return string_utils.obj_to_str( self )


# -----------------------------------
class SlightlyRandomIndex( object ):
    """
    About this class.....
    add the list and make a generator ?
    biased advance
    """
    #----------- init -----------
    def __init__( self, length, start = 0, width = 20, bias = 5  ):
        """
        See class doc
        andom_index.RandomIndex( len( file_as_list ), self.parameter.spicture_ran_width, self.parameter.picture_ran_bias  )
        """
        # this is the constructor run when you create
        # like  app = AppClass( 55 )
        self.length              = length
        self.ix_now              = start
        self.width               = 10       # width around current item
        self.bias                = 2        # direction we tend to move
        self.last                = 0        # index of the last item from get_next  a lot like sef.now_ix

    # -----------------------------------
    def get_next(self):
        """
        what it says, read
        ?? very inefficient
        """
        min             = int( - self.width/2 + self.bias )
        max             = int(   self.width/2 + self.bias )
        step            = random.randrange( min, max )
        self.ix_now     = self.ix_now + step
        self.ix_now     = self.ix_now % self.length
            # wrap around length both ways
        self.last       = self.ix_now
        return self.ix_now

    # -----------------------------------
    def __str__( self ):
        """
        universal __str__
        """
        return string_utils.obj_to_str( self )


# ---- eof


