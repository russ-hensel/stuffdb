#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
Created on Mon Jul 29 08:52:16 2024

        should still be useful for import code
        generation but if used move over to data dict


todo!!
        add to columnms like stuff or call from util

todo!!   add clear_fields

        ix_col          += 1
        item             = QTableWidgetItem( str( self.ix_seq  ) )
        table.setItem( ix_row, ix_col, item   )

        ix_col          += 1
        item             = QTableWidgetItem( str( record.value( "id" ) ) )
        table.setItem( ix_row, ix_col, item   )
        print( f"just set {record.value( "id"       ) = } ")

        ix_col          += 1
        item             = QTableWidgetItem( record.value( "photo_fn" ) )
        table.setItem( ix_row, ix_col, item   )

"""

# ---- imports
#import adjust_path
import pprint
import sys

#import pyperclip

#import string_util
import clip_string_utils
import data_dict_old

# import wat_inspector
# app         = wat_inspector.QApplication( sys.argv )  # Create the QApplication instance
# dialog      = wat_inspector.DisplayWat( app )


an_f     = "f"
l_b      = "{"
r_b      = "}"


# wat_inspector.go(  clip_string_utils, locals() )


TRIPLE_QUOTE   = '"""'
INDENT_4       = 4 * " "
INDENT_8       = 8 * " "
TAB            = "\t"

def   create_if_not_exists( create_sql ):
    """
    this just creates the sql
    good chance out of date
    see to_sql_create
    """
    table_name    = to_table_name( create_sql )
    splits        = create_sql.split( "(", 1 )
    rest_of_sql   = splits[ 1 ]

    begin_sql     = "CREATE TABLE IF NOT EXISTS {table_name} ("
    sql           = f"{begin_sql} {rest_of_sql}"

    print( sql )

    return sql


#-------------------------------------
def history_tab_build_field( i_col_name ):
    """
    what it says read
    Returns:
        none  --- perhaps permote some, but not likely
    """
    field          = f"""
    ix_col          += 1
    item             = QTableWidgetItem( str( record.value( "{i_col_name}" ) ) )
    table.setItem( ix_row, ix_col, item   )
    """
    return field

#-------------------------------------
def history_tab_build_gui( table_name, debug = False):
    """
    what it says read
    Returns:
        none  --- perhaps permote some, but not likely
    """
    #rint( name_list )


    print( f"{INDENT_4}# ---- code_gen: history_tab_build_gui tab -- build_gui -- begin table entries edit to desired fields")
    #name_list, type_list          = to_col_name(  sql )
    name_list     = to_col_name_list( table_name )
    for i_name in name_list:
        field   = history_tab_build_field( i_name )
        print( field )

    print( f"{INDENT_4}# ---- code_gen: history tab -- build_gui -- end table entries")

