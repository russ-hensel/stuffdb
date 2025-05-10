#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=E221,E201,E202,C0325,E0611,W0201,W0612
"""



"""

# ---- tof
# --------------------
if __name__ == "__main__":
    import main
    main.main()
# --------------------

# ---- imports
import functools
import inspect
import logging
import pprint
import subprocess
from functools import partial
from pathlib import Path

import data_dict
import gui_qt_ext
import info_about
#import key_words
import string_util
import text_edit_ext
#import table_model
import wat_inspector
from app_global import AppGlobal
from PyQt5.QtCore import QDate, QModelIndex, Qt, QTimer, pyqtSlot
# ---- begin pyqt from import_qt.py
from PyQt5.QtGui import (QFont,
                         QIntValidator,
                         QStandardItem,
                         QStandardItemModel,
                         QTextCursor)

from PyQt5.QtSql import (QSqlDatabase,
                         QSqlQuery,
                         QSqlQueryModel,
                         QSqlRelation,
                         QSqlRelationalDelegate,
                         QSqlRelationalTableModel,
                         QSqlTableModel)
from PyQt5.QtWidgets import (QAction,
                             QActionGroup,
                             QApplication,
                             QButtonGroup,
                             QCheckBox,
                             QComboBox,
                             QDialog,
                             QDateEdit,
                             QDockWidget,
                             QFileDialog,
                             QFrame,
                             QGridLayout,
                             QHBoxLayout,
                             QHeaderView,
                             QInputDialog,
                             QLabel,
                             QLineEdit,
                             QListWidget,
                             QMainWindow,
                             QMdiArea,
                             QMdiSubWindow,
                             QMenu,
                             QMessageBox,
                             QPushButton,
                             QSpacerItem,
                             QSpinBox,
                             QSizePolicy,
                             QTableView,
                             QTableWidget,
                             QTableWidgetItem,
                             QTabWidget,
                             QTextEdit,
                             QVBoxLayout,
                             QWidget)

import custom_widgets as cw
import data_manager
import parameters
#import ex_qt
#import exec_qt
#import mdi_management
import picture_viewer

# ---- import end

FIF             = info_about.INFO_ABOUT.find_info_for

EXEC_RUNNER     = None  # setup below
# MARKER              = ">snip"

LOG_LEVEL       = 10    # higher is more

logger          = logging.getLogger( )

# make sure not dups maybe should be in data_manager
RECORD_NULL         = 0
RECORD_FETCHED      = 1
RECORD_NEW          = 2
RECORD_DELETE       = 3

WIDTH_MULP          = 8 # for some column widths

#   stuffdb_tabbed_sub_window.

RECORD_STATE_DICT   = { RECORD_NULL:    "RECORD_NULL",
                        RECORD_FETCHED: "RECORD_FETCHED",
                        RECORD_NEW:     "RECORD_NEW",
                        RECORD_DELETE:  "RECORD_DELETE",
                        }


# ---- open in idle
def open_python_file_in_idle( python_filename, ): # conda_env ):
    """

    open_python_file_in_idle_may_need_move_broken

    taken from clipboard Dec 2024
    we write and execute a shell script to do this

    currently if file does not exist it will be created

    return
        None

    """
    script_filename   =  "temp_idle_script.sh"  # first time around set to executable ??  add ./ ??
    conda_env         =  "py_12_misc"
    # script_path        = Path( script_filename )
    # script_path_abs    = script_path.absolute()

    # !!!!!!!!!!!!!!!!!!!!!! next seems missing look at help and old code
    sh_text            = open_in_idle_string( python_filename, conda_env  )

    with open( script_filename, 'w') as a_file: # a will append  w will overwrite
        a_file.write( sh_text )

    ret    =    subprocess.Popen( [ f"./{script_filename}",  ]   )

# --------------------------------
def model_submit_all( model, msg ):
    """
    add a bit of error checking to submitAll()
    ok     = stuffdb_tabbed_sub_window.model_submit_all( model,  "we are here" )

    ok     = stuffdb_tabbed_sub_window.model_submit_all( model,  f"we are here {id = }" )
    """
    debug_loc        = "model_submit_all"
    if model.submitAll():
        debug_msg        = f"{debug_loc} >>> {msg = }  "
        logging.error( debug_msg )   #logging.log( LOG_LEVEL,  debug_msg, )
        ok   = True

    else:
        error = model.lastError()
        error_msg     = f"{debug_loc}  error: {msg = }\n {error.text() = } "
        logging.error( error_msg )
        ok   = False

    return ok

#-------------------------
def build_pic_filename( *, file_name, sub_dir    ):
    """
    Returns:
        filename if exists else default from parameters
        perhaps fold into fix_pic_filename( filename   ):  !! ??
        file_name   = base_document_tabs.build_pic_filename( file_name, sub_dir )
                      base_document_tabs.build_pic_filename( file_name, sub_dir    )
        return None if fails
    """
    # for debugging may need this
    if type( sub_dir ) != str:
        msg    = "based_document_tabs build_pic_filename bad subdir look at self.ix_sub_dir"
        logging.error( msg )
        # import inspect  # for debug i
        # import logging
        debug_loc       = f"build_pic_filename"
        debug_msg       = f"{debug_loc} >>> bad subdir look at self.ix_sub_dir  {sub_dir = }"
        logging.error( debug_msg )

        return None

    root            = AppGlobal.parameters.picture_db_root

    if file_name == "":
        return None

    file_name       = file_name.strip()
    sub_dir         = sub_dir.strip()

    full_file_name  = f"{root}/{sub_dir}/{file_name}".replace( "\\", "/" )
    full_file_name  = full_file_name.replace( "///", "/" )
        # just in case we have dups !! this is crude
    full_file_name  = full_file_name.replace( "//", "/" )
        # just in case we have dups

    debug_msg       = f"build_pic_filename full_file_name build_pic_filename {full_file_name = }"
    logging.debug( debug_msg )

    return full_file_name

#-------------------------
def fix_pic_filename( filename   ):
    """
    Returns:
        filename if exists else default from parameters
        file_name   = base_document_tabs.fix_pic_filename( file_name )
    """
    ok   = True
    if filename is None:
        ok = False

    else:
        file_path       = Path( filename )
        ok              = file_path.exists()

    if not ok:
        filename   = AppGlobal.parameters.pic_nf_file_name

    return filename

#-----------------------------------
def is_delete_ok(   ):
    """
    Returns:
        is_ok
    if not base_document_tabs.is_delete_ok():
        return


    """
    msg_box = QMessageBox()
    msg_box.setWindowTitle("Your choice")
    msg_box.setText("Delete ok?")

    # Adding buttons
    choice_no  = msg_box.addButton("No - delete",  QMessageBox.ActionRole)
    choice_yes = msg_box.addButton("Yes - delete", QMessageBox.ActionRole)

    msg_box.setModal(True)

    msg_box.exec_()

    if   msg_box.clickedButton() == choice_no:
        is_ok      = False

    elif msg_box.clickedButton() == choice_yes:
        is_ok      = True

    return is_ok

# -------------------------------
def table_widget_no_edit( table_widget  ):
    """
    think makes all of a table widget non editable
    from chat
    take a table widget Q..... what  maybe descendants of abstract
    and make it non editable
    .... put this in examples
    """
    table = table_widget
    for row in range(table.rowCount()):
        for column in range(table.columnCount()):
            item = table.item(row, column)
            if item is not None:
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)


# -----------------------------------
class ReadOnlySqlTableModel( QSqlTableModel ):
    """
    from chat -- test me  use for list, something similar for history
    !! think not needed can disable all in view i think
    """
    def __init__(self, parent=None, db=None):
        """
        from chat
        """
        super(ReadOnlySqlTableModel, self).__init__(parent, db)

    # -----------------------
    def flags(self, index):
        """
        # Make all cells non-editable
        """
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

