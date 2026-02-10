# -*- coding: utf-8 -*-
# ---- tof

"""
    parameters    for  stuffdb

        parameters.PARAMETERS.

"""

# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main
# --------------------

from   pathlib import Path
import textwrap
import datetime

# ---- local imports
global PARAMETERS   # just a reminder ??
PARAMETERS   = None
# parameters.PARAMETERS

import logging
import os
import sys

import running_on
import string_utils
from   app_global import AppGlobal
import startup_functions

VERBOSE   = False
SYS_ARGS  = sys.argv

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

                    self.db_file_name      = "/tmp/ramdisk/helpdb_from_scratch.db"

        """
        #breakpoint( )
        if self.mode_from_command_line():
            return

        note  = """
        if you set the mode from the command line you will not
        get here"""

        self.mode_data_sync()
        #self.mode_data_sync_b()
        #self.mode_github()
        # self.mode_picture_test()
        #self.mode_github()
        #self.mode_postgres()

        # ----mode_mh_2025_hd
        # self.mode_mh_2025_hd()
        # self.mode_theprof()
        # self.mode_king_homer()
        #self.mode_server_king_homer()
        #self.mode_sync_king_homer()

        #self.mode_russ_2025_ram()
        #self.mode_build_new_ram()
        #self.mode_helpdb_from_scratch()
        # self.mode_russ_2025_ram()
        #self.mode_github()

    # -------
    def mode_new_user( self ):
        """
        a mode for the new user, pretty much empty,
        a new user may experiment here.
        this !! should be revised to use demo_db.db  or similar
        """
        self.mode               = "mode_new_user"
        print( "------------------------------------ mode new user ")

        # ---- type and location of the db file
        self.db_type            = "QSQLITE"
            # the type of database, so far we only support SQLite
        self.db_file_name       = "./data/python_ex.db"

    # -------
    def mode_from_computer_id( self ):
        """
        this is an idea that is not yet worked out -- may not work
        or just be default + running on
        """
        self.mode               = "mode_from_computer_id"

        # ---- type and location of the db file
        self.db_type            = "QSQLITE"
            # the type of database, so far we only support SQLite
        self.db_file_name       = "./data/python_ex.db"

    # -------
    def mode_build_new_ram( self ):
        """
        /tmp/ramdisk/helpdb_from_scratch.db
        """
        self.mode               = "mode_build_new_ram"

        # ---- type and location of the db file
        self.db_type            = "QSQLITE"
        self.db_file_name       = "/tmp/ramdisk/russ2025/stuffdb.db"

        self.logging_level      = logging.DEBUG   # ERROR

       # self.icon               =  "./misc/db_red_on_yellow.png"
        self.icon               =  "./misc/db_green_on_black.png"
       # self.icon               =  "./misc/db_red_on_black.png"

    # -------
    def mode_helpdb_from_scratch( self ):
        """
        /tmp/ramdisk/helpdb_from_scratch.db
        """
        self.mode               = "mode_helpdb_from_scratch"

        # ---- type and location of the db file
        self.db_type            = "QSQLITE"
        self.db_file_name       = "/tmp/ramdisk/helpdb_from_scratch.db"

        self.logging_level      = logging.DEBUG   # ERROR

    # -------
    def mode_theprof( self ):
        """
        moved code to running+on_tweaks
        """
        self.mode               = "mode_theprof"

    # -------
    def mode_picture_test( self ):
        """
        moved code to running+on_tweaks
        """
        self.mode               = "mode_picture_test"
        self.db_file_name       = "/mnt/8ball1/first6_root/temp_picture_test/stuffdb.db"
        self.db_file_name       = "./data_test/stuffdb.db"
        #self.db_file_name       = "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/stuffdb/data_test/stuffdb.db"

        self.db_lock_file_name  = None
        self.db_lock_file_name  = "./data_test/lock_db.txt"     # if present then db is locked else none

        self.picture_db_root    = "/mnt/8ball1/first6_root/temp_picture_test/picture_db"
            # all pictures once in the db should be under this directory

        self.picture_db_sub         = "/99"
                  #
            # subdir for above used when adding new pictures

        self.picture_browse     = "/mnt/8ball1/first6_root/temp_picture_test/temp_picture_src"

        self.icon               =  "./misc/db_green_on_black.png"
        self.icon               =  "./misc/db_red_on_black.png"
        self.icon               =  "./misc/red_tube.png"

    # -------
    def mode_sync_king_homer( self ):
        """
        moved code to running+on_tweaks
        """
        self.mode               = "mode_sync_king_homer"
        self.db_file_name       = "./data_sync/stuffdb.db"      #  = "sample.db"   =  ":memory:"
        self.db_lock_file_name  = "./data_sync/lock_db.txt"     # if present then db is locked else none

        self.icon               =  "./misc/db_green_on_black.png"

    # -------
    def mode_data_sync( self ):
        """
        moved code to running+on_tweaks
        """
        self.mode               = "mode_data_sync"
        self.db_file_name      = "./data_sync/stuffdb.db"      #  = "sample.db"   =  ":memory:"

        self.db_lock_file_name = "./data_sync/lock_db.txt"     # if present then db is locked else none

        #self.db_lock_file_name = None
        # /mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/stuffdb/data_sync/stuffdb.db
        #  /mnt/k_wd_pp_silver/backup_on_k/russ/0000/python00/python3/_projects/stuffdb/data/king_homer

        # /mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/stuffdb/data_sync/stuffdb.db
        self.icon               =  "./misc/db_green_on_black.png"

    # -------
    def mode_data_sync_b( self ):
        """
        moved code to running+on_tweaks
        """
        self.mode              = "mode_data_sync_b"
        self.db_file_name      = "./data_sync_b/stuffdb.db"      #  = "sample.db"   =  ":memory:"
        self.db_lock_file_name = "./data_sync_b/lock_db.txt"     # if present then db is locked else none

        self.icon              = "./misc/db_green_on_black.png"

    # -------
    def mode_postgres( self ):
        """
        moved code to running+on_tweaks
        """
        self.mode              = "mode_postgres"

        self.db_type            = "POSTG"

        self.db_host_name       = "localhost"
        self.db_port            = 5432
        self.db_name            = "postgres"
        self.db_user            = "russ"
        self.db_password        = "nopassword"

        self.icon              = "./misc/db_green_on_black.png"

    # -------
    def mode_king_homer( self ):
        """
        moved code to running+on_tweaks
        """
        self.mode               = "mode_king_homer"

    # -------
    def mode_fattony( self ):
        """
        moved to running_on
        """
        self.mode               = "mode_fattony"


    # -------
    def mode_github( self ):
        """
        test if will run in github, will probably be a lot like new user
        use production db -- primary
        """
        self.mode               = "mode_github"

        # # ---- type and location of the db file
        # self.db_type            = "QSQLITE"
        #     # the type of database, so far we only support SQLite

        self.db_file_name       = "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/data/theprof/stuffdb.db"
        self.db_file_name       = "./data/helpdb_from_scratch.db"
        self.db_file_name       = self.project_root  + "/data_sync/stuffdb.db"
        self.db_lock_file_name  = self.project_root  + "/data_sync/lock_db.txt"
              # if present then db is locked else none
        # self.logging_level      = logging.DEBUG   # ERROR

        self.icon               =  "./misc/db_red_on_black.png"

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

        computer_id         =  self.running_on.computer_id
            # same as hostname

        if computer_id == "smithers":
            self.win_geometry       = '1450x700+20+20'      # width x height position
            self.ex_editor          =  r"D:\apps\Notepad++\notepad++.exe"
            self.db_file_name       =  "smithers_db.db"

        # ---- king_homer_db  ThinkCentreThinkCentre
        elif computer_id == "kinghomer":
            self.ex_editor          =  r"xed"
            self.db_file_name       =  "./data/king_homer/stuffdb.db"

            self.picture_db_root    = "/mnt/8ball1/first6_root/PhotoDB/"
            self.picture_db_sub     = "/25"

        # ---- bulldog
        elif computer_id == "bulldog":
            self.ex_editor          =  "xed"
            self.db_file_name       =  "bulldog_db.db"

        # ----  ["millhouse", "millhouse-mint" ]
        elif computer_id in ["millhouse", "millhouse-mint" ]:
            self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"
            #self.win_geometry   = '1300x600+20+20'

            # type and location of the db file
            self.db_type            = "QSQLITE"
            self.db_file_name       = "./data/russ2025/russ2025.db"
            self.db_file_name       = "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/data/russ2025/russ2025.db"
            self.db_file_name       = "./data/russ2025/russ2025.db"
            self.db_file_name       = "./data/millhouse/millhouse.db"
            self.db_file_name       = "./data/millhouse/stuffdb.db"

            self.picture_db_root    = "/mnt/WIN_D/PhotoDB/"  # real thing
            self.picture_db_root    = "/home/russ/sync_with_fattony/PhotoDB"
            ## self.picture_db_root    = "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/data/test_photo/test_add_to_db"

            self.picture_db_sub     = "/99"
            self.picture_db_sub     = "/test_delete"
            self.picture_db_sub     = "/25"

            self.picture_browse     = "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/data/test_photo/test_add_to_db"
            self.picture_browse     = "/mnt/WIN_D/PhotosRaw/2025"

            self.logging_level      = logging.DEBUG   # ERROR

            self.icon               =  "./misc/db_red_on_yellow.png"
            self.icon               =  "./misc/db_green_on_black.png"
            #self.icon               =  "./misc/db_red_on_black.png"

        elif computer_id == "millhouse-mint":
            #self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"
            #self.win_geometry   = '1300x600+20+20'

            pass

        # ---- fattony
        elif computer_id == "fattony":
            self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"

            # ---- type and location of the db file
            self.db_type            = "QSQLITE"
            self.db_file_name       = "./data/russ2025/russ2025.db"
            self.db_file_name       = "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/data/russ2025/russ2025.db"
            self.db_file_name       = "./data/russ2025/russ2025.db"
            self.db_file_name       = "./data/fattony/stuffdb.db"


            self.db_file_name      = "./data_sync_b/stuffdb.db"      #  = "sample.db"   =  ":memory:"
            self.db_lock_file_name = "./data_sync_b/lock_db.txt"     # if present then db is locked else none

            self.icon              = "./misc/db_green_on_black.png"

            self.picture_db_root    = "/mnt/WIN_D/PhotoDB/"  # real thing
            ## self.picture_db_root    = "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/data/test_photo/test_add_to_db"
            self.picture_db_root    = "//media/russ/m_toshiba_silver/sync_on_fattony/PhotoDB"

            self.picture_db_sub     = "/99"
            self.picture_db_sub     = "/test_delete"
            self.picture_db_sub     = "/25"

            self.picture_browse     = "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/data/test_photo/test_add_to_db"
            self.picture_browse     = "/mnt/WIN_D/PhotosRaw/2025"

            self.logging_level      = logging.DEBUG   # ERROR
            self.logging_level      = logging.INFO

            # self.icon               =  "./misc/db_red_on_yellow.png"
            # self.icon               =  "./misc/db_green_on_black.png"
                                         #/misc/db_green_on_black.png
            # /mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/misc/db_green_on_black.png
            #self.icon               =  "./misc/db_red_on_black.png"

        # ---- "russ-thinkpad-p72": === theprof mint
        elif computer_id == "russ-thinkpad-p72":

            self.project_root       = "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb"
            # ---- ....appearance -- including sizes

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

            self.use_add_where      = True    # on criteria have add_where field
            self.use_geo_photo      = True   # True use the photo geo parts of app

            # ---- type and location of the db file
            self.db_type            = "QSQLITE"
            # self.db_file_name       = "./data/russ2025/russ2025.db"
            # self.db_file_name       = "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/data/russ2025/stuffdb.db"
            self.db_file_name       =  "./data/theprof/stuffdb.db"

            self.picture_db_root    = "/mnt/WIN_D/PhotoDB/"  # real thing
            ## self.picture_db_root    = "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/data/test_photo/test_add_to_db"

            self.picture_db_sub     = "/99"
            self.picture_db_sub     = "/test_delete"
            self.picture_db_sub     = "/25"

            self.picture_browse     = "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/data/test_photo/test_add_to_db"
            self.picture_browse     = "/mnt/WIN_D/PhotosRaw/2025"

            self.logging_level      = logging.DEBUG   # ERROR

            self.icon               =  "./misc/db_red_on_yellow.png"
            self.icon               =  "./misc/db_green_on_black.png"
            #self.icon               =  "./misc/db_red_on_black.png"

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

    # ---- ------->> default mode, always call
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

        self.project_root   = "./"  # might want to resolve

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

        # ---- appearance -- including sizes, notes_only

        self.notes_only         = False
            # only the notes part of the app
            # will be available

        # control initial size and position with:
        self.qt_width           = 1200
        self.qt_height          = 600
        self.qt_xpos            = 50
        self.qt_ypos            = 50

        # sizes for the wat-inspector in qt
        self.wat_qt_width       = 1300
        self.wat_qt_height      = 800
        self.wat_qt_xpos        = 10
        self.wat_qt_ypos        = 10

        # ---- doc is a mdi doc like a help_document
        self.doc_qt_width       = 900
        self.doc_qt_height      = 600
        self.doc_qt_xpos        = 20
        self.doc_qt_ypos        = 20

        self.set_maximized      = True   # maximize main window on startup
        self.set_doc_maximized  = True

        # icon for running app
        self.icon               = r"./misc/icon_red.png"
        self.icon               =  "./misc/binocular.png"
        self.icon               =  "./misc/iconfinder_database_103466.png"
        self.icon               =  "./misc/db_red_on_yellow.png"

        self.text_edit_font     = ("Arial", 12)

        # ---- logging
        self.pylogging_fn       = "./output/app.py_log"
            # file name for the python logging

        # next two seem redundant
        self.log_mode               = "w"    # "a" append "w" truncate and write
        self.delete_log_on_start    = True
            # if True you get a new log file every time the program starts

        self.logging_level          = logging.DEBUG         # may be very verbose
        self.logging_level          = logging.INFO
        self.logging_level          = logging.DEBUG
            # logging level used by app logger

        self.logger_id          = "stuffdb"
            # id of app in logging file

        # ---- file  and path names more
        self.picture_browse     = "/mnt/WIN_D/PhotosRaw/2024/pixel4a/july4"
            # browsing starts from here see PictureDocument

        # picture to use when a valid picture is not found or does not exist
        self.pic_nf_file_name   = "./misc/404.png"

        self.picture_db_root    = "/mnt/WIN_D/PhotoDB/"
            # all pictures once in the db should be under this directory

        self.picture_db_sub         = "test_delete for mode default"
                  # no leading /
                  # /mnt/WIN_D/temp_photo/dest/99
            # subdir for above used when adding new pictures

        self.output_dir             = "./output"
            # ISSUES WITH ./ SO USE FULL PATH FOR HOW -- RESOLVE IT LATER
            # the directory used for most output

        self.picture_editor         = "gimp-2.10"
            # the editor that will be envoked when you edit a picture

        # ---- .... db type POSTG and ...

        self.db_type            = "POSTG"

        self.db_host_name       = "localhost"
        self.db_port            = 5432
        self.db_name            = "russdb"
        self.db_user            = "russ"
        self.db_password        = "nopassword"

        # ---- .... db type QSQLITE and location of the db file
        self.db_type           = "QSQLITE"
            # the type of database, so far we only support SQLite

        # think for qt4_by_example not stuff
        self.db_file_name      = ":memory:"
        self.db_file_name      = "sample.db"   #  = "sample.db"   =  ":memory:"
        self.db_file_name      = "default.db"     #  = "sample.db"   =  ":memory:"
        self.db_lock_file_name = "./data/lock_db.txt"    # if present then db is locked
        #self.db_file_name        = "/tmp/ramdisk/qt_sql.db"

        # this is the name of a program: its executable with path info.
        # to be used in opening an external editor
        self.ex_editor         =  r"D:\apps\Notepad++\notepad++.exe"    # russ win 10
        self.ex_editor         = "xed"

        self.text_editor       = "xed"

        self.text_editor_list  = [ "xed", "gedit" ]

        # control button for editing the readme file
        self.readme_fn          = "readme_rsh.txt"   # or None to suppress in gui
            # a readme file accessible from the main menu

        # or anything else ( will try to shell out may or may not work )
        self.help_fn       =  "./docs/help.txt"   #  >>. this is the path to our main .py file self.py_path + "/" +
        self.help_path     =  "./docs"
            # what it says, but not used much as most help is in the db

        self.idle_venv     = "py_12_misc"   # idle will open in this python venv
            # path leading to all docs and help

        self.use_add_where = False    # on criteria have add_where field

        # default for the list
        self.add_where_defaults = [ "",
                                    "", ]

        # ---- file match tolerance
        self.dt_tolerance       = datetime.timedelta(  days=7, hours= 0,   )

        self.size_tolerance     = 1_000   # bytes

        # ---- screen dirt  -- tuples would do as well but would need code change
        self.screen_dirt   =    { "`":        "",
                                  "### ":     "",
                                  "###":      "",
                                  ">>>":      "",   }

        # ---- note_default_text
        # do not want to couple custom widgets to parametes, but maybe I should
        # or a try except to app globals ??
        self.note_default_text  = (
                                    ">>Search   .........\n"
                                    ">>Search   .........\n"
                                    "\n\n\n"
                                    ">>find_dn  .........\n"
                                    ">>find_dn  .........\n\n"
                                    )

        #self.note_default_text = textwrap.dedent( self.note_default_text ).strip()
        #self.help_file       =  "http://www.opencircuits.com/Python_Smart_ClipBoard"

        # ---- startup   for now choose from members of startup functions  -- add argument??
        #self.startup_function   = startup_functions.say_hello
        self.startup_function   = startup_functions.default_startup
            # function, perhaps open note_1 will be called at startup

        self.use_geo_photo     = False   # True use the photo geo parts of app
            # if true add a lot of dependencies

        self.poll_delta_t      = 200      # 200 ok at least on win longer does not fix linux prob
        self.poll_delta_t      = 100
            # not used, reserved if we add a second thread
            # how often we poll for clip changes, in ms,
            # think my computer works well as low as 10ms

        self.auto_run           = True  # run code examples -- !! what but needed

        # ---- templates snippets a bit odd to control left margin --
        self.num_help_snippets  = 4

        # ---- Python template
        self.text_snippets      = {}
        template_name           = "Python"
        template_text           = (
        """
        >>Py -------- a_python_template --------

        print( f"a_python_template { 0 = }" )

        >>end --------

        """ )
        self.text_snippets[template_name] = textwrap.dedent( template_text ).strip()

        # ----.... Bash template
        template_name          = "Bash"
        template_text          = (
        """
        >>Bash ------------ bash_template ------------
        ls -lah    /usr/bin/*.*
        pwd
        cd ~
        pwd
        cd  ../
        ls *.py

        >>end ------------

        """  )
        self.text_snippets[template_name] = textwrap.dedent( template_text ).strip()

        self.get_sudo      = True
            # check code for use

        # -------- Dividers  just dividers for text notes
        template_name          = "Dividers"
        template_text          = (
        """
        ============ note_about_what  ============


        ------------------------


        ============ end ============
        """  )
        self.text_snippets[template_name] = textwrap.dedent( template_text ).strip()

        # ---- ....text template
        template_name          = "Text"
        template_text          = (
        """
        >>Text  ./parameters.py
        """  )
        self.text_snippets[template_name] = textwrap.dedent( template_text ).strip()

        # ---- ...."Default Text"
        self.note_default_text
        template_name          = "Default Text"
        template_text          = self.note_default_text
        self.text_snippets[template_name] = textwrap.dedent( template_text ).strip()

        # ---- .... url template
        template_name          = "Url"
        template_text          = (
        """
        >>url  https://www.youtube.com/feed/subscriptions#on&off&types=uploads

        """  )
        self.text_snippets[template_name] = textwrap.dedent( template_text ).strip()

        # ---- .... idle_template
        template_name          = "Idle"
        template_text          = (
        """
        >>idle  -------- python_that_runs_this --------
        print( "high_their_sailor")
        print( "done")
        >>end --------

        """  )
        self.text_snippets[template_name] = textwrap.dedent( template_text ).strip()

        # ---- ....idle_file_template
        template_name          = "Idle_file"
        template_text          = (
        """
        >>idle_file   ./libs/example_file_in_libs.py
        """  )
        self.text_snippets[template_name] = textwrap.dedent( template_text ).strip()

        # ---- .... "Note Header"
        template_name          = "Note Header"
        template_text          = (
        """
        >>Search
        >>Search

        >>Find_dn
        >>Find_dn


        """  )
        self.text_snippets[template_name] = textwrap.dedent( template_text ).strip()
        a_dict     = self.text_snippets


        # ---- .... shell template
        template_name          = "Shell"
        template_text          = (
        """
        >>Shell  /mnt/WIN_D/PhotoDB/00/00july_06.jpg

        """  )
        self.text_snippets[template_name] = textwrap.dedent( template_text ).strip()
        a_dict     = self.text_snippets

        # ---- sort the templates so the user does not
        #print(  "sort on key item[0]" )
        self.text_snippets = {a_key: a_value for a_key, a_value in sorted( a_dict.items(), key = lambda item: item[0] ) }
        #print( b_dict )

        # ---- systems for helpdb ??alpha  to sort make all quotes the same
        self.systems_list      =  [    '',
                            'Arduino',
                            'Bash',
                            'CAD/Print',
                            'CompHard',
                            'Delete',
                            'Electronics',
                            'Garden',
                            'House',
                            'Linux',
                            'Powerbuilder',
                            'Programming',
                            'Python',
                            'RasPi',
                            'RshPy',
                            'Russ',
                            'SQL',
                            'StuffDB',
                            'TBD',
                            'Tools',
                            'Web',

                        ]

        # ---- add a sort for the systems

    #--------------------------
    def mode_from_command_line( self ):
        """
        checks to see if command line wants to set the mode
        this is done with an eval with just a bit of checking
        """
        if len( SYS_ARGS ) > 1:
            mode_str    = SYS_ARGS[1]

            if not mode_str.startswith( "mode_"):
                print( f"{mode_str = } needs to start with 'mode_'")
                return False

            exec_str           = f"self.{mode_str}()"
            try:
                eval( exec_str, globals(), locals()  )
            except ValueError as error:

                error_message = str(error)
                msg  = (f"Caught an error: {error_message} for {exec_str = }")
                print( msg )
                return False

            return True

        return False

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
                #  very dark greenhouse this has issues on RasPi
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
        print( str(AppGlobal.parameters))

        """
        # new_indented    = "\n    "   # but it nice to have some whitespace to see ...
        a_str = "\n "
        a_str   = f"{a_str}>>>>>>>>>>* Parameters (some) *<<<<<<<<<<<<"
        a_str   = string_utils.to_columns( a_str, ["mode",       f"{self.mode}" ] )
        a_str   = string_utils.to_columns( a_str, ["computer_id", f"{self.running_on.computer_id}" ] )



        a_str   = string_utils.to_columns( a_str, ["db_type",
                                           f"{self.db_type}" ] )


        a_str   = string_utils.to_columns( a_str, ["db_file_name",
                                           f"{self.db_file_name}" ] )

        a_str   = string_utils.to_columns( a_str, ["db_lock_file_name",
                                           f"{self.db_lock_file_name}" ] )


        a_str   = string_utils.to_columns( a_str, ["db_host_name",
                                           f"{self.db_host_name}" ] )


        a_str   = string_utils.to_columns( a_str, ["db_port",
                                           f"{self.db_port}" ] )

        a_str   = string_utils.to_columns( a_str, ["db_name",
                                           f"{self.db_name}" ] )

        a_str   = string_utils.to_columns( a_str, ["logger_id", f"{self.logger_id}" ] )
        a_str   = string_utils.to_columns( a_str, ["logging_level", f"{self.logging_level}" ] )
        a_str   = string_utils.to_columns( a_str, ["pylogging_fn",    f"{self.pylogging_fn}" ] )

        a_str   = string_utils.to_columns( a_str, [ "log_mode",
                                                  f"{self.log_mode}" ] )


        a_str   = string_utils.to_columns( a_str, [ "delete_log_on_start -- deprecate for log_mode",
                                                  f"{self.delete_log_on_start}" ] )

        a_str   = string_utils.to_columns( a_str, [ "use_geo_photo",
                                                  f"{self.use_geo_photo}" ] )

        a_str   = string_utils.to_columns( a_str, [ "use_add_where",
                                                  f"{self.use_add_where}" ] )
        # a_str   = string_util.to_columns( a_str, ["gui_text_log_fn", f"{self.gui_text_log_fn}" ] )

        a_str   = string_utils.to_columns( a_str, ["readme_fn", f"{self.readme_fn}" ] )
       # a_str   = string_utils.to_columns( a_str, ["help_file",    f"{self.help_file}" ] )


        a_str   = string_utils.to_columns( a_str, ["parameter_dir", f"{self.parameter_dir}" ] )
        a_str   = string_utils.to_columns( a_str, ["icon", f"{self.icon}" ] )


        a_str   = string_utils.to_columns( a_str, ["computername", f"{self.computername}" ] )
        a_str   = string_utils.to_columns( a_str, ["our_os", f"{self.our_os}" ] )
        a_str   = string_utils.to_columns( a_str, ["py_path", f"{self.py_path}" ] )
        a_str   = string_utils.to_columns( a_str, ["set_default_path_here", f"{self.set_default_path_here}" ] )
        a_str   = string_utils.to_columns( a_str, ["poll_delta_t", f"{self.poll_delta_t}" ] )



        a_str   = string_utils.to_columns( a_str, ["help_fn",
                                           f"{self.help_fn}" ] )
        a_str   = string_utils.to_columns( a_str, ["help_path",
                                           f"{self.help_path}" ] )

        # a_str   = string_utils.to_columns( a_str, ["log_gui_text",
        #                                    f"{self.log_gui_text}" ] )
        a_str   = string_utils.to_columns( a_str, ["opening_dir",
                                           f"{self.opening_dir}" ] )
        a_str   = string_utils.to_columns( a_str, ["os_win",
                                           f"{self.os_win}" ] )
        a_str   = string_utils.to_columns( a_str, ["picture_browse",
                                           f"{self.picture_browse}" ] )


        a_str   = string_utils.to_columns( a_str, ["picture_db_root",
                                           f"{self.picture_db_root}" ] )
        a_str   = string_utils.to_columns( a_str, ["picture_db_sub",
                                           f"{self.picture_db_sub}" ] )

        a_str   = string_utils.to_columns( a_str, ["pic_nf_file_name",
                                           f"{self.pic_nf_file_name}" ] )


        a_str   = string_utils.to_columns( a_str, ["platform",
                                           f"{self.platform}" ] )
        a_str   = string_utils.to_columns( a_str, ["qt_height",
                                           f"{self.qt_height}" ] )
        a_str   = string_utils.to_columns( a_str, ["qt_width",
                                           f"{self.qt_width}" ] )
        a_str   = string_utils.to_columns( a_str, ["qt_xpos",
                                           f"{self.qt_xpos}" ] )
        a_str   = string_utils.to_columns( a_str, ["qt_ypos",
                                           f"{self.qt_ypos}" ] )


        a_str   = string_utils.to_columns( a_str, ["wat_qt_height",
                                           f"{self.wat_qt_height}" ] )
        a_str   = string_utils.to_columns( a_str, ["wat_qt_width",
                                           f"{self.wat_qt_width}" ] )
        a_str   = string_utils.to_columns( a_str, ["wat_qt_xpos",
                                           f"{self.wat_qt_xpos}" ] )
        a_str   = string_utils.to_columns( a_str, ["wat_qt_ypos",
                                           f"{self.wat_qt_ypos}" ] )


        a_str   = string_utils.to_columns( a_str, ["running_on",
                                           f"{self.running_on}" ] )

        return a_str

        #---- sort into above


# something like this for creating on import
# ---------------
def create_if_needed( ):
    global PARAMETERS
    if not PARAMETERS:

        print( "create_if_needed creating global parameters.PARAMETERS")
        PARAMETERS    = Parameters()

# --------------------

create_if_needed()


# =================== eof ==============================
# ---- eof



