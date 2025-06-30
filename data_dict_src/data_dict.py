#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""
Created on Thu Jan  2 11:50:38 2025

@author: russ

access
import data_dict
data_dict.build_it()
something    = data_dict.DATA_DICT.function( a_table_name )

see rpt_data_dict and some sql util thing

help for tab_custom_update_manager may be of assist

"""
import adjust_path
import logging
import string_util
import custom_widgets

# ---- end imports

__VERSION__   = "not maintained"

DATA_DICT     = None  # created on import is instance of DataDict()
SKIP          = "THIS IS A VALUE INDICATING A SKIP"
# ---- defaults  --- use if dict entry is None
default_values                              = {}   # key   = var/use with use often not ind

default_values[ "max_len" ]                 = None     # none means no output of a value

# keep synced
default_values[ "detail_edit_class" ]       = "cw.CQLineEdit"
default_values[ "form_edit" ]               = "cw.CQLineEdit"

default_values[ "is_key_word" ]             = None      #     = True,
default_values[ "edit_to_rec" ]             = None
default_values[ "is_keep_prior_enabled" ]   = SKIP
default_values[ "form_read_only" ]          = SKIP


default_values[ "rec_to_edit_cnv" ]         = SKIP
default_values[ "dict_to_edit_cnv" ]        = SKIP


default_values[ "edit_to_rec_cnv" ]         = SKIP
default_values[ "edit_to_dict_cnv" ]        = SKIP

# cw.CQLineEdit

def get_value( *, field_name  = None, atribute = None, current_value = None ):
    """
    when value is None get a default
        default may be SKIP

    """
    if current_value is not None:
        return current_value

    value    = default_values[ atribute ]

    return value


# ---- defaults None is changed to

# ---- !! check to see if implemented
# get rid of defaults on input ---sometimes non just skips any output
# ---- none may be converted to:
COLUMN_SPAN   = 2   # this should be for normal fields 1 is smallest

# ---- default on input

COLUMN_ORDER  = 100

# print( "    path now:" )
# for i_path in sys.path:
#     print( "        ", i_path )
def create_some_data_dict_from_sql( sql ):
    """

    sql   --- like

CREATE TABLE photo_subject  (
id  INTEGER,
photo_id_old  VARCHAR(15),
table_id_old  VARCHAR(15),
table_joined  VARCHAR(30),
photo_id  INTEGER,
table_id  INTEGER )

                    column_name    = "id",
                    db_type        = "INTEGER",
                    display_type   = "integer",
                    max_len        = None,
                    default_func   = None,   )
    a_table_dict.add_column( a_column_dict )

