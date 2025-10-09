#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 08:28:36 2024

old stuff_document_edit.EditStuffEvents( model, keygen, index = None, parent = None)
now
stuff_document_edit.EditStuffEvents(

"""
# ---- tof
# --------------------
if __name__ == "__main__":
    import main

# --------------------

# ---- imports

import logging
import sys

from app_global import AppGlobal
from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtSql import (QSqlDatabase,
                         QSqlDriver,
                         QSqlQuery,
                         QSqlRecord,
                         QSqlRelation,
                         QSqlRelationalDelegate,
                         QSqlRelationalTableModel,
                         QSqlTableModel)

from PyQt5.QtWidgets import (QApplication,
                             QComboBox,
                             QDateTimeEdit,
                             QDialog,
                             QDialogButtonBox,
                             QFormLayout,
                             QGridLayout,
                             QHBoxLayout,
                             QLabel,
                             QLineEdit,
                             QMainWindow,
                             QMessageBox,
                             QPushButton,
                             QSpinBox,
                             QTableView,
                             QVBoxLayout,
                             QWidget)

# ---- imports local

logger          = logging.getLogger( )

# for custom logging level at module
LOG_LEVEL  = 20   # higher is more

# ---- end imports



class EditStuffEvents( QDialog ):
    """
    Dialog for adding or editing a record in the stuff_event table.
    my first tweak before custom edits
    see also the planting_eent  verstion which uses custom edits
    perhaps this should as well

    """

    def __init__(self, parent=None, edit_data=None ):
        """
        includes the building of the form which is not
        done in planting_event


        """
        super().__init__(parent)
        self.setWindowTitle("Add New Event" if edit_data is None else "Edit Event")
        if parent is None:
            1/0 # need parent which is the tab where the model is
        # Create form layout and fields
        form_layout = QFormLayout()

        # ID field
        widget       = QLineEdit()
        self.id_edit = widget
        widget.setReadOnly( True )
        widget.setMaxLength( 10 )
        form_layout.addRow( "ID:", widget )

        # Stuff ID field
        widget             = QLineEdit()
        self.stuff_id_edit = widget
        widget.setMaxLength(10)
        widget.setReadOnly( True )
        form_layout.addRow( "Stuff ID:", self.stuff_id_edit )

        # Event date/time field (stored as integer timestamp)
        self.event_date_edit = QDateTimeEdit(QDateTime.currentDateTime())
        form_layout.addRow("Event Date:", self.event_date_edit)

        # DLR field (integer)

        self.dlr_spinbox = QSpinBox()
        self.dlr_spinbox.setRange(0, 9999)
        form_layout.addRow("DLR:", self.dlr_spinbox)

        # Comment field
        self.comment_edit = QLineEdit()

        self.comment_edit.setMaxLength(150)
        self.comment_edit.setMinimumWidth( 350  )
        form_layout.addRow("Comment:", self.comment_edit)

        # Type field
        self.type_combobox = QComboBox()
        # Add your event types here
        self.type_combobox.addItems(["Type1", "Type2", "Type3"])
        form_layout.addRow("Type:", self.type_combobox)

        # If we're editing, populate the fields with the existing data
        if edit_data is not None:

            a_id     = edit_data["id"]
            if type( a_id ) == int:
                a_id   = str( a_id )

            self.id_edit.setText( a_id )

            # ---- stuff id
            data     = edit_data["stuff_id"]
            if type( data ) == int:
                data   = str( data )

            self.stuff_id_edit.setText( data )

            # Convert timestamp to QDateTime
            dt    = QDateTime()
            dt.setSecsSinceEpoch(edit_data["event_dt"])
            self.event_date_edit.setDateTime(dt)

            pennies     = int( float( edit_data["dlr"] ) )
            self.dlr_spinbox.setValue(int( pennies ) )

            self.comment_edit.setText(edit_data["cmnt"])

            # Find and set the index for the type
            index = self.type_combobox.findText(edit_data["type"])
            if index >= 0:
                self.type_combobox.setCurrentIndex(index)

        # Button box
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(button_box)

        self.setLayout( main_layout )

    def get_form_data(self):
        """
        Get the data from the form fields as a dictionary.
        """
        a_id   = self.id_edit.text().strip()
        if a_id == "":
            a_id  = 0
        else:
            a_id  = int( a_id )

        stuff_id = self.stuff_id_edit.text().strip()
        if stuff_id == "":
            stuff_id  = 0
        else:
            stuff_id  = int( stuff_id )

        data = {
            #"id": int( self.id_edit.text() ),
            "id":        a_id,

            #"stuff_id":  int( self.stuff_id_edit.text() ),
            "stuff_id":   stuff_id,

            "event_dt":  int(self.event_date_edit.dateTime().toSecsSinceEpoch()),
            "dlr":       self.dlr_spinbox.value(),
            "cmnt":      self.comment_edit.text(),
            "type":      self.type_combobox.currentText()
        }
        msg    = f"EditStuffEvents.get_form_data {data = }"
        print( msg )
        return data


# ---- eof