#-------------------------------------
def detail_tab_build_fields( table_name, debug = False):
    """
    was detail_tab_build_gui(
    this version should use my new controls
    adjusted for type
 r_field_name = "requiredr"
    """
    #rint( name_list )
    indent_1     = 8 * " "
    indent_2    = "\n" + 40 * " "  + indent_1

    print( "" )
    what     = "detail_tab_build_gui use for _build_fields was_build_gui "
    print( f"        # ---- code_gen: {what} -- begin table entries")

    name_list, db_type_list, display_type_list = sqllists_for_table( table_name  )
   # name_list, type_list, my_type_list         =
    print( f"        # ---- code_gen: {what} -- begin table entries")


    for i_name, i_type, i_my_type in zip( name_list, db_type_list, display_type_list ):

        if i_my_type == "skip":
            print( f"# skip{i_name}")

        elif  i_name == "id":
            print( f"{indent_2}# qdates make these non editable")
            #args  = f'{indent}parent = None, \n            r_field_name = "{i_name}", r_type = "integer", f_type = "string" '
            args  = ( f'{indent_2}parent         = None, '
                      f'{indent_2}field_name     = "{i_name}", '
                      f'{indent_2}db_type        = "integer",  '
                      f'{indent_2}display_type   = "string" ' )

            line   =   (
                f'\n{indent_1}# ---- {i_name} '
                f'\n{indent_1}edit_field                  = custom_widgets.CQLineEdit( {args}) '
                f'\n{indent_1}self.{i_name}_field         = edit_field '
                f'\n{indent_1}#edit_field.setPlaceholderText( "{i_name}" ) '
                f'\n{indent_1}self.field_list.append( edit_field ) '
                f'\n{indent_1}layout.addWidget( edit_field )  '
                )

        elif   i_my_type == "timestamp":
            print( f"{indent_2}# timestamp to qdates make these non editable")
            #args  = f'{indent}parent = None, \n            r_field_name = "{i_name}", r_type = "integer", f_type = "string" '
            args  = ( f'{indent_2}parent         = None, '
                      f'{indent_2}field_name     = "{i_name}", '
                      f'{indent_2}db_type        = "timestamp",  '
                      f'{indent_2}display_type   = "qdate" ' )

            line   =   (
                f'\n{indent_1}# ---- {i_name} '
                f'\n{indent_1}edit_field                  = custom_widgets.CQDateEdit( {args}) '
                f'\n{indent_1}self.{i_name}_field         = edit_field '
                f'\n{indent_1}#edit_field.setPlaceholderText( "{i_name}" ) '
                f'\n{indent_1}self.field_list.append( edit_field ) '
                f'\n{indent_1}layout.addWidget( edit_field )  '
                )

        elif   i_my_type == "integer":
            print( f"{indent_2}# timestamp to qdates make these non editable")
            #args  = f'{indent}parent = None, \n            r_field_name = "{i_name}", r_type = "integer", f_type = "string" '
            args  = ( f'{indent_2}parent         = None, '
                      f'{indent_2}field_name     = "{i_name}", '
                      f'{indent_2}db_type        = "integer",  '
                      f'{indent_2}display_type   = "string" ' )

            line   =   (
                f'\n{indent_1}# ---- {i_name} '
                f'\n{indent_1}edit_field                  = custom_widgets.CQLineEdit( {args}) '
                f'\n{indent_1}self.{i_name}_field         = edit_field '
                f'\n{indent_1}#edit_field.setPlaceholderText( "{i_name}" ) '
                f'\n{indent_1}self.field_list.append( edit_field ) '
                f'\n{indent_1}layout.addWidget( edit_field )  '
                )


        else:

            # assume string
            # args  = ( f' parent = None, '
            #           f'\n{24*" "}data_field_name = "{i_name}", data_out_type = "string", data_in_type = "string" ' )
            args  = ( f'{indent_2}parent         = None, '
                      f'{indent_2}field_name     = "{i_name}", '
                      f'{indent_2}db_type        = "string", '
                      f'{indent_2}display_type   = "string" ' )


            line   =   (
                f'\n{indent_1}# ---- {i_name} '
                f'\n{indent_1}edit_field                  = custom_widgets.CQLineEdit( {args}) '
                f'\n{indent_1}self.{i_name}_field         = edit_field '
                f'\n{indent_1}edit_field.setPlaceholderText( "{i_name}" ) '
                f'\n{indent_1}self.field_list.append( edit_field ) '
                f'\n{indent_1}layout.addWidget( edit_field )  '
                )

        print( line )
    print( "" )
    print( f"        # ---- code_gen: {what} -- end table entries")
    print( "" )



#-------------------------------------
def detail_tab_clear_fields(   ):
    """
    what it says read
    Returns:
        none  --- perhaps permote some, but not likely

            self.name_field.clear()
            self.add_kw_field.clear()

    """
    print( "need all new code here ")


    field          = f"""
    ix_col          += 1
    item             = QTableWidgetItem( str( record.value( "{i_col_name}" ) ) )
    table.setItem( ix_row, ix_col, item   )
    """
    return field

#-------------------------------------
def detail_tab_record_to_field( sql ):
    """
    what it says read
    Returns:
    name_list, type_list          = to_col_name(  sql )
    set_r_type
    for i_name, i_type in zip( name_list, type_list ):
    """
    #rint( name_list )

    print( "" )
    print( "# ---- code_gen: detail_tab - ")
    name_list, type_list          = to_col_name(  sql )
    print( "# ---- code_gen: detail_tab -- _record_to_field -- begin code \n\n")
    for i_name, i_type in zip( name_list, type_list ):

        line   =  (
        f"""self.{i_name}_field.set_from_record( record )"""
        )
        print( line )

    print( "# ---- code_gen: detail_tab -- _record_to_field -- end table entries")
    print( "" )


