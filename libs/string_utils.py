#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# ---- tof
"""

may expect AppGlobal.parameters and AppGlobal.logging ??

@author: russ


import string_list_utils
"""

# ---- Imports
#import pprint
import os

# import adjust_path
import string_util

#from   app_global import AppGlobal


# ----------------------------------------
def extract_self( a_string ):
    """
    extract all the self.xxx = assignments
    this is used for things like construction of __init__ and __str__

    += and -= need to be delt with , perhaps change to "=" then extract
    return
        set of the xxx's
    ex:
        set_self   = clip_string_utils.extract_self( a_string )

    """
    # may be others but ones i use the most
    a_string      = a_string.replace( "+=", "")
    a_string      = a_string.replace( "-=", "")
    # clean up lines
    ( lines, ix_deleted )    = clean_string_to_list( a_string,
                                 delete_tailing_spaces  = True,
                                 delete_comments        = False,
                                 delete_blank_lines     = False,   )
    # remove leading space
    lines_new   = []
    for i_line in lines:
        lines_new.append( i_line.strip() )
    # print( lines )

    # starts with self
    lines       = lines_new
    lines_new   = []
    for i_line in lines:
        if  i_line.startswith( "self." ):
            lines_new.append( i_line )

    # remove self.
    lines       = lines_new
    lines_new   = []
    for i_line in lines:
          lines_new.append( i_line[ 5: ])

    # get assignments
    lines    = lines_new
    lines_new   = []
    for i_line in lines:
        # look for = must be something on both sides
        splits   = i_line.split( "=", maxsplit = 1 )
        if len( splits ) == 2 :
            lines_new.append( splits[0].strip() )

    # no dots no left paren
    lines       = lines_new
    lines_new   = []
    set_new     = set( )
    for i_line in lines:
        if "." not in i_line and "(" not in i_line:
            set_new.add( i_line )

    # lets sort ... and return as a list
    instance_list = sorted( list( set_new ) )
    return instance_list

# ----------------------------------------
def clean_string( a_string ):
    """
    clean up string into non empty parts, eliminate excess white space

    is this worth a function ?? this is a one liner
    :param self:
    :param a_string:
    :return: list of clean parts or clean string

    """
    # cmd> url  https://stackoverflow.com/questions/4302027/how-to-open-a-url-in-python
    # cmd> url  http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/
    # a_url  = r"http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/"

    #print "clean up whitespace "
    # sentence = ' hello \r\n   apple'
    # print sentence.split()
    b_string = " ".join(a_string.split())
    #  print b_string

    return b_string

# ------------------------------------------
def count_leading_spaces( a_string ):
    """
    what it says, read
    https://stackoverflow.com/questions/13648813/what-is-the-pythonic-way-to-count-the-leading-spaces-in-a-string
    """
    leading_spaces   = len( a_string ) - len( a_string.lstrip(' ') )

    return leading_spaces

# ---- is functions -------------------------------
def is_url( a_string,  ):
    """
    !! seee if moved to clip_utils


    v2->v3
    clean up the string and see if it starts with a url, return cleaned url

    is the ( cleaned up ) string a url? !!
           url must be on the first line if multiple and at first non white space
    consider typing the string get_string_type
    return tuple ( boolean, cleaned up url ( truncate at space or cr or lf ... ) )
    """
    is_url_bool                 = False

    parts       = a_string.split()
    test_url    = parts[0]
    #test_url   = (a_string.split() ).[0])  #.strip()     # parse off using whitespace  and strip

    for i_prefix in URL_VALID_PREFIXS:
        if test_url.find( i_prefix ) == 0:    # find str2 in str1
            is_url_bool = True

    if is_url_bool:
        return ( is_url_bool, test_url )
    else:
        return( is_url_bool, "" )

# ------------------------------------------
def is_filename( a_string,  ):
#def is_filename( self, a_string,  ):   is_file    file_exists  ?? not sure
    """
    !! check is moved to utils
    looks to see if file exists
    clean up a_string and see if it starts with a file name
    return flag, cleaned_up_filename
    is the  string a file name -- full path
    might at least strip the name??
    unlike is url no clean up, perhaps a different name
    consider typing the string get_string_type
    return ( < boolean >, <cleaner filename perhaps > )

    """
    #print( "a_string = " + str( a_string ) )
    parts       = a_string.split()
    test_fn     = parts[0]
    #rint( "parts = " + str( parts ) )
    #rint( "----------------------------")
    #print( "a_string = " + str( a_string ) )

    is_fn        =  os.path.isfile( test_fn )   # accepts spaces on end under windows
    #print( a_string )
    #print( " in is_filename  " + str( is_fn ) )

    return is_fn, test_fn


# ------------------------------
def print_uni( a_string_ish ):
    """
    print even if unicode char messes it con
    maybe doing as a call is over kill
    """
    print(  a_string_ish.encode( 'ascii', 'ignore') )


# ------------------------------------------
def eval_transform( a_string ):
    """
    eval a string to special characters
    !! add exception processing
    may not be used .... delted
    not sure about print( joe ) an error, deliberate
    """
    print( joe )
    b_string    = eval( a_string,  locals(),  globals() )
    print( f">{a_string}<  >>>>  >{b_string}<")
    return b_string

# ----------------------------------------
def eval_f_string( a_fstring ):
    """
    conditional conversion to an fstring begins with single or double quote
    return
        tuple
        if a_fstring is fsting its eval, else unchanged
        else result of eval
       ( no_exception, ret_string )
    """
    no_exception   = True
    ret_string     = a_fstring
    if a_fstring.startswith( 'f"') or a_fstring.startswith( "f'" ):
        #int( f"clip_string_utils eval_f_string yes yes yes >>{a_fstring})
        #print( locals( ) )
        # print( globals() )
        #snippet  = snippet[ 4:]
        try:
            ret_string  = eval( a_fstring, globals(), locals(),  )
        except Exception as a_except:
            no_exception   = False
            ret_string  = "eval_f_string () unfortunately snippet caused exception"
            # change to loggiong or somethin else better
            print( type(a_except)  )   # the exception instance
            print( "a_except.args = {a_except.args}"  )   # arguments stored in .args
            print( a_except     )      # __str__ allows args to printed directlyeval_f_string

    return ( no_exception, ret_string )

# ------------------------------------------
def string_to_py_list( a_string ):
    """
    Purpose:
        take a multiline string and turn it into a python
        list of strings
        usual clean up of lines
        make multiline if long
        left trim lines for leading spaces

    Notes:
        what if stuff already includes quotes.... tough
        returns a string of python code

    """
    string_list, __     = clean_string_to_list( a_string )

    a_list              = []  # return as list or back to string

    len_max             = 0
    tot_len             = 0

    for i_string in string_list:
        print( i_string )
        i_string  = i_string.lstrip()
        i_len      = len( i_string )
        tot_len   += i_len                    # ?? place for wallrus
        if i_len > len_max:
            len_max  = i_len

        a_list.append( f'"{i_string}"' )

        # ret.append( "======>" + i_string )
    if tot_len > 100:
        a_string   = ", \n".join( a_list )
    else:
        a_string   = ", ".join( a_list )

    a_string   = f"[ {a_string} ]"

    # if False: # debug
    #     print( f"i_string =           {i_string}")
    #     print( f"    leading_spaces       {i_leading_spaces}")
    #     print( f"    first_eq             {ix_first_eq}")
    #     print( f"    ix_first_pound_sign, {ix_first_pound_sign}")


    return a_string

# ---- eof


