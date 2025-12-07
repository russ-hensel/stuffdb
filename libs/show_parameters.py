#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 08:28:36 2024

stuff_document_edit.EditStuffEvents( model, keygen, index = None, parent = None)



"""

# ---- tof

# --------------------
if __name__ == "__main__":
    import main
    main.main()
# --------------------


#import sys



from qt_compat import QApplication, QAction, exec_app, qt_version
from PyQt.QtWidgets import QMainWindow, QToolBar, QMessageBox
from qt_compat import Qt, DisplayRole, EditRole, CheckStateRole
from qt_compat import TextAlignmentRole
from qt_compat import MoveStart, KeepAnchor



from PyQt.QtCore import Qt
from PyQt.QtSql import (QSqlDatabase,
                         QSqlDriver,
                         QSqlQuery,
                         QSqlRecord,
                         QSqlRelation,
                         QSqlRelationalDelegate,
                         QSqlRelationalTableModel,
                         QSqlTableModel)
from PyQt.QtGui import QFont

from PyQt.QtWidgets import (QApplication,
                             QComboBox,
                             QDialog,
                             QFormLayout,
                             QGridLayout,
                             QHBoxLayout,
                             QLabel,
                             QLineEdit,
                             QMainWindow,
                             QMessageBox,
                             QPushButton,
                             QTableView,
                             QTextEdit,
                             QVBoxLayout,
                             QWidget)

# ---- local imports
# import  tracked_qsql_relational_table_model

import parameters
from   app_global import AppGlobal

class DisplayParameters( QDialog ):
    """
    dialog to display parameters

    """
    # ------------------------------------------
    def __init__(self,  parent ):
        """
        Args:

        Returns:
            None.

        """
        super().__init__( parent )
        self.parent         = parent  # parent may be a function use parent_window
        self.parent_window  = parent
        msg   = "Display Parameters "

        self.setWindowTitle( msg  )

        qt_xpos     = 10
        qt_ypos     = 10
        qt_width    = 1000
        qt_height   = 600
        self.tab_help_dict   = { }
        self.setGeometry(  qt_xpos,
                           qt_ypos ,
                           qt_width,
                           qt_height  )

        self._build_gui()

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says, read?
        """
        layout              = QVBoxLayout( self )
        self.layout         = layout

        text_edit           = QTextEdit()
        # layout.addWidget(text_edit, 4, 0, 1, 3)  # Row 4, Column 0, RowSpan 1, ColumnSpan 3
        self.text_edit      = text_edit
        font = QFont( "Courier New" )  # Set a monospaced font "Courier New"
        font.setPointSize( 10 )
        text_edit.setFont(font)

        layout.addWidget( text_edit )

        # parm_text           = str( parameters.PARAMETERS )
        parm_text           =  str( AppGlobal.parameters )

        cursor = text_edit.textCursor()
        cursor.insertText( parm_text )

        # cursor.movePosition(cursor.Start)
        cursor.movePosition( MoveStart, KeepAnchor )  # 5 6 compat
        text_edit.setTextCursor(cursor)
        text_edit.ensureCursorVisible()

        # cursor = text_edit.textCursor()
        # cursor.insertText( parm_text )

        # --- ADD/REPLACE THESE LINES ---
        cursor.clearSelection()                  # removes the selection
       # cursor.movePosition(cursor.Start)        # move cursor to the very beginning
        text_edit.setTextCursor(cursor)          # apply the new cursor (no selection)
        text_edit.setReadOnly(True)               # write-protect the widget
        # --------------------------------





        #  ---- buttons
        button_layout           = layout

        a_widget                = QPushButton("OK")
        self.save_button        = a_widget
        a_widget.clicked.connect( self.accept )
        button_layout.addWidget( a_widget )

# ---- eof
