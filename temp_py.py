# -- >>idle
import adjust_path
import stuff_util_sql   as su
import data_dict

db        = su.create_connection(  use_temp = True  )
data_dict.build_it()

#table_name      = "key_gen"
table_name      = "help_info"

# ---- run command ---- read first

print( "here we go" )

record_count   = su.print_record_count( db,   table_name = table_name )
print( f"{ record_count = }" )

max_id   = su.get_max_id( db,   table_name = table_name )

print( f"{ max_id = }" )

# make bigger than max_id
#su.init_key_gen( db, table_name, 200 )


