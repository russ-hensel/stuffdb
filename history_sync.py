#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# ---- tof
"""
Created on Sun Mar 29 10:25:10 2026

@author: russ

begin to sync rows across the application
use signals and slots

import history_sync
history_sync.build_it()

history_sync.HISTORY_SYNC



"""


from qtpy.QtCore import QObject, Signal
from qtpy.QtSql import ( QSqlQuery )

import logging


from app_global import AppGlobal

MISSING_VALUE  = None    # need a unique object for this
# OR DICT_SYNC

# ALBUM_SYNC   = None
# STUFF_SYNC   = None

STUFF_QUERY    = "SELECT id, name, title, descr,   FROM stuff  WHERE id = :arg_id"
     # perhaps later can get from data dict

ALBUM_QUERY    = "SELECT id, name, cmnt,  FROM photoshow  WHERE id = :arg_id"

PLANT_QUERY    = "SELECT id, name, latin_name,  add_kw, descr  FROM plant  WHERE id = :arg_id"

#--------------------------
class DictSender( QObject ):
    pre_mutate   =  Signal()    # a signal not a methoe
    post_mutate  =  Signal()
    #--------------------------
    def emit_pre_mutate( self,   ):
        """
        a method, emits a signal
        """
        self.pre_mutate.emit(   )

    #--------------------------
    def emit_post_mutate( self,   ):
        self.post_mutate.emit(   )

#--------------------------
class HistorySync( QObject ):  # QObject my not really be needed
    def __init__( self, sql = None ):
        """
        the usual
        perhaps one for each ddl being dict synced
        """
        super().__init__()
        self.ddl_dict    = {}   # dict for the ddl
        self.my_sender   = DictSender()
        self.sql      = sql

    #--------------------------
    def add_item(self, key, value ):
        """
        add item to dict, if value is missing
        do sql to find
        """
        self.my_sender.emit_pre_mutate()

        # !! refactor ??
        if value != MISSING_VALUE:
            self.ddl_dict[key] = value

        else:
            if key not in self.ddl_dict: # should always be the case
                value = self.topic_select( key )
                self.ddl_dict[key] = value

        self.my_sender.emit_post_mutate()

    #--------------------------
    def connect(self, cq_dict_combo_box):
        """

        """
        cq_dict_combo_box.history_sync  = self
        cq_dict_combo_box.dict_data     = self.ddl_dict
        self.my_sender.pre_mutate.connect(  cq_dict_combo_box.pre_mutate )
        self.my_sender.post_mutate.connect( cq_dict_combo_box.post_mutate )

    #--------------------------
    def topic_select(self, arg_id ):
        """

        """
        logger          = logging.getLogger( )
        query = QSqlQuery( AppGlobal.qsql_db_access.db )

        query.prepare( self.sql )
        query.bindValue(":arg_id", arg_id )

        if not query.exec_():  # Check if execution failed
            msg = ( f"query_print_tab Error executing query:  {query.lastError().text()}" )
            logging.error(msg)

        topic  = "" # in case query fails
        while query.next():
            topic     = f"{query.value(0)} {query.value(1)} {query.value(2)}"
            break  # only expect 1

        return topic


#------------------------------------
def build_itxxx():
    """


    """
    global HISTORY_SYNC
    if HISTORY_SYNC is None:
        HISTORY_SYNC =  HistorySync()




# ---- eof





