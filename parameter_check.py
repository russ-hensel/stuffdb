#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 08:34:26 2025

@author: russ
"""
# ---- tof
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
    main.main()
# --------------------

"""
check --- posibbly fix?



"""

# ---- imports
from pathlib import Path
from PyQt5.QtWidgets import (
                             QInputDialog,
                             QLabel,
                             QLineEdit,
                             QListWidget,
                             QMainWindow,
                             QMdiArea,
                             QMdiSubWindow,
                             QMenu,
                             QMessageBox,
                                 )


import adjust_path

import parameters
from app_global import AppGlobal
# ---- end imports


PARAMETERS   = parameters.PARAMETERS

def check_parameters( ):
    """ """

    pic_nf_file_name    = PARAMETERS.pic_nf_file_name
    picture_db_root     = PARAMETERS.picture_db_root
    picture_db_sub      = PARAMETERS.picture_db_sub

    picture_dir_path   = Path().joinpath( picture_db_root, picture_db_sub  )
    #str( picture_dir_path )
    if not picture_dir_path.exists( ):
        msg      = ( f"{picture_dir_path} not valid")
        QMessageBox.information( AppGlobal.main_window,
                                     "Bad Parameter Setting ", msg )
    # else:
    #     msg      = ( f"{picture_dir_path} exists")
    #     QMessageBox.information( AppGlobal.main_window,
    #                                     "ok Parameter Setting", msg )
#check_new_pictures()

    icon                = PARAMETERS.icon
    file                = Path( icon )
    if not file.exists( ):
        msg      = ( f"Icon {file = } not valid")
        QMessageBox.information( AppGlobal.main_window,
                                     "Bad Parameter Setting", msg )
    # else:
    #     msg      = ( f"{picture_dir_path} exists")
    #     QMessageBox.information( AppGlobal.main_window,
    #                                  "ok Parameter Settings", msg )
# ---- end imports


#-------------------------------






# ---- eof