#!/bin/bash

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

    systemctl daemon-reload

    echo "All unit files starting with 'station_@' and ending with '$_.service' have been deleted from /etc/systemd/system/ directory."
fi
