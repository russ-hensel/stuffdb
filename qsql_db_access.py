#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 16:41:23 2024

@author: russ
"""
# ---- imports
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
my reference list of qt imports comes from import_qt.py

PyQt5.QtSql.QSqlError



"""

# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    main.main()
# --------------------





# ---- begin pyqt from import_qt.py
# ---- QtGui
from PyQt5.QtGui import (
    QStandardItemModel,
    QStandardItem,
    QIcon,
           )
# ---- QtCore
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
    QToolBar,
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
    QVBoxLayout
    )

# ----QtWidgets Boxs, Dialogs
from PyQt5.QtWidgets  import (
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

from PyQt5.QtGui import (
    QIntValidator,
    )

# ---- QtSql
from PyQt5.QtSql import (
    QSqlDatabase,
    QSqlTableModel,
    QSqlQuery,
    QSqlError
    )

import sqlite3

# ---- imports local
from   app_global import AppGlobal
import ia_qt



# ----------------------------------------
class QsqlDbAccess(   ):
    """

    """
    def __init__( self,   ):
        """


        """

        self.connection   = None
        self.db           = None   # use as interface


        self.init_db()

    # --------------------------------
    def init_db( self, ):
        """
        why not just get_connection

        print( "Channel Subwindow init_db" )
        self.db = QSqlDatabase.addDatabase( AppGlobal.parameters.db_type )
        self.db.setDatabaseName(            AppGlobal.parameters.db_fn )
        if not self.db.open():
            QMessageBox.critical( None, "Database Error", self.db.lastError().text())

        db = AppGlobal.qsql_db_access.db
        xxxAppGlobal.db    = self.db   # globla avail
        db appears to be the connection

        """
        print( "QsqlDbAccess  init_db()" )
        self.db = QSqlDatabase.addDatabase( AppGlobal.parameters.db_type  )
        self.db.setDatabaseName(            AppGlobal.parameters.db_fn   )


        if not self.db.open():
            msg    = "Database Error: {self.db.lastError().databaseText()}"
            QMessageBox.critical(
                None,
                "databasenot open - Error!", msg
                                )

        print(  ia_qt.q_sql_database( self.db,
                                      msg           = "in init_db()",
                                      include_dir    = False) )

    # --------------------------------
    def get_connectionxxx( self, ):
        """
        consider in an object of its own
        is this how we connect it is unclear how this works, just a stab in dark
        uncleare where this needs to be located ...
        """
        if  self.connection:
            return self.connection

        else:
            # db_type    =  ..... ??
            self.connection = QSqlDatabase.addDatabase( AppGlobal.parameters.db_type  )
            self.connection.setDatabaseName( AppGlobal.parameters.db_fn   )


        if not self.connection.open():
            QMessageBox.critical(
                None,
                "Connection not open - Error!",
                "Database Error: %s" % self.connection.lastError().databaseText(),
            )

        msg      = f"get_connection for { AppGlobal.parameters.db_fn}"
        print( msg )
        AppGlobal.logger.debug( msg )

        return self.connection


    # --------------------------------
    def get_dbxx( self, ):
        """
        consider in an object of its own
        is this how we connect it is unclear how this works, just a stab in dark
        uncleare where this needs to be located ...
        """
        self.db = QSqlDatabase.addDatabase( AppGlobal.parameters.db_type  )
        self.db.setDatabaseName(            AppGlobal.parameters.db_fn   )


        print(  ia_qt.q_sql_database( self.db,
                                      msg           = "in get_db()",
                                     include_dir    = True ) )


        if not self.db.open():
            msg    = "Database Error: {self.db.lastError().databaseText()}"
            QMessageBox.critical(
                None,
                "databasenot open - Error!", msg
                                )


    def get_additional_connectionxxx(self):
        """
        you better remember to close
        can I make a context thing for it?

        Returns:
            connection (TYPE): DESCRIPTION.
        connection    = AppGlobal.qsul_db_access.get_additional_connection()
        """
        # Use the same SQLite connection for additional operations
        db              = QSqlDatabase.database()
        connection      = sqlite3.connect(db.databaseName())

        return connection


        # cursor = connection.cursor()
        # cursor.execute("SELECT * FROM records WHERE id = ?", (1,))
        # result = cursor.fetchall()
        # print(result)
        # connection.close()import sqlite3