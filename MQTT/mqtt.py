import paho.mqtt.client as mqtt
from datetime import datetime
import time
import os
from dotenv import load_dotenv

load_dotenv()

def write_in_file(file, msg):
    print(f"new message recieved on {datetime.now()}", file=file)
    print(f"payload: {msg}\n", file=file)

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def on_message(client, userdata, msg):
    # try: 
    with open(msg.topic + ".txt", 'a') as f:
        write_in_file(f, msg.payload.decode('ascii'))
    # except FileNotFoundError:
    #     with open(msg.topic, 'w') as f:
    #         write_in_file(f, msg.payload.decode('ascii'))

message_broker = os.environ['MQTT_BROKER']

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(message_broker, 1883, 60)

client.loop_start()

while True:
    option = input("Please pick one of the options below:\n  1. subscribe to a topic\n  2. publish a message to a topic\n  3. exit\n")
    if option == "1":
        topic = input("Please enter the topic you want to subscribe to:\n")
        client.subscribe(topic)
    elif option == "2":
        topic = input("Please enter the topic you want to publish to:\n")
        payload = input("Please enter your message:\n")
        client.publish(topic, payload=payload, qos=0, retain=False)
    elif option == "3":
        break
    else:
        print("Invalid option, please try again!")

client.loop_stop()
client.disconnect()
