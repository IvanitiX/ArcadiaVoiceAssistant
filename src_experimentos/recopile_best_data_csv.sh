#!/bin/bash

FILES="$1"
cd $FILES

for f in *
do
  # take action on each file. $f store current file name
  DATA=$(cat "$f" | tail -2 | head -1)
  str="$f $DATA"
  str_trimmed=${str//\t/}
  str_filter1=${str/Mejor combinación:/}
  str_filter2=${str_filter1/.csv/}
  str_filter3=${str_filter2/Alpha:/}
  str_filter4=${str_filter3/Beta :/}
  str_filter5=${str_filter4/CER :/ }
  str_format=${str_filter5//\// }
  echo "${str_format//./,}"
done
