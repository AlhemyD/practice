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
today = datetime.now()
date = (today - timedelta(days=200)).strftime('%Y-%m-%d')

#создание директории data

directory = os.path.join(os.path.dirname(os.path.realpath(__file__)),"../../data")
if os.path.exists(os.path.join(directory,date)):
    logger.warning(f"path {os.path.join(directory,date)} already exists so deleting it")
    subprocess.run(f"sudo rm -r {os.path.join(directory,date)}",shell=True,check=True)
if os.path.exists(os.path.join(directory,date+".zip")):
    logger.warning(f"file {os.path.join(directory,date+'.zip')} already exists so deleting it")
    subprocess.run(f"rm {os.path.join(directory,date+'.zip')}",shell=True,check=True)
if not os.path.exists(directory):
    os.makedirs(directory)
    logger.info(f"Directory '{directory}' created successfully.")

    #запуск скрипта скачиванияls
download_file_from_url(date)
file_name=date
try:
#архивация
    logger.info(f"start to unpack")
    unzip_path=os.path.join(os.path.dirname(os.path.realpath(__file__)),"unzip_data.sh")
    subprocess.run(f"bash {unzip_path} {file_name}", shell=True, check=True)
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

logger.info("Starting FastAPI")
fastapi_path=os.path.join(os.path.dirname(os.path.realpath(__file__)),'../all_services/create_scriprnx_service.sh')
subprocess.run(f"", shell=True, check=True)



logger.info("Starting a creation of DAEMONS")
cpub_path=os.path.join(os.path.dirname(os.path.realpath(__file__)),'../all_services/create_pub_services.sh')
subprocess.run(f"sudo bash {cpub_path} {date}", shell=True, check=True)
#while True:
#    schedule.run_pending()

