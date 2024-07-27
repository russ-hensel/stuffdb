#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 10:01:46 2024

@author: russ
"""

"""


"""

# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    main.main()

# --------------------




# ---- import  -- pyqt from import_qt.py
from PyQt5.QtGui import (
    QIntValidator,
    )

from PyQt5.QtGui import (
    QStandardItemModel,
    QStandardItem,
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


from   app_global import AppGlobal


# ----------------------------------------
class CustomSubWindow( QMdiSubWindow ):

    def __init__(self,  ):

        super().__init__()


    # --------------------------------
    def closeEvent(self, event):

        """
        """
        AppGlobal.mdi_management.delete_menu_by_title(  self.windowTitle( ) )

        self.on_close()
        event.accept()

        return

        # reply = QMessageBox.question(self, 'Message', 'Are you sure you want to close this window?',
        #                              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        # if reply == QMessageBox.Yes:
        #     self.on_close()
        #     event.accept()
        # else:
        #     event.ignore()

    # --------------------------------
    @pyqtSlot()
    def on_close(self):
        print(f"{self.windowTitle()} has been closed")