#-------------------------------------
def detail_tab_record_to_field_new_old( sql ):
    """
    what it says read
    Returns:
    name_list, type_list          = to_col_name(  sql )
    set_r_type
    for i_name, i_type in zip( name_list, type_list ):
    """
    #rint( name_list )

    print( "" )
    print( "# ---- code_gen: detail_tab - ")
    name_list, type_list          = to_col_name(  sql )
    print( "# ---- code_gen: detail_tab -- _record_to_field -- begin code \n\n")
    for i_name, i_type in zip( name_list, type_list ):

        line   =  (
        f"""self.{i_name}_field.set_r_type(    record.value(    "{i_name}"       ))"""
        )
        print( line )

    print( "# ---- code_gen: detail_tab -- _record_to_field -- end table entries")
    print( "" )



#-------------------------------------
def detail_tab_record_to_field_old( sql ):
    """
    what it says read
    Returns:
    name_list, type_list          = to_col_name(  sql )

    for i_name, i_type in zip( name_list, type_list ):
    """
    #rint( name_list )

    print( "" )
    print( "# ---- code_gen: detail_tab -- _record_to_field -- begin table entries")
    name_list, type_list          = to_col_name(  sql )

    for i_name in name_list:
        line   =  (
        f"""self.{i_name}_field.setText(    record.value(    "{i_name}"       ))"""
        )
        print( line )

    print( "# ---- code_gen: detail_tab -- _record_to_field -- end table entries")
    print( "" )

#-------------------------------------
def detail_tab_field_to_record( sql ):
    """
    what it says read
    Returns:

    """
    #rint( name_list )

    print( "" )
    print( "# ---- code_gen: code_gen: detail_tab -- field_to_record -- begin table entries")
    name_list, type_list          = to_col_name(  sql )

    for i_name in name_list:
        line   =  (
        f"""record.setValue( "{i_name}",     self.{i_name}_field.text())"""
        )
        print( line )

    print( "# ---- code_gen: code_gen: detail_tab -- field_to_record -- end table entries")
    print( "" )


#-------------------------------------
def edit_fields_for_form( sql ):
    """
    to make a form for a single record edit
    assumes a form layout

        a_widget                            = QLineEdit()
        self.photoshow_id_field             = a_widget
        self.photoshow_id_ix                  = 1
        self.layout.addRow( "photoshow_id",         a_widget )


    """
    #rint( name_list )

    what     = "edit_fields_for_form "
    print( f"        # ---- code_gen: {what} -- begin table entries")


    code                    = """
        layout              = QFormLayout()
        self.layout         = layout
        ix_field            = -1
    """
    print( code )


    name_list, type_list          = to_col_name(  sql )

    for i_name in name_list:
        line   =  (
        f"""
        ix_field                            += 1
        a_widget                            = QLineEdit()
        self.{i_name}_field                   = a_widget
        self.{i_name}_ix                      = ix_field
        layout.addRow( "{i_name}",    a_widget )"""

        )
        print( line )

    print( "" )
    print( f"        # ---- code_gen: {what} -- end table entries")
    print( "" )


#-------------------------------------
def fields_to_model( sql ):
    """


    """
    #rint( name_list )

    print( "" )
    what     = "fields_to_model "
    print( f"        # ---- code_gen: {what} -- !! need edit for type")


    # code                    = """
    #     layout              = QFormLayout()
    #     ix_field            = -1
    # """
    # print( code )

    name_list, type_list          = to_col_name(  sql )

    for i_name in name_list:
        line   =  (

        f"""
        # ---- {i_name}
        data       =  fix_none_int( self.{i_name}_field.text() )
        print( {an_f}"fields_to_model {i_name}  {l_b}data{r_b} {l_b}self.{i_name}_ix = {r_b}")
        model.setData( model.index(  ix_row, self.{i_name}_ix ), data )"""


        )
        print( line )

    print( "" )
    print( f"        # ---- code_gen: {what} -- end table entries")
    print( "" )

       #  print( f"fields_to_model photoshow_id { data } {self.photoshow_id_ix = }" )


