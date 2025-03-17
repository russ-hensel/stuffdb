#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 09:02:44 2025

@author: russ
"""


# ---- tof

# ---- imports

# ---- end imports


#-------------------------------

        # I have a model TableModel( headers )  base on QAbstractTableModel
        # And a proxy_model         = QSortFilterProxyModel()
        #        wher i  proxy_model.setSourceModel( self.model )

        #  and finally a view          = QTableView()

        # I can set the column headers on the Table Model but I am
        # having trouble setting the column widths.

        # Where is this done and is there anything special in the order of operations?



import sys
from PyQt5.QtWidgets import QApplication, QTableView, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QSortFilterProxyModel


class TableModel(QAbstractTableModel):
    def __init__(self, headers, data, parent=None):
        super().__init__(parent)
        self._headers = headers
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        elif role == Qt.BackgroundRole and index.column() == 0:
            return QColor("#f0f0f0")
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]
        return None


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Define headers and sample data
        headers = ["Photo ID", "Name", "Photo Filename"]
        data = [
            [1, "Alice", "alice.jpg"],
            [2, "Bob", "bob.png"],
            [3, "Charlie", "charlie.jpeg"],
            [4, "David", "david.bmp"],
        ]

        # Create the table model
        self.model = TableModel(headers, data)

        # Create a QSortFilterProxyModel for sorting/filtering
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)

        # Set up the view
        self.view = QTableView()
        self.view.setModel(self.proxy_model)

        # Set column widths
        self.view.setColumnWidth(0, 80)   # Photo ID
        self.view.setColumnWidth(1, 120)  # Name
        self.view.setColumnWidth(2, 500)  # Photo Filename

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

        # Window settings
        self.setWindowTitle("QTableView Example with QSortFilterProxyModel")
        self.resize(450, 250)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())




# ---- eof