# ---- parent of all top level documents not the detail tab  ------------------------------------
# ----------------------------------------
class DocumentBase( QMdiSubWindow ):
    """
    """
    def __init__(self, instance_ix = 0 ):
        """
        This is the parent for the document
        It holds our tabs
        when a document is created it registers itself with what mdi...?
        """
        super().__init__()

        self.subwindow_name     = "DocumentBase -- subwindow failed to set"

        self.instance_ix        = instance_ix

        mdi_area                = AppGlobal.main_window.mdi_area
            #we could return the subwindow for parent to add
        sub_window              = self
            # sub_window.setWindowTitle( "this title may be replaced " )
        self.db                 = AppGlobal.qsql_db_access.db

        self.prior_tab          = 0
        self.current_tab        = 0

        self.prior_criteria     = None
        self.current_criteria   = None    # init just after criteria tab created

        # for testing, generalization and ability not to create -- promoted
        self.criteria_tab       = None
        self.list_tab           = None
        self.detail_tab         = None
        self.text_tab           = None
        # self.pseodo_text_tab    = None   # for a non visual text tab with a data manager
        #                                     # is just the data_manager
        #                                     # may be created in the detail tab
        self.history_tab        = None
        self.picture_tab        = None


        # these and tab references should be created by the particular document
        # this works only for non movable tabs
        self.criteria_tab_index     = None
        self.list_tab_index         = None
        self.detail_tab_index       = None
        self.text_tab_index         = None
        self.history_tab_index      = None
        self.picture_tab_index      = None   # does this ever exist

        self.mapper                 = None    # !! delete when sage
        self.help_filename          = "help_file_not_set.txt"

        self.detail_table_id        = None    # set in descendant
        self.current_id             = None    # same as above, !! delete one
            # probably should be deleted in favor of one in detail in data_manager
        self.detail_table_name      = None    # set in descendant
        self.menu_action_id         = None    # set by midi_management id the menu
        # self.record_state
        self.current_tab_index      = 0       # assumed to be criteria

        self.tab_folder             = QTabWidget() # create for descendants

        # may want to keep at end of this init
        AppGlobal.mdi_management.register_document(  self )
        self.tab_folder.currentChanged.connect( self.on_tab_changed )

    # --------------------------------
    def __init_2__( self ):
        """call at end of child __init__ """
        # !! perhaps in ancestor to a post innit
        title       = self.subwindow_name
        if self.instance_ix !=0:
            title  += f" {self.instance_ix}"

        self.setWindowTitle( title )
        AppGlobal.mdi_management.update_menu_item( self )
        self.set_size_pos()

    # --------------------------------
    def set_size_pos( self ):
        """
        run after tab is added??
        """
        debug_msg = ( "set_size_pos--------------------------------------  " )
        logging.debug( debug_msg )

        # # --- works but window is hidden
        # self.showMaximized()
        # self.show()

        # ---- next partly works
        # this is a bit crude a kluge for now
        my_parameters       = AppGlobal.parameters
        qt_xpos             = my_parameters.doc_qt_xpos
        qt_ypos             = my_parameters.doc_qt_ypos
        qt_width            = my_parameters.doc_qt_width
        qt_height           = my_parameters.doc_qt_height

        self.setGeometry(  qt_xpos,
                            qt_ypos ,
                            qt_width,
                            qt_height  )

    # --------------------------------
    def get_topic( self ):
        """
        of the detail record -- implemented in stuff in people not working
        """
        return "DocumentBase need override for topic in descendant"

    # --------------------------------
    def get_record_state( self ):
        """
        @ property did not work
        record_state
        can this happen prior to creation of detail_tab
        maybe that was the property error
        """
        debug_self_detail_tab   = self.detail_tab
        return self.detail_tab.record_state

    # --------------------------------
    def have_updatable_edits( self ):
        """
        for debug
        think meaningless
        """
        have_updatable_edits  = self.detail_tab.data_manager.have_updatable_edits( log_it = True )
        # logging should just happen

    # --------------------------------
    @property
    def record_state( self ):
        """
        of the detail record
        seems not to work, I will change/add get_record_state
        but i get AttributeError: 'StuffDocument' object has no attribute 'record_state'
        """
        return self.detail_tab.record_state

    # --------------------------------
    @property
    def window_title( self ):
        """
        """
        return self.windowTitle()

    # ---- events ---------------------------
    # ------------------------------------------
    def on_list_clicked( self, index: QModelIndex ):
        """
        this opens a detail item for the criteria list clicked
        Args:
            index (QModelIndex): DESCRIPTION.

        """
        row                     = index.row()
        column                  = index.column()

        # debug_msg  = ( "DocumentBase.on_list_clicked Stuff Clicked on list"
        #               f"  row {row}, column { column}  save first ??" )  # " value: {value}" )
        # logging.debug( debug_msg )
        self.list_tab.list_ix   = row  # do !! we need this ??

        self.set_list_to_detail_ix( row )

    # ------------------------------------------
    def on_list_double_clicked( self, index: QModelIndex ):
        """
        so promoted? -- or delete
        what it says, read

        Args:
            index (QModelIndex):  where clicked

        """
        row                 = index.row()
        column              = index.column()
        #rint( f"Clicked on row {row}, column {column}, value tbd" ) # " value: {value}" )

    #----------------------------
    def on_tab_changed(self, index):
        """
        will kick off criteria select if ...
        what it says, read it
        """
        # debug_msg   = ( "on_tab_changed need validate update db but may be"
        #                " redundant in some cases so perhaps provide a mechanism to skip" )
        # logging.debug( debug_msg )

        old_index                = self.current_tab_index
        self.current_tab_index   = index
        #self.tab_page_info()
        if old_index == 0 and index != 0:  # !=0 happens at construct
            self.criteria_tab.criteria_select_if( )

        if ( index == self.criteria_tab_index ) and ( self.criteria_tab.key_words_widget is not None   ):
            self.criteria_tab.key_words_widget.setFocus()

    # --------------------------------
    def closeEvent(self, event):
        """
        may not be complete -- for example pending updates
        """
        AppGlobal.mdi_management.forget_document(  self )
        self.on_close()
        event.accept()

    # --------------------------------
    @pyqtSlot()
    def on_close( self ):
        """
        """
        debug_msg  = (f"{self.windowTitle()} has been closed")
        logging.debug( debug_msg )

    # ---- subwindow interactions
    # -----------------------------
    def next_list_to_detail( self ):
        """
        based on code in python programming and development
        make into a delta and absolute like code somewhere else

        On the list tab, move from one list item to the next
        """
        tab                = self.list_tab
        new_list_ix        = tab.list_ix + 1
        self.set_list_to_detail_ix( new_list_ix )

    # -----------------------------
    def prior_list_to_detail( self ):
        """
        see next_list_to_detail
        """
        tab                = self.list_tab
        new_list_ix        = tab.list_ix - 1
        self.set_list_to_detail_ix( new_list_ix )

    # ------------------------------------------
    def set_list_to_detail_ix( self, new_list_ix   ):
        """
        navigate the list for prior and next and ....
        go to absolute index from the list tab
            update before moving
        consider second arg a delta -- that might eliminate the prior next but
        working now
        """
        self.update_db()    # why !! try remove

        tab                 = self.list_tab
        no_rows             = tab.list_model.rowCount()

        if no_rows < 1:
            debug_msg  = ( "set_list_to_detail_ix  may need to clear some stuff" )
            logging.debug( debug_msg )

        list_ix             = tab.list_ix

        if new_list_ix >= no_rows:
            new_list_ix  =  no_rows -1

        elif new_list_ix < 0:
            new_list_ix  =  0
            # debug_msg     = f"set_list_to_detail_ix new_
                # list_ix {no_rows = } {new_list_ix = } tired to index before start"
            # logging.debug( debug_msg )
        # else in range

        tab.list_ix     = new_list_ix
        self.list_tab.list_view.selectRow(  new_list_ix )
        record          = tab.list_model.record( tab.list_ix  )
        id_data         = record.value( "id")

        # debug_msg   = ( "set_list_to_detail_ix may be a function for this" )
        # logging.debug( debug_msg )

        self.select_record( id_data )

        record    = self.detail_tab.data_manager.current_record
        self.record_to_history_table( record )

    # -----------------------------
    def prior_history_to_detail( self ):
        """
        --- but why not do this from the select that is coming up
            just send the selected record
            and update when the save is done
            function can be record to history( record ) called on the history tab
        """
        history_tab    = self.history_tab
        list_ix        = history_tab.list_ix
        self.set_history_to_detail_ix( list_ix - 1 )

    # -----------------------------
    def next_history_to_detail( self ):
        """
        see prior_history_to_detail
        """
        history_tab    = self.history_tab
        list_ix        = history_tab.list_ix
        self.set_history_to_detail_ix( list_ix + 1 )

    # ------------------------------------------
    def set_history_to_detail_ix( self, new_list_ix   ):
        """
        see  set_list_to_detail_ix
        """
        # !! think about comment_in
        #self.update_db()
        msg     = f"set_history_to_detail_ix  {new_list_ix = } "
        logging.debug( msg )

        self.update_db()

        history_tab         = self.history_tab
        list_ix             = history_tab.list_ix
        history_table       = history_tab.history_table
        no_rows             = history_table.rowCount()

        if new_list_ix >= no_rows:
            new_list_ix  =  no_rows -1
            msg     = f"new_history_ix {no_rows = } {new_list_ix = } tried to index past end"
            logging.error( msg )

        elif new_list_ix < 0:
            new_list_ix  =  0
            debug_msg     = ( f"new_history_ix {no_rows = } {new_list_ix = } "
                              "tired to index before start" )
            logging.debug( debug_msg )

        # else in range
        ID_COL                  = 0
        history_tab.list_ix     = new_list_ix

        item                    = history_table.item( new_list_ix, ID_COL )
        id_data                 = int( item.text() )
        # id_index                =  history_table.index( new_list_ix, 0 )
        # id_data                 =  history_table.data( id_index, Qt.DisplayRole )
        debug_msg               = (  "next_history_to_detail  try to get db_"
                                    f"key { new_list_ix = },  {id_data = }" )
        logging.debug( debug_msg )

        history_tab.select_row( new_list_ix )

        self.select_record( id_data )

    # -----------------------------
    def add_copy( self,  ):
        """
        could use create default_new_row
        what it says
            this is for a new row on the window -- no save

        Returns:
            None.
        compare to   new_record
        """
        self.new_record( option = "prior" )

    # -----------------------------
    def add_default( self,  ):
        """
        could use create default_new_row
        what it says
            this is for a new row on the window -- no save
            fill with default
        Returns:
            None.
        compare to new_record
        """
        self.new_record( option = "default" )

    #-------------------------------------
    def new_record( self, option = "default" ):
        """
        looks promotable, lets try this is the promote
        was  ---- default_new_record  changing to crud code  new_record
        defaults values for a new row in the detail and the
        text tabs

        Changes state of detail and related tabs
        see option in detail
        args
            next_key
            option      "default",
                        "prior   use prior on edits

        """
        self.update_db()
        debug_msg   = ( "DocumentBase new_record first validate, then save, "
                        "wait for except then go on save removed ")
        logging.log( LOG_LEVEL,  debug_msg, )
        # self.validate()
        # self.update_db()

        # next key should come from the detail data_manager  we can let the
        # detail windows do this then get the key
        # next_key      = AppGlobal.key_gen.get_next_key( self.detail_table_name )
        debug_msg   = ( f"new_record change self.detail_tab.default_new_row( next_key ) " )
        logging.log( LOG_LEVEL,  debug_msg, )

        self.detail_tab.new_record( next_key = None, option = option )
        next_key  = self.detail_tab.data_manager.current_id

        if  self.text_tab is not None:  # using next key from above
            self.text_tab.new_record( next_key, option = option  )

    # ------------------------------------------
    def criteria_select( self, ):
        """
        uses info in criteria tab to build list in list tab
        uses info from 2 tabs
        """
        self.criteria_tab.criteria_select()

    # ------------------------------------------
    def delete( self, ):
        """
        links to main menu bar save  ... might want to delete but look around

        """
        if not is_delete_ok():
            return

        current_id   = self.detail_tab.data_manager.current_id
        debug_msg    = ( f"DocumentBase_delete is current.id ok {current_id} ")
        logging.debug( debug_msg )

        debug_msg    = ( "DocumentBase_delete.... the detail items and all "
                         "that depend on it need to complete and route to update_db ")
        logging.debug( debug_msg )

        debug_msg    = ( "DocumentBase_delete convert to loop?? !! may need "
                          "to check record state ")
        logging.debug( debug_msg )

        if self.detail_tab is not None:
            self.detail_tab.delete_all()

        if self.text_tab is not None:
            self.text_tab.delete_all()

        self.list_tab.delete_row_by_id( current_id )

        self.history_tab.delete_row_by_id( current_id )

        self.next_list_to_detail()  # and hope it works --- need tab shift?

                # if not perhaps stay on criteria or clear the detail ... to
                # be done

        #self.current_id     = None
        # self.record_state   = RECORD_DELETE   # this is in detail tab not here
        #self.record_state   = RECORD_NULL

        debug_msg     = f"DocumentBase_delete  done   for {self.subwindow_name = }"
        logging.debug( debug_msg )

    # --------------------------
    def update_db( self,   ):
        """
        also know as update -- update detail tab and text...
        include validation and stop if fails

        only this update_db should validate, the rest
        should assume this one has use self.validate to check all

        """
        try:
            is_bad   = self.validate( )

        except cw.ValidationIssue as an_except:
            msg     = an_except.args[0]
            #rint( f"{msg = }" )
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Input Issue")
            msg_box.setText( msg )
            choice_a = msg_box.addButton( "Ok", QMessageBox.ActionRole )
            msg_box.setModal( True )
            msg_box.exec_()

            return

        if self.detail_tab is not None:
            self.detail_tab.update_db()

        if self.text_tab is not None:
            self.text_tab.update_db()

        loc        = f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name} "
        debug_msg  = f"{loc} >>> for {self.subwindow_name = }"
        logging.debug( debug_msg )

    # ---------------------------------------
    def validate( self, ):
        """
        validate all input, like accept text
        return
            if validation error will throw an exception
            else none
        """
        # self.data_manager.validate(  )

        # if self.get_record_state() == RECORD_NULL:
        #     msg       =  ( "BaseDocument validate do not
        #    validate null records this may be unnecessary or redundant")
        #     AppGlobal.logger.info( msg )
        #     return

        if self.detail_tab is not None:
            self.detail_tab.validate()

        if self.text_tab is not None:
            self.text_tab.validate()

        msg     = f"Document Base   validate... done for {self.subwindow_name = }"
        AppGlobal.logger.info( msg )
        #rint( msg )

    # ---------------------------------------
    def fetch_row_by_id( self, a_id ):
        """
        promoted
        rename call, delete

        what it says, mostly focused on the detail tab
        some seem to go direct to document's select_record
        """
        self.select_record( a_id )

    # ---------------------------------------
    def select_record( self, a_id ):
        """
        what it says, mostly focused on the detail tab
        should be promoted from other tabs
        it look like this could cause an endless loop
        no the tabs have their own method this is ok
        what about photo --- well things do not have one photo except photo itself
        """
        debug_msg   = ( "base document select_record  first validate, "
                        "then save, wait for except then go on ?? ")
        logging.debug( debug_msg )

        self.detail_table_id     = a_id     # also need in new and delete
        self.detail_tab.select_record(  a_id )
            # probably a  stuffdb_tabbed_sub_window.DetailTabBase

        if self.text_tab is not None:
            self.text_tab.select_record(  a_id )

        # # print is this right can it be in detail
        # if self.pseodo_text_tab is not None:
        #     self.pseodo_text_tab.select_record(  a_id )

        if self.picture_tab is not None:
            self.picture_tab.select_record(  a_id )

        # self.detail_to_history()

        tab_folder     = self.tab_folder  #  QTabWidget
        current_ix     = tab_folder.currentIndex()
        if current_ix not in [ self.detail_tab_index, self.text_tab_index, self.picture_tab_index, ]:
            tab_folder.setCurrentIndex( self.detail_tab_index )

    # --------
    def popup_delete_question( self ):
        """
        Generate a popup -- see message
        consider add more info later
        """
        msgbox      =  QMessageBox()
        msgbox.setWindowTitle("Confirm Delete")
        msgbox.setIcon( QMessageBox.Warning)
        msgbox.setText("Do you want to Delete this Record")
        botonyes =  QPushButton("Yes")
        msgbox.addButton(botonyes, QMessageBox.YesRole)
        botonno =  QPushButton("No")
        msgbox.addButton(botonno, QMessageBox.NoRole)
        msgbox.exec_()
        if msgbox.clickedButton() == botonno:
            return False
        else:
            return True

    # ---------------------------------------
    def record_to_history_table( self, record  ):
        """
        what it says, mostly focused on the detail tab
        """
        self.history_tab.record_to_table( record )

    # ---------------------------------------
    def search_me( self, criteria ):
        """
        externally driven search perhaps from text
        need to add what type of document
        """
        msg     = ( f"base document search_me {criteria = }")
        logging.debug( msg )
        self.criteria_tab.search_me( criteria )

    # ------------------------
    def prior_next_picture( self, delta ):
        """
        largely for the Album Picture Tab to navigate from
        this tab  -- promote??
        """
        # if self.photos_tab:
        #     return self.photos_tab.prior_next( delta )
        return   self.detail_tab.prior_next_picture( delta )

    # ------------------------------------------
    def doc_str( self, ):
        """
        links to main menu bar

        """
        print( f"self = {self}")

    # ------------------------------------------
    def tab_str( self, ):
        """
        links to main menu bar

        """
        msg     = ( f"tab_str not implemented yet {self}")
        logging.error( msg )

    # ------------------------------------------
    def data_manager_inspect( self, ):
        """
        links to main menu bar for debug
        """
        debug_msg   = ( f"data_manager_inspect will call debug_to_log  ")
        logging.debug( debug_msg )
        # make some locals for inspection
        # self_detail_tab         = self.detail_tab
        # self_text_tab           = self.text_tab
        # self_detail_table_name  = self.detail_table_name
        # parent_window = self.parent( ).parent( ).parent().parent()

        self.detail_tab.data_manager.debug_to_log()

    # ------------------------------------------
    def doc_wat_inspect( self, ):
        """
        links to main menu bar for debug
        """
        debug_msg    = ( f"doc_inspect may want to add to  {self}")
        logging.debug( debug_msg )
        # make some locals for inspection
        self_detail_tab         = self.detail_tab
        self_text_tab           = self.text_tab
        self_detail_table_name  = self.detail_table_name
        # parent_window = self.parent( ).parent( ).parent().parent()

        todo = """
        self.criteria_tab       = None
        self.list_tab           = None
        self.detail_tab         = None
        self.text_tab           = None
        self.history_tab        = None
        self.picture_tab        = None
        self.criteria_tab_index = None
        self.mapper             = None"""

        wat_inspector.go(
             msg            = "inspect !! more locals would be nice ",
             # inspect_me     = self.people_model,
             a_locals       = locals(),
             a_globals      = globals(), )

    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = "\n>>>>>>>>>>* DocumentBase  *<<<<<<<<<<<<"

        a_str   = string_util.to_columns( a_str, ["criteria_tab",
                                            f"{self.criteria_tab}" ] )
        # a_str   = string_util.to_columns( a_str, ["criteria_tab_index",
        #                                    f"{self.criteria_tab_index}" ] )
        # a_str   = string_util.to_columns( a_str, ["current_id",
        #                                    f"{self.current_id}" ] )
        # a_str   = string_util.to_columns( a_str, ["current_tab_index",
        #                                    f"{self.current_tab_index}" ] )
        a_str   = string_util.to_columns( a_str, ["detail_tab",
                                            f"{self.detail_tab}" ] )
        # a_str   = string_util.to_columns( a_str, ["detail_table_id",
        #                                    f"{self.detail_table_id}" ] )
        # a_str   = string_util.to_columns( a_str, ["detail_table_name",
        #                                    f"{self.detail_table_name}" ] )
        # a_str   = string_util.to_columns( a_str, ["history_tab",
        #                                    f"{self.history_tab}" ] )
        # a_str   = string_util.to_columns( a_str, ["list_tab",
        #                                    f"{self.list_tab}" ] )
        # # a_str   = string_util.to_columns( a_str, ["mapper",
        # #                                    f"{self.mapper}" ] )
        # a_str   = string_util.to_columns( a_str, ["menu_action_id",
        #                                    f"{self.menu_action_id}" ] )
        # a_str   = string_util.to_columns( a_str, ["picture_tab",
        #                                    f"{self.picture_tab}" ] )
        # a_str   = string_util.to_columns( a_str, ["subwindow_name",
        #                                    f"{self.subwindow_name}" ] )
        # a_str   = string_util.to_columns( a_str, ["tab_folder",
        #                                    f"{self.tab_folder}" ] )
        a_str   = string_util.to_columns( a_str, ["text_tab",
                                            f"{self.text_tab}" ] )

        # b_str   = self.super().__str__( self )
        # a_str   = a_str + "\n" + b_str

        return a_str

