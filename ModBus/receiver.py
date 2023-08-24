from pyModbusTCP.server import ModbusServer, DataBank
from datetime import datetime, timezone
import os, struct
from dotenv import load_dotenv


load_dotenv()


FILE_NAME = os.environ['FILE_NAME']

class CustomDataBank(DataBank):
    def set_holding_registers(self, address, word_list, srv_info=None):
        receive_time = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
        print(f'### Received at {receive_time}')
        
        send_time = struct.unpack("d", bytes(word_list))[0]
        with open(FILE_NAME, 'a') as file:
            print(f'{receive_time - send_time:.3f},{send_time:.3f},{receive_time:.3f}', file=file)
        
        return super().set_holding_registers(address, word_list, srv_info)

with open(FILE_NAME, 'w') as file:
    print('delay,send_time,receive_time', file=file)

server = ModbusServer("0.0.0.0", 12345, no_block=True, data_bank=CustomDataBank())
server.start()
print(f"### Server started")

try:
    while True:
        pass
except KeyboardInterrupt:
    print("### Stopping gracefully...")

server.stop()
