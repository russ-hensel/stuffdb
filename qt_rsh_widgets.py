

# ---- tof
""""










Put all work into the tabs of WidgetExample
    except perhaps for placer work in second example
    rest for code extraction and deletion


       a_widget  = QLabel( "Vd Start Date" )
        #placer.new_row()
        placer.place( a_widget )

        a_widget    = QDateEdit()
        a_widget.setCalendarPopup( True )
        a_widget.setDate(QDate( 2022, 1, 1 ))

        placer.place( a_widget )
        self.vid_start_date_widget    = a_widget

        # ----
        a_widget  = QLabel( "Vd End Date" )
        #placer.new_row()
        placer.place( a_widget )

        a_widget    = QDateEdit()
        a_widget.setCalendarPopup( True )
        a_widget.setDate(QDate( 2025, 1, 1 ))
        placer.place( a_widget )
        self.vid_end_date_widget    = a_widget
"""
# ---- search
"""
    Search for the following in the code below:

        border        -- only on some widgets not QWidget
        button
        checkbox
        combobox     is a dropdownlist ddl
        edit          QLineEdit,   QTextEdit,
        action
        menu
        groupbox
        isChecked
        get_text
        label
        lineEdit
        listbox      QListWidget         in ex_  listbox
        icon
        MessageBox     QMessageBox
        qdate
        self.showMinimized()
        minimized
        show
        iconify
        radiobutton
        radiobutton index
        row
        size
        text
        textOnLeft           for radiobutton
        widget
        partial

    See Also:

    Links
        Create Python GUIs with PyQt5 — Simple GUIs to full apps
            *>url  https://www.pythonguis.com/pyqt5/
        Qt Widget Gallery | Qt Widgets 5.15.14
            *>url  https://doc.qt.io/qt-5/gallery.html
        Widgets Classes | Qt Widgets 5.15.14
            *>url  https://doc.qt.io/qt-5/widget-classes.html


"""

# ---- imports


import time
from platform import python_version

import wat

import adjust_path

print( f"your python version is: {python_version()}"  )   # add to running on

# import PyQt5.QtWidgets as qtw    #  qt widgets avaoid so much import below
# from   PyQt5.QtCore import Qt, QTimer
# from   PyQt5 import QtGui


# ---- imports neq qt

import inspect
#import ia_qt
import subprocess
import sys
#import datetime
from datetime import datetime
# import PyQt5.QtWidgets as qtw    #  qt widgets avaoid so much import above
from functools import partial
from subprocess import PIPE, STDOUT, Popen, run


from PyQt5 import QtGui
from PyQt5.QtCore import QDate, QDateTime, QModelIndex, Qt, QTimer
from PyQt5.QtGui import QTextCursor
# sql
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
# widgets bigger
# widgets -- small
# layouts
from PyQt5.QtWidgets import (QAction,
                             QApplication,
                             QButtonGroup,
                             QCheckBox,
                             QComboBox,
                             QDateEdit,
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
                             QSizePolicy,
                             QTableView,
                             QTableWidget,
                             QTableWidgetItem,
                             QTabWidget,
                             QTextEdit,
                             QVBoxLayout,
                             QWidget)

import custom_widgets
import picture_viewer
import tab_model_index
import tab_qsql_database

import tab_qsql_table_model
import parameters
#import ex_helpers
import gui_qt_ext
#import ia_qt
import utils_for_tabs as uft
import wat
import wat_inspector

#wat_inspector    = wat.Wat( "joe")

# ---- end imports
what   = Qt.AlignCenter   # valid aligment perhaps to addWidget   layout.addWidget
#	addWidget(QWidget *widget, int stretch = 0, Qt::Alignment alignment = Qt::Alignment())


INDENT        = uft.INDENT
BEGIN_MARK_1  = uft.BEGIN_MARK_1
BEGIN_MARK_2  = uft.BEGIN_MARK_2




print_func_header  = uft.print_func_header




# --------------------------------
def set_groupbox_style( groupbox ):
    """ """
    groupbox.setStyleSheet("""
        QGroupBox {
            border: 2px solid blue;
            border-radius: 10px;
            margin-top: 15px;
        }

        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 3px;
            background-color: white;
        }
    """)


def print_func_header( what ):
        """
        what is says
        """
        #what    = "fix_me"
        print( f"{BEGIN_MARK_1}{what}{BEGIN_MARK_2}")