# ----------------------------------------
class DetailTabBase( QWidget ):
    """
    used for detail tabs and.....
    """
    def __init__(self, parent_window ):
        """
        lots of variable may not be used .... clean up later
        """
        # debug_msg  = ( "init  DetailTabBase  " )
        # logging.log( LOG_LEVEL,  debug_msg, )

        super().__init__( parent_window )

        self.parent_window       = parent_window

        self.viewer              = None   # tab may add
        self.add_ts              = None   # may only be valid for new

        # tab for a list of photos
        #self.sub_tab_list        = []        # will be called on select
              # and delete with our id here  self.sub_tab_list.append()   or parent_window.    ......
        self.tab_name            = "DetailTabBase -- >> tab failed to set<<< and... "
        # self.field_list          = []  # may not be used, but will be checked
            # check that children do not also implement this
        self.enable_send_topic_update    = False

        #self.mapper               = None
        self.picture_sub_tab      = None     # in case there is none

        #self.picture_sub_tab      = None   # but usually update in descendant
        # or could create and append on demand in the detail window
        # self.picture_sub_tab     = None

        # ----
        # next not right for text windows -- is not need there its own in init?
        self.table              = parent_window.detail_table_name
        self.table_name         = self.table   # !! eliminate one or other
        self.sub_tab_list       = []
        self.topic_edits        = []
            # the edits use for topics  probably tuples that need sorting

        self.pseodo_text_tab    = None    # may create, a data_manager in place of text_tab

        debug_msg    = ( f"init end DetailTabBase {self.tab_name}  " )
        logging.debug( debug_msg )

    # ---------
    def post_init(self, ):
        """
        call from child at the end of its init
        __init__ continued
        self.key_word_table_name: set to "" to suppress
        better text have own tab ?

        this build the standard detail db interface prior to
        building the gui which is next
        """
        debug_msg   = ( f"post_init DetailTabBase  {self.tab_name}  " )
        logging.debug( debug_msg )

        model                   = QSqlTableModel(
                                      self, AppGlobal.qsql_db_access.db )

        self.model              = model
        self.tab_model          = model

        model.setTable( self.table )

        self.data_manager                       = data_manager.DataManager( self.model )
        self.data_manager.next_key_function     = AppGlobal.key_gen.get_next_key
                # a_key_gen               = key_gen.KeyGenerator( a_qsql_db_access.db  )
                    #  AppGlobal.qsql_db_access.db
                # AppGlobal.key_gen       = a_key_gen.key_gen
                    # some_function( table_name )
        if self.key_word_table_name != "":
            self.data_manager.enable_key_words( self.key_word_table_name )

        #rint( f"post_init  end off to self._build_gui() DetailTabBase  {self.tab_name  }" )
        #rint( f"my data manager for {self.tab_name} \n{self.data_manager}")

        self._build_gui()

    #---------------------------------
    def _build_fields_from_dict( self, layout ):
        """
        What it says, read
            this is data dict driven code
            not in use was a proof of concept -- for now code gen plus tweak
            deleted look in old code to see
            deleted version now throws errors
        """

        # # ---- id
        # edit_field                  = cw.CQLineEdit(
        #                                         parent         = None,
        #                                         field_name     = "id",
        #                                         db_type        = "integer",
        #                                         display_type   = "string" )
        # self.id_field               = edit_field
        # edit_field.setPlaceholderText( "id" )
        # # edit_field.default_value    = 999 does not work
        # default_func               = partial( edit_field.do_ct_value, -99 )
        # edit_field.ct_default      = default_func
        # self.data_manager.add_field( edit_field )
        # layout.addWidget( edit_field )

        # column_list    = data_dict.DATA_DICT.get_table( self.table_name ).get_detail_columns(    )
        # for i_column in column_list:
        #     edit_field               = i_column.detail_edit_class(
        #                                                     parent         = None,
        #                                                     field_name     = i_column.column_name,
        #                                                     db_type        = i_column.edit_in_type,
        #                                                     display_type   = i_column.display_type,  )

        #     edit_field.setPlaceholderText( i_column.column_name )
        #     self.data_manager.add_field( edit_field )
        #     layout.addWidget( edit_field )

    # -----------------------------------------
    def update_db( self, ):
        """
        from russ crud was in phototexttab, probably universal
        """
        self.data_manager.update_db()

        if self.pseodo_text_tab is not None:  # a data_manager
            self.pseodo_text_tab.update_db()

        for i_tab in self.sub_tab_list:
            i_tab.update_db()

    # ---------------------------------------
    def validate( self, ):
        """
        validate all input, like accept text
        validations cause exceptions so return is not really required
        """
        self.data_manager.validate()

    # -------------------------------------
    def delete_all( self,   ):
        """
        delete all under this id   current_id

        """
        debug_msg   = ( "in stuffdb tab delete all ")
        logging.debug( debug_msg )

        self.data_manager.delete_all()
        # model  = self.tab_model



        # for i_sub_tab in self.sub_tab_list:
        #     if i_sub_tab:
        #         i_sub_tab.delete_all()

    # -------------------------------------
    def new_record( self, next_key, option = "default" ):
        """
        looks a bit like default new row
        args
            next_key
            option       "default",
                         "prior   use prior on edits
            normally next_key = None so data manager generates it

        """
        debug_msg = ( f"Detail_Tab_Base new_record {next_key = }   {option =} update.db")
        logging.log( LOG_LEVEL,  debug_msg, )
        # self.update.db()
        self.data_manager.new_record( next_key, option = option )

        next_key     = self.data_manager.current_id
        if self.pseodo_text_tab is not None:
            # self.pseodo_text_tab.clear_fields( option = "default" )
            self.pseodo_text_tab.new_record( next_key, option = option )

        debug_msg = ( f"Detail_Tab_Base clear out sub tabs?? !!")
        logging.log( LOG_LEVEL,  debug_msg, )

        # on an add we can select by id to clear them out and perhaps set a filter
        # use one of self.picture_i_tabsub_tabself.sub_tab_list       = []
        for i_tab in self.sub_tab_list:
            i_tab.select_by_id( next_key )  # key will not exist

    # ---------------------------
    def post_select_record( self, id_value  ):
        """
        some tweaking after a select, may need similar thing
        for update_db
        probably only implemented in descendant
        """
        pass

    # ---------------------------
    def select_record( self, id_value  ):
        """
        from russ crud  works

        """
        self.data_manager.select_record( id_value )

        if self.pseodo_text_tab is not None:
            self.pseodo_text_tab.select_record( id_value )

        for i_sub_tab in self.sub_tab_list:
            if i_sub_tab:
                i_sub_tab.select_by_id( id_value )

        self.send_topic_update()

    # ----------------------------
    def fetch_detail_row( self,  a_id = None ):
        """
        Args:
            id can be external or as chat has it fetched

        Returns:
            None.
        !!  promoted check does not exist in other tabs
                and is it ever called
        """
        a_id      = self.id_field.text()
        msg       = (  f"fetch_detail_row { a_id = }")
        logging.debug( msg )

        self.fetch_detail_row_by_id( a_id )

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
        self.data_manager.clear_fields( option = option)

        if self.pseodo_text_tab is not None:
            self.pseodo_text_tab.clear_fields( option = option)

    # -----------------------------------
    def send_topic_update( self, ):
        """
        topics are perhaps better as subjects
        called from select_record and perhaps other
        override, detail tab
        """
        msg     = ( "send_topic_update needs fixing !! just re-enabled ")
        logging.error( msg )
        # return
        debug_msg   = ( f" send_topic_update  <<<<<<<<<{ self.tab_name = } "
                         f" <<<<<<<<<<<<<<<<<<<< { self.enable_send_topic_update = } " )
        logging.debug( debug_msg )

        # AppGlobal.mdi_management.send_topic_update(
        #      table = self.table_name,  table_id = self.current_id, info = self.parent_window.topic )
        if self.enable_send_topic_update:

            send_signals = AppGlobal.mdi_management.send_signals
            #pic_subject = PicSubject()
            #mdi.send_topic_update("photo_table", 101, {"description": "Updated photo"})
            current_id    = self.data_manager.current_id
            send_signals.send_topic_update(
                #table = self.table_name,  table_id = self.current_id, info = self.parent_window.topic )
                table = self.table_name,  table_id = current_id, info = "topic info na" )

    # ------------------------
    def prior_next_picture( self, delta ):
        """
        largely for the Album Picture Tab to navigate from
        this tab  -- promote??
        """
        if self.pictures_tab:
            return self.pictures_tab.prior_next( delta )

    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = "\n>>>>>>>>>>* DetailTabBase *<<<<<<<<<<<<"

        # a_str   = string_util.to_columns( a_str, ["add_ts",
        #                                    f"{self.add_ts}" ] )
        # a_str   = string_util.to_columns( a_str, ["current_id",
        #                                    f"{self.current_id}" ] )
        # a_str   = string_util.to_columns( a_str, ["deleted_record_id",
        #                                    f"{self.deleted_record_id}" ] )
        a_str   = string_util.to_columns( a_str, ["enable_send_topic_update",
                                           f"{self.enable_send_topic_update}" ] )
        # a_str   = string_util.to_columns( a_str, ["field_list",
        #                                    f"{self.field_list}" ] )
        # a_str   = string_util.to_columns( a_str, ["key_word_edit_list",
        #                                    f"{self.key_word_edit_list}" ] )
        # a_str   = string_util.to_columns( a_str, ["key_word_obj",
        #                                    f"{self.key_word_obj}" ] )
        # a_str   = string_util.to_columns( a_str, ["key_word_table_name",
        #                                    f"{self.key_word_table_name}" ] )
        # a_str   = string_util.to_columns( a_str, ["mapper",
        #                                    f"{self.mapper}" ] )
        a_str   = string_util.to_columns( a_str, ["parent_window",
                                           f"{self.parent_window}" ] )
        a_str   = string_util.to_columns( a_str, ["picture_sub_tab",
                                           f"{self.picture_sub_tab}" ] )
        a_str   = string_util.to_columns( a_str, ["pictures_sub_tab",
                                           f"{self.pictures_sub_tab}" ] )
        # a_str   = string_util.to_columns( a_str, ["record_state",
        #                                    f"{self.record_state}" ] )
        a_str   = string_util.to_columns( a_str, ["sub_tab_list",
                                           f"{self.sub_tab_list}" ] )
        a_str   = string_util.to_columns( a_str, ["tab_name",
                                           f"{self.tab_name}" ] )
        a_str   = string_util.to_columns( a_str, ["viewer",
                                           f"{self.viewer}" ] )
        return a_str

