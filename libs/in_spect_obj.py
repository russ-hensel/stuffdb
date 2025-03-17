#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof

"""
the main file for info_about


--
--
"""


# ---- search
"""
Use
        think this is call but check

import in_spect_obj
print( in_spect_obj.IN_SPECT_OBJ )


use
or
in_spect_it    = in_spect_obj.IN_SPECT_OBJ.in_spect_it



in_spect_obj.IN_SPECT_OBJ.in_spect_it(
                    an_object,
                    # *,
                    msg      = None,
                    max_len  = None,
                    xin      = "",
                    print_it = True,
                    sty      = "",
                    include_dir  = False,  )

typically

info_about.INFO_ABOUT.find_info_for(
                    an_object,
                    msg      = msg
                        )

# with logging

log_msg      = info_about.INFO_ABOUT.find_info_for(
                    an_object,
                    msg         = msg,
                    print_it    = False
                   )
logging.debug( log_msg )



"""



doesitexist   = """

   my_type       =  QSqlTableWidget
       #a_str   = f"{a_str}\n{xin}{INDENT2}database()     = {a_obj.database() }"
       a_str   = f"{a_str}\n{xin}{INDENT2}rowCount()     = {a_obj.rowCount() }"
       # if a_obj.rowCount( ) > 0:

 """
import importlib
import sys
import logging

import in_spect_parameters
import in_spect_search

    # ia_parameters.PARAMETERS


# ---- end imports


IN_SPECT_OBJ    = None   # after import is an infoabout object


DEBUGGING       = False  # in testing may be changed externally

indent_0        = "   " # used for formatting
INDENT          = "    "
INDENT2         = INDENT

MAX_REPR_LEN    = 150 #
MAX_STR_LEN     = 150 #
MAX_LIST_ITEMS  = 8

NEW_LINE        = "\n"
MSG_PREFIX      = "\nInfo About >>>> "

LOG_LEVEL       = 20 # level form much debug       logging.log( LOG_LEVEL,  debug_msg, )

if DEBUGGING:
    pass

common_dir_items  = (
['__module__',
 '__lt__',
 '__le__',
 '__eq__',
 '__ne__',
 '__gt__',
 '__ge__',
 '__weakref__',
 '__doc__',
 '__hash__',
 '__new__',
 '__init__',
 '__dict__',
 '__repr__',
 '__str__',
 '__getattribute__',
 '__setattr__',
 '__delattr__',
 '__reduce_ex__',
 '__reduce__',
 '__subclasshook__',
 '__init_subclass__',
 '__format__',
 '__sizeof__',
 '__dir__',
 '__class__']
)

more_common_dir_items  = (
[ "__iter__", "__mod__", "__rmod__",

 "__len__", "__getitem__", "__add__", "__mul__", "__rmul__", "__contains__" ] )

common_dir_items = common_dir_items  + more_common_dir_items

def make_list( a_string,   ):
    """
    space delimited to string -- just a split??
    eliminate unless grows
    """
    splits      = a_string.split()
    return splits

# ------------------------
def is_imported( module_name,   ):
    """what it says
    too simple to live?
    not working just return false
    """
    return False
    is_imported   = module_name in sys.modules
    return is_imported

    # except Exception as an_except:   #  or( E1, E2 )
    #     ret = False

    # return ret

def create_instance( module_name, class_name ):
    """
    assumes no args to create class -
    could add args to this
    """
    if not is_imported( module_name, ):
         module = importlib.import_module( module_name )
    else:
        pass

    cls = getattr( module, class_name )

    instance = cls()

    return  instance


# ---------------------
def to_columns( item_list, format_list = ( "{: <30}", "{:<30}" ), indent = "    "  ):
    """
    for __str__  probably always default format_list
    see ColunmFormatter which is supposed to be more elaborate version
    see its __str__
    ex:
        import string_util
        a_str     = string_util.to_columns( a_str, ["column_data",    f"{self.column_data}"  ] )
        a_str     = string_util.to_columns( a_str,
                                            ["column_data",    f"{self.column_data}"  ],
                                            format_list = ( "{: <30}", "{:<30}" )
    """
    #rint ( f"item_list {item_list}.............................................................. " )
    line_out  = ""
    for i_item, i_format in zip( item_list, format_list ):
        a_col  = i_format.format( i_item )
        line_out   = f"{indent}{line_out}{a_col}"
    # if current_str == "":
    #     ret_str  = f"{line_out}"
    # else:
    #     ret_str  = f"{current_str}\n{line_out}"

    return line_out



