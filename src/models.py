from pydantic import BaseModel
import paho.mqtt.client as mqtt_client
from logger import get_logger

class Path(BaseModel):
    path: str

class Publisher:
    def __init__(self, station: str, broker: str, topic: str):
        self.station = station
        self.client = mqtt_client.Client(
                    mqtt_client.CallbackAPIVersion.VERSION2,
                    self.station
                )
        self.broker = broker
        self.topic = topic

    def connect(self):
        self.client.connect(self.broker)

    def loop_start(self):
        self.client.loop_start()

    def publish(self, data: str):
        self.client.publish(self.topic, data)

    def disconnect(self):
        self.client.disconnect()

    def loop_stop(self):
        self.client.loop_stop()

class Subscriber:
    
    def onmessage(self, client, userdata, message):
        logger=get_logger("subscriber_class")
        data=str(message.payload.decode("utf-8"))
        logger.info(data)
        print(data)

    def __init__(self, uid: str, broker: str, topic: str):
        self.uid = uid
        self.client = mqtt_client.Client(
                    mqtt_client.CallbackAPIVersion.VERSION2,
                    self.uid
                )
        self.broker = broker
        self.topic = topic
        self.client.on_message=self.onmessage

    def connect(self):
        self.client.connect(self.broker)

    def loop_start(self):
        self.client.loop_start()

    def subscribe(self):
        self.client.subscribe(self.topic)

    def disconnect(self):
        self.client.disconnect()

    def loop_stop(self):
        self.client.loop_stop()




