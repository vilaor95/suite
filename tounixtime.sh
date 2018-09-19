#!/bin/bash

OLDIFS=$IFS
IFS=$'\n'
cat $1 | while read line
do
    UTC=$(echo $line | awk -F, '{print $1}')
    UNIXTIME=$(date -d $UTC "+%s")
    if [ $? -eq 1 ] 
    then
        echo $line >> temp
    fi
    echo $line | sed "s/$UTC/$UNIXTIME/" >> temp
done

mv temp $1
IFS=$OLDIFS
