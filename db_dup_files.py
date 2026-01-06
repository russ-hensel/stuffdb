#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
just a bit of test in /mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/stuffdb/test/test_db_dup_files.py


"""


# ---- tof
#import adjust_path
# --------------------
if __name__ == "__main__":
    import main
# --------------------

# ---- imports
import functools
import inspect
import logging
import pprint
import subprocess
import os
import time

from   pathlib import Path
# from datetime import datetime
import datetime 



#from functools import partial
from pathlib import Path

from qt_compat import QApplication, QAction, exec_app, qt_version


# from PyQt.QtWidgets import QMainWindow, QToolBar, QMessageBox
# from qt_compat import Qt, DisplayRole, EditRole, CheckStateRole
# from qt_compat import TextAlignmentRole
# from qt_compat import QSizePolicy_Expanding, QSizePolicy_Minimum  # and look at qt_compat there may be more



# from PyQt.QtCore   import QDate, QModelIndex, Qt, QTimer, pyqtSlot
# from PyQt.QtCore   import Qt, QDateTime
# from PyQt.QtWidgets import QStyledItemDelegate
# from PyQt.QtGui import (QFont,
#                          QIntValidator,
#                          QStandardItem,
#                          QStandardItemModel,
#                          QTextCursor)

from PyQt.QtSql import (QSqlDatabase,
                         QSqlQuery,
                         QSqlQueryModel,
                         QSqlRelation,
                         QSqlRelationalDelegate,
                         QSqlRelationalTableModel,
                         QSqlTableModel)

# #from PyQt.QtGui import ( QAction, QActionGroup, )

# from PyQt.QtWidgets import (
#                              QFileDialog,
#                              QApplication,
#                              QButtonGroup,
#                              QCheckBox,
#                              QComboBox,
#                              QDialog,
#                              QDateEdit,
#                              QDockWidget,
#                              QFileDialog,
#                              QFrame,
#                              QGroupBox,
#                              QGridLayout,
#                              QHBoxLayout,
#                              QHeaderView,
#                              QInputDialog,
#                              QLabel,
#                              QLineEdit,
#                              QListWidget,
#                              QMainWindow,
#                              QMdiArea,
#                              QMdiSubWindow,
#                              QMenu,
#                              QMessageBox,
#                              QPushButton,
#                              QSpacerItem,
#                              QSpinBox,
#                              QSizePolicy,
#                              QTableView,
#                              QTableWidget,
#                              QTableWidgetItem,
#                              QTabWidget,
#                              QTextEdit,
#                              QVBoxLayout,
#                              QWidget)

 

logger          = logging.getLogger( )

# for custom logging level at module
LOG_LEVEL  = 10   # higher is more


# import collections
import parameters
# import data_dict
# import check_fix

# #import gui_qt_ext
# import info_about
#import key_words
#import string_util
# import text_edit_ext
#import table_model
#import wat_inspector
from app_global     import AppGlobal
# import qsql_utils

#import ex_qt
#import exec_qt
#import mdi_management


# ---- import end

  
 

def  clean_path_partxxx( path_part ):
    """
    consider add to some lib ??
    """

    # ---- crude but i hope effective
    if path_part:
        path_part    = path_part.replace( "\\", "/" )
    else:
        path_part    = ""

    path_part    = path_part.replace( "///", "/" )
    path_part    = path_part.replace( "//",  "/" )
    path_part    = path_part.removeprefix( "/" )
    path_part    = path_part.removesuffix( "/" )

    return path_part

 

# 

# ----------------------------------------
class DbFileInfo(   ):
    
    #---------------------
    def __init__( self, id, sub_dir, file_name ):
        
        """ 
        Pretty much a dict or dataclass, convert??
        could add exif data ??
        """
        
        # int in db
        self.id                 = id    
        
        # strings                 
        self.sub_dir            = sub_dir
        self.file_name          = file_name
         
        # ---- use @property 
        self._file_size         = None
        self._file_datetime     = None   # see prop to see which kind 
        self._file_path         = None
        self._full_file_name    = None 
        self._file_timestamp    = None 
        self._file_exists       = None
        
 
        self.dt_tolerance       = AppGlobal.parameters.dt_tolerance
  
        self.size_tolerance     = AppGlobal.parameters.size_tolerance
 
    #------------------------------  
    @property   
    def full_file_name( self ):
        
        """
        should we store ?
        we could be overclening ??
        
        other places this may be used
            picture something of other 
            # ------------------------
            picture detail tab: get_picture_file_name(self):
             
                full_file_name  = base_document_tabs.build_pic_filename( file_name = self.file_field.text(), sub_dir = self.sub_dir_field.text() )
                --->
                #-------------------------
                def build_pic_filename( *, file_name, sub_dir ):
        """
        if self._full_file_name is not None:
            return self._full_file_name
        
        if ( self.sub_dir is None ) or ( self.file_name is None ):
            return None
        
        root            = AppGlobal.parameters.picture_db_root
        
        file_name       = self.file_name.strip()
        if file_name == "":
            return None
        
        sub_dir         = self.sub_dir.strip()
    
        full_file_name  = f"{root}/{sub_dir}/{file_name}".replace( "\\", "/" )
        full_file_name  = full_file_name.replace( "///", "/" )
            # just in case we have dups !! this is crude
        full_file_name  = full_file_name.replace( "//", "/" )
            # just in case we have dups
    
        return full_file_name        
    
    #------------------------------
    def get_stats( self ):
        
        """  
        and path
        """    
        full_file_name   = self.full_file_name
        if full_file_name is None:
            # no can do
            self._file_exists = False
            return None
        
 
        file_path           = Path( full_file_name )
        self._file_path     = file_path

        if not file_path.exists():
            self._file_exists = False
            return None
        
        self._file_exists = True
        stats = file_path.stat()
            # could store and access ??
     
        size                = stats.st_size 
        self._file_size          = size 
   
        file_timestamp        = stats.st_ctime
        self._file_timestamp  = file_timestamp 
        
      
        self._file_datetime   = datetime.datetime.fromtimestamp( file_timestamp ) 
        
        
    #------------------------------  
    @property      
    def file_size( self ):
        
        """    
        """
        if self._file_size is None:
            self.get_stats()
            
        return self._file_size       
            
    #------------------------------  
    @property   
    def file_timestamp( self ):
        
        """    
        """        
        if self._file_timestamp is None:
            self.get_stats()

        return self._file_timestamp     

    #------------------------------  
    @property   
    def file_datetime( self ):
        
        """    
        """        
        if self._file_datetime is None:
            self.get_stats()

        return self._file_datetime     

    #------------------------------  
    @property   
    def file_exists( self ):
        
        """    
        """        
        if self._file_exists is None:
            self.get_stats()

        return self._file_exists  

        
 
    # -------------------------
    def is_match( self, file_name,    ):
        """ 
        need tollarances from parameters
        return
            true False None
            msg  -- informal 
            
            
            self.dt_tolerance       = datetime.timedelta(  days=7, hours= 0,   )
     
            self.size_tolerance     = 1_000   # bytes 
            
        """
        # these should be positive 
        
        db_file_info      = self 
 
        if file_name is None:
            # no can do
            return None, "file name is none"
        
 
        file_path           = Path( file_name )
        self._file_path     = file_path

        if not file_path.exists():
            return None,  "file does not exist"
       
        full_file_name = str( file_path.resolve() )
        file_path_name = file_path.name 
        
        if not file_path_name == db_file_info.file_name:
            return False, "failed name match"
        
        stats = file_path.stat()
           
        size                    = stats.st_size 
        self._file_size         = size 
   
        file_timestamp          = stats.st_ctime
        self._file_timestamp    = file_timestamp 
        
        
        file_datetime           = datetime.datetime.fromtimestamp( file_timestamp )
        self._file_datetime     = file_datetime     
        
        delta                    = db_file_info.file_size - size
        if delta < 0:
            delta = - delta
            
        if delta > self.size_tolerance:
            return False, "size tollerance exceeded"
        
        delta                    = db_file_info.file_datetime - file_datetime
        if delta < datetime.timedelta(0):
            delta = - delta
            
        if delta > self.dt_tolerance:
            return False, "datetime tollerance exceeded"
        
        return True, ""
            
# ----------------------------------------
class DbDupFiles(   ):
    """
    deal with duplaicat file issues
    be able to search db for a file name and 
    compare to some other file
    be able to be called again and again 
        perhaps should be functions 
    """
    def __init__(self,   ):
        """
        we need a db connection 
        and parametes to find the actual files
        """
        self.db_con       = AppGlobal.qsql_db_access.db
        self.parameters   = AppGlobal.parameters
  
    
        # query       = QSqlQuery(db)
        #sql         =   ( "SELECT id,  sub_dir, file  FROM photo "
                         # " WHERE  file = :file_path_name " )

  
    # -------------------------
    def find_if_dups( self, a_file_name  ):
        """
        return a list of all dups
            what about size and date 
            
        return 
                [] if fails
                itterable of potential dups 
        """
        # perhaps resolve the guy as a first step
        
      
        # db          = AppGlobal.qsql_db_access.db
        # query       = QSqlQuery(db)
        # sql         =   ( "SELECT id,  sub_dir, file  FROM photo "
        #                  " WHERE  file = :file_path_name " )
       
        file_path      = Path( a_file_name )
        full_file_name = str( file_path.resolve() )
        file_path_name = file_path.name
 
        query       = QSqlQuery( self.db_con )
        sql         =   ( "SELECT id,  sub_dir, file  FROM photo "
                         " WHERE  file = :file_path_name " )

        matching_files = []

        if not query.prepare(sql):  # do we need to prep and bind ove and over
            msg     = ( f"find_if_dups: Prepare failed: {query.lastError().text()}" )
            logging.error( msg )
            return None  # indicates failue

        query.bindValue(":file_path_name", file_path_name )

        if not query.exec_():
            msg     = ("Error executing query:" + query.lastError().text())
            logging.error( msg )
            return None  # indicates failue

        while query.next():
            a_id                = query.value(0)
            sub_dir             = query.value(1)
            file                = query.value(2)
            a_db_file_info      = DbFileInfo( a_id, sub_dir, file)
            matching_files.append( a_db_file_info )

     
        return matching_files


    # -------------------------
    def find_file_missing( self,   ):
        """
        work through records with file names and
        see if file exists, output is file name for records
        whenre that file is missing.
        self.parent_window.open_file_out( )
        starting_dir   = self.dir_widget.text()
        self.explore_dir( starting_dir, 0 , explore_args )

        #max_dir_depth 0 is unlimited
        self.parent_window.close_file_out( )

        """
        self.parent_window.open_file_out( )

        full_dir    = self.dir_widget.text()

        a_sub_dir   = full_dir.removeprefix( parameters.PARAMETERS.picture_db_root )

        db          = AppGlobal.qsql_db_access.db

        query       = QSqlQuery(db)

        sql = """
            SELECT id, sub_dir, file
            FROM photo
            WHERE sub_dir = :a_sub_dir
            ORDER BY id ASC
        """
        if not query.prepare(sql):
            msg     = ( f"Prepare failed: {query.lastError().text()}" )
            self.parent_window.output_to_file( msg )
            return

        query.bindValue(":a_sub_dir", a_sub_dir )

        # --- print results ---
        msg     =  (f"Files in sub_dir='{a_sub_dir}':")
        self.parent_window.output_to_file( msg )

        if not query.exec_():
            msg     = ("Error executing query:" + query.lastError().text())
            self.parent_window.output_to_file( msg )

            # msg      = query_str
            # self.parent_window.output_to_file( msg )

        ix_record_count  = 0
        while query.next():
            ix_record_count     += 1
            a_id                = query.value(0)
            sub_dir             = query.value(1)
            file                = query.value(2)

            msg         = (f"id={a_id}, sub_dir={sub_dir}, file={file} {ix_record_count = }")
            self.parent_window.output_msg(  msg )

            got_file    = self.find_file( sub_dir, file )

            if got_file:
                pass

            else:
                msg     = f"error no file found for {a_id}, file f{sub_dir}/{file}"
                self.parent_window.output_to_file( msg )

        # if   ix_record_count == 0:
        #     msg    = f"error no record found for file f{sub_dir}/{file}"
        #     self.parent_window.output_to_file( msg )

        # elif ix_record_count == 1:
        #     msg    = f"1 record found for file f{full_file_name} {base_path}"
        #     self.parent_window.output_to_file( msg )

        # else:
        #     msg    = f"errorish duplicate records found for file f{full_file_name} {base_path}"
        #     self.parent_window.output_to_file( msg )
        self.parent_window.close_file_out( )
        self.parent_window.activate_output_tab()


    # -------------------------
    def find_record_missing( self,   ):
        """
        work through files ( perhaps of a given directory )
        and see if they have 1 or more files
        output is the file names whre the record is missing.

        """
        explore_args   = ExploreArgs( max_dir_depth = 1 )
        self.parent_window.open_file_out( )
        starting_dir   = self.dir_widget.text()
        self.explore_dir( starting_dir, 0 , explore_args )

        #max_dir_depth 0 is unlimited
        self.parent_window.close_file_out( )

        msg     = (f"find_record_missing complete look for output file in {parameters.PARAMETERS.output_dir}")
        self.parent_window.output_msg(  msg )
        self.parent_window.activate_output_tab()

    # ---- support functions
    # ----------------------------------------------
    def explore_dir( self, starting_dir, dir_depth, explore_args  ):
        """
        set up to run process was for dups and keeps not part of this app
        recursive
        could collect files in a list and process as a batch at the end
        probably more efficient but for now one at a time

        explore and list files in dir and recursive to sub dirs
            starting_dir  = name of dir we start from
            dir_depth     = depth of starting_dir, 0 for initial call
            additional args   current depth
                           filter

        Args:
            starting_dir -- now a path or string ... may need bigger fix for now either !!

        """

        # starting_dir    = starting_dir.replace( "\\", "/" )    # normalize win/linux names
        new_dir_depth   = dir_depth + 1
        names           = os.listdir( starting_dir )  # may throw [WinError 3]

        msg             = f"exploring at depth {new_dir_depth}: {starting_dir}"
        # AppGlobal.logger.info( msg )
        # self.gui_write( msg + "\n" )
        self.parent_window.output_to_file( msg )

        for i_name in names:
            # file from / file to
            i_name        = i_name.replace( "\\", "/" )
            i_full_name   = os.path.join( starting_dir, i_name )
                ## ?? just default to / why not and remove next
            i_full_name   = i_full_name.replace( "\\", "/" )   # !! revise for path
            # next a named tuple
            i_file_info   = FileInfo( file_name         = i_name,
                                      path_name         = starting_dir,
                                      full_file_name    = i_full_name )

            # ---- for now no pause or cancel
            # could have pause here too #
            # if self.app_state.cancel_flag:
            #     msg = "user cancel"
            #     raise app_global.UserCancel( msg )

            # if self.app_state.pause_flag:
            #     time.sleep( self.parameters.ht_pause_sleep )

            # ---- is dir
            if os.path.isdir( i_full_name ):
                # msg     = ( f"os.path.isdir self.app_state.ix_explore_dir = "
                #             f"{self.app_state.ix_explore_dir} new_dir_depth = {new_dir_depth}"
                #             f"    explore_args.max_dir_depth = {explore_args.max_dir_depth}" )
                msg      = ( f"found sub dir {i_full_name}")
                self.parent_window.output_to_file( msg )


                if ( ( explore_args.max_dir_depth == 0  ) or
                     ( explore_args.max_dir_depth  >  new_dir_depth  ) ):
                         # may be more efficient placement of this so called once
                    #self.app_state.count_dir      += 1
                        # or one for file, one for dir, and one for error better ??
                    # if explore_args.df( i_full_name ):   # the filter for dir
                    #     msg     = f"making recursive call {i_full_name} {new_dir_depth}"
                    #     print( msg )
                    self.explore_dir( i_full_name, new_dir_depth, explore_args )
                    # else:
                    #     msg     = f"\nhit false on dir filter df  {i_full_name} "
                    #     print( msg )
                else:
                    msg         = f"\nhit max dir depth {i_full_name} {new_dir_depth} "
                    self.parent_window.output_to_file( msg )

                continue
            #import pdb; pdb.set_trace()
            # ---- is file
            # ==== we got a file not a dir
            file_size               = os.path.getsize(  i_full_name )
            base_path               = parameters.PARAMETERS.picture_db_root
            full_file_name          = i_full_name
            self.find_photo_by_full_file_name( base_path      = base_path,
                                               full_file_name = full_file_name )


    def find_file( self, sub_dir, file  ):
        """
        could be a file or a directory may want to make better
        assumes output file is open
        Find a record in the photo table where the concatenated sub_dir and file match the provided values.
        path = Path("/mnt/WIN_D/PhotoDB/14/dscn2802.jpg")

        if path.exists():
        """
        full_file_name    = f"{parameters.PARAMETERS.picture_db_root}{sub_dir}/{file}"
        path              = Path( full_file_name )

        is_found          = path.exists()

        msg  = ( f"find_file  >>{full_file_name}<< {is_found = }")
        self.parent_window.output_to_file( msg )

        return is_found


    def find_photo_by_full_file_name( self, *, base_path,  full_file_name ):
        """
        Find a record in the photo table where the concatenated BASE_PATH, sub_dir, and file match the provided values.
        Args:
            sub_dir (str): The subdirectory name.
            file_name (str): The file name.
        Returns:
            dict or None: A dictionary containing all fields of the matching record, or None if no match or error.
        """
        db                  = AppGlobal.qsql_db_access.db
        #BASE_PATH = "/photos/"  # Constant string for the base directory
        query = QSqlQuery( db)
        query_str = ( ""
            "SELECT id, "
            # " id_old, "
                   # name, add_kw, descr, type, series, author, dt_enter, format,
                   # inv_id, cmnt, status, dt_item, c_name, title, tag, old_inv_id,
                   " file, sub_dir "
                   # photo_url, camera, lens, f_stop, shutter, copyright
            " FROM photo "
            " WHERE :base_path || TRIM(sub_dir, '/' )  || '/' || file = :full_file_name "
            )

        query.prepare(query_str)
        #full_path = f"{sub_dir}/{file_name}"
        query.bindValue(":base_path",      base_path )
        query.bindValue(":full_file_name", full_file_name )

        if not query.exec_():
            msg     = ("Error executing query:" + query.lastError().text())
            self.parent_window.output_to_file( msg )

            msg      = query_str
            self.parent_window.output_to_file( msg )

            return None
        ix_record_count  = 0
        if query.next():
            ix_record_count  += 1
            record = {
                "id": query.value(0),
                # "id_old": query.value(1),
                # "name": query.value(2),
                # "add_kw": query.value(3),
                # "descr": query.value(4),
                # "type": query.value(5),
                # "series": query.value(6),
                # "author": query.value(7),
                # "dt_enter": query.value(8),
                # "format": query.value(9),
                # "inv_id": query.value(10),
                # "cmnt": query.value(11),
                # "status": query.value(12),
                # "dt_item": query.value(13),
                # "c_name": query.value(14),
                # "title": query.value(15),
                # "tag": query.value(16),
                # "old_inv_id": query.value(17),
                "file": query.value(1),
                "sub_dir": query.value(2)
                # "photo_url": query.value(20),
                # "camera": query.value(21),
                # "lens": query.value(22),
                # "f_stop": query.value(23),
                # "shutter": query.value(24),
                # "copyright": query.value(25)
            }
            msg    = str( record )
            self.parent_window.output_to_file( msg )

        if   ix_record_count == 0:
            msg    = f"error no record found for file f{full_file_name} {base_path}"
            self.parent_window.output_to_file( msg )

        elif ix_record_count == 1:
            msg    = f"1 record found for file f{full_file_name} {base_path}"
            self.parent_window.output_to_file( msg )

        else:
            msg    = f"errorish duplicate records found for file f{full_file_name} {base_path}"
            self.parent_window.output_to_file( msg )
        return

   
# ---- eof