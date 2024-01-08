#!/bin/bash

assignment=A5
dir=testing_directory
cd $dir


OIFS="$IFS"
IFS=$'\n'

for file in `find . -type f -name "*.py"`
do	
	cp ../datafiles/${assignment}/* .
	
	echo "Marking File" $file;
	python $file > /dev/null
done
