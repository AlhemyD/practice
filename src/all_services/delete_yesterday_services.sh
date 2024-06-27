#!/bin/bash

user=$(logname)

if [ $# -eq 0 ]; then
    echo "Please provide a date as an argument."
    exit 1
fi

date=$1
files=$(ls /etc/systemd/system/station_*"$date".service)

if [ -z "$files" ]; then
    echo "No unit files starting with 'station_@' and ending with '$date_.service' were found in /etc/systemd/system/ directory."
else
    for file in $files; do
        rm "$file"
    done
    systemctl stop $file

    systemctl daemon-reload

    echo "All unit files starting with 'station_@' and ending with '$_.service' have been deleted from /etc/systemd/system/ directory."
fi

stations_dir="/home/$user/practice/data/$1"

if [[ ! -e "$stations_dir" ]]; then
    echo "This directory $stations_dir doesn't exist."
else
    if [ -z "$(ls -A "$stations_dir")" ]; then
        echo "The directory $stations_dir is empty."
    else
        rm -f "$stations_dir"/*
        rmdir "$stations_dir"
        echo "All files and the folder $stations_dir have been deleted."
    fi
fi
