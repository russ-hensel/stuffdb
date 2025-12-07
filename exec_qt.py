# -*- coding: utf-8 -*-
\
# ---- tof
""""
Purpose:
    run a bit of python code and capture output
/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/exec_qt.py

Status:
     just started from wat_inskpector -- not sure why different
     becareful with dual codebase

    ...

References:

import ex_qt



"""
# ---- imports
#import adjust_path
import dis
import inspect
import io
import pprint
import subprocess
import sys
import traceback
from functools import partial
from pprint import pprint as pp
from subprocess import PIPE, STDOUT, Popen, run

# import wat

from qt_compat import QApplication, QAction, exec_app, qt_version
from PyQt.QtWidgets import QMainWindow, QToolBar, QMessageBox



from PyQt import QtGui
from PyQt.QtGui import QFont
from PyQt.QtCore import QDate, QDateTime, QModelIndex, Qt, QTimer
from PyQt.QtGui import QTextCursor, QTextDocument
# sql
from PyQt.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel

# from PyQt.QtGui import ( QAction, QActionGroup, )
from PyQt.QtWidgets import (
                             QApplication,
                             QButtonGroup,
                             QCheckBox,
                             QComboBox,
                             QDateEdit,
                             QDialog,
                             QGridLayout,
                             QGroupBox,
                             QHBoxLayout,
                             QLabel,
                             QLineEdit,
                             QListWidget,
                             QListWidgetItem,
                             QMainWindow,
                             QMenu,
                             QMessageBox,
                             QPushButton,
                             QRadioButton,
                             QTableView,
                             QTableWidget,
                             QTableWidgetItem,
                             QTabWidget,
                             QTextEdit,
                             QVBoxLayout,
                             QWidget)



# import info_about

       # self.setWindowTitle( msg  )

        # self.last_get_wat_str_obj   = None

        # if my_parameters is None:
        #     qt_xpos             = 5AUTORUN0
        #     qt_ypos             = 50
        #     qt_width            = 1200
        #     qt_height           = 600

        # else:
        #     qt_xpos             = my_parameters.wat_qt_xpos
        #     qt_ypos             = my_parameters.wat_qt_ypos
        #     qt_width            = my_parameters.wat_qt_width
        #     qt_height           = my_parameters.wat_qt_height

        # self.setGeometry(  qt_xpos,
        #                    qt_ypos ,
        #                    qt_width,
        #                    qt_height  )
# ---- module instances

a_wat_inspector         = None
go                      = None    # dialog.setup_go
display_wat             = None
testing                 = True
import info_about

#print( f"{info_about.INFO_ABOUT =}")

# for use in code this needs to be defined
# back in base_doxument perhaps


FIF       = info_about.INFO_ABOUT.find_info_for

def print_info_about( obj, msg ):
    FIF( obj, msg, print_it = True )

PFA  = print_info_about

# ---- a few parameters for you

try:
    import parameters
    my_parameters = parameters.Parameters()
    print( "import of parameters in wat_inspector ok ")

except:
    my_parameters = None
    print( "import of parameters in wat_inspector failed -------------------------------------- ")

if my_parameters is None:
    TEXT_EDITOR    = "gedit"
    AUTO_RUN       = True

else:
    TEXT_EDITOR    = my_parameters.text_editor
    AUTO_RUN       = my_parameters.auto_run



# !! need implementation
HELP_FILE          = "help.txt"
OUTPUT_FILE        = "output.txt"


# -----------------------
def get_traceback_list_aaaa( msg = "get_traceback_list", print_it = True ):
    """
    get_traceback_list()

    """
    stop_text = "main.py"

    #stop_text  File "/mnt/WIN_D/Russ/0000/python00/python3/_projects/rshlib/debug_util.py", line 171, in call_tbl

    keep = True
    short_list  = [">>>>>>>>>>>>>see what inspector instead get_traceback_list<<<<<<<<<<<<<<<<<<<<<<"]
    for i_item in reversed( traceback.format_stack() ):

        if keep:
            short_list.append( i_item )

            if stop_text in i_item:
                print( "stop ---------------------------------------")
                keep = False
    short_list.append( msg )
    short_list.append( ">>>>>>>>>>>>>get_traceback_list<<<<<<<<<<<<<<<<<<<<<<" )

    short_list    = list( reversed( short_list ) )
    if print_it:
        for i_item in short_list:
            print( i_item )

    return short_list

