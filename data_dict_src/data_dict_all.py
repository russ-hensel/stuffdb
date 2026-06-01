#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""
Created on Thu Jan  2 11:50:38 2025

aggerate across all modules was data_dict

    big change is it does not build itself.

access -- wrong
import data_dict
data_dict.build_it()
something    = data_dict.DATA_DICT.function( a_table_name )

see rpt_data_dict and some sql util thing

help for tab_custom_update_manager may be of assist

"""

# # -------------------- does not work from sub dir
# if __name__ == "__main__":
#     #----- run the full app
#     import main  # noqa  stops auto removal by pycln
#     pass
# # --------------------

import adjust_path
import logging
import importlib


# import string_utils as string_util
import string_utils
#import custom_widgets

# ---- end imports

__VERSION__   = "not maintained"

SCHEMA        = None  # created on import is instance of DataDict()
SKIP          = "!!SKIP**"

# ---- defaults None is changed to

# ---- !! check to see if implemented
# get rid of defaults on input ---sometimes non just skips any output
# ---- none may be converted to:
COLUMN_SPAN   = 2   # this should be for normal fields 1 is smallest

# ---- default on input

COLUMN_ORDER  = 100

# ---- defaults  --- use if dict entry is None  -- these are defaults
# now none to none is automatic
default_values                              = {}   # key   = var/use with use often not ind

default_values[ "max_len" ]                 = None     # none means no output of a value

# keep synced to modules defaults......

default_values[ "detail_edit_class" ]       = "cw.CQLineEdit"
default_values[ "form_edit" ]               = "cw.CQLineEdit"

default_values[ "is_key_word" ]             = None      #     = change to False
default_values[ "edit_to_rec" ]             = None
default_values[ "is_keep_prior_enabled" ]   = SKIP
default_values[ "form_read_only" ]          = SKIP

default_values[ "rec_to_edit_cnv" ]         = SKIP  # skip means let the widget default internally
default_values[ "dict_to_edit_cnv" ]        = SKIP


default_values[ "edit_to_rec_cnv" ]         = SKIP
default_values[ "edit_to_dict_cnv" ]        = SKIP
default_values[ "set_editable" ]            = SKIP


# --- new fix
default_values[ "col_head_width" ]          = -1

default_values[ "col_head_order" ]          = -1


default_values[ "topic_column_order" ]      = -1

default_values[ "form_col_span" ]           = -1

DEFAULT_VALUES                              = default_values


COL_ATTRIBUTES_ALPHA   = [
                            "column_name",
                            "col_head_order",
                            "col_head_text",
                            "col_head_width",
                            "create_self",
                            "db_type",
                            "default_func",
                            "detail_edit_class",
                            "dict_to_edit_cnv",
                            "display_order",
                            "edit_in_type",
                            "edit_to_dict_cnv",
                            "edit_to_rec",
                            "edit_to_rec_cnv",
                            "edit_tool_tip",
                            "foreign_key_info",
                            "form_col_span",
                            "form_edit",
                            "form_make_ref",
                            "form_read_only",
                            "initial_value",
                            "is_keep_prior_enabled",
                            "is_key_word",
                            "is_topic",
                            "max_len",
                            "placeholder_text",
                            "primay_key_ix",
                            "rec_to_edit",
                            "rec_to_edit_cnv",
                            "set_editable",
                            "topic_column_order",
                            "use_index",
                            "validate",
                               ]

COL_ATTRIBUTES_ALPHA   = [
                            "column_name",

                            "form_col_span",
                            "form_edit",
                            "form_make_ref",          # probably drop use dict
                            "form_read_only",

                            "display_order",

                            "initial_value",          # is used or replaced by partials
                            "is_keep_prior_enabled",
                            "is_key_word",

                            "edit_tool_tip",
                            "placeholder_text",

                            "validate",

                            "col_head_order",
                            "col_head_text",
                            "col_head_width",

                            "create_self",           # ??


                            "db_type",
                            "default_func",         # is used ??

                            "detail_edit_class",
                            "dict_to_edit_cnv",

                            "edit_in_type",

                            "edit_to_rec_cnv",
                            "edit_to_dict_cnv",

                            "rec_to_edit",
                            "rec_to_edit_cnv",

                            "edit_to_rec",         # what

                            "is_topic",             # phase out for topic_column_order
                            "topic_column_order",

                            "max_len",

                            "primay_key_ix",

                            "set_editable",

                            "foreign_key_info",
                            "use_index",

                               ]


# # --------------------------------
# def get_value( *, field_name  = None, attribute = None, current_value = None ):
#     """
#     depricate and remove
#     field_name not currently used
#     when value is None get a default
#         default may be SKIP

#     """
#     1/0
#     if current_value is not None:
#         return current_value

#     value    = default_values[ attribute ]

#     return value

