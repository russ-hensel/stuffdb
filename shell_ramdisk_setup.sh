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
# move this to a dir where it can run why not clipboard


# echo "The script you are running has:"
# echo "basename: [$(basename "$0")]"
# echo "dirname : [$(dirname "$0")]"
# echo "pwd     : [$(pwd)]"


# Python in a conda environment

echo "Run to setup stuffdb on ramdisk"



echo "Script executed from (pwd): ${PWD}"

SOURCE_DIR=$(pwd)
#echo $SOURCE_DIR

#echo "Source Dir: SOURCE_DIR ${SOURCE_DIR}"

BASEDIR=$(dirname $0)
echo "Script location basedir: ${BASEDIR}"


sudo mkdir /tmp/ramdisk #
sudo chmod 777 /tmp/ramdisk # all users can use
sudo mount -t tmpfs -o size=3G myramdisk /tmp/ramdisk #
# >> sudo mount -t tmpfs -o size=5G myramdisk /tmp/ramdisk # nG for the RAM disk,
mount | tail -n 1 # to see if it is mounted
cp /mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/data/*.db  /tmp/ramdisk/
cp /mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/data/russ/aug.* /tmp/ramdisk/




# here just wait for a keystroke ( or comment out )

echo "Done press <enter> to exit script"
read RESPONSE
