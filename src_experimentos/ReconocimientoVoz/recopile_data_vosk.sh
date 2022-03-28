#!/bin/bash

FILES="$1"
cd $FILES

for f in *
do
  # take action on each file. $f store current file name
  DATA=$(tr --delete '\n' < "$f")
  str="$f $DATA"
  str_filter1=${str/WER = /}
  str_filter2=${str_filter1/CER = / }
  str_format=${str_filter2/_Vosk.txt/  }
  echo "${str_format//./,}"
done
