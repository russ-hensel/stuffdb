#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""

KEY_WORDS:      custom text edit tab rsh
CLASS_NAME:     CQTextEditWidgetTab
WIDGETS:        CQTextEdit
STATUS:         unknown
TAB_TITLE:      CQTextEditWidget

         self.help_file_name     =  "find_this_file.txt"

"""
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main_qt
    #main.main()
# --------------------
# # --------------------
# if __name__ == "__main__":
#     #----- run the full app
#     import qt_fitz_book
#     qt_fitz_book.main()
# # --------------------


import glob
import inspect
import json
import math
import os
import subprocess
import sys
import time
from collections import namedtuple
from datetime import datetime
from functools import partial
from random import randint
from subprocess import PIPE, STDOUT, Popen, run

import pyqtgraph as pg  # import PyQtGraph after PyQt5
import wat
from PyQt5 import QtGui
from PyQt5.QtCore import (QAbstractListModel,
                          QAbstractTableModel,
                          QDate,
                          QDateTime,
                          QModelIndex,
                          QSize,
                          Qt,
                          QTime,
                          QTimer)
from PyQt5.QtGui import QColor, QImage, QPalette, QTextCursor, QTextDocument
# sql
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt5.QtWidgets import (QAction,
                             QApplication,
                             QButtonGroup,
                             QCheckBox,
                             QComboBox,
                             QDateEdit,
                             QDateTimeEdit,
                             QDial,
                             QDoubleSpinBox,
                             QFontComboBox,
                             QGridLayout,
                             QGroupBox,
                             QHBoxLayout,
                             QLabel,
                             QLCDNumber,
                             QLineEdit,
                             QListView,
                             QListWidget,
                             QListWidgetItem,
                             QMainWindow,
                             QMenu,
                             QMessageBox,
                             QProgressBar,
                             QPushButton,
                             QRadioButton,
                             QSizePolicy,
                             QSlider,
                             QSpinBox,
                             QStyledItemDelegate,
                             QTableView,
                             QTableWidget,
                             QTableWidgetItem,
                             QTabWidget,
                             QTextEdit,
                             QTimeEdit,
                             QVBoxLayout,
                             QWidget)

import parameters

import utils_for_tabs as uft
import wat_inspector
import custom_widgets



# ---- end imports

print_func_header   = uft.print_func_header




#  --------
class CQTextEditWidgetTab( QWidget ) :
    def __init__(self):
        """

        some content from and there may be more
        /mnt/WIN_D/Russ/0000/python00/python3/_projects/rshlib/gui_qt_ext.py

        """
        super().__init__()
        self.help_file_name     =  "find_this_file.txt"
        self._build_gui()

    # -----------------------
    def _build_gui(self,   ):
        """
        all build on a local QWidget
        count : const int
        currentData : const QVariant
        currentIndex : int
        currentText : QString
        duplicatesEnabled : bool
        editable : bool
        """
        tab_page      = self
        #layout        = QVBoxLayout( tab_page )
        layout        = QGridLayout( tab_page )
        button_layout = QHBoxLayout(   )

        # Create QTextEdit widget
        text_edit = custom_widgets.CQTextEdit()
        #text_edit =  QTextEdit()
        # layout.addWidget(text_edit, 4, 0, 1, 3)  # Row 4, Column 0, RowSpan 1, ColumnSpan 3
        self.text_edit  = text_edit

        # lets put in some starting text
        ex_text   = 5 * (

        """