#-------------------------------------
def sql_to_fields_old( sql ):
    """


    """
    #rint( name_list )

    print( "" )
    what     = "sql_to_fields "
    print( f"        # ---- code_gen: {what} -- begin table entries")


    name_list, type_list          = to_col_name(  sql )

    for i_name in name_list:
        line   =  (

        f"""
        # ---- {i_name}
        edit_field              = QLineEdit()
        self.{i_name}_field         = edit_field
        edit_field.setPlaceholderText( "{i_name}" )
        tab_layout.addWidget( edit_field )
        """

        )
        print( line )
    print( "" )
    print( f"        # ---- code_gen: {what} -- end table entries")
    print( "" )

#-------------------------------------
def sql_to_mapper( sql ):
    """
    mapper          = QDataWidgetMapper( self )
    self.mapper     = mapper
    mapper.setModel  (self.model)

    mapper.addMapping(self.id_field,             0)
    mapper.addMapping(self.title_field,          1)
    .......
    """
    #rint( name_list )

    print( "" )
    what     = "sql_to_mapper "
    print( f"        # ---- code_gen: {what} -- begin ")

    print( f"""
        # ---- mapper
        mapper          = QDataWidgetMapper( self )
        self.mapper     = mapper
        mapper.setModel  (self.model)
        """ )

    name_list, type_list          = to_col_name(  sql )

    for ix, i_name in enumerate( name_list ):
        line   =  (
        f"""{INDENT_8}mapper.addMapping(self.{i_name}_field,         {ix})  """
        )
        print( line )
    print( "" )
    print( f"        # ---- code_gen: {what} -- end table entries")
    print( "" )


#-------------------------------------
def sql_to_select( create_sql ):
    """


    """
    #rint( name_list )
    table_name      = to_table_name( create_sql )
    print( f"{table_name = }" )

    name_list, type_list          = to_col_name(  create_sql )

    what     = "sql_to_select, no binding  "
    print( f"        # ---- code_gen: {what} -- begin ")

    print(
        '# ---- select  sql'
        f'\n    sql        = """SELECT   '      )

    for ix, i_name in enumerate( name_list[ :-1]   ):
        line   =        f"""    {i_name},"""
        print( line )

    print( f"    {name_list[ -1 ] }  \n    FROM    {table_name}  {TRIPLE_QUOTE} "  )



    # print( f"     VALUES (" )

    # for ix, i_name in enumerate( name_list[ :-1]   ):
    #     line   =        f"""    :{i_name},"""
    #     print( line )

    # print( f"    :{name_list[ -1 ] } ) {TRIPLE_QUOTE}  " )

    # print( )
    # print()


    # for ix, i_name in enumerate( name_list    ):
    #     line   =        f"""    query.bindValue( ":{i_name}", {i_name} )"""
    #     print( line )

    # # print( f"    :{name_list[ -1 ] } )" )
    # # query.bindValue( ":can_execute",    can_execute   )






#-------------------------------------
def sql_to_insert_bind( table_name, debug ):
    """
    might work on indent !!


    code_gen.sql_to_insert( sql )

        sql        =  INSERT INTO    help_info (
        (,
        id,
        id_old,
        type,
        sub_system,
        system,
        key_words,
        ....

        is_example,
        can_execute )
         VALUES (
        :(,
        :id,
        :id_old,
        :type,
        :sub_system,
        .....

        and more bind info


    """
    #rint( name_list )
    # table_name   =  to_table_name( sql )
    # print( "" )
    indent_4     = "    "
    indent_8    = 2 * indent_4
    indent_12    = 3 * indent_4
    indent_16    = 4 * indent_4



    name_list, type_list, display_type_list           = to_col_name(  table_name )

    what     = "sql_to_insert_bind "
    print( f"{indent_12}# ---- code_gen: {what} -- begin ")
    print( "\n")
    print(
        f'{indent_12}# ---- import sql'
        f'\n{indent_12}sql        = """INSERT INTO    {table_name} ( '      )

    for ix, i_name in enumerate( name_list[ :-1]   ):
        line   =  f"""{indent_16}{i_name},"""
        print( line )

    print( f"{indent_16}{name_list[ -1 ] } )" )


    print( f"\n{indent_12}VALUES (" )

    for ix, i_name in enumerate( name_list[ :-1]   ):
        line   =        f"""{indent_16}:{i_name},"""
        print( line )

    print( f"{indent_16}:{name_list[ -1 ] } ) {TRIPLE_QUOTE}  " )

    print( )
    print()
    print( f"\n{indent_12}query.prepare( sql )\n" )

    for ix, i_name in enumerate( name_list    ):
        line   =        f"""{indent_12}query.bindValue( ":{i_name}", {i_name} )"""
        print( line )


    print( "" )
    print( f"{indent_12}# ---- sql_to_insert_bind end : {what} -- end table entries")
    print( "" )

