#!/bin/sh

ls 20* | xargs -n 1 tail -n +2 > all.txt
echo `head -n 1 2010-05-30.txt` > headertmp.txt
awk -v OFS="\t" '$1=$1' headertmp.txt > header.txt 
cat header.txt all.txt > allh.txt
rm headertmp.txt header.txt
