import paho.mqtt.client as mqtt
import os, time, random
from string import ascii_uppercase
from datetime import datetime, timezone
from sys import getsizeof
from dotenv import load_dotenv


load_dotenv()


def on_message(client, userdata, msg):
    print(msg)


MESSAGE_BROKER = os.environ['MQTT_BROKER']
TOPIC = os.environ['TOPIC']
DATA_LENGTH = int(os.environ['DATA_LENGTH'])
PUBLISH_PERIOD = int(os.environ['PUBLISH_PERIOD'])
PREFIX_SIZE = getsizeof(bytes(f"{datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp():.3f}#", 'ascii'))

client = mqtt.Client()
client.on_message = on_message
client.connect(MESSAGE_BROKER, 1883, 60)

try:
    client.loop_start()
    while True:
        N = DATA_LENGTH - PREFIX_SIZE
        random_string = ''.join(random.choices(ascii_uppercase, k=N))
        send_time = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
        client.publish(TOPIC, f"{send_time:.3f}#{random_string}")
        print(f'published on: {send_time:.3f}')
        time.sleep(PUBLISH_PERIOD)
except KeyboardInterrupt:
    print('### Stopping gracefully...')
client.loop_stop()
client.disconnect()
