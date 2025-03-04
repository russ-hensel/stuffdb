# -*- coding: utf-8 -*-
"""
Purpose:


Example use:


"""

# ---- To do
"""
ia has gotten a bit out of control, 2 versions,
    !! move to own module,
    !! refactor to reduce reppition
    !! move test to their own module ex_helpers_test.py may be it
"""


# ---- Search
"""
Search:

    evp          evaluate code


"""
# ---- Imports

# delap some imports so that environments
# that do not include them may still run


import collections
#import pandas as pd
#import numpy as np
#import sys
#import pprint
import io
import pprint
#import Series
#import DataFrame
#import pandas as pd
import sys
import time
from collections.abc import Sequence
from datetime import datetime
from pprint import pprint as pp

#from   pandas import Series, DataFrame

# ---- end imports



DEBUGGING       = False  # in testing may be changed externally

indent_0        = "   " # used for formatting
INDENT          = "    "
INDENT2         = INDENT

MAX_REPR_LEN    = 150 #
MAX_STR_LEN     = 150 #
MAX_LIST_ITEMS  = 8

if DEBUGGING:
    pass



common_dir_items  = (
['__module__',
 '__lt__',
 '__le__',
 '__eq__',
 '__ne__',
 '__gt__',
 '__ge__',
 '__weakref__',
 '__doc__',
 '__hash__',
 '__new__',
 '__init__',
 '__dict__',
 '__repr__',
 '__str__',
 '__getattribute__',
 '__setattr__',
 '__delattr__',
 '__reduce_ex__',
 '__reduce__',
 '__subclasshook__',
 '__init_subclass__',
 '__format__',
 '__sizeof__',
 '__dir__',
 '__class__']
)

more_common_dir_items  = (
[ "__iter__", "__mod__", "__rmod__",

 "__len__", "__getitem__", "__add__", "__mul__", "__rmul__", "__contains__" ] )

common_dir_items = common_dir_items  + more_common_dir_items


# ----------- helper helpers
dispatch_dict  = {}

msg_prefix  = "\n>>>> "

#rint( "begin functions")


def default_msg( type_as_string ):

    msg   = f"{msg_prefix}for instance of  {type_as_string}"

    return msg


# ----------- helper helpers
def not_instance( msg, my_type, my_type_str, a_obj, xin  ) :
    """
    returns
        string with message

    """
    a_str   = ""
    a_str   = ( f"{xin}{a_str}{msg} object is not an instance "
                     f"of {my_type_str} but is {type(a_obj)}" )

    return a_str

# ----------- helper helper

def short_repr( a_obj, max_len = MAX_REPR_LEN ):
    """
    make a repr, shorten if too long
    read code
    consider ret of is truncated in tuple

    """
    a_str  = repr( a_obj )

    if len( a_str ) > max_len:
        a_str  = a_str[ :max_len ] + "..."

    return a_str

# -----------
def short_str( a_obj, max_len = MAX_STR_LEN ):
    """
    make a str, shorten if too long
    read code
    consider ret of is truncated in tuple

    """
    a_str  = repr( a_obj )

    if len( a_str ) > max_len:

        a_str  = a_str[ :max_len ] + "..."
    return a_str


# ---------------------
def to_columns( current_str, item_list, format_list = ( "{: <30}", "{:<30}" ), indent = "    "  ):
    """
    for __str__  probably always default format_list
    see ColunmFormatter which is supposed to be more elaborate version
    see its __str__
    ex:
        import string_util
        a_str     = string_util.to_columns( a_str, ["column_data",    f"{self.column_data}"  ] )
        a_str     = string_util.to_columns( a_str,
                                            ["column_data",    f"{self.column_data}"  ],
                                            format_list = ( "{: <30}", "{:<30}" )
    """
    #rint ( f"item_list {item_list}.............................................................. " )
    line_out  = ""
    for i_item, i_format in zip( item_list, format_list ):
        a_col  = i_format.format( i_item )
        line_out   = f"{indent}{line_out}{a_col}"
    if current_str == "":
        ret_str  = f"{line_out}"
    else:
        ret_str  = f"{current_str}\n{line_out}"
    return ret_str


# ---- Info functions --  a nice set of info about an object with optional print

# ----------------------------------------
def  ia_obj(        a_obj,
                    msg             = None,
                    *,
                    max_len         = None,
                    xin             = "",      # some sort of indent
                    print_it        = True,
                    sty             = "",
                    include_dir     = False,
                    ):
    """
    doc is out of date
    Purpose:
        returns info as a string, and may print information about objects
        sort of a pretty print +
        has some isinstance branching to get the right  display
        this branches to right function for ease of calling
        may want to add more cases for different types
    args:
        a_obj    an object to examine
        msg      msg to be printed along with the other info -- if "" suppress or default?
        print_it    = bool   True = print else just return a string
        xin         = amount of extra indentation
        sty         = style   s = standard
                                v = verbose
                                t = tiny   m = minimal
                                c = compact

    Returns:
        str or may prints output
    Example Call:
        ex_helpers.ia_obj( a_obj, msg = "ia_obj:" )
    """
    debug   = False
    a_str   = "look for missing assignment"

    ix  = -1
    for my_type, type_tuple in   dispatch_dict.items( ):
        ix  += 1

        function, type_string  = type_tuple
        print( f"debug dispatch: {ix = } {my_type = }, {type_string = }, {function = }, , ")
        if isinstance( a_obj, my_type):
            print( f"dispatch on {ix = }")
            # if debug:
            #     print( f"off to {type_string} >>>>>>>>>>" )
            a_str   = function ( a_obj,
                                    msg             = msg,
                                    max_len         = max_len,
                                    xin             = xin,      # some sort of indent
                                    print_it        = print_it,
                                    sty             = "",
                                    include_dir     = include_dir,
                        )
            break

    return a_str

