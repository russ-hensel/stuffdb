

import    adjust_path

import  data_dict


table_name      = "stuff_event"
table_name      = "photo_subject"
table_name      = "photo_subject"
table_name      = "photo_subject"
table_name      = "people"
table_name      = "people_phone"

data_dict.build_it()
a_table          = data_dict.DATA_DICT.get_table( table_name )

msg       = "did your uncomment something"
msg        = a_table.to_sql_create()
msg        = a_table.sql_to_insert_bind()
#msg        = a_table.sql_to_insert_bind()
msg        = a_table.splits_to_bind()

print( msg )
