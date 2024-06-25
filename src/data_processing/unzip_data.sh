#!/bin/bash

user=$(logname)

# add the data directory at the beginning and .zip at the end
archive_name="/home/$user/practice/data/$1/$1.zip"

# unpack the file into a folder named after the argument
unzip "$archive_name" -d "/home/$user/practice/data/$1"

# unpack files from this directory
for file in $(ls "/home/$user/practice/data/$1"); do
  gunzip "/home/$user/practice/data/$1/$file"
done

rm "$archive_name"