# ----------------------------------------
def  ia_string_details( a_obj,  a_str, xin  ):
    """
    just the details about a string

    Args:
        a_ob (TYPE): DESCRIPTION.
        a_str (TYPE): DESCRIPTION.
         (TYPE): DESCRIPTION.

    Returns:
        a_str (TYPE): DESCRIPTION.

    a_str     = ia_string_details( a_obj, a_str )
    """
    a_srep  = short_str( a_obj )
    a_str   = f"{a_str}\n{xin}{INDENT}>{a_srep}<"
    a_str   = f"{a_str}\n{xin}{INDENT2}len(a_obj)               = {len(a_obj)}"


    return a_str

# ----------------------------------------
def  ia_plus_details(   a_obj,
                        msg                 = None,
                        *,
                        max_len             = None,
                        xin                 = "",      # some sort of indent
                        print_it            = True,
                        sty                 = "",
                        include_dir         = False,
                        my_type             ,
                        my_type_str         ,
                        details_function    = None    # will error out
                        ):
    """
    """

    if msg is None:
        msg  = default_msg( my_type_str )
    else:
        msg  = f"{msg_prefix}{msg} "

    if  isinstance(  a_obj, my_type  ):
        max_items  = MAX_LIST_ITEMS
        a_str   = ""
        a_str   = f"{xin}{a_str}for msg = {msg} object isinstance of {my_type_str}"

        a_str = details_function( a_obj,  a_str, xin  )

        if include_dir:
            a_str = f"{a_str}\n{xin} {dir_info( a_obj ) }"

    else:
        a_str   = not_instance( msg,  my_type, my_type_str,  a_obj, xin )

    if print_it:
        print( a_str )

    return a_str


# ----------------------------------------
def  ia_stringxx(a_obj,
                        msg             = None,
                        *,
                        max_len         = None,
                        xin             = "",
                        print_it        = True,
                        sty             = "",
                        include_dir     = False,
                        ):
    """
    Purpose:
        prints information about string
        see inof_about_obj
        do not iterate over it as strings are simple

    """
    my_type       =  str
    my_type_str   = "str"
    a_str         = ia_plus_details(a_obj,
                        msg                 = msg,
                        max_len             = max_len,
                        xin                 = xin,
                        print_it            = print_it,
                        sty                 = sty,
                        include_dir         = include_dir,
                        my_type             = my_type,
                        my_type_str         = my_type_str,
                        details_function    = ia_string_details
                        )
    return a_str



# ----------------------------------------
def  ia_string_old(a_obj,
                        msg             = None,
                        *,
                        max_len         = None,
                        xin             = "",      # some sort of indent
                        print_it        = True,
                        sty             = "",
                        include_dir     = False,
                        ):
    """





    Purpose:
        prints information about string
        see inof_about_obj
        do not iterate over it as strings are simple

    """
    my_type       =  str
    my_type_str   = "str"
    if msg is None:
        msg  = default_msg( my_type_str )
    else:
        msg  = f"{msg_prefix}{msg} "

    if  isinstance(  a_obj, my_type  ):
        max_items  = MAX_LIST_ITEMS

        a_str = ""


        a_srep  = short_str( a_obj )
        a_str   = f"{a_str}\n{xin}{INDENT}>{a_srep}<"


        a_str   = f"{a_str}\n{xin}{INDENT2}len(a_obj)               = {len(a_obj)}"
       # a_str   = f"{a_str}\n{xin}{INDENT2}lastError().text()       = {a_obj.lastError().text() }"

        if include_dir:
            a_str = f"{a_str}\n{xin} {dir_info( a_obj ) }"

    else:
        a_str   = not_instance( msg,  my_type, my_type_str,  a_obj, xin )

    if print_it:
        print( a_str )

    return a_str




