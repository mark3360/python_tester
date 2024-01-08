#!/bin/bash

cd testing_directory

OIFS="$IFS"
IFS=$'\n'

for file in `find . -type f -name "*.py"`
do
	cat ../testing_template.txt >> $file	

done
