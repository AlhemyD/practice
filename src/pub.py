import paho.mqtt.client as mqtt_client
import time
from models import Publisher
pub=Publisher("station1","broker.emqx.io","station/data")
pub.connect()
pub.loop_start()
for i in range(20):
    pub.publish( f"data - {i}")
    time.sleep(1)
pub.disconnect()
pub.loop_stop()