# ----------------------------------------
def  ia_sequence(a_obj,
                        msg             = None,
                        *,
                        max_len         = None,
                        xin             = "",      # some sort of indent
                        print_it        = True,
                        sty             = "",
                        include_dir     = False,
                        ):
    """
    Purpose:
        prints information about string
        see inof_about_obj
        do not iterate over it as strings are simple

    """
    my_type       =  Sequence
    my_type_str   = "Sequence"
    if msg is None:
        msg  = default_msg( my_type_str )
    else:
        msg  = f"{msg_prefix}{msg} "

    if  isinstance(  a_obj, my_type  ):
        max_items  = MAX_LIST_ITEMS

        a_str = ""

        nl_if  = "\n"

        if msg is not None:
            a_str   = f"\n{xin}{a_str}>>>{msg}"
        nl_if   = ""
        a_srep  = short_str( a_obj )
        a_str   = f"{a_str}{nl_if}{xin}{INDENT}>{a_srep}<"

        a_str   = f"{a_str}\n{xin}{INDENT2}len(a_obj)               = {len(a_obj)}"

        # list out some items
        ix = 0
        for  i_value in a_obj:

            a_str   = f"{a_str}\n{xin}{INDENT2}{i_value}"
            ix += 1
            if ix > max_items:

                a_str   = f"{a_str}\n{xin}{INDENT}and {len(a_obj) - max_items} more items.... "

                break

        if include_dir:
            a_str = f"{a_str}\n{xin} {dir_info( a_obj ) }"

    else:
        a_str   = not_instance( msg,  my_type, my_type_str,  a_obj, xin )

    if print_it:
        print( a_str )

    return a_str


# ----------------------------------------
def  info_about_bool( a_obj, msg = "for an instance of bool:",
                        *,
                        max_len  = None,
                        xin      = "",
                        print_it = True,
                        sty      = ""  ):
    """
    Purpose:
        prints information about boolean bool
        see inof_about_obj
        keep it short since bool are so simple

    """
    if  isinstance(  a_obj,  bool ):

        a_str   = ""

        nl_if  = "\n"
        if msg is not None:
            a_str   = f"{xin}{a_str}for msg = {msg}"
        nl_if  = ""
        a_srep  = short_str( a_obj )
        a_str   = f"{a_str}{nl_if}{xin}{INDENT}>{a_srep}<"

        a_str   = f"{a_str}\n{xin}{INDENT2}type is = { str( type(a_obj) ) }"
        #a_str   = f"{a_str}\n{INDENT2}str     = {str( a_obj )}"
        # a_repr  = short_repr( a_obj )
        # a_str   = f"{a_str}\n{xin}{INDENT2}repr    = {a_repr}"

    else:
        # print( f"\nfor msg = {msg} object is not an instance "
        #                  f"of Dict but is {type(a_obj)}" )
        a_str   = ""
        a_str   = ( f"{xin}{a_str}for msg = {msg} object is not an instance "
                         f"of bool but is {type(a_obj)}" )

    # a_str   = f"{a_str}\n{INDENT}------\n"

    return a_str



# ----------------------------------------
def  info_about_obj( a_obj,
                    msg        = "for a_object:",
                    print_it   = False,
                    xin        = "",
                    max_len    = None,
                    sty        = "",
                    debug      = DEBUGGING ):
    """
    change to ia_obj above and remove

    Purpose:
        returns info as a string, and may print information about objects
        sort of a pretty print +
        has some isinstance branching to get the right  display
        this branches to right function for ease of calling
        may want to add more cases for different types
    args:
        a_obj    an object to examine
        msg      msg to be printed along with the other info -- if "" suppress or default?
        print_it    = bool   True = print else just return a string
        xin         = amount of extra indentation
        sty         = style   s = standard
                                v = verbose
                                t = tiny   m = minimal
                                c = compact

    Returns:
        str or may prints output
    Example Call:
        ex_helpers.info_about_obj( a_obj, msg = "info_about_obj:" )
    """
    a_str   = "look for missing assignment"
    #found    = True
    # if  isinstance( a_obj, list ):
    #     if debug:
    #         print( "off to info_about_list")
    #     a_str   = info_about_list( a_obj, msg )

    # !! set up a dict, det the dict is instance, then just one call
    if   isinstance(  a_obj,  str ):
        if debug:
            print( "off to info_about_string >>>>>>>>>>" )
        a_str   = info_about_string( a_obj, msg,
                         max_len  = max_len,
                         xin      = xin,
                         print_it = print_it,
                         sty      = sty )

    elif   isinstance(  a_obj,  bool ):
        if debug:
            print( "off to bool >>>>>>>>>>" )
        a_str   = info_about_bool( a_obj, msg,
                         max_len  = max_len,
                         xin      = xin,
                         print_it = print_it,
                         sty      = sty )

    elif   isinstance(  a_obj,  Sequence ):
        if debug:
            print( "off to sequence >>>>>>>>>>" )
        a_str   = info_about_sequence( a_obj, msg,
                                      max_len  = max_len,
                                      xin      = xin,
                                      print_it = print_it,
                                      sty      = sty )

    # elif isinstance( a_obj, pd.DataFrame ):
    #     if debug:
    #         print( "off to info_about_dataframe >>>>>>>>>>" )
    #     a_str   = info_about_dataframe( a_obj, msg, xin )

    elif isinstance( a_obj, datetime ):
        if debug:
            print( "off to info_about_datetime >>>>>>>>>>" )

        a_str   = info_about_datetime( a_obj, msg,
                                      max_len  = max_len,
                                      xin      = xin,
                                      print_it = print_it,
                                      sty      = sty )

    elif isinstance( a_obj, dict ):
        if debug:
            print( "off to info_about_dict >>>>>>>>>>" )
        a_str   = info_about_dict( a_obj,  msg,
                                  max_len  = max_len,
                                  xin      = xin,
                                  print_it = print_it,
                                  sty      = sty  )

    # elif isinstance( a_obj, DataFrame ):
    #     info_about_dataframe( a_obj, msg )

    # elif isinstance( a_obj, DataFrame ):
    #     info_about_dataframe( a_obj, msg )

    else:
        if debug:
            print( "default info >>>>>>>>>>" )
        a_str   = ""
        #print(  "\n!!!! info_about_obj ---- did not identify object type" )
        a_str   = f"{xin}{a_str}for msg = {msg} object x is of Type {type(a_obj)}"
        a_str   = f"{xin}{a_str}\n{INDENT}>{a_obj}<"
        a_str   = f"{xin}{a_str}\n{INDENT}type is = { str( type(a_obj) ) }"
        a_str   = f"{xin}{a_str}\n{INDENT}str     = {str( a_obj )}"
        a_str   = f"{xin}{a_str}\n{INDENT}repr    = {repr(a_obj )}"

    a_str   = f"{xin}{a_str}\n{INDENT}------\n"

    if print_it:
        #print( ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print( a_str  )

    return a_str

