#!/bin/bash

# Run python in a conda environment
# Print Hello message
echo "Run idle with python in a conda environment"

# Activate conda environment
source /home/russ/anaconda3/etc/profile.d/conda.sh
conda activate py_12_misc

#activate myenv
python  -m idlelib  temp_stuff.py

# Deactivate the conda environment -- process my die so so what
conda deactivate

# here just wait for a keystroke ( or comment out )
read RESPONSE