# -------------------------
def to_tabbed_col_names( table_name,  debug = False, ):
    """column names to paste into spreadsheet
        but skip id
    """
    column_name_list, type_list, display_type_list    =  to_column_lists(  table_name,  debug = False, count_init = -1, )
    a_string    = TAB.join( column_name_list[1:] )
    print( a_string )



    # Copy text to clipboard
    #pyperclip.copy( a_string )

    # Get text from clipboard
    # copied_text = pyperclip.paste()
    # print(copied_text)

    # bad sideeffecst out of code
    # app         = QApplication([])  # You need a QApplication to interact with the clipboard
    # clipboard   = app.clipboard()

    # # Put a string into the clipboard
    # clipboard.setText( a_string )

    print("Text copied to clipboard!")




# -------------------------------
def    to_col_name_list(  table_name,  debug = False, count_init = -1, ):
    """ think now dows wht is in name """
    ret   = to_column_lists( table_name,  )
    return ret[ 0 ]

# -------------------------------
def    to_column_lists(  table_name,  debug = False, count_init = -1, ):
    """

            pretty much  sqllists_for_table( table_name )
    take sql and just get the column name and types, and my_types


    return as tuple of lists  -- see code
        column_name_list, type_list, display_type_list    =  to_column_lists(  table_name,  debug = False, count_init = -1, )
    """
    # ----------------------------------------
    # name_list, a_int      = clip_string_utils.clean_string_to_list(
    #                           a_string,
    #                           delete_tailing_spaces  = True,
    #                           delete_comments        = False,
    #                           delete_blank_lines     = True,   )
    #rint( f"to_col_name {debug = }")

    name_list, db_type_list, display_type_list = sqllists_for_table( table_name )


    new_name_list     = name_list
    new_type_list     = db_type_list
    new_my_type_list  = display_type_list
    if debug:
        print( f"{len(new_name_list) = } {new_name_list} {new_my_type_list}" )

    #rint( new_type_list )
    #counter_list, new_name_list, new_type_list
    i_counter = 0
    if debug:
        for   i_name, i_type, i_my_type in zip(   new_name_list, new_type_list, new_my_type_list ):
            print( f"{i_counter} {i_name = }  {i_type = } {i_my_type = }")
            i_counter  += 1

    return new_name_list, new_type_list, new_my_type_list

# -------------------------------
def    to_table_name(  create_sql ):
    """
    take sql and just get the column names
   CREATE TABLE  help_info
   (
    CREATE TABLE IF NOT EXISTS stuff_key_word (
    """
    splits           = create_sql.split(   )
    table_name       = splits[2]
    if table_name.lower() == "if":
       table_name       = splits[5]
    return table_name

