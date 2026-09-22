#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 08:55:37 2026

@author: russ
"""

# ---- tof

#

# ---- imports
import os



# ---- imports local -- then constants

def test_1():
    import os
    print("QT_API =", os.environ.get("QT_API"))

    import qtpy
    print("qtpy API =", qtpy.API_NAME)
    print("qtpy QT version =", qtpy.QT_VERSION)

    from PyQt6.QtCore import QT_VERSION_STR
    print("PyQt6 Qt =", QT_VERSION_STR)


def test_2():
    import sys
    import os
    print(sys.executable)

    print( f"{os.environ.get("QT_API") = }" )

    import qtpy
    print(qtpy.API_NAME)

    from qtpy.QtWidgets import QApplication
    print(QApplication)

    import os
    os.environ["QT_API"] = "pyqt6"

    import qtpy
    print(qtpy.API_NAME)


    # import os; os.environ['QT_API']='pyqt6'
    # import qtpy; print(qtpy.API_NAME, qtpy.QT_VERSION)
    # from qtpy.QtWebEngineWidgets import QWebEngineView; print('webengine ok')




test_1()
test_2()

# ---- eof ---------------------------


