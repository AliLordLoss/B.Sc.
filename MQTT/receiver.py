import paho.mqtt.client as mqtt
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from sys import getsizeof


load_dotenv()


def on_message(client, userdata, msg):
    receive_time = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
    send_time = (float(msg.payload.decode('ascii').split('#')[0]))
    with open(FILE_NAME, 'a') as file:
        print(f'{receive_time - send_time:.3f},{send_time:.3f},{receive_time:.3f},{getsizeof(msg.payload)}',file=file)


MESSAGE_BROKER = os.environ['MQTT_BROKER']
TOPIC = os.environ['TOPIC']
FILE_NAME = os.environ['FILE_NAME']

client = mqtt.Client()
client.on_message = on_message
client.connect(MESSAGE_BROKER, 1883, 60)

with open(FILE_NAME, 'w') as file:
    print('delay,send_time,receive_time,data_length',file=file)

try:
    client.loop_start()
    client.subscribe(TOPIC)
    while True:
        pass
except KeyboardInterrupt:
    print('### Stopping gracefully...')
client.loop_stop()
client.disconnect()
