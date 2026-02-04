# -*- coding: utf-8 -*-


# ---- tof
"""
Created on Wed Dec  1 13:01:36 2021

from stuff  clip_string_utils
do things to lists of strings, and perhaps
a few to and from strings retooled for rshlib


may expect AppGlobal.parameters and AppGlobal.logging ??

@author: russ

import string_list_utils
"""



# ---- Imports
#import pprint
#import os
import string_util

# import adjust_path


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


# # ----------------------------------------
# def redefine_constants_string( line_join = None ):
#     """
#     what it says read
#         why, no idea
#     """
#     global LINE_JOIN
#     if line_join is not None:
#         LINE_JOIN  = line_join

# ----------------------------------------
def list_remove_3_quotes_i_doubt_it( string_list ):
    """
    looks like return every other line
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

    # think slice with stride can do the seme
    for ix, i_split in enumerate( string_list ):
        if ix % 2 == 0:
            keeps.append( i_split )
    return keeps

# ----------------------------------------
def clean_string_to_list( in_text,
                          delete_tailing_spaces  = True,
                          delete_comments        = False,
                          delete_blank_lines     = False,   ):

    """
    from clip_string_utils in clipboard
    ( new_lines,   )  = clean_string_to_list( in_text,
                          delete_tailing_spaces  = True,
                          delete_comments        = False,
                          delete_blank_lines     = False,   )


    args:
    a_string                 = a_string of lines
    delete_blank_lines       = what it says  -- all spaces count as blank "  " functionally = ""
    delete_comments          = what it says  -- comment, # strip off from #,
                               may leave blank line if delete blanks not true
    delete_tailing_spaces    = what it says

    return  list of lines
    """

    lines         = in_text.splitlines()
    clean_list    = list_to_list_cleanup(  lines,
                                           delete_tailing_spaces = delete_tailing_spaces,
                                           delete_comments       = delete_comments,
                                           delete_blank_lines    = delete_blank_lines )
    return clean_list


# # ----------------------------------------
# def clean_string_to_string( in_text, *,
#                           delete_tailing_spaces  = True,
#                           delete_comments        = False,
#                           delete_blank_lines     = False,   ):
#     """
#     new_string  = clip_string_utils. clean_string_to_list( in_text,
#                           delete_tailing_spaces  = True,
#                           delete_comments        = False,
#                           delete_blank_lines     = False,   )
#     """

#     new_list      = clean_string_to_list( in_text,
#                               delete_tailing_spaces  = True,
#                               delete_comments        = False,
#                               delete_blank_lines     = False,   )

#     return "\n".join ( new_list )




# ----------------------------------------
def list_to_list_max_n_blank( lines, *, max_blank = 2  ):
    """
     make new list with a max of n blank line,
     trim trailing always
     return new list

        processing_function     = partial( string_list_utils.list_to_list_max_n_blank,  max_blank = 2 )


    """
    new_lines             = []
    consecutive_blanks    = 0
    for i_line in lines:
        i_line  = i_line.rstrip()
        if i_line == "":
            consecutive_blanks  += 1
        else:
            consecutive_blanks  = 0

        if consecutive_blanks <= max_blank:
            new_lines.append( i_line )

    return new_lines

# ----------------------------------------
def list_to_list_remove_dirt( lines, *, screen_dirt    ):
    """
     dirt_list is a list of dictts as in parameters.screen_dirt
     trim trailing always
     for i_key, i_value in a_dict.items():
     screen_dirt is a dict of old value to new value  -- why a dict
         could be itterable of itterables  butnow a dict of dicts
    """
    new_lines             = []

    for i_line in lines:
        i_line  = i_line.rstrip()
        for i_key, i_value in screen_dirt.items():
            i_line   = i_line.replace( i_key, i_value )

        new_lines.append( i_line )

    return new_lines

# ----------------------------------------
def list_to_list_cleanup( lines,  *,
                          delete_tailing_spaces  = True,
                          delete_comments        = False,
                          delete_blank_lines     = False,   ):

    """
    new_lines  = clip_string_utils.def clean_string_list_to_list(
                           lines,
                          delete_tailing_spaces  = True,
                          delete_comments        = False,
                          delete_blank_lines     = False,   )



    split string to a list, get rid of any remaining /r  and self.LINE_JOIN
    might make a comprehension if i computed a couple of functions
    speed is not so much an issue here, think about it ??
    args:
    a_string                 = a_string of lines
    delete_blank_lines       = what it says  -- all spaces count as blank "  " functionally = ""
    delete_comments          = what it says  -- comment, # strip off from #,
                               may leave blank line if delete blanks not true
    delete_tailing_spaces    = what it says

    return  ...  a_list
    """
    ix_deleted  = 0
    new_lines   = []

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

    return  new_lines


