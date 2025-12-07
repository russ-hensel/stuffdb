#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 16:41:04 2025

@author: russ
"""


# ---- tof

# ---- imports

# ---- end imports


#-------------------------------




"""

# ---- eofSuppose you are an skilled programmer using Python and
pyqt5  ( based on QT5 ).  Consider the following problem and
write  some python qt5 code to solve it.

I have a function that is counting:

def counter():

    for ix in range(10):
        print( ix )
        # output here to dialog

before the function begins to run I would like to open a dialog
like window, and then when the function runs
I would like to output some text to the dialog, see comment
in code after print.

Could you write a short application to do this?
"""

import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal
import time

class Worker(QThread):
    update_signal = pyqtSignal(str)

    def run(self):
        for ix in range(10):
            print(ix)  # Keeps the original print to console
            self.update_signal.emit(str(ix))  # Outputs to dialog
            time.sleep(0.5)  # Added sleep to visualize progressive updates; remove if not needed

class CounterDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Counter Output")
        self.layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.layout.addWidget(self.text_edit)
        self.setLayout(self.layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = CounterDialog()
    dialog.show()
    worker = Worker()
    worker.update_signal.connect(dialog.text_edit.append)
    worker.start()
    sys.exit(app.exec_())