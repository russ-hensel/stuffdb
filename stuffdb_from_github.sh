#!/bin/bash

# Run python in a conda environment
# Print Hello message
echo "Run .... with python in a uv environment"

# Activate environment
cd           $PYTHON_VENV
source       py_13_qt6/bin/activate
which        python
read         RESPONSE

# Navigate to the directory with main.py -- think is env var for this
#cd /mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb
cd /mnt/m_toshiba_silver/for_github/stuffdb

# Run the Python program -- with mode argument
#python main.py  mode_github_example_code_on_theprof
python main.py  mode_github
# Deactivate the conda environment


# here just wait for a keystroke ( or comment out )
echo "Enter to continue to exit"
read RESPONSE
