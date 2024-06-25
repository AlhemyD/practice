import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../log'))
from logger import get_logger
from download import download_file_from_url
import schedule
import subprocess
from formatting import reformat_crx_to_rnx
from parser import parsing

logger = get_logger("main")

#создание директории data

directory = "../../data"

if not os.path.exists(directory):
    os.makedirs(directory)
    logger.info(f"Directory '{directory}' created successfully.")

#запуск скрипта скачиванияls

logger.info("Data loading will start at 22:00")
#schedule.every().day.at("17:24").do(download_file_from_url)

#архивация
files_in_directory = os.listdir(directory)
if len(files_in_directory) != 0:
    if len(files_in_directory) == 1:
        file_name = files_in_directory[0]
        name, form =  os.path.splitext(file_name)
        try:
            logger.info(f"start to unpack")
            subprocess.run(f"bash unzip_data.sh {name}", shell=True, check=True)
            logger.info(f"Files unpacked successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"A file archiving error has occurred: {e}")
    else:
        file_name = files_in_directory[1]
        name, form =  os.path.splitext(file_name)
        logger.error("More than one file in the directory or no files found.")

#форматирование

    logger.info("I'm starting to format files from .crx to .rnx")
    directory_crx = os.path.join(directory, name)
    count_file = os.listdir(directory_crx)
    for file in range (len(count_file)):
        path_crx = os.path.join(directory_crx, count_file[file])
        reformat_crx_to_rnx(path_crx)

while True:
    schedule.run_pending()


