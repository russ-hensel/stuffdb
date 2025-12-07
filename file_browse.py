#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 10:18:28 2024

@author: russ
"""



# --------------------
if __name__ == "__main__":
    import main
    main.main()
# --------------------



#import ia_qt


import sys

import gui_qt_ext

from qt_compat import QApplication, QAction, exec_app, qt_version
from PyQt.QtWidgets import QMainWindow, QToolBar, QMessageBox



from PyQt.QtCore import Qt
from PyQt.QtSql import (QSqlDatabase,
                         QSqlDriver,
                         QSqlQuery,
                         QSqlRecord,
                         QSqlRelation,
                         QSqlRelationalDelegate,
                         QSqlRelationalTableModel,
                         QSqlTableModel)
# ----QtWidgets layouts
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
                             QVBoxLayout,
                             QWidget)

# ---- local imports
# import  tracked_qsql_relational_table_model



# ---- end imports


class FileBrowse( QDialog ):
    """
    what it says, read?
    see our test code in rshlib, not clear this adds anything ??/




    """
    # ------------------------------------------
    def __init__(self,   parent_window  = None,     ) :
        """
        Args:


        Returns:
            None.

        """
        super().__init__( parent_window )

        self.parent_window  = parent_window
        msg                 = "File Browse"
        self.setWindowTitle( msg  )
        self._build_gui()

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says, read?
        """

        self.layout             = QVBoxLayout( self )
        button_layout           = QHBoxLayout( self )

        a_widget                = gui_qt_ext.FileBrowseWidget(  )  # def __init__(self, parent=None, entry_width=None):

        self.layout.addWidget(  a_widget )

        self.layout.addLayout( button_layout )

        # ----
        a_widget                 = QPushButton("Ok")
        #self.cancel_button       = a_widget
        a_widget.clicked.connect(  self.accept )
        button_layout.addWidget( a_widget )

# ---- eof