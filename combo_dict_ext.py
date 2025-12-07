#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
Created on Fri Mar 21 13:21:57 2025

@author: russ

import combo_dict_ext

a_dict_ext   = combo_dict_ext.build_it( db )

think should and do init in the main window

"""


# ---- imports
import weakref


from qt_compat import QApplication, QAction, exec_app, qt_version
from PyQt.QtWidgets import QMainWindow, QToolBar, QMessageBox
from qt_compat import Qt, DisplayRole, EditRole, CheckStateRole
from qt_compat import TextAlignmentRole


# ---- QtSql
from PyQt.QtSql import (QSqlDatabase,
                         QSqlQuery,
                         QSqlQueryModel,
                         QSqlRelation,
                         QSqlRelationalDelegate,
                         QSqlRelationalTableModel,
                         QSqlTableModel)


import logging
import string_util
logger          = logging.getLogger( )

# combo_dict_ext.STUFF_COMBO_DICT_EXT
# ---- end imports

STUFF_COMBO_DICT_EXT    = None
PLANT_COMBO_DICT_EXT    = None    # combo_dict_ext.PLANT_COMBO_DICT_EXT
#
UPDATE                  = "updt"
UPDATE_DEL              = "up_del"


#-------------------------------
class  BaseComboDictExt():
    """ """

    def __init__( self, db, ):
        """
        db is a db connection
        get_docs_function   see use in code
        """
        self.db                     = db
        self.combo_dict             = { None: "None", 1: "one",   } # val stuff ids, val stuff data
        # add only weak rev these are not objects but callable
        self.edit_widget_list       = []   # weakref

    # ---------------------------------
    def update_widget_dict( self, update_type, a_id, info ):
        """
        first warn, then change
        if we used signals and slots we would go directly to the detail
        tab, maybe later
        """
        #maybe use list comp to delete unused widgets
        for i_widget_weak_ref in self.edit_widget_list:
            i_widget   = i_widget_weak_ref()
            if i_widget is not None:
                i_widget.update_dictionary( just_warning = True )

        if update_type == UPDATE:
            self.combo_dict[ a_id ] =  info

        else:
            pass
            # delete not done yet

        for i_widget_weak_ref in self.edit_widget_list:
            i_widget   = i_widget_weak_ref()
            if i_widget is not None:
                i_widget.update_dictionary( just_warning = False )

        pass   # debug

    def add_widget( self, widget ):
        """
        widget is a dict cb edit
        does not really add the widget but a function
        to get a reference  -- also add the back ref here
        """
        widget.widget_ext  = self
        self.edit_widget_list.append( weakref.ref( widget ) )

    # ------------------------------------------
    def add_info_for_id_if( self ):
        """
        actually an add or update
        if we already have the info on hand
            and perhaps also does a dict update
            if needed by compare of info
        """
        print( "add_info_for_id_if  !!please implement and use me")

    # ------------------------------------------
    def get_info_for_id_if( self, a_key ):
        """
        when there is not widget see plant_detail
        """
        if not a_key in self.combo_dict:
            value_not_used      = self.get_info_for_id( a_key )

        print( self )

    # ------------------------------------------
    def get_info_from_record( self, a_id, record ):
        """
        needs to be implemented by the descendant
        use this if you have the record in hand
        avoid the select you might otherwise have
        """
        msg    = "you forgot something"
        raise NotImplemented( msg )

    # ------------------------------------------
    def get_info_for_id( self, a_id ):
        """
        needs to be implemented by the descendant
        """
        msg    = "you forgot something"
        raise NotImplemented( msg )

    # ------------------------------------------
    def __str__( self ):
        """ quite a mess """
        a_str   = ""
        a_str   = ">>>>>>>>>>* PlantComboDictExt *<<<<<<<<<<<<"
        a_str   = string_util.to_columns( a_str, ["combo_dict",
                                           f"{self.combo_dict}" ] )

        for key, value in self.combo_dict.items():
            a_str  = f"{a_str}\n        {key}: {value}"


        a_str   = string_util.to_columns( a_str, ["db",
                                           f"{self.db}" ] )
        a_str   = string_util.to_columns( a_str, ["edit_widget_list",
                                           f"{self.edit_widget_list}" ] )
        # a_str   = string_util.to_columns( a_str, ["stuff_containers[ stuff_id ]",
        #                                    f"{self.stuff_containers[ stuff_id ]}" ] )
        return a_str

#-------------------------------
class  StuffComboDictExt( BaseComboDictExt ):
    """
    extend the functionality of CQComboDict widgets
        trying to avoid subclass because of problems in the past

    """
    # ------------------------------------------
    def get_info_for_id( self,  a_id ):
        """
        each dict probably needs its own extension here

        a little custom query
            Select one record  from the table

        Return
            mutates the dict and the widgets

        """
        query       = QSqlQuery( self.db )

        sql         = f"SELECT name FROM stuff where stuff.id = {a_id}"
        query.prepare( sql )
        query.bindValue( ":a_id", a_id )

        if not query.exec():
            msg   = ( f"get_info_for_id Query execution failed:  {query.lastError().text()}" )
            logging.error( msg, )

            info   = f"query_fail: {a_id}"

        if query.next():  # Fetch the first (and only) result
            info  =  query.value( 0 )

        else:
            msg   = ( f"get_info_for_id no record found {a_id}" )
            logging.error( msg, )

            info   = f"no record: {a_id = }"
            # a_mdi_management   = AppGlobal.mdi_management
            # a_mdi_management.update_stuff_container(   mdi_management.UPDATE, a_id, info )

        self.update_widget_dict(  update_type = UPDATE,
                                                a_id   = a_id,
                                                info   = info )
        pass # debug

    # ------------------------------------------
    def get_info_from_record( self, a_id, record ):
        """
        needs to be implemented by the descendant
        return
            mutate the dict
        """
        data        = record.value(  "name"  )
        info        = data
        self.update_widget_dict(  update_type = UPDATE,
                                                a_id   = a_id,
                                                info   = info )

#-------------------------------
class  PlantComboDictExt( BaseComboDictExt ):
    """
    for the plant table
    """
    # ------------------------------------------
    def get_info_for_id( self, a_id ):
        """
        each dict probably needs its own extension here

        a little custom query
            Select one record  from the table

        Return
            mutates the dict and the widgets
        """
        query       = QSqlQuery(  self.db )
        sql         = f"SELECT name, latin_name FROM plant where plant.id = {a_id}"
        query.prepare( sql )
        query.bindValue(":a_id", a_id )  # Bind the parameter

        if not query.exec():  # Execute the query
            msg   = ( f"get_info_for_id Query execution failed:  {query.lastError().text()}" )
            logging.error( msg, )

            info   = "query_fail: {a_id}"

        if query.next():  # Fetch the first (and only) result
            name  = query.value( 0 )  #  'name' column value
            ln    = query.value( 1 )
            info  = name.strip()[ : 10 ] + "/" + ln.strip()[ : 10 ]

        else:
            msg   = ( f"get_info_for_id no record found {a_id}" )
            logging.error( msg, )

            info   = "no record: {a_id}"

        self.update_widget_dict(  update_type = UPDATE,
                                                a_id   = a_id,
                                                info   = info )

        pass # debug

    # ------------------------------------------
    def get_info_from_record( self, a_id, record ):
        """
        needs to be implemented by the descendant
        return
            mutate the dict
        """
        data        = record.value(  "name"  )
        info        = data
        self.update_widget_dict(  update_type = UPDATE,
                                                a_id   = a_id,
                                                info   = info )
# --------------------------------
def build_it( db ):
    """ """
    global STUFF_COMBO_DICT_EXT
    global PLANT_COMBO_DICT_EXT

    if  not STUFF_COMBO_DICT_EXT:
        STUFF_COMBO_DICT_EXT  = StuffComboDictExt( db )


    if  not PLANT_COMBO_DICT_EXT:
        PLANT_COMBO_DICT_EXT  = PlantComboDictExt( db )

# ---- eof
