# -- >>idle
import  adjust_path
import  rpt_data_dict
import  data_dict
data_dict.build_it()
table_name      = "people_phone"

# ------------ choose one

#rpt_data_dict.rpt_display_order( table_name )

#rpt_data_dict.rpt_key_words( table_name )

#rpt_data_dict.gen_build_fields( table_name )

#rpt_data_dict.rpt_list_order( table_name )

#rpt_data_dict.rpt_topic_columns(  table_name  )

#rpt_data_dict.rpt_sql(  table_name  )

#rpt_data_dict.rpt_tables(     )

data_dict.rpt_sub_tab_columns_order(  table_name, verbose = True  )

