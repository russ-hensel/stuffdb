#!/bin/bash

# theprofm_bku_here_to_l.sh
# for the professor running mint
#      backup this dir and subs
#      to the correct place on
#      the "L"" drive
#
#      fror now send as arguments the current dir and
#      a code for the backup destination
#
move this to a dir where it can run why not clipboard


echo "The script you are running has:"
echo "basename: [$(basename "$0")]"
echo "dirname : [$(dirname "$0")]"
echo "pwd     : [$(pwd)]"


# Python in a conda environment

echo "Run backup...theprofm_bku_her_to_l.sh"

# Activate conda environment
source /home/russ/anaconda3/etc/profile.d/conda.sh
conda activate py_10

echo "Script executed from (pwd): ${PWD}"

SOURCE_DIR=$(pwd)
#echo $SOURCE_DIR

#echo "Source Dir: SOURCE_DIR ${SOURCE_DIR}"

BASEDIR=$(dirname $0)
echo "Script location basedir: ${BASEDIR}"


# Run the Python program
#python /mnt/WIN_D/Russ/0000/python00/python3/_projects/backup/call_backup_here_to_l.py  $SOURCE_DIR  to_l_data_for_mint
#python /mnt/WIN_D/Russ/0000/python00/python3/_projects/backup/backup_for_linux.py  $SOURCE_DIR  to_l_data_for_mint
# python /mnt/WIN_D/Russ/0000/python00/python3/_projects/backup/backup_for_linux.py  $SOURCE_DIR  usb_lsg_smallcase
# getting error on pwd   = \ try this july 2024
python /mnt/WIN_D/Russ/0000/python00/python3/_projects/backup/backup_for_linux.py  $BASEDIR  usb_lsg_smallcase


# Deactivate the conda environment
conda deactivate

# here just wait for a keystroke ( or comment out )
read RESPONSE


