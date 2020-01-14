#!/bin/bash

input=ACE_in.txt
tmp=tmp_DRS.txt
output=DRS.txt

./APE/ape.exe -file $input -cdrspp > $tmp

rm -f $output
started=false
while IFS= read -r line
do
  if [[ $line == *"  <drspp>"* ]]; then
	echo "$(echo "$line" | cut -c10-99)" >> $output
	started=true
	continue
  fi
  if [[ $line == *"["* ]]; then	
	echo "$line" >> $output
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
done < "$tmp"

rm -f $tmp

python3 DRS_to_Rules.py