# -------------------------------
def    to_data_dict (  table_name, debug = False ):
    """


    code_gen.to_sql_create(  table_name, debug = False )


    a_table_dict   = data_dict.TableDict(  "stuff" )
    a_data_dict.add_table ( a_table_dict )

    # ---- id
    a_column_dict = data_dict.ColumnDict(    column_name    = "id",
                                             db_type        = "INTEGER",
                                             display_type   = "integer",
                                             max_len        = None,
                                             default_func   = None,   )
    a_table_dict.add_column( a_column_dict )



    """

    a_str      = "=================\n\n\n"

    a_str      = f'{a_str}\n    # ---- {table_name} ---------------------------------------------'
    a_str      = f'{a_str}\n    a_table_dict   = data_dict.TableDict( "{table_name}" ) '
    a_str      = f'{a_str}\n    a_data_dict.add_table ( a_table_dict )'
    name_list, db_type_list, display_type_list = sqllists_for_table( table_name )

    for i_name, i_type, i_dtype in zip( name_list, db_type_list, display_type_list ):
        #print( i_name )
        a_str      = f'{a_str}\n\n    # ---- { i_name } '
        a_str      = f'{a_str}\n    a_column_dict = data_dict.ColumnDict(    column_name    = "{i_name}", '
        a_str      = f'{a_str}\n                                             db_type        = "{i_type}", '
        a_str      = f'{a_str}\n                                             display_type   = "{i_dtype}", '

        a_str      = f'{a_str}\n                                             max_len        = None,'
        a_str      = f'{a_str}\n                                             default_func   = None,   )'

        a_str      = f'{a_str}\n    a_table_dict.add_column( a_column_dict )'


        # msg   = f"{i_name}  {i_type}, {i_dtype}"
        # print( msg )

    print( a_str )
    return a_str


# -------------------------------
def    to_meta(  table_name, debug = False ):
    """
    from table name to create sql
    uses the table_dict

    code_gen.to_sql_create(  table_name, debug = False )
    """
    name_list, db_type_list, display_type_list = sqllists_for_table( table_name )

    for i_name, i_type, i_dtype in zip( name_list, db_type_list, display_type_list ):
        msg   = f"{i_name}  {i_type}, {i_dtype}"
        print( msg )


# -------------------------------
def    to_sql_create(  table_name, debug = False ):
    """
    from table name to create sql
    uses the table_dict

    code_gen.to_sql_create(  table_name, debug = False )
    """
    name_list, db_type_list, display_type_list = sqllists_for_table( table_name )
    sql   = f"CREATE TABLE  {table_name}  ("
    for i_name, i_type in zip( name_list, db_type_list ):
        sql   = f"{sql}\n{i_name}  {i_type},"
    sql = sql[ : -1 ] + " ) "
    print( sql )
    return sql


# -------------------------------
def    to_import_splits(  create_sql, debug ):
    """
    argumen shoudl be table name
    could also have a type list to make this smarter

    """
    # ----------------------------------------
    what    =  "to_import_splits"
    #1/0   # needs review esp next line
    name_list, type_list, display_type_list          = to_col_name( create_sql )

    print( "\n\n")
    print( f"# ---- {what} {len(name_list)-1 = }")  # id not in splits
    print( "\n\n")
    print( "!! add next ")
            # # we should get n splits
            # if len( splits ) != 33:
            #     pass
            #     raise Exception( f"wrong len of splits {len( splits ) = }")

    print(             "a_id               = ix_line   + KEY_OFFSET" )

    for ix_name, i_name in enumerate( name_list[ 1: ] ):

        print( f"{i_name}  = import_utils.no_quotes( splits[{ix_name} ] )  " )

    print( f"\n\n# end {what} {len(name_list)-1 = }")

    return

#------------------------------
def sqllists_for_table( table_name, debug = False ):
    """
    data_dict.sql_dict[ "photo" ]
    """
    table_dict_string   = data_dict_old.sql_dict[ table_name ]
    # CREATE TABLE  help_info (
    # 	id    			    INTEGER,         integer
    sql_list, a_int      = clip_string_utils.clean_string_to_list(
                              table_dict_string,
                              delete_tailing_spaces  = True,
                              delete_comments        = False,
                              delete_blank_lines     = True, )

    name_list           = []
    db_type_list        = []
    display_type_list   = []
    # need sql in just right format beware

    for i_line  in sql_list[1 :- 1]:
        splits   =  i_line.split(  )
        if debug:
            print( splits )
        i_name, i_db_type, i_display_type  = splits   # need to have right parts
        i_db_type        = i_db_type.replace( ",", "" )
        i_display_type   = i_display_type.replace( ",", "" )
        name_list.append( i_name )
        db_type_list.append( i_db_type )
        display_type_list.append( i_display_type )

    if debug:
        pprint.pprint( name_list )
        pprint.pprint( db_type_list )
        pprint.pprint( display_type_list )

    return ( name_list, db_type_list, display_type_list  )