# ----------------------------------------
def eval_info( a_obj,   ):
    """
    Purpose:
        prints information about objects
        sort of a pretty print +
        has some isinstance branching to get the right  display
        this branches to right function for ease of calling
        may want to add more cases for different types
    args:
        a_obj    an object to examine
        msg      msg to be printed along with the other info
    Returns:
        prints output
    Example Call:
        ex_helpers.info_about_obj( a_obj, msg = "info_about_obj:" )
    """
    sub_indent  = "    "
    #found    = True
    msg         = ""
    #print( " eval_info"  )
    if  isinstance( a_obj, list ):
        info_about_list( a_obj, msg )

    # elif  isinstance( a_obj, Series ):
    #     info_about_series( a_obj, msg )

    # elif isinstance( a_obj, pd.DataFrame ):
    #     info_about_dataframe( a_obj, msg )

    elif isinstance( a_obj, datetime ):
        info_about_datetime( a_obj, msg )

    elif isinstance( a_obj, dict ):
        info_about_dict( a_obj, msg )

    # elif isinstance( a_obj, DataFrame ):
    #     info_about_dataframe( a_obj, msg )

    # elif isinstance( a_obj, DataFrame ):
    #     info_about_dataframe( a_obj, msg )

    else:
        #print(  "\n!!!! info_about_obj ---- did not identify object type" )
        #print( f"\nfor msg = {msg} object is of Type {type(a_obj)}" )
        print( f"{sub_indent}>{a_obj}<")
        print( f"{sub_indent}type is = { str( type(a_obj) ) } \n     "
               f"{sub_indent}str     = {str( a_obj )} \n     repr    = {repr(a_obj )}" )

        #print( "------\n")

# ----------------------------------------
def  info_about_string( a_obj, msg = "for an instance of string:",
                        *,
                        max_len  = None,
                        xin      = "",
                        print_it = True,
                        sty      = ""  ):
    """
    Purpose:
        prints information about string
        see inof_about_obj
        do not iterate over it as strings are simple

    """
    if  isinstance(  a_obj,  str ):
        max_items  = MAX_LIST_ITEMS
        a_str   = ""
        nl_if  = "\n"
        if msg is not None:
            a_str   = f"{xin}{a_str}for msg = {msg}"
        nl_if  = ""
        a_srep  = short_str( a_obj )
        a_str   = f"{a_str}{nl_if}{xin}{INDENT}>{a_srep}<"

        a_str   = f"{a_str}\n{xin}{INDENT2}type is = { str( type(a_obj) ) }"
        #a_str   = f"{a_str}\n{INDENT2}str     = {str( a_obj )}"
        a_repr  = short_repr( a_obj )
        a_str   = f"{a_str}\n{xin}{INDENT2}repr    = {a_repr}"

        a_str   = f"{a_str}\n{xin}{INDENT2}len     = {len(a_obj)}"
        # ix = 0
        # for  i_value in a_obj:

        #     a_str   = f"{a_str}\n{INDENT2}{i_value}"
        #     ix += 1
        #     if ix > max_items:

        #         a_str   = f"{a_str}\n{INDENT}and {len(a_obj) - max_items} more items.... "
        #         break

    else:
        # print( f"\nfor msg = {msg} object is not an instance "
        #                  f"of Dict but is {type(a_obj)}" )
        a_str   = ""
        a_str   = ( f"{xin}{a_str}for msg = {msg} object is not an instance "
                         f"of string but is {type(a_obj)}" )

    # a_str   = f"{a_str}\n{INDENT}------\n"

    return a_str

