# -*- coding: utf-8 -*-
# ---- tof

"""
    temporary parameters    for  stuffdb
    to run along with sql utils

"""


from pathlib import Path



import logging
import os
import sys

import running_on
import string_util
# from app_global import AppGlobal

VERBOSE   = False
SYS_ARGS  = sys.argv


# if VERBOSE:
#     print( "parameters from -----  /_projects/stuffdb/parameters.py")
#     print( __file__ )

#===========================
class ParmsTemp( ):
    """
    manages parameter values: use it like an ini file but it is code
    """

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

        self.text_edit_font     = ("Arial", 12)

        # ---- logging
        self.pylogging_fn           = "./logs/app.py_log"
            # file name for the python logging

        # next two seem redundant
        self.log_mode               = "w"    # "a" append "w" truncate and write
        self.delete_log_on_start    = True
            # if True you get a new log file every time the program starts

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

        # ---- db type and location of the db file
        self.db_type                = "QSQLITE"
            # the type of database, so far we only support SQLite

        # self.db_fn              = "./data/appdb.db"
        # self.db_fn              = "/mnt/WIN_D/Russ/0000/python00/python3/_projects/stuffdb/data/sept_26.db"
        # self.db_fn              = "/tmp/ramdisk/sept_28.db"
        # self.db_fn              = "/tmp/ramdisk/sept_35.db"

        # think for qt4_by_example not stuff
        self.db_file_name      = ":memory:"
        self.db_file_name      = "/tmp/ramdisk/russ2025/russ2025.db"
        self.db_file_name      = "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/data/russ2025/russ2025.db"
        self.db_file_name      = "/tmp/ramdisk/russ2025/stuffdb.db"



        self.idle_venv          = "py_12_misc"   # idle will open in this python venv
            # path leading to all docs and help

        #self.help_file       =  "http://www.opencircuits.com/Python_Smart_ClipBoard"

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

        # ---- systems for helpdb ??alpha  to sort make all quotes the same
        self.systems_list      =  [    '',
                            'Bash',
                            'CAD/Print',
                            'Delete',
                            'Electronics',
                            'House',
                            'Linux',
                            'Powerbuilder',
                            'Programming',
                            'Python',
                            'RasPi',
                            'RshPy',              # subsystem the project
                            'Russ',
                            'StuffDB',
                            'TBD',
                            'Tools',

                        ]

    # ------->> default mode, always call
    def mode_from_command_line( self ):
        """
        checks to see if command line wants to set the mode
        note case statement so need to set up
            this sort of sucks esp since qt captures the exception
            consider something more like eval, perhaps hasattr
            and a dialog on failure
        """
        if len( SYS_ARGS ) > 1:
            mode_string     = SYS_ARGS[1]

            if mode_string     == "mode_new_user":
                self.mode_new_user()

            elif mode_string   == "mode_helpdb_on_theprof":
                self.mode_helpdb_on_theprof()

            elif mode_string   == "mode_github_example_code_on_theprof":
                self.mode_github_example_code_on_theprof()

            else:
                print( f"unknown_mode_string {mode_string =}")
                1/0   # !! fix better
            return True

        return False


    # -------
    def __init__( self, ):
        """
        Init for instance, usually not modified, except perhaps debug stuff
        ( if any )... but use plus_test_mode()
        may be down in listing because it should not be messed with.
        """
        #AppGlobal.parameters       = self   # register as a global -- phase out
        self.mode_default()
        #

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
        """
        # new_indented    = "\n    "   # but it nice to have some whitespace to see ...
        a_str = "\n "
        a_str   = f"{a_str}>>>>>>>>>>* ParmsTemp (some) *<<<<<<<<<<<<"
        a_str   = string_util.to_columns( a_str, ["mode",       f"{self.mode}" ] )
        a_str   = string_util.to_columns( a_str, ["computer_id", f"{self.running_on.computer_id}" ] )
        a_str   = string_util.to_columns( a_str, ["db_file_name",
                                           f"{self.db_file_name}" ] )

        a_str   = string_util.to_columns( a_str, ["db_type",
                                           f"{self.db_type}" ] )



        # a_str   = string_util.to_columns( a_str, ["parameter_dir", f"{self.parameter_dir}" ] )
        # a_str   = string_util.to_columns( a_str, ["icon", f"{self.icon}" ] )


        # a_str   = string_util.to_columns( a_str, ["computername", f"{self.computername}" ] )
        # a_str   = string_util.to_columns( a_str, ["our_os", f"{self.our_os}" ] )
        # a_str   = string_util.to_columns( a_str, ["py_path", f"{self.py_path}" ] )
        # a_str   = string_util.to_columns( a_str, ["set_default_path_here", f"{self.set_default_path_here}" ] )
        # a_str   = string_util.to_columns( a_str, ["poll_delta_t", f"{self.poll_delta_t}" ] )



        return a_str



# something like this for creating on import
# ---------------
def create_if_needed_disabled( ):
    pass
#     global PARAMETERS
#     if not PARAMETERS:

#           print( "creating global parameters.PARAMETERS")
#           PARAMETERS    = Parameters(




# =================== eof ==============================
# ---- eof
