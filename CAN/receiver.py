import can, os
from datetime import datetime, timezone
from dotenv import load_dotenv


load_dotenv()

FILE_NAME = os.environ['FILE_NAME']

def rcv(bus):
    while True:
        data = bus.recv()
        receive_time = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
        if data is None:
            continue
        send_time = data.data
        with open(FILE_NAME, 'a') as file:
            print(f'{receive_time - send_time},{send_time},{receive_time}', file=file)

with open(FILE_NAME, 'w') as file:
    print('delay,send_time,receive_time', file=file)

bustype = 'socketcan'
channel = 'can0'
bus = can.interface.Bus(channel=channel, bustype=bustype, bitrate=125000)

try:
    rcv(bus)
except KeyboardInterrupt:
    print('### Stopping gracefully...')
    bus.shutdown()
