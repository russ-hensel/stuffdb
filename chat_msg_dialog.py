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
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time

from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLabel, QTextEdit, QProgressBar,
    QDialog
)


# ----------------------------------------------------------------------
# Worker thread – does the counting
# ----------------------------------------------------------------------
class CounterWorker(QThread):
    text_signal     = pyqtSignal(str)   # append text
    progress_signal = pyqtSignal(int)   # 1 to 10
    finished_signal = pyqtSignal()      # done

    def run(self):
        for i in range(10):
            print(i)                                 # console output
            self.text_signal.emit(str(i))
            self.progress_signal.emit(i + 1)
            time.sleep(0.5)                          # <-- demo only

        self.finished_signal.emit()


# ----------------------------------------------------------------------
# Dialog that shows progress
# ----------------------------------------------------------------------
class CounterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Counting in progress…")
        self.setModal(True)                     # blocks main window
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        layout = QVBoxLayout(self)

        # ----- output text ------------------------------------------------
        layout.addWidget(QLabel("Output:"))
        self.txt = QTextEdit(readOnly=True)
        layout.addWidget(self.txt)

        # ----- progress bar -----------------------------------------------
        layout.addWidget(QLabel("Progress:"))
        self.pbar = QProgressBar(minimum=0, maximum=10)
        layout.addWidget(self.pbar)

        self.resize(380, 260)


# ----------------------------------------------------------------------
# Main application window
# ----------------------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Application")
        self.resize(600, 400)

        # Central widget with a button to start the counter
        central = QWidget()
        self.setCentralWidget(central)
        vbox = QVBoxLayout(central)

        btn = QPushButton("Start Counter Dialog")
        btn.clicked.connect(self.start_counter)
        vbox.addWidget(btn)
        vbox.addStretch()

    # ------------------------------------------------------------------
    def start_counter(self):
        """Create dialog, worker, connect signals and show."""
        dlg = CounterDialog(self)                # <-- main window is parent
        dlg.show()                               # non-blocking

        worker = CounterWorker(self)
        worker.text_signal.connect(dlg.txt.append)
        worker.progress_signal.connect(dlg.pbar.setValue)
        worker.finished_signal.connect(dlg.accept)   # close when done

        worker.start()


# ----------------------------------------------------------------------
def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())      # application stays alive after dialog closes


if __name__ == "__main__":
    main()