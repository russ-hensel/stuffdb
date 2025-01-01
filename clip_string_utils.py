# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 13:01:36 2021

import clip_string_utils

@author: russ

make singleton class, or module, lets try module
but give access to an instance of parameters


See Also:
    git hub, do search
    hettinger ex may still have some left
    ex_string.py
    python cookbook


Naming:
    transform       return tuple
    is              return boolean

import clip_string_utils
"""


# ---- Main --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    main.main()

# ---- Imports
#import pprint
import os

import string_util

#from   app_global import AppGlobal

# parameters injection  should only be on in testing -- but need for now
# !! this is bad think may have circular imports or smething
# import parameters
# parameters      = parameters.Parameters()


# next debug
#rint( parameters )
#rint( AppGlobal.parameters )
print( "clip_string_utils fix AppGlobal Ref" )
LINE_JOIN             = "\n"  # AppGlobal.parameters.line_join
    #  something like "\r\n"  use to join lines

URL_VALID_PREFIXS     = [ "www.", "http://", "https://" ]
    # used to help identify url's

NAME_TO_LITERAL_DICT  = { "newline": "\\n",
                          "tab":     "\t",
                          "nothing":  "",
                        }
    # use in gui for hard totype and see strings -- see function

# ---- for f_string eval
TAB         = "\t"
NEWLINE     = "\n"
CRLF        = "\r\n"
SPACE       = " "
TEST_STR    = ">>>>test<<<<"
NULL_STR    = ""







# ----------------------------------------
def redefine_constants_string( line_join = None ):
    """
    what it says read
        why, no idea
    """
    global LINE_JOIN
    if line_join is not None:
        LINE_JOIN  = line_join

# ----------------------------------------
def remove_3_quotes( a_string ):
    """
    purpose:
        remove tripple quoted parts of string
        must be there in pairs
    approach  -- scan first keeping, second deleting
    approach  -- split on
                 keep the even parts   0  not 1   2 yes

                 join  back then to list
    return
         list of string less the triple quoted parts
         why do I not rejoin here !! ??

    """
    keeps      = []
    splits     = a_string.split( '"""' )
    # think slice with stride can do the seme
    for ix, i_split in enumerate( splits ):
        if ix % 2 == 0:
            keeps.append( i_split )
    return keeps

