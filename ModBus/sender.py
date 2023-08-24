from pyModbusTCP.client import ModbusClient
from datetime import datetime, timezone
import os, time, struct
from dotenv import load_dotenv


load_dotenv()


HOST = os.environ['RECEIVER_IP']
PERIOD = int(os.environ['PERIOD'])

try:
    while True:
        client = ModbusClient(host=HOST, port=12345, timeout=5)
        send_time = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
        client.write_multiple_registers(0, struct.pack('d', send_time))
        time.sleep(PERIOD)
except KeyboardInterrupt:
    print('### Stopping gracefully...')
