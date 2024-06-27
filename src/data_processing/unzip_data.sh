#!/bin/bash

user=$(logname)

# add the data directory at the beginning and .zip at the end
if [ -d "/home/$user/practice/data" ]; then
    archive_name="/home/$user/practice/data/$1.zip"
    pattern="/home/$user/practice/data/$1"
else
    archive_name="/home/$user/src/practice/data/$1.zip"
    pattern="/home/$user/src/practice/data/$1"
fi


# unpack the file into a folder named after the argument
unzip "$archive_name" -d "$pattern"

# unpack files from this directory
for file in $(ls "$pattern"); do
  gunzip "$pattern/$file"
done

rm "$archive_name"
