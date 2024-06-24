import paho.mqtt.client as mqtt_client
import sys
sys.path.append("../modules")
from models import Publisher
sys.path.append("../log")
from logger import get_logger
import requests

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
pub = Publisher(rnx_file_name,"localhost","station/data")
#for i in data:
#    pub.publish(f"{pub.station}@%@%!{i}")


    
#date = (today - timedelta(days=200)).strftime('%Y-%m-%d')
date="2024-06-23"
link=f"http://localhost:8000/parsing/{date}/{rnx_file_name}"
response = requests.get(link, stream=True)
#print(response.parse_data[0])
def publ(pub, data):
    pub.connect()
    pub.loop_start()
    pub.publish(f"{pub.station}@%@%!{data}")
    pub.disconnect()
    pub.loop_stop()
publ(pub, rnx_file_name)
