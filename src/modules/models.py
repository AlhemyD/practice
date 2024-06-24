from pydantic import BaseModel
import paho.mqtt.client as mqtt_client


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
        self.client.publish(topic=self.topic, payload=data)

    def disconnect(self):
        self.client.disconnect()

    def loop_stop(self):
        self.client.loop_stop()
