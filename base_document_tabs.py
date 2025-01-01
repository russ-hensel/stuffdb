#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""



"""

# ---- tof
# --------------------
if __name__ == "__main__":
    import main
    main.main()
# --------------------

import functools
import pprint
from pathlib import Path

# ---- imports

from app_global import AppGlobal
# ---- Qt

from PyQt5.QtCore import QDate, QModelIndex, Qt, QTimer, pyqtSlot
# ---- begin pyqt from import_qt.py
from PyQt5.QtGui import QIntValidator, QStandardItem, QStandardItemModel, QTextCursor
# ---- QtSql
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
                             QDateEdit,
                             QDockWidget,
                             QFileDialog,
                             QFrame,
                             QGridLayout,
                             QHBoxLayout,
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
                             QSpinBox,
                             QTableView,
                             QTabWidget,
                             QTextEdit,
                             QVBoxLayout,
                             QWidget)

import custom_widgets
#import mdi_management
import picture_viewer
#import table_model
import wat_inspector
import subprocess
import key_words
import string_util
import info_about
import data_manager

FIF       = info_about.INFO_ABOUT.find_info_for

# -----------------------
def open_in_idle_string( python_filename, venv_name ):
    """
    taken from clipboard dec 2024
    Purpose:
        create a string for a .sh file to open
        a python file in a conda virtual env
        using idle

    Args:
        python_filename (TYPE): DESCRIPTION.
        venv_name (TYPE): DESCRIPTION.

    Returns:
        the string

    """
    python_path        = Path( python_filename )
    python_path_dir    = python_path.parent

    long_f_string      = (   # yes string is comming outdented in following lines
f"""
#!/bin/bash

# Run python in a conda environment
# Print Hello message
echo "Run idle with python in a conda environment"

# Activate conda environment
source /home/russ/anaconda3/etc/profile.d/conda.sh
conda activate {venv_name}

#activate myenv
python  -m idlelib  {python_filename}

# Deactivate the conda environment -- process my die so so what
conda deactivate

