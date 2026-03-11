# -*- coding: utf-8 -*-


"""
this is badly out of date ......

this writes files from memory, -- a dictionary  these files are the
same format as the basic data files, but cleaned up
more or less a rewrite.

clean up:
    are comments preserved?? -- not now
    is it sorted yes
    blank space is reduced  yes -- a blank line after each data item

tag files are "reduced" versions used to generate tag conversion lists
and define databases

running these off of some sort of file info, should it be a row thing
or just an info thing??

code may be related to
       display_txt  from easy db, greatly changed

"""

# put this at top of each app file:
# ------------------------------------------
if __name__ == "__main__":
    import main
    main.main()


# ---- Imports


import HTML
import string_utils as string_util

# ------------ local
from   app_global import AppGlobal
import app_exceptions


#====================================
class FileWriter(  ):
    """
    Writes out a file, all cleaned up
    not for query, but general purpose
    same format as normal input files
    possibly output multiple files
    """

    #  ----------- init -----------
    def __init__( self,     ):       #FileReader

        # AppGlobal.print_debug( f"FileWriter for {file_name_to_write}",  )

        # msg = f"FileWriter() for {file_name_to_write}"
        # AppGlobal.print_debug( msg,   )

        # self.file_data           = {}        #
        self.fileout              = None      # populated later by open_file
        self.file_data            = None      # for now save for debug
            # what format is this a section data or a file_reader all data
            # file_reader.full_data
        #self.header_read_status  = "0"       # 0   no attempt to read, see code for others
        #self.record_break        = ":===="   # may be shorter than the one written for safety

        # # these will be used by get_next_line as state full mutating return
        # self.ix_line             = 0       # use for error report
        # self.i_line              = None    # use for error report line buffering


    #  -----------
    def __str__( self, ):
        """
        return string of data, particularly useful for test and debug

        """
        a_str        = "__str__ for FileWriter"
        string_util.to_columns( a_str, [ "file_name_to_write",
                                        f"{self.file_name_to_write}"  ] )
        string_util.to_columns( a_str, [ "file_data",
                                        f"{self.file_data}"  ] )

        return a_str

    #  -----------
    def open_file( self,  file_name_to_write  ):
        """
        open the file, but called from init, generally you should not need to call elsewhere
        Return:  internal but you can check .filein ==  None for failure
        xxxRaises:  DBOjectException( msg )  ?? this nea

        """
        self.file_name_to_write       = file_name_to_write

        try:
            self.fileout         = open( self.file_name_to_write, "w",
                                         encoding = "utf8",
                                         errors = 'ignore' )
                  #"r"  )   "r+" read write open at beginning

        except:
            #filein.close() if error this is undefined

            msg = ( f"FileWriter.open_file for {self.fileoutn} "
                   "failed, how about improve error handling? ")
            AppGlobal.print_debug( msg,  )
            AppGlobal.gui.write_gui( msg )
            self.fileout         = None
            # raise db_objects.DBOjectException( msg )
            #1/0 # cheap exception
            raise

        # self.ix_line            = 0        # for error report and .......

    #  -----------
    def close_file( self,     ):       #FileReader
        """
        read it
        """
        try:
            self.fileout.close()

        except:
            msg = ( f"FileWriter.close_file for {self.file_name_to_write}"
                  " failed, how about improve error handling" )
            AppGlobal.print_debug( msg,   )

            self.fileout         = None

    #  -----------
    def write_tag_file( self,  file_name, file_data   ):
        """
        only write out the tags in the file_data

        """
        self.file_data  = file_data    # save for debug
        self.open_file( file_name )
        for  data_type, data_list in file_data.items():
            print( f"write_file writing ->>>> {data_type}: {data_list}\n" )   # may want nl configurable
            self.write_item(  data_type, [""] )

        self.close_file()

    #  -----------
    def write_file( self,  file_name, file_data_dict   ):
        """
        args:
            file_name
            file_data      is a ....reader.file_data_dict
            think file_data_dict is a section or the data part of a section
            or does it come from the db??
        """
        self.file_data_dict  = file_data_dict    # save for debug
        self.open_file( file_name )
        for  data_type, data_list in file_data_dict.items():
            #rint( f"write_file writing ->>>> {data_type}: {data_list}" )
            self.write_item(  data_type, data_list )

        self.close_file()

    #  -----------
    def write_blank_file( self,  file_name, file_data_dict   ):
        """
        sees to be same as write_tag_file ??
        args:
            file_name
            file_data      is a ....reader.file_data_dict
            or is it a Section.data_dict    in any case {tag: list_of_line_for_tag }
        """
        self.file_data_dict  = file_data_dict    # save for debug
        self.open_file( file_name )
        for  data_type, data_list in file_data_dict.items():
            #rint( f"write_file writing ->>>> {data_type}: {data_list}" )
            self.write_blank_item(  data_type, )    # looks like just could set data list to ""

        self.close_file()

    #  -----------
    def write_item( self,  data_type, data_list   ):
        """
        write a single line, data list has no \n ( dec22 )
        """
        #sg     = f"in write_item data_type = {data_type}, list = {data_list}"
        #rint( msg )
        if len( data_list ) == 0:
            line  = f"{data_type}:\n"
        else:
            line    = f"{data_type}:{data_list[0]}\n"

        self.fileout.write( line )
        for line in data_list[1:]:
            self.fileout.write( f"{line}\n" )
        self.fileout.write( "\n" )

    #  -----------
    def write_blank_item( self,  data_type,     ):
        """
        write a single line, no data
        """
        line    = f"{data_type}: "
        self.fileout.write( line )
        # for line in data_list[1:]:
        #     self.fileout.write( f"{line}" )
        self.fileout.write( "\n" )


