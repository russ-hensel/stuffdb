# -*- coding: utf-8 -*-
# ---- tof

"""
    parameters    for  stuff_db_qt

    parameters    for  stuffdb_qt
    parameters.PARAMETERS.

"""
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main

# --------------------

from pathlib import Path

# ---- local imports


global PARAMETERS
PARAMETERS   = None
# parameters.PARAMETERS

import logging
import os
import sys

import running_on
import string_util
from app_global import AppGlobal

VERBOSE   = False


if VERBOSE:
    print( "parameters from -----  /_projects/stuffdb/parameters.py")
    print( __file__ )

#===========================
class Parameters( ):
    """
    manages parameter values: use it like an ini file but it is code
    """
    # -------
    def choose_mode( self ):
        """
        typically choose one mode
            and if you wish add the plus_test_mode
            if you comment all out all modes you get the default mode which should
            run, perhaps not in the way you want
        """
        #self.mode_new_db()
        self.mode_github()
        self.mode_python_ex_on_theprof()

        #self.mode_builddb_on_theprof()

        #self.mode_russ_on_theprof()
        #self.mode_helpdb_on_theprof()

        # self.mode_temp_db_in_ram()
        # self.mode_add_real_pictures()



        #self.mode_russ_on_smithers()
        #self.new_user_mode()
        #self.millhouse_1_mode()

        # two of my computers
        #self.mode_millhouse_mint()
        #self.mode_theprof_mint()
        #self.russ_1_mode()

        # --- add on for testing, use as desired edit mode for your needs
        #self.plus_test_mode()


    # -------
    def new_user_mode( self ):
        """
        a mode for the new user, pretty much empty,
        a new user may experiment here.
        """
        self.mode               = "mode new_user"

        # ---- type and location of the db file
        self.db_type            = "QSQLITE"
            # the type of database, so far we only support sqllite
        self.db_file_name       = "./data/python_ex.db"

    # -------
    def mode_github( self ):
        """
        test if will run in github, will probably be a lot like new user
        """
        self.mode               = "mode_github"

        # ---- type and location of the db file
        self.db_type            = "QSQLITE"
            # the type of database, so far we only support sqllite

        self.db_file_name       = "./data/new.db"   #  = "sample.db"   =  ":memory:"
        self.db_file_name       = "./data/python_ex.db"

        self.logging_level      = logging.DEBUG   # ERROR

    # ---- ---->> Methods:  one for each mode
    # -------
    def mode_new_db( self ):
        """
        make directories the real pictures
        but not the new pictures for testing
        """
        self.mode               = "mode_new_db"

        # ---- type and location of the db file
        self.db_type            = "QSQLITE"
            # the type of database, so far we only support sqllite

        # use full name if calling form a subdirectory of the project at least fo now
        #self.db_file_name      = ":memory:"
        self.db_file_name       = "./data/new.db"   #  = "sample.db"   =  ":memory:"
        self.db_file_name       = "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/data/new.db"

        self.picture_db_root    = "/mnt/WIN_D/temp_photo"
        self.picture_db_sub     = "/99"
            # all pictures should be under this directory
        # ---- file  and path names
        self.picture_browse     = "/mnt/WIN_D/temp_photo_source"

        self.logging_level      = logging.DEBUG   # ERROR

    # -------
    def mode_add_real_pictures( self ):
        """
        make directories the real pictures
        but not the new pictures for testing
        """
        self.mode               =  self.mode  + "mode_add_real_pictures"
        self.picture_db_root    = "/mnt/WIN_D/temp_photo"
        self.picture_db_sub     = "/test_delete"
        self.picture_db_sub     = "/99/new_test"
            # all pictures should be under this directory
        # ---- file  and path names
        self.picture_browse     = "/mnt/WIN_D/temp_photo_source"

    # -------
    def mode_temp_db_in_ram( self ):
        """
        a mode for the help info while still in dev
        later will export data then reimport and
        perhaps rekey
        """
        self.mode               = "mode_temp_db_in_ram"
        # but do they use the same units ?
        self.qt_width           = 1200
        self.qt_height          = 700    # 700 most of win height
        self.qt_xpos            = 50
        self.qt_ypos            = 50

        # sizes for the wat-inspector in qt
        self.wat_qt_width       = 1300
        self.wat_qt_height      = 800
        self.wat_qt_xpos        = 10
        self.wat_qt_ypos        = 10

        self.picture_db_root    = "/mnt/WIN_D/temp_photo"
        self.picture_db_sub     = "/test_delete"
        self.picture_db_sub     = "/99/new_test"
            # all pictures should be under this directory
        # ---- file  and path names
        self.picture_browse     = "/mnt/WIN_D/temp_photo_source"

        # ---- type and location of the db file
        self.db_type            = "QSQLITE"
            # the type of database, so far we only support sqllite

        self.db_file_name       = "./data_help_db/helpdb.db"
        self.db_file_name       = "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/data_help_db/helpdb.db"
        self.db_file_name       = "/tmp/ramdisk/temp_db.db"

        self.logging_level      = logging.ERROR   # ERROR

    # -------
    def mode_builddb_on_theprof( self ):
        """
        use with full path to db so code from sub dirs will work
        """
        self.mode               = "mode_builddb_on_theprof"


        self.picture_db_root    = "/mnt/WIN_D/temp_photo"
        self.picture_db_sub     = "/test_delete"
        self.picture_db_sub     = "/99/new_test"
            # all pictures should be under this directory
        # ---- file  and path names
        self.picture_browse     = "/mnt/WIN_D/temp_photo_source"

        # ---- type and location of the db file
        self.db_type            = "QSQLITE"
            # the type of database, so far we only support sqllite

        self.db_file_name       = "./data_help_db/helpdb.db"
        self.db_file_name       = "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/data_help_db/helpdb.db"
        self.db_file_name       = "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/data/python_ex.db"
        #self.db_file_name       = "./data/python_ex.db"
        #/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/data_help_db/helpdb.db

        self.logging_level          = logging.INFO
        self.logging_level          = logging.DEBUG

    # -------
    def mode_helpdb_on_theprof( self ):
        """

        a mode for the help info while still in dev
        later will export data then reimport and
        perhaps rekey
        """
        self.mode               = "mode_helpdb_on_theprof"
        # but do they use the same units ?
        # self.qt_width           = 1200
        # self.qt_height          = 700    # 700 most of win height
        # self.qt_xpos            = 50
        # self.qt_ypos            = 50

        # # sizes for the wat-inspector in qt
        # self.wat_qt_width       = 1300
        # self.wat_qt_height      = 800
        # self.wat_qt_xpos        = 10
        # self.wat_qt_ypos        = 10

        self.picture_db_root    = "/mnt/WIN_D/temp_photo"
        self.picture_db_sub     = "/test_delete"
        self.picture_db_sub     = "/99/new_test"
            # all pictures should be under this directory
        # ---- file  and path names
        self.picture_browse     = "/mnt/WIN_D/temp_photo_source"

        # ---- type and location of the db file
        self.db_type            = "QSQLITE"
            # the type of database, so far we only support sqllite

        self.db_file_name       = "./data_help_db/helpdb.db"
        self.db_file_name       = "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/data_help_db/helpdb.db"
        self.db_file_name       = "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/data/python_ex.db"
        self.db_file_name       = "./data/python_ex.db"
        #/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/data_help_db/helpdb.db

        self.logging_level          = logging.INFO
        self.logging_level          = logging.DEBUG
    # -------
    def mode_python_ex_on_theprof( self ):
        """
        a mode for the help info while still in dev
        later will export data then reimport and
        perhaps rekey
        """
        self.mode               = "mode_python_ex_on_theprof"
        # but do they use the same units ?
        # self.qt_width           = 1200
        # self.qt_height          = 700    # 700 most of win height
        # self.qt_xpos            = 50
        # self.qt_ypos            = 50

        # # sizes for the wat-inspector in qt
        # self.wat_qt_width       = 1300
        # self.wat_qt_height      = 800
        # self.wat_qt_xpos        = 10
        # self.wat_qt_ypos        = 10

        self.picture_db_root    = "/mnt/WIN_D/temp_photo"
        self.picture_db_sub     = "/test_delete"
        self.picture_db_sub     = "/99/new_test"
            # all pictures should be under this directory
        # ---- file  and path names
        self.picture_browse     = "/mnt/WIN_D/temp_photo_source"

        # ---- type and location of the db file
        self.db_type            = "QSQLITE"
            # the type of database, so far we only support sqllite

        self.db_file_name       = "./data_help_db/helpdb.db"
        self.db_file_name       = "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/data_help_db/helpdb.db"
        #/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/data_help_db/helpdb.db
        #self.db_file_name       = "./data/python_ex.db"
        self.db_file_name       = "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/data/python_ex.db"
        #                          /mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/data/python_ex.db

    # -------
    def mode_russ_on_theprof( self ):
        """
        what it say
        """
        self.mode               = "mode_russ_on_theprof"
        # but do they use the same units ?
        self.qt_width           = 1200
        self.qt_height          = 700    # 700 most of win height
        self.qt_xpos            = 50
        self.qt_ypos            = 50

        # # control initial size and position with:
        # self.qt_width           = 1200
        # self.qt_height          = 500
        # self.qt_xpos            = 50
        # self.qt_ypos            = 50

        # sizes for the wat-inspector in qt
        self.wat_qt_width       = 1300
        self.wat_qt_height      = 800
        self.wat_qt_xpos        = 10
        self.wat_qt_ypos        = 10

        self.picture_db_root    = "/mnt/WIN_D/temp_photo"
            # all pictures should be under this directory
        # ---- file  and path names
        self.picture_browse     = "/mnt/WIN_D/temp_photo_source"


        self.picture_db_sub     = "/test_delete"
        self.picture_db_sub     = "/99/new_test"

    # -------
    def mode_russ_on_smithers( self ):
        """
        what it says
        """
        self.mode               = "mode_russ_on_theprof"
        # but do they use the same units ?
        self.qt_width           = 1200
        self.qt_height          = 700    # 700 most of win height
        self.qt_xpos            = 50
        self.qt_ypos            = 50

        # # control initial size and position with:
        # self.qt_width           = 1200
        # self.qt_height          = 500
        # self.qt_xpos            = 50
        # self.qt_ypos            = 50

        # sizes for the wat-inspector in qt
        self.wat_qt_width       = 1300
        self.wat_qt_height      = 800
        self.wat_qt_xpos        = 10
        self.wat_qt_ypos        = 10

        self.picture_db_root    = "/mnt/WIN_D/temp_photo"
            # all pictures should be under this directory
        # ---- file  and path names
        self.picture_browse     = "/mnt/WIN_D/temp_photo_source"

        self.picture_db_sub     = "/test_delete"
        self.picture_db_sub     = "/99/new_test"

        self.db_file_name              = "./data/appdb.db"
        self.db_file_name              = "./data/sept_35.db"

    # -------
    def mode_test_addon_ram_disk_db( self ):
        """
        what it says
        """
        self.mode               += " + mode_test_addon_in_memory_db"

        self.db_type                = "QSQLITE"
        self.db_file_name      = "/tmp/ramdisk/ramdisk.db"



    # -------
    def running_on_tweaks(self,  ):
        """
        not a mode, a tweak to other modes , see documentation
        you need to customize this for your own computers, what you may
            find here are customization's for russ and his computers
        use running on tweaks as a more sophisticated
            version of os_tweaks and computer name tweaks which
        may replace them
        this is computer name tweaks code,

        """
        self.os_tweaks()

        computer_id    =   self.running_on.computer_id

        if computer_id == "smithers":
            self.win_geometry       = '1450x700+20+20'      # width x height position
            self.ex_editor          =  r"D:\apps\Notepad++\notepad++.exe"
            self.db_file_name       =  "smithers_db.db"

        # ---- bulldog
        elif computer_id == "bulldog":
            self.ex_editor          =  r"gedit"
            self.db_file_name       =  "bulldog_db.db"


        elif computer_id == "millhouse":
            self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"
            #self.win_geometry   = '1300x600+20+20'
            self.db_file_name       =  "millhouse_db.db"

        elif computer_id == "millhouse-mint":
            #self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"
            #self.win_geometry   = '1300x600+20+20'

            pass

        # ---- theprof
        elif computer_id == "theprof":
            self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"
            self.db_file_name       =  "the_prof_db.db"

        # ---- "russ-thinkpad-p72":
        elif computer_id == "russ-thinkpad-p72":
            # ---- appearance -- including sizes

            # control initial size and position with:
            self.qt_width           = 1500
            self.qt_height          = 800
            self.qt_xpos            = 50
            self.qt_ypos            = 50

            # sizes for the wat-inspector in qt
            self.wat_qt_width       = 1300
            self.wat_qt_height      = 800
            self.wat_qt_xpos        = 10
            self.wat_qt_ypos        = 10

            # ---- doc is a mdi doc like help_document
            self.doc_qt_width       = 1300
            self.doc_qt_height      = 700
            self.doc_qt_xpos        = 20
            self.doc_qt_ypos        = 20

            self.logging_level      = logging.DEBUG

        elif computer_id == "bulldog-mint-russ":
            self.ex_editor          =  r"xed"

        else:
            msg    = ( f"In parameters: no special settings for computer_id {computer_id}" )
            logging.debug( msg )
            # next should be in os_tweaks not here
            if self.running_on.os_is_win:
                self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"
            else:
                self.ex_editor          =  r"leafpad"    # Linux raspberry pi maybe


    # ------->> default mode, always call
    def mode_default( self ):
        """
        sets up pretty much all settings
        documents the meaning of the modes
        call first, then override as necessary
        good chance these settings will at least let the app run

        Generally this mode should only be changed by developers
        """
        self.mode              = "mode_default"
            # name your config, it will show in app title
            # may be changed later in parameter init

        #--------------- automatic settings -----------------
        #---- running_on gathers information about you computer environment
        self.running_on   = running_on.RunningOn
        self.running_on.gather_data()

        # some of the next all?? should be moved over to RunningOn
        self.running_on.log_me( logger = None, logger_level = 10, print_flag = False )

        # this is the path to the main.py program --
        self.py_path                   = self.running_on.py_path

        self.set_default_path_here     = True
            # to make app location the default path in the app, Think True may always be best.
            # above may be tricky to reset, but we may have the original dir in running on
        # no easy way to override this ??
        if  self.set_default_path_here:     # Now change the directory to location of this file

            py_path     = self.running_on.py_path

            msg         = ( f"Parameters.py: Directory: (  >>{os.getcwd()}<< switch if not '' to >>{py_path}<<")
            logging.debug( msg )
            if py_path != "":
                os.chdir( py_path )

        # so we know our os  could be "linux" or our_os == "linux2"  "darwin"....
        self.our_os             = self.running_on.our_os
        self.os_win             = self.running_on.os_win          # boolean True if some version of windows
        self.computername       = self.running_on.computername    # a name of the computer if we can get it
        # directory where app was opened, not where it resides
        self.opening_dir        = self.running_on.opening_dir     # the opening dir before anyone changes it

        self.platform           = self.our_os           #  redundant

        # ---- appearance -- including sizes

        # control initial size and position with:
        self.qt_width           = 1200
        self.qt_height          = 500
        self.qt_xpos            = 50
        self.qt_ypos            = 50

        # sizes for the wat-inspector in qt
        self.wat_qt_width       = 1300
        self.wat_qt_height      = 800
        self.wat_qt_xpos        = 10
        self.wat_qt_ypos        = 10

        # ---- doc is a mdi doc like help_document
        self.doc_qt_width       = 900
        self.doc_qt_height      = 600
        self.doc_qt_xpos        = 20
        self.doc_qt_ypos        = 20

        # icon for running app
        self.icon               = r"./misc/icon_red.png"

        self.icon               =  "./misc/binocular.png"
        self.icon               =  "./misc/iconfinder_database_103466.png"
        self.icon               =  "./misc/db_red_on_yellow.png"


        self.text_edit_font     = ("Arial", 12)

        # ---- logging
        self.pylogging_fn           = "./logs/app.py_log"
            # file name for the python logging

        # next two seem redundant
        self.log_mode               = "w"    # "a" append "w" truncate and write
        self.delete_log_on_start    = True
            # if True you get a new log file everytime the program starts

        self.logging_level          = logging.DEBUG         # may be very verbose
        self.logging_level          = logging.INFO
        self.logging_level          = logging.DEBUG
            # logging level used by app logger

        self.logger_id              = "stuffdb"
            # id of app in logging file

        # ---- file  and path names more
        self.picture_browse         = "/mnt/WIN_D/PhotosRaw/2024/pixel4a/july4"
            # browsing starts from here see PictureDocument

        # picture to use when a valid picture is not found or does not exist
        self.pic_nf_file_name       = "./misc/404.png"

        self.picture_db_root        = "/mnt/WIN_D/PhotoDB/"
            # all pictures once in the db should be under this directory

        self.picture_db_sub         = "/test_delete"
            # subdir for above used when adding new pictures

        # ---- .... db type and location of the db file
        self.db_type                = "QSQLITE"
            # the type of database, so far we only support sqllite

        # self.db_fn              = "./data/appdb.db"
        # self.db_fn              = "/mnt/WIN_D/Russ/0000/python00/python3/_projects/stuffdb/data/sept_26.db"
        # self.db_fn              = "/tmp/ramdisk/sept_28.db"
        # self.db_fn              = "/tmp/ramdisk/sept_35.db"

        # think for qt4_by_ecample not stuff
        self.db_file_name      = ":memory:"
        self.db_file_name      = "sample.db"   #  = "sample.db"   =  ":memory:"
        self.db_file_name      = ":memory:"     #  = "sample.db"   =  ":memory:"
        #self.db_file_name        = "/tmp/ramdisk/qt_sql.db"

        # this is the name of a program: its executable with path info.
        # to be used in opening an external editor
        self.ex_editor         =  r"D:\apps\Notepad++\notepad++.exe"    # russ win 10
        self.text_editor       = "gedit"
        self.text_editor_list  = [ "xed", "gedit" ]

        # control button for editing the readme file
        self.readme_fn          = "readme_rsh.txt"   # or None to suppress in gui
            # a readme file accessible from the main menu

        # or anything else ( will try to shell out may or may not work )
        self.help_fn       =  "./docs/help.txt"   #  >>. this is the path to our main .py file self.py_path + "/" +
        self.help_path     =  "./docs"

        self.idle_venv     = "py_12_misc"   # idle will open in this python venv
            # path leading to all docs and help

        #self.help_file       =  "http://www.opencircuits.com/Python_Smart_ClipBoard"

        self.poll_delta_t      = 200      # 200 ok at least on win longer does not fix linux prob
        self.poll_delta_t      = 100
            # how often we poll for clip changes, in ms,
            # think my computer works well as low as 10ms

        self.auto_run           = True  # run code examples -- !! what but needed

        # ---- templates  a bit odd to control left margin -- !! change to textwrap
        self.text_templates     = {}
        template_name           = "Python"
        template_text           = (
"""
>>Py a_python_template

print( f"a_python_template { 0 = }" )

>>end -----------------
""" )
        self.text_templates[template_name] = template_text

        #---------------------------------
        template_name          = "Bash"
        template_text          = (
"""
>>Bash a_shell_template

print( f"bash a_shell_template still needs writing { 0 = }"
"""  )
        self.text_templates[template_name] = template_text

        # ---- text
        template_name          = "Text"
        template_text          = (
"""
>>Text  ./parameters.py
"""  )
        self.text_templates[template_name] = template_text

        # ---- url
        template_name          = "Url"
        template_text          = (
"""
>>url  https://www.youtube.com/feed/subscriptions#on&off&types=uploads
"""  )
        self.text_templates[template_name] = template_text

        # ---- .... shell template
        template_name          = "Shell"
        template_text          = (
"""
>>Shell  /mnt/WIN_D/PhotoDB/00/00july_06.jpg
"""  )
        self.text_templates[template_name] = template_text

        # ---- systems for helpdb ??alpha
        self.systems_list      =  [    '',
                        'Bash',
                        'Delete',
                        'Linux',
                        'Powerbuilder',
                        'Python',
                        'RasPi',
                        'RshPy',              # subsystem the project
                        'Russ',
                        'StuffDB',
                        'TBD',
                        ]

    # -------
    def __init__( self, ):
        """
        Init for instance, usually not modified, except perhaps debug stuff
        ( if any )... but use plus_test_mode()
        may be down in listing because it should not be messed with.
        """
        AppGlobal.parameters       = self   # register as a global -- phase out
        self.mode_default()
        self.running_on_tweaks()
        self.choose_mode()

        msg     = ( "--------------- PARAMETERS FILE -------------------", __file__ )
        logging.debug( msg )

        self.parameter_dir   = str( Path( __file__ ).parent )
        msg     = ( f"parameter_file_from {self.parameter_dir = }")
        logging.debug( msg )

        # next lets you use  parameters.PARAMETERS as a global
        global PARAMETERS
        if not PARAMETERS:
            msg     = ( "creating global parameters.PARAMETERS")
            PARAMETERS    = self
        else:
            msg     = ( "__init__ probably an error unless a restart")
            PARAMETERS    = self
            # 1/0
        logging.debug( msg )

        #rint( self ) # for debugging

    # -------
    def os_tweaks( self ):
        """
        this is an subroutine to tweak the default settings of "default_mode"
        for particular operating systems
        you may need to mess with this based on your os setup
        """
        if  self.os_win:
            self.icon               = r"./images/clipboard_b.ico"
                #  very dark greenhouse this has issues on rasPi
            self.icon               = r"./images/clipboard_b_red_GGV_icon.ico"
                #  looks same as clipboard_b_red_gimp.ico
            self.icon               = r"./images/clipboard_b_red_gimp.ico"    # pretty visible -- make black version -- cannot get gimp to do it

        else:
            pass
            #self.gui_style          = "linux"


    # ---------------------
    def to_columns( self, current_str, item_list, format_list = [ "{: <30}", "{:<30}" ], indent = "    "  ):
        """
        for __str__  probably always default format_list
        """
        #rint ( f"item_list {item_list}.............................................................. " )
        line_out  = ""
        for i_item, i_format in zip( item_list, format_list ):
            a_col  = i_format.format( i_item )
            line_out   = f"{indent}{line_out}{a_col}"
        ret_str  = f"{current_str}\n{line_out}"
        return ret_str

    # -----------------------------------
    def __str__( self,   ):
        """
        sometimes it is hard to see where values have come out this may help if printed.
        not complete, add as needed -- compare across applications and code above
        """
        # new_indented    = "\n    "   # but it nice to have some whitespace to see ...
        a_str = "\n "
        a_str   = f"{a_str}>>>>>>>>>>* Parameters (some) *<<<<<<<<<<<<"
        a_str   = string_util.to_columns( a_str, ["mode",       f"{self.mode}" ] )
        a_str   = string_util.to_columns( a_str, ["computer_id", f"{self.running_on.computer_id}" ] )
        a_str   = string_util.to_columns( a_str, ["db_file_name",
                                           f"{self.db_file_name}" ] )

        a_str   = string_util.to_columns( a_str, ["db_type",
                                           f"{self.db_type}" ] )

        a_str   = string_util.to_columns( a_str, ["logger_id", f"{self.logger_id}" ] )
        a_str   = string_util.to_columns( a_str, ["logging_level", f"{self.logging_level}" ] )
        a_str   = string_util.to_columns( a_str, ["pylogging_fn",    f"{self.pylogging_fn}" ] )

        a_str   = string_util.to_columns( a_str, [ "log_mode",
                                                  f"{self.log_mode}" ] )


        a_str   = string_util.to_columns( a_str, [ "delete_log_on_start -- depricatef for log_mode",
                                                  f"{self.delete_log_on_start}" ] )


        # a_str   = string_util.to_columns( a_str, ["gui_text_log_fn", f"{self.gui_text_log_fn}" ] )

        a_str   = string_util.to_columns( a_str, ["readme_fn", f"{self.readme_fn}" ] )
       # a_str   = string_util.to_columns( a_str, ["help_file",    f"{self.help_file}" ] )


        a_str   = string_util.to_columns( a_str, ["parameter_dir", f"{self.parameter_dir}" ] )
        a_str   = string_util.to_columns( a_str, ["icon", f"{self.icon}" ] )


        a_str   = string_util.to_columns( a_str, ["computername", f"{self.computername}" ] )
        a_str   = string_util.to_columns( a_str, ["our_os", f"{self.our_os}" ] )
        a_str   = string_util.to_columns( a_str, ["py_path", f"{self.py_path}" ] )
        a_str   = string_util.to_columns( a_str, ["set_default_path_here", f"{self.set_default_path_here}" ] )
        a_str   = string_util.to_columns( a_str, ["poll_delta_t", f"{self.poll_delta_t}" ] )






        a_str   = string_util.to_columns( a_str, ["help_fn",
                                           f"{self.help_fn}" ] )
        a_str   = string_util.to_columns( a_str, ["help_path",
                                           f"{self.help_path}" ] )

        # a_str   = string_util.to_columns( a_str, ["log_gui_text",
        #                                    f"{self.log_gui_text}" ] )
        a_str   = string_util.to_columns( a_str, ["opening_dir",
                                           f"{self.opening_dir}" ] )
        a_str   = string_util.to_columns( a_str, ["os_win",
                                           f"{self.os_win}" ] )
        a_str   = string_util.to_columns( a_str, ["picture_browse",
                                           f"{self.picture_browse}" ] )


        a_str   = string_util.to_columns( a_str, ["picture_db_root",
                                           f"{self.picture_db_root}" ] )
        a_str   = string_util.to_columns( a_str, ["picture_db_sub",
                                           f"{self.picture_db_sub}" ] )

        a_str   = string_util.to_columns( a_str, ["pic_nf_file_name",
                                           f"{self.pic_nf_file_name}" ] )


        a_str   = string_util.to_columns( a_str, ["platform",
                                           f"{self.platform}" ] )
        a_str   = string_util.to_columns( a_str, ["qt_height",
                                           f"{self.qt_height}" ] )
        a_str   = string_util.to_columns( a_str, ["qt_width",
                                           f"{self.qt_width}" ] )
        a_str   = string_util.to_columns( a_str, ["qt_xpos",
                                           f"{self.qt_xpos}" ] )
        a_str   = string_util.to_columns( a_str, ["qt_ypos",
                                           f"{self.qt_ypos}" ] )


        a_str   = string_util.to_columns( a_str, ["wat_qt_height",
                                           f"{self.wat_qt_height}" ] )
        a_str   = string_util.to_columns( a_str, ["wat_qt_width",
                                           f"{self.wat_qt_width}" ] )
        a_str   = string_util.to_columns( a_str, ["wat_qt_xpos",
                                           f"{self.wat_qt_xpos}" ] )
        a_str   = string_util.to_columns( a_str, ["wat_qt_ypos",
                                           f"{self.wat_qt_ypos}" ] )


        a_str   = string_util.to_columns( a_str, ["running_on",
                                           f"{self.running_on}" ] )

        return a_str

        #---- sort into above


        return a_str

# something like this for creating on import
# ---------------
def create_if_needed( ):
    global PARAMETERS
    if not PARAMETERS:

          print( "creating global parameters.PARAMETERS")
          PARAMETERS    = Parameters()

# --------------------

create_if_needed()


# =================== eof ==============================
# ---- eof