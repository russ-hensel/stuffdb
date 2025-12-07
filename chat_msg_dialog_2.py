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

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QTextEdit,
    QProgressBar, QLabel
)


class Worker(QThread):
    """Runs the counter in a background thread."""
    update_signal   = pyqtSignal(str)   # text to append
    progress_signal = pyqtSignal(int)   # progress bar value
    finished_signal = pyqtSignal()      # emitted when loop ends

    def run(self):
        for ix in range(10):
            print(ix)                                   # keep console output
            self.update_signal.emit(str(ix))
            self.progress_signal.emit(ix + 1)           # 1 to 10
            time.sleep(0.5)                             # demo only – remove later

        self.finished_signal.emit()                     # done


class CounterDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Counter with Progress")
        self.setGeometry(300, 300, 400, 300)

        # ---- layout -------------------------------------------------
        layout = QVBoxLayout()

        # Text output
        self.text_edit = QTextEdit(readOnly=True)
        layout.addWidget(QLabel("Output:"))
        layout.addWidget(self.text_edit)

        # Progress bar
        self.progress_bar = QProgressBar(minimum=0, maximum=10)
        layout.addWidget(QLabel("Progress:"))
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)


def main():
    app = QApplication(sys.argv)

    dlg = CounterDialog()
    dlg.show()

    worker = Worker()
    worker.update_signal.connect(dlg.text_edit.append)
    worker.progress_signal.connect(dlg.progress_bar.setValue)

    worker.finished_signal.connect(dlg.accept)   # close when done

    # optional: quit the whole app when the dialog is closed
    #dlg.finished.connect(app.quit)

    worker.start()
    app.exec_()
    #sys.exit(app.exec_())


if __name__ == "__main__":
    main()