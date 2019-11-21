#!/bin/bash

input=ACE_in.txt
tmp=tmp_DRS.txt
output=DRS.txt
vars=()

varsAppend () {
 for (( i=0; i<${#tmp1}; i++ )); do
   char="${tmp1:$i:1}"
   if [ "$char" == "[" ] || [ "$char" == "]" ] || [ "$char" == "," ]; then
    continue
   fi 
  vars=("${vars[@]}" "$char")
  done
  return 0
}

./APE/ape.exe -file $input -cdrspp > $tmp

rm -f $output
started=false
while IFS= read -r line
do
  if [[ $line == *"  <drspp>"* ]]; then
	tmp1=$(echo "$line" | cut -c10-99)
	varsAppend	
	echo "$tmp1" >> $output
	started=true
	continue
  fi
  if [[ $line == *"["* ]]; then
	tmp1="$line"
	varsAppend	
	echo "$tmp1" >> $output
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
