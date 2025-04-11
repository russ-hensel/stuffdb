# -*- coding: utf-8 -*-
"""
Purpose:
    part of my ( rsh ) library of reusable code
    a library module for multiple applications
    sometimes included with applications but not used
        as this make my source code management easier.


    possible additions

    str_to_list       break on th \n
                          and perhaps right strip blanks and \n
                          or just \n

    list_to_str        join using \n

    indent_str( a_str, n_spaces )         break into lines str_to_list and indnt by n spaces
    outdent_str( a_str, n_spaces )        break into lines and remove n_spaces , or characters from le4ft



"""


# ---- imports
#from pathlib import Path

URL_VALID_PREFIXS     = [ "www.", "http://", "https://" ]
    # used to help identify url's


# ----------------------------------------
def count_leading_spaces( a_string ):
    """
    helper function
    what it says, read
    return:
        count of leading spaces
        https://stackoverflow.com/questions/13648813/what-is-the-pythonic-way-to-count-the-leading-spaces-in-a-string
    space_count   = string_util.count_leading_spaces( a_string )
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

    it_is, url  = string_util.is_url( a_string )


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

# ---------------------
def to_columns( current_str, item_list, format_list = ( "{: <30}", "{:<30}" ), indent = "    "  ):
    """
    this is close to what is in string_util.py
    make a partial to avoid repeat of format list ??
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