#====================================
class FileWriter_old(  ):
    """
    Writes out a file, all cleaned up
    not for query, but general purpose
    same format as normal input files
    possibly output multiple files
    saving because I may be missing what this was for
    2024 mar 4
    """

    #  ----------- init -----------
    def __init__( self,     ):       #FileReader

        # AppGlobal.print_debug( f"FileWriter for {file_name_to_write}",  )

        # msg = f"FileWriter() for {file_name_to_write}"
        # AppGlobal.print_debug( msg,   )


        self.fileout              = None      # populated later by open_file
        self.file_data            = None      # for now save for debug
            # what format is this a section data or a file_reader all data
            # file_reader.full_data
        #self.header_read_status  = "0"       # 0   no attempt to read, see code for others
        #self.record_break        = ":===="   # may be shorter than the one written for safety

        # # these will be used by get_next_line as state full mutating return
        # self.ix_line             = 0       # use for error report
        # self.i_line              = None    # use for error report line buffering

    #  -----------
    def get_info_str( self, ):
        """
        return string of data, particularly useful for test and debug

        """
        a_string  = "Info on FileWriter"
        a_string  = f"{a_string}\n    self.file_name_to_write         >{self.file_name_to_write}<"
        a_string  = f"{a_string}\n    self.self.file_data             >{self.self.file_data}<"
        # a_string  = f"{a_string}\n    self.line_data_type  >{self.line_data_type}<"

        return a_string

    #  -----------
    def __str__( self, ):
        """
        return string of data, particularly useful for test and debug

        """
        a_str        = "__str__ for FileWriter"
        string_util.to_columns( a_str, [ "file_name_to_write",
                                        f"{self.file_name_to_write}"  ] )
        string_util.to_columns( a_str, ["file_data",
                                       f"{self.file_data}"  ] )

        return a_str

    #  -----------
    def open_file( self,  file_name_to_write  ):
        """
        open the file, but called from init, generally you should not need to call elsewhere
        Return:  internal but you can check .filein ==  None for failure
        xxxRaises:  DBOjectException( msg )  ?? this nea

        """
        self.file_name_to_write       = file_name_to_write

        try:
            self.fileout         = open( self.file_name_to_write, "w",
                                         encoding = "utf8",
                                         errors = 'ignore' )
        except:
            #filein.close() if error this is undefined

            msg = f"FileWriter.open_file for {self.fileoutn} failed, how about improve error handling"
            AppGlobal.print_debug( msg,  )
            AppGlobal.gui.write_gui( msg )
            self.fileout         = None
            # raise db_objects.DBOjectException( msg )
            #1/0 # cheap exception
            raise

        # self.ix_line            = 0        # for error report and .......

    #  -----------
    def close_file( self,     ):       #FileReader
        """
        read it
        """
        try:
            self.fileout.close()

        except:
            msg = ( f"FileWriter.close_file for "
                 "{self.file_name_to_write} failed, how about improve error handling?" )
            AppGlobal.print_debug( msg,   )

            self.fileout         = None

    #  -----------
    def write_tag_file( self,  file_name, file_data   ):
        """
        only write out the tags in the file_data

        """
        self.file_data  = file_data    # save for debug
        self.open_file( file_name )
        for  data_type, data_list in file_data.items():
            print( f"write_file writing ->>>> {data_type}: {data_list}\n" )   # may want nl configurable
            self.write_item(  data_type, [""] )

        self.close_file()

    #  -----------
    def write_file( self,  file_name, file_data_dict   ):
        """
        args:
            file_name
            file_data      is a ....reader.file_data_dict
            think file_data_dict is a section or the data part of a section
            or does it come from the db??
        """
        self.file_data_dict  = file_data_dict    # save for debug
        self.open_file( file_name )
        for  data_type, data_list in file_data_dict.items():
            #rint( f"write_file writing ->>>> {data_type}: {data_list}" )
            self.write_item(  data_type, data_list )

        self.close_file()

    #  -----------
    def write_blank_file( self,  file_name, file_data_dict   ):
        """
        args:
            file_name
            file_data      is a ....reader.file_data_dict
        """
        self.file_data_dict  = file_data_dict    # save for debug
        self.open_file( file_name )
        for  data_type, data_list in file_data_dict.items():
            #rint( f"write_file writing ->>>> {data_type}: {data_list}" )
            self.write_blank_item(  data_type, )    # looks like just could set data list to ""

        self.close_file()

    #  -----------
    def write_item( self,  data_type, data_list   ):
        """
        write a single line, data list has no \n ( dec22 )
        """
        #sg     = f"in write_item data_type = {data_type}, list = {data_list}"
        #rint( msg )
        if len( data_list ) == 0:
            line  = f"{data_type}:\n"
        else:
            line    = f"{data_type}:{data_list[0]}\n"

        self.fileout.write( line )
        for line in data_list[1:]:
            self.fileout.write( f"{line}\n" )
        self.fileout.write( "\n" )

    #  -----------
    def write_blank_item( self,  data_type,     ):
        """
        write a single line, no data
        """
        line    = f"{data_type}: "
        self.fileout.write( line )
        # for line in data_list[1:]:
        #     self.fileout.write( f"{line}" )
        self.fileout.write( "\n" )


