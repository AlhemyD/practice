import os
import sys, threading
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../log'))
from logger import get_logger
from download import download_file_from_url
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../functions'))
from check_archive import check_zip_integrity

import schedule
import subprocess
from formatting import reformat_crx_to_rnx
from parser import parsing
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta


logger = get_logger("main")

#создание директории data

directory = os.path.join(os.path.dirname(os.path.realpath(__file__)),"../../data")

if not os.path.exists(directory):
    os.makedirs(directory)
    logger.info(f"Directory '{directory}' created successfully.")

    #запуск скрипта скачиванияls
today = datetime.now()
date = (today - timedelta(days=200)).strftime('%Y-%m-%d')
download_file_from_url(date)
file_name=date
try:
#архивация
    logger.info(f"start to unpack")
    subprocess.run(f"bash unzip_data.sh {file_name}", shell=True, check=True)
    logger.info(f"Files unpacked successfully")
except subprocess.CalledProcessError as e:
    logger.error(f"A file archiving error has occurred: {e}")
#except KeyboardInterrupt:
#    pass

#форматирование

logger.info("I'm starting to format files from .crx to .rnx")
directory_crx = os.path.join(directory, file_name)
count_file = os.listdir(directory_crx)
for file in range (len(count_file)):
    path_crx = os.path.join(directory_crx, count_file[file])
    reformat_crx_to_rnx(path_crx)
logger.info("All files has been successfully reformatted")
#schedule.every().day.at("05:02").do(main)


#while True:
#    schedule.run_pending()

