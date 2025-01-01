#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 08:39:04 2024

@author: russ
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 08:28:36 2024

stuff_document_edit.EditStuffEvents( model, keygen, index = None, parent = None)



"""

# --------------------
if __name__ == "__main__":
    import main
    main.main()
# --------------------



# import ia_qt


import sys

from app_global import AppGlobal
from PyQt5.QtCore import Qt
from PyQt5.QtSql import (QSqlDatabase,
                         QSqlDriver,
                         QSqlQuery,
                         QSqlRecord,
                         QSqlRelation,
                         QSqlRelationalDelegate,
                         QSqlRelationalTableModel,
                         QSqlTableModel)
# ----QtWidgets layouts
from PyQt5.QtWidgets import (QApplication,
                             QComboBox,
                             QDialog,
                             QFormLayout,
                             QGridLayout,
                             QHBoxLayout,
                             QLabel,
                             QLineEdit,
                             QMainWindow,
                             QMessageBox,
                             QPushButton,
                             QTableView,
                             QVBoxLayout,
                             QWidget)

# ---- local imports
# import  tracked_qsql_relational_table_model



# ---- end imports



style       = "photo"  # or seq >
style       = "seq"  # or seq >

#------------
relation    = "none"    # one  two    # related columns
relation    = "one"    # one  two    # related columns
relation    = "two"    # one  two    # related columns



class MdiInfo( QDialog ):
    """
    what it says, read?


    """
    # ------------------------------------------
    def __init__(self,   parent_window  = None,  topics  = None   ) :
        """
        Args:


        Returns:
            None.

        """
        super().__init__( parent_window )

        self.parent_window  = parent_window
        self.topics         = topics
        msg    = "Mdi Info"

        self.setWindowTitle( msg  )

        self._build_gui()

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says, read?
        """

        #self.layout                     = QFormLayout()
        self.layout            = QVBoxLayout( self )
        #self.setLayout( self.layout )
        button_layout          = QHBoxLayout( self )
        # button_layout           =  QHBoxLayout()
        # self.layout.addChildLayout( button_layout )
        # button_layout           =  self.layout

        form_layout                     = QFormLayout()
        self.layout.addLayout( form_layout )
        self.layout.addLayout( button_layout )

        # ---- form
        a_widget                        = QLineEdit()
        self.id_field                   = a_widget
        self.id_ix                      = 0
        form_layout.addRow( "id",         a_widget )

        a_widget                        = QLineEdit()
        self.id_field                   = a_widget
        self.id_ix                      = 0
        form_layout.addRow( "id",         a_widget )

        for i_topic in self.topics.topic_list:
            print( i_topic )
            a_widget                        = QLineEdit()
            a_widget.setText( str(i_topic ) )
            self.id_field                   = a_widget
            self.id_ix                      = 0
            form_layout.addRow( "topic",         a_widget )

        # ----
        a_widget                  = QPushButton("Ok")
        self.cancel_button        = a_widget
        a_widget.clicked.connect(  self.accept )
        button_layout.addWidget( a_widget )



    # ---- model to fields var ------------------------------------------
    def model_to_fields( self ):
        """
        what it says, read?
        rename to model_to_fields
        """
        #self.model_to_fields_seq()
        self.model_to_fields_2()


    # ------------------------------------------
    def model_to_fields_1( self ):
        """
        what it says, read?
        rename to model_to_fields
        """
        model               = self.model

        ix_col              = -1

        # ix_col              += 1
        # data                = model.data( model.index(self.index.row(), ix_col) )
        # self.photo_photo_fn_field.setText( data )

        # ix_col              += 1
        # data                = model.data( model.index(self.index.row(), ix_col) )
        # self.seq_no_field.setText( str( data ) )

        ix_col              += 1
        data                = model.data( model.index( self.index.row(), ix_col) )
        self.id_field.setText( str( data ) )

        ix_col              += 1
        data                = model.data( model.index( self.index.row(), ix_col) )
        self.photoshow_id_field.setText( str( data ) )

    # ------------------------------------------
    def model_to_fields_2( self ):
        """
        what it says, read?

        """
        model               = self.model

        ix_col              = -1

        # ---- code_gen: model_to_fields  -- begin table entries

        # ---- id
        ix_col              += 1
        data                = model.data( model.index( self.index.row(), ix_col) )
        self.id_field.setText( str( data ) )

        # ---- stuff_id
        ix_col              += 1
        data                = model.data( model.index( self.index.row(), ix_col) )
        self.stuff_id_field.setText( str( data ) )

        # ---- cmnt
        ix_col              += 1
        data                = model.data( model.index( self.index.row(), ix_col) )
        self.cmnt_field.setText( str( data ) )

        # ---- event_ts
        ix_col              += 1
        data                = model.data( model.index( self.index.row(), ix_col) )
        self.event_ts_field.setText( str( data ) )

        # ---- dlr
        ix_col              += 1
        data                = model.data( model.index( self.index.row(), ix_col) )
        self.dlr_field.setText( str( data ) )

        # ---- type
        ix_col              += 1
        data                = model.data( model.index( self.index.row(), ix_col) )
        self.type_field.setText( str( data ) )

        # ---- no_comma
        ix_col              += 1
        data                = model.data( model.index( self.index.row(), ix_col) )
        self.no_comma_field.setText( str( data ) )

        # ---- code_gen: model_to_fields  -- end table entries