#----------------
def short_repr( a_obj, max_len = MAX_REPR_LEN ):
    """
    make a repr, shorten if too long
    read code
    consider ret of is truncated in tuple

    """
    a_str  = repr( a_obj )

    if len( a_str ) > max_len:
        a_str  = a_str[ :max_len ] + "..."

    return a_str

# -----------
def short_str( a_obj, max_len = MAX_STR_LEN ):
    """
    make a str, shorten if too long
    read code
    consider ret of is truncated in tuple

    """
    a_str  = repr( a_obj )

    if len( a_str ) > max_len:

        a_str  = a_str[ :max_len ] + "..."
    return a_str

# ----------------------------------------
class InSpectObj(   ):
    """
    About this class.....
    """
    #----------- init -----------
    def __init__(self,   ):
        """
        Usual init see class doc string
        """
        global INFO_ABOUT
        self.file_data_list       = None
        self.inspectors           = []
        # this is the constructor run when you create
        # like  app = AppClass( 55 )
        self.info_provider_list    = []
        #self.add_defined_inspectors()

        self.info_about_base       = InSpectObjBase()
        self._search()
        #INFO_ABOUT                 = self

        # now have file data list
    #--------------------
    def _search( self ):
        """ """
        debug_msg =  ( f"InfoAbout._search {in_spect_parameters.PARAMETERS}" )
        logging.log( LOG_LEVEL,  debug_msg, )

        search                  = in_spect_search.Search( )
        self.file_data_list     = search.file_data_list
            # sorted list is returned

        msg   = ( "------------- InfoAbout create objects ------------------")
        logging.log( LOG_LEVEL,  msg, )

        for i_file_data in self.file_data_list:
            module_name     = i_file_data[ "module:" ]
            class_names     = i_file_data[ "class_names:" ]
            class_names     = make_list( class_names )

            for i_class_name in class_names:
                debug_msg   = ( f"create {i_class_name}")
                logging.log( LOG_LEVEL,  debug_msg, )
                i_inspector   = create_instance( module_name, i_class_name )
                self.info_provider_list.append( i_inspector )

    #-------------------------
    def in_spect_it( self,
                    inspect_me,
                    *,
                    msg             = None,
                    max_len         = None,
                    xin             = "",
                    print_it        = True,
                    sty             = "",
                    include_dir     = False,  ):

        """
        search for an object that know about an  inspect_me
        msg    = info_about.INFO_ABOUT.find_info_for(
                        inspect_me,
                        msg             = "find_info_for",
                        max_len         = None,
                        xin             = "",
                        print_it        = False,
                        sty             = "",
                        include_dir     = False,  )

        """
        info  = None

        for i_info_provider in self.info_provider_list:
            if  i_info_provider.have_info_for( inspect_me ):
                print( "---------------")
                info = i_info_provider.get_info(
                         inspect_me,
                         msg            = msg,
                         max_len        = None,
                         xin            = "",
                         print_it       = True,
                         sty            = "",
                         include_dir    = False,
                        )
                break

        if info is None:
            #info = "no_info" # has info for everything, but not much
            info = self.info_about_base.get_info(
                     inspect_me,
                     msg            = None,
                     max_len        = None,
                     xin            = "",
                     print_it       = True,
                     sty            = "",
                     include_dir    = False,
                    )

        return info


    #----------- debug -----------
    #----------- main functions -----------
    def __str__( self ):
        a_str   = ""
        a_str   = ">>>>>>>>>>* InfoAbout *<<<<<<<<<<<<"
        a_str   = to_columns( a_str, ["info_about_base",
                                           f"{self.info_about_base}" ] )
        a_str   = to_columns( a_str, ["info_provider_list",
                                           f"{self.info_provider_list}" ] )
        return a_str

