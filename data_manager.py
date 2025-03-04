#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bad name
make manager for a model with fields

"""
# ---- tof
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    main.main()
# --------------------
# ---- import
from PyQt5.QtSql import QSqlRecord
import logging

import info_about
import string_util
import key_words
import qsql_utils
import custom_widgets




logger              = logging.getLogger( )
LOG_LEVEL           = 5 # level for more debug    higher is more debugging    logging.log( LOG_LEVEL,  debug_msg, )

# may also be defined in base doc or somewher else this should be reconciled
RECORD_NULL         = 0
RECORD_FETCHED      = 1
RECORD_NEW          = 2
RECORD_DELETE       = 3

def get_rec_data( record, field_name  ):
    """
    from custom widgets, here for debug ... consider adding some stuff to info_about
    get data from the record unless record is the data
    rec = record
    field_name ignored of record is the data
    but to aid in debugging assume rec is the data if not a qrecord
    data      = get_rec_data( record, field_name )
    """
    if  isinstance( record, QSqlRecord ):

        if record.indexOf( field_name ) == -1:
            msg         = ( f"get_rec_data Field {field_name} "
                            f"does not exist in the record.")
            logging.error( msg )
            raise ValueError( msg )
            #rint( f"set_data_from_record {debug_fn}")
            #data       = record.value( field_name  )
            # msg        =  ( f"set_data_from_record {field_name} {data = }"
            #                 f" {self.db_type = }")
            # logging.debug( msg )
        # still need None !!
    else:
        return record    # take as value field_name does not matter

    # if here have a record with valid field_name
    raw_data        = record.value( field_name  )

    return raw_data

# ---------------------------------
class DataManager(   ):
    """
    model with single db record active at a time
    with gui that is list of custom edits
    extract from stuff then put back
    assumes option of key word update
    may emit some signals somehow
    debug
        self.table_name
    """
    def __init__(self, model ):
        """
        from creator
            self._build_model()
            self.data_manager      = data_manager.DataManager( self.model )
            self.data_manager..next_key_function = some_function( table_name )

        """
        self.model                  = model   # what kind of modeql QSqlTableModel
            # all set uup with db connect

        self.next_key_function      = None   # should take table_name  self.next_key_function( self.table_name )
            # note needed if key is generated externally
        self.table_name             = model.tableName()

        self.current_id             = None  # None only if we do not have an id
        self.current_record         = None  # valid .... when for history
                                            # want after record from criterial list and
                                            # want to update on save

        self.record_state           = RECORD_NULL

        # key word is up there in parent
        self.key_word_table_name    = ""        # set in init of child ??
        self.id_field               = None      # infered below
        self.field_list             = []        # all field involved in the update
            # see add_field
        self.key_word_field_list    = []        # list of edits containing key words
            # field need to hold string data
                # can build with gui

        self.topic_field_list       = []           # list of edits containing topic info

            # check that childred do not also implement this  ?? should this be here?
        self.enable_send_topic_update    = False

    # -------------------------------------
    def debug_to_log( self,   ):
        """
        what it says may change for different debug tasks
        """
        msg     = f"DataManager.debug_to_log_ do some error check ..."
        logging.error( msg )
        for i_field in self.field_list:
            if i_field.ct_prior is None:
                msg     = f"DataManager.debug_to_log_ Error {i_field.field_name = } {i_field.ct_default = } { i_field.ct_prior = }"
                logging.error( msg )


    # -------------------------------------
    def enable_key_words( self, key_word_table ):
        """
        support for the key word table
        """
        self.key_word_table_name    = key_word_table
        db                          = self.model.database()
        self.key_word_obj           = key_words.KeyWords(  key_word_table,  db )

    # -------------------------------------
    def add_field( self,
                  edit_field,
                  is_key_word = False,
                  is_topic    = False ):
        """
        a field on the form and in the record so to speak
        a field is some class from custom_widgets....
        """
        self.field_list.append( edit_field )
        if edit_field.field_name == "id":
            self.id_field  = edit_field

        if is_key_word:
            # debug_msg     = f"DataManager.add_field is_key_word  {edit_field.field_name  = }"
            # logging.debug( debug_msg )

            self.key_word_field_list.append( edit_field )

        if is_topic:
            self.topic_field_list.append( edit_field )

    # -------------------------------------
    def model_record_info( self,   ):
        """

        """
        model       = self.model
        msg         = ( f"model_record_info {self.table_name = }" )
        log_msg     = info_about.INFO_ABOUT.find_info_for(
                            model,
                            msg         = msg,
                            print_it    = False
                           )
        logging.debug( log_msg )

        return log_msg

    # -------------------------------------
    def have_updatable_edits_deprocated( self, log_it = False ):
        """
        this is mainly for debugging
        have_updates = self.have_updatable_edits( )
        if not have_updates:
                have_updates = self.have_updatable_edits( log_it = True )
                but moving away from is_changed as is unreliable/needed
        """
        have_updates     = False
        for i_field in self.field_list:
            if i_field.is_changed:
                have_updates   = True
            if log_it:
                msg       = ( f"have_updatable_edits for {i_field.field_name} {i_field.is_changed = }" )
                logging.info( msg )

        self.model_record_info()

        return have_updates

    # -------------------------------------
    def new_record( self, next_key = None, option = "default" ):
        """new_record
        looks a bit like default new row
        args
            next_key
            option       "default",  see clear_fields for options
                         "prior      use prior on edits

        """
        msg      = ( f"DataManager new_record    {self.table_name}  should we create the record here ??")
        logging.debug( msg )

        if next_key is None:
            next_key                = self.next_key_function( self.table_name )

        self.current_id             = next_key

        self.clear_fields( option   = option  )
        self.record_state           = RECORD_NEW

        # think we need to use custon_widget
        #self.id_field.setText( str( next_key ) )
        self.id_field.set_preped_data( str(next_key ),  )

        self.current_id             = next_key
        if self.key_word_table_name:
            self.key_word_obj.string_to_old( "" )

        msg     = ( f"DataManager new_record time stuff may be lost  {self.table_name = } ")
        logging.debug( msg )
        msg     = ( "new_record need to fix up the picture tab if any or does document do it ??")
        logging.debug( msg )

    # ---------------------------
    def select_record( self, id_value  ):
        """
        from russ crud  works
        move to photo_detail and modify
        then promote
        promoted   seems ok to be here
        """
        record   = None
        model    = self.model

                # debug
        if id_value:
            #ia_qt.q_sql_query_model( model, "select_record 1" )
            model.setFilter( f"id = {id_value}" )
            model.select()

            #ia_qt.q_sql_query_model( model, "select_record 2" )
            if model.rowCount() > 0:
                record                  = model.record(0)
                self.id_field.setText( str(record.value("id")) )
                self.record_to_field( record )
                #self.textField.setText(record.value("text_data"))
                self.record_state       = RECORD_FETCHED
                self.current_id         = id_value
                self.current_record     = record
            else:
                msg    = f"Record not found! {self.table_name } {id_value = }"
                logging.error( msg )

        if self.key_word_table_name:
            self.key_word_obj.string_to_old(( self.get_kw_string()) )
        # self.send_topic_update()

    # -----------------------------------------
    def update_db( self, ):
        """
        from russ crud was in phototexttab, probably universal
        might want to move key word stuff
        """
        if   self.record_state   == RECORD_NULL:
            msg      = ( f"update_db record null no action, return {self.table_name}")
            logging.debug( msg )
            return
            # if self.key_word_table_name:
            #     self.key_word_obj.string_to_new(( self.get_kw_string()) )

        elif  self.record_state   == RECORD_NEW:
            self.update_new_record()
            if self.key_word_table_name:
                self.key_word_obj.string_to_new(( self.get_kw_string()) )

        elif  self.record_state   == RECORD_FETCHED:
            self.update_record_fetched()
            if self.key_word_table_name:
                self.key_word_obj.string_to_new(( self.get_kw_string()) )

        elif  self.record_state   == RECORD_DELETE:
            self.delete_record_update()
            if self.key_word_table_name:
                self.key_word_obj.string_to_new( "" )

        else:
            msg     = ( f"update_db wtf  {self.record_state = } " )
            logging.error( msg )
            1/0

        if self.key_word_table_name:
            self.key_word_obj.compute_add_delete( self.current_id  )
        #rint( f"update_db record state now:  {self.record_state = } ")
        #rint( "what about other tabs and subtabs")

    # ---------------------------
    def update_record_fetched(self):
        """
        from russ crud  -- copied from PictureTextTab -- now promoted
        what are the fields
        key words done in update_db
        when i had problems with update i had several versions of this
            now in Ver 63: I will delted them look in old versions if you
            want that code
        """
        self.update_record_fetched_v3( )

    # ---------------------------
    def update_record_fetched_v3(self):
        """
        from russ crud  -- copied from PictureTextTab -- now promoted
        what are the fields
        key words done in update_db
        v3   adding another select -- this seems wrong -- if work look for other options
        this seems to work so go with it for now
        """
        debug_msg    = ( f"update_record_fetched  {self.record_state  = }"   )
        logging.log( LOG_LEVEL,  debug_msg, )

        model    = self.model      # QSqlTableModel(
        if not self.record_state  == RECORD_FETCHED:
            msg   = ( f"update_record_fetched_v3 bad_state, return  {self.record_state  = } {self.table_name = }")
            logging.error( msg )
            return

        id_value = self.id_field.text()
        if id_value:

            # msg    = ( "update_record_fetched_v3 ")
            # logging.debug( msg )
            #model.setFilter(f"id = {id_value}")
            #model.select()
            if model.rowCount() > 0:

                record = model.record( 0 )
                self.field_to_record(  record )
                model.setRecord( 0, record)  # model.setRecord(0, record) chat says required
                #model.submitAll()
                ok   = self.model_submit_all( model, f"DataManager.update_record_fetched_v1 {id_value = } {self.table_name = } ")
                model.select()
            else:
                1/0   # pretty poor
        else:
            1/0   # pretty poor
            #model.setFilter("")  # seems wrong

    # ---------------------------
    def update_new_record( self ):
        """
        when i had problems with update i had several versions of this
            now in Ver 63: I will delted them look in old versions if you
            want that code

        """
        #self.update_new_record_v2( )
        self.update_new_record_v3( )  # v3 works others sseem not to

    # --------------------------
    def update_new_record_v2( self ):
        """
        here lets
            change the filter
            add the record
            modify the record
            add modle_debug to model_submit_all

        """
        msg       = ( f"document_manager update_new_record_v2  {self.table_name  = } " )
        logging.debug( msg )

        model   = self.model     # QSqlTableModel(
        if not self.record_state  == RECORD_NEW:
            msg       = ( f"document_manager save_new_record bad state, return  {self.record_state  = } {self.table_name  = } ")
            logging.error( msg )
            return

        model.setFilter( "" )  # hope does not trigger a fetch
        msg    = info_about.INFO_ABOUT.find_info_for(
                        model,
                        msg             = "update_new_record_v2 after filter to empty",
                        max_len         = None,
                        xin             = "",
                        print_it        = False,
                        sty             = "",
                        include_dir     = False,  )

        logging.debug( msg )

        record  = model.record()   # type is QSqlRecord

        self.field_to_record( record )

        # ERROr just for debugging
        record.setValue( "add_kw", "data_for_add_kw" )

        msg      = "update_new_record_v2 prior to insertRecord {model.rowCount() = } "

        # seems key to modify record first then insert -- may want to look into someroe r
        # but seems like that was what id did in ver 1
        model.insertRecord( model.rowCount(), record )  # QSqlTableModel

        msg      = "update_new_record_v2 post to insertRecord {model.rowCount() = } "


        msg    = info_about.INFO_ABOUT.find_info_for(
                        record,
                        msg             = "update_new_record_v2 after field_to_record new record",
                        max_len         = None,
                        xin             = "",
                        print_it        = False,
                        sty             = "",
                        include_dir     = False,  )
        logging.debug( f"\n{msg}" )

        msg    = info_about.INFO_ABOUT.find_info_for(
                        model,
                        msg             = "update_new_record_v2 after field_to_record ",
                        max_len         = None,
                        xin             = "",
                        print_it        = False,
                        sty             = "",
                        include_dir     = False,  )

        logging.debug( msg )

        ok   = self.model_submit_all( model, f"DataManager.update_new_record { self.current_id = } {self.table_name = } {self.record_state = }")

        self.record_state    = RECORD_FETCHED
        # msg      =  f"New record saved! { self.current_id = } "
        # rint( msg )
        #QMessageBox.information(self, "Save New", msg )
        model.setFilter( f"id = {self.current_id}" )  # hope does not trigger a fetch
        msg    = "update_new_record_v2 at very end "
        #model_debug( model, msg )


    # ---------------------------
    def update_new_record_v3( self ):
        """
        like v2 but a bit different on filters
        here lets
            change the filter
            add the record
            modify the record
            add modle_debug to model_submit_all
        """
        debug_msg       = ( f"document_manager update_new_record_v3  {self.table_name  = } " )
        logging.log( LOG_LEVEL,  debug_msg, )

        model   = self.model     # QSqlTableModel(
        if not self.record_state  == RECORD_NEW:
            msg       = ( f"document_manager update_new_record_v3 bad state, return  {self.record_state  = } {self.table_name  = } ")
            logging.error( msg )
            return

        #model.setFilter( "" )  # hope does not trigger a fetch
        model.setFilter( f"id = {self.current_id}" )

        debug_msg    = info_about.INFO_ABOUT.find_info_for(
                        model,
                        msg             = "update_new_record_v3 after filter to empty",
                        max_len         = None,
                        xin             = "",
                        print_it        = False,
                        sty             = "",
                        include_dir     = False,  )
        logging.log( LOG_LEVEL,  debug_msg, )

        record  = model.record()   # type is QSqlRecord

        self.field_to_record( record )

        # ERROr just for debugging
        #record.setValue( "add_kw", "data_for_add_kw" )

        debug_msg      = "update_new_record_v3 prior to insertRecord {model.rowCount() = } "
        logging.log( LOG_LEVEL,  debug_msg, )
        # seems key to modify record first then insert -- may want to look into someroe r
        # but seems like that was what id did in ver 1
        model.insertRecord( model.rowCount(), record )  # QSqlTableModel

        debug_msg      = "update_new_record_v3 post to insertRecord {model.rowCount() = } "
        logging.log( LOG_LEVEL,  debug_msg, )

        ok   = self.model_submit_all( model, f"DataManager.update_new_record_v3 { self.current_id = } {self.table_name = } {self.record_state = }")

        self.record_state    = RECORD_FETCHED
        # msg      =  f"New record saved! { self.current_id = } "
        # rint( msg )
        #QMessageBox.information(self, "Save New", msg )
        model.setFilter( f"id = {self.current_id}" )  # hope does not trigger a fetch

        msg          = "update_new_record_v3 at very end "
        debug_msg    = ( f"\n{msg}" )
        logging.log( LOG_LEVEL,  debug_msg, )

    # ---------------------------
    def update_new_record_v1( self ):
        """
        now in data_manager
        from russ crud worked   --- from photo_text -- worked
        photo-detal ng need edit trying worked --- move to ancestor
        insert new record earliern??")
        ideas
            model.setFilter("")  or perhaps to the new record

        """
        msg       = ( f"document_manager update_new_record  {self.table_name  = } " )
        logging.debug( msg )

        # # and some more debugging
        # have_updates = self.have_updatable_edits( )
        # if not have_updates:
        #     have_updates = self.have_updatable_edits( log_it = True )
        #     breakpoint()     # debug remove

        model   = self.model     # QSqlTableModel(
        if not self.record_state  == RECORD_NEW:
            msg       = ( f"document_manager save_new_record bad state, return  {self.record_state  = } {self.table_name  = } ")
            logging.error( msg )
            return

        record  = model.record()   # type is QSqlRecord

        self.field_to_record( record )
        model.insertRecord( model.rowCount(), record )

        log_msg    = ( f"data_manager.DataManager update_new_record {model.isDirty()} = " )
        logging.debug( log_msg )

        msg         = ( f"data_manager.DataManager update_new_record {1 =}")
        log_msg      = info_about.INFO_ABOUT.find_info_for(
                            record,
                            msg         = msg,
                            print_it    = False,
                           )
        logging.debug( log_msg )

        ok   = self.model_submit_all( model, f"DataManager.update_new_record { self.current_id = } {self.table_name = } {self.record_state = }")

        self.record_state    = RECORD_FETCHED

    # ---------------
    def model_submit_all( self, model, msg ):
        """
        add a bit of error checking to submitAll()
        ok     = stuffdb_tabbed_sub_window.model_submit_all( model,  "we are here" )

        ok     = stuffdb_tabbed_sub_window.model_submit_all( model,  f"we are here {id = }" )
        """
        debug_on   = False
        # if model.tableName() == "help_text":
        #     debug_on   = True
        # wat_inspector.go(
        #      msg            = "model_submit_all pre-submit",
        #      # inspect_me     = self.people_model,
        #      a_locals       = locals(),
        #      a_globals      = globals(), )

        if debug_on:
            debug_msg    = (  f"\ndata_manager debug on model_submit_all  caller says {msg}" )
            logging.log( LOG_LEVEL,  debug_msg, )

            debug_msg    = info_about.INFO_ABOUT.find_info_for(
                            model,
                            msg             = f"model prior to submitAll {self.record_state = }",
                            max_len         = None,
                            xin             = "",
                            print_it        = False,
                            sty             = "",
                            include_dir     = False,  )
            logging.log( LOG_LEVEL,  debug_msg, )

        if model.submitAll():
            debug_msg = ( f"data_manager   model_submit_all submitAll ok: {msg}")
            #logging.debug( debug_msg )
            logging.log( LOG_LEVEL,  debug_msg, )
            ok   = True

        else:
            error = model.lastError()
            error_msg     = f"data_manager model_submit_all submitAll error: {msg}"
            logging.error( error_msg )

            error_msg     = ( f"error text: {error.text()}")
            logging.error( error_msg )

            msg         = ( f"model_submit_all error continued    " )
            log_msg     = info_about.INFO_ABOUT.find_info_for(
                                model,
                                msg         = msg,
                                print_it    = False
                               )
            logging.debug( log_msg )

            ok   = False

        # wat_inspector.go(
        #      msg            = "model_submit_all post-submit",
        #      # inspect_me     = self.people_model,
        #      a_locals       = locals(),
        #      a_globals      = globals(), )
        if debug_on:
            debug_msg    = (  f"\ndata_manager debug on model_submit_all  caller says {msg}" )
            logging.log( LOG_LEVEL,  debug_msg, )

            debug_msg    = info_about.INFO_ABOUT.find_info_for(
                            model,
                            msg             = f"ndata_manager debug_on model POST to submitAll {self.record_state = }",
                            max_len         = None,
                            xin             = "",
                            print_it        = False,
                            sty             = "",
                            include_dir     = False,  )
            logging.log( LOG_LEVEL,  debug_msg, )

        return ok

    # ---------------------------------------
    def validate( self, ):
        """
        validate all input, like accept text
        validations cause exceptions so return is not really required
        """
        is_bad   = False
        for i_field in  self.field_list:
            debug_field_name    = i_field.field_name
            is_bad    = i_field.is_field_valid()
            # if is_bad:
            #     break

        # msg     = f"validate do we need sub_tabs now in stuffdb_tabbed... validate.... {is_bad = } "
        # #AppGlobal.logger.info( msg )
        #rint( msg )
        #return is_bad

    # -------------------------------------
    def get_field_data( self, field_name   ):
        """ is used or implimented
        may want a good search method for now just a linear
        search -- may use some caching
        not tested
        """
        field   = None
        for i_field in self.field_list:
            if i_field.field_name  == field_name:
                field    = i_field
                break

        if field is None:
            msg     = f"get_field_data could not find field {field_name = } {self.table_name = }"
            logging.error( msg )
            1/0
            return ""
        data    = field.get_raw_data( )  # better be string
        return data

    # -------------------------------------
    def get_kw_string( self,   ):
        """
        get the fields contaning key words
        and concatinate into one string
        self.field_list.append( edit_field )
        """

        #rint( "get_kw_string" )
        a_str  = " "
        for i_edit in self.key_word_field_list:
            a_str    = a_str + " " + i_edit.get_raw_data()

        #rint( f"get_kw_string {a_str = }")
        return a_str

    # -------------------------------------
    def get_topic_string( self,   ):
        """
        get the fields defining topic for this record
        and build  into one string
        self.field_list.append( edit_field )
        """
        #rint( "get_topic_string" )
        a_str  = " "
        for i_edit in self.topic_field_list:
            a_str    = a_str + " " + i_edit.get_raw_data()

        msg     = f"get_topic_string {a_str =  } {self.table_name = }"
        logging.debug( msg )
        return a_str

    # -------------------------------------
    def delete_all( self,   ):
        """
        delete all under this id   current_id

        """
        msg    = "in datamanager delete all "
        logging.debug( msg )
        model  = self.model

        # Loop through the rows in reverse order and delete them
        for row in range(model.rowCount() - 1, -1, -1 ):
            model.removeRow(row)

        # tehee is no view here we are more like a form that we may need to clear self.view.show()

        if model.submitAll():
            model.select()  # Refresh the model to reflect changes in the view
        else:
            model.database().rollback()  # Rollback if submitAll fails
            msg     = ( f"data_manager submitAll fail rollback {self.table_name = }")
            logging.error( msg )
        for i_sub_tab in self.sub_tab_list:
            if i_sub_tab:
                i_sub_tab.delete_all()

    # ------------------------
    def record_to_field(self, record ):
        """
        promoted
        move data from fetched record into the correct fields
        """
        # ---- code_gen: detail_tab -- _record_to_field -- begin code
        for i_field in  self.field_list:
            #rint( f"********record_to_field {i_field.field_name}")
            # i_field.set_data_from_record( record )
            i_field.rec_to_edit( record, )  # format = None  hidden in closure

    # ------------------------
    def field_to_record( self, record ):
        """
        move data from the fields to the record
        name for qt5_by_example,  text_data for stuff
        <class 'PyQt5.QtSql.QSqlRecord'>
        """
        for i_field in  self.field_list:
            if ( i_field.field_name  == "text_data" ) and ( isinstance( i_field, custom_widgets.CQTextEdit ) ):
                debug_msg   = ( f"field_to_record {i_field.field_name = } " )
                logging.log( LOG_LEVEL,  debug_msg, )
                if  i_field.text_edit_ext_obj is not None:
                    i_field.text_edit_ext_obj.cache_current()

            # use if need breakpooint
            # if LOG_LEVEL >= 10:
            #     debug_msg   = ( f"field_to_record {i_field.field_name = } !! remove " )
            #     logging.log( LOG_LEVEL,  debug_msg, )
            #     if i_field.field_name in [ "text_data", "name"  ]:
            #         field_name    =  i_field.field_name
            #         # breakpoint()
            #         pass # for breakpoint

            # i_field.get_data_for_record( record, self.record_state  )
            i_field.edit_to_rec(  record,  )  # format is hidden

    # ------------------------
    def clear_fields( self, option ):
        """
        reset_fields or preset field might be better
        add from_prior here
        what it says, read
        what fields, need a bunch of rename here
        clear_fields  clear_fields  -- or is this default
        !! but should users be able to?? may need on add -- this may be defaults
        "default",
                   "prior   use prior on edits

        move option inside control with argument
        """
        if option == "default":
            for i_field in self.field_list:
               # i_field.clear_data( to_prior = to_prior )
               i_field.ct_default(  )

        elif option == "prior":
            for i_field in self.field_list:
                pass   # debug
                print( f"{i_field = } {i_field.ct_prior = }")
                i_field.ct_prior(  )

    # ------------------------------
    def __str__( self ):

        a_str   = ""
        a_str   = ">>>>>>>>>>* DataManager *<<<<<<<<<<<<"

        a_str   = string_util.to_columns( a_str, ["table_name",
                                           f"{self.table_name}" ] )


        a_str   = string_util.to_columns( a_str, ["current_id",
                                           f"{self.current_id}" ] )
        a_str   = string_util.to_columns( a_str, ["enable_send_topic_update",
                                           f"{self.enable_send_topic_update}" ] )

        # consider looping thru them
        a_str   = string_util.to_columns( a_str, ["field_list",
                                           f"{self.field_list}" ] )

        for i_field in self.field_list:
            a_str   = string_util.to_columns( a_str, ["    i_field",
                                               f"{i_field}" ] )

        a_str   = string_util.to_columns( a_str, ["id_field",
                                           f"{self.id_field}" ] )
        a_str   = string_util.to_columns( a_str, ["key_word_field_list",
                                           f"{self.key_word_field_list}" ] )

        a_str   = string_util.to_columns( a_str, ["topic_field_list",
                                           f"{self.topic_field_list}" ] )


        a_str   = string_util.to_columns( a_str, ["key_word_table_name",
                                           f"{self.key_word_table_name}" ] )
        a_str   = string_util.to_columns( a_str, ["model",
                                           f"{self.model}" ] )
        a_str   = string_util.to_columns( a_str, ["next_key_function",
                                           f"{self.next_key_function}" ] )
        a_str   = string_util.to_columns( a_str, ["record_state",
                                           f"{self.record_state}" ] )

        # a_str   = string_util.to_columns( a_str, ["table_name",
        #                                    f"{self.table_name}" ] )

        a_str   = string_util.to_columns( a_str, ["current_record",
                                           f"{self.current_record}" ] )

        a_str   = string_util.to_columns( a_str, ["key_word_obj",
                                           f"{self.key_word_obj}" ] )
        return a_str

        if self.key_word_table_name:
            a_str   = a_str  + str( self.key_word_obj )

        return a_str


# ---- eof