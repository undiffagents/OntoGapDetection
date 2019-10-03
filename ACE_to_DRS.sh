#!/bin/bash

./APE/ape.exe -file ACE_in.txt -cdrspp > tmp_DRS.txt

input="tmp_DRS.txt"
output=DRS.txt
rm -f $output
started=false
while IFS= read -r line
do
  if [[ $line == *"  <drspp>"* ]]; then
	echo $line | cut -c8-99 >> $output
	started=true
	continue
  fi
  if [[ $line == *"</drspp>"* ]]; then
	break
  fi
  if [[ $line == *"   =&gt;"* ]]; then
	line="   =>"
  fi
  if $started; then 
	echo "$line" >> $output
  fi
done < "$input"