# ----------------------------------------
def clean_string_to_list_dup_delte_perhaps( in_text,
                          delete_tailing_spaces  = True,
                          delete_comments        = False,
                          delete_blank_lines     = False,   ):

    """
    new_lines  = clip_string_utils. clean_string_to_list( in_text,
                          delete_tailing_spaces  = True,
                          delete_comments        = False,
                          delete_blank_lines     = False,   )



    split string to a list, get rid of any remaining /r  and self.LINE_JOIN
    might make a comprehension if i computed a couple of functions
    speed is not so much an issue here, think about it ??
    args:
    a_string                 = a_string of lines
    delete_blank_lines       = what it says  -- all spaces count as blank "  " functionally = ""
    delete_comments          = what it says  -- comment, # strip off from #,
                               may leave blank line if delete blanks not true
    delete_tailing_spaces    = what it says

    return  ...  a_list
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

    return  new_lines




# ------------------------------------------
def list_to_string_lines( a_list ):
    """
    what it says
    put proper new line between list elements
    """
    a_string    =  LINE_JOIN.join( a_list )
    return a_string



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
    format_var    =  "{:<30}"  # !! needs to be examined


    lines  = clean_string_to_list( a_string,
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


        assign_to    = "= " + splits[1].strip()
        i_new_line   = string_util.to_columns( "",
                                            [var,    assign_to  ],
                                            format_list = [  format_var, "{:<50}" ],
                                            indent = "" )

        #i_new_line  = var + assign_to
        new_lines.append( i_new_line )

    return "\n".join( new_lines )

# ------------------------------------------
def allign_eq_signs_old(   ):
    """
    deleted look in backup if needed
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

# ---- sort and delete dups  --- mostly from clipboard cmd_processor and...

#----------------------------
def alt_line_sort( lines_in, which_line = 0, del_dups = False ):
    """

    processing_function     = partial( string_list_utils.alt_line_sort,  which_line = 0, del_dups = True   )

    to do or done
        still case sensitive
        reverse sort
        delete dups


    utility for alternate line sorts,
    all lines stripped at both ends
    assumes 2 lines, blank, if 3 consecutive lines inserts blank if
        this is done by removing all blank lines and put back one at end
    more than 2 lines removes extra

        if odd line at end will keep at end


    Args:
        lines_in     list ( like ) of strings
        which_line
                line to sort must be 0 or 1 for sort or del_dups
                = -1 just for clean up
    Return:
        revised list
    """
    if ( len( lines_in )  < 2 ):
        return lines_in

    # clean up white space often every third line but can be more or never
    # non blank lines need to appear in pairs, can have odd at end but
    # probably will be sorted oddly
    odd_at_end   = None
    lines_temp   = []
    for i_line in lines_in:
        line = i_line.strip()
        if line != "":
            lines_temp.append( line )

    odd             = True  # we are going to split into odd and even lines
    lines_odd       = []
    lines_even      = []

    for i_line in lines_temp:
        # alternate odd even  divisions seems as fast
        if odd:
            lines_odd.append( i_line )
            odd    = False
        else:
            lines_even.append( i_line )
            odd    = True

    if not odd:       # not odd = watiing foreven -- remove the extra odd
        odd_at_end  = lines_odd.pop( len( lines_odd ) - 1 )

    zipped         = zip( lines_odd, lines_even ) # Output: Zip Object. <zip at 0x4c10a30>
    if which_line == -1:
        sorted_zip = zipped
    else:
        sorted_zip     = sorted( zipped,  key=lambda i_list: i_list[ which_line ] )
    # rebuild the list
    out_list      = []
    dup_check     = "" # cannot occur
    for i_sorted in sorted_zip:
        # probably a better way to append the tuple ??
        a, b = i_sorted
        if del_dups:
            if which_line == 0:
                if a == dup_check:
                    continue
                else:
                    dup_check   = a

            elif  which_line == 1:
                if b == dup_check:
                    continue
                else:
                    dup_check   = b

        out_list.append( a )
        out_list.append( b )
        out_list.append( ""  )       # put in a blank line for readability

    if odd_at_end:
        out_list.append(  odd_at_end  )

    return out_list

# ---- consider from cmd processor

# transform_un_dent    -- something like this may be in use in CQTextEdit  --- so add
#
# transform_url_wiki
#
# transform_tab_to_space
# _transform_prefix_line  --- like line numbers or fixed bullet points
#  no blank lines --- list to max 0 blank
#
#  make lower or upper ?  cammel or other case
#
#   some of other go to string_utils
#

#
#   could have delete of consectu dups without sort but i do not think so
#
#
#


# ---- eof
