#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 11:36:16 2024

@author: russ
"""
# ----------------------------------------
class PhotoshowDetailListTab_pre_crud( QWidget  ):
    """
    tab in a tab, this is a list of the photos
    in the show
_   from detail tab   build_tab_photos



    """
    def __init__(self, parent_window ):
        """
        so i can have 2 lists, one of adds, one of deletes each can
        be a dict of info.
        manually put the data in the relational view and
        on submit generate queries for each

        the dict would be different for adds and deletes
        deletes only needs the photoshow_photo.id
        the add needs to display so needs some photo information:
        the dict would have the photo.id name and file_name for each photo and

        """
        super().__init__()
        self.parent_window   = parent_window
        self.sub_window      = parent_window.parent_window   # two levels up

        self.photo_tab       =  self.sub_window.photo_tab
        self.list_ix         = -1  # should track selected an item in detail
        self.list_table_name = "photoshow_photo"

        # # do we hanv this is whole table   no implied
        # self.sql_update = """
        #     SELECT
        #       photoshow_photo.id
        #       photoshow_photo.seq_no,
        #       photoshow_photo.photo_id
        #       photoshow_photo.photoshow_id

        #     FROM   photoshow_photo
        #     WHERE  photoshow_photo.photoshow_id.  = :id;
        # """
        AppGlobal.add_photo_target   = self
        self.db     = AppGlobal.qsql_db_access.db

        self.setup_models(  )

        self._build_gui()
        # self.select_by_id( id = 5529  )   # model   = self.setup_model( id = 5529 )

    # ------------------------------------------
    def _build_gui( self,  ):
        """
        what it says, read

        """
        page            = self
        tab             = page


        # ---- read
        main_layout          = QVBoxLayout( self )
        photo_layout         = QHBoxLayout( self )

        main_layout.addLayout( photo_layout )

        #view_read         = QTableView()     # claud could not get to work
        view_read         = QTableWidget()   # blackbox
        self.view_read    = view_read
        self.view_read.setColumnCount(5)
        self.view_read.setHorizontalHeaderLabels(["Photo Name",
                                             "Photo File Name",
                                             "Photo ID",
                                             "Photo Show Name",
                                             "Photo Show ID",
                                             ])

        view_read.cellClicked.connect( self._on_list_click  )
        photo_layout.addWidget( self.view_read )
        self.create_context_menu()

        # ---- photo
        a_photo_viewer            = photo_viewer.PhotoViewer( self )
        self.photo_viewer         = a_photo_viewer
        photo_layout.addWidget( a_photo_viewer )

        # view                = QTableView()
        # self.view_display   = view
        # view.setModel( model )


        # ---- write
        self.view_write    = QTableView()
        main_layout.addWidget( self.view_write )
        # # Set up the layout

        # self.widget.setLayout( self.layout )

        # self.layout.addWidget( view )


        # ---- buttons -- test photo select
        button_layout          = QHBoxLayout( self )
        main_layout.addLayout( button_layout )

        # a_widget  = QLabel( "for the photos>>" )
        # button_layout.addWidget( a_widget )

        # a_widget        = QPushButton( "29" )
        # connect_to      = functools.partial( self.select_by_id,
        #                                       29  )
        # a_widget.clicked.connect(  connect_to )
        # button_layout.addWidget( a_widget )

        # a_widget        = QPushButton( "2299" )
        # connect_to      = functools.partial( self.select_by_id,
        #                                      2299  )
        # a_widget.clicked.connect(  connect_to )
        # self.layout.addWidget( a_widget )

        # #
        # a_widget        = QPushButton( "<prior" )
        # #a_widget.clicked.connect(  self.fit_in_view )
        # button_layout.addWidget( a_widget )

        # #
        # a_widget        = QPushButton( "next>" )
        # #a_widget.clicked.connect(  self.fit_in_view )
        # button_layout.addWidget( a_widget )

        #
        a_widget        = QPushButton( "add row" )
        a_widget.clicked.connect(  self.add_row )
        button_layout.addWidget( a_widget )

        #
        a_widget        = QPushButton( "delete_row" )
        #a_widget.clicked.connect(  self.add_row )
        button_layout.addWidget( a_widget )
        #
        a_widget        = QPushButton( "save_all" )
       # a_widget.clicked.connect(  self.add_row )
        button_layout.addWidget( a_widget )

    # --------------------
    def create_context_menu(self):
        """
        what it says

        """
        self.contextMenu = QMenu(self)

        addAction        = QAction("Add Row", self)
        #addAction.triggered.connect(self.addRow)
        self.contextMenu.addAction(addAction)

        deleteAction = QAction("Delete Row", self)
        #deleteAction.triggered.connect(self.deleteRow)
        self.contextMenu.addAction(deleteAction)

        self.view_read.setContextMenuPolicy(Qt.CustomContextMenu)
        self.view_read.customContextMenuRequested.connect( self.showContextMenu )

    def showContextMenu( self, pos ):
        """
        what it says
        !! change my name

        Args:
            pos (TYPE): DESCRIPTION.

        Returns:
            None.

        """
        self.contextMenu.exec_( self.view_read.mapToGlobal(pos) )

    # ---------------------------------
    def setup_models( self,  ):
        """
        may have too many instances
        Returns:
            modifies self, establishes -- wrong names
            self.view_model
            self.edit_model
            self.sql_read
        """
        # ---- read model

        self.sql_read = """
            SELECT
              photo.name,
              photo.photo_fn,
              photo.id,
              photoshow.name,
              photoshow.id,
              photoshow_photo.seq_no,
              photoshow_photo.photoshow_id
            FROM   photo
            JOIN   photoshow_photo
            ON     photoshow_photo.photo_id = photo.id
            JOIN   photoshow
            ON     photoshow.id = photoshow_photo.photoshow_id
            WHERE  photoshow.id = :id;
        """


        # """
        # #model        = QSqlQueryModel()
        # # next to allow additions
        # model               = sql_query_model_plus.SqlQueryModelPlus( )
        # # self.model_display  = model
        # # Prepare the SQL query
        # query              = QSqlQuery()
        # query.prepare( model )

        # # model              =  QSqlTableModel()
        # # self.model_update  = model
        # # Prepare the SQL query

        #model        = QSqlQueryModel()
        # pre bb for model
        # query_model_read       =  sql_query_model_plus.SqlQueryModelPlus()
        # self.query_model_read  = query_model_read

        query_read            = QSqlQuery()
        self.query_read_prep  = query_read  # looks wrong

        query_read.prepare(  self.sql_read  )

        # Bind values to the query  --- can leave until we do query
        query_read.bindValue(":id", id )

        # Execute the query and set the model
       # query.exec_()
        # query_model_read.setQuery( query_read,  )

        # ---- write model
        #db     = AppGlobal.qsql_db_access.db

        table_model_write        = QSqlTableModel( self,  self.db )
        self.table_model_write   = table_model_write

        self.table_model_write.setTable( "photoshow_photo" )
        self.table_model_write.setEditStrategy( QSqlTableModel.OnManualSubmit )
        self.table_model_write.setFilter( "photoshow_id = 29 " )


    # ------------------------------------------
    def _on_list_click( self, row, column ):
        """
        what it says, read
        now just a table
        """
        print("Row %d and Column %d was clicked" % (row, column))

        print( f"PhotoshowDetailListTab_on_list_click   ")
        # row                     = index.row()
        # column                  = index.column()
        self.list_ix           = row
        self.prior_next( 0 )


    # ------------------------------------------
    def _display_photo_by_fn( self, file_name  ):
        """
        what it says, read
        do we need this?
        """
        self.photo_viewer.display_file( file_name )


    # ------------------------------------------
    def prior_next( self, delta  ):
        """
        get and put in control the prior or next photo
        using delta to determine which

        what it says, read
        direction  + forward, -backward 0 at start
        -- perhaps let it use any number so as to jump around


        watch for off by one, assume zero indexing

        """
        #prior_list_ix    = self.list_ix  # ng
        no_rows    = self.view_read.rowCount()

        list_ix                  = self.list_ix
        new_list_ix              = list_ix + delta
        # self.list_ix           = row
        if no_rows <= 0:
            msg     = f"prior_next {no_rows = } {delta = } should clear display"
            print( msg )

        if new_list_ix >= no_rows:
            new_list_ix  =  no_rows -1
            msg     = f"prior_next {no_rows = } {delta = } tried to index past end"
            print( msg )

        elif new_list_ix < 0:
            new_list_ix  =  0
            msg     = f"prior_next {no_rows = } {delta = } tired to index before start"
            print( msg )
        # else in range

        self.list_ix           = new_list_ix
        # fn_index               = self.query_model_read.index( new_list_ix, 1 )
        # file_name              = self.query_model_read.data( fn_index, Qt.DisplayRole )

        fn_item               =  self.view_read.item( self.list_ix,  1 )
        file_name  = fn_item.text() if fn_item is not None else ""

        #rint( f"change to prior next 0 {file_name = }" )
        self._display_photo_by_fn( file_name )

        self.photo_tab.display_file( file_name )  # the other tab in sub window
        print( "above bad because hard to find self.photo_tab.display_file( file_name )"  )


    #-------------------------------------
    def add_photo_to_show( self, row_dict  ):
        """
         use app global until i have something better
         for awhile same function down down there
         call via app_global
         AppGlobal.add_photo_target.add_photo_to_show( row_dict )
        """
        print( f"add_photo_to_show I was targeted  {row_dict}")
        self.add_row( row_dict )


    # ------------------------------------------
    def add_row( self,  row_dict = None   ):
        """
        None until get more hooked up
        post black box
        looks like we are missing sequence no
        and will need update for it ?
        add row data will be missing some values
        we will add here
        for now only at end
        """
        if row_dict is None:
            row_dict  = {}  # but will have error later

        # ---- setup data

        next_key                = AppGlobal.key_gen.get_next_key( self.list_table_name )

        # ---- sequence no
        max_seq            = 0
        seq_no_field_id    = 3
        for ix      in  range( 0, self.table_model_write.rowCount() ):
            ix_index          = self.table_model_write.index( ix, seq_no_field_id )
            seq_no            = self.table_model_write.data(  ix_index, Qt.DisplayRole )
            max_seq           = max( max_seq, seq_no )

        seq_no   = max_seq + 1
        #rint( f"{seq_no = }   ")
        photoshow_photo_id      = next_key

        # much is phony data -- later in call
        row_dict ["photoshow_id" ]             = self.photoshow_id
        row_dict ["photoshow_photo_seq_no" ]   = 999,
        row_dict ["seq_no" ]                   = seq_no,
        row_dict[ "photoshow_name" ]           = "don't need ps name"

        # must match the select order
        row_list    = [ row_dict[ "photo_name" ],
                               row_dict[ "photo_fn" ],
                               row_dict[ "photo_id" ],
                               row_dict[ "photoshow_name" ],
                               row_dict[ "photo_name" ],
                               row_dict[ "photoshow_id" ],
                               row_dict[ "photoshow_photo_seq_no" ],
                               row_dict[ "photoshow_photo_id" ],
                            ]

        # ---- read
        # self.query_model_read.addRow( row_list )
        # self.query_model_read.layoutChanged.emit()

        view_read      = self.view_read
        row            =  view_read.rowCount()
        #rint( f"{row = }")  -- look at query
        view_read.setRowCount( row + 1 )
        view_read.setItem(row, 0, QTableWidgetItem( row_dict[ "photo_name" ]  ) )
        view_read.setItem(row, 1, QTableWidgetItem( row_dict[ "photo_fn" ]  ) )
        view_read.setItem(row, 2, QTableWidgetItem( row_dict[ "photo_id" ]  ) )
        view_read.setItem(row, 3, QTableWidgetItem( row_dict[ "photoshow_name" ]  ) )
        view_read.setItem(row, 4, QTableWidgetItem( row_dict[ "photoshow_id" ]  ) )
        # may be more

        # ---- write
        record          =  self.table_model_write.record()
        record.setValue(  "id",   photoshow_photo_id               )

        record.setValue(  "photoshow_id",   row_dict[ "photoshow_id" ]    )
        record.setValue(  "photo_id",       row_dict[ "photo_id" ]    )

        field_name  = "seq_no"
        record.setValue(  field_name,       row_dict[ field_name ]    )

        ok   = self.table_model_write.insertRecord( -1,  record  )  #const QSqlRecord &record)addRow( custom_row_data)
        print( f"add_row  insert record {ok = }")

        self.table_model_write.layoutChanged.emit()

    # ------------------------------------------
    def add_row_pre_bb( self,    ):
        """
        looks like we are missing sequence no
        and will need update for it ?
        add row data will be missing some values
        we will add here

        """

        # ---- setup data

        next_key                = AppGlobal.key_gen.get_next_key( self.list_table_name )

        # ---- sequence no
        max_seq            =0
        seq_no_field_id    = 3
        for ix      in  range( 0, self.table_model_write.rowCount() ):
            ix_index          = self.table_model_write.index( ix, seq_no_field_id )
            seq_no            = self.table_model_write.data(  ix_index, Qt.DisplayRole )
            max_seq           = max( max_seq, seq_no )

        seq_no   = max_seq + 1
        #rint( f"{seq_no = }   ")


        photoshow_photo_id      = next_key
        row_dict            = { "photo_name":               "this is a photo_name",
                               "photo_fn":                 "/mnt/WIN_D/PhotoDB/13/Dsc02602.jpg",
                               "photo_id":                  999,
                               "photoshow_name":           "photoshow_name data ",
                               "photoshow_id":              self.photoshow_id,
                               "photoshow_photo_seq_no":    999,
                               "photoshow_photo_id":        photoshow_photo_id,
                               "seq_no":                    seq_no,
                               }

        # must match the select order
        row_list    = [ row_dict[ "photo_name" ],
                               row_dict[ "photo_fn" ],
                               row_dict[ "photo_id" ],
                               row_dict[ "photoshow_name" ],
                               row_dict[ "photo_name" ],
                               row_dict[ "photoshow_id" ],
                               row_dict[ "photoshow_photo_seq_no" ],
                               row_dict[ "photoshow_photo_id" ],
                            ]

        # ---- read
        self.query_model_read.addRow( row_list )
        self.query_model_read.layoutChanged.emit()

        # ---- write
        record          =  self.table_model_write.record()
        record.setValue(  "id",   photoshow_photo_id               )

        record.setValue(  "photoshow_id",   row_dict[ "photoshow_id" ]    )
        record.setValue(  "photo_id",       row_dict[ "photo_id" ]    )

        field_name  = "seq_no"
        record.setValue(  field_name,       row_dict[ field_name ]    )


        ok   = self.table_model_write.insertRecord( -1,  record  )  #const QSqlRecord &record)addRow( custom_row_data)
        print( f"add_row  insert record {ok = }")

        self.table_model_write.layoutChanged.emit()

        """
        record = model.record()

        # Populate the QSqlRecord with data
        record.setValue("name", "New Photo")
        record.setValue("photo_fn", "new_photo.jpg")
        record.setValue("id", None)  # Assuming the ID is auto-increment
        record.setValue("photoshow_id", 1)  # Example value

        # Insert the QSqlRecord into the model
        if model.insertRecord(-1, record):
            print("Record inserted successfully")
             # query_model_read
             # table_model_write
"""

    # ------------------------------------------
    def select_by_id ( self, id ):
        """
        black box
        what it says, read
        id is the id of the photo show
        self.edit_model.setFilter( "id = 33 " )

        #model.setFilter(f'photoshow.id = {photoshow_id}')

        # Set the sort order
        column_to_sort_by   = 0  # Index of the column to sort by (e.g., 0 for the first column)
        sort_order          = Qt.AscendingOrder  # or Qt.DescendingOrder
        self.edit_model.setSort(column_to_sort_by, sort_order)


        msg       = f"{self.edit_model.selectStatement()}"
        print( msg )
        """
        self.photoshow_id   = id

        print( f"select_by_id  {id = }")

        # ---- write
        self.table_model_write.setFilter( f"photoshow_id = {id} " )
        self.table_model_write.select()
        self.view_write.setModel( self.table_model_write )

        # ---- read
        sql_read = f"""
            SELECT
              photo.name AS photo_name,
              photo.photo_fn,
              photo.id AS photo_id,
              photoshow.name AS photoshow_name,
              photoshow.id AS photoshow_id
            FROM   photo
            JOIN   photoshow_photo
            ON     photoshow_photo.photo_id = photo.id
            JOIN   photoshow
            ON     photoshow.id = photoshow_photo.photoshow_id
            WHERE  photoshow.id = :id;
        """

        query_read      = QSqlQuery( self.db )

        query_read.prepare( sql_read )
        query_read.bindValue( ":id", id )

        #is_ok      =  query_read.exec( )

        view_read  = self.view_read

        if query_read.exec_():
            while query_read.next():
                row =  view_read.rowCount()
                #rint( f"{row = }")
                view_read.setRowCount( row + 1 )
                view_read.setItem(row, 0, QTableWidgetItem( query_read.value(0)))
                view_read.setItem(row, 1, QTableWidgetItem( query_read.value(1)))
                view_read.setItem(row, 2, QTableWidgetItem( str(query_read.value(2))))
                view_read.setItem(row, 3, QTableWidgetItem( query_read.value(3)))
                view_read.setItem(row, 4, QTableWidgetItem( str(query_read.value(4))))
        else:
            QMessageBox.critical(self, "Error", "view_read Failed to execute query")

        # photo display
        self.list_ix    = 0
        self.prior_next( 0 )