# ----------------------------------------
class ListTabBase( DetailTabBase ):
    """
    parent for list tabs
    how much of DetailTabBase is used perhaps go back to widget

    """
    def __init__(self, parent_window ):
        """
        use in
            list tab for almost anything

        """
        super().__init__( parent_window  )
        #self.list_ix            = 5

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says, read
        !! placeingrid should come out
        """
        page            = self

        # a_notebook.addTab( page, 'Channels ' )
        placer          = gui_qt_ext.PlaceInGrid(
            central_widget=page,
            a_max=0,
            by_rows=False  )

        # Set up the model
        model_class         = QSqlTableModel
        model_class         = ReadOnlySqlTableModel
        model               = model_class(
                                 self, self.parent_window.db )
        self.list_model     = model   # but changed by the criteria_tab

        model.setTable( self.parent_window.detail_table_name )

        model.setEditStrategy( QSqlTableModel.OnManualSubmit )

        # ----view
        view                 = QTableView()
        view.horizontalHeader().setSectionResizeMode( QHeaderView.Interactive )

        # Use QHeaderView.Interactive to allow manual column width adjustments.
        # Avoid using QHeaderView.Stretch or QHeaderView.ResizeToContents

        self.list_view       = view     # consider change to just self.view\
        view.setSelectionBehavior( QTableView.SelectRows )
        view.setModel( model )
        placer.place(  view )
        view.clicked.connect( self.parent_window.on_list_clicked )

        # !! next is too much  col_head_order
        columns          = data_dict.DATA_DICT.get_list_columns( self.parent_window.detail_table_name )
        col_head_texts   = [  ]  # plus one for sequence
        col_names        = [  ]
        col_head_widths  = [  ]
        for i_column in columns:
            col_names.append(        i_column.column_name  )
            col_head_texts.append(   i_column.col_head_text  )
            col_head_widths.append(  i_column.col_head_width  )

        # !! better done in on loop over columns, do not need the lists
        for ix_col, i_text in enumerate( col_head_texts ):
            #rint( f" {ix_col = } { i_text = }")
            model.setHeaderData( ix_col, Qt.Horizontal,  i_text )

        # ?? look around fro redundancy
        for ix_col, i_width in enumerate( col_head_widths ):
            #rint( f" {ix_col = } { i_width = }")
            view.setColumnWidth( ix_col, i_width * WIDTH_MULP )

    #-------------------------------
    def delete_row_by_id ( self, id_to_delete ):
        """
        called after a record delete perhaps from document
        seems best of redoing the select
        """
        model           = self.list_model

        debug_msg       = ( "ListTabBase_delete_row_by_id end gonna just"
                            f" do a criteria_select  {model.rowCount() = } ).")
        logging.log( LOG_LEVEL,  debug_msg, )

        self.parent_window.criteria_tab.criteria_select()

        debug_msg  = (  "ListTabBase_delete_row_by_id Deletion loop_"
                       f"complete (in model only id = {id_to_delete} ).")
        logging.log( LOG_LEVEL,  debug_msg, )

    #-------------------------------
    def delete_row_by_id_without_updatexxxxx( self, id_to_delete ):
        """called after a record delete perhaps from document
        full of chat tries and retries

        """
           # Iterate from bottom to top to avoid shifting row indices

        model    = self.list_model

        #print(f"Is model editable? {model.isReadOnly()}")
            # Should print False see next

        debug_msg  = (  "ListTabBase_delete_row_by_id begin  "
                       f"{model.rowCount() = } {model.isReadOnly() = }")
        logging.log( LOG_LEVEL,  debug_msg, )

        for row in reversed(range(model.rowCount())):
            id_index = model.index(row, model.fieldIndex("id"))
            if model.data(id_index) == id_to_delete:
                debug_msg  = ( "ListTabBase_delete_row_by_id Deleting "
                               f"row with id = {id_to_delete} at row {row}")
                logging.log( LOG_LEVEL, debug_msg, )

                #model.removeRow(row)  # but row still there according to chat
                    #or try rows
                if model.removeRows(row, 1):
                    model.layoutChanged.emit()
                    print( "ListTabBase_delete_row_by_id Row count"
                           f" after removeRows: {model.rowCount()}")
                else:
                    print("ListTabBase_delete_row_by_id Failed to remove row.")



                model.rowsRemoved.emit( QModelIndex(), row, row)
                model.layoutChanged.emit()
                # # next to refresh -- but is probably wrong from chat
                # topLeft         = model.index(row, 0)
                # bottomRight     = model.index(row, model.columnCount() - 1)
                # model.dataChanged.emit( topLeft, bottomRight )


        debug_msg  = ( f"ListTabBase_delete_row_by_id end  {model.rowCount() = } ).")
        logging.log( LOG_LEVEL,  debug_msg, )

        debug_msg  = (  "ListTabBase_delete_row_by_id Deletion loop_complete"
                       f" (in model only id = {id_to_delete} ).")
        logging.log( LOG_LEVEL,  debug_msg, )

# ----------------------------------------
class SubTabBase( QWidget ):
    """
    used for detail many sub tabs but some like text and picture may be special
    """
    def __init__(self, parent_window ):
        """
        use in
            moving to stuff event
            PictureSubjectSubTab( stuffdb_tabbed_sub_window.StuffdbSubTabTab ):
        """
        super().__init__()
        self.parent_window  = parent_window

        self.db             = AppGlobal.qsql_db_access.db

        #self.table_name      = self.parent_window.table_name  --- no this is photo
        self.field_dict     = None   # set in descendant
        self.current_id     = None

        debug_msg  = ( "in SubTabBase  tab appends to a window list is this correct?? -- maybe ")
        logging.debug( debug_msg )

        self.parent_window.sub_tab_list.append( self )    # a function might be better
        self.current_id      = None  # probably get from somewhere else ??

    # -----------------------
    def update_db( self,    ):
        """
        for debugging

        do not need key generation on new
        model               = QSqlTableModel( self, self.db )
        model_indexer       = table_model.ModelIndexer( model )
        self.model_indexer  = model_indexer

        self.model_subject  = model
        """
        debug_msg   = ( "update_db  SubTabBase this simple? db commit here?? ")
        logging.debug( debug_msg )

        model       =  self.model  # QSqlTableModel
        model.submitAll()
        self.db.commit()

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says, read
        """
        page                = self

        layout              = QVBoxLayout( page )
        button_layout       = QHBoxLayout()

        layout.addLayout( button_layout )

        # Set up the view
        view                 = QTableView()
        model                = self.model
        #self.list_view       = view
        self.view            = view
        view.setModel( self.model )

        ix_col = -1   # could make loop or even list comp
        for i_column_name, col_dict in self.field_dict.items():
            ix_col    += 1

            model.setHeaderData( ix_col, Qt.Horizontal, col_dict[ "col_head_text"  ] )
            view.setColumnWidth( ix_col,                col_dict[ "col_head_width" ] )

        layout.addWidget( view )

        # ---- buttons
        widget        = QPushButton( 'Add' )
        widget.clicked.connect( self.add )
        button_layout.addWidget( widget )

        #
        widget        = QPushButton( 'Edit')
        widget.clicked.connect( self.edit_selected_record )
        button_layout.addWidget( widget )

        #
        widget        = QPushButton('Delete')
        widget.clicked.connect(self.delete_record)
        button_layout.addWidget( widget )

    # ------------------------------------------
    def _build_dialog( self, ):
        """
        what it says, read
        """
        1/0 # implement in desceanat

    # ---------------------------------------
    def select_by_id( self, a_id ):
        """
        maybe make ancestor and promote
        """
        1/0  # in descendant
        # model               = self.model

        # self.current_id     = id
        # model.setFilter( f"people_id = {a_id}" )  # for stuff_event
        # # model_write.setFilter( f"pictureshow_id = {id} " )
        # model.select()

    # -------------------------------------
    def default_new_rowxxxxx( self ):
        """tail_tab.default_new_row( next_key )
        default values for a new row in the detail and the
        text tabs

        Returns:
            None.

        """
        next_key      = AppGlobal.key_gen.get_next_key(
                                  self.detail_table_name )
        self.detail_tab.default_new_row( next_key )
        self.text_tab.default_new_row(   next_key )

    #---------------- restart here model view dialog name
    #  ---- chat functions
    def add(self):
        """
        Open dialog to add a new event and insert it into the model.
        """
        dialog      = self._build_dialog( edit_data = None )
        model       = self.model

        if dialog.exec_() == QDialog.Accepted:
            form_data   = dialog.get_form_data()

            # Create a new record
            row         = self.model.rowCount()
            self.model.insertRow(row)

            model.non_editable_columns  = { 99 } # beyond all columns -- delete soon

            self.fix_add_keys( form_data )  # mutable dict so no return needed.

            ix_col = -1   # could make loop or even list comp
            for i_column_name, col_dict in self.field_dict.items():
                try:  # if we do not have all fields will get key errors
                    ix_col    += 1
                    model.setData( model.index( row, ix_col ), form_data[ i_column_name ] )
                except KeyError as error:
                    # if we do not want to do all fields
                    error_message = str(error)
                    debug_msg = ( f"add KeyError Caught an error: {error_message} skipping this field" )
                    logging.log( LOG_LEVEL,  debug_msg, )

    # -------------------------------------------
    def get_selected_row_data(self):
        """
        Get the data from the currently selected row.
        """
        model       = self.model

        indexes     = self.view.selectedIndexes()
        if not indexes:
            QMessageBox.warning( self, "Warning", "No record selected." )
            return None

        # Get the model row index
        model_row = indexes[0].row()
        data  = {}

        field_ix = -1   # could make loop or even list comp
        for field_name, col_dict in self.field_dict.items():
            field_ix          += 1
            data[field_name]   = model.data( model.index( model_row, field_ix))
            # model.setHeaderData( ix_col, Qt.Horizontal, col_dict[ "col_head_text"  ] )
            # view.setColumnWidth( ix_col,                col_dict[ "col_head_width" ] )

        return (model_row, data)  # is this best return, even needed ??

    # ----------------------------------
    def edit_selected_record(self):
        """
        from stuff then update
        Open dialog to edit the currently selected event.
        """
        selected_data = self.get_selected_row_data()
        if selected_data is None:
            return

        row, data = selected_data

        # # Open dialog with the current data
        # #dialog = StuffEventDialog(self, edit_data=data)
        # dialog = people_document_edit.EditPeopleContact( self, edit_data = data )
            # self the parent tab
        dialog    = self._build_dialog( data )
        model     = self.model

        if dialog.exec_() == QDialog.Accepted:
            form_data = dialog.get_form_data()

            # for field_name, field_ix in  PEOPLE_CONTACT_COLUMN_DICT.items():
            #     model.setData( model.index( row, field_ix ), form_data[ field_name ] )

            field_ix = -1   # could make loop or even list comp
            for i_column_name, col_dict in self.field_dict.items():
                field_ix    += 1
                model.setData( model.index( row, field_ix ), form_data[ i_column_name ] )
                # model.setHeaderData( ix_col, Qt.Horizontal, col_dict[ "col_head_text"  ] )
                # view.setColumnWidth( ix_col,                col_dict[ "col_head_width" ] )

    # ------------------------------------------
    def delete_record(self):
        """
        what it says, read?

        set current id, get children
        """
        msg   = "delete_record ... not implemented"
        QMessageBox.warning(self, "Sorry", msg )

    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = ">>>>>>>>>>* PeopleEventSubTab  *<<<<<<<<<<<<"

        return a_str

