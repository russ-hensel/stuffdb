#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""
APPLICATION:    info_about
# will sort from high first to low --- class names put more base first
SORT_ORDER:     5

class name in order from most specialized to least -- can we assume
any are built that are not in this module -- for now no
CLASS_NAMES:    InfoAboutList  InfoAboutString InfoAboutDatetime InfoAboutTimeDelta
"""

from datetime import datetime, timedelta

import info_about as ia

# ---- end imports


DEBUGGING       = False  # in testing may be changed externally


INDENT          = ia.INDENT
INDENT2         = ia.INDENT2

MAX_REPR_LEN    = ia.MAX_REPR_LEN
MAX_STR_LEN     = ia.MAX_STR_LEN
MAX_LIST_ITEMS  = ia.MAX_LIST_ITEMS

NEW_LINE        = "\n"


if DEBUGGING:
    pass


# ---- now the actural cases --------------------------------
# -----------------------------------
class InfoAboutList( ia.InfoAboutBase  ):
    """
    What it says
        this will be the only child class with doc strings
        unless they differ from this one
    """
    #----------- init -----------
    def __init__(self,   ):
        """
        Usual init see class doc string
        """
        super( ).__init__(     )  # message
        self.my_class    = list

    #-------------------------
    def custom_info( self ):
        """
        this should be the custom inspection for this type ( is instance )
        """
        self.add_line(  "custom_info for a list" )

        # list out some items
        ix = 0
        for  i_value in self.inspect_me:
            self.add_line( f"{self.xin}{INDENT2}>{i_value}<" )

            #a_str   = f"{a_str}\n{xin}{INDENT2}{i_value}"
            ix += 1
            if ix > MAX_LIST_ITEMS:
                more_items   = len(self.inspect_me) - MAX_LIST_ITEMS
                self.add_line( f"{self.xin}{INDENT}and{more_items} more items.... " )
                #a_str   = f"{a_str}\n{xin}{INDENT}and {len(a_obj) - max_items} more items.... "

                break
    # --------------------------
    def have_info_forxxx( self, a_obj ):
        """
        """
        have_info  = isinstance(  a_obj, list  )
        return have_info

# -----------------------------------
class InfoAboutDict( ia.InfoAboutBase  ):

    #----------- init -----------
    def __init__(self,   ):

        super( ).__init__(     )  # message
        self.my_class    = dict

    #-------------------------
    def custom_info( self ):

        self.add_line(  "custom_info for a dict" )

        ix = 0
        for  i_key, i_value in self.inspect_me.items():

            ix += 1
            if ix > MAX_LIST_ITEMS:
                more_items   = len(self.inspect_me) - MAX_LIST_ITEMS
                self.add_line( f"{self.xin}{INDENT}and{more_items} more items.... " )
                #a_str   = f"{a_str}\n{xin}{INDENT}and {len(a_obj) - max_items} more items.... "
                break

            self.add_line( f"{self.xin}{INDENT} {i_key = } {i_value = }" )

    # --------------------------
    def have_info_forxxx( self, a_obj ):

        return isinstance(  a_obj, list  )

# -----------------------------------
class InfoAboutString( ia.InfoAboutBase  ):

    #----------- init -----------
    def __init__(self,   ):

        super( ).__init__(     )  # message
        self.my_class    = str

    #-------------------------
    def custom_info( self ):

        self.add_line(  "custom_info about a str -- nothing really custom " )
        # self.add_line(  f"{self.xin}{INDENT2}{self.inspect_me.toPlainText() = }" )
        # ix = 0
        # for  i_key, i_value in self.inspect_me.items():

        #     ix += 1
        #     if ix > MAX_LIST_ITEMS:
        #         more_items   = len(self.inspect_me) - MAX_LIST_ITEMS
        #         self.add_line( f"{self.xin}{INDENT}and{more_items} more items.... " )
        #         #a_str   = f"{a_str}\n{xin}{INDENT}and {len(a_obj) - max_items} more items.... "
        #         break

        #     self.add_line( f"{self.xin}{INDENT} {i_key = } {i_value = }" )

# -----------------------------------
class InfoAboutDatetime( ia.InfoAboutBase  ):

    #----------- init -----------
    def __init__(self,   ):

        super( ).__init__(     )
        self.my_class    = datetime

    #-------------------------
    def custom_info( self ):

        self.add_line(  "custom_info about a datetime  " )

        obj         = self.inspect_me
        self.add_line(  "custom_info about a str -- nothing really custom " )

        self.add_line(  f"{self.xin}{INDENT2}{obj.year = }     {obj.month = }      {obj.day =} " )
        self.add_line(  f"{self.xin}{INDENT2}{obj.hour = }     {obj.minute = }      {obj.second =} " )
        self.add_line(  f"{self.xin}{INDENT2}{obj.microsecond = }       " )
        self.add_line(  f"{self.xin}{INDENT2}{obj.tzname = }       " )


        # a_str   = f"{a_str}\n{INDENT2}year:        {a_obj.year}    month:   {a_obj.month}    day:     {a_obj.day}"
        # # a_str   = f"{a_str}\n{INDENT2}month:       {a_obj.month}"
        # # a_str   = f"{a_str}\n{INDENT2}day:         {a_obj.day}"
        # a_str   = f"{a_str}\n{INDENT2}hour:        {a_obj.hour}      minute:  {a_obj.minute}    second:  {a_obj.second}"
        # # a_str   = f"{a_str}\n{INDENT2}minute:      {a_obj.minute}"
        # # a_str   = f"{a_str}\n{INDENT2}second:      {a_obj.second}"
        # a_str   = f"{a_str}\n{INDENT2}microsecond: {a_obj.microsecond}"
        # a_str   = f"{a_str}\n{INDENT2}tzinfo:      {a_obj.tzname()}  "

        # self.add_line(  f"{self.xin}{INDENT2}toPlainText()            = {self.inspect_me.toPlainText() }" )

# datetime.timedelta( days = 1, minutes = 3 )
# -----------------------------------
class InfoAboutTimeDelta( ia.InfoAboutBase  ):

    #----------- init -----------
    def __init__(self,   ):

        super( ).__init__(     )  # message
        self.my_class    =  timedelta

    #-------------------------
    def custom_info( self ):
        obj         = self.inspect_me
        self.add_line(  "custom_info about a timedalta  " )

        self.add_line(  f"{self.xin}{INDENT2}{obj.days = }  {obj.seconds= }  " )
        #self.add_line(  f"{self.xin}{INDENT2}{obj.seconds }" )


        #self.add_line(  f"{self.xin}{INDENT2}toPlainText()            = {self.inspect_me.toPlainText() }" )
        # ix = 0
        # for  i_key, i_value in self.inspect_me.items():

        #     ix += 1
        #     if ix > MAX_LIST_ITEMS:
        #         more_items   = len(self.inspect_me) - MAX_LIST_ITEMS
        #         self.add_line( f"{self.xin}{INDENT}and{more_items} more items.... " )
        #         #a_str   = f"{a_str}\n{xin}{INDENT}and {len(a_obj) - max_items} more items.... "
        #         break

        #     self.add_line( f"{self.xin}{INDENT} {i_key = } {i_value = }" )

# ---- end of inspectors

# -----------------------------------
class InfoAboutxxx( ia.InfoAboutBase  ):

    #----------- init -----------
    def __init__(self,   ):

        super( ).__init__(     )  # message
        self.my_class    = str

    #-------------------------
    def custom_info( self ):
        obj         = self.inspect_me
        self.add_line(  "custom_info about a str -- nothing really custom " )

        self.add_line(  f"{self.xin}{INDENT2}{obj.xxxx() }" )

        self.add_line(  f"{self.xin}{INDENT2}toPlainText()            = {self.inspect_me.toPlainText() }" )
        # ix = 0
        # for  i_key, i_value in self.inspect_me.items():

        #     ix += 1
        #     if ix > MAX_LIST_ITEMS:
        #         more_items   = len(self.inspect_me) - MAX_LIST_ITEMS
        #         self.add_line( f"{self.xin}{INDENT}and{more_items} more items.... " )
        #         #a_str   = f"{a_str}\n{xin}{INDENT}and {len(a_obj) - max_items} more items.... "
        #         break

        #     self.add_line( f"{self.xin}{INDENT} {i_key = } {i_value = }" )

# ---- end of inspectors

# info_about              = ia.InfoAbout( )
# get                     = info_about.get_info


# list_of_inspectors      = []

# list_of_inspectors.append( InfoAboutDict() )
# list_of_inspectors.append( InfoAboutList() )
# list_of_inspectors.append( InfoAboutDatetime() )
# list_of_inspectors.append( InfoAboutTimeDelta() )

# info_about.add_inspectors( list_of_inspectors   )

# # ---- main
# # --------------------
# if __name__ == "__main__":
#     #----- for running examples


#     # inof_about.get()
#     info            = get( 10 * [ 1, 2, 3, 4] ,
#                                         msg          = "here is a list with more args",
#                                         max_len      = None,
#                                         xin          = "",
#                                         print_it     = True,
#                                         sty          = "",
#                                         include_dir  = False,  )
#     print( info )


#     info            = get( datetime( 2008, 11, 10, 17, 53, 59 )   ,
#                                         msg          = "here is a list with more args",
#                                         max_len      = None,
#                                         xin          = "",
#                                         print_it     = True,
#                                         sty          = "",
#                                         include_dir  = False,  )
#     print( info )






#     # ---- next
#     # do not construct out of context
#     # inspect_this     = QLineEdit()

#     # info            = info_about.get_info( inspect_this ,

#     #                                     msg          = "here is a list with more args",
#     #                                     max_len      = None,
#     #                                     xin          = "",
#     #                                     print_it     = True,
#     #                                     sty          = "",
#     #                                     include_dir  = False,  )


#     #print( info  )
# # --------------------
#     #call_tbl()

# ---- eof