#  --------
class TemplateCopyMeWidgetTab( QWidget ) :
    def __init__(self):
        """

        """
        super().__init__()
        self._build_gui()


    def _build_gui(self,   ):
        """
        all build on a local QWidget
        count : const int
        currentData : const QVariant
        currentIndex : int
        """

        tab_page      = self

        layout        = QVBoxLayout( tab_page )
        button_layout = QHBoxLayout( )


        # ---- QGroupBox
        #groupbox   = QGroupBox()
        # groupbox   = QGroupBox( "QGroupBox 1" )   # version with title
        # layout.addWidget( groupbox )
        # layout_b     = QHBoxLayout( groupbox  )
        # self.build_gui_in_groupbox( layout_b )

        # ---- buttons
        layout.addLayout ( button_layout )

        label       = "mutate"
        widget      = QPushButton( label )
        #widget.clicked.connect( self.combo_reload )
        button_layout.addWidget( widget )

        # ----
        label       = "inspect"
        widget      = QPushButton( label )
        widget.clicked.connect( self.inspect )
        button_layout.addWidget( widget )


    # --------------------------
    def inspect( self, arg  ):
        """
        count : const int
        currentData : const QVariant
        currentIndex : int
        currentText : QString
        duplicatesEnabled : bool
        editable : bool
        """
        print( f"inspect { '' }  --------",   )

        # widget         = self.combo_1

        # info           = widget.count()
        # msg            = f".count() {info}"
        # print( msg )

        # info           = widget.currentData()    # seem to always get None
        # msg            = f".currentData() {info}"
        # print( msg )

        # # qt5 not working for me
        # # info           = widget.editable
        # # msg            = f".editable {info}"
        # # print( msg )



        # info           = widget.placeholderText()
        # msg            = f".placeholderText() {info}"
        # print( msg )

        # self.show_combo_values()   # move this code here


        # print( f"inspect end { '' } --------",   )

