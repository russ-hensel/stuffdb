#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 10:31:01 2024

@author: russ
"""

"""


I forgot to say the tab should be able to
updated rows, so I have changed my request
just a bit to include it.

Now I want:

I am using python qt 5.15.3) with an SQLite database.

the database has a table defined as:


CREATE TABLE channel (
    id       INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    yt_id    VARCHAR( 40 ),
    name     VARCHAR( 40 ),
    url      VARCHAR( 100 ),
    mypref   INTEGER,
    mygroup  VARCHAR( 20 )

I would like a qtwindow with a tab.
On the tab should be a widgets for displaying
one row from the db, perhaps linked by
a  QDataWidgetMapper.

The tab should have 3 buttons so as to be able to:
    fetch a single row based on its id.
       and provide for its update
    delete a fetched row.
    create a new empty row
        and provide for its update

Can you create sample Python code for this?



detail_db_subwindow.py

"""

#

# ------------------- chat
"""

import sqlite3

def setup_database():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS channel (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            yt_id VARCHAR(40),
            name VARCHAR(40),
            url VARCHAR(100),
            mypref INTEGER,
            mygroup VARCHAR(20)
        )
    ''')
    conn.commit()
    conn.close()

setup_database()




"""

import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
                             QTabWidget, QLabel, QMessageBox)
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlRecord
from PyQt5.QtGui import QIntValidator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SQLite Database Viewer")
        self.setGeometry(100, 100, 600, 400)

        # Initialize the database connection
        self.init_db()

        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a tab widget
        self.tabs = QTabWidget()
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(self.tabs)

        # Add the tab
        self.add_tab()

    def init_db(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName('example.db')
        if not self.db.open():
            QMessageBox.critical(None, "Database Error", self.db.lastError().text())

        self.model = QSqlTableModel( self, self.db )
        self.model.setTable("channel")
        self.model.select( )

    def add_tab(self):
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)

        self.id_field = QLineEdit()
        self.id_field.setValidator(QIntValidator())
        self.id_field.setPlaceholderText("Enter ID")
        tab_layout.addWidget(self.id_field)

        self.yt_id_field = QLineEdit()
        self.yt_id_field.setPlaceholderText("YouTube ID")
        tab_layout.addWidget(self.yt_id_field)

        self.name_field = QLineEdit()
        self.name_field.setPlaceholderText("Name")
        tab_layout.addWidget(self.name_field)

        self.url_field = QLineEdit()
        self.url_field.setPlaceholderText("URL")
        tab_layout.addWidget(self.url_field)

        self.mypref_field = QLineEdit()
        self.mypref_field.setValidator(QIntValidator())
        self.mypref_field.setPlaceholderText("Preference")
        tab_layout.addWidget(self.mypref_field)

        self.mygroup_field = QLineEdit()
        self.mygroup_field.setPlaceholderText("Group")
        tab_layout.addWidget(self.mygroup_field)

        button_layout = QHBoxLayout()

        fetch_button = QPushButton("Fetch")
        fetch_button.clicked.connect(self.fetch_row)
        button_layout.addWidget(fetch_button)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_row)
        button_layout.addWidget(delete_button)

        create_button = QPushButton("Create")
        create_button.clicked.connect(self.create_row)
        button_layout.addWidget(create_button)

        update_button = QPushButton("Update")
        update_button.clicked.connect(self.update_row)
        button_layout.addWidget(update_button)

        tab_layout.addLayout(button_layout)

        self.tabs.addTab(tab, "Channel")

    def fetch_row(self):
        id = self.id_field.text()
        if id:
            self.model.setFilter(f"id = {id}")
            self.model.select()
            if self.model.rowCount() > 0:
                record = self.model.record(0)
                self.yt_id_field.setText(record.value("yt_id"))
                self.name_field.setText(record.value("name"))
                self.url_field.setText(record.value("url"))
                self.mypref_field.setText(str(record.value("mypref")))
                self.mygroup_field.setText(record.value("mygroup"))
            else:
                QMessageBox.warning(self, "Fetch Error", "No record found with the given ID.")
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a valid ID.")

    def delete_row(self):
        id = self.id_field.text()
        if id:
            self.model.setFilter(f"id = {id}")
            self.model.select()
            if self.model.rowCount() > 0:
                self.model.removeRow(0)
                self.model.submitAll()
                QMessageBox.information(self, "Delete Success", "Record deleted successfully.")
                self.clear_fields()
            else:
                QMessageBox.warning(self, "Delete Error", "No record found with the given ID.")
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a valid ID.")

    def create_row(self):
        yt_id   = self.yt_id_field.text()
        name    = self.name_field.text()
        url     = self.url_field.text()
        mypref = self.mypref_field.text()
        mygroup = self.mygroup_field.text()

        record = self.model.record()
        record.setValue("yt_id", yt_id)
        record.setValue("name", name)
        record.setValue("url", url)
        record.setValue("mypref", int(mypref) if mypref else None)
        record.setValue("mygroup", mygroup)

        if self.model.insertRecord(-1, record):
            self.model.submitAll()
            QMessageBox.information(self, "Create Success", "Record created successfully.")
            self.clear_fields()
        else:
            QMessageBox.warning(self, "Create Error", "Failed to create record.")

    def update_row(self):
        id = self.id_field.text()
        if id:
            self.model.setFilter(f"id = {id}")
            self.model.select()
            if self.model.rowCount() > 0:
                record = self.model.record(0)
                record.setValue("yt_id", self.yt_id_field.text())
                record.setValue("name", self.name_field.text())
                record.setValue("url", self.url_field.text())
                record.setValue("mypref", int(self.mypref_field.text()) if self.mypref_field.text() else None)
                record.setValue("mygroup", self.mygroup_field.text())

                if self.model.setRecord(0, record):
                    self.model.submitAll()
                    QMessageBox.information(self, "Update Success", "Record updated successfully.")
                else:
                    QMessageBox.warning(self, "Update Error", "Failed to update record.")
            else:
                QMessageBox.warning(self, "Update Error", "No record found with the given ID.")
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a valid ID.")

    def clear_fields(self):
        self.id_field.clear()
        self.yt_id_field.clear()
        self.name_field.clear()
        self.url_field.clear()
        self.mypref_field.clear()
        self.mygroup_field.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