# ----------------------------------------
def  info_about_bool( a_obj, msg = "for an instance of bool:",
                        *,
                        max_len  = None,
                        xin      = "",
                        print_it = True,
                        sty      = ""  ):
    """
    Purpose:
        prints information about boolean bool
        see inof_about_obj
        keep it short since bool are so simple

    """
    if  isinstance(  a_obj,  bool ):

        a_str   = ""

        nl_if  = "\n"
        if msg is not None:
            a_str   = f"{xin}{a_str}for msg = {msg}"
        nl_if  = ""
        a_srep  = short_str( a_obj )
        a_str   = f"{a_str}{nl_if}{xin}{INDENT}>{a_srep}<"

        a_str   = f"{a_str}\n{xin}{INDENT2}type is = { str( type(a_obj) ) }"
        #a_str   = f"{a_str}\n{INDENT2}str     = {str( a_obj )}"
        # a_repr  = short_repr( a_obj )
        # a_str   = f"{a_str}\n{xin}{INDENT2}repr    = {a_repr}"

    else:
        # print( f"\nfor msg = {msg} object is not an instance "
        #                  f"of Dict but is {type(a_obj)}" )
        a_str   = ""
        a_str   = ( f"{xin}{a_str}for msg = {msg} object is not an instance "
                         f"of bool but is {type(a_obj)}" )

    # a_str   = f"{a_str}\n{INDENT}------\n"

    return a_str


# ----------------------------------------
def  info_about_sequence( a_obj, msg = "for a_sequence:",
                          *,
                          max_len  = None,
                          xin      = "",
                          print_it = True,
                          sty      = ""  ):

    """
    Purpose:
        prints information about series
        see inof_about_obj
    args:
        a_obj    an object to examine -- best an instance of series
        msg      msg to be printed along with the other info
    Returns:
        prints output
    Example Call:
        ex_helpers.info_about_series( a_obj, msg = "info_about_series:" )
    """
    if  isinstance(  a_obj,  Sequence,  ):
        max_items  = MAX_LIST_ITEMS

        a_str   = ""
        a_str   = f"{xin}{a_str}for msg = {msg} object isinstance of Sequence"
        a_srep  = short_str( a_obj )
        a_str   = f"{a_str}\n{xin}{INDENT}>{a_srep}<"

        a_str   = f"{a_str}\n{xin}{INDENT2}type is = { str( type(a_obj) ) }"
        #a_str   = f"{a_str}\n{xin}{INDENT2}str     = {str( a_obj )}"
        a_repr  = short_repr( a_obj )
        a_str   = f"{a_str}\n{xin}{INDENT2}repr    = {a_repr}"

        a_str   = f"{a_str}\n{xin}{INDENT2}len     = {len(a_obj)}"

        # list out some items
        ix = 0
        for  i_value in a_obj:

            a_str   = f"{a_str}\n{xin}{INDENT2}{i_value}"
            ix += 1
            if ix > max_items:

                a_str   = f"{a_str}\n{xin}{INDENT}and {len(a_obj) - max_items} more items.... "
                break

    else:
        # print( f"\nfor msg = {msg} object is not an instance "
        #                  f"of Dict but is {type(a_obj)}" )
        a_str   = ""
        a_str   = ( f"{a_str}for msg = {msg} object is not an instance "
                         f"of Dict but is {type(a_obj)}" )

    # a_str   = f"{a_str}\n{INDENT}------\n"

    return a_str

# # ----------------------------------------
# def  info_about_dataframe( a_obj, msg = "for a DataFrame:", indent = "", xin = "", print_it = True ):
#     """
#     Purpose:
#         another info about function -- see related functions, inof_about_....
#         read
#         broken, fix when need
#     """
#     1/0
#     sub_indent   = "    "
#     if  isinstance( a_obj, pd.DataFrame ):
#         print( f"\n{indent}msg {msg}" )
#         print( f"{indent}{sub_indent}     DataFrame: >{a_obj}<" )

#         print( f"     dataframe.values: >{a_obj.values}<" )
#     else:
#         print( f"\nfor msg = {msg} object is not an instance of DataFrame but is {type(a_obj)}" )
#     print( "------\n")

