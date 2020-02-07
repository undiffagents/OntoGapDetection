#!/bin/bash

input=ACE_in.txt
tmp=tmp_DRS.txt
output=DRS.txt
output2=RULES.txt

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

<<<<<<< HEAD
letters=()
names=()
rm -f $output2
fact=false
letter=' '
while IFS= read -r line
do
  if [[ $line == *" "* ]] && $fact; then
	line="$(echo -e "${line}" | sed -e 's/^[[:space:]]*//')"
  fi

  if [[ $line == *"predicate("* ]]; then
	var1="$(echo -e ${line} | cut -f 3 -d ',' | cut -f 1 -d ',')"
	var2="$(echo -e ${line} | cut -f 4 -d ',' | cut -f 1 -d ')')"
	if [[ $var1 == *"named("* ]] || [[ $var1 == *"string("* ]] && [[ $var2 == $letter ]]; then
		name="$(echo -e ${var1} | cut -f 2 -d '('| cut -f 1 -d ')')"
		outval="${outval}(${name})"
		echo $outval >> $output2
		outval=""
		letters+=($letter)
		names+=($name)
	elif $fact; then
		name=$outval
		outval="${outval}(${name})"
		echo $outval >> $output2
		outval=""
		letters+=($letter)
		names+=($name)
	else
		echo ""
	fi
	
  fi

  if [[ $line == *"object("* ]]; then
	outval="$(echo -e ${line} | cut -f 2 -d ',')"
	letter=${line:7:1}
	fact=true
	continue
  fi

done < "$output"

for i in "${letters[@]}"
do
	echo $i
done 
for i in "${names[@]}"
do
	echo $i
done 
=======
python3 DRS_to_Rules.py
>>>>>>> e56b28db80ddb34cd814a6faead0b8ae9ff6d61b