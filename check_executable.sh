#!/bin/bash

cd testing_directory

OIFS="$IFS"
IFS=$'\n'

for file in `find . -type f -name "*.py"`
do

	sed "/[\"\'].*csv.*[\"\']/d" $file > tmpfile
	cat tmpfile > $file
	rm tmpfile
		
	sed "/[\"\'].*CSV.*[\"\']/d" $file > tmpfile
	cat tmpfile > $file
	rm tmpfile

	sed "s/10000/10/" $file > tmpfile
	cat tmpfile > $file
	rm tmpfile 

	# Attempt to execute the Python File as is
	python $file
	x=$?
	if [ $x -ne 0 ]; then
		echo $file " is unexecutable";
		cat ../unexecutable.py > $file
	#else
	#	rm $file
	fi

done