# ----------------------------------------
def  info_about_dict( a_obj, msg = "",
                      *,
                      max_len  = None,
                      xin      = "",
                      print_it = True,
                      sty      = ""  ):
    """
    Purpose:
        another info about function -- see related functions, inof_about_....
        read
    Args:
        a_obj  a_dict
        msg    a message to be printed has default

    Returns:
        prints output
    Example Call:
        ex_helpers.info_about_dict( a_obj, msg = "info_about_dict:" )

    """
    if  isinstance( a_obj, dict ):
        if max_len is None:
            max_items  = 5
        else:
            max_items = max_len

        a_str   = ""
        #print(  "\n!!!! info_about_obj ---- did not identify object type" )
        a_str   = f"{a_str}for msg = {msg} object isinstance of dict"
        a_srep  = short_str( a_obj )
        a_str   = f"{a_str}\n{INDENT}>{a_srep}<"
        a_str   = f"{a_str}\n{INDENT2}type is = { str( type(a_obj) ) }"
        # a_srep  = short_str( a_obj )
        # a_str   = f"{a_str}\n{INDENT2}str     = {str( a_obj )}"
        a_repr  = short_repr( a_obj )
        a_str   = f"{a_str}\n{INDENT2}repr    = {a_repr}"
        a_str   = f"{a_str}\n{INDENT2}len     = {len(a_obj)}"

        ix = 0
        for  key, value in a_obj.items():

            a_str   = f"{a_str}\n{INDENT2}{key}: {value}"
            ix += 1
            if ix > max_items:
                a_str   = f"{a_str}\n{INDENT}and {len(a_obj) - max_items} more items.... "
                break

    else:
        # print( f"\nfor msg = {msg} object is not an instance "
        #                  f"of Dict but is {type(a_obj)}" )
        a_str   = ""
        a_str   = ( f"{a_str}for msg = {msg} object is not an instance "
                         f"of Dict but is {type(a_obj)}" )

    # a_str   = f"{a_str}\n{INDENT}------\n"
    if print_it:
        #print( ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print( a_str  )

    return a_str

# ----------------------------------------
def info_about_list( a_obj, msg = "for a list:",
                      *,
                      max_len  = None,
                      xin      = "",
                      print_it = True,
                      sty      = ""  ):
    """
    Purpose:
        another info about function -- see related functions, inof_about_....
        read
    """
    sub_indent  = "    "
    max_items   = 5
    if  isinstance( a_obj, list ):
        if msg != "":
            print( f"\n{xin}msg: {msg}" )
        #print( f"     Dict: >{a_obj}<" )
        # print( f"\nfor msg = {msg} object is of Type {type(a_obj)}" )
        print( f">{a_obj}<")
        print( f"type is = { str( type(a_obj) ) } \n     "
               f"str     = {str( a_obj )} \n     repr    = {repr(a_obj )}" )
        print( f"{xin}{sub_indent}length of list is: {len( a_obj )}")
        print( f"{xin}{sub_indent}list --------->" )
        ix = 0
        for i_list in a_obj:
            print( f"{xin}{sub_indent}** {ix} {i_list}" )
            ix += 1
            #print( ix )
            if ix > max_items:
                print( f"\n{xin}{sub_indent}and {len(a_obj) - max_items} more items.... "  )
                break

    else:
        # print( f"\nfor msg = {msg} object is not an instance "
        #                  f"of Dict but is {type(a_obj)}" )
        a_str   = ""
        a_str   = ( f"{a_str}for msg = {msg} object is not an instance "
                         f"of Dict but is {type(a_obj)}" )
    #print( "------\n")

# ----------------------------------------
def info_about_unicode( a_obj, msg = None,
                       *,
                       max_len  = None,
                       xin      = "",
                       print_it = True,
                       sty      = ""  ):

    """
    Purpose:
        another info about function -- see related functions, inof_about_....
        read
    """
    1/0 # fix when needed
    if msg is None:
        msg = f"info about a {type( a_obj)}"

    if  isinstance( a_obj, str ):
        info_about_unicode_str( a_obj, msg   )
    elif isinstance( a_obj, bytes ):
        info_about_bytes( a_obj, msg   )

    else:
        print( f"\nfor msg = {msg} object is not unicode but is a {type(a_obj)}" )
    print( "------\n")

# ----------------------------------------
def info_about_unicode_str( a_obj, msg = "for a unicode for a str:",
                           *,
                           max_len  = None,
                           xin      = "",
                           print_it = True,
                           sty      = ""  ):
    """
    Purpose:
        another info about function -- see related functions, info_about_....
        read
    """
    1/0 # fix when needed
    if  isinstance( a_obj, str ):
        print( f"\nmsg: {msg}" )
        #print( f"     Dict: >{a_obj}<" )
        print( f"object isinstance of str of type {type(a_obj)}")
        print( f"as a string it is >{a_obj}<")

        msg     =  f"   repr is >{a_obj.__repr__()}<"
        print( msg )

        print( f"length of str is: {len( a_obj )}")
        if a_obj.isascii():
            msg = f"a_obj is ASCII = >{a_obj}<"
        else:
            msg = f"a_obj NOT ASCII >{a_obj}<"
        print( msg )
        msg     =  f"   repr is >{a_obj.__repr__()}<"
        print( msg )

    else:
        print( f"\nfor msg = {msg} object is not an instance of str but is a {type(a_obj)}" )
    print( "------\n")

