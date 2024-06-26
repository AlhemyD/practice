#!/bin/bash

user=$(logname)

unit_name="fastapi_@scriprnx.service"

if [[ -f /etc/systemd/system/$unit_name ]]; then
    if ! systemctl is-active --quiet $unit_name; then
        systemctl start $unit_name
    fi

else
    cp /home/$user/practice/src/all_services/fastapi_@.service /etc/systemd/system/$unit_name
    sed -i "s/%user/$user/g" /etc/systemd/system/$unit_name
    systemctl daemon-reload
    systemctl enable $unit_name
    systemctl start $unit_name
fi