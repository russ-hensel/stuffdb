#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
module of helpers for >>py to extend functionality beyond just stuffdb.py ...
"""


# ---- tof

# ---- imports

# ---- end imports


#-------------------------------


from PyQt5.QtWidgets import (  QMessageBox, )

def confirm_continue( msg ):

    msg_box    = QMessageBox()
    msg_box.setIcon( QMessageBox.Information )
    msg_box.setText( msg )
    msg_box.setWindowTitle( "Continue?" )
    msg_box.setStandardButtons(  QMessageBox.Yes | QMessageBox.No )

    msg_box.setDefaultButton( QMessageBox.No  )

    ret    = msg_box.exec_()
    if ret == QMessageBox.No:
        1/0
        return False
    return True



# ---- eof