# ----------------------------------------
def info_about_bytes( a_obj, msg = "for a unicode for a bytes:",
                     *,
                     max_len  = None,
                     xin      = "",
                     print_it = True,
                     sty      = ""  ):
    """
    Purpose:
        another info about function -- see related functions, inof_about_....
        read
    """
    1/0 # fix when needed
    if  isinstance( a_obj,  bytes ):
        print( f"\nmsg: {msg}" )
        #print( f"     Dict: >{a_obj}<" )
        print( f"length of bytes is: {len( a_obj )}")
        # if a_obj.isascii():
        #     msg = f"a_obj is ASCII {a_obj}"
        # else:
        #     msg = f"a_obj NOT ASCII {a_obj}"
        # print( msg )
        msg     =  f"   repr>>{a_obj.__repr__()}"
        print( msg )

        # for  i_list in a_obj:
        #      print( f"** {i_list}" )

    else:
        print( f"\nfor msg = {msg} object is not an instance of bytes but is  a {type(a_obj)}" )
    print( "------\n")

# ------------- Helper
def info_about_datetime( a_obj, msg = 'Info on a datetime',
                        *,
                        max_len  = None,
                        xin      = "",
                        print_it = True,
                        sty      = ""  ):
    """
    ex_helpers.info_about_datetime( dt_data, msg = "here be message" )
    """

    if  isinstance(  a_obj,  datetime ):
        max_items  = MAX_LIST_ITEMS

        a_str   = ""
        #print(  "\n!!!! info_about_obj ---- did not identify object type" )
        a_str   = f"{a_str}for msg = {msg} object isinstance of datetime"
        a_srep  = short_str( a_obj )
        a_str   = f"{a_str}\n{INDENT}>{a_srep}<"

        a_str   = f"{a_str}\n{INDENT2}type is = { str( type(a_obj) ) }"
        # a_str   = f"{a_str}\n{INDENT2}str     = {str( a_obj )}"
        a_repr  = short_repr( a_obj )
        a_str   = f"{a_str}\n{INDENT2}repr:        {a_repr}"

        a_str   = f"{a_str}\n{INDENT2}year:        {a_obj.year}    month:   {a_obj.month}    day:     {a_obj.day}"
        # a_str   = f"{a_str}\n{INDENT2}month:       {a_obj.month}"
        # a_str   = f"{a_str}\n{INDENT2}day:         {a_obj.day}"
        a_str   = f"{a_str}\n{INDENT2}hour:        {a_obj.hour}      minute:  {a_obj.minute}    second:  {a_obj.second}"
        # a_str   = f"{a_str}\n{INDENT2}minute:      {a_obj.minute}"
        # a_str   = f"{a_str}\n{INDENT2}second:      {a_obj.second}"
        a_str   = f"{a_str}\n{INDENT2}microsecond: {a_obj.microsecond}"
        a_str   = f"{a_str}\n{INDENT2}tzinfo:      {a_obj.tzname()}  "

    else:
        # print( f"\nfor msg = {msg} object is not an instance "
        #                  f"of Dict but is {type(a_obj)}" )
        a_str   = ""
        a_str   = ( f"{a_str}for msg = {msg} object is not an instance "
                         f"of datetime but is {type(a_obj)}" )


    # str_hr    = ("0" + str( dt_data.hour   ))[ -2 : ]   # may be number formatting that puts on missing leading 0
    # str_min   = ("0" + str( dt_data.minute ))[ -2 : ]
    # str_time_of_day    = str_hr + ":" + str_min
    #print( f"str_time_of_day   >{str_time_of_day}<")

    if print_it:
        print( a_str  )

    return a_str

# ------------- Helper
def info_about_timedelta( delta, msg = None,
                            *,
                            max_len  = None,
                            xin      = "",
                            print_it = True,
                            sty      = ""  ):
    """
    ex_helpers.info_about_timedelta( a_delta, msg = "here be message" )
    """
    if not msg:
        msg   = 'Info on a timedelta'

    print(  2*"\n" +f"delta.               {delta}" )
    print(  f"delta.min (minimum)  {delta.min }"  )
    print( "these are the only attributes related to instance, compute others")
    print(  f"delta.days           {delta.days}"  )
    print(  f"delta.seconds        {delta.seconds }"  )
    print(  f"delta.microseconds   {delta.microseconds }"  )

    print( "compute minutes/sec possibility on 2 different days" )
    minutes_delta   =  int( ( ( delta.days * 60 * 60 * 24 ) + delta.seconds ) / 60 )
    print(  f"minutes_delta   {minutes_delta}"  )

    print( "compute minutes possibility on 2 different days" )
    seconds_delta   =  int( ( ( delta.days  * 60 * 24 ) + delta.seconds )   )
    print(  f"seconds_delta   {seconds_delta}"  )

    # print(  f"60 * 60 * 24   {60 * 60 * 24}"  )

# ----------------------------------------
def str_about_dictxxx( a_obj, msg = "for a dict:", starting_indent = "" ):
    """
    Purpose:
        may be a leftover or not
    Args:
        a_obj object to be examined
        msg    message to print

    Returns:
        print output
        str
    """
    ret_str   = f"{starting_indent}{msg}"

    if  isinstance( a_obj, dict ):
        #ret_str   =  f"\nmsg {msg}" )
        #print( f"     Dict: >{a_obj}<" )
        ret_str   =  f"{ret_str}\n{starting_indent}dict list --------->"
        for key, value in a_obj.items():
            ret_str   =  f"{ret_str}\n{starting_indent}{indent_0} {key}: {value}"

        #print( f"     dataframe.values: >{a_obj.values}<" )
        # print( f"     a_series.index: >{a_series.index}<" )
    else:
        ret_str   = ( f"\n{starting_indent}for msg = {msg} object "
                     f"is not an instance of Dict but is {type(a_obj)}" )
        ret_str   = ( "{ret_str}\n{starting_indent}------\n")

    return ret_str

