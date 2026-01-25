#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 13:26:54 2025

@author: russ
"""


# ---- tof

# ---- imports

import adjust_path



# ---- end imports


#-------------------------------
import  rpt_data_dict
import  data_dict
data_dict.build_it()

#table_name      = "people"
#table_name      = "people_text"
#table_name      = "people_key_word"
# ---- .... people
# table_name      = "people"
# table_name      = "people_text"
table_name      = "people_phone"


#table_name      = "photo_subject"
#table_name      = "photoshow"


table_name      = "help_info"
table_name      = "help_text"
# table_name      = "help_key_word"

# table_name      = "key_gen"

#table_name      = "planting"

table_name      = "test_table"



# ---- begin reports

# ---- ....
# ---- ....report on create sql
#rpt_data_dict.rpt_sql( table_name  )
# ---- ........ rpt_sql_pg
rpt_data_dict.rpt_sql_pg( table_name  )

#rpt_data_dict.rpt_list_columns_sql_order( table_name )
#rpt_data_dict.rpt_list_column_names_sql_order( table_name )
#rpt_data_dict.rpt_list_column_varcar_limits( table_name )

# ---- ....report on columh list heading..
#rpt_data_dict.rpt_list_order( table_name  )

# ---- detail tab
# ---- ........ report on field display oredr
#rpt_data_dict.rpt_display_order( table_name )

# ---- ........ gen_build_fields
#rpt_data_dict.gen_build_fields( table_name )




# ---- eof