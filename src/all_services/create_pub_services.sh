#!/bin/bash

user=$(logname)

data_dir="/home/$user/practice/data/$1"

# Перебираем файлы по дате в директории data
for file in $(ls -t $data_dir); do

    if [[ $file == *rnx ]]; then
        unit_name="station_@${file%%_*}_$1.service"
    elif [[ $file == *o ]]; then
        unit_name="station_@${file:0:4}_$1.service"
    fi

    # Проверяем, есть ли юнит файл для данного файла
    if [[ -f /etc/systemd/system/$unit_name ]]; then
        # Если демон не запущен, то запускаем его
        if ! systemctl is-active --quiet $unit_name; then
            systemctl start $unit_name
        fi
    else
        # Создаем новый юнит файл для данного файла
        cp /home/$user/practice/src/all_services/station_@.service /etc/systemd/system/$unit_name
        
	if [[ $file == *rnx ]]; then
            sed -i "s/%i/${file%%_*}/g" /etc/systemd/system/$unit_name
	elif [[ $file == *o ]]; then
            sed -i "s/%i/${file:0:4}/g" /etc/systemd/system/$unit_name
        fi

        sed -i "s/%date/$1/g" /etc/systemd/system/$unit_name
        sed -i "s/%user/$user/g" /etc/systemd/system/$unit_name
        systemctl daemon-reload
        systemctl enable $unit_name
        systemctl start $unit_name
    fi
done
