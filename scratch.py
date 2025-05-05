

# ---------------------- some problem getting this to run
# import adjust_path
# import  fluent_python_helpers as fph


# deck = fph.FrenchDeck()




































        model               = QSqlQueryModel( )
        view                = QTableView()

                                             display_order  = 30,
                                             max_len        = None,
                                             default_func   = None,
                                             is_key_word    = True,



I am in Python using qt and its widgets I am trying to join two tables.
I have included the creat statements.
I think I have a mistake.  Please comment on:

    # ---------------------------------
    def _build_model( self, ):
        """

        --------------------
        photoshow
            CREATE TABLE photoshow    (
                 id  INTEGER,
                 id_old  VARCHAR(15),
                 name  VARCHAR(50),
                 cmnt  VARCHAR(100),
                 start_date  INTEGER,
                 end_date  INTEGER,
                 create_date  INTEGER,
                 type  VARCHAR(20),
                 add_kw  VARCHAR(50),
                 web_site_dir  VARCHAR(240)
                )

        CREATE TABLE photo_in_show    (
                 id  INTEGER,
                 photo_id_old  VARCHAR(15),
                 photo_show_id_old  VARCHAR(15),
                 sequence  INTEGER,
                 photo_in_show_id_old  VARCHAR(15),
                 photo_id  INTEGER,
                 photo_show_id  INTEGER,


        """

        model              =  QSqlRelationalTableModel(  self, self.db    )
        self.model         = model

        model.setTable( self.table_name )

        ix_foreign_key        = 0


        foreign_table         = "photo_in_show"
        foreign_table_key     = "photo_show_id"

        self.model.setRelation( ix_foreign_key, QSqlRelation( foreign_table,
                                foreign_table_key,
                                "id"  ))



















#-------------------------------


select_by_id PictureAlbumtSubTab
SQL select: SELECT relTblAl_0.id,photoshow."id_old",photoshow."name",
photoshow."cmnt",photoshow."start_date",photoshow."end_date",photoshow."create_date",
photoshow."type",photoshow."add_kw",photoshow."web_site_dir"
FROM photoshow,photo_in_show relTblAl_0
WHERE (photoshow."id"=relTblAl_0.photo_show_id) AND (photo_in_show.photo_id = 1023)

                SELECT

                photoshow.name,
                photoshow.id,

                photo_in_show.photo_id,

                photo_in_show.sequence,
                photo_in_show.photo_show_id


                FROM   photoshow
                JOIN   photo_in_show  ON   photo_in_show.photo_show_id  = photoshow.id


                WHERE  photo_in_show.photo_id = 1023 ;
----------------------------------






# ---- eof



for i_field in self.field_list:
    print( f"{i_field.field_name}")




        a_partial           = partial( self.do_ct_value, "" )
        self.ct_default     = a_partial



column_list

criteria_dict

SELECT   photo.id,  photo.name,  photo.title,  photo.add_kw, photo.descr    FROM photo

     ORDER BY  dt_item ASC






- DEBUG - PictureViewer Failed to load image pixmap is null
2025-03-26 10:34:13,826 - DEBUG - PictureViewer display_file error     file_name = '' file_exists = False
2025-03-26 10:34:13,828 - DEBUG - ListTabBase_delete_row_by_id