# ------------------------------------
class ExecWindow( QDialog ):
    """
    window for the wat inspector
    """
    # ------------------------------------------
    def __init__(self,
                 app,
                 parent = None,
                 # *,
                 # code,
                 # globals,
                 # locals,
                 ):
        """
        the usual
        """
        super().__init__( parent )
        # self.locals      = locals
        # self.code        = code
        # self.globals     = globals

        self.app      = app

        self._build_gui()

        msg   = "Exec QT not wat_inspector"
        self.setWindowTitle( msg  )

        self.last_get_wat_str_obj   = None

        if my_parameters is None:
            qt_xpos             = 50
            qt_ypos             = 50
            qt_width            = 1200
            qt_height           = 600

        else:
            qt_xpos             = my_parameters.wat_qt_xpos
            qt_ypos             = my_parameters.wat_qt_ypos
            qt_width            = my_parameters.wat_qt_width
            qt_height           = my_parameters.wat_qt_height

        self.setGeometry(  qt_xpos,
                            qt_ypos ,
                            qt_width,
                            qt_height  )

        self.last_position = 0

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says, read?
        """
        # self._build_menu() some issues here

        layout          = QVBoxLayout( self )
        self.layout     = layout

        row_layout      = QHBoxLayout(   )
        layout.addLayout( row_layout )

        # ---- msg_label
        widget          = QLabel( "msg goes here " )
        self.msg_label  = widget
        row_layout.addWidget( widget,  )

        # ----
        row_layout      = QHBoxLayout(   )
        layout.addLayout( row_layout )

        # widget        = QPushButton( "Where" )
        # widget.clicked.connect(  self.do_where_am_i )
        # row_layout.addWidget( widget,   )

        # # ---- Cust Inspect
        # widget          = QPushButton( "Cust Inspect" )
        # widget.clicked.connect(         self.do_info_about )
        # row_layout.addWidget( widget,   )

        # # ---- Cust Inspect
        # widget          = QPushButton( "Get Super" )
        # widget.clicked.connect(         self.do_get_super )
        # row_layout.addWidget( widget,   )

        # # ---- Obj Help
        # widget          = QPushButton( "Obj Help" )
        # widget.clicked.connect(         self.do_type_help )
        # row_layout.addWidget( widget,   )

        # ---- Obj Help
        widget          = QPushButton( "Exec Code" )
        widget.clicked.connect(         self.exec_code )
        row_layout.addWidget( widget,   )

        row_layout      = QHBoxLayout()
        layout.addLayout( row_layout )

        widget              = QLabel( "Code" )
        row_layout.addWidget( widget,   )

        # widget              = QLabel( "Globals" )
        # row_layout.addWidget( widget,   )

        # ----new row
        row_layout      = QHBoxLayout(   )
        layout.addLayout( row_layout )

        widget                  = QTextEdit(    )
        self.code_text_widget   = widget
        font                    = QFont( "Courier New" )  # Set a monospaced font "Courier New"
        font.setPointSize(12)
        widget.setFont(font)
        #widget.setGeometry( 50, 50, 200, 200 )
        # widget.itemClicked.connect( self.do_inspect_clicked_local )
        row_layout.addWidget( widget,   )

        # # ---- globals
        # widget              = QListWidget(    )
        # self.global_widget  = widget
        # #widget.setGeometry( 50, 50, 200, 200 )
        # widget.itemClicked.connect( self.do_inspect_clicked_global )
        # row_layout.addWidget( widget,   )

        row_layout      = QHBoxLayout()
        layout.addLayout( row_layout )

        # ---- text edit
        widget                      = QTextEdit()
        #self.text_edit              = widget
        self.output_text_widget     = widget
        font                        = QFont( "Courier New" )  # Set a monospaced font "Courier New"
        font.setPointSize(12)
        widget.setFont(font)

        row_layout.addWidget( widget,   )

        # ---- bottom and buttons
        button_layout           = QHBoxLayout()
        layout.addLayout( button_layout,    )

        widget                  = QLineEdit()
        self.line_edit          = widget
        widget.setPlaceholderText("Enter search text")
        button_layout.addWidget( widget, )

        # Buttons
        widget                  = QPushButton("Down")
        self.down_button        = widget
        widget.clicked.connect(self.search_down)
        button_layout.addWidget( widget,   )

        widget           = QPushButton("Up")
        self.up_button   = widget
        widget.clicked.connect(self.search_up)
        button_layout.addWidget( widget,   )

        button_layout           = QHBoxLayout()
        layout.addLayout( button_layout,     )

        # ---- next bottom layout
        button_layout           = QHBoxLayout()
        layout.addLayout( button_layout,      )
        chat = """
        In a QComboBox, there isn't a direct signal equivalent to returnPressed like in QLineEdit. However, you can achieve similar behavior depending on what you're trying to accomplish:

    Detect when the user presses Enter while editing the text
    If your QComboBox is editable, you can use the lineEdit() method to access the embedded QLineEdit and connect its returnPressed signal.
    combo_box = QComboBox()
