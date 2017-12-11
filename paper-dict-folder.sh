#!/bin/bash
 
# Purpose:
#   Convert all pdf-files in one directory
#
# Instructions:
#   provide your <directory path> and assign it to `dirpath`
#

if [ $# != 1 ] ; then 
	echo "Please input folder"; 
	exit 1 ; 
fi

dirpath=${1}
for i in ${dirpath}/*.pdf; do
	f=`echo ${i} | sed 's,.*/,,'`
    echo "paper-dict(ing) ${f}"
    python3 -B paper-dict.py -i "${i}" -o "paper-dict-${f}" 
done