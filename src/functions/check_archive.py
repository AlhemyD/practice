import zipfile
from logger import get_logger
import os
import gzip
import subprocess

logger = get_logger("check")

def check_zip_integrity(zip_file_path):
    #logger.info(f"I'm starting to check the archive for integrity")
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as file:
            zip_test = file.testzip()
            directoria, file_name = os.path.split(zip_file_path)
            if zip_test is None:
                logger.info(f"The archive is complete:  {file_name}")
                return True
            else:
                #logger.error(f"The archive is damaged: {zip_test}")
                return False
    except zipfile.BadZipFile as e:
        #logger.error(f"Error when opening a .zip archive: {e}")
        return False

def check_gz(gz_file_path):
    logger.info(f"I'm starting to check the archive for integrity")
    try:
        with gzip.open(gz_file_path, 'rb') as f:
            for _ in f:
                pass
        logger.info(f"'{gz_file_path}' is not corrupted.")
    except OSError as e:
        logger.error(f"'{gz_file_path}' is corrupted. Error: {e}")

def check_z_archive(file_path):
    # Определяем тип файла с помощью утилиты file
    file_type = subprocess.check_output(['file', file_path]).decode()

    # Проверяем, является ли файл архивом формата .Z
    if '.Z' in file_type:
        print("The file is in .Z archive format.")
    else:
        print("The file is not in .Z archive format.")

zip_file = 'download_and_unzip/unbj3390.23d.Z'
check_z_archive(zip_file)
