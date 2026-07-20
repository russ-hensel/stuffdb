#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 21:22:28 2026

@author: russ
"""

# ---- tof

# --------------------
if __name__ == "__main__":
    import main   # noqa  stops auto removal by pycln
# --------------------

# ---- imports

from pathlib import Path


# ---- imports local


import photo_plus_ext
from   app_global import AppGlobal


# -----------------------------------
class ExifExtrctToUi( ):
    """
    see init
    """
    def __init__( self, field_dict ):
        """
        when called will get the filename
             extract the exif data
             put the data in the fields
             field_dict[ field_name ] = widget
        the usual
                exif_extract_to_ui.ExifExtrctToUi( field_dict )

        """
        self.field_dict         = field_dict
            # dict of widgets key: field name
        self.photo_plus         = photo_plus_ext.PhotoPlus()
        self.picture_db_root    = AppGlobal.parameters.picture_db_root

    # -----------------------------------
    def get_full_path( self, file_sub, file_name ):
        """
        this may already be kicking around as a method
            base comes from parameters
            args, some protection against "/" may need more
            return full_path   -- not resolved
        """
        a_path          = Path()
        file_base       = self.picture_db_root
        file_sub        = file_sub.replace( "/", "" )
        full_path       = a_path.joinpath( file_base, file_sub, file_name  )

        return full_path

    # -----------------------------------
    def add_exif_data( self ):
        """
        check against data_dict  -- seem ok
        check against pp PhotoPlus
            # setup
            self.exif_to_ui    = exif_extract_to_ui.ExifExtrctToUi( field_dict )
            self.exif_to_ui.add_exif_data()

            !! may need current exif so do not update if already have

        """
        current_val_dict   = {}

        field_name         = "sub_dir"
        widget             = self.field_dict[ field_name ]
        widget.edit_to_dict( current_val_dict )  # value in current_val_dict
        sub_dir            = current_val_dict[ field_name ]

        field_name         = "file"
        widget             = self.field_dict[ field_name ]
        widget.edit_to_dict( current_val_dict )  # value in current_val_dict
        file               = current_val_dict[ field_name ]

        field_name         = "exif_make"
        widget             = self.field_dict[ field_name ]
        widget.edit_to_dict( current_val_dict )  # value in current_val_dict
        exif_make          = current_val_dict[ field_name ]

        full_path         = self.get_full_path( sub_dir, file )

        if full_path is None:
            return

        # !! debug delete some
        if exif_make is None or exif_make == "":
            pass
        else:
            print( "^^^^^^^^^^ no need for exif extraction ")
            return

        # can we use path??   #pp.reset( full_path )
        pp      = self.photo_plus
        pp.reset( str( full_path ) )

        exif_dict      =  pp.get_exifread_exif_dict()
        # key is the field_name, but perhaps not matching the form
                # key is a name exifread_dict[ "make" ]    =....

        # !! think about a better test??
        if exif_dict[ "lat" ] or exif_dict[ "make" ] is not None:

            # if True:  # just debug
            #     print( "got exif")
            #     for key, value in exif_dict.items():
            #         #rint( key, value )
            #         msg       = f"    exif_dict -- {key}: {value} {type(value)}"
            #         print( msg )

            # is there not a function to get to a dict   edit_to_dict may be too much
                  #                 widget      pp
            self.update_field( "exif_make",    "make",  current_val_dict,   exif_dict )
            self.update_field( "exif_model",   "model", current_val_dict,   exif_dict )
            self.update_field( "exif_lat",     "lat",   current_val_dict,   exif_dict )
            self.update_field( "exif_lon",     "lon",   current_val_dict,   exif_dict )
            self.update_field( "exif_ts",      "ts",    current_val_dict,   exif_dict )

    # -----------------------------------
    def update_field( self, field_name, exif_field_name, current_val_dict, exif_dict ):
        """
        do one field
            both dict go from names to values ?
            field dict pass as class attribute, could do with exif_dict as well

            current_val_dict
            exif_dict      # =  pp.get_exifread_exif_dict()  has
        """
        widget             = self.field_dict[ field_name ]
        widget.edit_to_dict( current_val_dict )  # value in current_val_dict
        current_data       = current_val_dict[ field_name ]

        exif_data          = exif_dict[ exif_field_name ]

        if exif_data is None or exif_data == current_data:
            pass

        else:
            current_val_dict[ field_name ] = exif_data
            widget.dict_to_edit( current_val_dict )


# # ---- eof ---------------------------
