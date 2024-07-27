#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 09:22:07 2024

@author: russ

query_model    =  sql_query_model_plus.SqlQueryModelPlus()
SqlQueryModelPlus

allows insert of row


"""

# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    main.main()
# --------------------

# ---- import

from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5.QtCore import Qt


class  SqlQueryModelPlus( QSqlQueryModel ):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.additional_row = []

    def addRow(self, row_data):
        self.additional_row = row_data
        self.layoutChanged.emit()

    # row count here messed up some of my other code, but chat put it here
    # def _rowCount(self, parent=None):
    #     count = super().rowCount(parent)
    #     if self.additional_row:
    #         count += 1
    #     return count

    # def data(self, index, role=Qt.DisplayRole):
    #     if not index.isValid() or role != Qt.DisplayRole:
    #         return None

    #     if index.row() < super().rowCount():
    #         return super().data(index, role)
    #     elif index.row() == super().rowCount():
    #         return self.additional_row[index.column()]
    #     return None
