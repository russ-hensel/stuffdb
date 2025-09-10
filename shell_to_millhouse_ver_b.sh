

echo "The script is to copy files for qt_widget_by_example to its github location on my drive :"


cd  /mnt/WIN_D/Russ/0000/python00/python3/_projects/qt_by_example/

#cp  qt_sql_widgets.py   /mnt/WIN_D/for_github/qt_by_example/   -f
#
#/mnt/WIN_D/Russ/0000/python00/python3/_projects/qt_by_example/qt_sql_widgets.py
#
#
#/mnt/WIN_D/for_github/qt_by_example/test_target

#


ls
echo "hit any key to continue... "
read RESPONSE



# ------------------ stuffdb  --------------------------
SOURCE_BASE="/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb"
TARGET_BASE="/mnt/millhouse/rsync/_projects/stuffdb"

#rsync -u -t --progress \
#  /mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/*.* \
#                                            "$TARGET_BASE"

rsync -u -t --progress          "$SOURCE_BASE"/*.*  \
                                "$TARGET_BASE"

rsync -u -t --progress          "$SOURCE_BASE"/docs/*.*  \
                                "$TARGET_BASE"/docs

# ---------------------------

rsync -u -t --progress          "$SOURCE_BASE"/qt_tabs/*.*  \
                                "$TARGET_BASE"/qt_tabs

rsync -u -t --progress          "$SOURCE_BASE"/sql/*.*  \
                                "$TARGET_BASE"/sql

rsync -u -t --progress          "$SOURCE_BASE"/misc/*.*  \
                                "$TARGET_BASE"/misc

rsync -u -t --progress          "$SOURCE_BASE"/data_dict_src/*.*  \
                                "$TARGET_BASE"/data_dict_src


rsync -u -t --progress          "$SOURCE_BASE"/py_helpers/*.*  \
                                "$TARGET_BASE"/qt_tabs

rsync -u -t --progress          "$SOURCE_BASE"/qt_tabs/*.*  \
                                "$TARGET_BASE"/qt_tabs

rsync -u -t --progress          "$SOURCE_BASE"/data/*.*  \
                                "$TARGET_BASE"/data


 rsync -u -t --progress         "$SOURCE_BASE"//data/russ2025/*.*  \
                                "$TARGET_BASE"//data/russ2025



#-------------


# ------------------ rshlib --------------------------
TARGET_BASE="/mnt/millhouse/rsync/_projects/rshlib"
SOURCE_BASE="/mnt/WIN_D/russ/0000/python00/python3/_projects/rshlib"
#-------------------------


#rsync -u -t --progress \
#  /mnt/WIN_D/russ/0000/python00/python3/_projects/rshlib/*.* \
                                           "$TARGET_BASE/"

rsync -u -t --progress          "$SOURCE_BASE"/*.*  \
                                "$TARGET_BASE"/

rsync -u -t --progress \       "$SOURCE_BASE"/rshlib_qt/*.*  \
                               "$TARGET_BASE"/rshlib_qt

rsync -u -t --progress \       "$SOURCE_BASE"/in_spect/*.*  \
                               "$TARGET_BASE"/in_spect


rsync -u -t --progress \       "$SOURCE_BASE"/in_spect/*.*  \
                               "$TARGET_BASE"/in_spect

rsync -u -t --progress \       "$SOURCE_BASE"/app_services/*.*  \
                               "$TARGET_BASE"/app_services

rsync -u -t --progress \       "$SOURCE_BASE"/os_call/*.*  \
                               "$TARGET_BASE"/os_call

rsync -u -t --progress \       "$SOURCE_BASE"/in_spect/*.*  \
                               "$TARGET_BASE"/in_spect

rsync -u -t --progress \       "$SOURCE_BASE"/in_spect/*.*  \
                               "$TARGET_BASE"/in_spect



# ---------------------





# here just wait for a keystroke ( or comment out )
echo "hit <enter> to continue and exit "
read RESPONSE


# --------------------- eof