# ----------------------------------------
class SubTabBaseOld( QWidget ):
    """
    used for detail many sub tabs but some like text and picture may be special

    """
    def __init__(self, parent_window ):
        """
        use in
            moving to stuff event
            PictureSubjectSubTab( stuffdb_tabbed_sub_window.StuffdbSubTabTab  ):

        """
        super().__init__()
        self.parent_window  = parent_window

        self.db             = AppGlobal.qsql_db_access.db

        #self.table_name      = self.parent_window.table_name  --- no this is photo

        self.current_id     = None

        debug_msg  = ( "in SubTabBase  tab appends to a window list is this correct?? -- maybe ")
        logging.debug( debug_msg )

        self.parent_window.sub_tab_list.append( self )    # a function might be better

    # -----------------------
    def update_db( self,    ):
        """
        for debugging

        do not need key generation on new
        model               = QSqlTableModel( self, self.db )
        model_indexer       = table_model.ModelIndexer( model )
        self.model_indexer  = model_indexer

        self.model_subject  = model

        """
        debug_msg   = ( "update_db  StuffdbSubSubTab this simple? db commit here??  ")
        logging.debug( debug_msg )

        model       =  self.model    # QSqlTableModel( self, self.db )
        model.submitAll()
        self.db.commit()

# ----------------------------------------
class CriteriaTabBase( QWidget ):
    """
    criteria tab parent, not sure if useful yet ..
    """
    def __init__(self, parent_window ):
        """
        lots of variable may not be used .... clean up later
        """
        super().__init__()

        self.criteria_dict          = {}
        self.critera_widget_list    = []
        self.critera_is_changed     = True
        self.parent_window          = parent_window
        self.key_words_widget       = None      # set to value in gui if used

        self.tab_name               = "CriteriaTab set in child"
        self._build_tab()
        self.clear_criteria()

    # -----------------------------
    def add_date_widgets( self, placer, row_lables = ("Edit", "Add") ):
        """
        might want to add labels to the
        arguments and default to edit and add
        """
        # ---- dates
        placer.new_row()
        widget  = QLabel( row_lables[0] )
        placer.new_row()
        placer.place( widget )

        # widget                  = QDateEdit()
        # self.end_date_widget    = widget
        # widget.setCalendarPopup( True )
        # widget.editingFinished.connect( lambda: self.criteria_changed( True ) )
        # widget.setDate(QDate( 2025, 1, 1 ))
        # placer.place( widget )
        widget, widget_to_layout       = self.make_criteria_date_widget()
        #widget                         = self.make_criteria_date_widget()
        self.start_edit_date_widget    = widget
        widget.critera_name  = "start_edit_date"
        self.critera_widget_list.append( widget )
        widget.setDate(QDate( 2025, 1, 1 ))
        placer.place( widget )

        widget  = QLabel( "to" )
        placer.place( widget )

        widget, widget_to_layout       = self.make_criteria_date_widget()
        self.end_edit_date_widget       = widget
        widget.critera_name  = "end_edit_date"
        self.critera_widget_list.append( widget )
        widget.setDate(QDate( 2025, 1, 1 ))
        placer.place( widget )

        # ---- placer.new_row()
        placer.new_row()
        widget  = QLabel( row_lables[1] )
        placer.new_row()
        placer.place( widget )

        widget, widget_to_layout       = self.make_criteria_date_widget()
        self.start_add_date_widget      = widget
        widget.critera_name  = "add_start_date"
        self.critera_widget_list.append( widget )
        widget.setDate(QDate( 2025, 1, 1 ))
        placer.place( widget_to_layout )

        widget  = QLabel( "to" )
        placer.place( widget )

        widget, widget_to_layout       = self.make_criteria_date_widget()
        self.end_add_date_widget        = widget
        widget.critera_name  = "add_end_date"
        self.critera_widget_list.append( widget )
        widget.setDate(QDate( 2025, 1, 1 ))
        placer.place( widget_to_layout )

    # -------------------------------
    def _build_top_widgets_grid( self, grid_layout ):
        """
        what it says read, std for all criteria tabs
        lets add a Hbox
        now on an hbox placed on the grid layout
        return
            mutates
            creates new row, uses creates another
        """
        grid_layout.new_row()
        button_layout    = QHBoxLayout()
        grid_layout.addLayout( button_layout, grid_layout.ix_col, grid_layout.ix_row, 1, 5  )
        #row: int, column: int, rowSpan: int, columnSpan:
            # int, alignment: Union[Qt.Alignment, Qt.AlignmentFlag] = Qt.Alignment()):
        grid_layout.new_row()

        # ---- may need a spacer where titles are in rest of page
        # width    = 35
        # widget   = QSpacerItem( width, 10, QSizePolicy.Expanding, QSizePolicy.Minimum )
        # #grid_layout.new_row()
        # # grid_layout.addWidget( widget )
        # grid_layout.addItem( widget, grid_layout.ix_row, grid_layout.ix_col    )  # row column
        # grid_layout.ix_col  += 1

        # ---- buttons
        a_widget        = QPushButton( "Clear" )
        a_widget.clicked.connect(  self.clear_criteria )
        button_layout.addWidget( a_widget )

        a_widget        = QPushButton( "Go -->" )
        a_widget.clicked.connect(  self.parent_window.criteria_select )
        button_layout.addWidget( a_widget )

        a_widget        = QPushButton( "Paste/Go -->" )
        a_widget.clicked.connect(  self.paste_go )
        button_layout.addWidget( a_widget )

        a_widget        = QPushButton( "Clear/Paste/Go -->" )
        a_widget.clicked.connect(  self.clear_go )
        button_layout.addWidget( a_widget )

        grid_layout.new_row()

    # -------------------------------
    def _build_top_widgets_placer_delete( self, placer ):
        """
        what it says read, std for all criteria tabs
        lets add a Hbox
        """
        placer.new_row()
        button_layout    = QHBoxLayout()
        placer.layout.addLayout( button_layout, placer.ix_col, placer.ix_row, 0, 5  )
        #row: int, column: int, rowSpan: int, columnSpan: int, alignment: Union[Qt.Alignment, Qt.AlignmentFlag] = Qt.Alignment()):
        placer.new_row()
        # ---- buttons
        a_widget        = QPushButton( "Clear" )
        a_widget.clicked.connect(  self.clear_criteria )
        button_layout.addWidget( a_widget )

        a_widget        = QPushButton( "Go -->" )
        a_widget.clicked.connect(  self.parent_window.criteria_select )
        button_layout.addWidget( a_widget )

        a_widget        = QPushButton( "Paste/Go -->" )
        a_widget.clicked.connect(  self.paste_go )
        button_layout.addWidget( a_widget )

        a_widget        = QPushButton( "Clear/Paste/Go -->" )
        a_widget.clicked.connect(  self.clear_go )
        button_layout.addWidget( a_widget )

    # -------------------------------
    def add_buttons( self, placer ):
        """
        debug
        this should be called add_debug_widgets
        """
        placer.new_row()
        widget  = QLabel( "unknown" )
        self.criteria_changed_widget = widget
        self.criteria_changed_widget.setText( "self.criteria_changed_widget" )
        placer.place( widget, columnspan = 2 )

        # ---- buttons
        a_widget        = QPushButton( "Clear Criteria change widget " )
        a_widget.clicked.connect(  self.clear_criteria )
        placer.new_row()
        placer.place( a_widget )

        a_widget        = QPushButton( "Run Select" )
        a_widget.clicked.connect(  self.parent_window.criteria_select )
        #placer.new_row()
        placer.place( a_widget )

        a_widget        = QPushButton( "show_criteria" )
        a_widget.clicked.connect( lambda: self.show_criteria(   ) )
        #placer.new_row()
        placer.place( a_widget )

        a_widget        = QPushButton( "Criteria Unchanged" )
        a_widget.clicked.connect( lambda: self.criteria_changed( False ) )
        #placer.new_row()
        placer.place( a_widget )

    # -------------------------
    def make_criteria_date_widget( self,   ):
        """
        THE WIDGETS HAVE CHANGED SINCE THIS WAS WRITTEN, FIX WHEN NEXT USED

        what it says, read
        make our standard date widgets

        return two widgets both same holdover from old code fix sometime ,
        starting and ending widget in a tuple
        """
        #widget                  = QDateEdit()
        widget                   = cw.CQDateCriteria()   # need types here perhaps !!
        widget.editingFinished.connect( lambda: self.criteria_changed( True ) )
        widget.userDateChanged.connect( lambda: self.criteria_changed( True ) )
        widget.setCalendarPopup( True )
        widget.setDisplayFormat( "dd/MM/yyyy" )
        widget.setDate( QDate( 2025, 1, 1 ))
        #widget_to_layout            = widget.container
        return ( widget, widget )
        # widget, widget_to_layout  =self.make_criteria_date_widget()

    # ---- Actions
    def criteria_select_if( self,   ):
        """
        What it says, read
            note: strip the strings
        """
        if self.critera_is_changed:
            self.criteria_select()
        else:
            pass
            # debug_msg  = ( "criteria_select_if no select !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            # logging.debug( debug_msg )
        # put in criteria_select  !! self.criteria_is_changed = False
        self.critera_is_changed = False

    #---------------------------
    def criteria_changed( self, is_changed ):
        """
        What it says, read
            note: strip the strings
        """
        self.critera_is_changed  = is_changed
        self.criteria_changed_widget.setText( f"criteria_changed {is_changed = }" )

    # -----------------------------
    def get_criteria( self ):
        """
        What it says, read
            note: strip the strings
            dates not yet right
            mutates self.criteria_dict but also returns
            !! could eliminate and let select get as needed
        """
        self.criteria_dict                  = {}
        criteria_dict                       = self.criteria_dict
        for i_criteria in self.critera_widget_list:
            i_criteria.build_criteria( criteria_dict )

        return criteria_dict

    # -----------------------------
    def clear_criteria( self ):
        """
        What it says, read
        """
        for i_criteria in self.critera_widget_list:
           # i_criteria.set_data_default()
            i_criteria.set_default()

    # -----------------------------
    def paste_go( self ):
        """
        What it says, read
        paste key word only then go
        """
        self.key_words_widget.set_data( QApplication.clipboard().text( ) )
        QApplication.clipboard().text( )
        self.criteria_select()

    # -----------------------------
    def clear_go( self ):
        """
        What it says, read
            think clear paste and go ?
        """
        #int( "clear_go --------------------------------------- add the clear ")
        self.clear_criteria()
        self.key_words_widget.set_data( QApplication.clipboard().text( ) )
        QApplication.clipboard().text( )
        self.criteria_select()
    # -----------------------------
    def search_me(self, criteria ):
        """
        external search should be overridden in each document type
        not implemented better
        """
        1/0

    # -----------------------------
    def get_date_criteria(self,  ):
        """
        gets as timestamps
        return
            modifies self.criteria_dict
        """
        criteria_dict   = self.criteria_dict
        # criteria_dict[ "channel_group" ]        = self.channel_group_widget.currentText().strip()

        criteria_dict[ "start_edit_date" ]  = self.start_edit_date_widget.get_date( )
        criteria_dict[ "end_edit_date" ]    = self.end_edit_date_widget.get_date(   )
        criteria_dict[ "start_add_date" ]   = self.start_add_date_widget.get_date( )
        criteria_dict[ "end_add_date" ]     = self.end_add_date_widget.get_date( )

    # -------------------------
    def show_criteria( self,   ):
        """
        what it says, read
            this is for debug, think should dump soon
        """
        criteria   = self.get_criteria()
        print( f"show_criteria {criteria}")
        pprint.pprint( criteria )

    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = "\n>>>>>>>>>>* CriteriaTabBase *<<<<<<<<<<<<"

        return a_str

