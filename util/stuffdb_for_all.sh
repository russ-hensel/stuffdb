#!/bin/bash


echo "Run stuffdb all machines with env var set "
echo "  "
echo "The script you are running has:"
echo "basename: [$(basename "$0")]"
echo "dirname : [$(dirname "$0")]"
echo "pwd     : [$(pwd)]"

# Activate uv environment
#source  $PYTHON_VENV/py_13/bin/activate
source              $PYTHON_VENV/py3_13_qt6/bin/activate

#source  /home/russ/python_uv_venv/py3_13_qt6/bin/activate



echo  "Which Python:"
which   python
echo  "end which Python:"

# Run the Python program


# python /mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/backup/backup_for_linux.py $SOURCE_DIR   kingholmer_backup_on_k
#python /mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/backup_qt/from_sh.py   $SOURCE_DIR   kingholmer_backup_on_k


# next is for debugging
#export QT_DEBUG_PLUGINS=1


cd         $PYTHON_PROJECTS/stuffdb
echo       $PYTHON_PROJECTS/stuffdb
python     main.py


# here just wait   ( or comment out )
echo "enter to exit"
read RESPONSE

# Keep an interactive shell running
#exec bash
