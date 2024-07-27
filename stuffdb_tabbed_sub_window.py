#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 10:01:46 2024


"""


# --------------------
if __name__ == "__main__":
    import main
    main.main()
# --------------------


# ---- begin pyqt from import_qt.py
from PyQt5.QtGui import (
    QIntValidator,
    )

from PyQt5.QtGui import (
    QStandardItemModel,
    QStandardItem,
                        )
# ---- QtCore
# -------- xx
from PyQt5.QtCore  import  (
    QDate,
    QModelIndex,
    QTimer,
    Qt,
    pyqtSlot,
                            )

# ----QtWidgets
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QAction,

    QDateEdit,
    QMenu,
    QAction,
    QLineEdit,
    QActionGroup,
    QApplication,
    QDockWidget,
    QTabWidget,



    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QSpinBox,
    QMdiSubWindow,
    QTextEdit,
    QButtonGroup,

    )

# ----QtWidgets big
from PyQt5.QtWidgets import (
    QAction,
    QMenu,
    QApplication,
    QMainWindow,

    QTableView,
    QFrame,
    QMainWindow,
    QMdiArea,
    QMdiSubWindow,
    QMdiArea,
    QMdiSubWindow,
    )

# ----QtWidgets layouts
from PyQt5.QtWidgets import (
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    )

# ----QtWidgets Boxs, Dialogs
from PyQt5.QtWidgets import (
    QAction,
    QActionGroup,
    QDockWidget,
    QFileDialog,
    QInputDialog,

    QLabel,
    QListWidget,
    QMenu,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QCheckBox,
    QComboBox,
    )

# ---- QtSql
from PyQt5.QtSql import (
    QSqlDatabase,
    QSqlTableModel,
    QSqlQuery
    )

# ---- more imports
import ia_qt
from   app_global import AppGlobal


# ----------------------------------------
class StuffdbTabbedSubWindow( QMdiSubWindow ):

    def __init__(self,  ):

        super().__init__()

        # window title stuff to here?
        # may never be referenced, remove?
        self.RECORD_NULL         = 0
        self.RECORD_FETCHED      = 1
        self.RECORD_NEW          = 2
        self.RECORD_DELETE       = 3

        self.subwindow_name      = "StuffdbTabbedSubWindow -- subwindow failed to set"

        # for testing, generalization and ability not to create -- promoted
        self.criteria_tab       = None
        self.list_tab           = None
        self.detail_tab         = None
        self.text_tab           = None
        self.history_tab        = None
        self.criteria_tab_index = None
# missing photo tab ???



    # --------------------------------
    def closeEvent(self, event):

        """
        """
        AppGlobal.mdi_management.delete_menu_by_title(  self.windowTitle( ) )

        self.on_close()
        event.accept()

    # --------------------------------
    @pyqtSlot()
    def on_close( self ):
        print(f"{self.windowTitle()} has been closed")


    # ---- subwindow interactions
    # -----------------------------
    def next_list_to_detail( self ):
        """

        based on code in python programming and development
        Returns:
            None.

        """
        tab                =  self.list_tab
        tab.list_ix += 1
        if  tab.list_ix >    tab.list_model.rowCount() - 1:
            tab.list_ix   =  tab.list_model.rowCount() - 1
            # beep and return
            #self.list_ix    = 0

        record          = tab.list_model.record( tab.list_ix  )
        id_data         = record.value( "id")
        print( f"next_list_to_detail {id_data = } {record = } " )

        #self.detail_tab.fetch_detail_row_by_id( id_data )
        self.detail_tab.select_record( id_data )
        self.text_tab.select_record( id_data )

        #self.detail_tab.id_field.setText( str( id_data )  ) # fetch currently does not include the id

    # -----------------------------
    def prior_list_to_detail( self ):
        """
        based on code in python programming and development
        Returns:
            None.

        """
        tab                =  self.list_tab
        tab.list_ix -= 1
        if  tab.list_ix <    0:
            tab.list_ix   =  0
            print( "and you are at the beginning" )
            #!! is retrun ok
            # frequency_hz   = 2500  # windows only
            # duration_ms    = 1000
            # winsound.Beep( frequency_hz, duration_ms )
            # beep and return
            #self.list_ix    = 0

        record          = tab.list_model.record( tab.list_ix  )
        id_data         = record.value( "id")
        #rint( f"next_list_to_detail {id_data = } {record = } " )

        # self.detail_tab.fetch_detail_row_by_id( id_data )
        self.detail_tab.select_record( id_data )
        self.text_tab.select_record( id_data )

        #self.detail_tab.id_field.setText( str( id_data )  ) # fetch currently does not include the id

    #-------------------------------------
    def new_record( self ):
        """
        looks promotable, lets try this is the promote
        was  ---- default_new_record  changing to crud code  new_record
        defaults values for a new row in the detail and the
        text tabs

        Changes state of detail and related tabs

        """
        next_key      = AppGlobal.key_gen.get_next_key( self.detail_table_name )
        print( "new_record change self.detail_tab.default_new_row( next_key ) " )
        # was self.detail_tab.default_new_row( next_key )

        if  self.detail_tab is not None:
            self.detail_tab.new_record( next_key )

        if  self.text_tab is not None:
            self.text_tab.new_record( next_key )



    # -----------------------------
    def prior_history_to_detail( self ):
        """
        !! promote as nothing seem to depend on which window type
        based on code in python programming and development
        Returns:
            None.

        """
        history_tab   = self.history_tab
        history_model = self.history_tab.history_model
        row_count     = history_model.rowCount()
        if row_count  <= 0:
            print( "next_history_to_detail Beep, no rows in history" )
            return

        self.history_tab.list_ix -= 1

        if self.history_tab.list_ix  < 0:
            self.history_tab.list_ix  = 0
            print( "next_history_to_detail Beep, hit begin_in history" )

        id_index                =  history_model.index( self.history_tab.list_ix, 0 )
        db_key                  =  history_model.data( id_index, Qt.DisplayRole )
        print( f"prior_history_to_detail  rty to get db_key { self.history_tab.list_ix = },  {db_key = }" ) # " value: {value}" )

        self.detail_tab.select_record( db_key )
        self.text_tab.select_record(   db_key )
        # self.detail_tab.fetch_detail_row_by_id( db_key )
        # self.detail_tab.id_field.setText( str(  db_key )  ) # fetch currently does not include the id

    # -----------------------------
    def next_history_to_detail( self ):
        """
        !! promote as nothing seem to depend on which window type
        based on code in python programming and development
        Returns:
            None.

        """
        history_tab   = self.history_tab
        history_model = self.history_tab.history_model
        row_count     = history_model.rowCount()
        if row_count  <= 0:
            print( "next_history_to_detail Beep, no rows in history" )
            return

        self.history_tab.list_ix += 1

        if self.history_tab.list_ix  > row_count - 1:
            self.history_tab.list_ix  = row_count - 1
            print( "next_history_to_detail Beep, hit end in history" )
             # beep and return ??

        id_index                =  history_model.index( self.history_tab.list_ix, 0 )
        db_key                  =  history_model.data( id_index, Qt.DisplayRole )
        print( f"next_history_to_detail  rty to get db_key { self.history_tab.list_ix = },  {db_key = }" )

        #self.detail_tab.fetch_detail_row_by_id( db_key )

        self.detail_tab.select_record( db_key )
        self.text_tab.select_record(   db_key )

        #self.detail_tab.id_field.setText( str( db_key )  ) # fetch currently does not include the id

        # // SET THE TAB?

    # ---- testing, probably delete
    # --------------------------------------
    def create_test_tab_content(self, text):
        """
        this is just for testing delete soon ( ver5 )
        what it says, read
        was a second one in old_ref

        return
            layout tab for placement

        """
        tab         = QWidget()
        layout      = QVBoxLayout(tab)
        label       = QLabel(text)
        layout.addWidget(label)
        return tab

    # --------------------------
    def update_db( self,   ):
        """
        also know as update -- update detail tab and text...
        """
        #self.detail_tab.db_update()

        if self.detail_tab is not None:
            self.detail_tab.update_db()

        if self.text_tab is not None:
            self.text_tab.update_db()

        msg     = "now in stuffdb_tabed... update_db.... need to complete and route to db_update -- done ??"
        print( msg )

    # --------
    def popup_delete_question(self):
        """
        Generate a popup ........
        consider add more info later
        """
        msgbox  =  QMessageBox()
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

    # -----------------------------------
    def detail_to_history( self, ):
        """
        what it says, read
        links two sub_windows

        """
        index    = self.detail_tab.tab_model.index( 0, 0 )
        ia_qt.q_sql_query_model( self.detail_tab.tab_model, "detail_to_history ancestor" )
        self.add_row_history( index )

# ----------------------------------------
class StuffdbTab( QWidget ):

    def __init__(self,  ):

        super().__init__()
        self.RECORD_NULL         = 0
        self.RECORD_FETCHED      = 1
        self.RECORD_NEW          = 2
        self.RECORD_DELETE       = 3

        self.add_ts              = None                 # may only be valid for new
        self.new_record_id       = None                 # may only be valid for new ??
        self.record_state        = self.RECORD_NULL     # take out of descandants
        #self.deleted_id          = None # change to below
        self.deleted_record_id   = None

        self.tab_name            = "StuffdbTab -- tab failed to set"

    # ---------------------------
    def update_record_fetched(self):
        """
        from russ crud  -- copied from PhotoTextTab -- now promoted
        what are the fields
        """
        print( f"update_record_fetched  {self.record_state  = }")
        # model    = self.detail_text_model
        model    = self.tab_model
        if not self.record_state  == self.RECORD_FETCHED:
            print( f"update_record_fetched bad state, return  {self.record_state  = }")
            return

        id_value = self.id_field.text()
        if id_value:
            model.setFilter(f"id = {id_value}")
            model.select()
            if model.rowCount() > 0:
                record = model.record(0)

                self.field_to_record(  record )
                # # ---- timestamps
                # record.setValue( "add_ts",   self.add_ts_field.text()) # should have already been set
                # record.setValue( "edit_ts",  self.edit_ts_field.text())

                model.setRecord(0, record)
                model.submitAll()
                msg            = f"update_record_fetched Record ( fetched ) saved! {id_value =}"
                print( msg )
                QMessageBox.information(self, "Save",  msg )
            model.setFilter("")

    # ---------------------------
    def update_new_record( self ):
        """
        from russ crud worked   --- from phot_text -- worked
        photo-detal ng need edit tryint worked --- move to ancestor

        """
        print( f"StuffdbTab update_new_record  {self.record_state  = }")
        model    = self.tab_model
        if not self.record_state  == self.RECORD_NEW:
            print( f"save_new_record bad state, return  {self.record_state  = }")
            return

        record = model.record()

        self.field_to_record( record )

        model.insertRecord( model.rowCount(), record )
        model.submitAll()
        self.record_state    = self.RECORD_FETCHED
        msg      =  f"New record saved! { self.new_record_id = } "
        print( msg )
        #QMessageBox.information(self, "Save New", msg )

    # -----------------------------------------
    def update_db( self, ):
        """
        from russ crud was in phototexttab, probably universal
        looks like can promote to ancestor
        """
        if   self.record_state   == self.RECORD_NULL:
            print( "update_db record null no action, return ")

        elif  self.record_state   == self.RECORD_NEW:
            self.update_new_record()

        elif  self.record_state   == self.RECORD_FETCHED:
            self.update_record_fetched()

        elif  self.record_state   == self.RECORD_DELETE:
            self.delete_record_update()

        else:
            print( f"update_db wtf  {self.record_state = } ")

        print( f"update_db record state now:  {self.record_state = } ")

    # ---------------------------
    def select_record( self, id_value  ):
        """
        from russ crud  works
        move to photo_detail and modigy
        then promote
        promoted   seems ok to be here
        """
        model    = self.tab_model
        msg      = f"select_record {self.tab_name } {id_value = }"
        print( msg )
                # consider get rid of thirt if
        if id_value:
            #ia_qt.q_sql_query_model( model, "select_record 1" )
            model.setFilter( f"id = {id_value}" )
            model.select()
            #ia_qt.q_sql_query_model( model, "select_record 2" )
            if model.rowCount() > 0:
                record = model.record(0)
                self.id_field.setText( str(record.value("id")) )
                self.record_to_field( record )
                #self.textField.setText(record.value("text_data"))
                self.record_state       = self.RECORD_FETCHED
            else:
                msg    = f"Record not found! {self.tab_name } {id_value = }"
                print( msg )
                QMessageBox.warning(self, "Select",  msg )
            #ia_qt.q_sql_query_model( model, "select_record 3 ancestor " )
            # model.setFilter("")  # why what happes if we leave alone
                  # comment out here seems to fix history should be ok across all tabs
            #ia_qt.q_sql_query_model( model, "select_record 4  ancestor" )
    # ---------------------
    def delete_record(self):
        """
        from russ crud  --- think ok in photo_text
        will move same to detail tab .... testing here
        ok in photo_detail
        try promote -- ok
        """
        if  self.record_state  == self.RECORD_DELETE:
            print( f"delete_record already in state    {self.record_state  = } will return")
            return

        if  self.record_state  == self.RECORD_NEW:
            print( f"delete_record record is new   {self.record_state  = } clear fields")
            self.clear_fields()
            self.record_state  = self.RECORD_NULL
            return

        self.record_state       = self.RECORD_DELETE
        id_value                = self.id_field.text()
        self.deleted_record_id  = id_value  # may have datatype issues here ??
        self.clear_fields()

    # ---------------------------
    def new_record(self, a_key ):
        """
        from russ crud
        photo_detail ok
        promote
        """
        print( f"new_record  {self.record_state  = } { a_key = } you may have pending updates")

        # if not self.record_state  == record_fetched:
        #     print( f"save_record_fetched bad state, return  {self.record_state  = }")
        #     return
        print( f"new_record  from {self.record_state  = }")
        self.clear_fields()
        #new_id                  = self.key_gen.get_next_key()

        self.new_record_id      = a_key
        self.id_field.setText( str( a_key ) )
        # self.text_data_field.setText( f"this is default text for {new_id} get code from default_new_row")

        self.record_state       = self.RECORD_NEW

    # ---------------------
    def delete_record_update(self):
        """
        from russ crud  --- think ok in photo_text
        try in photo_detail  ok
        promote
        """
        model    = self.tab_model
        if not self.record_state  == self.RECORD_DELETE:
            print( f"delete_record_update bad state, return  {self.record_state  = }")
            return
        id_value    = self.deleted_record_id
        if id_value:
            model.setFilter(f"id = {id_value}")
            model.select()
            if model.rowCount() > 0:
                model.removeRow(0)
                model.submitAll()
                self.clear_fields()  # will fix record state
                self.record_state       = self.RECORD_NULL
                msg        = "Record deleted! {id_value = } "
                print( msg )
                #QMessageBox.information(self, "Delete", msg )
            model.setFilter( "" )

# ---- eof ---------------------------