combo_box.setEditable(True)
widget.lineEdit().returnPressed.connect(your_function)


"""
        # ---- Filters
        widget                  = QComboBox()
        self.filter_widget      = widget
        widget.setEditable( True )
        widget.lineEdit().returnPressed.connect( self.filter ) # setEditable first
        #widget.setPlaceholderText( "Enter filter text" )
        button_layout.addWidget( widget, )

        values    =  [ "def", "class"]
        for value in values:
            #item = QListWidgetItem( value )
            widget.addItem( value )

        widget                  = QPushButton("Filter Beginning of Line")
        #self.down_button        = widget
        widget.clicked.connect( self.filter )
        button_layout.addWidget( widget,   )

        # ---- next bottom layout
        button_layout           = QHBoxLayout()
        layout.addLayout( button_layout,    )

        # ---- QListWidget
        widget                  = QComboBox(    )
        self.filter_widget_sil  = widget
        widget.setEditable( True )
        widget.lineEdit().returnPressed.connect( self.filter_sil )
        #widget.setGeometry( 50, 50, 200, 200 )
        # widget.setPlaceholderText( "Enter filter text" )
        button_layout.addWidget( widget, )

        values    =  [ "height",
                       "width",
                       "size",
                       "action",
                       "event",
                       "index",
                       "count"
                      ]
        for value in values:
            #item = QListWidgetItem( value )
            widget.addItem( value )

        # ---- "Filter SIL"
        widget                  = QPushButton("Filter Somewhere in Line")
        #self.down_button        = widget
        widget.clicked.connect( self.filter_sil )
        button_layout.addWidget( widget,   )

        # ---- another button layout
        button_layout           = QHBoxLayout()
        layout.addLayout( button_layout,     )

        a_widget                = QPushButton("Append to File")
        self.save_button        = a_widget
        a_widget.clicked.connect(         self.write_file )
        button_layout.addWidget( a_widget )

        a_widget                = QPushButton("Edit File")
        self.save_button        = a_widget
        a_widget.clicked.connect(         self.edit_file )
        button_layout.addWidget( a_widget )

        a_widget                = QPushButton("Help")
        self.save_button        = a_widget
        a_widget.clicked.connect(         self.open_general_help )
        button_layout.addWidget( a_widget )

        a_widget                = QPushButton("Run")
        a_widget.clicked.connect(         self.exec_code )
        #self.save_button        = a_widget
        #a_widget.clicked.connect(   self.do_ok )
        button_layout.addWidget( a_widget )

        a_widget                = QPushButton("Done")
        self.save_button        = a_widget
        a_widget.clicked.connect(   self.do_ok )
        button_layout.addWidget( a_widget )

    # ------------------------------------
    def _build_menu( self,  ):
        """
        what it say
            may not be able to have a menu bar on this type of widget
        """
        menubar         = self.menuBar()
        self.menubar    = menubar

        # a_menu.addSeparator()

        # ---- Help
        menu_help       = menubar.addMenu( "Help" )

        action          = QAction( "README.md...", self )
        connect_to      = partial( self.open_txt_file, "README.md" )
        action.triggered.connect( connect_to )
        menu_help.addAction( action )

        action          = QAction( "General Help...", self )
        connect_to      = partial( self.open_txt_file, HELP_FILE )
        action.triggered.connect( connect_to )
        menu_help.addAction( action )

        action          = QAction( "Developer Notes...", self )
        connect_to      = partial( self.open_txt_file, "readme_rsh.txt" )
        action.triggered.connect( connect_to )
        menu_help.addAction( action )

    #-------
    def open_general_help( self,   ):
        """
        what it says read:
        """
        doc_name           = HELP_FILE
        ex_editor          = TEXT_EDITOR
        proc               = subprocess.Popen( [ ex_editor, doc_name ] )

    # ----------------------------------------
    def exec_and_display_print( self, ):
        """
        what it says
        """
        code            = self.code_text_widget.toPlainText() # so users can edit

        original_stdout = sys.stdout
        captured_output = io.StringIO()

        try:
            sys.stdout  = captured_output  # Redirect stdout to the string buffer
            result      = exec( code, self.globals, self.locals )


        except Exception as an_exception:
            msg        = f'**** exec caused exception {an_exception}'
            print( msg )
            s_trace = traceback.format_exc()
            msg     = f"format-exc       >>{s_trace}<<"
            print( msg )


        finally:
            sys.stdout = original_stdout  # Restore the original stdout


        #rint( "exe_qt exec_and_display_print ---------- end_capture_here ----------------")

        # Get the captured content as a string
        captured_content = captured_output.getvalue()
        # rint("Captured Content:")
        #rint(captured_content)

        # Cleanup
        captured_output.close()

        #title       = "what title "
        title       = self.msg
        self.display_text( title = title, main_text = captured_content )

    # ------------------------------------------
    def exec_code( self,    ):
        """
        what it says, read?
        """
        self.exec_and_display_print()

        return

        do_wat      = True
        code        = self.code
        try:
            result   = exec( code, self.globals, self.locals )

        except Exception as an_except:
            msg     = f"a_except         >>{an_except}<<  type  >>{type( an_except)}<<"
            print( msg )

            msg     = f"an_except.args   >>{an_except.args}<<"
            print( msg )

            s_trace = traceback.format_exc()
            msg     = f"format-exc       >>{s_trace}<<"
            print( msg )

            result   = "got exception "
            do_wat   = False

        if do_wat:
            main_text   = self.get_wat_str(  result )
            title        = f"Eval -> {code}"

        else:
            title       = f"Eval -> {code}"
            main_text   = s_trace

        self.display_text( title = title, main_text = main_text )

    # # ------------------------------------------
    # def do_info_about( self ):
    #     """
    #     what it says
    #     """
    #     #main_text   = self.info_about.get_info( self.last_get_wat_str_obj , msg = "what about it " )
    #     main_text   = FIF( self.last_get_wat_str_obj, msg = "what about it " )

    #     self.display_text( title = "info_about", main_text = main_text )

    # # ------------------------------------------
    # def get_source_code( self, ):
    #     """
    #     It does not work for built-in functions, classes, or objects defined interactively.
    #     Dynamic Objects: If the object is dynamically created
    #     (e.g., using exec or lambda), inspect.getsource() might not work.
    #     """
    #     # or consider ( or both? )
    #     self.get_source_code_eval()
    #     return

    #     # --- return above ?
    #     try:
    #         # Retrieve the source code of the object
    #         obj_type     = type( self.last_get_wat_str_obj )
    #         source_code  = inspect.getsource( obj_type )

    #     except Exception as e:
    #         source_code  =   f"Could not retrieve source { obj_type = } code due to exception {e = }"

    #     self.display_text( title = "Source Code", main_text = source_code )

    # ------------------------------------------
    def get_source_code_eval( self, ):
        """
        suggested by chat that it might work were direct code fails,
        seems a bit dubious
        """
        try:
            # Retrieve the source code of the object
            obj_type     = type( self.last_get_wat_str_obj )
            code         = "inspect.getsource( obj_type ) "
            source_code  = eval( code, globals(), locals() )

        except Exception as e:
            source_code  =   f"Could not retrieve source { obj_type = } code due to exception {e = }"

        self.display_text( title = "Source Code", main_text = source_code )

    # # ------------------------------------------
    # def do_type_help( self ):
    #     """
    #     get help for the obect
    #     """
    #     help_text     = self.get_help_as_string( self.last_get_wat_str_obj )

    #     self.display_text( title = "Object Help", main_text = help_text )


    # ------------------------------------------
    def do_test( self ):
        """
        """
        main_text   = self.info_about.get_info( self.last_get_wat_str_obj , msg = "what about it " )

        self.display_text( title = "info_about", main_text = main_text )

    # # ------------------------------------------
    # def do_where_am_i( self ):
    #     """
    #     """
    #     print(f"where_am_i   {''}")
    #     widget              = self.text_edit
    #     widget.clear()
    #     debug               = get_traceback_list()
    #     main_text           = "\n".join( get_traceback_list() )
    #     title               = "Where in the code are you:"

    #     self.display_text( title = title, main_text= main_text )

    # ------------------------------------------
    def setup_go(   self,
                    *,
                    code           = None,
                    a_locals       = None,
                    a_globals      = None,
                    msg            = "no message given for this code",
                    autorun        = AUTO_RUN ):   # probably AUTORUN  or out to caller
        """
        what it says.
        """
        #rint( f"setup_go with {msg = } " )
        self.autorun  = autorun
        if code is None:
            1/0
        self.msg     = msg
        self.msg_label.setText( msg )
        self.setup( code = code,   a_locals = a_locals, a_globals = a_globals   )
        #self.do_inspect( inspect_me )
        self.show()
        if self.autorun:
            self.exec_code()
        # print( "next app exec can we see if already running?")
        # self.app.exec_()
        # print( "after  app exec can we see if already running?")

    # ------------------------------------------
    def setup( self, *, code,  a_locals = None,  a_globals = None ):
        """
        what it says.
        """
        self.code       = code
        self.code_text_widget.setText( code )

        self.locals          = a_locals
        self.globals         = a_globals


    # # ------------------------------------------
    # def do_inspect_clicked_global( self, item  ):
    #     """
    #     what it says
    #     """
    #     widget              = self.global_widget
    #     # row                 = widget.row( item )

    #     text               = item.text()
    #     i_object           = self.globals[ text ]

    #     title         = f"Global -> {text}"
    #     main_text     = self.get_wat_str( i_object )
    #     self.display_text( title = title, main_text = main_text )


    # ---------------------
    def filter_sil( self ):
        """
        filter the lines based on text at start:
            ignore blank space
            case insensitive
        """
        #print( self.filter_widget_sil.currentText() )

        filter_text = self.filter_widget_sil.currentText().casefold()
        all_text    = self.output_text_widget.toPlainText()
        splits      = all_text.split( "\n" )

        new_lines   = []

        for i_split in splits:
            i_test    = i_split.strip()
            if  filter_text   in  i_test.casefold():
                new_lines.append( i_split )

        #rint( new_lines )
        new_text       = "\n".join( new_lines )
        self.display_text( f"Results filtered on {filter_text}", new_text )

    # ---------------------
    def filter( self ):
        """
        filter the lines based on text at start:
            ignore blank space
            case insensitive
        """
        filter_text = self.filter_widget.currentText().casefold()
        all_text    = self.output_text_widget.toPlainText()
        splits      = all_text.split( "\n" )

        new_lines   = []

        for i_split in splits:
            i_test    = i_split.strip()
            if i_test.casefold().startswith( filter_text ):
                new_lines.append( i_split )

        #rint( new_lines )
        new_text       = "\n".join( new_lines )
        self.display_text( f"Results filtered on {filter_text}", new_text )

    #  --------
    def copy_all_text( self, text_edit ):
        """
        what it says
            copy into clipboard -- may be messed up on wich widget
        """
        # Save current cursor position
        cursor = text_edit.textCursor()
        original_position = cursor.position()

        text_edit.selectAll()
        text_edit.copy()   # goed to clipboard
        all_text = text_edit.toPlainText()

        # Restore cursor
        cursor.setPosition(original_position)
        text_edit.setTextCursor(cursor)
        return  all_text

    # ------------------------------------------
    def write_file( self,   ):
        """
        read it
        !! add the message and some seperation .. other stuff ?
        """
        my_text    = self.copy_all_text( self.output_text_widget )

        file_name  = OUTPUT_FILE
        with open( file_name, 'a') as a_file:    # a will append so file should be deleted time to time "w" will be for write no append ?
            a_file.write( my_text)     # f"{i_line}\n" )

    # ------------------------------------------
    def edit_file( self,   ):
        """
        read it
        """
        file_name           = OUTPUT_FILE
        ex_editor           = TEXT_EDITOR
        proc                = subprocess.Popen( [ ex_editor, file_name ] )

    # ------------------------------------------
    def inspect_object( self, an_object  ):
        """
        what it says, read?
        output result to text_edit widget
        """
        #rint( "inspect_object >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        #print( f"i_object { self.inspect_me = }   {type( self.inspect_me ) = }")
        widget              = self.output_text_widget
        widget.clear()
        #self.inspect_me     = inspect_me
        ex_text             = self.get_wat_str( an_object )
        cursor              = widget.textCursor()

        ex_text    = f"inspect_object { '' }: \n {ex_text}"
        cursor.insertText( ex_text )

        cursor.movePosition(QTextCursor.Start)   # .End
        widget.setTextCursor(cursor)

    # # --------------------------
    # def get_wat_str( self,  obj, options_dict = None ):
    #     """
    #     get the string from wat
    #     """
    #     msg      = wat( obj, str = True, gray = True )

    #     self.last_get_wat_str_obj  = obj

    #     return msg

    def display_text( self, title = "no_title_fix", main_text = "this_sis_the_main_text" ):
        """
        what it says, read
            leave cursor at top
        """
        full_text           = f"{title}\n\n{main_text}"

        widget              = self.output_text_widget
        widget.clear()
        #self.inspect_me     = inspect_me

        cursor              = widget.textCursor()

        cursor.insertText( full_text )

        cursor.movePosition(QTextCursor.Start)   # or .End
        widget.setTextCursor( cursor )

    # ---------------------
    def search_down(self):
        """
        search for text
            case insensitive
        """
        search_text = self.line_edit.text()
        if search_text:
            cursor = self.output_text_widget.textCursor()
            cursor.setPosition( self.last_position )
            found = self.output_text_widget.find(search_text)

            if found:
                self.last_position = self.output_text_widget.textCursor().position()
            else:
                # Reset position if end is reached and no match
                self.last_position = 0

    # ---------------------
    def search_up(self):
        search_text = self.line_edit.text()
        if search_text:
            cursor = self.output_text_widget.textCursor()
            cursor.setPosition( self.last_position )
            # Use QTextDocument.FindBackward for backward search
            found = self.output_text_widget.find(search_text, QTextDocument.FindBackward)

            if found:
                self.last_position = self.output_text_widget.textCursor().position()
            else:
                # Reset position if start is reached and no match
                self.last_position = self.output_text_widget.document().characterCount()

    #-------
    def open_txt_file( self, file_name  ):
        """
        what it says
        """
        proc               = subprocess.Popen( [ TEXT_EDITOR, file_name ] )

    def do_ok( self ):
        """
        close out window
        """
        self.accept()

