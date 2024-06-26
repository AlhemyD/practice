import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../log'))
from logger import get_logger
from download import download_file_from_url
import schedule
import subprocess
from formatting import reformat_crx_to_rnx
from parser import parsing
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta


logger = get_logger("main")

#создание директории data

directory = "../../data"

if not os.path.exists(directory):
    os.makedirs(directory)
    logger.info(f"Directory '{directory}' created successfully.")

    #запуск скрипта скачиванияls
today = datetime.now()
date = (today - timedelta(days=200)).strftime('%Y-%m-%d')

logger.info("Data loading will start at 22:00")
scheduler = BlockingScheduler()
scheduler.add_job(lambda: download_file_from_url(date), 'cron', hour=16, minute=5)

try:
    scheduler.start()
except KeyboardInterrupt:
    pass

#архивация

try:
    logger.info(f"start to unpack")
    subprocess.run(f"bash unzip_data.sh {file_name}", shell=True, check=True)
    logger.info(f"Files unpacked successfully")
except subprocess.CalledProcessError as e:
    logger.error(f"A file archiving error has occurred: {e}")


#форматирование

logger.info("I'm starting to format files from .crx to .rnx")
directory_crx = os.path.join(directory, file_name)
count_file = os.listdir(directory_crx)
for file in range (len(count_file)):
    path_crx = os.path.join(directory_crx, count_file[file])
    reformat_crx_to_rnx(path_crx)

#schedule.every().day.at("05:02").do(main)


#while True:
#    schedule.run_pending()