#====================================
class SelectHTMLWriter(   ):
    """
    from easy_db.py file_writes, in process
    HTML.py - a Python module to easily generate HTML tables and lists | Decalage
        *>url  https://www.decalage.info/python/html
    ?? first implementation lots of room for improve  !! right now seems not to work at all
    !! add paging option
    ?? use tuple to reduce mem use
    """
    #----------- init -----------
    def __init__(self, fileout_name ):
        """
        see class doc
        """

        # !! not sure we will use
        self.file_name       = fileout_name
        self.table_info      = None

        self.html_table      = None   # create in write header
        # more def in other functions
        self.fileout         = None   # create in write header  why not here

    #----------- init -----------
    def write_header( self, table_info ):  # all of row object or just some part or something else
        """
        Purpose: see title
        Args: Return: state change, output
        Raises: none planned
        """
        self.table_info             = table_info # perhaps use later, or put in init
        lines                       = []

        self.col_names              = [ i_format[0] for i_format in table_info.format_list ]
        self.html_table             = HTML.Table( header_row = self.col_names )

        msg   = f"write_header()  self.col_names  {self.col_names}"
        AppGlobal.print_debug( msg )

        self.fileout                = open( self.file_name, "w",
                                           encoding = "utf8",
                                           errors = 'replace' )

        #<h1>Bob fell over the chicken. [H1]</h1>
        i_line    = ( "<h2>SelectHTMLWriter output from "
                     f"{AppGlobal.controller.app_name} "
                     f"{AppGlobal.controller.version}</h2>" )
        self.fileout.write( i_line )

        i_line    = f"<h3>SQL used was = {self.table_info.sql}</h3>"
        self.fileout.write( i_line  )

#        lines.append( i_line  )
#        lines.append( f" self.table_info.sql = {self.table_info.sql}"  )
#
#        msg       = "\n".join( lines )
#        AppGlobal.logger.log( AppGlobal.force_log_level, msg )

    #----------------------
    def write_row( self, row_object ):
        """
        Purpose: see title
        Args: Return: state change, output
        Raises: none planned
        for now just accumulate, then render in footer
        might want to output in pages... chunks
        """

        data_columns    = []
        for ix_col, i_col in enumerate( self.col_names ):
            # list comp ?? perhaps not, or perhaps
            i_data    = row_object.get_value( i_col,  row_object.ix_db_value )
            data_columns.append( i_data )

        row_for_html    =  data_columns
