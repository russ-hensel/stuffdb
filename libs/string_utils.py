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
#import string_util

#from   app_global import AppGlobal

URL_VALID_PREFIXS     = [ "www.", "http://", "https://" ]


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
def begins_with_url( a_string, ):
    """
    it_is  = string_util.begins_with_url( a_string )
    """
    parts       = a_string.split()
    if len( parts ) == 0: # pretty much null string
        return False
    test_url    = parts[0]
    #test_url   = (a_string.split() ).[0])  #.strip()     # parse off using whitespace  and strip

    for i_prefix in URL_VALID_PREFIXS:
        if test_url.find( i_prefix ) == 0:    # find str2 in str1 !! better bings with
            return  True

    return False


# ---- is functions -------------------------------
def begins_with_file_name( a_string, ):
    """
    it_is  = string_utils.begins_with_url( a_string )
    """
    parts       = a_string.split()
    if len( parts ) == 0: # pretty much null string
        return False
    test_file_name    = parts[0]
    #test_url   = (a_string.split() ).[0])  #.strip()     # parse off using whitespace  and strip

    if test_file_name.startswith( "/") or test_file_name.startswith( "~/"):
        if "." in test_file_name:
            return  True

    return False



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



# -----------------------------------------
class ColumnFormater( ):

    """
    a_file_deleter    = FileDeleter( )
    a_file_deleter.do_delete_empty( a_path )

    what_deleted     = a_file_deleter.delete_list

    ?? consider adding an output print function to display the progress

    """
    def __init__(self,   ):
        """
        what it says, read

        """
        ...
        self.reset( None )

    # ----------------------------------------
    def reset( self, a_path ):
        """
        reset for reuse


        """
        self.column_data   = []  # fill with tuples of the column data
        self.column_specs  = []  # list of dicts as below in column order

        # a_spcec       =  { "width": 5,
        #                    "allign": "r",   # "l"
        #                     }

    # ----------------------------------------
    def get_default_spec(  self ):
        a_default_spec  =  { "width": 5,
                            "allign": "r",   # "l"
                             }
        return a_default_spec


    # ----------------------------------------
    def add_line( self, column_tuple  ):
        """
        what it says, read

        """
        pass
        self.column_data.append( column_tuple )
        # Could check length against column specs

    # ----------------------------------------
    def add_column( self, column_spec ):
        """
        what it says, read

        """
        self.column_specs.append( column_spec )


    # ----------------------------------------
    def get_str( self,  ):
        """

        """

        a_str   = ""

        for i_line in self.column_data:
            a_str   = f"{a_str}\n"
            for ix_col, i_col_data in enumerate( i_line ):
                a_line  = ( i_col_data + "          " )[ 0: self.column_specs[ ix_col ]["width"] ]

        a_str   = f"{a_str} {a_line}"

            #for i_column_spec in self.column_specs
        return a_str

    #------------------
    def __str__( self, ):
        """
        Purpose:
           see title, what it says, read, for debug
        Return:
           a string of info about object
        Raises:
           none planned

        """
        newline  = "\n" + " " * 4
        a_str    = ""
        a_str    = f"{a_str}>>>>>>>>>>* ColumnFormatter (some values) *<<<<<<<<<<<<"
        #a_str    = ( f"{a_str}\n{self.__class__.__name__}: name = {self.name}" )
        # a_str    = f"super().__str__()"

        a_str    = f"{a_str}{newline}column_specs                {self.column_specs}"
        a_str    = f"{a_str}{newline}column_data                 {self.column_data}"

        # convert to
        a_str   = to_columns( a_str, ["column_specs",        f"{self.column_specs}" ] )
        a_str   = to_columns( a_str, ["column_data",         f"{self.column_data}"  ] )



        # a_str    = f"{a_str}{newline}computer_id         {self.running_on.computer_id}"
        # a_str    = f"{a_str}{newline}logger_id           {self.logger_id}"

        return a_str

def num_to_string( an_int ):
    """
    string_util.num_to_string( an_int )
    """
    test_val   =  1_000_000_000
    if an_int > test_val:
        an_int = an_int/test_val
        text   = f"{an_int:.3f} Giga"
        return text

    test_val   =  1_000_000
    if an_int > test_val:
        an_int = an_int/test_val
        text   = f"{an_int:.3f} Mega"
        return text

    test_val   =  1_000
    if an_int > test_val:
        an_int = an_int/test_val
        text   = f"{an_int:.3f} Kilo"
        return text

    test_val   =  1
    if an_int > test_val:
        an_int = an_int/test_val
        text   = f"{an_int:.3f} "
        return text

    test_val   =  .001
    if an_int > test_val:
        an_int = an_int / test_val
        text   = f"{an_int:.3f} mili"
        return text

    test_val   =  .000001
    if an_int > test_val:
        an_int = an_int/test_val
        text   = f"{an_int:.3f} micro"
        return text

    text   = str( an_int )
    return text

#---------------------------
def test_num_to_string():
    """


    """
    an_int  = 36.53
    print( f"{an_int} -> {num_to_string(an_int)}")

    an_int  = an_int/10
    print( f"{an_int} -> {num_to_string(an_int)}")

    an_int  = an_int/10
    print( f"{an_int} -> {num_to_string(an_int)}")

    an_int  = an_int/10
    print( f"{an_int} -> {num_to_string(an_int)}")

    an_int  = an_int/10
    print( f"{an_int} -> {num_to_string(an_int)}")

    an_int  = an_int/10
    print( f"{an_int} -> {num_to_string(an_int)}")

    # print( "---------------------")
    # an_int  = 3.53 *   1_000_000_000
    # print( f"{num_to_string(an_int)}")

    # an_int  = 36.53 *   1_000_000_000
    # print( f"{num_to_string(an_int)}")

    # an_int  = 36.53
    # print( f"{num_to_string(an_int)}")

    # an_int  = 36.53  *   1_000
    # print( f"{num_to_string(an_int)}")

    # an_int  = .3653
    # print( f"{num_to_string(an_int)}")

    # an_int  = 3.653/1_000
    # print( f"{an_int} -> {num_to_string(an_int)}")

def test_column_formatter():
    """


    """
    a_column_formatter   = ColumnFormater()

    column_spec          = a_column_formatter.get_default_spec()
    a_column_formatter.add_column( column_spec )
    a_column_formatter.add_column( column_spec )

    a_line               = "name",   "john"
    a_column_formatter.add_line( a_line )
    a_line               = "name",   "sueellenjone"
    a_column_formatter.add_line( a_line )
    a_line               = "nm",   "johnthan"
    a_column_formatter.add_line( a_line )

    print( a_column_formatter )
    print( a_column_formatter.get_str() )


#test_column_formatter()
# --------------------
if __name__ == "__main__":
   test_num_to_string()
# --------------------




# ---- eof

# ---- eof


