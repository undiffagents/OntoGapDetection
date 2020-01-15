#!/bin/bash

input=ACE_in.txt
tmp=tmp_DRS.txt
output=DRS.txt

./APE/ape.exe -file $input -cdrspp > $tmp

rm -f $output
started=false
while IFS= read -r line
do

  if [[ $started ]] && [[ $line == *"</drspp>"* ]]; then
	break
  elif [[ $started == false ]] && [[ $line == *"  <drspp>"* ]]; then
	line="$(echo "$line" | cut -c10-99)"
	started=true
  elif [[ $started ]] && [[ $line == *"   =&gt;"* ]]; then
	line="   =>"
  fi

  if $started; then 
	echo "$line" >> $output
  fi

done < "$tmp"


rm -f $tmp

python3 DRS_to_Rules.py
