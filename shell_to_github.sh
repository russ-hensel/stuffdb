

echo "The script is to copy files for qt_widget_by_example to its github location on my drive :"


cd  /mnt/WIN_D/Russ/0000/python00/python3/_projects/qt_by_example/

#cp  qt_sql_widgets.py   /mnt/WIN_D/for_github/qt_by_example/   -f
#
#/mnt/WIN_D/Russ/0000/python00/python3/_projects/qt_by_example/qt_sql_widgets.py
#
#
#/mnt/WIN_D/for_github/qt_by_example/test_target

# still need all of docs



ls
echo "hit any key to continue... "
read RESPONSE
#/mnt/WIN_D/for_github/stuffdb
rsync -u -t -progress       /mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/*.*                   /mnt/WIN_D/for_github/stuffdb
rsync -u -t -progress       /mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/docs/*.*              /mnt/WIN_D/for_github/stuffdb/docs
rsync -u -t -progress       /mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/qt_tabs/*.*           /mnt/WIN_D/for_github/stuffdb/qt_tabs
rsync -u -t -progress       /mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/misc/*.*              /mnt/WIN_D/for_github/stuffdb/misc
rsync -u -t -progress       /mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/sql/*.*               /mnt/WIN_D/for_github/stuffdb/sql
rsync -u -t -progress       /mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/data_dict_src/*.*     /mnt/WIN_D/for_github/stuffdb/data_dict_src

rsync -u -t -progress       /mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/data/python_ex.db     /mnt/WIN_D/for_github/stuffdb/data


 


# to libs ----------------------------------------------
rsync -u -t -progress       /mnt/WIN_D/russ/0000/python00/python3/_projects/rshlib/rshlib_qt/*.*        /mnt/WIN_D/for_github/stuffdb/libs

rsync -u -t -progress       /mnt/WIN_D/russ/0000/python00/python3/_projects/rshlib/in_spect/*.*         /mnt/WIN_D/for_github/stuffdb/libs
rsync -u -t -progress       /mnt/WIN_D/russ/0000/python00/python3/_projects/rshlib/app_services/*.*     /mnt/WIN_D/for_github/stuffdb/libs



rsync -u -t -progress       /mnt/WIN_D/russ/0000/python00/python3/_projects/rshlib/string_util.py     /mnt/WIN_D/for_github/stuffdb/libs
rsync -u -t -progress       /mnt/WIN_D/russ/0000/python00/python3/_projects/rshlib/os_call.py         /mnt/WIN_D/for_github/stuffdb/libs


#rsync -u -t -progress       /mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/qsql_utils.py     /mnt/WIN_D/for_github/qt5_by_example/libs

#cp  theprofm_bku_here_to_l.sh     /mnt/WIN_D/for_github/qt_by_example/   -f
# cp  utils_for_tabs.py       /mnt/WIN_D/for_github/qt_by_example/   -f




# ---------------------





# here just wait for a keystroke ( or comment out )
echo "hit any key to continue and exit "
read RESPONSE


# --------------------- eof
