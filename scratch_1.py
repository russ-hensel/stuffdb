#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 09:09:01 2025

@author: russ
"""


# ---- tof

# ---- imports


        key         = "class_name"
        if i_line.startswith(  f"{key.upper()}:"):
                i_line    = i_line[ len(key) + 1 : ].strip()
                doc_data[ key ] = doc_data[ key ] + " " + i_line

        key         = "widgets"
        if i_line.startswith(  f"{key.upper()}:"):
                i_line    = i_line[ len(key) + 1 : ].strip()
                doc_data[ key ] = doc_data[ key ] + " " + i_line

        key         = "tab_title"
        if i_line.startswith(  f"{key.upper()}:"):
                i_line    = i_line[ len(key) + 1 : ].strip()
                doc_data[ key ] = doc_data[ key ] + " " + i_line

        key         = "description"
        if i_line.startswith(  f"{key.upper()}:"):
                i_line    = i_line[ len(key) + 1 : ].strip()
                #doc_data[ key ] = doc_data[ key ] + " " + i_line
                doc_data[ key ] = i_line  # needs to be on one line

        key         = "how_complete"
        if i_line.startswith(  f"{key.upper()}:"):
                i_line    = i_line[ len(key) + 1 : ].strip()
                #doc_data[ key ] = doc_data[ key ] + " " + i_line
                doc_data[ key ] = i_line  # needs to be on one line

        key         = "wiki_link"
        if i_line.startswith(  f"{key.upper()}:"):
                i_line    = i_line[ len(key) + 1 : ].strip()
                #doc_data[ key ] = doc_data[ key ] + " " + i_line
                doc_data[ key ] = i_line  # needs to be on one line



module              = doc_data[ "module" ].strip()  # !! redundatan hack fix
how_complete        = doc_data[ "how_complete" ].strip()
how_complete        = how_complete.replace( "#", " ")

print( f"add_docs_to_db tab file: {how_complete = }" )
# if how_complete != "":
#     breakpoint()

if how_complete    == "":
    how_complete   = "1 #default "
splits             = how_complete.split( " " )
how_complete       = int( splits[0] )

if how_complete < parameters.PARAMETERS.min_complete:
    msg    = ( f"TabDBBuilder dropping {module = } because of "
            "-- not complete enough {how_complete = }  )" )
    logging.debug( msg )
    continue

module       = doc_data[ "module" ].strip()
class_name   = doc_data[ "class_name" ].strip()
if not bool( class_name ) or not bool( module ):
    msg    = ( f"TabDBBuilder dropping {module = } because of "
                "-- not bool( {class_name = } ) or not bool( module )" )
    logging.debug( msg )
    continue

