import can, time, os, struct
from datetime import datetime, timezone
from dotenv import load_dotenv


load_dotenv()

PERIOD = int(os.environ['PERIOD'])

bustype = 'socketcan'
channel = 'can0'
bus = can.interface.Bus(channel=channel, bustype=bustype, bitrate=125000)

try:
    while True:
        send_time = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
        data = struct.pack('d', send_time)
        print(f"### Sending at {send_time:.3f}")
        bus.send(can.Message(arbitration_id=0, data=data, is_extended_id=False))
        time.sleep(PERIOD)
except KeyboardInterrupt:
    print('### Stopping gracefully...')
    bus.shutdown()
