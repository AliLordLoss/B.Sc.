import can, os, struct
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
        print(f"### Received at {receive_time:.3f}")
        send_time = struct.unpack("d", data.data)[0]
        with open(FILE_NAME, 'a') as file:
            print(f'{receive_time - send_time:.3f},{send_time:.3f},{receive_time:.3f}', file=file)

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
