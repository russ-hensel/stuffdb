#!/bin/bash


echo "Run stuffdb shell script"
echo "	this version is for the computer called KingHolmer  "
echo "The script you are running has:"
echo "basename: [$(basename "$0")]"
echo "dirname : [$(dirname "$0")]"
echo "pwd     : [$(pwd)]"


# Activate uv environment -- usual uv activate -- edit for your environment
source  /home/russ/python_uv_venv/py3_13_qt6/bin/activate
which   python   # report on python

# Run the Python program -- edit for your environment
cd         /mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/stuffdb
echo       /mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/stuffdb

# next should work on any computer
python     main.py


# here just wait  ( or comment out )
echo "enter to continue"
read RESPONSE
