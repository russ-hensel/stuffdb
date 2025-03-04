#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""

"""

import data_dict


# ---- build it
def build_it( a_data_dict ):
    """


    """
    #a_data_dict    = data_dict.DATA_DICT

    #---- table_code




    # ---- table_code_end



# ---- eof

# --------------------
# ---- build it end

# ---- type templates ====================================================================


    # ---- some_time_stamp
    a_column_dict = data_dict.ColumnDict(    column_name    = "some_time_stamp",
                                             db_type        = "INTEGER",
                                             display_type   = "timestamp",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )





    # ---- some_varcar
    a_column_dict = data_dict.ColumnDict(    column_name    = "some_varcar",
                                             db_type        = "VARCHAR(15)",
                                             display_type   = "string",
                                             max_len        = None,
                                             default        = None, )
    a_table_dict.add_column( a_column_dict )