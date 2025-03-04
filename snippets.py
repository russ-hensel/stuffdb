#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 07:23:12 2025

@author: russ
"""


# ---- tof

# ---- imports

# ---- end imports


#-------------------------------


# ---- eof



logger          = logging.getLogger( )
LOG_LEVEL       = 20 # level form much debug    higher is more debugging    logging.log( LOG_LEVEL,  debug_msg, )

        debug_msg       = ( f"document_manager update_new_record_v3  {self.table_name  = } " )
        logging.log( LOG_LEVEL,  debug_msg, )


        msg       = ( f"document_manager save_new_record bad state, return  {self.record_state  = } {self.table_name  = } ")
        logging.error( msg )
        logging.debug( debug_msg )