# --------------------------------
def get_column_valuexxx( column, attribute ):
    """
    None may be turned into something else
    replaces get_value  -- attribute as string
    """
    raw_value   = getattr( column, attribute )

    # !! should not need these
    if raw_value == "True":
        msg    = f"get_column_value {column.field_name} return True"
        print( msg )
        return True

    if raw_value == "False":
        msg    = f"get_column_value {column.field_name} return False"
        print( msg )
        return False

    if raw_value is not None:
        msg    = f"get_column_value {column.field_name} return raw valiue {raw_value}"
        print( msg )
        return raw_value

    # if here is None, use get and default to None if other value not used
    # value       = default_values[ attribute ]
    value       = default_values.get( attribute, None )

    msg    = f"get_column_value {column.field_name} return valiue {value}"
    print( msg )
    return value



# print( "    path now:" )
# for i_path in sys.path:
#     print( "        ", i_path )
def create_some_data_dict_from_sqlxxxx( sql ):
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
def make_name_to_ix_dictxxxx( table_name, verbose = False ):
    """
    Code gen or run-time for sub tab list columns
        for the secondary tables

    """
    if verbose:
        print()
        msg        = f"make_name_to_ix_dict {table_name}"
        print( msg )

    #header_dict     = { }   # nexted dict see below
    a_table             = SCHEMA.get_table( table_name )
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
        in use april 2026

    """
    if verbose:
        print()
        msg        = f"rpt_sub_tab_columns_order {table_name}"
        print( msg )

    header_dict     = { }   # nexted dict see below
    a_table         = SCHEMA.get_table( table_name )
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
        col_head_width     = i_column.col_head_width  #  ( )
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
class SchemaDict(   ):
    """
    think wrong
         for the stuff table....\
    db_schema_name   .... may be many instances of the schema
    db_name
    """
    def __init__(self, db_schema_name, module_list = [] ):
        self.db_schema_name     = db_schema_name
        self.table_dicts        = {}
        self.import_modules( module_list )
        global SCHEMA

        if SCHEMA:
            1/0

        SCHEMA  = self

    # --------------------------------
    def import_modules(self, module_list  ):
        """
        the usual
            consider protection against a second import of the same
            module
            module list
        """
        for i_module in module_list:
            a_module = importlib.import_module( i_module )
            a_module.build_it( self )


    # --------------------------------
    def add_table(self, a_table  ):
        """
        the usual
        """
        self.table_dicts[ a_table.table_name ] = a_table

    # --------------------------------
    def get_table( self, a_table_name ):
        """
        what it says
        return a TableDict instance or None
        """
        i_table      = self.table_dicts.get( a_table_name, None  )
        if i_table is None:
            error_msg      = f"get_table could not find table {a_table_name = }"
            logging.error( error_msg )

        return i_table

    # ----------------------
    def print_table(self, a_table_name  ):
        """
        print out a table
        """
        i_table      = self.table_dicts.get( a_table_name  )
        print( i_table )

    #------------------------------------------------
    def get_table_name_list( self):
        """ """
        table_list   = [ i_table_name for i_table_name in self.table_dicts.keys(  ) ]
        return table_list

    #------------------------------------------------
    def get_list_columns_sql_order( self, a_table_name   ):
        """
        deprecated use the TableDict
        """
        error_msg      = ( f"get_list_columns_sql_order deprecated use TableDict {a_table_name}" )
        logging.error( error_msg )
        a_table      = self.table_dicts.get( a_table_name  )
        if a_table is None:
            error_msg      = f"get_list_columns_sql_order self.table_dicts.get failed for table {a_table_name}"
            logging.error( error_msg )
            raise ValueError( error_msg )

        column_list  = a_table.get_list_columns_sql_order()
        return column_list

    # ----------------------
    def get_list_columns(self, a_table_name  ):
        """
        deprecate use the TableDict
        simplify call to a given table
            columns for a history tab to move data from a record to a history table
            see history_tab record_to_table
        """
        error_msg      = ( f"get_list_columns deprecated but should run ??use TableDict {a_table_name}" )
        logging.error( error_msg )
        a_table      = self.table_dicts.get( a_table_name  )
        if a_table is None:
            error_msg      = ( "self.table_dicts.get_list_columns failed"
                             f" for table {a_table_name}" )
            logging.error( error_msg )
            raise ValueError( error_msg )

        column_list  = a_table.get_list_columns()
        return column_list

    #------------------------------------------------
    def make_name_to_ix_dict( self, a_table_name ):
        """
        deprecated use the TableDict  i think
        get the columns name and corresponding
        index  make into a dict
        """
        error_msg      = (   "make_name_to_ix_dict deprecated"
                            f" use TableDict {a_table_name}" )
        logging.error( error_msg )
        a_table      = self.table_dicts.get( a_table_name  )
        return   a_table.make_name_to_ix_dict()

    # ------------------------
    def __str__( self, ):
        """ """
        a_str       = "==== SchemaDict ======"
        a_str       = f"{a_str}\n   {self.db_schema_name = }"
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
    hold the schema, mostly a list of ColumnDicts for a table
    get a column by field name
            ix_column = a_table_dict.name_to_ix_dict[ "field_name" ]
            column    = a_table_dict.columns[ ix_column ]


    """
    def __init__(self, table_name ):
        """
        the usual
        """
        self.table_name    = table_name
        self.columns       = []

    #------------------------------------------------
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
        could change to a comp.
        return  name_to_ix_dict
        """
        name_to_ix_dict   = {}

        for ix_column, i_column in enumerate( self.columns ):
            name_to_ix_dict[  i_column.column_name ]  = ix_column

        return name_to_ix_dict

    #------------------------------------------------
    def get_topic_columns_dup( self, ):
        """
        what does dup mean
        !! not optimized
        """
        column_list    = []

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

            if i_is_topic is True:
                column_list.append( i_name )

        #column_list.sort( key = lambda i_column: i_column.in_history )
        # breakpoint()
        return column_list

    #------------------------------------------------
    def get_key_word_columns( self, ):
        """
        get a list of the column objects for this table
        needs test
        returns
            key_word_column_list of type columns = columnDict, not the names
        """
        # key_word_column_list    = []

        # for ix_column, i_column in enumerate( self.columns ):


        #     i_name          = i_column.column_name
        #     i_my_type       = i_column.column_name       # work in progress or error
        #     i_display_type  = i_column.display_type
        #     i_form_edit     = i_column.form_edit
        #     i_is_key_word   = i_column.is_key_word
        #     i_placeholder   = i_column.placeholder_text
        #     i_default_func  = i_column.default_func
        #     i_is_topic      = i_column.is_topic

        #     i_detail_edit_class = i_column.detail_edit_class
        #     # i_db_convert_type   = i_column.db_convert_type   # string for VARCHAR text....

        #     if i_is_key_word is True:
        #         key_word_column_list.append( i_name )

        key_word_column_list     = [ i_column for i_column in self.columns if i_column.is_key_word  ]

        #column_list.sort( key = lambda i_column: i_column.in_history )
        # breakpoint()
        return key_word_column_list

    #------------------------------------------------
    def get_key_word_columns_old(self,    ):
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
    def get_columns_for_detail(self,    ):
        """
        redo get_detail_columns for automatic generation of forms from data dict
        """
        column_list    = self.columns
        column_list.sort( key = lambda i_column: i_column.display_order )



        # for ix_column, i_column in enumerate( self.columns ):

        #     i_name              = i_column.column_name

        #     i_detail_edit_class = i_column.detail_edit_class

        #     if i_name == "id": # skip the id column
        #         continue

        #     if i_detail_edit_class == "skip":
        #         continue

        #     if i_detail_edit_class is None:
        #         # looks like it set to cause an error -- track down where used
        #         i_detail_edit_class          = "cw.CQLineEdit is this right in data dict"
        #         i_column.detail_edit_class   = i_detail_edit_class

        #     column_list.append( i_column )

        return column_list

    #------------------------------------------------
    def get_detail_columns(self,    ):
        """
        get the columns ( not including id )
        for the detail tab, add field_label??
        looks like translation is bad idea
            returns the ColumnDict's' that are not id or skip
        """
        column_list    = []

        for ix_column, i_column in enumerate( self.columns ):

            i_name              = i_column.column_name

            i_detail_edit_class = i_column.detail_edit_class

            if i_name == "id": # skip the id column
                continue

            if i_detail_edit_class == "skip":
                continue

            if i_detail_edit_class is None:
                # looks like it set to cause an error -- track down where used
                i_detail_edit_class          = "cw.CQLineEdit is this right in data dict"
                i_column.detail_edit_class   = i_detail_edit_class

            column_list.append( i_column )

        return column_list

    #------------------------------------------------
    def get_list_columns( self, ):
        """
        get the columns ( not including id ) in the correct order  --- sorted
        for the history tab, add column heading
        column    = data_dict.DATA_DICT.get_history_columns( a_table_name )
        """
        column_list    = []

        for ix_column, i_column in enumerate( self.columns ):

            i_col_head_width     = i_column.col_head_width

            if   i_col_head_width < 0:
                continue

            #rint( f"appending {i_column.column_name}"  )

            column_list.append( i_column )

        column_list.sort( key = lambda i_column: i_column.col_head_order )

        return column_list

    #------------------------------------------------
    def get_list_columns_sql_order( self, ):
        """
        this is all the columns, not the column names
        get the columns ( including id ) in the correct order  --- not sorted
            combine with  get_list_columns
            assume order in data_dict is the sql order

        !! convert to a comp

        """
        column_list    = []

        for ix_column, i_column in enumerate( self.columns ):
            column_list.append( i_column )

        return column_list

    #------------------------------------------------
    def get_list_column_names_sql_order( self,    ):
        """
        the column names


        """
        column_list    = self.get_list_columns_sql_order()
        name_list      = [ i_column.column_name for i_column in column_list ]


        return name_list

    #------------------------------------------------
    def get_list_column_varcar_limits( self,    ):
        """

        returns ex:
                {'id_old': 15, 'type': 15, 'sub_system': 20, 'system': 20, 'key_words': 120,
                 'table_name': 40, 'column_name': 40, 'java_type': 20, 'java_name': 175,
                 'java_package': 150, 'title': 150, 'is_example': 1, 'can_execute': 1}

        """
        column_list    = self.get_list_columns_sql_order()
        # name_list      = [ i_column.column_name for i_column in column_list ]

        limit_dict     = {}
        for i_column in column_list :
            db_type     = i_column.db_type

            if db_type.startswith( "VARCHAR" ):
                db_len     = db_type[ 8:  ]
                db_len     = db_len[   :-1]
                db_len     = int( db_len )
                limit_dict[i_column.column_name ] = db_len

        return limit_dict

    #------------------------------------------------
    def get_topic_columns( self,):
        """
        get the columns ( not including id ) in the correct order
        topic columns
        column    = data_dict.DATA_DICT.get_history_columns( a_table_name )
        !! a comp for part of this
        return
            a list of column names, strings  -- in order
        """
        column_list    = []

        # !! make comp
        for ix_column, i_column in enumerate( self.columns ):

            if  i_column.topic_column_order < 0:
                continue

            column_list.append( i_column )

        column_list.sort( key = lambda i_column: i_column.topic_column_order )

        column_names    = [ i_column.column_name for i_column in column_list ]

        return column_names

    #------------------------------------------------
    def to_history_list(self,    ):
        """
        for set_list_to_detail_ix
            use list of strings then  join
            looks like code generation
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

            i_name          = i_column.column_name

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
        revised and runs, may be wrong, but now shorter and clearer
        build form
        use list and join

        _build_fields( self, layout ):
            code gen
        return
            str of code
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

            # using getattr now
            # field_name          = i_column.column_name

            # column_form_edit    = i_column.form_edit
            # i_is_key_word       = i_column.is_key_word
            # placeholder_text    = i_column.placeholder_text

            # topic_column_order      = i_column.topic_column_order
            # form_col_span           = i_column.form_col_span
            # is_keep_prior_enabled   = i_column.is_keep_prior_enabled
            # form_read_only          = i_column.form_read_only
            # rec_to_edit_cnv         = i_column.rec_to_edit_cnv
            # dict_to_edit_cnv        = i_column.dict_to_edit_cnv

            # edit_to_rec_cnv         = i_column.edit_to_rec_cnv
            # edit_to_dict_cnv        = i_column.edit_to_dict_cnv
            # form_make_ref           = i_column.form_make_ref
            # set_editable            = i_column.set_editable
            # edit_tool_tip           = i_column.edit_tool_tip

            if  True:
                #line_list.append(  '' )
                line_list.append(  '' )
                value     = get_column_value( i_column, "column_name" )
                line_list.append( f'{indent_1}# ---- {value}' )


                # ---- form_edit
                value     = get_column_value( i_column, "form_edit" )

                if value is not SKIP:
                    line_list.append( f'{indent_1}edit_field                  = {value}(' )
                # was
                # line_list.append( f'{indent_1}edit_field                  = cw.{i_form_edit}(' )

                #line_list.append( f'{indent_2}# qdates make these non editable' )
                #args  = f'{indent}parent = None, \n            r_field_name = "{i_name}", r_type = "integer", f_type = "string" '
                args  = "see below"
                line_list.append( f'{indent_2}parent         = None, ' )

                value     = get_column_value( i_column, "column_name" )
                line_list.append( f'{indent_2}field_name     = "{value}",   ' )
                # next defaults to False so only really need if true

                is_keep_prior_enabled     = get_column_value( i_column, "is_keep_prior_enabled" )
                line_list.append( f'{indent_2}is_keep_prior_enabled     = {is_keep_prior_enabled}, ) ' )

                # ---- form_make_ref create instance with field name
                # in future use form dict do not need instance var
                value     = get_column_value( i_column, "form_make_ref" )
                form_make_ref = value
                if form_make_ref:
                    line_list.append( f'{indent_1}self.{i_column.column_name}_field     = edit_field' )

                # # ---- set_editable
                value     = get_column_value( i_column, "set_editable" )
                if value is not SKIP:
                    line_list.append( f'{indent_1}edit_field.set_editable        = edit_field.set_editable( {value} )' )

                # # ---- rec_to_edit_cnv
                value     = get_column_value( i_column, "rec_to_edit_cnv" )
                if value is not SKIP:
                    line_list.append( f'{indent_1}edit_field.rec_to_edit_cnv        = edit_field.{value}' )

                # ---- dict_to_edit_cnv
                value     = get_column_value( i_column, "dict_to_edit_cnv" )
                if value is not SKIP:
                    line_list.append( f'{indent_1}edit_field.dict_to_edit_cnv       = edit_field.{value}' )

                # ---- edit_to_rec_cnv
                value     = get_column_value( i_column, "edit_to_rec_cnv" )
                if value is not SKIP:
                    line_list.append( f'{indent_1}edit_field.edit_to_rec_cnv        = edit_field.{value}' )

                # ---- edit_to_dict_cnv
                value     = get_column_value( i_column, "edit_to_dict_cnv" )
                if value is not SKIP:
                    line_list.append( f'{indent_1}edit_field.edit_to_dict_cnv       = edit_field.{value}' )

                # ---- form read only
                value     = get_column_value( i_column, "form_read_only" )
                if value is not SKIP:
                    line_list.append( f'{indent_1}edit_field.setReadOnly( {value} ) ' )

                #line_list.append( f'{indent_1}self.{i_name}_field     = edit_field' )
                # ---- is_keep_prior_enabled  this is too late to do it myst be in init if true
                value     = get_column_value( i_column, "is_keep_prior_enabled" )
                if value is not SKIP:
                    line_list.append( f'{indent_1}edit_field.is_keep_prior_enabled        = {value}' )

                # ---- problem here !! ??
                value     = get_column_value( i_column, "is_keep_prior_enabled" )
                if value >= 0:
                    line_list.append( f'{indent_1}self.topic_edits.append( (edit_field, {value} ) ) ' )

                # ---- placeholder_text
                value     = get_column_value( i_column, "placeholder_text" )
                line_list.append( f'{indent_1}edit_field.setPlaceholderText( "{value}" ) ' )

                # # ---- rec_to_edit rec
                # if i_column.rec_to_edit:  # if not none the default
                #     line_list.append( f'{indent_1}edit_field.rec_to_edit     = edit_field.{i_column.rec_to_edit}   ' )

                # ---- validator
                # line_list.append( f'{indent_1}# still validator / default func  {i_default_func} ' )
                #         #edit_field.setPlaceholderText( "add_ts" )

                # ---- key word
                value     = get_column_value( i_column, "is_key_word" )
                line_list.append( f'{indent_1}self.data_manager.add_field( edit_field, is_key_word = {value} ) ' )


                # ---- form_col_span
                # perhaps next is for is_topic
                #line_list.append( f'{indent_1}self.data_manager.add_field( edit_field, is_key_word = {i_is_key_word} ) ' )
                value     = get_column_value( i_column, "form_col_span" )
                form_col_span = value
                # fix in get_column value
                if form_col_span is None:
                    form_col_span = COLUMN_SPAN

                line_list.append( f'{indent_1}layout.addWidget( edit_field, columnspan = {form_col_span} ) ' )

               # edit_field.setReadOnly( True )

               # self.form_read_only         = form_read_only

        a_str       = "\n".join( line_list )

        return a_str

    #------------------------------------------------
    def to_upgrade_self_test( self, ):
        """
        upgrade the current dict to a better version of itself
        see rebuild_dict.py
        """
        #1/0   # now a down grade

        indent_b   = " " * 20


        a_str       = ''
        a_str       = f'{a_str}\n                              '
        a_str       = f'{a_str}\n    # ---- {self.table_name} ---------------------------------------------'
        a_str       = f'{a_str}\n    a_table_dict   = data_dict.TableDict( "{self.table_name}" ) '
        a_str       = f'{a_str}\n    a_data_dict.add_table ( a_table_dict )'


        for ix_column, i_column in enumerate( self.columns ):

            #for i_name, i_type, i_dtype in zip( name_list, db_type_list, display_type_list ):
            #print( i_name )
            a_str      = f'{a_str}\n\n    # ---- { i_column.column_name } {ix_column} '
            a_str      = f'{a_str}\n    a_column_dict = data_dict.ColumnDict( "   column_name       = "{i_column.column_name}", '

            # ---- db_type
            item       = i_column.column_name
            if item is not None:
                a_str      = f'{a_str}\n               column_name      = "{item}", '


            a_str      = f'{a_str}\n                                             db_type           = "{i_column.db_type}", '

            # ---- db_type
            item       = i_column.db_type
            if item is not None:
                a_str      = f'{a_str}\n               db_type          = "{item}", '


            # ---- detail_edit_class
            item       = i_column.detail_edit_class
            if item is not None:
                a_str      = f'{a_str}\n                detail_edit_class = "{item}", '

            # ---- form_edit
            item       = i_column.form_edit
            if item is not None:
                a_str      = f'{a_str}\n                form_edit          = "{item}", '

            # ---- rec_to_edit_cnv
            item       = i_column.rec_to_edit_cnv
            if item is not None:
                a_str      = f'{a_str}\n                rec_to_edit_cnv   = "{item}", '

            # ---- dict_to_edit_cnv
            item       = i_column.dict_to_edit_cnv
            if item is not None:
                a_str      = f'{a_str}\n                dict_to_edit_cnv  = "{item}", '


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

            # ----  topic_column_order
            item       = i_column.topic_column_order
            if item is not None and item > -1:
                a_str      = f'{a_str}\n                                             topic_column_order = {item}, '

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


            # ---- close
            a_str      = f'{a_str} )  '

            #a_str      = f'{a_str}\n                                             default        = "{i_column.default}   )'

            a_str      = f'{a_str}\n    a_table_dict.add_column( a_column_dict )'

        print( a_str )

        return a_str

    #---------------------------
    def to_sql_create( self, ):
        """
        what it says, read
        return
            single long string
        """
        sql      = f"CREATE TABLE  {self.table_name}    ("

        for ix_column, i_column in enumerate( self.columns ):
            key_part    = ""
            # if i_column.primay_key_ix is not None:
            #     key_part    = " PRIMARY KEY NOT NULL "
            if ix_column > 0:
                line    = ","
            else:
                line    = ""

            db_type = i_column.db_type
            if  db_type == "TIMESTAMP":
                db_type  = "INTEGER"

            line        = f"{line}\n     {i_column.column_name}  {db_type} {key_part}"
            sql         = f"{sql}{line}"
        sql             = f"{sql} \n    ) ;"

        return sql

    #---------------------------
    def to_sql_create_pg( self, ):
        """
        what it says, read
                 primay_key_ix          = None,       # None not part of prirmy key
                 use_index              = None,
           id INTEGER PRIMARY KEY NOT NULL,

        for now for only one key part primary
        """
        sql      = f"CREATE TABLE {self.table_name}    ("    # spacing may be problematic

        for ix_column, i_column in enumerate( self.columns ):
            key_part    = ""
            if i_column.primay_key_ix is not None:
                key_part    = " PRIMARY KEY "
            if ix_column > 0:
                line    = ","
            else:
                line    = ""

            db_type = i_column.db_type
            if  db_type == "TIMESTAMP":
                db_type  = "BIGINT"

            line        = f"{line}\n     {i_column.column_name}  {db_type} {key_part}"
            sql         = f"{sql}{line}"

        # ---- second pass
        for ix_column, i_column in enumerate( self.columns ):

            if i_column.foreign_key_info is not None:
                sql         = f"{sql},    "
                line        = ""
                line        = f"{line}\n     {i_column.foreign_key_info}  "
                sql         = f"{sql}{line}"
                sql         = f"{sql}\n    "


        sql             = f"{sql}\n    ); "

        return sql

    #---------------------------
    def sql_to_insert_bind( self, debug = True ):
        """
        what it says, read
        code gen for data import
        written to make it easy to comment out columns
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

        line_list.append(  f'{indent_1}sql        = ( "INSERT INTO    {self.table_name} ( " '  )

        ntc             = ","  # connects the lines, read carefully
        ix_max          = len( self.columns ) -1

        for ix_column, i_column in enumerate( self.columns ):
            i_type          = i_column.db_type
            i_db_type       = i_column.db_type
            i_field_name      = i_column.column_name

            if ix_column == ix_max:
                ntc = " ) "

            line_list.append(  f'{indent_1}"{i_field_name}{ntc}"  ', )

        # ---- second pass
        line_list.append(  f"{indent_1}   " )
        line_list.append(  f'{indent_1}"VALUES ( " ' )

        ntc             = ","
        ix_max          = len( self.columns ) -1

        for ix_column, i_column in enumerate( self.columns ):
            i_type          = i_column.db_type
            i_db_type       = i_column.db_type
            i_field_name    = i_column.column_name
            i_edit_in_type  = i_column.edit_in_type

            if ix_column == ix_max:
                ntc = ""

            line_list.append(  f'{indent_1}":{i_field_name}{ntc} "'  )
        line_list.append(  f'{indent_1}")" ) ' )
        #line_list.append(  f'{indent_1} ) ' )

        # ---- third pass
        line_list.append(  f"{indent_1} " )

        line_list.append(  f'{indent_1}if VERBOSE:  # move to above this block ' )
        line_list.append(  f'{indent_1}    pass ' )
        line_list.append(  f'{indent_1}    #print( .....' )

        line_list.append(  f'{indent_1}# query = QSqlQuery( db )    # better may be above this block ' )

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
        code gen for imports
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
        key_word_column_list   = [ i_column.column_name for i_column in key_word_column_list]

    """
    def __init__(self,  *,
                 column_name            = None,
                 db_type                = None,   # for sql
                 # db_convert_type    = None,    # for record to field looks same as edit_in_type
                 edit_in_type           = None,    # for missing sql types and edit input type
                                               # some confusion with db_type
                 form_edit              = None,    # edit to be used, pretty much auto for most fields plus Int but not dates
                 display_type           = None,
                 display_order          = COLUMN_ORDER,
                 max_len                = None,
                 default_func           = None,
                 validate               = None,
                 is_key_word            = False,
                 placeholder_text       = None,   # will be defaulted
                 create_self            = None,   # create a self .reference -- better put in transaction
                 is_topic               = None,   # part of get topic  --- do not use, use topic_column_order
                 #in_history         = None,   # to maintain the history list
                 #column_head        = None,   # to label the columns
                 detail_edit_class      = None,   # default to custom_edit.CQLineEdit(   "skip" to skip it
                 # display_order    = number then we sort but what about None ?
                 set_editable           = None,   # None default to no output else    edit_field.setEditable( True )
                 col_head_text          = None,
                 col_head_width         = -1,
                 col_head_order         = -1,      # my default based on sql
                 topic_column_order     = -1,      # not a topic column
                 rec_to_edit            = None,    # no _build_gui output, edit will default
                 edit_to_rec            = None,
                 form_col_span          = None,    # defaulted later
                 form_read_only         = None,    # what it says on detail edit fields None defaults to False
                 form_make_ref          = False,   # when code generating create a self. reference
                 rec_to_edit_cnv        = None,    # the widget will do its own default we decode to SKIP
                 edit_to_rec_cnv        = None,
                 edit_to_dict_cnv       = None,
                 dict_to_edit_cnv       = None,
                 edit_tool_tip          = None,     # will default to what
                                                    # bool False, no tip
                                                    # bool True, use field name or something derived
                                                    # string, use string
                 primay_key_ix          = None,       # None not part of prirmy key  index from zero
                 use_index              = None,     # None no index
                 is_keep_prior_enabled  = False,
                 initial_value          = None,      # may mean null or not

                 foreign_key_info       = None,     #

                         # """
                         # CONSTRAINT fk_help_text_help_info
                         #     FOREIGN KEY (id)
                         #     REFERENCES help_info(id)
                         #     ON DELETE CASCADE
                         # """

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
        self.topic_column_order     = topic_column_order
        self.display_order          = display_order
        self.form_col_span          = form_col_span
        self.form_read_only         = form_read_only

        self.create_self            = create_self
        self.set_editable           = set_editable
        self.edit_to_rec            = edit_to_rec    # string name of function
        self.rec_to_edit            = rec_to_edit
        self.is_keep_prior_enabled  = is_keep_prior_enabled
        self.rec_to_edit_cnv        = rec_to_edit_cnv
        self.edit_to_rec_cnv        = edit_to_rec_cnv
        self.edit_to_dict_cnv       = edit_to_dict_cnv
        self.dict_to_edit_cnv       = dict_to_edit_cnv
        self.form_make_ref          = form_make_ref
        self.use_index              = use_index
        # # ---- edit_to_rec....
        # if edit_to_rec is None and rec_to_edit is None:
        #     if  db_type  == "INTEGER":
        #         self.edit_to_rec   = "edit_to_rec_str_to_int"
        #         self.rec_to_edit   = "rec_to_edit_int_to_str"

        self.detail_edit_class      = detail_edit_class
        self.edit_tool_tip          = edit_tool_tip
        self.primay_key_ix          = primay_key_ix
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

        self.foreign_key_info   = foreign_key_info

    # --------------------------------
    def get_column_value_as_string( self,   ):
        """

        """
        indent           = "    "
        # attribute_list   = [
        #                     "column_name",
        #                     "col_head_order",
        #                     "col_head_text",
        #                     "col_head_width",
        #                     "create_self",
        #                     "db_type",
        #                     "default_func",
        #                     "detail_edit_class",
        #                     "dict_to_edit_cnv",
        #                     "display_order",
        #                     "edit_in_type",
        #                     "edit_to_dict_cnv",
        #                     "edit_to_rec",
        #                     "edit_to_rec_cnv",
        #                     "edit_tool_tip",
        #                     "foreign_key_info",
        #                     "form_col_span",
        #                     "form_edit",
        #                     "form_make_ref",
        #                     "form_read_only",
        #                     "initial_value",
        #                     "is_keep_prior_enabled",
        #                     "is_key_word",
        #                     "is_topic",
        #                     "max_len",
        #                     "placeholder_text",
        #                     "primay_key_ix",
        #                     "rec_to_edit",
        #                     "rec_to_edit_cnv",
        #                     "set_editable",
        #                     "topic_column_order",
        #                     "use_index",
        #                     "validate",
        #                        ]

        a_str    = "Attribute List get_column_value_as_string\n"
        for i_attr in COL_ATTRIBUTES_ALPHA:
            raw_attr  = str( getattr( self, i_attr ) )
            value     = str( self.get_column_value( i_attr ) )
            a_str     = f"{a_str}\n{indent}{i_attr:<20} attr = {raw_attr:<20} get_value = {str(value):<20}"


        return a_str

    # --------------------------------
    def get_column_value( self, attribute ):
        """
        NOT FOR WIDGETS OR FUNCTIONS

        value is the value to be used, a lazy default
        replaces get_value  -- attribute as string
        !! sort of a mess - short term, rethink

        ?? break into different functions for different types
        reunite in future ??

        return string, number, or SKIP
        """
        # if attribute  == "":
        #     breakpoint()

        # check on self or field_edit ....
        if self.column_name in [ "name", "title" ] and attribute == "is_keep_prior_enabled":
            # msg   = ( f"get_column_value {self.column_name = } "
            #           f"{attribute = }" )

            # print( msg )
            # breakpoint()
            pass   # for breakpoint !!

        value           = getattr( self, attribute )
        if value is None:
            value   = DEFAULT_VALUES.get( attribute, None )
                # may still be none
        # kluge !! fix for now
        if value == -1:
            value = 1

        # # remove module if present !! later should not be needed
        # if isinstance( raw_value,  str, ):
        #     splits      = raw_value.split( "." )
        #     raw_value   = splits[ -1 ] #
        #     # sort of assumes no valid strings, is this right ??
        #     raw_value   = DEFAULT_VALUES.get( attribute, None )
        #     value       = raw_value


        # if raw_value is not None:
        #     msg    = f"get_column_value** {self.column_name = } {attribute = } return raw_value {raw_value} "
        #     print( msg )
        #     return raw_value

        # # if here is None, use get and default to None if other value not used
        # # value       = default_values[ attribute ]


        # # remove module if present !! later should not be needed
        # if isinstance( value,  str, ):
        #     splits  = value.split( "." )
        #     value   = splits[ -1 ] #

        # msg    = f"get_column_value {self.column_name = } {attribute = } return value {value} "
        # print( msg )

        return value

    # # --------------------------------
    # def get_column_widget( self, attribute ):
    #     """
    #     always resoves to a widget as string, no module
    #     never None

    #     """

    #     if attribute  == "":
    #         breakpoint()

    #     value       = getattr( self, attribute )

    #     # remove module remove later
    #     splits      = value.split( "." )
    #     value       = splits[ -1 ] #
    #     # sort of assumes no valid strings, is this right ??
    #     raw_value   = DEFAULT_VALUES.get( attribute, None )
    #     value       = raw_value


    #     if raw_value is not None:
    #         msg    = f"get_column_value** {self.column_name = } {attribute = } return raw_value {raw_value} "
    #         print( msg )
    #         return raw_value

    #     # if here is None, use get and default to None if other value not used
    #     # value       = default_values[ attribute ]


    #     # remove module if present !! later should not be needed
    #     if isinstance( value,  str, ):
    #         splits  = value.split( "." )
    #         value   = splits[ -1 ] #

    #     msg    = f"get_column_value*** {self.column_name = } {attribute = } return value {value} "
    #     print( msg )

    #     return value


    # --------------------------------
    def get_column_widget_class( self, attribute ):
        """
        # gets a string, name of class, no module
        # remove module if present !! later should not be needed
        """
        value    = getattr( self, attribute )
        if value is None:
            value   = DEFAULT_VALUES.get( attribute, None )

        splits      = value.split( "." )
        value       = splits[ -1 ] #

        # always a string, class name

        return value

    # --------------------------------
    def get_column_function( self, attribute ):
        """
        value is the value to be used, a lazy default
        replaces get_value  -- attribute as string
        !! sort of a mess - short term, rethink

        functions are strings, looked up in base_document
        but this could return a string
        """
        # if attribute  == "":
        #     breakpoint()

        value       = getattr( self, attribute )
        if value is None:
            value       = DEFAULT_VALUES.get( attribute, None )
                # a string name of function or SKIP
        return value

    # --------------------------------
    def __str__( self, ):
        """universal __str__ """
        return string_utils.obj_to_str( self )

# ---------------------------------
def test():

    print( "data_dict_all.test()")
    a_schema_dict   = SchemaDict( "stuffdb" )
    a_schema_dict.import_modules( [ "data_dict_help",
                                    "data_dict_stuff"])

    msg     = f"{a_schema_dict}"
    print( msg )

    a_table_dict    = TableDict(  "help_text" )

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
    a_schema_dict.add_table( a_table_dict )

    print( SCHEMA )

    msg  = """
    not sure this is worth much -- consider delete but better may be find_dict_modules.py
    look for the test in  own .p
    """
    print( msg )
    print( "data_dict_all.test() end ")

# --------------------
if __name__ == "__main__":
    #----- run the full app

    test()

# --------------------


# ---- eof
