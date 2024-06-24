#!/bin/bash

# add the data directory at the beginning and .zip at the end
archive_name="../../data/$1.zip"

# unpack the file into a folder named after the argument
unzip "$archive_name" -d "../../data/$1"

# unpack files from this directory
for file in $(ls "../../data/$1"); do
  gunzip "../../data/$1/$file"
done
