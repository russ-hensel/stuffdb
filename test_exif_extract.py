#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
run inside stuffdb environment, perhaps as a helper
use own db connect thru alternate parms

/mnt/8ball1/first6_root/photos/photos_raw/from_phone/moved_to_computer/older_june23_copy


"""

# ---- tof

# # --------------------
# if __name__ == "__main__":
#     import main   # noqa  stops auto removal by pycln
# # --------------------

# ---- imports

from pathlib import Path


# ---- imports local

import adjust_path
import stuff_util_sql as su
import parms_temp
import photo_plus_ext


"""
Generator over a Qt SQL query: prepared SELECT with named bind variables.

Each step yields a dict with keys id, name, file, sub_dir (photo table fields).

Example::

    gen = PhotoRowGenerator(
        db,
        "SELECT id, name, file, sub_dir FROM photo WHERE type = :ptype",
        bind_values={"ptype": "print"},
    )
    for row in gen:
        print(row["id"], row["name"])
"""

from qtpy.QtSql import QSqlQuery

# Columns returned in every yielded dict (see spec / photo table).
OUTPUT_KEYSxxx = ("id", "name", "file", "sub_dir")


class PhotoRowGenerator:
    """
    Iterable that runs one prepared SELECT and yields one dict per row.

    Parameters
    ----------
    database : QSqlDatabase
        Open Qt database connection.
    select_sql : str
        SELECT must return columns id, name, file, sub_dir (by name).
    bind_values : dict, optional
        Named bind values, e.g. {"ptype": "print"} or {":ptype": "print"}.
    """

    def __init__( self, database, select_sql, *, output_keys = None, bind_values = None ):
        """ """
        self._database      = database
        self._select_sql    = select_sql
        self._bind_values   = dict( bind_values or {} ) # chats trick, slower?
        self._query         = None

        if output_keys is None:
            output_keys     = {}
        self.output_keys    =  output_keys

        self.last_error     = ""


    # -----------------------------------------
    def __iter__(self):
        """ """
        self._query = QSqlQuery( self._database )

        if not self._query.prepare( self._select_sql ):
            self.last_error = self._query.lastError().text()
            raise RuntimeError(f"prepare failed: {self.last_error}")

        for name, value in self._bind_values.items():
            placeholder = name if str(name).startswith(":") else f":{name}"
            self._query.bindValue( placeholder, value )

        if not self._query.exec_():
            self.last_error = self._query.lastError().text()
            raise RuntimeError( f"exec failed: {self.last_error}" )

        self.last_error = ""
        return self

    # -----------------------------------------
    def __next__(self):
        if self._query is None or not self._query.next():
            raise StopIteration
        return self._row_to_dict()

    # -----------------------------------------
    def _row_to_dict( self ):
        """ """
        row = {}

        for key in self.output_keys:
            val = self._query.value( key )

            # do we need this
            if key == "id" and val is not None:
                try:
                    val = int(val)
                except ( TypeError, ValueError ):
                    pass
            row[key] = val

        return row


# Example SELECT for the photo table (spec).
DEFAULT_PHOTO_SELECT = (
    "SELECT id, name, file, sub_dir FROM photo WHERE type = :ptype"
)


class ExifExtractor( ):
    def __init__( self, db, sql, out_file_name ):
        """
        the usual
        """
        #super().__init__()
        self.db             = db
        self.sql            = sql
        self.out_file_name  = out_file_name
        self.output_keys    =  ( "id", "name", "file", "sub_dir" )
        self.parameters     = parms_temp.ParmsTemp()
        self.photo_plus     = photo_plus_ext.PhotoPlus()

    # -----------------------------------
    def get_full_path( self, file_sub, file_name ):
        """
        base comes from parameters
        args, some protection against "/" may need more
        return full_path   -- not resolved
        """
        a_path          = Path()
        file_base       = self.parameters.picture_db_root
        file_sub        = file_sub.replace( "/", "" )
        full_path       = a_path.joinpath( file_base, file_sub, file_name  )

        return full_path

    # -----------------------------------
    def get_exif( self, file_sub, file_name ):
        """

        return dict of my version of values
        """

    # -----------------------------------
    def test_add_exif_data( self ):
        """

        """
        ix_max          = 300000
        prg             = PhotoRowGenerator( self.db ,
                                                select_sql  = self.sql,
                                                output_keys = self.output_keys )

        pp              = self.photo_plus

        for ix, i_dict in enumerate( prg ):
            # self.output_keys    =  ( "id", "name", "file", "sub_dir" )
            #rint( "\n\n---------------------------------")
           #print( f"{ix} -> {i_dict}")
           #rint( f"{self.get_full_path(  i_dict[ "sub_dir" ], i_dict[  "file" ] ) = }")

            file_name   = i_dict[  "file" ]

            if file_name is None or  file_name == "":
                continue

            full_path    = self.get_full_path( i_dict[ "sub_dir" ], i_dict[ "file" ] )
            print( f"{ix = }  {full_path = }")

            # can we use path??   #pp.reset( full_path )
            pp.reset( str( full_path ) )

            #exif_string     =  pp.get_exif_string()
            pp.get_exifread_exif_dict()

            a_dict      =  pp.get_exifread_exif_dict()

            # !! think about a better test??
            if a_dict[ "lat" ] or a_dict[ "make" ] is not None:
                print( "got exif")
                dict_ix = 0

                for key, value in a_dict.items():
                   #rint( key, value )
                   dict_ix     += 1
                   ret     = f"     {dict_ix} -- {key}: {value} {type(value)}"
                   print( ret )

            if a_dict != {}:
                if False:
                    print( "update row off")
                else:
                    self.update_row( i_dict[ "id" ], a_dict )

            if ix > ix_max:
                print( ">>>>>>>>>>>>>>>>>Hit Max Rpw <<<<<<<<<<<<<<<<<<<<<<<<<<<")
                break

    # -----------------------------------
    def update_row( self, id_value, exif_dict ):
        """
        -1 error
        0  different kind of error
        """
        query   = QSqlQuery( self.db )

        sql     = ( "UPDATE photo "
                     "SET  "
                        " exif_make     = :exif_make, "
                        " exif_model    = :exif_model, "
                        " exif_lat      = :exif_lat, "
                        " exif_lon      = :exif_lon, "
                        " exif_ts       = :exif_ts "
                                  # watch out for , delete it
                     "WHERE id = :id" )

        # Prepare the UPDATE statement with bind variables
        if not query.prepare( sql ):
            print( f"Failed to prepare query: {query.lastError().text()}" )
            return -1

        # Bind values
        query.bindValue(":id",          id_value )
        query.bindValue(":exif_make",   exif_dict[ "make" ] )
        query.bindValue(":exif_model",  exif_dict[ "model" ] )
        query.bindValue(":exif_lat",    exif_dict[ "lat" ] )
        query.bindValue(":exif_lon",    exif_dict[ "lon" ] )
        query.bindValue(":exif_ts",     exif_dict[ "ts" ] )

        # Execute the query
        if not query.exec_():
            print(f"Query execution failed: {query.lastError().text()}")
            return -1

        # Check if any rows were affected
        rows_affected   = query.numRowsAffected()

        if rows_affected == 0:
            # would be an error
            print(f"No rows updated for id {id_value}")

        return rows_affected

#------------------------------------
def test_1():
    """
        see parms_temp for db

        see sql for select, will rewriet now could change


    """
    db   = su.create_connection( use_temp = True )   # beware not using True
    sql  = (
        "SELECT id, name, file, sub_dir FROM photo WHERE sub_dir = '24' "
    )
        # match out var and bind to this
    out_file_name       = "./exif_out"

    a_exif_extractor    =  ExifExtractor( db = db, sql = sql, out_file_name = out_file_name )

    a_exif_extractor.test_add_exif_data(   )

# --------------------
if __name__ == "__main__":

    test_1()
# --------------------



# ---- eof ---------------------------


