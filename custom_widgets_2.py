#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 08:28:33 2026

@author: russ
"""

# ---- tof

# --------------------
if __name__ == "__main__":
    import main   # noqa  stops auto removal by pycln
# --------------------

# ---- imports
#import functools
import logging

from   functools import partial

# ---- Qt
from qtpy.QtCore import QAbstractListModel

from qtpy.QtCore import ( QModelIndex,
                          QObject,
                          Qt,
                          Slot,
                          Signal, )

from qtpy.QtSql import (QSqlQuery)

# from PyQt.QtGui import ( QAction, QActionGroup, )

from qtpy.QtWidgets import ( QComboBox,
                             QLineEdit )

# ---- imports local -- then constants
from   app_global     import AppGlobal
# import data
import history_sync
import custom_widgets as cw

LOG_LEVEL           = 1    # higher is more
        # logging.log( LOG_LEVEL,  debug_msg, )
logger              = logging.getLogger( )


# watch out for trailing comma ins sql column names
STUFF_QUERY    = "SELECT id, name, title, descr   FROM stuff  WHERE id = :arg_id"
     # perhaps later can get from data dict

ALBUM_QUERY    = "SELECT id, name, cmnt  FROM photoshow  WHERE id = :arg_id"

PLANT_QUERY    = "SELECT id, name, latin_name,  add_kw, descr  FROM plant  WHERE id = :arg_id"

PLANTING_BED_QUERY = STUFF_QUERY



#--------------------------
class ModelSender( QObject ):
    """
    sender for KeyValueListModel
        not sure if we need
    """
    key_save        =  Signal()    # a signal not a method
    key_restore     =  Signal()
    #--------------------------
    def emit_key_save( self,   ):
        """
        a method, emits a signal
        """
        self.key_save.emit(   )

    #--------------------------
    def emit_key_restore( self,   ):
        """
        the box should restore the key, the
        model change is complete
        """
        self.key_restore.emit(   )

# --------------------------------------------------
class KeyValueListModel(QAbstractListModel):
    """
    create as singleton for each set of combo boxes see below
    this stores the data, but does not keep current
    selection info
    one model can serve multiple comboboxs
        A small 2-column model:
        column 0 = key (int) or None
        column 1 = value (str)

    we should be able to create once in mdi management and
    have it in charge of the signals
    """
    # -----------------------
    def __init__(self, sql,  parent = None ):
        super().__init__(parent)
        self.KEY_ROLE    = Qt.UserRole
        self.VALUE_ROLE  = Qt.UserRole + 1

        self._rows = [
            ( None, "<none>"),
        ]
        self.sender    = ModelSender()
        self.sql       = sql

    # -----------------------
    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._rows)

    # -----------------------
    def columnCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return 2

    # -----------------------
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()
        if row < 0 or row >= len(self._rows):
            return None

        key, value = self._rows[row]

        # For combo rendering, always provide the string value.
        if role in (Qt.DisplayRole, Qt.EditRole):
            return value

        # Always provide the integer key as user data.
        if role == self.KEY_ROLE:
            return key

        if role == self.VALUE_ROLE:
            return value

        # Optional: if a caller asks for "column-like" values by display role,
        # still allow access to both fields by QModelIndex column.

        if role == Qt.ToolTipRole:

            if col == 0:
                return f"key={key}"

            if col == 1:
                return f"value={value}"

        return None

    # -----------------------
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """
        what it says, read
        but more info might be good
        """
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if section == 0:
                return "key"
            if section == 1:
                return "value"
        return None

    # -----------------------
    def row_for_key( self, target_key):
        """
        given a key find the row
        if not found then try to select to get it
            -1 if not found
        """
        for row, (key, _value) in enumerate(self._rows):
            if key == target_key:
                return row

        ok   = self.select_row_for_key( target_key )

        # now it should work
        for row, (key, _value) in enumerate(self._rows):
            if key == target_key:
                return row

        return -1

    # -----------------------
    def select_row_for_key( self, target_key ):
        """
        find and add at end
            should have already down row_for_key and found missing

        """
        # #--------------------------
        # def topic_select(self, arg_id ):
        self.sender.emit_key_save()

        select_ok       = False
        logger          = logging.getLogger( )
        query = QSqlQuery( AppGlobal.qsql_db_access.db )

        query.prepare( self.sql )
        query.bindValue(":arg_id", target_key )

        if not query.exec_():
            msg = ( f"select_row_for_key error executing query:  {query.lastError().text()}" )
            logging.error(msg)
            return select_ok

        while query.next():
            topic     = f"{query.value(0)} {query.value(1)} {query.value(2)}"
            select_ok = True
            break  # only expect 1

        if select_ok:  # could be inside
            self.append_row( target_key, topic, )

        self.sender.emit_key_save()

        return  select_ok

    # -----------------------
    def append_row(self, key, value):
        """
        what it says, read
        """
        insert_row = len(self._rows)
        self.beginInsertRows(QModelIndex(), insert_row, insert_row)
        self._rows.append((key, value))
        self.endInsertRows()

    # -----------------------
    def prepend_row(self, key, value):
        """
        what it says, read
        """
        self.beginInsertRows(QModelIndex(), 0, 0)
        self._rows.insert(0, (key, value))
        self.endInsertRows()

#-------------------------------
class CQModelComboBox( QComboBox, cw.CQEditBase ):
    """
    starting code from chat
    may need to run a select for values not in dd

    """
    def __init__(self,
                 parent                 = None,
                 field_name             = None,
                 is_keep_prior_enabled  = None ):
        """ """
        # init both parents
        QLineEdit.__init__( self, None  )     # need arg ?

        cw.CQEditBase.__init__( self,
                        parent                  = parent,
                        field_name              = field_name,
                        is_keep_prior_enabled   = is_keep_prior_enabled )

        # debug_msg    = ( "say give each its own copy of index_to_key ... but could centralized ")
        # logging.log( LOG_LEVEL,  debug_msg, )



       #  self.key_wilst_mutating = None
       #  self.key_missing        = None    # set to a key while wating for it to be added
        #self.history_sync       = None
        self.kvl_model          = None      # model wehre i get my data set in connect

        # # others do this it might work for us with None
        # a_partial           = partial( self.do_ct_value, None )
        # self.ct_default     = a_partial
        # self.ct_prior       = self.do_ct_prior
        # may instead index to 0 or ...
        a_partial               = partial( self.set_value, a_value = "" )
        self.set_clear          = a_partial
        self.set_default        = a_partial

        if self.is_keep_prior_enabled:
            self.set_prior      = self.set_pass

        else:
            self.set_prior      = a_partial

        self.db_value       = None
            # value from the db, used in debugging

        # these should be the only functions we need -- !! check holdovers
        self.rec_to_edit    = self.rec_to_dict_edit
        self.edit_to_rec    = self.dict_edit_to_rec

    #----------------------------
    def rec_to_dict_edit( self, record, format = None ):
        """
        convert from record format to edit format
        this is more or less a prototype
        note that I know my own field_name
        set_prepped_data
        """
        self.debug_format   = format   # unhide the closure

        raw_data            = cw.get_rec_data( record, self.field_name )
        converted_data      = raw_data
        self.set_preped_data( converted_data )

        msg                 = f"rec_to_dict_edit set value {self.field_name =} {raw_data = }"
        logging.debug( msg )

        return converted_data

    #----------------------------
    def dict_edit_to_rec( self, record, format = None ):
        """
        convert from edit format to record format
        this is more or less a prototype
        will use field name, if record is not a record skip placing in
        record for debug
        """
        self.debug_format    = format  # should not be used for this type
        converted_data       = self.get_raw_data()

        msg         = f"dict_edit_to_rec {self.field_name = } {converted_data = }"
        logging.debug( msg )

        cw.set_rec_data( record, self.field_name, converted_data )

        return converted_data # debug only set above

    #----------------------------
    def set_preped_data( self, a_key, is_changed = None ):
        """
        new
            for now assume dict is ok
        """
        # # do i have the key?
        # if not a_key in self.widget_ext.combo_dict:
        #     # fix it
        #     self.index_valid    = False
        #     self.db_value       = a_key
        #     value_not_used      = self.widget_ext.get_info_for_id( a_key )
        #         # old comments may be some truth
        #             # this will update the dictionary and  call all the
        #             # tabs to refresh using some function
        #             # but this may need to know the ddl is invalid
        #             # which set in warning
        #             # update will be called later

        # else:

        #     self.set_selection_by_key( a_key )
        # self.set_selection_by_key( a_key )
        row     = self.kvl_model.row_for_key( a_key )
        self.setCurrentIndex( row )

    #----------------------------
    def get_raw_data( self, ):
        """'
        key should be correct type
        this actually should be the data to go back to the db
        """
        data    = self.currentData( Qt.UserRole )
        return data

    #---------------------------
    def update_dictionaryxxxx(self, just_warning = True ):
        """
        2 events, a warning to save the id and
        then telling the dict has change --
        but the index may not be valid -- as for
        a new record in the fetch process  -- how do we detect that
        """
        if just_warning:
            self.db_value       = self.get_value_by_index()   # probably same as  get_raw_data()
            self.index_valid    = False
        else:
            self.load_combo_box()
            self.index_valid    = True
            self.set_selection_by_key( self.db_value )

    #----------------------------
    @Slot( )
    def key_save( self, ):
        """
        the dictionary is about to be mutated but we assume
        for now the key will not be deleted if it is we should
        I guess make sure there is a null in it and use that
        a mutate could include an entire swap of the dict, managed
        the same way
        """
        self.saved_key    = self.currentData( self.kvl_model.KEY_ROLE )

    #----------------------------
    @Slot( )
    def key_restore( self, ):
        """
        the dictionary has been mutated so find the key ... index and
        put it back
        """
        if self.saved_key is not None:
            row = self.key_value_model.row_for_key( current_key_2 )
            self.setCurrentIndex( row )

    # --------------------------
    def get_value_by_indexxxx( self ):
        """
        but if index is invalid get our backup copy
        """
        if self.index_valid:
            index   = self.currentIndex()
            key     = self.index_to_key.get(index)
            value   = self.widget_ext.combo_dict.get(key)

        else:
            value   = self.db_value

        return value

    # --------------------------
    def get_index_by_keyxxx( self, key ):
        """ """
        ix     = self.key_to_ix.get( key, -1 )
        return ix

    # --------------------------
    def get_key_by_indexxxx( self, index = None ):
        """
        that is by the current index
        """
        if index is None:
            index     = self.currentIndex()

        key       = self.ix_to_key.get( index, None )
        #value = self.dict_data.get(key)
        debug_msg   = (f"get_key_by_index Selected key: {key}")
        logging.log( LOG_LEVEL,  debug_msg, )
        return key

    # # --------------------------
    # def get_index_by_key(self):
    #     """
    #     that is by the current index
    #     """


    #     #value = self.dict_data.get(key)
    #     debug_msg   = (f"get_key_by_index Selected key: {key}")
    #     logging.log( LOG_LEVEL,  debug_msg, )
    #     return key

    # --------------------------
    def set_selection_by_keyxxx( self, key ):
        """
        if we do not have the key and we have a history sync
        we will ask it to add it
        """
        ix     = self.get_index_by_key( key )

        # !! refactor
        if ix == -1:

            if self.history_sync:
                self.key_missing = key
                self.history_sync.add_item( key, history_sync.MISSING_VALUE )

        self.setCurrentIndex( ix )
                # self.label.setText(f"Selection Set to: {self.dict_data[key]}")

    # --------------------------
    def setPlaceholderText( self, ignoered ):
        """
        add missing method ??
        so we can call without harm """
        pass

    # --------------------------
    def connect_to_kvl_model( self, kvl_model ):
        """ """
        self.kvl_model   = kvl_model  # may be rudundant

        self.setModel( kvl_model )
        kvl_model.sender.key_save.connect(     self.key_save    )
        kvl_model.sender.key_restore.connect(  self.key_restore )

        #self.my_sender.post_mutate.connect( cq_dict_combo_box.post_mutate )


# # ---- in use
# # ---- plant_id  by hand id_in_old ---------------
#import custom_widgets_2 as cw_2
# edit_field                 = CQModelComboBox(
#                              field_name = "plant_id" )

# # self.in_album_widget   = edit_field
# kvl_model     = AppGlobal.mdi_management.get_key_value_list_model( "plant" )
# # could check have default values or do in get function better
# edit_field.connect_to_kvl_model( kvl_model )  # or other way around connect_widget

# ---- eof