# --------------------- helper -------------------------
def show_timedeltaxxx( delta ):
    """
    Purpose:
        prints info about a time delta, perhaps should be an info_about_... function
        what it says, read
    Returns:
        prints output
           x
        123
    """
    print(  2*"\n" +f"delta.               {delta}" )
    print(  f"delta.min (minimum)  {delta.min }"  )
    print( "these are the only attributes related to instance, compute others")
    print(  f"delta.days           {delta.days}"  )
    print(  f"delta.seconds        {delta.seconds }"  )
    print(  f"delta.microseconds   {delta.microseconds }"  )

    print( "compute minutes/sec possibly on 2 different days" )
    minutes_delta   =  int( ( ( delta.days * 60 * 60 * 24 ) + delta.seconds ) / 60 )
    print(  f"minutes_delta   {minutes_delta}"  )

    print( "compute minutes possibly on 2 different days" )
    seconds_delta   =  int( ( ( delta.days  * 60 * 24 ) + delta.seconds )   )
    print(  f"seconds_delta   {seconds_delta}"  )

    print(  f"60 * 60 * 24   {60 * 60 * 24}"  )

# ----------------------------------------
def  dir_info( a_obj, msg = "dir info:", ):
                        # *,
                        # max_len  = None,
                        # xin      = "",
                        # print_it = True,
                        # sty      = ""  ):
    """
    Purpose:
        list out some __dir__() info as a string

        <class 'PyQt5.QtSql.QSqlError.ErrorType'>
        databaseText
        a_atter = <built-in method databaseText of QSqlError object at 0x7f84245a0350>
        driverText
        a_atter = <built-in method driverText of QSqlError object at 0x7f84245a0350>
        isValid
        a_atter = <built-in method isValid of QSqlError object at 0x7f84245a0350>

        might be nice to shorten or declutter items

    """
    #msg       = f"directory (non standard items) for object of type {type( a_obj ) = }"
    msg       = f"directory (non standard items):"
    #print( msg )

    the_dir  = a_obj.__dir__()
    reduced_dir  = [ i_dir  for   i_dir in the_dir if i_dir not in common_dir_items ]
    reduced_dir.sort()
    current_str = ""
    for i_dir in reduced_dir:

            # clean it up a bit ??
            #print( i_dir )
            a_atter     =   getattr( a_obj, i_dir, None )
            # if a_atter.startswith( "<built-in method" ):
            #     a_atter  = "method"
            # if a_atter.startswith( "<built-in method" ):
            #     a_atter  = "method"

            #print( f"{i_dir= } .... {a_atter = }", flush = True )
            # to_columns( current_str, item_list, format_list = ( "{: <30}", "{:<30}" ), indent = "    "  ):

            current_str = to_columns( current_str, [ str( i_dir ), str( a_atter) ] )

    msg   = msg + "\n" + current_str

    return msg


# order may matter, do most specific first
dispatch_dict[ str ]        = (  ia_string,    "str" )
dispatch_dict[ Sequence ]   = (  ia_sequence,  "Sequence" )



# dispatch_dict[ str ]        = (  ia_string,    "str" )



# dispatch_dict[ QSqlTableModel ] = (  q_sql_table_model,  "QSqlTableModel" )
# dispatch_dict[ QSqlQuery ]      = (  q_sql_query,        "QSqlQuery" )

# ---- tests  should be moved to


def test_dir_info( ):

    # obj   = QLineEdit()   # not well liked
    obj   = "astring"
    #obj   = QSqlTableModel()
    print( dir_info( obj ) )




def test_ia_obj( ):
    """
    need to test with all types
    """
    # obj   = QLineEdit()   # not well liked
    #a_obj   = "astring"
    a_obj   = [ "alist_0","alist_0", "alist_0" ]
    #a_obj   = QSqlTableModel()
    # print ( type( a_obj ) )
    #a_obj   = QSqlQueryModel()
    #print( class( obj ))
    #return
    #ia_string ( a_obj,

    obj_list  =  [
                    # [ "alist_0","alist_0", "alist_0" ],
                "this is a string",


           ]

    for i_obj in obj_list:
        print( "\n\n------------------------------------------------")
        ia_obj( i_obj,

            msg   = "\n\nthis is not a default message for ia_obj() ",
            max_len         = None,
            xin             = "",      # some sort of indent
            print_it        = True,
            sty             = "",
            include_dir     = False,
            )

# ---- test actually here
#test_dir_info()

# --------------------
if __name__ == "__main__":
    #----- run the full app

    pass
    # test_ia_obj()


    # print( "eof in info_about  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")


# ---- Eof =============================







