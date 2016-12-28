#!/bin/bash
 
# Purpose:
#   Convert all pdf-files in one directory
#
# Instructions:
#   provide your <directory path> and assign it to `dirpath`
#
dirpath=<directory path>
for i in ${dirpath}/*.pdf; do
  filename="pdf2words-$(basename -s .pdf $(echo ${i} | tr -d " ")).txt"
  ./pdf2words -i ${i} > ${dirpath}/${filename}
done 