# ----------------------------------------
def extract_self( a_string ):
    """
    extract all the self.xxx = assignments

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

# ----------------------------------------
def clean_string_to_list( in_text,
                          delete_tailing_spaces  = True,
                          delete_comments        = False,
                          delete_blank_lines     = False,   ):
    #def clean_string( a_string ):
    """
    ( new_lines, ix_deleted )  = clean_string_to_list( in_text,
                          delete_tailing_spaces  = True,
                          delete_comments        = False,
                          delete_blank_lines     = False,   )



    !! needs better description



    split string to a list, get rid of any remaining /r  and self.LINE_JOIN
    might make a comprehension if i computed a couple of functions
    speed is not so much an issue here, think about it ??
    args:
    a_string                 = a_string of lines
    delete_blank_lines       = what it says  -- all spaces count as blank "  " functionally = ""
    delete_comments          = what it says  -- comment, # strip off from #,
                               may leave blank line if delete blanks not true
    delete_tailing_spaces    = what it says

    return  ... beware a tuple of ( a_list, a_int ) int is count of stuff deleted ?? refactor out
    """
    ix_deleted  = 0
    new_lines   = []

    lines   = in_text.splitlines()
    for i_line in lines:
        # clean_line        = i_line.strip( "\r" ) no longer needed
        if delete_comments:
            ix            = i_line.find( "#")
            if ix != -1:
                i_line            = i_line[  : ix ]
                clean_line_strip  = i_line.rstrip(  )

                if clean_line_strip == "":
                    ix_deleted   += 1
                    continue

        clean_line_strip  = i_line.rstrip(  )

        if( clean_line_strip == "" ) and ( delete_blank_lines ):
            ix_deleted   += 1
        else:
            if delete_tailing_spaces:
                new_lines.append( clean_line_strip )
            else:
                new_lines.append( i_line )

    return ( new_lines, ix_deleted )


# ------------------------------------------
def eval_transform( a_string ):
    """
    eval a string to special characters
    !! add exception processing
    may not be used .... delted
    not sure about print( joe ) an error , deliberate
    """
    print( joe )
    b_string    = eval( a_string,  locals(),  globals() )
    print( f">{a_string}<  >>>>  >{b_string}<")
    return b_string

# ------------------------------------------
def count_leading_spaces( a_string ):
    """
    what it says, read
    https://stackoverflow.com/questions/13648813/what-is-the-pythonic-way-to-count-the-leading-spaces-in-a-string
    """
    leading_spaces   = len( a_string ) - len( a_string.lstrip(' ') )

    return leading_spaces

# ------------------------------------------
def list_to_string_lines( a_list ):
    """
    what it says
    put proper new line between list elements
    """
    a_string    =  LINE_JOIN.join( a_list )
    return a_string

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

# ------------------------------------------
def allign_eq_signs( a_string ):
    """
    Purpose:
        alligns = signs, using first line as a template
        preserves comments
        ignores blank lines and all comment lines
        trims trailing blanks

    Notes:

        must have an exposed = sign on first line
        allign stops if change in indent
                     no = sign found on a line -- unless blank or comment



    ?? probably want to skip blank lines ... may not allow as first
    inconsistent use of i and ix

    !! need to add += ......


    returns a list, not a sting, join with list_to_string_lines( a_list ) if you want a string

            abc         = def   # comment

    change to indicate success ?
    i_format  = "{: <30}"
    a_col  = i_format.format( i_item )

    find_eq

    """

    ( lines, ix_deleted )  = clean_string_to_list( a_string,
                          delete_tailing_spaces  = True,
                          delete_comments        = False,
                          delete_blank_lines     = False,   )
    space_count  = None
    new_lines    = []
    for i_line in lines:
        if space_count is None:
            space_count   = string_util.count_leading_spaces( i_line )
            find_eq       = i_line.find( "=",   )
            if find_eq == 0:
                return a_string
            #format_var    =  '{:<'  + str( find_eq - space_count ) + '}'
            format_var    =  '{:<'  + str( find_eq     ) + '}'
        splits        = i_line.split( "=" )
        if len( splits)  < 2:
            # no =
            i_new_line   = i_line
            new_lines.append( i_new_line )
            continue

        var          = ( space_count * " " ) + splits[0].strip()
        #format_var    =  '"{: <' 30}"

        assign_to    = "= " + splits[1].strip()
        i_new_line   = string_util.to_columns( "",
                                            [var,    assign_to  ],
                                            format_list = [  format_var, "{:<50}" ],
                                            indent = "" )

        #i_new_line  = var + assign_to
        new_lines.append( i_new_line )

    return "\n".join( new_lines )


# ------------------------------------------
def allign_eq_signs_old( a_string ):
    """
    Purpose:
        alligns = signs, using first line as a template
        preserves comments
        ignores blank lines and all comment lines
        trims trailing blanks

    Notes:

        must have an exposed = sign on first line
        allign stops if change in indent
                     no = sign found on a line -- unless blank or comment



    ?? probably want to skip blank lines ... may not allow as first
    inconsistent use of i and ix

    !! need to add += ......


    returns a list, not a sting, join with list_to_string_lines( a_list ) if you want a string
    """
    string_list, __    = clean_string_to_list( a_string )


    ix_eq_0              = True
    ret                  = []  # return as list or back to string
    stop_allign          = False
    left_hand_length     = None

    for i_string in string_list:
        #rint( i_string )

        if stop_allign:  # look for another below
            ret.append( i_string )
            continue

        i_leading_spaces     = count_leading_spaces( i_string )
        ix_first_eq          = i_string.find( "=" )
        ix_first_pound_sign  = i_string.find( "#" )

        # see if all blank or all comment
        test    = i_string.strip()
        if test == "":
            print( "blank line" )
            ret.append( i_string )
            continue








        # else:
        #     #rint( "non blank" )

        if i_leading_spaces == ix_first_pound_sign:
            print( "comment line" )
            ret.append( i_string )
            continue
        # else:
        #     #rint("not comment")
        #     pass

        if ix_eq_0: # first time through the loop
            #leading_spaces   = i_leading_spaces
            ix_eq_0          = False
            #if leading_spaces

        if ix_first_eq == -1:
            stop_allign   = True

        if ( ix_first_pound_sign > 0 ) and ( ix_first_pound_sign < ix_first_eq  ):
            stop_allign   = True

        if stop_allign: # only on first time thru
            ret.append( i_string )
            continue

        left_side, right_side  = i_string.split( "=", 1 )   # this should always give len of 2

        # now the first time thru we need to get the length of the
        # part to the left of the =
        if left_hand_length is None:
            left_hand_length   = len( left_side )

        else:  # not first time thru, pad out the
            pass

        # f_expression   = f"'{splits[0]}':<{left_hand_length}"
        # f_expression   = f"'{splits[0]}':<{left_hand_length}"
        # f_expression   = f"'{splits[0]}':<19"
        #fm            = "<50"
        #print( "fexpression", f_expression )
        #new_str     = f"{f_expression} = {splits[1]}"
        #new_str     = f"{splits[0]:<50} = {splits[1]}"
        #breakpoint()
        left_side   = left_side.rstrip( )
        new_str     = left_side.ljust( left_hand_length , ' ' )
        right_side  = right_side.strip()
        new_str     = f"{new_str} = {right_side}"
        #new_str     = f"{splits[0]:fm} = {splits[1]}"

        ret.append( new_str )

        # print( f"splits {splits} {len(splits)}")
        # ret.append( "======>" + i_string )


        if False: # debug
            print( f"i_string =           {i_string}")
            print( f"    leading_spaces       {i_leading_spaces}")
            print( f"    first_eq             {ix_first_eq}")
            print( f"    ix_first_pound_sign, {ix_first_pound_sign}")

    return ret

# ------------------------------
def print_uni( a_string_ish ):
    """
    print even if unicode char messes it con
    maybe doing as a call is over kill
    """
    print(  a_string_ish.encode( 'ascii', 'ignore') )


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



# =================== eof ================
