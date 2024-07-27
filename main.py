# -*- coding: utf-8 -*-
"""



"""
from   pathlib import Path
import sys

# sys.path.append( r"D:\Russ\0000\python00\python3\_projects\rshlib"  )
# sys.path.append( "../")
sys.path.insert( 1, "../rshlib" )
sys.path.insert( 1, "./ex_qt" )
sys.path.insert( 1, ".//mnt/WIN_D/Russ/0000/python00/python3/_examples/" )
sys.path.insert( 1, ".//mnt/WIN_D/Russ/0000/python00/python3/_examples/qt" )

# see comment in web_search.py
#sys.path.append( "/media/russ/j_sg_bigcase/sync_py_3/_projects/rshlib/" )


# import  run_stuff_db


def main( ):
    import stuffdb_qt
    stuffdb_qt.main()

# --------------------
if __name__ == "__main__":
    # #----- run the full app
    main( )

# =================== eof ==============================