table_name_her
    """


    print( "\n")
    print( "# ---- create_some_data_dict_from_sql  ---------------------" )
    print()

    # get the table name   CREATE TABLE photo_subject  (
    splits     = sql.split( "\n")
    for i_line in splits:
        i_line   = i_line.strip()
        i_line   = i_line.replace( "  ", " ")
        i_line   = i_line.replace( "  ", " ")
        i_line   = i_line.replace( ",", "")
        if i_line == "":
            continue
        if i_line.startswith(  "CREATE TABLE" ):
            splits     = i_line.split( " " )
            table_name = splits[ 2 ]
            break


    print( "\n\n")
    print( f"    # ---- {table_name}  ---------------------" )
    print( f'    a_table_dict   = data_dict.TableDict(  "{table_name}" ) ' )
    print(  '    a_data_dict.add_table ( a_table_dict )' )
    print()

    splits     = sql.split( "\n")
    for i_line in splits:
        i_line   = i_line.strip()
        i_line   = i_line.replace( "     ", " ")
        i_line   = i_line.replace( "  ", " ")
        i_line   = i_line.replace( "  ", " ")
        i_line   = i_line.replace( ",", "")
        if i_line == "":
            continue

        #print( i_split )
        parts    = i_line.split( " ")
        #rint( parts )

        column_name  = parts[0]
        db_type      = parts[1]

        #rint( f"{column_name = }: {db_type = }")
        #rint()

        if column_name   == "CREATE":
            continue

        display_type  = "error"

        if db_type == "INTEGER":
            display_type = "integer"

        if db_type == "TEXT":
            display_type = "string"

        print( f'    # ---- "{column_name}",   '   )
        print( f'    a_column_dict = data_dict.ColumnDict( column_name  = "{column_name}",   '   )
        print( f'                                          db_type      = "{db_type}",   '   )
        print( f'                                          display_type = "{display_type}",   '   )
        print( f'                                          max_len        = None,  '   )
        print( f'                                          default_func   = None,   )    '   )


        #print()
        print(  '    a_table_dict.add_column( a_column_dict )'   )
        print( )

# -------------------------------------------
def make_name_to_ix_dict( table_name, verbose = False ):
    """
    Code gen or run-time for sub tab list columns
        for the secondary tables

    """
    if verbose:
        print()
        msg        = f"make_name_to_ix_dict {table_name}"
        print( msg )

    #header_dict     = { }   # nexted dict see below
    a_table             = DATA_DICT.get_table( table_name )
    name_to_ix_dict     = a_table.make_name_to_ix_dict()

    if verbose:
        ix      = 0
        for i_colum_name, i_order in name_to_ix_dict.items():
            msg    = f'{ix} { i_colum_name = }   {i_order = }   '
            print( msg )
            ix      += 1


# -------------------------------------------
def rpt_sub_tab_columns_order( table_name, verbose = False ):
    """
    Code gen or runtime for sub tab list columns
        for the secondary tables

    """
    if verbose:
        print()
        msg        = f"rpt_sub_tab_columns_order {table_name}"
        print( msg )

    header_dict     = { }   # nexted dict see below
    a_table         = DATA_DICT.get_table( table_name )
    columns         = a_table.get_list_columns_sql_order()

    for ix, i_column in enumerate( columns ):
        i_type          = i_column.db_type
        i_db_type       = i_column.db_type
        column_name     = i_column.column_name
        i_my_type       = i_column.column_name       # work in progress or error
        i_display_type  = i_column.display_type
        i_form_edit     = i_column.form_edit
        i_is_key_word   = i_column.is_key_word
        i_placeholder   = i_column.placeholder_text
        i_default_func  = i_column.default_func
        i_is_topic      = i_column.is_topic
        col_head_text      = i_column.col_head_text
        col_head_width     = i_column.col_head_width
        col_head_order      = i_column.col_head_order

        a_dict   = {  }
        a_dict[ "col_head_text" ]    = col_head_text
        a_dict[ "col_head_width" ]   = col_head_width
        header_dict[ column_name ]   = a_dict

    if verbose:
        ix      = 0
        for i_key, i_column_dict in header_dict.items():
            msg    = f'{ix} { i_key = } text: {i_column_dict["col_head_text"]}  width: {i_column_dict["col_head_width"]}  '
            print( msg )
            ix      += 1

    return header_dict


# ----------------------------------------
class DataDict(   ):
    """
    for the stuff table....
    """
    def __init__(self, db_name ):
        self.db_name        = db_name
        self.table_dicts    = {}

    def add_table(self, a_table  ):
        """
        the usual
        """
        self.table_dicts[a_table.table_name ] = a_table

    def get_table(self, a_table_name  ):
        """
        what it says
        """
        i_table      = self.table_dicts.get( a_table_name  )
        if i_table is None:
            print( f"could not find table {a_table_name = } ")
            print( str(self) )
        return i_table

    # ----------------------
    def print_table(self, a_table_name  ):
        """
        print out a table
        """
        i_table      = self.table_dicts.get( a_table_name  )
        print( i_table )

    def get_table_name_list( self):
        """ """
        table_list   = [ i_table_name for i_table_name in self.table_dicts.keys(  ) ]
        return table_list


    #------------------------------------------------
    def get_list_columns_sql_order( self, a_table_name   ):
        """
        """
        a_table      = self.table_dicts.get( a_table_name  )
        if a_table is None:
            error_msg      = f"get_list_columns_sql_order self.table_dicts.get failed for table {a_table_name}"
            logging.error( error_msg )
            raise ValueError( error_msg )

        column_list  = a_table.get_list_columns_sql_order()
        #print( column_list )
        return column_list


    # ----------------------
    def get_list_columns(self, a_table_name  ):
        """
        simplify call to a given table
            columns for a history tab to move data from a record to a history table
            see history_tab record_to_table
        """
        a_table      = self.table_dicts.get( a_table_name  )
        if a_table is None:
            error_msg      = f"self.table_dicts.get failed for table {a_table_name}"
            logging.error( error_msg )
            raise ValueError( error_msg )

        column_list  = a_table.get_list_columns()
        print( column_list )
        return column_list

    #------------------------------------------------
    def make_name_to_ix_dict( self, a_table_name ):
        """
        get the columns name and corresponding
        index  make into a dict
        """
        a_table      = self.table_dicts.get( a_table_name  )
        return   a_table.make_name_to_ix_dict()

    # ------------------------
    def __str__( self, ):
        """ """
        a_str       = "==== DataDict ======"
        a_str       = f"{a_str}\n   {self.db_name = }"
        a_str       = f"{a_str}\n   and our tables are:"
        for i_table_name, i_table_dict in self.table_dicts.items(  ):
            a_str   =  f"{a_str}\n   {i_table_name}"
            # a_td    =  str( i_table_dict )
            # a_str   = a_str + a_td
            # for i_column, i_column_props in i_values.items():
            #     a_str       = f"{a_str}       {i_column = }"
        return a_str

# ----------------------------------------
class TableDict(  ):
    """
    for the stuff table....
    """
    def __init__(self, table_name ):
        """
        the usual
        """
        self.table_name    = table_name
        self.columns        = []

    def add_column(self, a_column  ):
        """
        the usual
        """
        self.columns.append( a_column )

    #------------------------------------------------
    def make_name_to_ix_dict( self, ):
        """
        get the columns name and corresponding
        index  make into a dict
        """
        name_to_ix_dict   = {}

        for ix_column, i_column in enumerate( self.columns ):
            i_type          = i_column.db_type
            i_db_type       = i_column.db_type
            i_edit_in_type  = i_column.edit_in_type
            i_name          = i_column.column_name
            i_my_type       = i_column.column_name       # work in progress or error
            i_display_type  = i_column.display_type
            i_form_edit     = i_column.form_edit
            i_is_key_word   = i_column.is_key_word
            i_placeholder   = i_column.placeholder_text
            i_default_func  = i_column.default_func
            i_is_topic      = i_column.is_topic
           # i_in_history    = i_column.in_history   # do not include id ... number for order
            i_detail_edit_class = i_column.detail_edit_class
            # i_db_convert_type   = i_column.db_convert_type   # string for VARCHAR text....

            name_to_ix_dict[ i_name ]  = ix_column

        return name_to_ix_dict


    #------------------------------------------------
    def get_key_word_columns(self,    ):
        """
        !! not optimized
        """
        key_word_column_list    = []

        for ix_column, i_column in enumerate( self.columns ):


            i_name          = i_column.column_name
            i_my_type       = i_column.column_name       # work in progress or error
            i_display_type  = i_column.display_type
            i_form_edit     = i_column.form_edit
            i_is_key_word   = i_column.is_key_word
            i_placeholder   = i_column.placeholder_text
            i_default_func  = i_column.default_func
            i_is_topic      = i_column.is_topic

            i_detail_edit_class = i_column.detail_edit_class
            # i_db_convert_type   = i_column.db_convert_type   # string for VARCHAR text....

            if i_is_key_word is True:
                key_word_column_list.append( i_name )

        #column_list.sort( key = lambda i_column: i_column.in_history )
        # breakpoint()
        return key_word_column_list


    #------------------------------------------------
    def get_detail_columns(self,    ):
        """
        get the columns ( not including id )
        for the detail tab, add field_label??
        """
        column_list    = []

        for ix_column, i_column in enumerate( self.columns ):
            i_type          = i_column.db_type
            i_db_type       = i_column.db_type
            i_edit_in_type  = i_column.edit_in_type
            i_name          = i_column.column_name
            i_my_type       = i_column.column_name       # work in progress or error
            i_display_type  = i_column.display_type
            i_form_edit     = i_column.form_edit
            i_is_key_word   = i_column.is_key_word
            i_placeholder   = i_column.placeholder_text
            i_default_func  = i_column.default_func
            i_is_topic      = i_column.is_topic
            i_in_history    = i_column.in_history   # do not include id ... number for order
            i_detail_edit_class = i_column.detail_edit_class
            # i_db_convert_type   = i_column.db_convert_type   # string for VARCHAR text....

            if i_name == "id": # skip the id column
                continue

            if i_detail_edit_class == "skip":
                continue

            if i_detail_edit_class is None:
                i_detail_edit_class          = cw.CQLineEdit
                i_column.detail_edit_class   = i_detail_edit_class

            column_list.append( i_column )

        #column_list.sort( key = lambda i_column: i_column.in_history )

        return column_list

    #------------------------------------------------
    def get_list_columns( self,    ):
        """
        get the columns ( not including id ) in the correct order  --- sorted
        for the history tab, add column heading
        column    = data_dict.DATA_DICT.get_history_columns( a_table_name )
        """
        column_list    = []

        for ix_column, i_column in enumerate( self.columns ):
            i_type          = i_column.db_type
            i_db_type       = i_column.db_type
            i_name          = i_column.column_name
            i_my_type       = i_column.column_name       # work in progress or error
            i_display_type  = i_column.display_type
            i_form_edit     = i_column.form_edit
            i_is_key_word   = i_column.is_key_word
            i_placeholder   = i_column.placeholder_text
            i_default_func  = i_column.default_func
            i_is_topic      = i_column.is_topic

            i_col_head_order          = i_column.col_head_order
            i_col_head_text      = i_column.col_head_text
            i_col_head_width     = i_column.col_head_width

            if   i_col_head_width < 0:
                continue

            #rint( f"appending {i_column.column_name}"  )

            column_list.append( i_column )

        column_list.sort( key = lambda i_column: i_column.col_head_order )

        return column_list

    #------------------------------------------------
    def get_list_columns_sql_order( self,    ):
        """
        get the columns ( not including id ) in the correct order  --- not sorted
            combine with  get_list_columns
            assume order in data_dict is the sql order

        uses i_col_head_width >= 0 for selection

        for the history tab, add column heading
        column    = data_dict.DATA_DICT.get_history_columns( a_table_name )
        """
        column_list    = []

        for ix_column, i_column in enumerate( self.columns ):
            i_type          = i_column.db_type
            i_db_type       = i_column.db_type
            i_name          = i_column.column_name
            i_my_type       = i_column.column_name       # work in progress or error
            i_display_type  = i_column.display_type
            i_form_edit     = i_column.form_edit
            i_is_key_word   = i_column.is_key_word
            i_placeholder   = i_column.placeholder_text
            i_default_func  = i_column.default_func
            i_is_topic      = i_column.is_topic

            i_col_head_order          = i_column.col_head_order
            i_col_head_text      = i_column.col_head_text
            i_col_head_width     = i_column.col_head_width

            # if   i_col_head_width < 0:
            #     continue

            #rint( f"appending {i_column.column_name}"  )

            column_list.append( i_column )

        # column_list.sort( key = lambda i_column: i_column.col_head_order )

        return column_list

    #------------------------------------------------
    def get_topic_columns( self,    ):
        """
        get the columns ( not including id ) in the correct order
        topic columns
        column    = data_dict.DATA_DICT.get_history_columns( a_table_name )
        """
        column_list    = []

        for ix_column, i_column in enumerate( self.columns ):
            i_type          = i_column.db_type
            i_db_type       = i_column.db_type
            i_name          = i_column.column_name
            i_my_type       = i_column.column_name       # work in progress or error
            i_display_type  = i_column.display_type
            i_form_edit     = i_column.form_edit
            i_is_key_word   = i_column.is_key_word
            i_placeholder   = i_column.placeholder_text
            i_default_func  = i_column.default_func
            i_is_topic      = i_column.is_topic

            i_col_head_order          = i_column.col_head_order
            i_col_head_text      = i_column.col_head_text
            i_col_head_width     = i_column.col_head_width
            topic_colunm_order   = i_column.topic_colunm_order

            if   topic_colunm_order < 0:
                continue

            #rint( f"appending {i_column.column_name}"  )

            column_list.append( i_column )

        column_list.sort( key = lambda i_column: i_column.topic_colunm_order )

        return column_list

    #------------------------------------------------
    def to_history_list(self,    ):
        """
        for set_list_to_detail_ix
            use list of strings then  join
        """
        line_list    = []
        #rint( name_list )
        indent_1     = 8 * " "
        indent_2     = 40 * " "  + indent_1

        line_list.append(  " ---- still needs review/test ....... " )
        what     = "history_tab record_to_table"

        line_list.append( f"        # ---- code_gen: {what} -- begin table entries" )

        #line_list.append(  f'    # ---- {self.table_name} ---------------------------------------------' )

        for ix_column, i_column in enumerate( self.columns ):
            i_type          = i_column.db_type
            i_db_type       = i_column.db_type
            i_name          = i_column.column_name
            i_my_type       = i_column.column_name       # work in progress or error
            i_display_type  = i_column.display_type
            i_form_edit     = i_column.form_edit
            i_is_key_word   = i_column.is_key_word
            i_placeholder   = i_column.placeholder_text
            i_default_func  = i_column.default_func
            i_is_topic      = i_column.is_topic
            i_in_history    = i_column.in_history   # do not include id ... number for order

            #problem with db_type should perhaps be edit_input_type or similar for now tweak
            # i_db_type
            if   i_in_history is None:
                continue

            elif i_in_history is True:
                i_in_history = 99   # should have a number place at end

            elif i_in_history == -1:
                continue

            # later we will collect and sort

            # ix_col          += 1
            # item             = QTableWidgetItem( str( record.value( "title" ) ) )
            # table.setItem( ix_row, ix_col, item   )


            line_list.append(  '' )
            #line_list.append( f'{indent_1}# ---- {i_name}' )
            line_list.append( f'{indent_1}ix_col          += 1' )
            line_list.append( f'{indent_1}item             = QTableWidgetItem( str( record.value( "{i_name}" ) ) ) ' )
            line_list.append( f'{indent_1}table.setItem( ix_row, ix_col, item   ) ' )

            # line_list.append( f'{indent_2}display_type   = "{i_display_type}", ' )
            # line_list.append( f'{indent_2} ) ' )

        a_str       = "\n".join( line_list )
        return a_str

    #------------------------------------------------
    def to_build_form( self,    ):
        """
        build form
        use list and join

        _build_fields( self, layout ):

        """
        line_list       = []
        #rint( name_list )
        indent_1        = 8 * " "
        indent_2        = 40 * " "  + indent_1

        #line_list.append(  " ---- still needs review/test ....... " )
        what            = f"TableDict.to_build_form {__VERSION__} for {self.table_name}"

        line_list.append( f"\n        # ---- code_gen: {what} -- begin table entries ----------------------- " )

        #line_list.append(  f'    # ---- {self.table_name} ---------------------------------------------' )

        column_list           = self.columns[ : ] # make copy
        column_list.sort( key = lambda i_column: i_column.display_order   )

        for ix_column, i_column in enumerate( column_list ):
            i_type          = i_column.db_type
            i_db_type       = i_column.db_type
            field_name          = i_column.column_name
            i_my_type       = i_column.column_name       # work in progress or error
            i_display_type  = i_column.display_type
            column_form_edit     = i_column.form_edit
            i_is_key_word   = i_column.is_key_word
            placeholder_text   = i_column.placeholder_text
            i_default_func      = i_column.default_func
            i_is_topic              = i_column.is_topic   # phasing out
            topic_colunm_order      = i_column.topic_colunm_order
            form_col_span           = i_column.form_col_span
            is_keep_prior_enabled   = i_column.is_keep_prior_enabled
            form_read_only          = i_column.form_read_only
            rec_to_edit_cnv         = i_column.rec_to_edit_cnv
            dict_to_edit_cnv        = i_column.dict_to_edit_cnv

            edit_to_rec_cnv         = i_column.edit_to_rec_cnv
            edit_to_dict_cnv        = i_column.edit_to_dict_cnv
            form_make_ref           = i_column.form_make_ref


            if  True:
                #line_list.append(  '' )
                line_list.append(  '' )
                line_list.append( f'{indent_1}# ---- {field_name}' )

                # ---- form edit
                value     = get_value( field_name = field_name, atribute = "form_edit" , current_value =  column_form_edit  )
                if value is not SKIP:
                    line_list.append( f'{indent_1}edit_field                  = {value}(' )
                # was
                # line_list.append( f'{indent_1}edit_field                  = cw.{i_form_edit}(' )

                #line_list.append( f'{indent_2}# qdates make these non editable' )
                #args  = f'{indent}parent = None, \n            r_field_name = "{i_name}", r_type = "integer", f_type = "string" '
                args  = "see below"
                line_list.append( f'{indent_2}parent         = None, ' )
                line_list.append( f'{indent_2}field_name     = "{field_name}",   ' )
                # next defaults to False so only really need if true
                line_list.append( f'{indent_2}is_keep_prior_enabled     = {is_keep_prior_enabled}, ) ' )

                # ---- form_make_ref create instance with field name
                # self.id_old_field         = edit_field
                if form_make_ref:
                    line_list.append( f'{indent_1}self.{field_name}_field     = edit_field' )

                # ---- rec_to_edit_cnv
                value     = get_value( field_name       = field_name,
                                       atribute         = "rec_to_edit_cnv" ,
                                       current_value    =  rec_to_edit_cnv  )
                if value is not SKIP:
                    line_list.append( f'{indent_1}edit_field.rec_to_edit_cnv        = edit_field.{value}' )

                # ---- dict_to_edit_cnv
                value     = get_value( field_name       = field_name,
                                       atribute         = "dict_to_edit_cnv" ,
                                       current_value    =  dict_to_edit_cnv  )
                if value is not SKIP:
                    line_list.append( f'{indent_1}edit_field.dict_to_edit_cnv       = edit_field.{value}' )

                # ---- edit_to_rec_cnv
                value     = get_value( field_name       = field_name,
                                       atribute         = "edit_to_rec_cnv" ,
                                       current_value    =  edit_to_rec_cnv  )
                if value is not SKIP:
                    line_list.append( f'{indent_1}edit_field.edit_to_rec_cnv        = edit_field.{value}' )

                # ---- edit_to_dict_cnv
                value     = get_value( field_name       = field_name,
                                       atribute         = "edit_to_dict_cnv" ,
                                       current_value    =  edit_to_dict_cnv  )
                if value is not SKIP:
                    line_list.append( f'{indent_1}edit_field.edit_to_dict_cnv       = edit_field.{value}' )


                # ---- form read only
                value     = get_value( field_name            = field_name,
                                      atribute          = "form_read_only" ,
                                      current_value     =  form_read_only  )
                if value is not SKIP:
                    line_list.append( f'{indent_1}edit_field.setReadOnly( {value} ) ' )

                #line_list.append( f'{indent_1}self.{i_name}_field     = edit_field' )
                # ---- is_keep_prior_enabled  this is too late to do it myst be in init if true
                value     = get_value( field_name            = field_name,
                                      atribute          = "is_keep_prior_enabled" ,
                                      current_value     =  is_keep_prior_enabled  )
                if value is not SKIP:
                    line_list.append( f'{indent_1}edit_field.is_keep_prior_enabled        = {value}' )

                if topic_colunm_order >=0:
                    line_list.append( f'{indent_1}self.topic_edits.append( (edit_field, {topic_colunm_order} ) ) ' )

                line_list.append( f'{indent_1}edit_field.setPlaceholderText( "{placeholder_text}" ) ' )



                # # ---- rec_to_edit rec
                # if i_column.rec_to_edit:  # if not none the default
                #     line_list.append( f'{indent_1}edit_field.rec_to_edit     = edit_field.{i_column.rec_to_edit}   ' )

                # ---- validator
                # line_list.append( f'{indent_1}# still validator / default func  {i_default_func} ' )
                #         #edit_field.setPlaceholderText( "add_ts" )

                # ---- key word
                line_list.append( f'{indent_1}self.data_manager.add_field( edit_field, is_key_word = {i_is_key_word} ) ' )

                # perhaps next is for is_topic
                #line_list.append( f'{indent_1}self.data_manager.add_field( edit_field, is_key_word = {i_is_key_word} ) ' )
                if form_col_span is None:
                    form_col_span = COLUMN_SPAN

                line_list.append( f'{indent_1}layout.addWidget( edit_field, columnspan = {form_col_span} ) ' )

       # edit_field.setReadOnly( True )

                # self.form_read_only         = form_read_only

        a_str       = "\n".join( line_list )
        return a_str
    #------------------------------------------------
    def to_build_form_old( self,    ):
        """
        build form
        use list and join

        _build_fields( self, layout ):

        """
        line_list       = []
        #rint( name_list )
        indent_1        = 8 * " "
        indent_2        = 40 * " "  + indent_1

        #line_list.append(  " ---- still needs review/test ....... " )
        what            = f"TableDict.to_build_form {__VERSION__} for {self.table_name}"

        line_list.append( f"\n        # ---- code_gen: {what} -- begin table entries ----------------------- " )

        #line_list.append(  f'    # ---- {self.table_name} ---------------------------------------------' )

        column_list           = self.columns[ : ] # make copy
        column_list.sort( key = lambda i_column: i_column.display_order   )


        for ix_column, i_column in enumerate( column_list ):
            i_type          = i_column.db_type
            i_db_type       = i_column.db_type
            i_name          = i_column.column_name
            i_my_type       = i_column.column_name       # work in progress or error
            i_display_type  = i_column.display_type
            i_form_edit     = i_column.form_edit
            i_is_key_word   = i_column.is_key_word
            i_placeholder   = i_column.placeholder_text
            i_default_func      = i_column.default_func
            i_is_topic              = i_column.is_topic   # phasing out
            topic_colunm_order      = i_column.topic_colunm_order
            form_col_span           = i_column.form_col_span
            is_keep_prior_enabled   = i_column.is_keep_prior_enabled
            # self.edit_to_rec            = edit_to_rec    # string name of function
            # self.rec_to_edit            = rec_to_edit

            if i_name in [ "id", "id_old" ]:
                pass
                #print( str( i_column ))
                #breakpoint()

            #problem with db_type should perhaps be edit_input_type or similar for now tweak
            # i_db_type
            # if  i_db_type   == "INTEGER":
            #     i_db_type   = "integer"

            # else:
            #     i_db_type   = "string"

            # if i_my_type == "skip":   # maybe use order < 0
            #     line_list.append( f'# skip{i_name} ')

            if  True:
                #line_list.append(  '' )
                line_list.append(  '' )
                line_list.append( f'{indent_1}# ---- {i_name}' )

                # ---- form edit
                value     = get_value( atribute = "form_edit" , current_value =  i_column.form_edit  )
                if value is not None:
                    line_list.append( f'{indent_1}edit_field                  = {value}(' )
                # was
                # line_list.append( f'{indent_1}edit_field                  = cw.{i_form_edit}(' )

                #line_list.append( f'{indent_2}# qdates make these non editable' )
                #args  = f'{indent}parent = None, \n            r_field_name = "{i_name}", r_type = "integer", f_type = "string" '
                args  = "see below"
                line_list.append( f'{indent_2}parent         = None, ' )
                line_list.append( f'{indent_2}field_name     = "{i_name}", ' )
                line_list.append( f'{indent_2}db_type        = "{i_db_type}",  ' )
                line_list.append( f'{indent_2}display_type   = "{i_display_type}", ' )
                line_list.append( f'{indent_2} ) ' )

                # self.id_old_field         = edit_field
                line_list.append( f'{indent_1}self.{i_name}_field     = edit_field' )

                if i_name in [ "id", "id_old" ]:
                    line_list.append( f'{indent_1}edit_field.setReadOnly( True ) ' )
                elif False:  # check for editable
                    pass

                if is_keep_prior_enabled:
                    line_list.append( f'{indent_1}edit_field.is_keep_prior_enabled        = True' )

                if topic_colunm_order >=0 :
                    line_list.append( f'{indent_1}self.topic_edits.append( (edit_field, {topic_column_order} ) ) ' )

                line_list.append( f'{indent_1}edit_field.setPlaceholderText( "{i_placeholder}" ) ' )

                # ---- edit_to rec
                value     = get_value( atribute = "edit_to_rec" , current_value =  i_column.edit_to_rec  )
                if value is not None:
                    line_list.append( f'{indent_1}edit_field.edit_to_rec                  = edit_field.{value}' )

                # if i_column.edit_to_rec:  # if not none the default
                #     line_list.append( f'{indent_1}edit_field.edit_to_rec     = edit_field.{i_column.edit_to_rec}   ' )


                # ---- rec_to_edit rec
                if i_column.rec_to_edit:  # if not none the default
                    line_list.append( f'{indent_1}edit_field.rec_to_edit     = edit_field.{i_column.rec_to_edit}   ' )


                line_list.append( f'{indent_1}# still validator / default func  {i_default_func} ' )
                        #edit_field.setPlaceholderText( "add_ts" )
                line_list.append( f'{indent_1}self.data_manager.add_field( edit_field, is_key_word = {i_is_key_word} ) ' )

                # perhaps next is for is_topic
                #line_list.append( f'{indent_1}self.data_manager.add_field( edit_field, is_key_word = {i_is_key_word} ) ' )
                if form_col_span is None:
                    form_col_span = COLUMN_SPAN

                line_list.append( f'{indent_1}layout.addWidget( edit_field, columnspan = {form_col_span} ) ' )

                if i_column.form_read_only:  # perhaps None
                    line_list.append( f'{indent_1}edit_field.setReadOnly( True )' )


       # edit_field.setReadOnly( True )

                # self.form_read_only         = form_read_only

        a_str       = "\n".join( line_list )
        return a_str

    #------------------------------------------------
    def to_upgrade_self(self,    ):
        """
        upgrade the current dict to a better version of itself
        """
        #1/0   # now a down grade
        a_str       = ''
        a_str       = f'{a_str}\n                              '
        a_str       = f'{a_str}\n    # ---- {self.table_name} ---------------------------------------------'
        a_str       = f'{a_str}\n    a_table_dict   = data_dict.TableDict( "{self.table_name}" ) '
        a_str       = f'{a_str}\n    a_data_dict.add_table ( a_table_dict )'


        for ix_column, i_column in enumerate( self.columns ):

            #for i_name, i_type, i_dtype in zip( name_list, db_type_list, display_type_list ):
            #print( i_name )
            a_str      = f'{a_str}\n\n    # ---- { i_column.column_name } {ix_column} '
            a_str      = f'{a_str}\n    a_column_dict = data_dict.ColumnDict(    column_name       = "{i_column.column_name}", '
            a_str      = f'{a_str}\n                                             db_type           = "{i_column.db_type}", '

            # ---- detail_edit_class
            item       = i_column.detail_edit_class
            if item is not None:
                a_str      = f'{a_str}\n                                             detail_edit_class = "{item}", '

            # ---- form_edit
            item       = i_column.form_edit
            if item is not None:
                a_str      = f'{a_str}\n                                             form_edit   = "{item}", '

            # ---- rec_to_edit_cnv
            item       = i_column.rec_to_edit_cnv
            if item is not None:
                a_str      = f'{a_str}\n                                             rec_to_edit_cnv   = "{item}", '

            # ---- dict_to_edit_cnv
            item       = i_column.dict_to_edit_cnv
            if item is not None:
                a_str      = f'{a_str}\n                                             dict_to_edit_cnv  = "{item}", '


            # ---- edit_to_rec_cnv
            item       = i_column.edit_to_rec_cnv
            if item is not None:
                a_str      = f'{a_str}\n                                             edit_to_rec_cnv   = "{item}", '


            # ---- edit_to_dict_cnv
            item       = i_column.edit_to_dict_cnv
            if item is not None:
                a_str      = f'{a_str}\n                                             edit_to_dict_cnv  = "{item}", '

            # ---- max_len
            item       = i_column.max_len
            if item is not None:
                a_str      = f'{a_str}\n                                             max_len   = {item}, '

            # ---- placeholder_text
            item       = i_column.placeholder_text
            if item is not None:
                a_str      = f'{a_str}\n                                             placeholder_text  = "{item}", '

            # ---- display_order
            item       = i_column.display_order
            if item is not None:
                a_str      = f'{a_str}\n                                             display_order     = {item}, '

            # ---- create_self
            item       = i_column.create_self
            if item is not None:
                a_str      = f'{a_str}\n                                             create_self  = "{item}", '

            # ---- is_topic
            item       = i_column.is_topic
            if item is not None:
                a_str      = f'{a_str}\n                                             is_topic     = {item}, '

            # ----  topic_colunm_order
            item       = i_column.topic_colunm_order
            if item is not None and item > -1:
                a_str      = f'{a_str}\n                                             topic_colunm_order = {item}, '



            # ---- form_col_span
            item       = i_column.form_col_span
            if item is not None:
                a_str      = f'{a_str}\n                                             form_col_span     = {item}, '

            # ---- form_read_only
            item       = i_column.form_read_only
            if item is not None:
                a_str      = f'{a_str}\n                                             form_read_only    = {item}, '

            # ---- is_keep_prior_enabled
            item       = i_column.is_keep_prior_enabled
            if item is not None:
                a_str      = f'{a_str}\n                                             is_keep_prior_enabled    = {item}, '


            # ---- is_key_word
            item       = i_column.is_key_word
            if item is not None and item is not False:
                a_str      = f'{a_str}\n                                             is_key_word       = {item}, '


            # ---- col_head_text
            item       = i_column.col_head_text
            if item is not None:
                a_str      = f'{a_str}\n                                             col_head_text     = "{item}", '

            # ---- col_head_width
            item       = i_column.col_head_width
            if item is not None and item > 0:
                a_str      = f'{a_str}\n                                             col_head_width    = {item}, '


            # ---- col_head_order
            item       = i_column.col_head_order
            if item is not None and item > 0:
                a_str      = f'{a_str}\n                                             col_head_order    = {item}, '


            # ---- close )
            a_str      = f'{a_str} )  '


            #a_str      = f'{a_str}\n                                             default        = "{i_column.default}   )'

            a_str      = f'{a_str}\n    a_table_dict.add_column( a_column_dict )'


        return a_str

    #---------------------------
    def to_sql_create( self, ):
        """
        what it says, read
        """
        sql      = f"CREATE TABLE  {self.table_name}    ("

        for ix_column, i_column in enumerate( self.columns ):

            if ix_column > 0:
                line    = ","
            else:
                line    = ""
            line        = f"{line}\n     {i_column.column_name}  {i_column.db_type}"
            sql         = f"{sql}{line}"
        sql             = f"{sql}\n    )"

        return sql

    #---------------------------
    def sql_to_insert_bind( self, debug = True ):
        """
        what it says, read

        """
        what           = "sql_to_insert_bind ---- code gen"
        column_list    = []

        line_list    = []
        #rint( name_list )
        indent_1     = 12 * " "
        indent_2     = 40 * " "  + indent_1

        line_list.append(  '' )
        line_list.append(  f'{indent_1}# ---- {what}  ' )
        line_list.append(  '' )

        line_list.append(  f'{indent_1}sql        =   """INSERT INTO    {self.table_name} ( ' )

        ntc             = ","
        ix_max          = len( self.columns ) -1

        for ix_column, i_column in enumerate( self.columns ):
            i_type          = i_column.db_type
            i_db_type       = i_column.db_type
            i_field_name      = i_column.column_name

            if ix_column == ix_max:
                ntc = ""

            line_list.append(  f"{indent_1}{i_field_name}{ntc}", )



        # ---- second pass
        line_list.append(  f"{indent_1}   " )
        line_list.append(  f"{indent_1}VALUES ( " )

        ntc             = ","
        ix_max          = len( self.columns ) -1

        for ix_column, i_column in enumerate( self.columns ):
            i_type          = i_column.db_type
            i_db_type       = i_column.db_type
            i_field_name      = i_column.column_name
            i_edit_in_type  = i_column.edit_in_type

            if ix_column == ix_max:
                ntc = ""

            line_list.append(  f"{indent_1}:{i_field_name}{ntc}"  )
        line_list.append(  f'{indent_1} ) """' )
        #line_list.append(  f'{indent_1} ) ' )

        # ---- third pass
        line_list.append(  f"{indent_1} " )
        line_list.append(  f"{indent_1}query.prepare( sql )   " )
        line_list.append(  f"{indent_1} " )
        #line_list.append(  f"{indent_1}VALUES ( " )

        ntc             = ","
        ix_max          = len( self.columns ) -1

        for ix_column, i_column in enumerate( self.columns ):
            i_type          = i_column.db_type
            i_db_type       = i_column.db_type
            i_field_name      = i_column.column_name

            if ix_column == ix_max:
                ntc = ""

            line_list.append(  f'{indent_1}query.bindValue( ":{i_field_name}", {i_field_name} )'   )

        line_list.append(  '' )
        line_list.append(  f'{indent_1}# ---- {what} ends  ' )


        a_str       = "\n".join( line_list )
        return a_str

    #----------------------------------
    def splits_to_bind( self, debug = True ):
        """
        what it says, read
        first written for stuff_events

        """
        what           = "splits_to_bind ---- code gen "
        column_list    = []
        line_list      = []

        indent_1       = 12 * " "

        line_list.append(  '' )
        line_list.append(  f'{indent_1}# ---- {what} - will need editing -------------------------------' )
        line_list.append(  '' )
        line_list.append(  f'{indent_1}ix_adj = -1 ' )
        line_list.append(  '' )

        for ix_column, i_column in enumerate( self.columns ):
            i_field_name        = i_column.column_name
            line_list.append(  f"{indent_1}{i_field_name}          = import_utils.no_quotes( splits[ {ix_column} + ix_adj ] ) "  )

        line_list.append(  '' )
        line_list.append(  f'{indent_1}# ---- {what} ends  ' )


        a_str       = "\n".join( line_list )
        return a_str

    # ------------------------------
    def __str__( self, ):
        """ """
        a_str       = "\n\n Table Dict "
        a_str       = f"{a_str}   {self.table_name = }"
        for i_column  in self.columns:
            b_str   = str ( i_column )
            a_str   = f"{a_str}{b_str}"
            # a_str   =  f"{a_str}\n    # ---- {i_column.column_name}  "
            # a_str   =  f"{a_str}\n     {i_column}  "
        return a_str


# ----------------------------------------
class ColumnDict(  ):
    """

    for list headers
        is it in the header
            use col_head_width
        what is the header text     a string, default to column name
            col_head_text
        how wide is the header      an int,   0 means not in  header
            col_head_width
        what is the column order ( in lists )
            col_order
        is data editable           - always no
    """
    def __init__(self,  *,
                 column_name        = None,
                 db_type            = None,   # for sql
                 # db_convert_type    = None,    # for record to field looks same as edit_in_type
                 edit_in_type       = None,    # for missing sql types and edit input type
                                               # some confusion with db_type
                 form_edit          = None,    # edit to be used, pretty much auto for most fields plus Int but not dates
                 display_type       = None,
                 display_order          = COLUMN_ORDER,
                 max_len                = None,
                 default_func           = None,
                 validate               = None,
                 is_key_word            = False,
                 placeholder_text       = None,   # will be defaulted
                 create_self            = None,   # create a self .reference -- better put in transaction
                 is_topic               = None,   # part of get topic
                 #in_history         = None,   # to maintain the history list
                 #column_head        = None,   # to label the columns
                 detail_edit_class      = None,   # default to custom_edit.CQLineEdit(   "skip" to skip it
                 # display_order    = number then we sort but what about None ?
                 col_head_text          = None,
                 col_head_width         = -1,
                 col_head_order         = -1,      # my default based on sql
                 topic_colunm_order     = -1,      # not a topic column
                 rec_to_edit            = None,    # no _build_gui output, edit will default
                 edit_to_rec            = None,
                 form_col_span          = None,    # defaulted later
                 form_read_only         = None,    # what it says on detail edit fields None defaults to False
                 form_make_ref          = False,   # when code generating create a self. reference
                 rec_to_edit_cnv        = None,
                 edit_to_rec_cnv        = None,
                 edit_to_dict_cnv       = None,
                 dict_to_edit_cnv       = None,

                 is_keep_prior_enabled  = False,

                 # rec_to_edit         = "rec_to_edit_str_to_str",
                 # edit_to_rec         = "edit_to_rec_str_to_str",

            ):
        """
        the usual
        """
        # ---- column_name ......
        #self.in_history         = in_history
        self.column_name            = column_name
        self.db_type                = db_type
        self.topic_colunm_order     = topic_colunm_order
        self.display_order          = display_order
        self.form_col_span          = form_col_span
        self.form_read_only         = form_read_only

        self.create_self            = create_self

        self.edit_to_rec            = edit_to_rec    # string name of function
        self.rec_to_edit            = rec_to_edit
        self.is_keep_prior_enabled  = is_keep_prior_enabled
        self.rec_to_edit_cnv        = rec_to_edit_cnv
        self.edit_to_rec_cnv        = edit_to_rec_cnv
        self.edit_to_dict_cnv       = edit_to_dict_cnv
        self.dict_to_edit_cnv       = dict_to_edit_cnv
        self.form_make_ref          = form_make_ref
        # # ---- edit_to_rec....
        # if edit_to_rec is None and rec_to_edit is None:
        #     if  db_type  == "INTEGER":
        #         self.edit_to_rec   = "edit_to_rec_str_to_int"
        #         self.rec_to_edit   = "rec_to_edit_int_to_str"

        self.detail_edit_class      = detail_edit_class

        # # ---- edit_in_type
        # if edit_in_type is None:
        #     if  db_type  == "INTEGER":
        #         edit_in_type      = "integer"

        #     elif db_type.startswith( "VAR" ):
        #         edit_in_type      = "string"

        #     elif db_type ==  "TEXT":
        #         edit_in_type      = "string"

        self.edit_in_type       = edit_in_type

        # ---- is_key_word
        self.is_key_word        = is_key_word
        self.validate           = validate

        if placeholder_text is None:
            self.placeholder_text   = column_name
        else:
            self.placeholder_text   = placeholder_text

        # if form_edit is None:
        #     form_edit      = "CQLineEdit"
        self.form_edit      =  form_edit

        self.display_type   =  display_type

        self.is_topic       = is_topic

        self.max_len        = max_len
        self.default_func   = default_func

        # ---- col_head_text      = None,
        if col_head_text is None:
            col_head_text = column_name

        self.col_head_text      = col_head_text

        self.col_head_order     = col_head_order

        self.col_head_width     =  col_head_width

        pass

        pass

    def __str__( self, ):
        """ """
        a_str   = ""
        a_str   = ">>>>>>>>>>* ColumnDict *<<<<<<<<<<<<"
        a_str   = string_util.to_columns( a_str, ["col_head_order",
                                           f"{self.col_head_order}" ] )
        a_str   = string_util.to_columns( a_str, ["col_head_text",
                                           f"{self.col_head_text}" ] )
        a_str   = string_util.to_columns( a_str, ["col_head_width",
                                           f"{self.col_head_width}" ] )
        a_str   = string_util.to_columns( a_str, ["column_name",
                                           f"{self.column_name}" ] )
        a_str   = string_util.to_columns( a_str, ["db_type",
                                           f"{self.db_type}" ] )
        a_str   = string_util.to_columns( a_str, ["default_func",
                                           f"{self.default_func}" ] )
        a_str   = string_util.to_columns( a_str, ["detail_edit_class",
                                           f"{self.detail_edit_class}" ] )
        a_str   = string_util.to_columns( a_str, ["display_order",
                                           f"{self.display_order}" ] )
        a_str   = string_util.to_columns( a_str, ["display_type",
                                           f"{self.display_type}" ] )
        a_str   = string_util.to_columns( a_str, ["edit_in_type",
                                           f"{self.edit_in_type}" ] )
        a_str   = string_util.to_columns( a_str, ["edit_to_rec",
                                           f"{self.edit_to_rec}" ] )
        a_str   = string_util.to_columns( a_str, ["form_col_span",
                                           f"{self.form_col_span}" ] )
        a_str   = string_util.to_columns( a_str, ["form_edit",
                                           f"{self.form_edit}" ] )
        a_str   = string_util.to_columns( a_str, ["is_key_word",
                                           f"{self.is_key_word}" ] )
        a_str   = string_util.to_columns( a_str, ["is_topic",
                                           f"{self.is_topic}" ] )
        a_str   = string_util.to_columns( a_str, ["max_len",
                                           f"{self.max_len}" ] )
        a_str   = string_util.to_columns( a_str, ["placeholder_text",
                                           f"{self.placeholder_text}" ] )
        a_str   = string_util.to_columns( a_str, ["rec_to_edit",
                                           f"{self.rec_to_edit}" ] )
        a_str   = string_util.to_columns( a_str, ["topic_column_order",
                                           f"{self.topic_column_order}" ] )
        a_str   = string_util.to_columns( a_str, ["validate",
                                           f"{self.validate}" ] )
        return a_str


def test():
    """


    """
    a_data_dict   = DataDict(   "stuffdb" )
    a_table_dict  = TableDict(  "help_text" )

    a_column_dict = ColumnDict(    column_name    = "id",
                                   db_type        = "INTEGER",
                                   display_type   = "integer",
                                   max_len        = None,
                                   default_func= None,   )

    a_table_dict.add_column( a_column_dict )

    a_column_dict = ColumnDict(    column_name    = "id_old",
                                   db_type        = "VARCHAR(15)",
                                   display_type   = "string",
                                   max_len        = None,
                                   default_func   = None, )

    a_table_dict.add_column( a_column_dict )

    # ----
    a_column_dict = ColumnDict(    column_name    = "text_data",
                                   db_type        = "TEXT",
                                   display_type   = "string",
                                   max_len        = None,
                                   default_func= None, )

    a_table_dict.add_column( a_column_dict )
    a_data_dict.add_table( a_table_dict )

    #print( a_table_dict.to_sql() )

    #print( a_data_dict )

    print( a_table_dict.to_upgrade_self() )


# def for_import( ):
#     print( "for_import")
#     global DATA_DICT

#     if DATA_DICT is None:
#         DATA_DICT = DataDict( "stuffdb" )
#     else:
#         return

#     import data_dict_stuff
#     data_dict_stuff.build_dd

def build_it_old( db_name ):
    global DATA_DICT
    if DATA_DICT is None:
        DATA_DICT = DataDict( db_name )
    print( DATA_DICT )


def  build_it( db_name = None ):
    """build one time  """
    # global DATA_DICT

    if not db_name:
        db_name = "default, probably stuffdb"

    global DATA_DICT
    if  DATA_DICT:
        return  DATA_DICT

    build_it_old(  db_name )


    import data_dict_help
    data_dict_help.build_it( DATA_DICT )
    #return
    # import data_dict_people
    # data_dict_people.build_it( data_dict.DATA_DICT )

    import data_dict_photo     # missing photo_subject
    data_dict_photo.build_it(  DATA_DICT )

    import data_dict_plant
    data_dict_plant.build_it(  DATA_DICT )

    import data_dict_planting
    data_dict_planting.build_it(  DATA_DICT )

    import data_dict_people
    data_dict_people.build_it(  DATA_DICT )

    import data_dict_stuff
    data_dict_stuff.build_it(  DATA_DICT )

    import data_dict_photoshow
    data_dict_photoshow.build_it(  DATA_DICT )

    import data_dict_key_gen
    data_dict_key_gen.build_it(  DATA_DICT )

    import data_dict_photoshow
    data_dict_photoshow.build_it( DATA_DICT )

    import data_dict_qt5_example
    data_dict_qt5_example.build_it(  DATA_DICT )


    #rint( f"{data_dict.DATA_DICT}" )
    print( "DATA_DICT created ")
    return  DATA_DICT

#build_it()

    # data_dict.DATA_DICT.print_table( "photo" )


    # a_table    = data_dict.DATA_DICT.get_table( "photo_key_word" )
    # # sql         = a_table.to_sql_create ()
    # # print( sql )

    # print( f"{a_table}" )
    # print( a_table.to_build_form() )

# for_import()

# # --------------------
# if __name__ == "__main__":
#     #----- run the full app

#     build_it()

# # --------------------


# ---- eof