# ------------------------------------
class ExecRunner(   ):
    """
    main class for the inspector basically to create the window
    """
    # ------------------------------------------
    def __init__(self,  app,  parent = None ):
        """

        """
        # global    display_wat
        # global    app_for_wat
        # global    go
        # global    a_wat_inspector

        # a_wat_inspector      = self
        # go                   = self.create_window

        # self.last_get_wat_str_obj  = None

        self.app            = app

        # self.wat_window     = None    # not sure which kind to use
        # self.parent         = parent  # parent may be a function use parent_window
        # self.parent_window  = parent

    # --------------------------
    def create_window( self,
                              code,
                              a_locals   = None,
                              a_globals  = None,
                              msg        = None,
                              autorun    = False):

        """ """
        self.window    = ExecWindow( self.app )  # is necessary ??
        # self.window.show( )
        self.window.setup_go(   code        = code,
                                a_locals    = a_locals,
                                a_globals   = a_globals,
                                msg         = msg,
                                autorun     = autorun)

    # # ------------------------------------------
    # def setup_go(   self,
    #                 *,
    #                 a_locals       = None,
    #                 a_globals      = None,
    #                 msg            = "no message" ):



        self.app.exec_()

# -----------------
def run_test():
    """
    example run/sanity test
    """
    app          = QApplication(  [] )  # Create the QApplication instance

    runner       = ExecRunner( app  )

    a_local_list    = [ 1,2,3,5 ]

    runner.create_window(
                code     = "1+1 \n2+ 2\nprint( 'hello')  ",
                a_locals   = locals(),
                a_globals  = globals(),
                msg        = "my message in argument" )

# --------------------
if __name__ == "__main__":
    #----- for running examples
    run_test()



"""

Scratch text:


-


"""

# ---- eof






