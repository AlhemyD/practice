#!/bin/bash

files=$(ls /etc/systemd/system/station_@*.service)

if [ -z "$files" ]; then
    echo "No unit files starting with 'station_@' and ending with 'service' were found in /etc/systemd/system/ directory."
else
    for file in $files; do
        rm $file
    done

    systemctl daemon-reload

    echo "All unit files starting with 'station_@' and ending with 'service' have been deleted from /etc/systemd/system/ directory."
fi