# here just wait for a keystroke ( or comment out )
read RESPONSE
"""  ).strip()

    #rint( f"here is the open in idle_string: \n>>{long_f_string}<<"  )
    return long_f_string

# ---- open in idle
def open_python_file_in_idle(  python_filename, ): # conda_env ):
    """
    taken from clipboard dec 2024
    we write and execute a shell script to do this

    currently if file does not exist it will be created

    return
        None

    """
    script_filename   =  "temp_idle_script.sh"  # first time around set to executable ??  add ./ ??
    conda_env         =  "py_12_misc"
    # script_path        = Path( script_filename )
    # script_path_abs    = script_path.absolute()

    sh_text            = open_in_idle_string( python_filename  , conda_env  )

    with open( script_filename, 'w') as a_file: # a will append  w will oveerwrite
        a_file.write( sh_text )

    ret    =    subprocess.Popen( [ f"./{script_filename}",  ]   )


# --------------------------------
def model_submit_all( model, msg ):
    """
    add a bit of error checking to submitAll()
    ok     = stuffdb_tabbed_sub_window.model_submit_all( model,  "we are here" )

    ok     = stuffdb_tabbed_sub_window.model_submit_all( model,  f"we are here {id = }" )
    """

    # wat_inspector.go(
    #      msg            = "model_submit_all pre-submit",
    #      # inspect_me     = self.people_model,
    #      a_locals       = locals(),
    #      a_globals      = globals(), )


    if model.submitAll():
        print( f"submitAll {msg}")
        ok   = True
    else:
        error = model.lastError()
        error_msg     = f"submitAll error: {msg}"
        print( error_msg )
        print( f"error text: {error.text()}")
        AppGlobal.logger.error( error_msg )
        ok   = False

    # wat_inspector.go(
    #      msg            = "model_submit_all post-submit",
    #      # inspect_me     = self.people_model,
    #      a_locals       = locals(),
    #      a_globals      = globals(), )

    return ok

RECORD_NULL         = 0
RECORD_FETCHED      = 1
RECORD_NEW          = 2
RECORD_DELETE       = 3

#   stuffdb_tabbed_sub_window.

RECORD_STATE_DICT   = { RECORD_NULL:    "RECORD_NULL",
                        RECORD_FETCHED: "RECORD_FETCHED",
                        RECORD_NEW:     "RECORD_NEW",
                        RECORD_DELETE:  "RECORD_DELETE",
                        }

#-------------------------
def build_pic_filename( file_name, sub_dir    ):
    """
    Returns:
        filename if exists else default from parameters
        perhaps fold in fix_pic_filename( filename   ):  !! ??
        file_name   = base_document_tabs.build_pic_filename( file_name, sub_dir )

    """
    # for debugging may need this
    if type( sub_dir ) != str:
        msg    = "build_pic_filename bad subdir look at self.ix_sub_dir"
        print( msg )
        return None

    root         = AppGlobal.parameters.picture_db_root
    # !file_dir     = self.sub_dir_field.text() + "/"
    # file_name    = self.file_field.text().strip()

    if file_name == "":
        return None
    file_name        = file_name.strip()
    sub_dir          = sub_dir.strip()

    full_file_name   = f"{root}/{sub_dir}/{file_name}".replace( "\\", "/" )
    full_file_name   = full_file_name.replace( "///", "/" )  # just in case we have dups
    full_file_name   = full_file_name.replace( "//", "/" )   # just in case we have dups

    print( f"build_pic_filename {full_file_name}")

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
        # msg         = f"display_file, file not found {filename} "
        # AppGlobal.logger.info( msg )
        # rint( msg )
    if not ok:
        filename   = AppGlobal.parameters.pic_nf_file_name
    return filename

#-----------------------------------
def is_delete_ok(   ):
    """
    Returns:
        None.

    """
    msg_box = QMessageBox()
    msg_box.setWindowTitle("Your choice")
    msg_box.setText("Delete ok?")

    # Adding buttons
    choice_no  = msg_box.addButton("No - delete",  QMessageBox.ActionRole)
    choice_yes = msg_box.addButton("Yes - delete", QMessageBox.ActionRole)

    # Set the dialog to be modal (blocks interaction with other windows)
    msg_box.setModal(True)

    # Execute the message box and wait for a response
    msg_box.exec_()

    if msg_box.clickedButton() == choice_no:
        is_ok      = False
        #rint( "Choice A selected" )

    elif msg_box.clickedButton() == choice_yes:
        is_ok      = True
        #int( "Choice B selected" )

    return is_ok

# -------------------------------
def table_widget_no_edit( table_widget  ):
        """
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
    """
    def __init__(self, parent=None, db=None):
        """
        from chat
        """
        super(ReadOnlySqlTableModel, self).__init__(parent, db)

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
    def __init__(self,  ):
        """
        This is the parent for the document
        It holds our tabs

        """
        super().__init__()

        # window title stuff to here?
        # may never be referenced, remove?
        ## move to module level

        self.subwindow_name      = "DocumentBase -- subwindow failed to set"

        # for testing, generalization and ability not to create -- promoted
        self.criteria_tab       = None
        self.list_tab           = None
        self.detail_tab         = None
        self.text_tab           = None
        self.history_tab        = None
        self.picture_tab        = None
        self.criteria_tab_index = None
        self.mapper             = None

        # # get -- set items for a window -- expose as instance var use @property if not
        # # instance var
        # window_title       for  i_window.windowTitle()  and  window_id.windowTitle()
        # menu_action_id     from midi management
        # topic_dict         table, table_id  info --- string make up of something
        # info               for topic dict    get_info
        # table_id
        # table
        # record state        for the primary

        self.detail_table_id           = None    # set in descendant
        self.current_id                = None    # same as above, !! delete one
        self.detail_table_name         = None    # set in descendant
        self.menu_action_id            = None    # set by midi_management id the menu
        # self.record_state
        self.current_tab_index         = 0       # assumed to be criteria

        self.tab_folder                = QTabWidget() # create for descandants

        # may want to keep at end of this init
        AppGlobal.mdi_management.register_document(  self )
        self.tab_folder.currentChanged.connect( self.on_tab_changed )

    def __init_2__xxx( self ):
        """finish off init after desceanant has run its init"""
        self.tab_folder.currentChanged.connect( self.on_tab_changed )
        1/0  # not in current use
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
        mayey that was the property error
        """
        debug_self_detail_tab   = self.detail_tab
        return self.detail_tab.record_state

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
        Args:
            index (QModelIndex): DESCRIPTION.

        !! promote the whole thing from stuff removed there and rest
        might be functioalize if we use an argumen for self.list.tab
        """
        print( f"on_list_clicked  save first if necessary and looks promotable ")
        row                     = index.row()
        column                  = index.column()

        self.list_tab.list_ix   = row

        id_index                = self.list_tab.list_model.index(
            index.row( ), 0 )
        db_key                  = self.list_tab.list_model.data(
            id_index, Qt.DisplayRole )
        print( f"Stuff Clicked on list row {row}, column {
            column}, {db_key=}" )  # " value: {value}" )

        # self.detail_tab.fetch_detail_row_by_id( db_key )
        self.fetch_row_by_id( db_key )

        self.main_notebook.setCurrentIndex( self.detail_tab_index )
        # self.detail_tab.id_field.setText( str( db_key )  ) # fetch currently does not include the id

    #----------------------------
    def on_tab_changed(self, index):
        """
        will kick off criteria select if ...
        what it says, read it
        """
        print( "on_tab_changed need validate update db but may be redundant in some cases so perhaps provide a mechanism to skip" )

        self.validate()
        self.update_db()

        old_index                = self.current_tab_index
        #rint(f"stuf_tabbed_sub_window on_tab_changed from { self.current_tab_index = } to {index = }")
        self.current_tab_index   = index
        #self.tab_page_info()
        if old_index == 0 and index != 0:  # !=0 happens at construct
            self.criteria_tab.criteria_select_if( )

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
        print(f"{self.windowTitle()} has been closed")

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
        go to absolute index from the list tab
        consider second arg a delta
        """
        self.update_db()

        tab                     =  self.list_tab
        no_rows                  = tab.list_model.rowCount()

        if no_rows < 1:
            print( "set_list_to_detail_ix  may need to clear some stuff" )

        list_ix                  = tab.list_ix

        if new_list_ix >= no_rows:
            new_list_ix  =  no_rows -1
            msg     = f"new_list_ix {no_rows = } {new_list_ix = } tried to index past end"
            print( msg )
            AppGlobal.logger.error( msg )

        elif new_list_ix < 0:
            new_list_ix  =  0
            msg     = f"new_list_ix {no_rows = } {new_list_ix = } tired to index before start"
            print( msg )

        # else in range

        tab.list_ix     = new_list_ix
        self.list_tab.list_view.selectRow(  new_list_ix )
        record          = tab.list_model.record( tab.list_ix  )
        id_data         = record.value( "id")
        #rint( f"next_list_to_detail {id_data = } {record = } " )

        print( "set_list_to_detail_ix may be a function for this" )
        self.select_record( id_data )
        # self.detail_tab.select_record( id_data )
        # if self.text_tab:
        #     self.text_tab.select_record( id_data )

    # -----------------------------
    def prior_history_to_detail( self ):
        """
        --- but why not do this from the select that is coming up
            just send the selected record
            and update when the save is done
            function can be record to history( record )  called on the history tab
        """
        history_tab    = self.history_tab
        list_ix        = history_tab.list_ix
        self.set_history_to_detail_ix( list_ix - 1 )

    # -----------------------------
    def next_history_to_detail( self ):
        """

        """
        history_tab    = self.history_tab
        list_ix        = history_tab.list_ix
        self.set_history_to_detail_ix( list_ix + 1 )

    # ------------------------------------------
    def set_history_to_detail_ix( self, new_list_ix   ):
        """

        """
        self.update_db()

        history_tab         = self.history_tab
        list_ix             = history_tab.list_ix
        history_table       = history_tab.history_table
        no_rows             = history_table.rowCount()


        if new_list_ix >= no_rows:
            new_list_ix  =  no_rows -1
            msg     = f"new_history_ix {no_rows = } {new_list_ix = } tried to index past end"
            print( msg )
            AppGlobal.logger.error( msg )

        elif new_list_ix < 0:
            new_list_ix  =  0
            msg     = f"new_history_ix {no_rows = } {new_list_ix = } tired to index before start"
            print( msg )

        # else in range
        ID_COL                  = 1
        history_tab.list_ix     = new_list_ix

        item                    = history_table.item( new_list_ix, ID_COL )
        id_data                 = int( item.text() )
        # id_index                =  history_table.index( new_list_ix, 0 )
        # id_data                 =  history_table.data( id_index, Qt.DisplayRole )
        msg                     = ( f"next_history_to_detail  try to get db_key { new_list_ix = },  {id_data = }" )
        AppGlobal.logger.debug( msg )
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
        compare to   new_record
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

        print( "new_record first validate, then save, wait for except then go on ")

        self.validate()

        self.update_db()


        next_key      = AppGlobal.key_gen.get_next_key( self.detail_table_name )
        print( f"new_record change self.detail_tab.default_new_row( next_key ) " )
        # was self.detail_tab.default_new_row( next_key )

        if  self.detail_tab is not None:
            self.detail_tab.new_record( next_key, option = option )

        if  self.text_tab is not None:
            self.text_tab.new_record( next_key, option = option  )

    # ------------------------------------------
    def criteria_select( self, ):
        """
        uses info in criteria tab to build list in list tab
        uses info from 2 tabs
        """
        # rint( "criteria_select in Plant sub window next pull over channel_select " )
        self.criteria_tab.criteria_select()

    # ------------------------------------------
    def delete( self, ):
        """
        links to main menu bar save  ... might want to delete but look around

        """
        # self.detail_tab.update_detail_row()
        # self.text_tab.update_text_row()
        # rint( "save.... need to complete")

        if not is_delete_ok():
            return

        print( "delete.... the detail items and all that depend on it need to complete and route to update_db ")
        print( "convert to loop?? !! may need to check record state ")

        if self.detail_tab is not None:
            self.detail_tab.delete_all()

        if self.text_tab is not None:
            self.text_tab.delete_all()

        self.current_id     = None

        # self.record_state   = RECORD_DELETE   # this is in detail tab not here
        #self.record_state   = RECORD_NULL

        msg     = f"sUB wINDOE.delete...  ....   for {self.subwindow_name = }"
        print( msg )

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

        except custom_widgets.ValidationIssue as an_except:
            msg     = an_except.args[0]
            #rint( f"{msg = }" )
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Input Issue")
            msg_box.setText( msg )
            choice_a = msg_box.addButton( "Ok", QMessageBox.ActionRole)
            msg_box.setModal( True )
            msg_box.exec_()

            return


        if self.detail_tab is not None:
            self.detail_tab.update_db()

        if self.text_tab is not None:
            self.text_tab.update_db()

        msg     = f"now in stuffdb_tabbed... update_db....   for {self.subwindow_name = }"
        AppGlobal.logger.info( msg )
        print( msg )

    # ---------------------------------------
    def validate( self, ):
        """
        validate all input, likd accept text
        return
            if validation error will throw an exception
            else none
        """
        # self.data_manager.validate(  )

        # if self.get_record_state() == RECORD_NULL:
        #     msg       =  ( "BaseDocument validate do not validate null records this may be unnecesary or redundant")
        #     AppGlobal.logger.info( msg )
        #     return

        if self.detail_tab is not None:
            self.detail_tab.validate()

        if self.text_tab is not None:
            self.text_tab.validate()

        msg     = f"Document Base   validate....   done for {self.subwindow_name = }"
        AppGlobal.logger.info( msg )
        #rint( msg )

    # ---------------------------------------
    def fetch_row_by_id( self, id ):
        """
        promoted
        rename call, delete

        what it says, mostly focused on the detail tab
        some seem to go direct to doucments select_record
        """
        self.select_record( id )

    # ---------------------------------------
    def select_record( self, a_id ):
        """
        what it says, mostly focused on the detail tab
        should be promoted from other tabs
        it look like this could cause an end less loop
        no the tabs have their own method this is ok
        what about photo --- well things do not have one photo except photo itself
        """
        print( "select_record  first validate, then save, wait for except then go on ")

        self.validate()

        self.update_db()


        self.detail_table_id     = a_id     # also need in new and delete
        self.detail_tab.select_record(  a_id )
            # probably a  stuffdb_tabbed_sub_window.DetailTabBase

        if self.text_tab is not None:
            self.text_tab.select_record(  a_id )

        if self.picture_tab is not None:
            self.picture_tab.select_record(  a_id )

        # self.detail_to_history()
        self.main_notebook.setCurrentIndex( self.detail_tab_index )

    # --------
    def popup_delete_question(self):
        """
        Generate a popup ........
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
        what it says, mostly focused on the detail tab -- promote ??
        """
        self.history_tab.record_to_table( record )

    # ------------------------
    def prior_next_picture( self, delta ):
        """
        largely for the Album Picture Tab to navigate from
        this tab  -- promote??
        """
        # if self.photos_tab:
        #     return self.photos_tab.prior_next( delta )
        return   self.detail_tab.prior_next_picture( delta )

    # -----------------------
    def __str__( self ):

        a_str   = ""
        a_str   = ">>>>>>>>>>* DocumentBase  *<<<<<<<<<<<<"


        a_str   = string_util.to_columns( a_str, ["criteria_tab",
                                           f"{self.criteria_tab}" ] )
        a_str   = string_util.to_columns( a_str, ["criteria_tab_index",
                                           f"{self.criteria_tab_index}" ] )
        a_str   = string_util.to_columns( a_str, ["current_id",
                                           f"{self.current_id}" ] )
        a_str   = string_util.to_columns( a_str, ["current_tab_index",
                                           f"{self.current_tab_index}" ] )
        a_str   = string_util.to_columns( a_str, ["detail_tab",
                                           f"{self.detail_tab}" ] )
        a_str   = string_util.to_columns( a_str, ["detail_table_id",
                                           f"{self.detail_table_id}" ] )
        a_str   = string_util.to_columns( a_str, ["detail_table_name",
                                           f"{self.detail_table_name}" ] )
        a_str   = string_util.to_columns( a_str, ["history_tab",
                                           f"{self.history_tab}" ] )
        a_str   = string_util.to_columns( a_str, ["list_tab",
                                           f"{self.list_tab}" ] )
        # a_str   = string_util.to_columns( a_str, ["mapper",
        #                                    f"{self.mapper}" ] )
        a_str   = string_util.to_columns( a_str, ["menu_action_id",
                                           f"{self.menu_action_id}" ] )
        a_str   = string_util.to_columns( a_str, ["picture_tab",
                                           f"{self.picture_tab}" ] )
        a_str   = string_util.to_columns( a_str, ["subwindow_name",
                                           f"{self.subwindow_name}" ] )
        a_str   = string_util.to_columns( a_str, ["tab_folder",
                                           f"{self.tab_folder}" ] )
        a_str   = string_util.to_columns( a_str, ["text_tab",
                                           f"{self.text_tab}" ] )



        # b_str   = self.super().__str__( self )
        # a_str   = a_str + "\n" + b_str

        return a_str



