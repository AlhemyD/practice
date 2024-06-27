# Приложение по парсингу RINEX файлов #
## Выполнили Галиулина Оксана, Сисимирова Дарья, Пиякин Павел ##

Ссылка на используемый конвертатор в Rinex

`https://terras.gsi.go.jp/ja/crx2rnx.html` - Дата обращения: 19.06.2024

## Описание проекта ##
Данный проект представляет собой систему, разработанную для имитации потоков данных, получаемых с ГНСС (глобальной навигационной спутниковой системы) приемников в реальном времени. Наш проект имитирует процесс получения данных со спутника и направлению их к пользователю в режиме реального времени, то есть при наступлении определенного временного периода выводятся определенные данные, полученные со спутников.

## Общие этапы работы ##

1. Данные скачиваются, архив с ними распаковывается, после чего файлы конвертируются в другой формат.
2. Запускается демон, который будет держать файла для парсига данных запущенным
3. После запускаются демоны для публикации данных из каждого файла.
4. Пользователь может запустиь subscriber и посмотреть какие данные приходят для данного момента времени.

## Архитектура проекта ##
![Архитектура](project_scheme_drawio.svg)

## Установка ##
1. Скачайте репозиторий с помощью команды, выполнив ее в терминале, находясь в домашней директории:
``git clone https://github.com/AlhemyD/practice.git``
2. Затем перейти в папку проекта командой ``cd practice``
3. Установить командой ``python3 setup.py install``
   
## Использование ##
### 1. Отредактируйте crontab (? - УБРАТЬ): ###

Этот этап необходим для автоматического запуска всех нужных скриптов по определенному времени.

Cron – это планировщик задач. Если подробнее, то это утилита, позволяющая выполнять скрипты на сервере в назначенное время с заранее определенной периодичностью. Crontab – это таблица с расписанием запуска скриптов и программ, оформленная в специальном формате, который умеет считывать компьютер. Для каждого пользователя системы создается отдельный crontab-файл со своим расписанием. Эта встроенная в Linux утилита доступна на низком уровне в каждом дистрибутиве.


1.1 Откройте файл командой ``crontab -e``

1.2 Вставьте в конец файла строку ``0 0 * * * python3 /home/(имя вашего юзера)/practice/src/data_processing/main.py > /home/(имя вашего юзера)/output.log 2>&1``

### 1. Запустите main_starter.py

выполните команду вида 
`` python3 practice/src/data_processing/main_starter.py``
Пока этот файл запущен, каждый день в 22:00 будут скачиваться новые данные, а в 00:00 удаляться старые
   
### 2. Активируйте subscriber.py ###

2.1 Перейдите в папку командой ``cd practice/src/pub_sub/``

2.2 Запустите скрипт для получения данных от брокера командой ``python3 sub.py``

## Описание работы отдельных частей проекта: ##

## Работа с файлами ##

[**download.py**](https://github.com/AlhemyD/practice/blob/main/src/data_processing/download.py) отвечает за скачивание файлов. Скачивание файлов происходит в 22:00 по времени сервера, после наступления которого посылается запрос для получения данных по дате по ссылке "https://api.simurg.space/datafiles/map_files?date={date}", на место "{date}" встает дата, данные для которой получает приложение. Данные скачиваются в архив zip формата, название которого является текущей датой. После скачивания начинается процесс разархивации.

[**unzip_data.sh**](https://github.com/AlhemyD/practice/blob/main/src/data_processing/unzip_data.sh) отвечает за распаковку файлов. На вход подается дата, получаемая через main.py, после чего скрипт находит архив с названием дата.zip и начинает распаковку с помощью команды unzip, после данного процесса скрипт приступает к распаковке самих файлов, он проходится по архиву и с помощью команды gunzip разархивирует файлы. После этого удаляется архив и работа переходит к форматированию.

[**formatting.py**](https://github.com/AlhemyD/practice/blob/main/src/data_processing/formatting.py) отвечает за конвертацию файлов в другой формат. На вход данный скрипт получает путь к файлу crx или d, после чего проверяет существует ли такой файл, применяет команду ``../../lib/RNXCMP_4.1.0_Linux_x86_32bit/bin/CRX2RNX``  на выходе мы получаем сконвертированные в формат rnx или o файлы. 

[**parser.py**](https://github.com/AlhemyD/practice/blob/main/src/data_processing/parser.py) отвечает за парсинг файлов, используется в **scriprnx.py**. На вход данный скрипт получает название файла, после этого он начинает с помощью библиотеки gnss_tec получать данные из файла формата rnx или o.

[**scriprnx.py**](https://github.com/AlhemyD/practice/blob/main/src/data_processing/scriprnx.py) также отвечает за парсинг файлов. Данный скрипт использует fastapi и функцию парсинга из **parser.py** в своей работе. Демон для данного файла создается после форматирования, если его не было в нужной директории. После запуска данного скрипта publisher обращается к нему для парсинга файлов.

После запуска демона для **scriprnx.py** генерируются демоны для публикации файлов.

## Запуск демонов и описание их работы ##

Юнит-файл — это простой текстовый файл в стиле ini, который кодирует информацию о службе, сокете, устройстве, точке монтирования, точке автоматического монтирования, файле подкачки или разделе, целевой цели запуска, отслеживаемом пути к файловой системе, таймер, управляемый и контролируемый systemd, срез управления ресурсами или группа внешне созданных процессов. Прочитать подробнее вы сможете по [ссылке](https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html#User%20Unit%20Search%20Path). 

Примерный шаблон юнит-файла выглядит так:

```

[Unit]
Description=description for this daemon - описание демона

[Service]
ExecStart=/usr/bin/python3 /home/%user/practice/src/pub_sub/pub.py - запускаемый скрипт

Environment=PYTHONUNBUFFERED=1 - переменная окружения

Restart=on-failure - автоматический перезапуск при сбое

Type=simple - тип сервиса (процесс демона запускается и работает в фоне)

User=%user - имя пользователя, от имени которого будет запущен сервис

TimeoutSec=100 - устанавливает время ожидания в секундах для выполнения сервиса

[Install]
WantedBy=default.target - указывает, что сервис должен быть запущен по умолчанию при загрузке системы, используя default.target

```

Для генерации демона для **scriprnx.py** используется файл **create_scriprnx_service.sh**, который проверяет есть ли такой сервис в директории /etc/systemd/system/, если нет, то он его создает на основе шаблона для данного сервиса [fastapi_@.service](https://github.com/AlhemyD/practice/blob/main/src/all_services/fastapi_%40.service), подставляя в файл текущего пользователя

Для генерации служб для каждого файла, данные из которых надо будет опубликовать используется файл **create_pub_services.sh**, который проходится по каждому файлу в директории, берет из его названия часть и добавляет дату и смотрит есть ли такой файл в /etc/systemd/system/, если да, то он его пропускает, а если нет, то создает сервисный файл для данного файла. Эти демоны нужны для поддержания работы паблишеров для публикуемых файлов. Данный скрипт создает демонов на основе [station_@.service](https://github.com/AlhemyD/practice/blob/main/src/all_services/station_%40.service), с помощью sed он подставляет мнформацию о передаваемой дате, юзере и названии станции

## Publisher ##

Данный скрипт написан на языке python и отвечает за публикацию данных по определенному времени

## Subscriber ##

Данный скрипт написан на языке python и отвечает за получение данных от всех pub.py

## Лицензия
Этот проект распространяется под лицензией MIT. Подробности можно найти в файле LICENSE.