#        msg   = f"row_for_html >>{row_for_html}<<"
#        AppGlobal.print_debug( msg )

        self.html_table.rows.append( row_for_html )

#        msg   =  str( row_object )   #.ix_db_value
#        AppGlobal.logger.log( AppGlobal.force_log_level, msg )

    #---------------------
    def write_footer(self, footer_info ):
        """
        Purpose: see title
        Args: Return: state change, output
        Raises: none planned
        """
        msg  = "write_footer for html, something more probably needed here "
        print( msg )
        htmlcode      = str( self.html_table )
#        AppGlobal.print_debug( htmlcode )

        self.fileout.write( htmlcode )

#        i_line    =  ":======== eof footer ============"
#        self.fileout.write( i_line   + "\n" )

        self.fileout.close( )

    #---------------------
    def open_output (self,   ):
        """
        Purpose: see title
        Args:
        Return:
            AppGlobal.os_open_txt_file( fileout_name  )
            AppGlobal.os_open_url( fileout_name  )

        """
        url          = self.file_name
        AppGlobal.os_open_url( url  )

#====================================
class SelectCSVWriter( object ):
    """
    Purpose: write a tab separate file
    ?? use format column lengths
    for now make this writer out lines in order -- ?? what order
    """
    #----------- init -----------
    def __init__(self, fileout_name ):
        """
        see class doc
        """

        # !! not sure we will use
        self.file_name       = fileout_name
        self.table_info      = None

        self.html_tablexxxx      = None   # create in write header
        # more def in other functions
        self.fileout         = None   #  a file handle
                                        #create in write header  why not here


    #----------- init -----------
    def write_header( self, table_info ):
        """
        Purpose: see title
        Args: Return: state change, output
        Raises: none planned
        """
        msg   = "write header...."
        AppGlobal.print_debug( msg )

        self.fileout                = open( self.file_name, "w",
                                            encoding = "utf8",
                                            errors = 'replace' )

        self.col_names              =  [ i_format[0] for i_format in table_info.format_list ]
        msg   = f"write_header()  self.col_names  {self.col_names}"
        AppGlobal.print_debug( msg )

        i_line   = []
        for ix_col, i_col in enumerate( self.col_names ):
            #i_data    = self.fix_null( row[ ix_col ] )

            #i_data    = row_object.get_value( i_col,  row_object.ix_db_value )
            i_line.append( f"{i_col}" )    #may need more processing for CSV
        line = "\t".join( i_line )
        self.fileout.write( line    + "\n" )

    #----------------------
    def write_row(self, row_object ):
        """
        Purpose: see title
        Args: Return: state change, output
        Raises: none planned
        """
        i_line   = []
        for ix_col, i_col in enumerate( self.col_names ):
            #i_data    = self.fix_null( row[ ix_col ] )

            i_data    = row_object.get_value( i_col,  row_object.ix_db_value )
            i_line.append( f"{i_data}" )    #may need more processing for CSV
        line = "\t".join( i_line )
        self.fileout.write( line    + "\n" )

    #---------------------
    def write_footer(self, footer_info ):
        """
        Purpose: see title
        Args: Return: state change, output
        Raises: none planned
        """
#        i_line    =  ":======== eof footer ============"
#        self.fileout.write( i_line   + "\n" )

        self.fileout.close( )

    #---------------------
    def open_output (self,   ):
        """
        Purpose: see title
        Args:
        Return:
            AppGlobal.os_open_txt_file( fileout_name  )
            AppGlobal.os_open_url( fileout_name  )

        """
        AppGlobal.os_open_txt_file( self.file_name )