#----------------------
class InSpectObjBase(   ):
    """
    lots may be implemented as utations
    """

    #----------- init -----------
    def __init__(self,       ):
        """
        Usual init see class doc string
        """
        self.reset()
        self.my_class    = None

    #---------------------
    def reset( self, ):
        """ """
        self.msg                   = ""
        self.line_list             = []
        #self.

    # --------------------------
    def have_info_for( self, a_obj ):

        return isinstance(  a_obj, self.my_class   )

    # def have_info_for( self, obj ):
    #     """ """
    #     have_info  = isinstance(  obj, self.my_class  )
    #     return have_info

    # ------------------------
    def get_info( self,
                    inspect_me,
                    *,
                    msg             = None,
                    max_len         = None,
                    xin             = "",
                    print_it        = True,
                    sty             = "",
                    include_dir     = False,
                    details_only    = False, ):
        """ """
        self.reset()

        self.inspect_me     = inspect_me
        self.msg            = msg
        self.max_len        = max_len
        self.xin            = xin
        self.print_it       = print_it
        self.sty            = sty
        self.include_dir    = include_dir
        self.details_only   = details_only
        self.fix_msg( )
        self.add_line( self.msg )  # move inside fix._msg ??

        self.begin_info()
        self.mid_info()
        self.custom_info()

        self.dir_info()

        info                =  NEW_LINE.join( self.line_list )

        return info

    # ----------------------------------------
    def  dir_info( self  ):
        """
        Purpose:
            list out some __dir__() info as a string

            <class 'PyQt5.QtSql.QSqlError.ErrorType'>
            databaseText
            a_atter = <built-in method databaseText of QSqlError object at 0x7f84245a0350>
            driverText
            a_atter = <built-in method driverText of QSqlError object at 0x7f84245a0350>
            isValid
            a_atter = <built-in method isValid of QSqlError object at 0x7f84245a0350>

            might be nice to shorten or declutter items

        """
        if  not self.include_dir:
            # self.line_list.append(  f"include_dir IS FALSE " )
            return

        #msg       = f"directory (non standard items) for object of type {type( a_obj ) = }"
        #msg       = f"directory (non standard items):"
        #rint( msg )

        the_dir         = self.inspect_me.__dir__()
        reduced_dir     = [ i_dir  for   i_dir in the_dir if i_dir not in common_dir_items ]
        reduced_dir.sort()
        current_str     = ""
        for i_dir in reduced_dir:

            # clean it up a bit ??
            #rint( i_dir )
            a_atter     =   getattr( self.inspect_me, i_dir, None )
            # if a_atter.startswith( "<built-in method" ):
            #     a_atter  = "method"
            # if a_atter.startswith( "<built-in method" ):
            #     a_atter  = "method"

            #rint( f"{i_dir= } .... {a_atter = }", flush = True )
            # to_columns( current_str, item_list, format_list = ( "{: <30}", "{:<30}" ), indent = "    "  ):

            current_str = to_columns(  [ str( i_dir ), str( a_atter) ] )
            self.add_line( current_str )

    # -----------------------
    def add_line( self, i_line ):
        """
        this is info for all
        """
        self.line_list.append( i_line )

    # ------------------------------
    def begin_info( self ):
        """
        this is info for all
        """
        #self.add_line(  "so it begins" )
        self.add_line( f"object is instance of {self.my_class} and type {type( self.inspect_me)}" )

        a_srep      = short_str( self.inspect_me )
        self.add_line( f">>>>>>>>>>{self.xin}{INDENT}>{a_srep}<" )
        #a_str   = f"{xin}{a_str}for msg = {msg} object isinstance of Sequence"
        #self.add_line(   "end of begin " )
        # a_srep  = short_str( a_obj )
        # a_str   = f"{a_str}\n{xin}{INDENT}>{a_srep}<"

        # a_str   = f"{a_str}\n{xin}{INDENT2}type is = { str( type(a_obj) ) }"
        # #a_str   = f"{a_str}\n{xin}{INDENT2}str     = {str( a_obj )}"
        # a_repr  = short_repr( a_obj )
        # a_str   = f"{a_str}\n{xin}{INDENT2}repr    = {a_repr}"

    #-------------------------
    def mid_info( self ):
        """
        this is info for all -- seems to all hav emove to begin.
        """
        #self.add_line(  "so it begins" )
        #self.add_line( f"object is of type {type( self.inspect_me)}" )
        #a_str   = f"{xin}{a_str}for msg = {msg} object isinstance of Sequence"
        #self.add_line(   "" )

    #-------------------------
    def custom_info( self ):
        """
        this should be custom
        """
        self.add_line( f"{self.xin}{INDENT2}custom_info from info about base to be done " )
        #self.add_line( f"object is an instance of {type( self.inspect_me)}" )
        #a_str   = f"{xin}{a_str}for msg = {msg} object isinstance of Sequence"
        #self.add_line(   "" )

    # ------------------------
    def fix_msg( self ):
        """ """
        if self.msg is None:
            #self.msg  = default_msg( my_type_str )
            self.msg    = f"{MSG_PREFIX}for instance of  {type( self.inspect_me )}"

        else:
            self.msg    = f"{MSG_PREFIX}{self.msg} "

    # ------------------------
    def return_info( self ):
        """ """
        info       = "\n".join( self.line_list )


if IN_SPECT_OBJ is None:
    IN_SPECT_OBJ = InSpectObj()


# ---- eof
