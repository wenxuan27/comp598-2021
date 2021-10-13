#!/bin/bash

# set the input file path into the variable input
input=$1

# count the number of lines 
count_lines=$(< $input wc -l) 

if [ $count_lines -lt 10000 ]
    then
    >&2 echo "Error: The input file needs to contain at least 10,000 lines but you only have ${count_lines}"
else
    # print out the number of lines 
    echo "$count_lines"

    # read and print out the first line
    read -r line < "$input"
    echo "$line"

    # # get the last 10000 lines and then pipe it into grep to pattern match "potus"
    tail -n 10000 $1 | grep -ic "potus"

    # # get the lines between 100 and 200 (inclusively and pipe it into grep to pattern match "fake")
    sed -n '100,200p' $1 | grep -c "(?<![a-zA-Z0-9])fake(?![a-zA-Z0-9])"
fi