-------------------
1 And you know the sun's settin' fast,
2 And just like they say, nothing good ever lasts.
3 Well, go on now and kiss it goodbye,
4 But hold on to your lover,
5 'Cause your heart's bound to die.
6 Go on now and say goodbye to our town, to our town.
7 Can't you see the sun's settin' down on our town, on our town,
8 Goodnight.
        """ )

        cursor = text_edit.textCursor()
        cursor.insertText( ex_text )

        layout.addWidget( text_edit, 0, 0, 1, 1)   # args are
            # widget: The widget you want to add to the grid.
            # row: The row number where the widget should appear (starting from 0).
            # column: The column number where the widget should appear (starting from 0).
            # rowSpan (optional): The number of rows the widget should span (default is 1).
            # columnSpan (optional): The number of columns the widget should span (default is 1).
            # alignment (optional): The ali

        # ---- buttons
        layout.addLayout ( button_layout, 1, 0, 1, 1 )



        widget = QPushButton( "delete\n_text" )
        widget.clicked.connect(lambda: self.delete_text(text_edit))
        widget.setMaximumWidth(150)
        button_layout.addWidget( widget,   )

        widget = QPushButton( "inspect\n_widget" )
        widget.clicked.connect(lambda: self.inspect_widget(text_edit))
        widget.setMaximumWidth(150)
        button_layout.addWidget( widget,   )

        widget = QPushButton( "change\n_widget" )
        widget.clicked.connect(lambda: self.change_widget( text_edit ))
        widget.setMaximumWidth(150)
        button_layout.addWidget( widget,   )

        widget = QPushButton( "copy_line_of_text" )
        widget.clicked.connect(lambda: self.copy_line_of_text( text_edit ))
        widget.setMaximumWidth(150)
        button_layout.addWidget( widget,   )

        widget = QPushButton( "copy_n_\nlines_of_text" )
        widget.clicked.connect(lambda: self.copy_n_lines_of_text( text_edit, 5 ))
        widget.setMaximumWidth(150)
        button_layout.addWidget( widget,   )

        insert_button = QPushButton("insert\n_text")
        insert_button.clicked.connect(lambda: self.insert_text(text_edit, "Inserted Text"))
        widget        = insert_button
        #group_placer.new_row( )
        button_layout.addWidget( widget,  )

        copy_selected_button = QPushButton("copy_selected\n_text")
        copy_selected_button.clicked.connect(lambda: self.copy_selected_text(text_edit))
        widget = copy_selected_button
        # layout.addWidget(copy_selected_button, 6, 0)
        #group_placer.new_row( )
        button_layout.addWidget( widget,   )

        widget = QPushButton("clear\n_text")
        widget.clicked.connect( lambda: self.clear_text( ) )
        clear_button = widget
        # layout.addWidget(copy_selected_button, 6, 0)
        #group_placer.new_row( )
        button_layout.addWidget( widget,   )

        # label       = "mutate\n"
        # widget      = QPushButton( label )
        # widget.clicked.connect( self.mutate )
        # button_layout.addWidget( widget )

        # ----
        label       = "inspect\n"
        widget      = QPushButton( label )
        widget.clicked.connect( self.inspect )
        button_layout.addWidget( widget )

        # ---- breakpoint
        label       = "breakpoint\n"
        widget      = QPushButton( label )
        widget.clicked.connect( self.breakpoint )
        button_layout.addWidget( widget )



    # ---------------------------------------
    def display_string( self, a_string, update_now = False ):
        """
        !! we may phase out for print_string  or the reverse ??
             make one call the other
        print to message area, with scrolling and
        log if we are configured for it

        parameters.gui_text_log_fn    = False  # "gui_text.log"
                                               # a file name or something false


        parameters.log_gui_text       = False # True or false to log text
        parameters.log_gui_text_level = 10    # logging level for above

        !! add parameter clear_msg = True or false

        """
        print(  f"in display_string, with a_string = {a_string}")
        # return
        #   try  !!!  QTextEdit.clear()
        cursor = self.text_edit.textCursor()
        # cursor.movePosition( QTextCursor::End )
        cursor.insertText( a_string )

    #  --------
    def print_message(self, text):
        """
        what it says
        """
        print_func_header( "print_message" )
        print("Button clicked:", text)

    #  --------
    def clear_text( self ):
        """
        what is says, see also delete_text
        """
        print_func_header( "clear_text" )
        self.text_edit.clear()

    #-------------------
    def delete_text(self, text_edit):
        """
        what it says
        """
        print_func_header( "delete_text" )
        text_edit.clear()

    #  --------
    def copy_text(self, text_edit):
        """
        what it says
        """
        print_func_header( "copy_text" )
        selected_text      = text_edit.toPlainText()
        QApplication.clipboard().setText(selected_text)
        print(  f" copy_text -> {selected_text }" )

    #  --------
    def copy_all_text( self, text_edit ):
        """
        what it says
        from chat, test?
        """
        print_func_header( "copy_all_text" )
        # Save current cursor position
        cursor = text_edit.textCursor()
        original_position = cursor.position()


        text_edit.selectAll()
        text_edit.copy()   #  goes to clipboard
        all_text = self.text_edit.toPlainText()

        # Restore cursor to its original position
        cursor.setPosition(original_position)
        text_edit.setTextCursor(cursor)
        return  all_text


    #--------------------
    def insert_text(self, text_edit, text):
        """
        insert text at the cursor position
        """
        print_func_header( "insert_text" )

        cursor = text_edit.textCursor()
        cursor.insertText(text)

    #----------------------------
    def copy_selected_text(self, text_edit, ):
        """
        """
        print_func_header( "copy_selected_text" )

        selected_text = text_edit.textCursor().selectedText()
        QApplication.clipboard().setText(selected_text)
        print(  f" copy_selected_text -> {selected_text }" )

    #----------------------
    def copy_n_lines_of_text(self, text_edit, num_lines ):
        """
        for cursor see:
        https://doc.qt.io/qtforpython-5/PySide2/QtGui/QTextCursor.html#synopsis


        chat:
            .....
            can get stuck at bottom of text
        """
        print_func_header( "copy_n_lines_of_text" )
        print( f"{num_lines = }")
        print( "also finds x y for the cursor")
        cursor = text_edit.textCursor()

        # Save the original cursor position
        original_position       = cursor.position()

        cursor.movePosition(cursor.StartOfLine)
        prior_start_of_line     = cursor.position()
        # List to store the next lines
        lines = []

        # Collect the next `num_lines` lines
        for _ in range( num_lines ):
            # Select the line from the start to the end
            cursor_rect = text_edit.cursorRect(cursor)
            x = cursor_rect.x()
            y = cursor_rect.y()
            print( f"cursor at {x =} {y =}")

            cursor.movePosition(cursor.EndOfLine, cursor.KeepAnchor)
            line_text = cursor.selectedText()

            # Add the selected line to the list
            lines.append(line_text)

            # Move to the start of the next line -- take 2 moves ??
            cursor.movePosition(cursor.Down)
            cursor.movePosition(QTextCursor.StartOfLine)
            position       = cursor.position()
            if position == prior_start_of_line:
                print( "hit the end")
                break
            else:
                prior_start_of_line     = position
            cursor_rect = text_edit.cursorRect(cursor)
            x = cursor_rect.x()
            y = cursor_rect.y()
            print( f"cursor  down at {x =} {y =}")


        # Restore the original cursor position
        cursor.setPosition(original_position)
        self.text_edit.setTextCursor(cursor)

        # Print or return the list of lines
        print(f"Next {num_lines} lines:",  )
        print(f"  {len(lines) = }" )
        for i_line in lines:
            print( i_line )
        return lines

    #----------------------
    def copy_line_of_text(self, text_edit):
        """
        chat:
        With a QTextWidge holding some text:
        from the cursor position copy the text from the
        beginning of the line to the end of the line.
        """
        print_func_header( "copy_line_of_text" )

        cursor              = text_edit.textCursor()
        # Save the original cursor position
        original_position   = cursor.position()
        cursor.movePosition( cursor.StartOfLine )

        # Select the text from the beginning to the end of the line
        cursor.movePosition(cursor.EndOfLine, cursor.KeepAnchor)
        selected_text = cursor.selectedText()
        # print(f"Copied text: {selected_text = }")

        # Optionally, copy to the system clipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(selected_text)

        # Restore the original cursor position
        cursor.setPosition(original_position)
        self.text_edit.setTextCursor(cursor)

        print(f"Copied text: {selected_text = }")

    #----------------
    def inspect_widget(self, what_arg ):
        """
        in a QTextEdit how do i find the position of the cursor
        move the cursor to some position, move the cursor to the top, or bottom
        """
        print_func_header( "inspect_widget" )
        print( "\n >>>> inspect_widget.inspect_widget  -- to do "   )
        print( "some cursor stuff in copy__")
        print( f"copy_all_text {self.copy_all_text( self.text_edit )}" )

    #--------------------
    def change_widget(self, text_edit ):
        """
        in a QTextEdit how do i find the position of the cursor
        move the cursor to some positext_edit.show()tion, move the cursor to the top, or bottom

        # Move the cursor by 5 characters while keeping the selection
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 5)

        # Apply the modified cursor to the QTextEdit to reflect the selection
        text_edit.setTextCursor(cursor)
        """
        print( "\n>>>>change_widget   -- to do "   )
        print( "some cursor stuff in copy__")

        # Ensure that the cursor is visible and the widget scrolls to it
        text_edit.ensureCursorVisible()

        cursor = text_edit.textCursor()
        cursor.setPosition(10)  # Moves the cursor to position 10 in the text
        text_edit.setTextCursor(cursor)
        # Move the cursor by 5 characters while keeping the selection
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 5)
        # Apply the modified cursor to the QTextEdit to reflect the selection
        text_edit.setTextCursor(cursor)
        text_edit.show()
        # time.sleep( 1 )

        print( "\n>>>>change_widget   -- to do "   )

    # ------------------------
    def inspect(self):
        """
        the usual
        """
        print_func_header( "inspect" )

        # make some locals for inspection
        my_tab_widget = self
        parent_window = self.parent( ).parent( ).parent().parent()

        wat_inspector.go(
             msg            = "inspect !! add more locals ",
             # inspect_me     = self.people_model,
             a_locals       = locals(),
             a_globals      = globals(), )

    # ------------------------
    def breakpoint(self):
        """
        keep this in each object so user breaks into that object
        """
        print_func_header( "breakpoint" )
        breakpoint()