# ---- for detail tab probably  Picture List Tab PicturePictureTab used for text tab base ----------------------------------
# ----------------------------------------
# was class StuffdbTab( QWidget ):
class DetailTabBase( QWidget ):
    """
    used for detail tabs ands.....
    """
    def __init__(self, parent_window ):
        """
        lots of variable may not be used .... clean up later
        """
        print( "init  DetailTabBase  " )
        super().__init__( parent_window )

        self.parent_window       = parent_window

        # self.table_name          = "DetailTabBase unknown, please set"

        self.viewer              = None   # tab may add
        self.add_ts              = None                 # may only be valid for new

          # list of edits containing key words
            # field need to hold string data
                # can build with gui

        #self.deleted_id          = None # change to below

    # tab for a list of photos
        #self.sub_tab_list        = []        # will be called on select
              # and delete with our id here  self.sub_tab_list.append()   or parent_window.    ......
        self.tab_name            = "DetailTabBase -- >> tab failed to set<<< and... "
        # self.field_list          = []  # may not be used, but will be checked
            # check that childred do not also implement this
        self.enable_send_topic_update    = False

        #self.mapper               = None
        self.picture_sub_tab      = None     # in case there is none

        #self.picture_sub_tab      = None   # but usually update in desceandnt
        # or could create and append on demand in the detail window
        # self.picture_sub_tab     = None

        # ----

        # next not right for text windows
        self.table              = parent_window.detail_table_name
        self.table_name         = self.table   # !! eliminate one or other
        self.sub_tab_list        =  []

        print( "init end DetailTabBase  " )


    def post_init(self, ):
        """
        call from child at the end of its init
        __init__ continued
        self.key_word_table_name: set to "" to suppress
        better text have own tab ?
        """
        print( "post_init   DetailTabBase  {self.tab_name  }" )

        model                   = QSqlTableModel(
                            self, AppGlobal.qsql_db_access.db )

        self.model              = model
        self.tab_model          = model  # !! ogase iyt

        #self.table              = self.parent_window.detail_table_name

        model.setTable( self.table )

        # ---- data maanager
        self.data_manager      = data_manager.DataManager( self.model )
        #self.data_manager.next_key_function = self.key_gen     # some_function( table_name )
        if self.key_word_table_name != "":
            self.data_manager.enable_key_words(  self.key_word_table_name  )

        print( f"post_init  end off to self._build_gui() DetailTabBase  {self.tab_name  }" )

        self._build_gui()


    # -----------------------------------------
    def update_db( self, ):
        """
        from russ crud was in phototexttab, probably universal
        looks like can promote to ancestor
        """
        self.data_manager.update_db()


        # if   self.record_state   == RECORD_NULL:
        #     print( "update_db record null no action, return ")
        #     return
        #     # if self.key_word_table_name:
        #     #     self.key_word_obj.string_to_new(( self.get_kw_string()) )

        # elif  self.record_state   == RECORD_NEW:
        #     self.update_new_record()
        #     if self.key_word_table_name:
        #         self.key_word_obj.string_to_new(( self.get_kw_string()) )

        # elif  self.record_state   == RECORD_FETCHED:
        #     self.update_record_fetched()
        #     if self.key_word_table_name:
        #         self.key_word_obj.string_to_new(( self.get_kw_string()) )

        # elif  self.record_state   == RECORD_DELETE:
        #     self.delete_record_update()
        #     if self.key_word_table_name:
        #         self.key_word_obj.string_to_new( "" )

        # else:
        #     print( f"update_db wtf  {self.record_state = } ")
        # if self.key_word_table_name:
        #     self.key_word_obj.compute_add_delete( self.current_id  )
        # #rint( f"update_db record state now:  {self.record_state = } ")
        # #rint( "what about other tabs and subtabs")

    # ---------------------------
    def update_record_fetchedxxxx(self):
        """
        from russ crud  -- copied from PictureTextTab -- now promoted
        what are the fields
        """
        msg    = ( f"update_record_fetched  {self.record_state  = }")
        print( msg )
        AppGlobal.logger.error( msg )
        # model    = self.detail_text_model
        model    = self.tab_model      # QSqlTableModel(
        if not self.record_state  == RECORD_FETCHED:

            msg   = ( f"update_record_fetched bad state, return  {self.record_state  = }")
            print( msg )
            AppGlobal.logger.error( msg )
            return

        id_value = self.id_field.text()
        if id_value:
            # why should we need this
            print( "some save commented out ")
            #model.setFilter(f"id = {id_value}")
            #model.select()
            if model.rowCount() > 0:

                # use mapper or field to record
                if self.mapper:
                    self.mapper.submit()
                else:
                    record = model.record(0)
                    self.field_to_record(  record )
                    model.setRecord(0, record)
                # # ---- timestamps
                # record.setValue( "add_ts",   self.add_ts_field.text()) # should have already been set
                # record.setValue( "edit_ts",  self.edit_ts_field.text())

                #model.submitAll()
                ok   = model_submit_all( model, f"DetailTabBase.update_record_fetched {id_value =}")
                # msg            = f"update_record_fetched Record ( fetched ) saved! {id_value =} fix error check "
                # rint( msg )
                #QMessageBox.information(self, "Save",  msg )

            model.setFilter("")

    # ---------------------------
    def update_new_recordxxxx( self ):
        """
        from russ crud worked   --- from photo_text -- worked
        photo-detal ng need edit trying worked --- move to ancestor

        """
        print( f"DetailTabBase update_new_record  {self.record_state  = }")
        model   = self.tab_model     # QSqlTableModel(
        if not self.record_state  == RECORD_NEW:
            msg       = ( f"save_new_record bad state, return  {self.record_state  = }")
            print( msg )
            return

        record  = model.record()

        self.field_to_record( record )

        model.insertRecord( model.rowCount(), record )

        #model.submitAll()
        if self.mapper:
            self.mapper.submit()
        else:
            record = model.record(0)
            self.field_to_record(  record )
            model.setRecord(0, record)

        ok   = model_submit_all( model, f"DetailTabBase.update_new_record { self.current_id = } ")

        self.record_state    = RECORD_FETCHED
        # msg      =  f"New record saved! { self.current_id = } "
        # rint( msg )
        #QMessageBox.information(self, "Save New", msg )

    # ---------------------------------------
    def validate( self, ):
        """
        validate all input, likd accept text
        validations cause exceptions so return is not really required
        """
        self.data_manager.validate()
        # is_bad   = False
        # for i_field in  self.field_list:
        #     is_bad    = i_field.validate(   )
        #     if is_bad:
        #         break

        # msg     = f" do we need sub_tabs now in stuffdb_tabbed... validate.... {is_bad = }   for {self.tab_name = }"
        # AppGlobal.logger.info( msg )
        # print( msg )
        # return is_bad

    # -------------------------------------
    def get_kw_stringxxx( self,   ):
        """
        get the fields contaning key words
        and concatinate into one string
        self.data_manager.add_field( edit_field )
        """
        print( "in stuffdb tab get_kw_string" )
        a_str  = " "
        for i_edit in self.key_word_edit_list:
            a_str    = a_str + i_edit.get_raw_data()

        print( f" {a_str = }")
        return a_str

    # -------------------------------------
    def delete_all( self,   ):
        """
        delete all under this id   current_id

        """
        print( "in stuffdb tab delete all ")

        self.data_manager.delete_all()
        # model  = self.tab_model

        # # Loop through the rows in reverse order and delete them
        # for row in range(model.rowCount() - 1, -1, -1 ):
        #     model.removeRow(row)

        # # tehee is no view here we are more like a form that we may need to clear self.view.show()

        # if model.submitAll():
        #     model.select()  # Refresh the model to reflect changes in the view
        # else:
        #     model.database().rollback()  # Rollback if submitAll fails
        #     print( "DetailTabBase submitAll fail rollback ")

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

        """
        self.data_manager.new_record( next_key, option = "default" )



        # print( f"DetailTabBase new_record  {self.tab_name} {self.table_name} {next_key} do we do again ?")
        # self.clear_fields( option   = option  )
        # self.record_state           = RECORD_NEW

        # # think we need to use custon_widget
        # #self.id_field.setText( str( next_key ) )
        # self.id_field.set_data( next_key, "integer" )

        # self.current_id             = next_key
        # if self.key_word_table_name:
        #     self.key_word_obj.string_to_old( "" )
        # print( "new_record time stuff may be lost ")

        # print( "new_recordneed to fix up the picture tab if any or does document do it ??")

    # ---------------------------
    def select_record( self, id_value  ):
        """
        from russ crud  works
        move to photo_detail and modify
        then promote
        promoted   seems ok to be here
        """
        self.data_manager.select_record( id_value )
        # record   = None
        # model    = self.tab_model

        #         # consider get rid of thirt if
        # if id_value:
        #     #ia_qt.q_sql_query_model( model, "select_record 1" )
        #     model.setFilter( f"id = {id_value}" )
        #     model.select()

        #     #ia_qt.q_sql_query_model( model, "select_record 2" )
        #     if model.rowCount() > 0:
        #         record                  = model.record(0)
        #         self.id_field.setText( str(record.value("id")) )
        #         self.record_to_field( record )
        #         #self.textField.setText(record.value("text_data"))
        #         self.record_state       = RECORD_FETCHED
        #         self.current_id         = id_value
        #     else:
        #         msg    = f"Record not found! {self.tab_name } {id_value = }"
        #         print( msg )
        #         AppGlobal.logger.error( msg )
        #         #QMessageBox.warning(self, "Select",  msg )
        #     #ia_qt.q_sql_query_model( model, "select_record 3 ancestor " )
        #     # model.setFilter("")  # why what happens if we leave alone
        #           # comment out here seems to fix history should be ok across all tabs
        #     #ia_qt.q_sql_query_model( model, "select_record 4  ancestor" )

        # # may be more like events plantings....  remove Picture soon ? or keep as special

        # if record:
        #     #rint( "in DetailTabBase, now dowing history probably only place should be done on select look for other calls  ")
        #     self.parent_window.record_to_history_table( record )

        # # if self.pictures_tab:
        # #     self.pictures_tab.select_by_id( id_value )

        for i_sub_tab in self.sub_tab_list:
            if i_sub_tab:
                i_sub_tab.select_by_id( id_value )

        # if self.mapper:
        #     self.mapper.setCurrentIndex( 0 )

        #     msg = "set mapper to index 0"
        #     print( msg )
        #     AppGlobal.logger.debug( msg )

        # if self.key_word_table_name:
        #     self.key_word_obj.string_to_old(( self.get_kw_string()) )
        self.send_topic_update()

    # # ------------------------
    # def record_to_field(self, record ):
    #     """
    #     promoted
    #     mov data from fetched record into the correct fields
    #     """
    #     # ---- code_gen: detail_tab -- _record_to_field -- begin code
    #     for i_field in  self.field_list:
    #         i_field.set_data_from_record( record )

    #     # next might be better in select_record but does that have the record
    #     self.parent_window.record_to_history_table( record )

    # # ------------------------
    # def field_to_record( self, record ):
    #     """
    #     trying promote, for new edits

    #     """
    #     for i_field in  self.field_list:
    #         i_field.get_data_for_record( record, self.record_state  )

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

        # if option == "default":
        #     for i_field in self.field_list:
        #        # i_field.clear_data( to_prior = to_prior )
        #        i_field.set_data_to_default(  )

        # elif option == "prior":
        #     for i_field in self.field_list:
        #         i_field.set_data_to_prior(  )

    # -----------------------------------
    def send_topic_update( self, ):
        """
        topics are perhaps better as subjects
        called from select_record and perhaps other
        override,  detail tab
        """
        msg     = ( "send_topic_update needs fixing !! just reenabled ")
        print( msg )
        AppGlobal.logger.error( msg )
        # return
        print( f" send_topic_update  <<<<<<<<<{ self.tab_name = } <<<<<<<<<<<<<<<<<<<< { self.enable_send_topic_update = } " )
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
        a_str   = ">>>>>>>>>>* DetailTabBase *<<<<<<<<<<<<"

        # a_str   = string_util.to_columns( a_str, ["add_ts",
        #                                    f"{self.add_ts}" ] )
        a_str   = string_util.to_columns( a_str, ["current_id",
                                           f"{self.current_id}" ] )
        a_str   = string_util.to_columns( a_str, ["deleted_record_id",
                                           f"{self.deleted_record_id}" ] )
        a_str   = string_util.to_columns( a_str, ["enable_send_topic_update",
                                           f"{self.enable_send_topic_update}" ] )
        # a_str   = string_util.to_columns( a_str, ["field_list",
        #                                    f"{self.field_list}" ] )
        a_str   = string_util.to_columns( a_str, ["key_word_edit_list",
                                           f"{self.key_word_edit_list}" ] )
        a_str   = string_util.to_columns( a_str, ["key_word_obj",
                                           f"{self.key_word_obj}" ] )
        a_str   = string_util.to_columns( a_str, ["key_word_table_name",
                                           f"{self.key_word_table_name}" ] )
        a_str   = string_util.to_columns( a_str, ["mapper",
                                           f"{self.mapper}" ] )
        a_str   = string_util.to_columns( a_str, ["parent_window",
                                           f"{self.parent_window}" ] )
        a_str   = string_util.to_columns( a_str, ["picture_sub_tab",
                                           f"{self.picture_sub_tab}" ] )
        a_str   = string_util.to_columns( a_str, ["pictures_sub_tab",
                                           f"{self.pictures_sub_tab}" ] )
        a_str   = string_util.to_columns( a_str, ["record_state",
                                           f"{self.record_state}" ] )
        a_str   = string_util.to_columns( a_str, ["sub_tab_list",
                                           f"{self.sub_tab_list}" ] )
        a_str   = string_util.to_columns( a_str, ["tab_name",
                                           f"{self.tab_name}" ] )
        a_str   = string_util.to_columns( a_str, ["viewer",
                                           f"{self.viewer}" ] )
        return a_str

