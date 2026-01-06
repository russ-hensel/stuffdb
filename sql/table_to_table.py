


# ---- tof



import sys
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlError

#-------------------------------
def connect_src():
    """

    """
    # ---- .... db type QSQLITE and location of the db file
    db_type         = "QSQLITE"
    db_file_name    = "./data_test/stuffdb.db"
    db_file_name    = "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/stuffdb/data_test/stuffdb.db"

    db              = QSqlDatabase.addDatabase( db_type, "src_con"  )
            # make this name unique -- from utils....
    db.setDatabaseName( db_file_name )

    if not db.open():
        msg    = f"connect_src database Error: {db.lastError().databaseText()} {db_file_name =} "
        print( msg, )


    connection_name   = db.connectionName()
    debug_msg         = ( f"{connection_name = }")
    print( debug_msg )

    return db

def connect_dest():
    """

    """

    db_type             = "POSTG"
    db_host_name        = "localhost"
    db_port             = 5432
    db_name             = "postgres"
    db_user             = "russ"
    db_password         = "nopassword"

    db                  = QSqlDatabase.addDatabase( "QPSQL", "dest_con" )

    db.setHostName(         db_host_name )
    db.setPort(             db_port       )
    db.setDatabaseName(     db_name       )
    db.setUserName(         db_user       )
    db.setPassword(         db_password  )

    if not db.open():
        print("connect_dest database connection failed:", db.lastError().text())
        1/0
    else:
        print("Database connected successfully!")


    # db         = QSqlDatabase.addDatabase( AppGlobal.parameters.db_type, connection_name  )
    #         # make this name unique -- from utils....
    # db.setDatabaseName( db_file_name )

    connection_name   = db.connectionName()
    debug_msg         = ( f"{connection_name = }")
    print( debug_msg )
    # logging.log( LOG_LEVEL,  debug_msg, )

    return db


#--------------------------------
def run_transfer_help_info():
    """
    """


    src_db      = connect_src()

    dest_db     = connect_dest()

    print( "---- end connect ---- \n\n")
    if not src_db.open() or not dest_db.open():
        print("Database Connection Error!")
        print(f"Source: {src_db.lastError().text()}")
        print(f"Dest: {dest_db.lastError().text()}")
        return

    # 2. DEFINE COLUMNS (From your schema) -- could code gen from data_dict
    columns = [
        "id", "id_old", "type", "sub_system", "system", "key_words",
        "add_ts", "edit_ts", "table_name", "column_name", "java_type",
        "java_name", "java_package", "title", "is_example", "can_execute"
    ]

    # --- 1. DEFINE YOUR SCHEMA LIMITS --- consider code gen
    # Add any column here that has a VARCHAR limit
    limits = {
        "id_old": 15,
        "type": 15,
        "sub_system": 20,
        "system": 20,
        "key_words": 70,
        "table_name": 40,
        "column_name": 40
    }



    # ----- can use different names or not
    source_table    = "help_info"
    dest_table      = "help_info_transfer"
    dest_table      = "help_info"

    select_query    = QSqlQuery(src_db)
    select_query.prepare(f"SELECT * FROM {source_table}")

    # Build the INSERT string using named placeholders (e.g., :id, :type)
    # !! do we really need to do this over and over
    placeholders    = ", ".join([f":{col}" for col in columns])
    col_string      = ", ".join(columns)
    insert_sql      = f"INSERT INTO {dest_table} ({col_string}) VALUES ({placeholders})"

    insert_query    = QSqlQuery(dest_db)
    insert_query.prepare(insert_sql)

    # 4. EXECUTION LOOP
    if not select_query.exec_():
        print(f"Select failed: {select_query.lastError().text()}")
        return

    print("Transfer started...")

    # Use a transaction for reliability and a slight speed boost
    dest_db.transaction()

    while select_query.next():
        record = select_query.record()

        # --- VARIABLE ASSIGNMENT ---
        # We store values in a dictionary so they are "named for the column"
        row = {}
        for col in columns:
            row[col] = record.value(col)

        # --- check len of varcar
        for col, max_len in limits.items():
            val = row.get(col)
            if val and isinstance(val, str) and len(val) > max_len:
                print(f"!!! LENGTH ERROR at ID {row['id']} !!!")
                print(f"Column '{col}' is too long!")
                print(f"Value: '{val}'")
                print(f"Length: {len(val)} (Limit: {max_len})")
                # Optional: truncate it automatically so the program continues
                # row[col] = val[:max_len]




        # ---- cleanup .....
        if row['add_ts'] == "":
            row['add_ts'] = None

        if row['edit_ts'] == "":
            row['edit_ts'] = None

        msg   = ( f"{row['key_words'] = }")
        print( msg )

        # ---- subsystem
        data        = row['sub_system']
        if len( data ) > 15:
            data   = data[ :15 ]
            row['sub_system']  = data

        msg   = ( f"{row['sub_system'] = } { len(row['sub_system'] ) =  }")
        print( msg )


        msg   = ( f"{row['edit_ts'] = }")
        print( msg )

        msg   = ( f"{row['add_ts'] = }")
        print( msg )


        msg   = ( f"{row['id'] = }")
        print( msg )


        # --- DATA MODIFICATION AREA ---
        # # Example: Modify 'java_package' if it meets a condition
        # if row['java_package'] == "com.old.package":
        #     row['java_package'] = "com.new.package"



        # # Example: Ensure 'is_example' is always uppercase
        # if isinstance(row['is_example'], str):
        #     row['is_example'] = row['is_example'].upper()
        # ------------------------------

        # --- 5. BIND VARIABLES AND INSERT ---
        for col in columns:
            insert_query.bindValue(f":{col}", row[col])

        if not insert_query.exec_():
            print(f"Insert failed at ID {row['id']}: {insert_query.lastError().text()}")
            dest_db.rollback()
            return

    dest_db.commit()
    print("Transfer completed successfully.")

    # Cleanup
    src_db.close()
    dest_db.close()


