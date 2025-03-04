#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
Created on Thu Jan 23 08:36:02 2025

@author: russ
"""


# ---- imports
#from   collections.abc import Sequence
import collections
import time

# ---- end imports


#-------------------------------


# ----------------------------------------
class CodeTimer():
    """
    Purpose:
        Time code, particularly for comparisons
        report ratios
        !! consider a calibrate for empty start stop
        !! what about time clock
    Example use:

        import ex_helpers
        a_code_timer = ex_helpers.CodeTimer()
        a_code_timer.start( msg = "what are we testing?"  )
        # something
        a_code_timer.stop()

        # repeat

        a_code_timer.report()

    """
    def __init__( self, ):
        self.Timed      = collections.namedtuple( "Timed", "msg  timing" )
        self.perf_end   = None
        self.time_end   = None
        self.reset()

    # ----------------------------------------
    def reset( self,  ):
        """
        Purpose:
            call to reset history and anything else needed
            for reuse of object
        Return:
            mutates self
        """
        self.records      = []

    # ----------------------------------------
    def start( self, msg = None ):
        """
        Purpose:
            call to start timing
        Args:
            msg       message associated with this timing
        Return:
            mutates self
        """
        self.msg          = msg
        self.time_start   = time.time()
        self.perf_start   = time.perf_counter()
        self.time_end     = self.time_start

        self.perf_end     = self.perf_start

    # ----------------------------------------
    def stop( self, rpt = True ):
        """
        Purpose:
            call at end of timing
        Args:
            rpt      if true prints a little report on the timing
        Return:
            mutates self
        """
        self.time_end   = time.time()
        self.perf_end   = time.perf_counter()

        perf_elapsed    = self.perf_end - self.perf_start

        a_record        = self.Timed( msg = self.msg,  timing =  perf_elapsed )

        self.records.append( a_record )

        if rpt:
            self._report_stop( )

    # ----------------------------------------
    def _report_stop( self, ):
        """
        Purpose:
            call after end of timing -- on stop
            print a report of that timing
        Return:
            prints output
        """
        print( f"Stop: {self.msg}" )

        # msg   = ( f"    by time:         {self.time_end - self.time_start} seconds" )
        # print( msg )

        msg   = ( f"    by perf_counter: {self.perf_end - self.perf_start} seconds" )
        print( msg )

    # ----------------------------------------
    def report( self,   ):
        """
        Purpose:
            call after set of timings for relative timings
            prints a report
        Return:
            prints output
        """
        print( "\nRelative Timings:")
        # make base timing the last one
        base_timing    = self.records[ -1 ].timing

        #base_timing = None
        for a_record in self.records:
            a_msg       = a_record.msg
            a_timing    = a_record.timing
            # if base_timing is None:
            #     # will happen on first timing
            #     base_timing = a_timing

            #timing_msg   =  f"{a_msg}  perf_time = {a_timing} relative time = {relative_timing}"
            relative_timing  = a_timing / base_timing
            # need better formatting
            timing_msg   =  f"{a_msg}\n    perf_time = {a_timing} relative time = {relative_timing}"
            print( timing_msg )





# ---- eof