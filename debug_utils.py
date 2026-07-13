#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 08:19:18 2026

see also or instead   SEE INSPECT

/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/rshlib/in_spect


"""

# ---- tof

# --------------------
if __name__ == "__main__":
    import main   # noqa  stops auto removal by pycln
# --------------------

# ---- imports

# -----------------------
def model_dump( model, msg = "model dump msg" ):
    """
    believe is a debug thing
    what type need models be?
    import debug_utils
    debug_utils.model_dump( model )
    """
    print( "model_dump begin")

    # ia_qt.q_abstract_table_model( model )
    # ia_qt.q_sql_table_model( model )

    for col in range( model.columnCount() ):
        field_name  = model.record().fieldName( col )
        field_ix    = model.fieldIndex( field_name )   # usually same as col
        print( f"{col = }  {field_ix = }  {field_name = }" )

    row_count    = model.rowCount()
    column_count = model.columnCount()
    print( f"model_dump begin {row_count = } ")

    for row in range( row_count ):
        row_data = []

        for column in range( column_count ):
            # Get the index for the current row and column
            index   = model.index( row, column )
            # Get the data for the current index
            data    = model.data( index )
            row_data.append( data )

            # # next is debug perhaps
            # if   column == 2:
            #     table_name = data

            # elif column == 1:
            #     table_id = data

        print(f"Row {row}: {row_data}")
    print( "model_dump end")



# ---- imports local -- then constants





# ---- eof ---------------------------