# ----------------------------------------
class SubTabBase( QWidget ):
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

        print( "in SubTabBase  tab appendsin to a window list is this correct?? -- maybe ")
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
        print( "update_db  stsw.StuffdbSubSubTab this simple? db commit here??  ")
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

        self.tab_name               = "CriteriaTab set in child"
        self._build_tab()
        self.clear_criteria()

    # -----------------------------
    def add_date_widgets( self, placer, row_lables = ("Edit", "Add") ):
        """
        might want to add lables to the
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
    def _build_top_widgets( self, placer ):
        """
        what it says read, std for all criteria tabs
        """
        placer.new_row()

        # ---- buttons
        a_widget        = QPushButton( "Clear" )
        a_widget.clicked.connect(  self.clear_criteria )
        placer.new_row()
        placer.place( a_widget )

        a_widget        = QPushButton( "ReSelect" )
        a_widget.clicked.connect(  self.parent_window.criteria_select )
        #placer.new_row()
        placer.place( a_widget )

    # -------------------------------
    def add_buttons( self, placer ):
        """
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
        what it says, read
        make our standard date widgets

        return two widgets both same holdover from old code fix sometime , starting and ending widget in a tuple
        """
        #widget                  = QDateEdit()
        widget                   = custom_widgets.CQDateCriteria()   # need types here prehaps !!
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
            print( "no select !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # put in criteria_select  !! self.critera_is_changed = False
        self.critera_is_changed = False

    def criteria_changed( self, is_changed ):
        """
        What it says, read
            note: strip the strings
        """
        self.critera_is_changed  = is_changed
        self.criteria_changed_widget.setText( f"criteria changed {is_changed = }" )

    # -----------------------------
    def get_criteria( self ):
        """
        What it says, read
            note: strip the strings
            promotable
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
            i_criteria.set_data_default()

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

        """
        criteria   = self.get_criteria()
        print( f"show_criteria {criteria}")
        pprint.pprint( criteria )

# ----------------------------------------
class StuffdbHistoryTab( QWidget ):

    def __init__(self, parent_window  ):

        super().__init__()
        self.parent_window   = parent_window

        self.list_ix         = 0    # should be active and selected
        self.ix_seq          = 0    # may be obsolete
        self.ix_col_seq      = 0
        self.ix_col_id       = 1
        self._build_gui()
        self.tab_name        = "StuffdbHistoryTab -- tab failed to set"

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
                pass    # problem in item or talbe >>
                #import pbd
                print( "find_id_in_table error !!")
                #breakpoint()     # pdb.set_trace()  # Start the debugger here

                return - 1

            #rint( f"find_id_in_table {item.text()}" )
            # if no item ,no match
            if item and item.text() == str_id:
                ix_found = row

        #rint( f">>>>>>>>>>>>find_row_with_text {str_id = } {ix_found = }")

        return ix_found

    # ----------------------------
    def on_cell_clicked( self, ix_row, ix_col  ):
        """
        what it says read
        call to self.parent_window so the detail tab selects the id
        probably promote
        """
        table           = self.history_table

        item            = table.item( ix_row, self.ix_col_id  )
        self.list_ix    = ix_row
        a_id             = int( item.text() )
        # msg        = f"on_cell_clicked  Row {ix_row}, Column {self.ix_col_id}, Data: {a_id = }"
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

# ==================================
class TextTabBase( DetailTabBase  ):
    """
    taken from StuffTextTab -- make this the ansistor
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
        self.tab_name            = "TextTabBase should be redefined"
        self.key_word_table_name = ""   # supress key word processing
        # def in child
        # self.table_name          = "stuff"
        # self.tab_name            = "StuffTextTab"

        # model                    = QSqlTableModel(
        #     self, AppGlobal.qsql_db_access.db )
        # self.tab_model           = model  # !! change everywhere
        # # self.detail_text_model   = model # !! remove  everywhere
        # model.setTable( parent_window.text_table_name )


    # -------------------------------------
    def _build_gui( self ):
        """
        what it says read
        Returns:
            none
        """
        tab                 = self
        #tab_layout          = QVBoxLayout(tab)
        tab_layout          = QGridLayout(tab)
            # widget: The widget you want to add to the grid.
            # row: The row number where the widget should appear (starting from 0).
            # column: The column number where the widget should appear (starting from 0).
            # rowSpan (optional): The number of rows the widget should span (default is 1).
            # columnSpan (optional): The number of columns the widget should span (default is 1).
            # alignment (optional): The ali
        # could have a button layout down one side ??

        # ---- id
        edit_field            =  custom_widgets.CQLineEdit(
                                     parent         = None,
                                     field_name     = "id",
                                     db_type        = "integer",
                                     display_type   = "string" )

        self.id_field        = edit_field
        # self.id_field.setValidator( QIntValidator() )
        edit_field.setPlaceholderText("Enter ID")
        self.data_manager.add_field( edit_field, ) # is_key_word = True )
        tab_layout.addWidget( edit_field, 0, 1  )

        ix_row      = 1
        label       = "b1"
        widget = QPushButton( label )
        # widget.clicked.connect( self.combo_reload )
        tab_layout.addWidget ( widget, 1, 0,   )

        # ---- textedit   entry_widget         = QTextEdit()
        edit_field         = custom_widgets.CQTextEdit(
                                    parent         = None,
                                    field_name     = "text_data",
                                    db_type        = "string",   # or text ??
                                    display_type   = "string" )
        entry_widget         = edit_field
        self.text_data_field = edit_field
        edit_field.setPlaceholderText( "Some Long \n   text on a new line " )
        self.data_manager.add_field( edit_field, )
        self.data_manager.add_field( edit_field )
        tab_layout.addWidget( edit_field, 1, 1, 5, 5 )

        ix_row      += 1
        label       = "Copy\nLine"
        widget = QPushButton( label )
        connect_to  =  functools.partial( self.copy_line_of_text, entry_widget )
        widget.clicked.connect( connect_to )
        tab_layout.addWidget ( widget, ix_row, 0,   )

        ix_row   += 1
        label       = "run\npython"
        widget = QPushButton( label )
        connect_to  =  functools.partial( self.run_python, entry_widget )
        widget.clicked.connect( connect_to )
        #widget.clicked.connect( self.do_python )
        tab_layout.addWidget ( widget, ix_row, 0,   )

        ix_row   += 1
        label       = "b4"
        widget = QPushButton( label )
        # widget.clicked.connect( self.combo_reload )
        tab_layout.addWidget ( widget, ix_row, 0,   )

        # self.name_field = QLineEdit()
        # self.name_field.setPlaceholderText("Name")
        # tab_layout.addWidget(self.name_field)

        button_layout = QHBoxLayout()


    # # -----------------------------
    # def add_copy( self, next_key ):
    #     """
    #     could use create default_new_row
    #     what it says
    #         this is for a new row on the window -- no save
    #         fill with default
    #     Returns:
    #         None.
    #     compare to   new_record
    #     """
    #     # capture needed fields
    #     # yt_id    = self.yt_id_field.text()
    #     text_data       = self.text_data_field.text()

    #     self.default_new_row( next_key )

    #     self.text_data_field.setTtext( f"{text_data} \n ------ \n {text_data}")

    # # -----------------------------
    # def add_copy( self, next_key ):
    #     """
    #     could use create default_new_row
    #     what it says
    #         this is for a new row on the window -- no save
    #         fill with default
    #     Returns:
    #         None.
    #     compare to   new_record
    #     """
    #     # capture needed fields
    #     # yt_id    = self.yt_id_field.text()
    #     text_data       = self.text_data_field.text()

    #     self.default_new_row( next_key )

    #     self.text_data_field.setTtext( f"{text_data} \n ------ \n {text_data}")

    # -----------------------------
    def default_new_row_hide(self, next_key ):
        """
        what it says
            this is for a new row on the window -- no save
            needs key but timestamp stuff from detail not text
        arg:
            next_key for table, just trow out if not used
        Returns:
            None.

        """
        self.clear_detail_fields()

        self.text_data_field.setText(
            f"this is the default text for id { next_key=}" )

        # # ---- ??redef add_ts
        # a_ts   = str( time.time() ) + "sec"
        # # record.setValue( "add_ts",  a_ts    )
        # self.add_ts_field.setText(  a_ts )
        # self.edit_ts_field.setText( a_ts )

        self.id_field.setText( str( next_key ) )

    # ----------------------------
    def fetch_detail_row_hide( self, id=None ):
        """
        Args:
            id can be external or as chat has it fetched

        Returns:
            None.
        !! could be promoted
        """
        id      = self.id_field.text()
        print( f"stuff text tab fetch_row { id=}")
        self.fetch_detail_row_by_id( id )

    # -----------------------------
    def fetch_text_row_by_id_hide( self, id   ):
        """
        what it says, read
        or is is not a fetch, a copy over, not what I want
        !! need to fix -- updates may no         t work
        also need to check for more id errors, perhaps
        Args:
            id (TYPE): DESCRIPTION.

        """
        model     = self.detail_text_model
        model.setFilter( (f"id = {id}") )
        model.select()
        if model.rowCount() > 0:
            record = model.record(0)
            self.text_data_field.setText(  record.value(    "text_data"     ))
            # self.name_field.setText(   record.value(    "name"      ))
            # self.url_field.setText(    record.value(     "url"       ))
            # self.mypref_field.setText(str(record.value(  "mypref")   ))
            # self.mygroup_field.setText(record.value(     "mygroup"   ))
        else:

            msg     = f"Fetch Error: No record tor text_data found with the given ID. {
                id = }"
            QMessageBox.warning(self, "Error", msg )
            AppGlobal.logger.error( msg )

        # else:
        #     QMessageBox.warning(self, "Input Error", f"Please enter a valid ID. { id = }")

    # -----------------------------
    def delete_detail_row_hide(self):
        """
        looks like could be promoted -- dbkey needs to stay id
              but need to delete detail_cildren as well
              but need to delete key words as well
        what it says read
         delete_detail_row delete_detail_row
        Returns:
            None.
        """
        model       = self.detail_text_model
        id          = self.id_field.text()
        if id:
            model.setFilter( f"id = {id}" )
            model.select()
            if model.rowCount() > 0:
                model.removeRow(0)

                ok     = model_submit_all( model,  f"StuffTextTab.delete_detail_row {id = }" )
                # QMessageBox.information(
                #     self, "Delete Success", "detail_text_model Record deleted successfully.")
                self.clear_detail_fields()
            else:
                msg   = "Delete Error: No record found with the given ID. { id = } "
                QMessageBox.warning(self, "Error", msg )
                AppGlobal.logger.error( msg )
        else:
            msg  = f"Please enter a valid ID. { id = }"
            QMessageBox.warning(self, "Input Error",
                                "Please enter a valid ID.")
            AppGlobal.logger.error( msg )

    # -------------------------
    def update_text_row_hide(self):
        """
        are we calling i do not see the message box
        what it says, read
        row is the model   detail.model ??
        !! change to update_detail_row
        Returns:
            None.
        update_detail_row update_detail_row
        table name in:
        primary key is     id
        text in            text_data

        """
        model   = self.detail_model
        id      = self.id_field.text()
        if id:
            model.setFilter(f"id = {id}")
            model.select()
            if model.rowCount() > 0:
                record = model.record(0)
                record.setValue( "text_data", self.text_data_field.text() )
                # record.setValue("name",     self.name_field.text())


                if model.setRecord( 0, record ):
                    #model.submitAll()
                    ok     = model_submit_all(
                               model,  f"StuffTextTab.update_text_row {id = }" )
                    msg    = "Text data Record updated successfully. text_data ... wrong error check "
                    AppGlobal.logger.debug( msg )
                    #QMessageBox.information(self, "Update Success", msg )
                else:
                    msg    = f"text data Update Error Failed to update record. text_data {
                        id = }"
                    AppGlobal.logger.error( msg )
                    QMessageBox.warning(self, "Error", msg )
            else:
                msg    = f"No record found with the given ID.text_data {
                    id = } "
                AppGlobal.logger.error( msg )
                QMessageBox.warning(self, "Update Error", msg )
        else:
            msg    = f"Input Error", "Please enter a valid ID.text_data  {id = } "
            AppGlobal.logger.debug( msg )

            QMessageBox.warning(self, "Input Error", msg )

    # ------------------------
    def run_python(self, text_edit ):
        """
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
        lines                   = []
        cursor                  = text_edit.textCursor()

        original_position       = cursor.position()
        cursor.movePosition( cursor.StartOfLine )
        prior_start_of_line     = cursor.position()

        # wat_inspector.go(
        #      msg            = "inspect ",
        #      a_locals       = locals(),
        #      a_globals      = globals(), )

        for ix in range( 20 ):

            cursor.movePosition(cursor.EndOfLine, cursor.KeepAnchor )
            selected_text = cursor.selectedText()

            selected_text   = selected_text.strip()
            if selected_text == "":
                break
            else:
                pass
            lines.append( selected_text + "\n" )

            # Move to the start of the next line 2 steps
            cursor.movePosition(cursor.Down)
            cursor.movePosition(QTextCursor.StartOfLine)
            position       = cursor.position()
            if position == prior_start_of_line:
                print( "hit the end of text")
                break
            else:
                pass

        # print()
        # print()
        # full_text   = "\n".join( lines )
        # print( f"full text\n {full_text}" )

        # lets write a file and try to run it
        file_name  = "temp_stuff.py"
        with open( file_name, 'w') as a_file:
            # this may not have \n at end of line
            a_file.writelines( lines  )

        open_python_file_in_idle(file_name )


    # ------------------------
    def clear_fields_hide(self, to_prior ):
        """
        what it says, read
        what fields, need a bunch of rename here
        clear_detail_fields  clear_detail_fields  !! do differntly for custom controls >>
        """
        self.id_field.clear()
        self.text_data_field.clear()
        # self.name_field.clear()

    # ------------------------
    def field_to_record_hide( self, record ):        # self.url_field.clear()
        # self.mypref_field.clear()
        # self.mygroup_field.clear()
        """
        in photo may be promotable --- need new ancestor
        for the updates, get the gui data into the record
        assume for new add time and id are already there?? or in a self.xxx
        since not sure how works put in instance
        """
        # if self.record_state    == self.RECORD_NEW:  # may be needed
        #     # self.record_id
        #     self.id_field.setText(  str( self.record_id     ) )
        #     pass

        if self.record_state    == RECORD_NEW:  # may be needed
            record.setValue("id", int( self.current_id ) )

        # record.setValue( "add_kw",     self.add_kw_field.text())

        record.setValue( "text_data", self.text_data_field.toPlainText())

        # ---- timestamps
        # record.setValue( "add_ts",   self.add_ts_field.text()) # should have already been set
        # record.setValue( "edit_ts",  self.edit_ts_field.text())

        # new_id     = sexxxxlf.id_field.text()
        # new_text   = self.text_data_field.toPlainText()
        # if new_id and new_text:
        #     record = model.record()
        #     record.setValue("id", int( new_id) )
        #     record.setValue("text_data", new_text)
        #     model.insertRecord( model.rowCount(), record

    # ------------------------
    def record_to_field_hide(self, record ):
        """
        in photo may be promotable
        should be for fetch
        """
        if self.record_state    ==  RECORD_NEW:  # may be needed
            # self.record_id
            self.id_field.setText(  str( self.current_id     ) )

        self.id_field.setText(str(record.value( "id" )))
        # self.textField.setText(record.value("text_data"))
        self.text_data_field.setText(  record.value( "text_data"     ))
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
        print( "TextEditTab.copy_line_of_text"   )

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

        print(f"Copied text: {selected_text = }")

        #rint( "copied text is {1 = } "   )
        return selected_text

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

        self.picture_sub_tab    = None     # but usually update in desceandnt
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

        # !! next is bad -- picture does not hav a picture sub tab
        document           = self.parent_window
        picture_sub_tab    = document.detail_tab.picture_sub_tab  # may be None
        # ---- buttons -- test picture select

        # ---- buttons
        button_layout   = QHBoxLayout(   )
        tab_layout.addLayout( button_layout )

        if picture_sub_tab:   # becaue picture doe not have this
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
        acll from ?
        !! use instead filename  = stuffdb_tabbed_sub_window.fix_pic_filename( filename   )
        """
        if file_name is None:
            file_name = ""   # prevents error Path()

        file_path       = Path( file_name )

        if not file_path.exists():  # look for function to chedk this and may have already been done
            file_name   = AppGlobal.parameters.pic_nf_file_name

        self.viewer.display_file( file_name )
        self.fit_in_view()

    # ---------------------------
    def select_record( self, id_value  ):
        """
        !! this may be promot by mistake
        this is override of parent as we get file name from
        our detail sister tab
        """
        picture_file_name    = self.parent_window.detail_tab.get_picture_file_name()
        #rint( f"picture picture tab, select_record {picture_file_name}")

        self.display_file( picture_file_name )

    # ------------------------------------------
    def select_by_id ( self, id ):
        """
        try to get one that works
        """
        print( f"picture picture tab select_by_id, do I get called ................................select_by_id")

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
        print( f"prior_next {file_name = }")
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
            print( msg )
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
    which is a bit more complicate

    except for table name this should be the same for all items

    we do not really need to fetch any data from the

    photo_subject table

    """
    # ------------------------------------------
    def __init__(self, parent_window ):
        """

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
        self.db             = AppGlobal.qsql_db_access.db

        self._build_gui()

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says, read

        """
        page            = self
        tab             = page

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
        self.view.setModel( self.model )

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
        """
        # ----
        model               =   QSqlQueryModel(   )
        self.model          =   model
        # Set the headers for the columns
        model.setHeaderData( 0, 0, "Photo ID")
        model.setHeaderData( 1, 0, "Name")
        model.setHeaderData( 2, 0, "Photo Filename")

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
    def select_by_id ( self, id ):
        """
        try to get one that works
        """
        table_id        = id
        model           = self.model  #   a QSqlQueryModel()
        table_joined    = self.pictures_for_table

        query           = QSqlQuery()

        # Prepare the SQL statement with bind placeholders
        sql_query = """
        SELECT
           photo.id,
           photo.name,
           photo.file,
           photo.sub_dir
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

        # SELECT
        #    photo.id,
        #    photo.name,
        #    photo.file,
        #    photo.sub_dir
        # FROM
        #     photo_subject
        # JOIN
        #     photo
        # ON
        #     photo_subject.photo_id      = photo.id
        # WHERE
        #     photo_subject.table_joined  = "stuff"
        # AND
        #     photo_subject.table_id      = 3085;



        # test_query_not_used = (
        # """
        # SELECT
        #     photo.id,
        #     photo.name,
        #     photo.photo_fn
        # FROM
        #     photo_subject
        # JOIN
        #     photo
        # ON
        #     photo_subject.photo_id = photo.id
        # WHERE
        #     photo_subject.table_joined = "stuff";

        # """ )
        query.prepare( sql_query )

        # Bind the actual values to the placeholders
        query.bindValue(":table_joined", table_joined )
        query.bindValue(":table_id",     table_id     )

        is_ok  = AppGlobal.qsql_db_access.query_exec_model( query,
                                                  model,
                                                  msg = "PictureListSubTabBase select_by_id" )

        self.view.setModel( model )
        self.set_picture_ix( 0 )

    # ------------------------------------------
    def prior_next( self, delta, absolute = False   ):
        """
        get and put in control the prior or next picture
        using delta to determine which
            # delta = 0 is special see code wy use set_picture_ix

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
            msg     = f"set_picture_ix {no_rows = }  should clear display or no pic pic "
            print( msg )
            file_name        = fix_pic_filename( None   )
            self._display_picture( file_name )
            AppGlobal.logger.debug( msg )
            return file_name

        if new_list_ix >= no_rows:
            new_list_ix  =  no_rows -1
            msg     = f"set_picture_ix {no_rows = } {new_list_ix = } tried to index past end"
            print( msg )
            AppGlobal.logger.debug( msg )

        elif new_list_ix < 0:
            new_list_ix  =  0
            msg     = f"set_picture_ix {no_rows = } {new_list_ix = } tired to index before start"
            print( msg )
            AppGlobal.logger.debug( msg )
        # else in range

        self.list_ix        = new_list_ix
        # fn_index               = self.query_model_read.index( new_list_ix, 1 )
        # file_name              = self.query_model_read.data( fn_index, Qt.DisplayRole )
        ix_fn                =  2  # column number
        ix_sub_dir           =  3
        #fn_item               =  model.item( self.list_ix,  ix_fn )  # may need to be model or ....

        sub_dir              = model.data( model.index( self.list_ix, ix_sub_dir ) )
        file_name            = model.data( model.index( self.list_ix, ix_fn ) )
        # combine next two ??
        fn_item              = build_pic_filename( file_name, sub_dir )
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
        file_name               = fn_item
        msg     = ( f"set_picture_ix { file_name  = }")
        print( msg )
        AppGlobal.logger.debug( msg )

        #rint( f"change to prior next 0 {file_name = }" )
        #self._display_picture_by_fn( file_name )

        #self.picture_tab.display_file( file_name )  # the other tab in sub window
        #rint( "above bad because hard to find self.picture_tab.display_file( file_name )"  )

        self._display_picture( file_name )
        return file_name

    def _display_picture( self, file_name ):
        """
        just do the display no checking
        usually from set_picture_ix
        """
        self.picture_viewer.display_file( file_name )
        print( "really...." )
        other_picture_tab   =  self.parent_window.parent_window.picture_tab
        if other_picture_tab:
            other_picture_tab.display_file( file_name )

# ---- eof ---------------------------