#  --------
class CustomWidgetTab( QWidget ) :
    def __init__(self):
        """

        """
        super().__init__()
        self._build_gui()


    def _build_gui(self,   ):
        """
        all build on a local QWidget
        count : const int
        currentData : const QVariant
        currentIndex : int

        edits

        criteria

        """
        tab_page        = self
        lbl_stretch     = 0
        widget_stretch  = 3

        self.lbl_stretch     = lbl_stretch
        self.widget_stretch  = widget_stretch


        layout              = QVBoxLayout( tab_page )

        groupbox_criteria   = QGroupBox( "Criteria" )
        set_groupbox_style( groupbox_criteria )

        groupbox_edits      = QGroupBox( "Edits" )
        set_groupbox_style( groupbox_edits )

        button_layout       = QHBoxLayout( )

        layout.addWidget( groupbox_edits )
        g_layout            = QVBoxLayout( groupbox_edits  )

        # # ---- edits --------------------------------
        # layout.addWidget( groupbox_edits )
        # g_layout            = QVBoxLayout( groupbox_edits  )
        self._build_gui_in_gb_edit( g_layout )

        # ---- criteria --------------------------------
        layout.addWidget( groupbox_criteria )
        g_layout            = QVBoxLayout( groupbox_criteria  )
        self._build_gui_in_gb_criteria( g_layout )


        # ---- buttons
        layout.addLayout ( button_layout )

        label       = "mutate_1\n"
        widget      = QPushButton( label )
        widget.clicked.connect( self.mutate_1 )
        button_layout.addWidget( widget )

        label       = "mutate_2\n"
        widget      = QPushButton( label )
        widget.clicked.connect( self.mutate_2 )
        button_layout.addWidget( widget )

        # ---- raise_except
        widget = QPushButton("raise\n_except")
        # widget.clicked.connect(lambda: self.print_message(widget.text()))
        a_widget        = widget
        widget.clicked.connect( lambda: self.raise_except( ) )
        button_layout.addWidget( widget )

        label       = "default\n"
        widget      = QPushButton( label )
        widget.clicked.connect( self.default )
        button_layout.addWidget( widget )

        # # ----
        # label       = "inspect"
        # widget      = QPushButton( label )
        # widget.clicked.connect( self.inspect )
        # button_layout.addWidget( widget )

        # # ----
        # label       = "wat_inspect"
        # widget      = QPushButton( label )
        # widget.clicked.connect( self.wat_inspect )
        # button_layout.addWidget( widget )

        # ---- PB inspect
        widget              = QPushButton("inspect\n")
        connect_to        = self.inspect
        widget.clicked.connect( connect_to )
        button_layout.addWidget( widget )

        # ---- PB breakpoint
        widget              = QPushButton("breakpoint\n ")
        connect_to          = self.breakpoint
        widget.clicked.connect( connect_to )
        button_layout.addWidget( widget )


    # ------------------------
    def _build_gui_in_gb_edit(self, layout  ):
        """
        build some of the gui in a groupbox
        """
        lbl_stretch         = self.lbl_stretch
        widget_stretch      = self.widget_stretch

        # ---- CQLineEdit
        b_layout        = QHBoxLayout( )
        layout.addLayout( b_layout )

        widget            = QLabel( "CQLineEdit_1")
        b_layout.addWidget( widget,  stretch = lbl_stretch )

        widget            = custom_widgets.CQLineEdit(  self, field_name    = "CQLineEdit_1", )
        self.line_edit_1_widget = widget
        b_layout.addWidget( widget,  stretch = widget_stretch )

        # ---- CQLineEdit_2
        b_layout        = QHBoxLayout( )
        layout.addLayout( b_layout )

        widget            = QLabel( "CQLineEdit_2")
        b_layout.addWidget( widget,  stretch = lbl_stretch )

        widget            = custom_widgets.CQLineEdit(  self, field_name    = "CQLineEdit_2", )
        self.line_edit_2_widget = widget
        b_layout.addWidget( widget,  stretch = widget_stretch )


        # ---- CQDateEdit_1
        b_layout        = QHBoxLayout( )
        layout.addLayout( b_layout )

        widget            = QLabel( "CQDateEdit_1")
        b_layout.addWidget( widget,  stretch = lbl_stretch )

        widget              = custom_widgets.CQDateEdit(  self, field_name    = "a field name", )
        self.date_edit_1_widget = widget
        b_layout.addWidget( widget,  stretch = widget_stretch )

        # ---- CQDateEdit_n
        b_layout        = QHBoxLayout( )
        layout.addLayout( b_layout )

        widget            = QLabel( "CQDateEdit_n:")
        b_layout.addWidget( widget,  stretch = lbl_stretch )

        widget            = custom_widgets.CQDateEdit(  self, field_name    = "a field name", )
        self.date_edit_2_widget = widget
        b_layout.addWidget( widget,  stretch = self.widget_stretch )


    def _build_gui_in_gb_criteria(self, layout  ):
        """
        build some of the gui in a groupbox
        """
        lbl_stretch        = self.lbl_stretch
        widget_stretch     = self.widget_stretch

        # ---- CQLineEditCriteria_1
        b_layout        = QHBoxLayout( )
        layout.addLayout( b_layout )

        widget            = QLabel( "CQLineEditCriteria_1 :")
        b_layout.addWidget( widget,  stretch = lbl_stretch )

        widget            = custom_widgets.CQLineEditCriteria(  self,   )
        self.line_edit_criteria_1_widget = widget
        b_layout.addWidget( widget,  stretch = widget_stretch )

        # ---- CQDateCriteria_1
        b_layout        = QHBoxLayout( )
        layout.addLayout( b_layout )

        widget            = QLabel( "CQDateCriteria_1:")
        b_layout.addWidget( widget,  stretch = self.lbl_stretch )

        widget            = custom_widgets.CQDateCriteria(    )
        self.date_critera_1_widget = widget
        # widget           = widget.container
        b_layout.addWidget( widget,  stretch = self.widget_stretch )

        widget            = QLabel( "CQDateCriteria_2:")
        b_layout.addWidget( widget,  stretch = self.lbl_stretch )

        widget            = custom_widgets.CQDateCriteria(    )
        self.date_critera_2_widget = widget
        # widget           = widget.container
        b_layout.addWidget( widget,  stretch = self.widget_stretch )


    # # --------------------------
    # def wat_inspect( self, arg  ):
    #     """
    #     # wat_inspector.go( self, locals() )
    #     can i give a list of objects like locals?
    #     """
    #     date_criteria_1_widget  =         self.date_criteria_1_widget
    #     date_criteria_2_widget  =         self.date_criteria_2_widget

    #     wat_inspector.go( self, locals() )

    # --------------------------
    def examine( self, arg  ):
        """
        count : const int
        currentData : const QVariant
        currentIndex : int
        currentText : QString
        duplicatesEnabled : bool
        editable : bool        widget                          = self.make_criteria_date_widget()
        """
        """
        !!What it says
        """
        print_func_header( "examine" )

        a_timestamp    = self.date_edit_2_widget.get_data_as_timestamp()


        print( f"inspect date_edit_2_widget.get_data_as_timestamp() { a_timestamp = }",   )


        # widget         = self.combo_1

        # # info           = widget.count()
        # msg            = f".criteria widget {a_timestamp = }"
        # print( msg )

        # info           = widget.currentData()    # seem to always get None
        # msg            = f".currentData() {info}"
        # print( msg )
        print( "line edit ---------------")
        widget    = self.line_edit_1_widget
        msg       = f"{widget.data_value = }"
        print( msg )

        widget.data   = "changed data with @property.setter"

        widget    = self.line_edit_1_widget
        msg       = f"{widget.data_value = }"
        print( msg )

        # ---- edits
        msg       = "\nFor the edit widgets:"
        msg       = f"{self.date_edit_1_widget.data_value = }"
        print( msg )
        msg       = f"{self.date_edit_2_widget = }"
        print( msg )
        msg       = f"{ self.line_edit_1_widget = }"
        print( msg )
        msg       = f"{self.line_edit_2_widget = }"
        print( msg )



        print( f"inspect end { '' } --------",  )

    # --------------------------
    def default( self, arg  ):
        """
        !!What it says
        """
        print_func_header( "default" )


        print( f"\n\n\ndefaultt { '' }  --------",   )

        print( "self.line_edit_1_widget" )
        widget       =   self.line_edit_1_widget
        widget.set_data_default()

        widget       =   self.line_edit_2_widget
        widget.set_data_default()

        print( "self.line_edit_1_widget" )
        print( "self.line_edit_1_widget" )
        widget       =    self.date_edit_1_widget
        widget.set_data_default()


        print( "self.line_edit_2_widget" )
        widget       =    self.date_edit_2_widget
        widget.set_data_default()


        print( "self.date_criteria_1_widget" )
        widget       =   self.date_critera_1_widget
        widget.set_date_default()

    # --------------------------
    def mutate_1( self, arg  ):
        """
        !!What it says
        """
        print_func_header( "mutate_1" )

        self.date_critera_widget.set_date_default()
        self.date_edit_widget.set_data_default()

    # --------------------------
    def mutate_2( self, arg  ):
        """
        !!What it says
        """
        print_func_header( "mutate_2" )
        what    = "add_record -- tbd"
        print( f"{BEGIN_MARK_1}{what}{BEGIN_MARK_2}")
        print( f"\n\n\ninspect { '' }  --------",   )
        self.date_critera_widget.set_date_default()
        self.date_edit_widget.set_data_default()

    # --------------------------
    def raise_except( self,   ):
        """

        """
        try:
            raise custom_widgets.ValidationIssue( "why o why", self )


        except custom_widgets.ValidationIssue  as an_except:
            #an_except.why, an_except.this_control
            # msg     = f"a_except         >>{an_except}<<  type  >>{type( an_except)}<<"
            # print( msg )

            # msg     = f"an_except.args   >>{an_except.args}<<"
            # print( msg )

            # s_trace = traceback.format_exc()
            # msg     = f"format-exc       >>{s_trace}<<"
            # print( msg )
            # AppGlobal.logger.error( msg )   #    AppGlobal.logger.debug( msg )
            msg     = an_except.args[0]
            print( f"{msg = }" )
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Input Issue")
            msg_box.setText( msg )

            # Adding buttons
            choice_a = msg_box.addButton( "Ok", QMessageBox.ActionRole)
            # choice_b = msg_box.addButton( "Choice B", QMessageBox.ActionRole)

            # Set the dialog to be modal (blocks interaction with other windows)
            msg_box.setModal( True )

            # Execute the message box and wait for a response
            msg_box.exec_()

    # ------------------------
    def inspect(self):
        """
        the usual
        """
        print_func_header( "inspect" )

        # make some locals for inspection
        my_tab_widget = self
        parent_window = self.parent( ).parent( ).parent().parent()

        self_line_edit_1_widget   = self.line_edit_1_widget
        self_line_edit_1_widget = self.line_edit_1_widget
        self_date_edit_1_widget = self.date_edit_1_widget
        self_date_edit_2_widget = self.date_edit_2_widget
        self_line_edit_criteria_1_widget = self.line_edit_criteria_1_widget

        wat_inspector.go(
             msg            = "inspect !! more locals would be nice ",
             # inspect_me     = self.people_model,
             a_locals       = locals(),
             a_globals      = globals(), )

    # ------------------------
    def breakpoint(self):
        """
        keep this in each object so user breaks into that object
        """
        print_func_header( "breakpoint" )
        breakpoint()