#--------------------------------
def run_transfer_help_text():
    """
    There are about 230 null ids probably failed match
    will drop for now might want to find out...
    """


    src_db      = connect_src()

    dest_db     = connect_dest()

    print( "---- end connect ---- \n\n")
    if not src_db.open() or not dest_db.open():
        print("Database Connection Error!")
        print(f"Source: {src_db.lastError().text()}")
        print(f"Dest: {dest_db.lastError().text()}")
        return

    # ----- can use different names or not
    source_table    = "help_text"
    dest_table      = source_table


    # 2. DEFINE COLUMNS (From your schema) -- could code gen from data_dict
    # rpt_list_column_names_sql_order
    columns = ['id', 'id_old', 'text_data']



    # --- 1. DEFINE YOUR SCHEMA LIMITS --- consider code gen
    # Add any column here that has a VARCHAR limit
    #  rpt_data_dict.rpt_list_column_varcar_limits( table_name )
    limits = {'id_old': 15}



    select_query    = QSqlQuery(src_db)
    select_query.prepare(f"SELECT * FROM {source_table}")

    # Build the INSERT string using named placeholders (e.g., :id, :type)
    # !! do we really need to do this over and over
    placeholders    = ", ".join([f":{col}" for col in columns])
    col_string      = ", ".join(columns)
    insert_sql      = f"INSERT INTO {dest_table} ({col_string}) VALUES ({placeholders})"

    insert_query    = QSqlQuery(dest_db)
    insert_query.prepare(insert_sql)

    # 4. EXECUTION LOOP
    if not select_query.exec_():
        print(f"Select failed: {select_query.lastError().text()}")
        return

    print("Transfer started...")

    # Use a transaction for reliability and a slight speed boost
    dest_db.transaction()

    while select_query.next():
        record = select_query.record()

        # --- VARIABLE ASSIGNMENT ---
        # We store values in a dictionary so they are "named for the column"
        row = {}
        for col in columns:
            row[col] = record.value(col)

        # --- check len of varcar
        for col, max_len in limits.items():
            val = row.get(col)
            if val and isinstance(val, str) and len(val) > max_len:
                print(f"!!! LENGTH ERROR at ID {row['id']} !!!")
                print(f"Column '{col}' is too long!")
                print(f"Value: '{val}'")
                print(f"Length: {len(val)} (Limit: {max_len})")
                # Optional: truncate it automatically so the program continues
                # row[col] = val[:max_len]


        msg   = ( f"{row['id'] = }")
        print( msg )


        # --- insection

        if row['id'] is None or row['id'] == "":
            msg    = ( "skippine null id ")
            print( msg  )
            continue

        # # Example: Modify 'java_package' if it meets a condition
        # if row['java_package'] == "com.old.package":
        #     row['java_package'] = "com.new.package"



        # # Example: Ensure 'is_example' is always uppercase
        # if isinstance(row['is_example'], str):
        #     row['is_example'] = row['is_example'].upper()
        # ------------------------------

        # --- 5. BIND VARIABLES AND INSERT ---
        for col in columns:
            insert_query.bindValue(f":{col}", row[col])

        if not insert_query.exec_():
            print(f"Insert failed at ID {row['id']}: {insert_query.lastError().text()}")
            dest_db.rollback()
            return

    dest_db.commit()
    print("Transfer completed successfully.")

    # Cleanup
    src_db.close()
    dest_db.close()

#---- main
if __name__ == "__main__":
    run_transfer_help_text()







# ---- eof