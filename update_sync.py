#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 10:26:47 2026

update_sync.py


"""

# ---- tof

# --------------------
if __name__ == "__main__":
    import main   # noqa  stops auto removal by pycln
# --------------------

# ---- imports
import  logging
from    qtpy.QtCore import (
                            QObject,
                            Signal,
                           )
#from     qtpy.QtSql import QSqlRecord

import  data_dict_all



# ---- imports local -- then constants
logger      = logging.getLogger( )
#for custom logging level at module
LOG_LEVEL   = 20   # higher is more

# -----------------------------------------
class UpdateSyncSignals( QObject ):
    """
    my signals for db changes and document topics
    some for picture topics
    also stuff containers
    """
    # these seem to be class level objects -- only define the types
    update_sync_pre          = Signal( object, str, str, int, object )  # no self because magic
    update_sync_post         = Signal(  )
        # ?? might add update_source
        # source_object  object
        # update_type,  str
        # table_name,   str,
        # table_id      int
        # object        QSqlRecord or  update_dict   dict ,

    # --------------------------
    def emit_update_sync_pre( self,
                                 sender,
                                 type_of_change,      # select update add delete
                                 table_name,
                                 table_id,
                                 record_or_dict,
                                ):
        """
        why self here not in declaration because magic
        """
        debug_msg   = ( "stuff_container_update emit next")
        logging.log( LOG_LEVEL,  debug_msg, )

        self.update_sync_pre.emit(
                                sender,
                                type_of_change,      # select update add delete
                                table_name,
                                table_id,
                                record_or_dict,       # data payload
                                )

    # --------------------------
    def emit_update_sync_post( self ):
        """
        """
        debug_msg   = ( "stuff_container_update emit next")
        logging.log( LOG_LEVEL,  debug_msg, )

        self.update_sync_post.emit(  )

# ------------------------------------
class UpdateSync(   ):
    def __init__(self, arg_parameters = None ):
        """
        the usual
        """
        self.update_sync_signals     = UpdateSyncSignals()

    # ------------------------
    def update_info(
        self,
        sender,
        type_of_change,      # select update add delete
        table_name,
        table_id,
        record_or_dict,
        ):
        """
        """
        pass
        self.update_sync_signals.emit_update_sync_pre(
                            sender,
                            type_of_change,      # select update add delete
                            table_name,
                            table_id,
                            record_or_dict,
                            )

        self.update_sync_signals.emit_update_sync_post(  )
        pass

# ------------------------------------
def record_to_topic( table_name, record ):
    """
    given a table_name record return the topic for it
    update_sync.record_to_topic( table_name, record )
    """
    #RECORD_TO_TOPIC_DICT[ table_name ]( table_name, record )

    a_table         = data_dict_all.SCHEMA.get_table( table_name )
    topic           = f"{table_name} {record.value( "id" ) } "
    topic           = f" {record.value( "id" ) } "
    col_names       = a_table.get_topic_columns()

    for i_col_name in col_names:
        topic    = f"{topic} {record.value( i_col_name ) } "
    # topic    = "fix me"
    splits     = topic.split( )
    topit      = " ".join( splits )
    return topic




# # ------------------------------------
# def people_record_to_topic( record ):
#     """
#     """

#     topic    = "fix me"

# # needs to be at end
# RECORD_TO_TOPIC_DICT    = { "stuff":   stuff_record_to_topic,
#                             "people":  people_record_to_topic
     #                      }

# ---- eof ---------------------------






