import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../log'))
from datetime import datetime, timedelta
import schedule
import time
import subprocess
import requests
from logger import get_logger

logger = get_logger("download")

def download_file_from_url(date): 
    #today = datetime.now()
    #date = (today - timedelta(days=3)).strftime('%Y-%m-%d')
    #link = "https://drive.google.com/file/d/1cU9FzjT_e_gUC_eRycWcvi3mmP2n_XM7/view?usp=sharing"
    link = f"https://api.simurg.space/datafiles/map_files?date={date}"
    file_name = f"{date}.zip"
    #file_name = "2023-12-05.zip"
    file_path = os.path.join("../../data", file_name)
    logger.info(f"Downloading file from {link}...")

    with open(file_path, "wb") as f:
        print("Downloading %s" % file_name)
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                sys.stdout.flush()

#    print(f"{file_name} was downloaded successfully")
    logger.info(f"File downloaded successfully to {file_name}")
    
    #закоментировала потому что эта часть кода удёт в main.py
    
#    print(f"start to unpack")
#    subprocess.run(f"sudo bash unzip_data.sh {date}", shell=True)
#    logger.info(f"Files unpacked successfully")

#Это должно быть тут потому что функция запускается по времени и 
#print там не нужен. Нужно чтобы он был вне функции когда время ещё не наступило

#print("Data loading will start at 22:00")
#logger.info("test loggar")
#schedule.every().day.at("08:59").do(download_file_from_url)

#while True:
#    schedule.run_pending()
