#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
just a place to explore code
"""


# ---- tof

# ---- imports

# ---- end imports


#-------------------------------


from PyQt5.QtWidgets import (  QMessageBox, )
from collections import defaultdict


# ---- eof

KEY_DICT    = { "sys":      "system",
                "system":      "system",
                "subsys":   "sub_system",
                "name": "name",
                "id": "id",


                }
class AClass():

    def __init__( self ):
        pass

    def parse_search_part( self, criteria, part ):
        """

        still needs error check
        """
        splits    = part.split( "=" )
        key       = (splits[0].strip()).lower()
        value     = splits[1].strip()
        # may need type conversion when get to dates
        key       = KEY_DICT[key]
        criteria[key] = value




    def parse_search_stuffdb( self, a_string ):
        """
        >>search jeoe sue   /sys=python /subsys=qt
        change to a dict

        cirteria = {key_words: "joe" "sue" }



        """
        criteria    = defaultdict( None )
        parts       = a_string.split( "/" )
        key_words   = parts[0].strip()
        criteria[ "key_words" ] = key_words

        for i_part in parts[ 1: ]:
            try:
                self.parse_search_part( criteria, i_part  )
            except ValueError as error:
                # Access the error message
                error_message = str(error)
                msg  = (f"Parse >>search Caught an error: {error_message}")
                msg_box             = QMessageBox()
                msg_box.setIcon( QMessageBox.Information )
                msg_box.setText( msg )
                msg_box.setWindowTitle( "Sorry that is a No Go " )
                msg_box.setStandardButtons( QMessageBox.Ok )

        print( criteria )

        return criteria



a_class   = AClass()


a_class.parse_search(   "word b_word, /sys=Python" )
a_class.parse_search(   "word b_word, /sys=Python" )
a_class.parse_search(   "word b_word, /sys=Python  /subsys=qt" )
a_class.parse_search(   "word b_word, /subsys=Python  /subsys=qt" )
a_class.parse_search(   "word b_word, /subsys=qt7  /sys=Python" )




