#!/bin/bash

# add the data directory at the beginning and .zip at the end
archive_name="data/$1.zip"

# unpack the file into a folder named after the argument
unzip "$archive_name" -d "data/$1/"

# remove all files that do not have the crx.gz extension
for file in $(ls "data/$1" | grep -v "\.crx\.gz"); do
  rm -f "data/$1/$file"
done

# unpack files with the crx.gz extension
for file in $(ls "data/$1" | grep "\.crx\.gz"); do
  gunzip "data/$1/$file"
done