# ----------------------------------------
class HistoryTabBase( QWidget ):

    def __init__(self, parent_window  ):

        super().__init__()
        self.parent_window   = parent_window

        self.list_ix         = 0    # should be active and selected
        self.ix_seq          = 0    # may be obsolete
        self.ix_col_seq      = 0
        self.ix_col_id       = 0
        self._build_gui()
        self.tab_name        = "CriteriTabBase -- tab failed to set"

    # -------------------------------------
    def _build_gui( self ):
        """
        what it says read
        update ver 21 to picture_sub_window
        some, all promotable??
        Returns:
            none
        """
        tab                 = self
        columns             = data_dict.DATA_DICT.get_list_columns( self.parent_window.detail_table_name )

        table                = QTableWidget(
                                       0, len( columns ), self )  # row column  parent
        self.history_table  = table

        # ---- column header and width

        for ix_col, i_column in enumerate( columns):
            #rint( f" {ix_col = } { i_width = }")
            table.setHorizontalHeaderItem( ix_col, QTableWidgetItem( i_column.col_head_text )  )
            table.setColumnWidth(          ix_col, i_column.col_head_width * WIDTH_MULP )

        table.setSelectionBehavior( QTableWidget.SelectRows )  # Select entire rows

        table_widget_no_edit( table )

        # table.clicked.connect( self.parent_window.on_history_clicked )
        # table.clicked.connect( self.on_list_clicked )
        table.cellClicked.connect( self.on_cell_clicked )

        layout2     = QVBoxLayout()
        layout2.addWidget( table )
        tab.setLayout( layout2 )

    # ------------------------
    def find_id_in_table( self, a_id  ):
        """
        what it says read
        return ix_row or -1 if not found
        just a linear search
        """
        str_id              = str( a_id )
        table               = self.history_table  # QTableWidget(

        ix_found            = -1

        for row in range( table.rowCount() ):
            item    = table.item( row, self.ix_col_id )
            if item is None:
                msg   = ( "find_id_in_table error !!")
                logging.error( msg )
                #breakpoint()     # pdb.set_trace()  # Start the debugger here

                return - 1

            #rint( f"find_id_in_table {item.text()}" )
            # if no item ,no match
            if item and item.text() == str_id:
                ix_found = row

        #rint( f">>>>>>>>>>>>find_row_with_text {str_id = } {ix_found = }")

        return ix_found   # check the caller for -1

    # ----------------------------
    def on_cell_clicked( self, ix_row, ix_col  ):
        """
        what it says read
        call to self.parent_window so the detail tab selects the id
        does not use prior next but could
        """
        self.parent_window.update_db()

        table           = self.history_table

        item            = table.item( ix_row, self.ix_col_id  )
        self.list_ix    = ix_row
        a_id             = int( item.text() )
        # msg        = f"on_cell_clicked  Row {ix_row}, Column
        #    {self.ix_col_id}, Data: {a_id = }"
        # rint( msg )
        self.parent_window.select_record( a_id )

    # ----------------------------
    def select_row(self, row_index ):
        """
        Select a specific row.  not in query sense
        table               = self.history_table  # QTableWidget(
        """
        #rint( "StuffdbHistoryTabselect_row {row_index = }" )
        self.history_table.selectRow( row_index )

    # -------------------------------------
    def record_to_table( self, record ):
        """
        what it says read
        from stuff history tab
        """
        table           = self.history_table  # QTableWidget(

        a_id            = record.value( "id" )
        str_id          = str( a_id )

        ix_row          = self.find_id_in_table( a_id )
        if ix_row >=0:
            debug_msg   = ( f"record_to_table found row {ix_row} in "
                             "future update maybe for now skip adding by return ")
            logging.debug( debug_msg )
            return

        columns    = data_dict.DATA_DICT.get_list_columns( self.parent_window.detail_table_name )
        col_head_texts   = [ "seq" ]  # plus one for sequence
        col_names        = [ "seq" ]
        col_head_widths  = [ "10"  ]

        # this works with the wrong column headings, they may be defined elsewhere like in build gui
        # but this is at least better
        col_head_texts   = [  ]  # we were off so
        col_names        = [  ]
        col_head_widths  = [  ]

        for i_column in columns:
            col_names.append(        i_column.column_name  )
            col_head_texts.append(   i_column.col_head_text  )
            col_head_widths.append(  i_column.col_head_width  )

        # ---- insert
        self.ix_seq     += 1
        row_position    = table.rowCount()
        table.insertRow( row_position )
        ix_col          = -1
        ix_row          = row_position   # or off by 1

        ix_col          += 1
        item             = QTableWidgetItem( str( self.ix_seq  ) )
        table.setItem( ix_row, ix_col, item   )

        for i_col_name in col_names:

            # # begin code gen ?  --- no drive from data dict
            #ix_col          += 1
            #rint( f"base record_to_tablerecord-to_table {ix_col}, {i_col_name}" )

            item             = QTableWidgetItem( str( record.value( i_col_name ) ) )
            table.setItem( ix_row, ix_col, item   )
            ix_col          += 1


    def delete_row_by_id( self, id_to_delete ):
        """
        Delete a row from QTableWidget where the value in column 0 matches id_to_delete.
        """
        table_widget   = self.history_table

        # Iterate through rows from bottom to top to avoid index shifting
        for row in reversed(range(table_widget.rowCount())):
            item = table_widget.item(row, 0)
            if item and item.text() == str(id_to_delete):
                debug_msg  = (f"HistoryTabBase_delete_row_by_id Deleting row {row} with id = {id_to_delete}")
                logging.log( LOG_LEVEL,  debug_msg, )

                table_widget.removeRow(row)
                table_widget.viewport().update() # if just one row
                return

        debug_msg  = (f"HistoryTabBase_delete_row_by_id No row found with id = {id_to_delete}")
        logging.log( LOG_LEVEL,  debug_msg, )