#  --------
class PictureViewerPlusTab( QWidget ) :

# ---- main window ------------------------------------------
#  --------
class CustomWidgetExamples__now_in_qt_by_example( QMainWindow ):
    def __init__(self):
        """
        window with many widgets, placed with regular layouts

        refactoring from earlier code, not yet done
        spinbox here but not in visible code also QTextEdit....
        stacked..... missing
        """
        super().__init__()


        my_parameters   = parameters.Parameters()
        self.parameters = my_parameters
        uft.parameters  = my_parameters
        uft.main_window = self



        qt_xpos     = 10
        qt_ypos     = 10
        qt_width    = 3000
        qt_height   = 600
        self.tab_help_dict   = { }
        self.setGeometry(  qt_xpos,
                           qt_ypos ,
                           qt_width,
                           qt_height  )

        # !! still needs work
        global DB_FILE

        DB_FILE             = my_parameters.db_file_name
        uft.DB_FILE         = DB_FILE
        uft.TEXT_EDITOR     = my_parameters.text_editor


        # self._build_menu()
        self.doc_dir        = "./docs/"
        self.create_db()


        self.build_gui()


    def build_gui( self ):
        """
        main gui build method -- for some sub layout use other methods
        """
        self.setWindowTitle( "CustomWidgetExamples" )
        #self.setIcon( QMessageBox.Warning) #
        #self.setWindowIcon( QtGui.QIcon('clipboard_b_red_gimp.ico') )
        self.setWindowIcon( QtGui.QIcon( './designer.png' ) )  # cannot get this to work


        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        central_widget_layout  =  QVBoxLayout( central_widget )

        # --- out main layout
        layout      = QVBoxLayout(   )
        central_widget_layout.addLayout( layout )

        self.build_menu( )

        # ---- Create tabs
        self.tab_widget = QTabWidget()   # really the folder for the tabs
                                         # tabs themselves are just Widgets
        # Set custom height for the tabs
        self.tab_widget.setStyleSheet("QTabBar::tab { height: 40px; }") # 40 enough for 2 lines ??
        layout.addWidget( self.tab_widget   )

        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        layout.addWidget( self.tab_widget   ) # what do the numbers mean

        # # ----
        # tab      = uft.SeperatorTab()
        # title    = "Tab\nDraft>>"
        # self.tab_widget.addTab( tab, title  )
        tab      = tab_qsql_database.QSqlDatabaseTab()
        title    = "QSqlDatabase\n&QSqlQuery"
        self.tab_widget.addTab( tab, title  )
        self.tab_help_dict[ title ] = "qsql_database_tab.txt"

        # # ---- QSqlTableModelTab
        # tab      = tab_qsql_table_model.QSqlTableModelTab()
        # title    = "QSqlTableModel\n"
        # self.tab_widget.addTab( tab, title  )
        # self.tab_help_dict[ title ] = "qsql_table_model_tab.txt"



        # title    = "QQComboBox\nWidgetTab"
        # tab      = QComboBoxWidgetTab()
        # self.tab_widget.addTab( tab, title  )
        # self.tab_help_dict[ title ] = "combo_box_widdget_tab.txt"

        title    = "CQTextEdit\nWidgetTab"
        tab      = CQTextEditWidgetTab()
        self.tab_widget.addTab( tab, title  )
        self.tab_help_dict[ title ] = "text_edit_widget_tab.txt"

        # # ----
        # tab      = uft.SeperatorTab()
        # title    = "Tab\nDraft>>"
        # self.tab_widget.addTab( tab, title  )

        # ----"Custom\nWidgetTab"
        title    = "Custom\nWidget"
        tab      = CustomWidgetTab()
        self.tab_widget.addTab( tab, title  )
        self.tab_help_dict[ title ] = "custom_widget_tab.txt"

        # ----"Custom\nWidgetTab"
        title    = "Model\nIndex"
        tab      = tab_model_index.Model_Index_Tab()
        self.tab_widget.addTab( tab, title  )
        self.tab_help_dict[ title ] = "model_index_tab.txt"


        # title    = "QGridLayout\nWidgetTab"
        # tab      = GridLayoutWidgetTab()
        # self.tab_widget.addTab( tab, title  )
        # self.tab_help_dict[ title ] = "layout_Widget_tab.txt"

        # title    = "QList\nWidgetTab"
        # tab      = QListWidgetTab()
        # self.tab_widget.addTab( tab, title  )
        # self.tab_help_dict[ title ] = "list_widdget_tab.txt"



        title    = "PictureViewer\nTab"
        tab      = PictureViewerTab()
        self.tab_widget.addTab( tab, title  )
        self.tab_help_dict[ title ] = "picture_viewer_tab.txt"

        title    = "PictureViewerPlus\nTab"
        tab      = PictureViewerPlusTab()
        self.tab_widget.addTab( tab, title  )
        self.tab_help_dict[ title ] = "picture_viewer_plus_tab.txt"

        title    = "TemplateCopy\nMeWidgetTab"
        tab      = TemplateCopyMeWidgetTab()
        self.tab_widget.addTab( tab, title  )
        self.tab_help_dict[ title ] = "template_copy_me_tab.txt"

        # tab      = self.create_tab_with_buttons( ["Button 1", "Button 2", "Button 3"])
        # self.tab_widget.addTab( tab, "Tab 1"  )


    # ------------------------------------
    def build_menu( self,  ):
        """
        what it says read:

        """
        menubar         = self.menuBar()
        self.menubar    = menubar

        # a_menu.addSeparator()

        # ---- Help
        menu_help       = menubar.addMenu( "Help" )

        action          = QAction( "General Help...", self )
        connect_to      = self.open_general_help
        action.triggered.connect( connect_to )
        menu_help.addAction( action )

        action          = QAction( "Current Tab Help...", self )
        connect_to      = self.open_tab_help
        action.triggered.connect( connect_to )
        menu_help.addAction( action )

    #-------
    def create_db( self,   ):
        """
        what it says read:
        """
        self.sample_db          =  tab_qsql_database.SampleDB()

    #----------------------------
    def not_implemented( self,   ):
        """
        what it says read:
        """
        QMessageBox.information(self, "Not Implemented", "Working on this...")

    #-------
    def open_general_help( self,   ):
        """
        what it says read:

        """
        doc_name            =   "qt_widgets_help.txt"
        ex_editor          = r"xed"
        proc               = subprocess.Popen( [ ex_editor, doc_name ] )

    #-------
    def open_tab_help( self,   ):
        """
        what it says read:
            still needs work
        """
        tab_title    = self.tab_widget.tabText( self.tab_widget.currentIndex())
        print( f"{tab_title = }")


        doc_name  = self.tab_help_dict.get( tab_title, "no_specific_help.txt")
        print( f"{doc_name = }")
        ex_editor          = r"xed"

        proc               = subprocess.Popen( [ ex_editor, doc_name ] )
        #AppGlobal.os_open_txt_file( doc_name  )


    #----------------------------
    def not_implemented( self,   ):
        """
        what it says read:
        """
        QMessageBox.information(self, "Not Implemented", "Working on this...")

    #----------------------------
    def on_tab_changed(self, index):
        """
        what it says, read it
        """
        print(f"on_tab_changed  {index = }")
        self.tab_page_info()

    def tab_page_info( self ):
        """
        what it says, read it
        """
        nb    = self.tab_widget
        print(f"nb.select()  >>{nb.currentIndex() = }<<")
        print(f'>>{nb.tabText(nb.currentIndex()) = }<<')
        # print(f'{ nb.index("current" ) = }' )

    #-----------------------------------------------
    def build_list_widget_tabxxx(self,   ):
        """

        """
        tab_page      = QWidget()
        layout        = QVBoxLayout( tab_page )

        widget        = QListWidget(    )
        widget.setGeometry( 50, 50, 200, 200 )
        layout.addWidget( widget )

        #widget.itemClicked.connect( self.activate_clicked_command )

        values    =  [ "one", "two"]
        for value in values:
            item = QListWidgetItem( value )
            widget.addItem( item )

        widget.clear()

        values    =  [ "oneish", "twoish"]
        for value in values:
            item = QListWidgetItem( value )
            widget.addItem( item )
            index_to_select = 2

            widget.setCurrentRow(index_to_select)

        ia_qt.q_list( widget )

        return tab_page



    # ---- build_layout_tab -----------------------------------------------------
    # #-----------------------------------------------
    # def build_layout_tabxxxx(self,   ):
    #     """
    #     build a tab to show off layout widgets
    #     """
    #     tab_page      = QWidget()
    #     layout        = QVBoxLayout( tab_page )

    #     layout_a     = QHBoxLayout(    )
    #     layout.addLayout( layout_a )
    #     self.layout_tab_layout_a   = layout_a

    #     self.widget_ix              = 22
    #     widget                      = QPushButton( f"Button   {self.widget_ix}")
    #     layout_a.addWidget( widget )
    #     self.layout_tab_button_1    = widget
    #     self.widget_temp            = widget

    #     layout_b     = QHBoxLayout(    )
    #     layout.addLayout( layout_b )

    #     widget = QPushButton("show_values")
    #     layout_b.addWidget( widget )

    #     widget = QPushButton("remove_add_widget")
    #     layout_b.addWidget( widget )
    #     widget.clicked.connect( lambda: self.remove_add_widget_layout_tab() )

    #     widget = QPushButton("replace_widget")
    #     layout_b.addWidget( widget )
    #     widget.clicked.connect( lambda: self.replace_widget_layout_tab() )
    #    # --------
    #     widget = QPushButton( "minimize" )  # showminimized iconify
    #     layout_b.addWidget( widget )
    #     widget.clicked.connect(lambda: self.iconify( ))

    #     return tab_page

    # #-----------------------------------------------
    # def remove_add_widget_layout_tab( self, ):
    #     """
    #     deletes and adds but position may change
    #     """
    #     print( "replace widget is better may need delete later ")
    #     self.widget_ix             += 1
    #     widget = QPushButton("Button + str(self.widget_ix)")

    #     #layout_b.addWidget( widget )

    #     self.layout_tab_layout_a.removeWidget( self.widget_temp  )
    #     self.widget_temp   = widget
    #     # button1.deleteLater()  # Optionally delete the old widget
    #     self.layout_tab_layout_a.addWidget( widget )

    # #-----------------------------------------------
    # def replace_widget_layout_tab( self, ):
    #     """
    #     deletes and adds but position may change
    #     """
    #     print( "replace_widget_layout_tab")
    #     widget                      = self.widget_temp
    #     self.widget_ix             += 1
    #     widget_new                  = QPushButton( f"Button   {self.widget_ix}")
    #     #self.keep_me                = widget_new
    #     # stop from delete

    #     self.replace_layout_widget( self.layout_tab_layout_a, widget, widget_new )
    #     self.widget_temp            = widget_new

    #     # print( f"{widget}")
    #     # print( f"{widget_new}")

    # def replace_layout_widget( self, layout, widget, widget_new ):
    #     """
    #     function should work copy and paste
    #     will be a problem if widget is not found in layout

    #     Args:
    #         layout (TYPE): DESCRIPTION.
    #         widget (TYPE): DESCRIPTION.

    #     """
    #     # print( f"{widget}")
    #     # print( f"{widget_new}")
    #     # Find the index of the existing widget
    #     index               = layout.indexOf( widget )
    #     print( f"widget at {index}")
    #     # Remove the old widget
    #     widget_to_remove    = layout.takeAt(index).widget()

    #     # see if this is causing a problem
    #     if widget_to_remove:
    #         widget_to_remove.deleteLater()

    #     # Insert the new widget at the same index
    #     layout.insertWidget( index, widget_new )



    # def table_widget_no_edit(self,  ):
    #     """
    #     from chat

    #     """
    #     table = self.table
    #     for row in range(table.rowCount()):
    #         for column in range(table.columnCount()):
    #             item = table.item(row, column)
    #             if item is not None:
    #                 item.setFlags(item.flags() & ~Qt.ItemIsEditable)



    # def table_widget_add_row(self, data=None):
    #     """
    #     Method to add a row with optional data

    #     """
    #     row_position = self.table.rowCount()
    #     self.table.insertRow(row_position)

    #     # If data is provided, set it in the cells
    #     if data:
    #         for i, item in enumerate(data):
    #             self.table.setItem(row_position, i, QTableWidgetItem(item))

    # # Method to delete the selected row
    # def table_widget_delete_row(self):
    #     selected_row = self.table.currentRow()
    #     if selected_row >= 0:
    #         self.table.removeRow(selected_row)

    # # Method to edit a particular cell
    # def table_widget_edit_cell(self, row, column, new_value):
    #     self.table.setItem(row, column, QTableWidgetItem(new_value))

    # # Example method to add an item to a particular cell
    # def table_widget_add_item(self, row, column, value):
    #     self.table.setItem(row, column, QTableWidgetItem(value))

    # ---- button tab ------------------------------------------------
    def build_button_tab(self,   ):
        """
        all build on a local QWidget
        count : const int
        currentData : const QVariant
        currentIndex : int
        currentText : QString
        duplicatesEnabled : bool
        editable : bool
        """
        1/0
        tab_page      = QWidget()

        layout        = QVBoxLayout( tab_page )

        # ---- combo_1
        widget        = QComboBox()
        self.combo_1  = widget

        widget.addItem('Zero')
        widget.addItem('One')
        widget.addItem('Two')
        widget.addItem('Three')
        widget.addItem('Four')

        widget.currentIndexChanged.connect( self.conbo_currentIndexChanged )
        widget.currentTextChanged.connect(  self.combo_currentTextChanged  )

        #widget.currentTextChanged.connect(self.current_text_changed)
        widget.setMinimumWidth( 200 )

        layout.addWidget( widget )

        # ---- combo_2
        widget        = QComboBox()
        self.combo_2  = widget

        widget.addItem('Zero')
        widget.addItem('One')
        widget.addItem('Two')
        widget.addItem('Three')
        widget.addItem('Four')
        #widget.editable( True )
        widget.setEditable( True )

        widget.currentIndexChanged.connect( self.conbo_currentIndexChanged )
        widget.currentTextChanged.connect(  self.combo_currentTextChanged  )

        #widget.currentTextChanged.connect(self.current_text_changed)
        widget.setMinimumWidth( 200 )

        layout.addWidget( widget )

        # ---- bottoms
        label       = "combo\n_reload"
        widget = QPushButton( label )
        widget.clicked.connect( self.combo_reload )

        layout.addWidget( widget )

        # ----
        label       = "combo\n_info"
        widget = QPushButton( label )
        widget.clicked.connect( self.combo_info )

        layout.addWidget( widget )

        return tab_page


    # --------
    def get_layout_widgets(self, layout):
        """

        Args:
            layout (TYPE): DESCRIPTION.

        Returns:
            None.

        """
        widgets = []
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item.widget():
                widgets.append(item.widget())
            elif item.layout():
                # recursion
                widgets.extend( self.get_layout_widgets( item.layout() ) )
        # return widgets
        for widget in widgets:
            print(type(widget).__name__)

    # --------
    def current_text_changed(self, s):
        """

        """
        print("Current text: ", s)

    # --------
    def on_rb_clicked(self):
        """
        """
        radioButton = self.sender()
        if radioButton.isChecked():
            print( "\nCountry is %s" % (radioButton.country))
            #print(   "Id is       %s" % (radioButton.i ))
            print( f"self.country_group.id( radioButton ) {self.country_group.id( radioButton )}")
        print(f"country_group.checkedButton() >{self.country_group.checkedButton()}<" )
        checked_button    = self.country_group.checkedButton()
        print(f"checked_button.text(){checked_button.text()}" )
        # next seem to be assigned negative numbers ...
        print(f"country_group.checkedId() >{self.country_group.checkedId()}<" )
        buttons    = self.country_group.buttons()
        for i_button in buttons:
            print( f"{i_button}")

    # --------
    def show_values(self):
        """
        show all the values from widgets
        """
        print( "get and show values of widgets")

        line_edit_value  = self.line_edit_ex_1.text()
        cbox_value       = str( self.cbox_ex_1.isChecked())
        # need to save  list and loop thru    radioButton.isChecked() --- or ask the group
        cb1_text         = self.combobox_ex_1.currentText()

        msg   = ( f"\nline_edit_value    = {line_edit_value}"
                  f"\ncbox_value         = {cbox_value}"
                  f"\ncb1_text           = {cb1_text}"
        )
        print( msg )
        # self.message_widget.display_string( msg, )

    # --------
    def print_message(self, text):
        print("Button clicked:", text)

     # --------
    def make_partial_widget_clicked( self, widget):
        """
        """
        from functools import partial
        a_partial_foo       = partial( self.widget_clicked,  widget = widget )  # will set first arg    # --------

        return a_partial_foo

    # --------
    def widget_clicked( self, widget):
        """
        alternative button clicked function
        seems like will not work with lambda instead use make_partial_widget_clicked
        """
        print( "widget_clicked" )
        print( f"widget >{widget}<")
        print( f"widget.text() >{widget.text()}<")

    # ----
    def iconify( self ):
        """
        what is says, same as minimize
        """
        self.showMinimized()   # for minimizing your window

    # --------
    def close_event(self, event):
        """
         ask if user wishes to close
        """
        if self.popup_question():
            print("The program was shut down.")
            event.accept()
        else:
            print("not exiting")
            event.ignore()

    # --------
    def popup_question(self):
        """
        Generate a popup that requests if you want to do something or not.
        here exit the application --- see close_event
        """
        msgbox =  QMessageBox()
        msgbox.setWindowTitle("Whatever title you want to add.")
        msgbox.setIcon( QMessageBox.Warning)
        msgbox.setText("Do you want to quit WidgetExample?")
        botonyes =  QPushButton("Yes")
        msgbox.addButton(botonyes, QMessageBox.YesRole)
        botonno =  QPushButton("No")
        msgbox.addButton(botonno, QMessageBox.NoRole)
        msgbox.exec_()
        if msgbox.clickedButton() == botonno:
            return False
        else:
            return True

# --------
def main():
    ex_name  = "ex_widget_example"
    # print( f"{ex_helpers.begin_example( ex_name )}"
    #         "\n    window with a lot of the basic widgets  "
    #       )

        # wat_inspector.go( self, locals() )

    app             = QApplication(sys.argv)
    #dialog          = wat_inspector.DisplayWat( app )  # Create an instance of your custom QDialog
    a_wat_inspector  = wat_inspector.WatInspector( app ) # Create an instance of your custom QDialog

    # self.q_app.exec_()   # perhaps move to run method

    window  = CustomWidgetExamples()
    window.show()
    #sys.exit(
    app.exec()
    # ex_helpers.end_example( ex_name )
    sys.exit( 0 )

main()





# ---- eof ----------------------------------

