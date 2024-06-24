import sys, requests, json
sys.path.append("../modules")
from models import Publisher
sys.path.append("../log")
from logger import get_logger
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
logger = get_logger("pub")

'''
скрипт вызывается командой вида^

python3 pub.py {rnx_file_name}

т.е.

python3 pub.py darw00aus-r-20240010000-01d-30s-mo.rnx



'''
rnx_file_name = sys.argv[1] #Тогда здесь будет имя файла rnx
#data = sys.argv[2:] #А здесь будет список ['1', '2', '3', '4', '5', '6']

'''
Предполагается, что в data будут передаваться пропарсенные данные, 
которые нужно опубликовать
'''
def publ(pub, data):
    pub.publish(f"{pub.station}@%@%!{data}")


pub = Publisher(rnx_file_name,"localhost","station/data")
pub.connect()
pub.loop_start()
#for i in data:
#    pub.publish(f"{pub.station}@%@%!{i}")


    
date = (datetime.now() - timedelta(days=200)).strftime('%Y-%m-%d')
#date="2024-06-23"
link=f"http://localhost:8000/parsing/{date}/{rnx_file_name}"
response = requests.get(link, stream=True).json()
if "error" in response:
    logger.error(f"error during request for station {pub.station} - error - {response['error']}")
    print(response)
else:
    logger.info(f"Parsed data for station {pub.station} successfully. Starting scheduler")

    '''
    '{} {}: {} {}'.format(
                    tec.timestamp,
                    tec.satellite,
                    tec.phase_tec,
                    tec.p_range_tec,
                )

    "2024-01-01 00:00:00 G12: 7.8285638894945935 22.766467356433278",
    '''
    for data in response["parse_data"]:
        date=list(map(int, (datetime.now().strftime('%Y-%m-%d')).split("-")))
        time = list(map(int, str(data.split(" ")[1]).split(":")))
        dt=datetime(date[0],date[1],date[2], time[0],time[1],time[2])

        scheduler.add_job(publ, 'date', run_date=dt, args=[pub,data])
scheduler.start()

try:
    while True:
        pass
except KeyboardInterrupt or Exception:
    pub.disconnect()
    pub.loop_stop()
    scheduler.shutdown()
    logger.error(f"Cought an Exception for station {pub.station} - Exception - {Exception}")