# ==================================
class TextTabBase( DetailTabBase  ):
    """
    taken from StuffTextTab -- make this the ancestor
    do we need DetailTabBase ??
    """
    #--------------------------------------
    def __init__(self, parent_window  ):
        """
        Args:
            parent_window (TYPE): DESCRIPTION.
            TextTab
        """
        super().__init__( parent_window )
        #self.parent_window       = parent_window
        #self._create_gui()
        self.tab_name               = "TextTabBase should be redefined"
        self.table                  = parent_window.text_table_name
        self.key_word_table_name    = ""   # suppress key word processing

    # -------------------------------------
    def _build_gui( self ):
        """
        what it says read
        Returns:
            none

        !!!!!!!!!!! a lot like the help_document text
            now copy method from there and tweak

        """
        tab                 = self

        tab_layout          = QVBoxLayout( tab )
            # widget: The widget you want to add to the grid.
            # row: The row number where the widget should appear (starting from 0).
            # column: The column number where the widget should appear (starting from 0).
            # rowSpan (optional): The number of rows the widget should span (default is 1).
            # columnSpan (optional): The number of columns the widget should span (default is 1).
            # alignment (optional):
        # could have a button layout down one side ??

        self._build_text_gui( tab_layout )

    # -------------------------------------
    def _build_text_gui( self, a_layout ):
        """
        like to build gui on text tabs borrowed here
        in help_document, try to make copy over to base document text tab
        we may be able to make this a method in base see base document ??

        new since last back lets use boxes
        like to build gui on text tabs borrowed here
        in help_document, try to make copy over to base document text tab
        we may be able to make this a method in base see base document ??
        """
        tab_layout      = QHBoxLayout()
        a_layout.addLayout( tab_layout )

        button_layout   = QVBoxLayout()
        tab_layout.addLayout( button_layout )

        # ---- text layout lets favor it for space
        text_layout     = QVBoxLayout()
        tab_layout.addLayout( text_layout, stretch=2 )

        data_manager    = self.data_manager

        # ---- TextEdit   needs to be defined at beginning with extension object
        # and monkey patch
        edit_field          = cw.CQTextEdit(
                                    parent         = None,
                                    field_name     = "text_data",
                                                  )
        text_entry_widget   = edit_field
        font                = QFont( * parameters.PARAMETERS.text_edit_font ) # ("Arial", 12)
        edit_field.setFont(font)
        self.text_data_field = edit_field    # may be used for editing
        edit_field.setPlaceholderText( "Some Long \n   text on a new line " )
        data_manager.add_field( edit_field, )
        text_layout.addWidget( edit_field, )  # what order row column
        text_edit_ext_obj         = text_edit_ext.TextEditExt( AppGlobal.parameters, text_entry_widget)
        self.text_edit_ext_obj    = text_edit_ext_obj

        # tab                 = self

        # tab_layout          = QGridLayout(tab)
        #     # widget: The widget you want to add to the grid.
        #     # row: The row number where the widget should appear (starting from 0).
        #     # column: The column number where the widget should appear (starting from 0).
        #     # rowSpan (optional): The number of rows the widget should span (default is 1).
        #     # columnSpan (optional): The number of columns the widget should span (default is 1).
        #     # alignment (optional):
        # # could have a button layout down one side ??

        # ---- id
        widget                  =  cw.CQLineEdit(
                                     parent         = None,
                                     field_name     = "id",
                                                )
        self.id_field               = widget
        widget.setReadOnly( True )

        data_manager.add_field( widget, )
        button_layout.addWidget( widget, )

        label           = "Paste Clip"
        widget          = QPushButton( label )
        # connect_to  =  functools.partial( self.run_python_idle, text_entry_widget )
        # widget.clicked.connect( connect_to )
        widget.clicked.connect( self.text_edit_ext_obj.paste_clipboard  )
        button_layout.addWidget( widget, )

        # ---- template may not even need in self
        print( "monkey_patch_here_please")
        ddl_widget, ddl_button_widget  = self.text_edit_ext_obj.build_up_template_widgets()

        button_layout.addWidget( ddl_widget  )
        button_layout.addWidget( ddl_button_widget  )

        # ---- copy line
        label           = "Copy\nLine"
        widget = QPushButton( label )
        # connect_to  =  functools.partial( self.copy_line_of_text, text_entry_widget )
        # widget.clicked.connect( connect_to )
        button_layout.addWidget( widget, )

        label           = "run\npython idle"
        widget          = QPushButton( label )
        # connect_to  =  functools.partial( self.run_python_idle, text_entry_widget )
        # widget.clicked.connect( connect_to )
        #widget.clicked.connect( self.do_python )
        button_layout.addWidget( widget, )

        # ---- Paste Prior
        label           = "Paste Prior"
        widget          = QPushButton( label )
        # connect_to  =  functools.partial( self.run_python_idle, text_entry_widget )
        # widget.clicked.connect( connect_to )
        widget.clicked.connect( self.text_edit_ext_obj.paste_cache )
        button_layout.addWidget( widget, )

        # ---- Paste Prior
        label           = "Remove Lead/Trail"
        widget          = QPushButton( label )
        # connect_to  =  functools.partial( self.run_python_idle, text_entry_widget )
        # widget.clicked.connect( connect_to )
        widget.clicked.connect( self.text_edit_ext_obj.strip_lines_in_selection  )
        button_layout.addWidget( widget, )

        # ---- search text
        search_layout       = QHBoxLayout()
        text_layout.addLayout( search_layout )
        # ix_row          -= 1
        # ix_col          += 1
        widget              = QLineEdit()
        search_line_edit    = widget
        widget.setPlaceholderText("Enter search text")
        search_layout.addWidget( widget,   )

        # ---- up down Buttons
        widget                  = QPushButton("Down")
        down_button             = widget
        # connect below
        connect_to      = functools.partial( self.text_edit_ext_obj.search_down, search_line_edit ,)
                  #text_entry_widget  ) # entry_widget =.CQTextEdit(
        down_button.clicked.connect( connect_to )
        search_layout.addWidget( widget,  )

        widget           = QPushButton("Up")
        up_button        = widget
        connect_to      = functools.partial( self.text_edit_ext_obj.search_up, search_line_edit ,)
        up_button.clicked.connect( connect_to )
        search_layout.addWidget( widget,   )

        # # ---- qt_exec
        # label           = "qt_exec"
        # widget          = QPushButton( label )
        # connect_to  =  functools.partial( text_edit_ext.qt_exec, text_entry_widget )
        # widget.clicked.connect( connect_to )
        # # # widget.clicked.connect( self.qt_exec )
        # text_layout.addWidget( widget,  )

        # ---- >>
        label       = ">>"
        widget      = QPushButton( label )
        #connect_to  = functools.partial( text_edit_ext_obj.cmd_exec, text_entry_widget )
        connect_to  =   text_edit_ext_obj.cmd_exec
        widget.clicked.connect( connect_to )
        text_layout.addWidget ( widget,     )

    # -------------------------------------
    def _build_text_gui_old( self, a_layout ):
        """
        we may be able to make this a method in base see help document ??
        now in base  what changes
            change data_manager to
                data_manager    = self.data_manager


            like to build gui on text tabs borrowed here
            in help_document, try to make copy over to base document text tab
        """

        tab_layout      = QGridLayout( )
        a_layout.addLayout( tab_layout )

        data_manager    = self.data_manager

        ix_row          = 0
        ix_col          = 0

        # tab                 = self

        # tab_layout          = QGridLayout(tab)
        #     # widget: The widget you want to add to the grid.
        #     # row: The row number where the widget should appear (starting from 0).
        #     # column: The column number where the widget should appear (starting from 0).
        #     # rowSpan (optional): The number of rows the widget should span (default is 1).
        #     # columnSpan (optional): The number of columns the widget should span (default is 1).
        #     # alignment (optional):
        # # could have a button layout down one side ??

        # ---- id
        ix_row      += 1
        ix_col       = 0
        widget                  =  cw.CQLineEdit(
                                     parent         = None,
                                     field_name     = "id",
                                            )
        self.id_field               = widget
        widget.setReadOnly( True )
        #edit_field.default_value    = 999
        data_manager.add_field( widget, ) # is_key_word = True )
        tab_layout.addWidget( widget, ix_row, ix_col )

        # ---- textedit   entry_widget         = QTextEdit()
        ix_row          += 1
        ix_col          = 1

        edit_field         = cw.CQTextEdit(
                                    parent         = None,
                                    field_name     = "text_data",
                                                 )
        entry_widget            = edit_field  # !! redundant
        text_entry_widget       = edit_field
        self.text_data_field    = edit_field    # may be used for editing
        font                    = QFont( * parameters.PARAMETERS.text_edit_font )
        edit_field.setFont(font)

        edit_field.setPlaceholderText( "Some Long \n   text on a new line " )
        data_manager.add_field( edit_field, )

        tab_layout.addWidget( edit_field, ix_row, ix_col,  5, 5 )

        #--------------- !! not sure about these think we need
            # as monkey patch but may have moved into TextEditExt
        text_edit_ext_obj         = text_edit_ext.TextEditExt( AppGlobal.parameters, text_entry_widget)
        self.text_edit_ext_obj    = text_edit_ext_obj

        ix_row          += 1
        ix_col          = 0
        label           = "Copy\nLine"
        widget = QPushButton( label )
        # connect_to  =  functools.partial( self.copy_line_of_text, entry_widget )
        # widget.clicked.connect( connect_to )
        tab_layout.addWidget( widget, ix_row, ix_col )

        ix_row          += 1
        ix_col          = 0
        label           = "run\npython idle"
        widget          = QPushButton( label )
        # connect_to  =  functools.partial( self.run_python_idle, entry_widget )
        # widget.clicked.connect( connect_to )
        #widget.clicked.connect( self.do_python )
        tab_layout.addWidget( widget, ix_row, ix_col )

        # ---- qt_exec
        ix_row          += 1
        ix_col          = 0
        label           = "qt_exec"
        widget          = QPushButton( label )
        #connect_to      = functools.partial( text_edit_ext.search_down,
        #    search_line_edit , entry_widget  )
        #down_button.clicked.connect( connect_to )
        connect_to  =  functools.partial( text_edit_ext.qt_exec, entry_widget )
        widget.clicked.connect( connect_to )
        # # widget.clicked.connect( self.qt_exec )
        tab_layout.addWidget( widget, ix_row, ix_col )

        ix_row   += 1
        label       = ">>"
        widget      = QPushButton( label )
        #connect_to  =  functools.partial( text_edit_ext.cmd_exec, entry_widget )
        connect_to  =   text_edit_ext_obj.cmd_exec
        widget.clicked.connect( connect_to )
        tab_layout.addWidget ( widget, ix_row, 0,   )

        # ---- search text
        ix_col          += 1
        widget                  = QLineEdit()
        search_line_edit        = widget
        widget.setPlaceholderText("Enter search text")
        tab_layout.addWidget( widget, ix_row, ix_col )

        # ---- up down Buttons
        ix_col          += 1
        widget                  = QPushButton("Down")
        down_button             = widget
        # connect below
        tab_layout.addWidget( widget, ix_row, ix_col )

        ix_col          += 1
        widget           = QPushButton("Up")
        up_button        = widget
        # connect below
        tab_layout.addWidget( widget, ix_row, ix_col )

        connect_to      = functools.partial(
                          self.text_edit_ext_obj.search_down, search_line_edit ,)
        down_button.clicked.connect( connect_to )

        connect_to      = functools.partial(
                          self.text_edit_ext_obj.search_up, search_line_edit , entry_widget  )
        up_button.clicked.connect( connect_to )

    # ------------------------
    def run_python_idle( self, text_edit ):
        """
        !! move from base to text ext
        now an experiment to do python esp for now examples
        assume starts from line we are on
        scan down until we hit a blank line, which
        marks the end of the example

        then run it how -- see cmd assist
-------------------
1 And you know the sun's settin' fast,
2 And just like they say, nothing good ever lasts.
3 Well, go on now and kiss it goodbye,
4 But hold on to your lover,
5 'Cause your heart's bound to die.
6 Go on now and say goodbye to our town, to our town.
7 Can't you see the sun's settin' down on our town, on our town,
8 Goodnight.

print( "hello world")
print( "hello russ")
print( "good by")
breakpoint()

        """
        code_lines       = self.get_snippet_lines(   )
        #rint( code_lines )
        code_lines       = self.undent_code_lines(code_lines)
        code_lines[0]    = "# " + code_lines[0]
        code_lines       = [i_line + "\n" for i_line in code_lines ]

        debug_msg  = ( f"run_python_idle {code_lines = }")
        logging.debug( debug_msg )

        file_name  = "temp_stuff.py"
        with open( file_name, 'w') as a_file:
            # this may not have \n at end of line
            a_file.writelines( code_lines   )

        open_python_file_in_idle( file_name )

    # ---- Text manipulation ------------------------------------------------------
    #----------------------
    def copy_line_of_text(self, text_edit ):
        """
        chat:
        With a QTextWidge holding some text:
        from the cursor position copy the text from the
        beginning of the line to the end of the line.

        Note text goes into clipboard we should add an argument for that !!
        """
        debug_msg   = ( "TextEditTab.copy_line_of_text"   )
        logging.debug( debug_msg )

        cursor              = text_edit.textCursor()
        # Save the original cursor position
        original_position   = cursor.position()
        cursor.movePosition( cursor.StartOfLine )

        # Select the text from the beginning to the end of the line
        cursor.movePosition(cursor.EndOfLine, cursor.KeepAnchor)
        selected_text = cursor.selectedText()
        # rint(f"Copied text: {selected_text = }")

        # Optionally, copy to the system clipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(selected_text)

        # Restore the original cursor position
        cursor.setPosition(original_position)
        text_edit.setTextCursor(cursor)

        #rint(f"Copied text: {selected_text = }")

        return selected_text

    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = "\n>>>>>>>>>>* TextTabBase *<<<<<<<<<<<<"
        return a_str

# ==================================
class StuffdbPictureTab(  DetailTabBase   ):
    """
    taken from photo --- do we want this inherit
    look at promotion in parents not sure why this needs to be here as well
    """
    def __init__(self, parent_window  ):
        """
        this tab does not interact with the db directly
        big view of the picture
        """
        super().__init__( parent_window )

        self.picture_sub_tab    = None     # but usually update in descendant
        #rint( f"PicturePictureTab __init__ {parent_window = }")
        self.__build_gui()

    #-------------------------------------
    def __build_gui( self ):
        """
        what it says read
        Returns:
            none
        """
        tab                 = self
        tab_layout          = QVBoxLayout(tab)

        #viewer              = picture_viewer.PictureViewer( self )
        viewer              = picture_viewer.PictureViewerPlus( self )
        self.viewer         = viewer
        tab_layout.addWidget( viewer )

        self.display_file()

        # !! next is bad -- picture does not have a picture sub tab
        document           = self.parent_window
        picture_sub_tab    = document.detail_tab.picture_sub_tab  # may be None
        # ---- buttons -- test picture select

        # ---- buttons
        button_layout       = QHBoxLayout(   )
        tab_layout.addLayout( button_layout )

        if picture_sub_tab:   # because picture doe not have this
            widget          = QPushButton('Next>')
            connect_to      = functools.partial( picture_sub_tab.prior_next, 1 )
            widget.clicked.connect( connect_to )
            button_layout.addWidget( widget )

            widget          = QPushButton( '<Prior')
            connect_to      = functools.partial( picture_sub_tab.prior_next, -1 )
            widget.clicked.connect( connect_to )
            button_layout.addWidget( widget )

        a_widget        = QPushButton( "fit" )
        a_widget.clicked.connect(  self.fit_in_view )
        button_layout.addWidget( a_widget )

    # -----------------------------
    def display_file( self,  file_name = "/mnt/WIN_D/PhotoDB/02/102-0255_img.jpg"  ):
        """
        what it says, read
        call from ?
        !! use instead filename  = stuffdb_tabbed_sub_window.fix_pic_filename( filename   )
        """
        if file_name is None:
            file_name = ""   # prevents error Path()

        file_path       = Path( file_name )

        if not file_path.exists():  # look for function to check this and may have already been done
            file_name   = AppGlobal.parameters.pic_nf_file_name

        self.viewer.display_file( file_name )
        self.fit_in_view()

    # ---------------------------
    def select_record( self, id_value  ):
        """
        !! this may be promote by mistake
        this is override of parent as we get file name from
        our detail sister tab
        """
        picture_file_name    = self.parent_window.detail_tab.get_picture_file_name()
        #rint( f"picture picture tab, select_record {picture_file_name}")

        self.display_file( picture_file_name )

    # ------------------------------------------
    def select_by_id ( self, a_id ):
        """
        try to get one that works
        """
        debug_msg    = (   "picture picture tab select_by_id, do I get called"
                          f" ................................select_by_id {a_id}")
        logging.debug( debug_msg )

    # ---- zooms, may also be in context map, may want buttons for these
    #          or delete
    #-------------------------------------
    def zoom_in(self):
        self.viewer.zoom_in()
        #rint("Zoomed In")

    #-------------------------------------
    def zoom_out(self):
        self.viewer.zoom_out()
        #rint("Zoomed Out")

    def reset_zoom(self):
        self.viewer.reset_zoom()
        #rint("Zoom Reset")

    #-------------------------------------
    def fit_in_view(self):
        self.viewer.fit_in_view()
        #rint("PicturePictureTab Fit in View")

