#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 16:13:31 2024

@author: russ
"""

# ---- imports
import re


# ------------------------------------------
class KeyWords(   ):
    """
    in flux, needs better name move testing
    """
    def __init__(self):
        """
        do some key word processing
            still have to figur out how much
            think can include the db work

        """
        self.is_done            = False
            # do we hav uuptodate current and old

        self.old_string           = ""
        self.new_string           = ""
        # perhaps all should be sets

        self.new_key_words        = []

        self.old_key_words        = []
        self.key_word_tn          = None



        self.add_key_words        = set( )
        self.delete_key_words     = set( )

    #----------------------------------
    def string_to_key_words( self,  a_string ):
        """
        !! change to return a set

        Args:
            a_string (TYPE): DESCRIPTION.

        set   of key words

        split up camel case
        remove and split on dirt   !! durt might remain
        lower case
        remove terminal s on over 2 characters
        make list
        lower


        """
        key_word_list    = self.split_on_caps_and_whitespace( a_string )
        key_word_list    = [ a_word.lower( ) for a_word in key_word_list ]

        # try modify in place in list rathere than new list
        new_key_word_set  = set()
        for a_key_word   in key_word_list:
            pass
            # might do lower case here
            if len( a_key_word ) > 3:
                if a_key_word.endswith( "s" ):
                    a_key_word    = a_key_word[ : -1]
            new_key_word_set.add( a_key_word )
        key_word_set  = new_key_word_set

        return key_word_set

    #----------------------------------
    def string_to_old( self, a_string ):
        """
        process a string to key words

        """
        self.is_done            = False
        self.old_string         = a_string
        self.old_key_words      = self.string_to_key_words( a_string )

    #----------------------------------
    def string_to_new( self, a_string ):
        """
        process a string to key words

        """
        self.is_done            = False
        self.new_string         = a_string
        self.new_key_words      = self.string_to_key_words( a_string )

    #----------------------------------
    def compute_add_delete( self,   ):
        """
        process a string to key words

        """
        pass


    # --------------------------------------
    def split_on_caps_and_whitespace( self, a_string ):
        """
        chat says
        chat_cammel_split.py

        Returns:
            split_words in a list

        """
        # Split based on whitespace
        words = re.split( r'\s+', a_string )

        # Split based on embedded capitest_string tal letters
        split_words = []
        for word in words:
            split_words.extend(re.findall(r'[a-z]+|[A-Z]+(?![a-z])|[A-Z][a-z]*', word))

        return split_words

    # --------------------------------------
    def update_key_words( self,   ):
        """

        Returns:
            db adds and deleteds done

        """
        print( "!!tbd")




a_key_words  = KeyWords()

a_string  = "This 123 !!  ##  # isATest StringWithSeveral with with withs EmbeddedCaps AndWhiteSpace"

print( a_string )
print( a_key_words.string_to_key_words( a_string) )