#====================================
class SelectGUIWriter( object ):
    """
    Purpose: write file names to the gui

    """
    #----------- init -----------
    def __init__(self, fileout_name ):
        """
        see class doc
        """
        # self.file_name       = file_name
        # self.table_info      = table_info

        # !! not sure we will use may be in query
        self.file_name       = fileout_name
        self.table_info      = None
        self.ix_record       = None

       # self.html_table      = None   # create in write header
        # more def in other functions
        self.fileout         = None   # create in write header  why not here

    #----------- init -----------
    def write_header( self, table_info ):
        """
        Purpose: see title
        Args: Return: state change, output
        Raises: none planned

        must have filename in select, perhaps only it
        raises some issues

        """
        msg   = "SelectGUIWriter write header...."
        AppGlobal.print_debug( msg )

        self.col_names              =  [ i_format[0] for i_format
                                         in table_info.format_list ]
        msg   = f"write_header()  self.col_names  {self.col_names}"
        AppGlobal.print_debug( msg )

        self.gui      = AppGlobal.gui

        self.gui.clear_scan_list(  )
        self.ix_record       = 0

    #----------------------
    def write_row(self, row_object ):
        """
        Purpose: see title
        Args: Return: state change, output
        Raises: none planned
        """
        self.ix_record += 1

        msg             = f"gui writer { self.ix_record} {row_object}"
        print( msg )

        i_line          = []
        for ix_col, i_col in enumerate( self.col_names ):
            #i_data    = self.fix_null( row[ ix_col ] )

            i_data    = row_object.get_value( i_col,  row_object.ix_db_value )
            i_line.append( f"{i_data}" )    #may need more processing for CSV
        line = "\t".join( i_line )

        self.gui.insert_row_scan_list( line )

    #---------------------
    def write_footer(self, footer_info ):
        """
        Purpose: see title
        Args: Return: state change, output
        Raises: none planned
        """
#        i_line    =  ":======== eof footer ============"
#        self.fileout.write( i_line   + "\n" )

        #self.fileout.close( )
        pass

#====================================
class SelectTXTWriter( object ):
    """
    from easy_db.py file_writes, in process
    HTML.py - a Python module to easily generate HTML tables and lists | Decalage
        *>url  https://www.decalage.info/python/html
    ?? first implementation lots of room for improve  !! right now seems not to work at all
    !! add paging option
    ?? use tuple to reduce mem use
    """
    #----------- init -----------
    def __init__(self, fileout_name ):
        """
        see class doc
        """
        # self.file_name       = file_name
        # self.table_info      = table_info

        # !! not sure we will use
        self.file_name       = fileout_name
        self.table_info      = None

        # more def in other functions
        self.fileout         = None   # create in write header  why not here

    #----------- init -----------
    def write_header( self, table_info ):  # all of row object or just some part or something else
        """
        Purpose: see title
        Args: Return: state change, output
        Raises: none planned
        """
        self.table_info             = table_info # perhaps use later, or put in init
        # lines                       = []

        self.col_names              = [ i_format[0] for i_format in table_info.format_list ]
        # self.html_table             = HTML.Table( header_row = self.col_names )

        msg   = f"write_header()  self.col_names  {self.col_names}"
        AppGlobal.print_debug( msg )

        self.fileout                = open( self.file_name, "w", encoding = "utf8", errors = 'replace' )

        #<h1>Bob fell over the chicken. [H1]</h1>
        i_line    = f"SelectHTMLWriter output from {AppGlobal.controller.app_name} {AppGlobal.controller.version}"
        self.fileout.write( i_line )

        i_line    = f"    SQL used was = {self.table_info.sql}>"
        self.fileout.write( i_line  )

    #----------------------
    def write_row( self, row_object ):
        """
        Purpose: see title
        Args: Return: state change, output
        Raises: none planned
        for now just accumulate, then render in footer
        might want to output in pages... chunks
        """
        line      = "===================="
        self.fileout.write( line    + "\n" )
        for ix_col, i_col in enumerate( self.col_names ):
            i_data    = row_object.get_value( i_col,  row_object.ix_db_value )
            line      = f"{i_col}:{i_data}"
            self.fileout.write( line    + "\n" )

    #---------------------
    def write_footer(self, footer_info ):
        """
        Purpose: see title
        Args: Return: state change, output
        Raises: none planned
        """
        msg  = "write_footer for txt, something more probably needed here "
        print( msg )

        i_line    =  ":======== eof footer ============"
        self.fileout.write( i_line   + "\n" )

        self.fileout.close( )

#        msg       = "\n".join( lines )
#        AppGlobal.logger.log( AppGlobal.force_log_level, i_line )

    #---------------------
    def open_output (self,   ):
        """
        Purpose: see title
        Args:
        Return:
            AppGlobal.os_open_txt_file( fileout_name  )
            AppGlobal.os_open_url( fileout_name  )

        """
        AppGlobal.os_open_txt_file( self.file_name )


# ---- eof ===============