# ----------------------------------------
class StuffdbPictureTab_not_photo( QWidget ):

    def __init__(self, parent_window  ):
        """
        this tab does not interact with the db directly

        Args:
            parent_window (TYPE): DESCRIPTION.

        """
        super().__init__()
        self.parent_window   = parent_window

        self.tab_name        = "StuffdbPictureTab for some other doc??"   # may not be needed
        # rint( f"PhotoPhotoTab __init__ {parent_window = }")
        self._build_gui()

    # ----------------------------
    def prior_next( self, delta ):
        """
        flip thru pictures
        """
        file_name   = self.parent_window.prior_next_picture( delta )
        debug_msg   = ( f"prior_next {file_name = }")
        logging.debug( debug_msg )

        if file_name:
            #self.viewer.display_file( file_name )
            self.display_file( file_name )

    # -------------------------------------
    def _build_gui( self ):
        """
        what it says read
        Returns:
            none
        """
        tab                 = self
        tab_layout          = QVBoxLayout( tab )

        #viewer              = picture_viewer.PictureViewer( self )
        viewer              = picture_viewer.PictureViewerPlus( self )
        self.viewer         = viewer
        tab_layout.addWidget( viewer )

        # ----file_name
        widget                = QLabel( "should be filename" )
        #placer.new_row()
        self.filename_widget  = widget
        tab_layout.place( widget )

        #self.display_file()

        button_layout          = QHBoxLayout( )
        tab_layout.addLayout( button_layout )

        # ---- buttons
        a_widget        = QPushButton( "fit" )
        a_widget.clicked.connect(  self.fit_in_view )
        button_layout.addWidget( a_widget )

        #
        a_widget        = QPushButton( "<prior" )
        connect_to      = functools.partial( self.prior_next, -1 )
        a_widget.clicked.connect(  connect_to )
        button_layout.addWidget( a_widget )

        #
        a_widget        = QPushButton( "next>" )
        connect_to      = functools.partial( self.prior_next, 11 )
        a_widget.clicked.connect(  connect_to )
        button_layout.addWidget( a_widget )

    # -----------------------------
    def display_file( self, file_name="/mnt/WIN_D/PhotoDB/02/102-0255_img.jpg"  ):
        """
        what it says, read
        """
        # pixmap      = QPixmap( file_name )
        # self.viewer.set_photo( pixmap )
        file_path       = Path( file_name )
        if not file_path.exists():
            msg         = f"display_file, file not found {file_name} "
            logging.error( msg )

            file_name   = AppGlobal.parameters.pic_nf_file_name

        self.viewer.display_file( file_name )
        self.filename_widget.setText( file_name )
        self.fit_in_view()

    # ---------------------------
    def select_record( self, id_value  ):
        """
        not really selected but trick off file display
        """
        self.prior_next( 0 )

    # -------------------------------------
    def zoom_in(self):
        self.viewer.zoom_in
        print("Zoomed In")

    # -------------------------------------
    def zoom_out(self):
        self.viewer.zoom_out
        print("Zoomed Out")

    def reset_zoom(self):
        self.viewer.reset_zoom()
        #rint("Zoom Reset")

    # -------------------------------------
    def fit_in_view(self):
        self.viewer.fit_in_view()
        #rint("picturePhotoTab Fit in View")

# ----------------------------------------
class PictureListSubTabBase( QWidget  ):
    """
    from albums picture list but no update -- and albums not currently using
            --- also for stuff, plant.... is albums the special one
    probably should be in other picture lists like events....

    see how much can add to an ancestor
    this is from chat code
    needs to select from photo where join to photo_subject is
    for this subject

    different from album which joins to photoshow_photo
    which is a bit more complicated

    except for table name this should be the same for all items

    we do not really need to fetch any data from the

    photo_subject table
    """
    # ------------------------------------------
    def __init__(self, parent_window ):
        """
        the usual init, read
        """
        super().__init__()
        self.parent_window      = parent_window
        self.sub_window         = parent_window.parent_window   # two levels up

        #self.picture_tab       = self.sub_window.picture_tab
        self.list_ix            = -1  # should track selected an item in detail
        #self.list_table_name = None   # fix in descendant
        self.list_table_name    = "photoshow_photo"
        self.table_name         = self.list_table_name # -- clean up
        self.pictures_for_table = "set me in child init "
        # xxxx  AppGlobal.add_photo_target   = self
        self.db                 = AppGlobal.qsql_db_access.db

        self._build_gui()

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says, read
        """
        page                 = self

        main_layout          = QVBoxLayout( self )
        picture_layout       = QHBoxLayout(   )
        button_layout        = QHBoxLayout(   )

        main_layout.addLayout( picture_layout )
        main_layout.addLayout( button_layout )

        # ---- view
        view                = QTableView()
        self.view           = view
        view.setSelectionBehavior( QTableView.SelectRows )
        view.clicked.connect( self._on_list_click  )

        picture_layout.addWidget( self.view )

        # ---- picture
        a_picture_viewer      = picture_viewer.PictureViewer( self )
        self.picture_viewer   = a_picture_viewer
        picture_layout.addWidget( a_picture_viewer )

        self._build_model()

        view.setModel( self.model )

        view.setEditTriggers(QTableView.NoEditTriggers) # no editing

        # ---- buttons -- test picture select
        widget         = QPushButton('Next>')
        connect_to     = functools.partial( self.prior_next, 1 )
        widget.clicked.connect( connect_to )
        button_layout.addWidget( widget )

        #
        widget        = QPushButton( '<Prior')
        connect_to     = functools.partial( self.prior_next, -1 )
        widget.clicked.connect( connect_to )
        button_layout.addWidget( widget )

    # ------------------------------------------
    def _build_model( self, ):
        """
        what it says, read?
        from russ_qrm
        sql set in select_by_id
        """
        # ----
        model               = QSqlQueryModel( )
        self.model          = model
        # Set the headers for the columns -- needs to be done after connect?

    # ------------------------------------------
    def _on_list_click( self, index,   ):
        """
        what it says, read
        now just a table
        """
        #rint( f"_on_list_click {index = }"   )  # the row?
        row                     = index.row()
        # column                  = index.column()
        #rint( f"PictureListSubTabBase on_list_click {row = }  ")

        self.list_ix           = row
        self.prior_next( 0 )   # 0 sets to beginning

    # ------------------------------------------
    def select_by_id ( self, a_id ):
        """
        try to get one that works
        messing with order to get headers to work
        """
        table_id        = a_id
        model           = self.model  #   a QSqlQueryModel()
        table_joined    = self.pictures_for_table

        query           = QSqlQuery()

        # Prepare the SQL statement with bind placeholders
        sql_query = """
        SELECT
           photo.id,
           photo.name,
           photo.sub_dir,
           photo.file
        FROM
            photo_subject
        JOIN
            photo
        ON
            photo_subject.photo_id      = photo.id
        WHERE
            photo_subject.table_joined  = :table_joined
        AND
            photo_subject.table_id      = :table_id;
        """
        self.view.setModel( model )
        query.prepare( sql_query )

        # Bind the actual values to the placeholders
        query.bindValue(":table_joined", table_joined )
        query.bindValue(":table_id",     table_id     )

        is_ok  = AppGlobal.qsql_db_access.query_exec_model( query,
                                    model,
                                    msg = "PictureListSubTabBase select_by_id" )

        self.set_headers()
        self.set_picture_ix( 0 )

    # ------------------------------------------
    def prior_next( self, delta, absolute = False   ):
        """
        get and put in control the prior or next picture
        using delta to determine which
            # delta = 0 is special see code why use set_picture_ix

        what it says, read
        direction  + forward, -backward 0 at start
        -- perhaps let it use any number so as to jump around


        watch for off by one, assume zero indexing
        return file_name or None
           delta = delta from current position
           zero may be a special number

        """
        # this is an alternative use in album absolute = False as arg
        # if absolute:
        #     new_list_ix           = delta
        # else:
        #     new_list_ix           = list_ix + delta

        new_list_ix        = self.list_ix + delta  # fixed in set.....

        file_name          = self.set_picture_ix( new_list_ix )

        return file_name

    # ------------------------------------------
    def set_picture_ix( self, picture_ix   ):
        """
        try to go to absolute index
        fix up as necessary
        special values
        ints  give the absolute position

        """
        view    = self.view    #  QTableView
        model   = self.model   #  QSqlQueryModel
        #prior_list_ix    = self.list_ix  # ng
        no_rows                  = model.rowCount()

        list_ix                  = self.list_ix
        new_list_ix              = picture_ix
        # self.list_ix           = row
        if no_rows <= 0:
            debug_msg     = f"set_picture_ix {no_rows = }  should clear display or no pic pic "
            logging.debug( debug_msg )
            file_name        = fix_pic_filename( None   )
            self._display_picture( file_name )
            return file_name

        if new_list_ix >= no_rows:
            new_list_ix  =  no_rows -1
            debug_msg     = f"set_picture_ix {no_rows = } {new_list_ix = } tried to index past end"
            logging.debug( debug_msg )

        elif new_list_ix < 0:
            new_list_ix  =  0
            debug_msg     = f"set_picture_ix {no_rows = } {new_list_ix = } tired to index before start"
            logging.debug( debug_msg )
        # else in range

        self.list_ix        = new_list_ix
        # fn_index               = self.query_model_read.index( new_list_ix, 1 )
        # file_name              = self.query_model_read.data( fn_index, Qt.DisplayRole )
        ix_fn                =  3  # column number
        ix_sub_dir           =  2
        #fn_item               =  model.item( self.list_ix,  ix_fn )  # may need to be model or ....

        sub_dir              = model.data( model.index( self.list_ix, ix_sub_dir ) )
        file_name            = model.data( model.index( self.list_ix, ix_fn ) )
        # combine next two ??
        fn_item              = build_pic_filename( file_name = file_name, sub_dir = sub_dir )
        fn_item              = fix_pic_filename( fn_item )
        index                = self.model.index( self.list_ix, 0)

        # Get the selection model from the QTableView
        selection_model = self.view.selectionModel()

        selection_model.clearSelection()

        # Select the entire row
        selection_model.select( index, selection_model.Select | selection_model.Rows )

        view                    = self.view
        # Optionally, scroll to the selected row
        self.view.scrollTo( index )

        #file_name  = fn_item.text() if fn_item is not None else ""
        file_name       = fn_item
        debug_msg       = ( f"set_picture_ix { file_name  = }")
        logging.debug( debug_msg )

        self._display_picture( file_name )
        return file_name

    #---------------------------
    def _display_picture( self, file_name ):
        """
        just do the display no checking
        usually from set_picture_ix
        """
        self.picture_viewer.display_file( file_name )

        other_picture_tab   =  self.parent_window.parent_window.picture_tab
        if other_picture_tab:
            other_picture_tab.display_file( file_name )

    def set_headers( self ):
        """
        what it says, read
        """
        model   = self.model
        view    = self.view

        ix_col  = 0
        model.setHeaderData( ix_col, Qt.Horizontal, "ID")
            #  Qt.Horizontal or Qt.Vertical
        view.setColumnWidth( ix_col, 50  )

        ix_col  += 1
        model.setHeaderData( ix_col, Qt.Horizontal, "Name")
        view.setColumnWidth( ix_col, 250 )

        ix_col  += 1
        model.setHeaderData( ix_col, Qt.Horizontal, "Folder")
        view.setColumnWidth( ix_col, 100 )

        ix_col  += 1
        model.setHeaderData( ix_col, Qt.Horizontal, "Photo Filename")
        view.setColumnWidth( ix_col, 250 )

        # chat says put last
        view.setModel( model )

    #------------------------------
    def update_db( self ):
        """update_db
        for now a forward, pull back later
        """
        pass
        # msg   = f"PictureListSubTabBase update_db no implementation is it needed?"
        # logging.error( msg )

# ---- eof ---------------------------
