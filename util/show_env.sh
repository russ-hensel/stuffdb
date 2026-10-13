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



echo       my env:
echo       PYTHON_PROJECTS       $PYTHON_PROJECTS
echo       PYTHON_VENV           $PYTHON_VENV
echo       GITHUB_DIR            $GITHUB_DIR




# here just wait   ( or comment out )
echo "enter to exit"
read RESPONSE