# ---- run from here -----------------------------------------------
# ------------------
def test_edit_fields_for_form( ):
    """
    read it
    """
    edit_fields_for_form( ret_sql() )





#test_edit_fields_for_form()

# # ------------------
# def test_1( ):
#     """
#     read it
#     """
#     sql             = ret_sql()
#    name_list, type_list          = to_col_name(  sql )
#     print( name_list )

# # test_1()

# def  test_2():
#     """
#     read it
#     """

#     history_tab_build_gui( ret_sql() )

# #test_2()


# def  test_3():
#     """
#     read it
#     """
#         FUNCTION       = detail_tab_record_to_field( ret_sql() )

# # test_3()

# # -----------------------
# def  test_4():
#     """
#     read it
#     """
#     detail_tab_field_to_record( ret_sql() )

# test_4()
# ---- run from here -----------------------------------------------
# --------------------
if __name__ == "__main__":

    TABLE_NAME    = "people"
    TABLE_NAME    = "people_text"



    # TABLE_NAME    = "help_info"
    # TABLE_NAME    = "help_text"
    # TABLE_NAME    = "key_gen"
    # # TABLE_NAME    = "people_text"
    # TABLE_NAME    = "photo"
    # TABLE_NAME    = "photo_key_word"
    # #TABLE_NAME    = "photo_subject"
    # TABLE_NAME    = "planting"
    # TABLE_NAME    = "planting_key_word"


    # TABLE_NAME    = "plant"
    # TABLE_NAME    = "plant_key_word"
    # TABLE_NAME    = "plant_text"


    TABLE_NAME    = "photo"
    TABLE_NAME    = "photoshow"
    # TABLE_NAME    = "photo_in_show"
    # TABLE_NAME    = "stuff"



    DEBUG         = 1
    #TABLE_NAME    = "photo_subject"

    # ---- function
    #FUNCTION       = sqllists_for_table    # check the sqldict look right
    FUNCTION       = to_sql_create
    FUNCTION       = to_meta
    FUNCTION       = to_data_dict
    # FUNCTION       = to_col_name


    FUNCTION(    TABLE_NAME, DEBUG  )

    # FUNCTION       = to_import_splits   # past tinot import_xxxx.py
    # FUNCTION       = sql_to_insert_bind   # change class to a_calss.... type

    # FUNCTION       = to_tabbed_col_names
    #FUNCTION       = detail_tab_build_fields

    #FUNCTION       = history_tab_build_gui


    #FUNCTION       = detail_tab_record_to_field

    #FUNCTION      = sql_to_fields
    # FUNCTION      = sql_to_mapper
    #FUNCTION      = detail_tab_record_to_field

    # sql    = data_dict.sql_dict[ TABLE_NAME  ]
    #print( sql )
    # ---- run it
    #FUNCTION(    TABLE_NAME, DEBUG  )

    # print( "#    end code gen ")

    #   to_import_splits
    #code_gen.to_import_splits(  sql )

    # ---- sql_to_insert_bind
    #code_gen.sql_to_insert_bind( sql )

    #   detail tab
    #code_gen.sql_to_fields(  sql  )

    #  - history
    #history_tab_build_gui( "planting"  )


    #code_gen.sql_to_select( data_dict.sql_dict["stuff"]  )


    #print( code_gen.to_col_name( sql ) )

    #code_gen.detail_tab_record_to_field( data_dict.sql_dict["stuff"] )    # ---- record_to_field

    #---- field_to_record
    #code_gen.detail_tab_field_to_record( ( data_dict.sql_dict["stuff"] ) )

    # # ---- stuff events
    # # ---- field_to_record
    # if 0 == 1:
    #     code_gen.edit_fields_for_form( ret_sql_stuff_event() )

    # # ---- fields_to_model
    # if 0:
    #     code_gen.fields_to_model( ret_sql_stuff_event() )

    # # ---- model_to_fields
    # if 1    :
    #     code_gen.model_to_fields( ret_sql_stuff_event() )

    # # ---- edit_fields_for_form
    # if 0    :
    #     code_gen.edit_fields_for_form( ret_sql_stuff_event() )
