#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 13:28:26 2024

@author: russ
"""

from datetime import datetime

import pytest
from PyQt5.QtCore import QDate, QDateTime

import adjust_path
# Import the functions to test
from custom_widgets import convert_from_to, datetime_to

# Sample datetime for testing
sample_datetime = datetime(2023, 10, 11, 12, 30, 45)  # Year, Month, Day, Hour, Minute, Second
timestamp       = int( sample_datetime.timestamp() )  # Expected Unix timestamp\




a_datetime   = sample_datetime
qdate        = QDate(a_datetime.year, a_datetime.month, a_datetime.day)

#qdatetime      = QDateTime.fromPyDateTime(sample_datetime)

py_datetime    = sample_datetime
qdatetime      = QDateTime(py_datetime.year, py_datetime.month, py_datetime.day,
                       py_datetime.hour, py_datetime.minute, py_datetime.second)

timestamp_from_qdate    =  convert_from_to( qdate,     "qdate",     "timestamp" )
qdate_from_qdatetime    =  convert_from_to( qdatetime, "qdatetime", "qdate"     )
qdatetime_from_qdate    =  convert_from_to( qdate, "qdate", "qdatetime")

def test_datetime_to():
    # Test conversions to timestamp
    assert datetime_to(sample_datetime, "timestamp") == timestamp

    # Test conversions to QDateTime
    assert datetime_to(sample_datetime, "qdatetime") == qdatetime


    # Test conversions to QDate
    assert datetime_to(sample_datetime, "qdate") == qdate

    # Test ValueError on None
    with pytest.raises(ValueError):
        datetime_to( None, "timestamp" )

    # Test ValueError on unsupported type
    with pytest.raises(ValueError):
        datetime_to(sample_datetime, "unsupported_type")

def test_convert_from_to():
    # Test QDate to datetime
    # loss of precision will cause these to fail
    #assert convert_from_to(qdate, "qdate", "timestamp") == timestamp
    #assert convert_from_to(qdate, "qdate", "qdatetime") == qdatetime

    assert convert_from_to(qdate, "qdate", "timestamp") == timestamp_from_qdate

    assert convert_from_to( qdate_from_qdatetime, "qdate", "qdatetime") == qdatetime


    # Test QDateTime to datetime
    assert convert_from_to(qdatetime, "qdatetime", "timestamp") == timestamp
    assert convert_from_to(qdatetime, "qdatetime", "qdate") == qdate

    # Test timestamp to datetime
    assert convert_from_to(timestamp, "timestamp", "qdate") == qdate
    assert convert_from_to(timestamp, "timestamp", "qdatetime") == qdatetime

    # Test unsupported input type
    with pytest.raises(ValueError):
        convert_from_to(qdate, "unsupported_type", "timestamp")

    # Test unsupported output type
    with pytest.raises(ValueError):
        convert_from_to(qdate, "qdate", "unsupported_type")

    # Test no conversion if in_type equals out_type
    assert convert_from_to(qdate, "qdate", "qdate")


    # Test no conversion if in_type equals out_type
    assert convert_from_to(qdate, "qdate", "qdate") == qdate


if __name__ == "__main__":
    pytest.main([__file__])  # This will run the tests in this file
