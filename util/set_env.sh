#!/bin/bash


echo "Run stuffdb all machines with env var set "
echo "  "
echo "The script you are running has:"
echo "basename: [$(basename "$0")]"
echo "dirname : [$(dirname "$0")]"
echo "pwd     : [$(pwd)]"

# Activate uv spyder qt5 environment
source  $PYTHON_VENV/py_13/bin/activate
which   python


echo "SET THE ENV -- ARE YOU SURE enter to CONTINUE"
read RESPONSE

cd         $PYTHON_PROJECTS/stuffdb

# ======== kingholmer values ========

#export PYTHON_VENV="/home/russ/python_uv_venv"
#export PYTHON_PROJECTS="/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects"
#export GITHUB_DIR="/mnt/m_toshiba_silver/for_github"

# ======== jeff values ========

#export PYTHON_VENV="/home/russ/python_uv_venv"
#export PYTHON_PROJECTS="/media/russ/d_hard_drive/russ/0000/python00/python3/_projects"
#export GITHUB_DIR="not implemented"


# ======== # millhouse values ========

#export PYTHON_VENV="/home/russ/python_uv_venv"
#export PYTHON_PROJECTS="/home/russ/sync_on_fattony/russ/0000/python00/python3/_projects"
#export GITHUB_DIR=""
#

# ======== fattony values ========

export PYTHON_VENV="/home/russ/python_uv_venv"
export PYTHON_PROJECTS="/media/russ/m_toshiba_silver/sync_on_fattony/russ/0000/python00/python3/_projects"
 


#cd         $PYTHON_PROJECTS/stuffdb

echo       my env:
echo       PYTHON_PROJECTS       $PYTHON_PROJECTS
echo       PYTHON_VENV           $PYTHON_VENV
echo       GITHUB_DIR            $GITHUB_DIR



# here just wait   ( or comment out )
echo "enter to exit"
read RESPONSE



