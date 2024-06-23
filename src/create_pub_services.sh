#!/bin/bash

data_dir="/home/$(whoami)/practice/src/download_and_unzip/data/$1"
temp = "/etc/systemd/system/station_@.service"

# Перебираем файлы по дате в директории data
for file in $(ls -t $data_dir); do
    file_path="$data_dir/$file"
    unit_name="station_@$file.service"

    # Проверяем, есть ли юнит файл для данного файла
    if [[ -f /etc/systemd/system/$unit_name ]]; then
        # Если демон не запущен, то запускаем его
        if ! systemctl is-active --quiet $unit_name; then
            systemctl start $unit_name
        fi
    else
        # Создаем новый юнит файл для данного файла
        cp /etc/systemd/system/station_@.service /etc/systemd/system/$unit_name
        sed -i "s/%I/$file/g" /etc/systemd/system/$unit_name
        systemctl daemon-reload
        systemctl start $unit_name
    fi
done
