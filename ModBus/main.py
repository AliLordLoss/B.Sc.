from pyModbusTCP.server import ModbusServer, DataBank
from pyModbusTCP.client import ModbusClient
from datetime import datetime
import socket
import fcntl
import struct


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', bytes(ifname[:15], 'utf-8'))
    )[20:24])


def write_in_file(file, msg):
    print(f"new message received on {datetime.now()}", file=file)
    print(f"payload: {msg}\n", file=file)


class CustomDataBank(DataBank):
    def set_holding_registers(self, address, word_list, srv_info=None):
        print('### New message received!')
        data = ''.join(map(chr, word_list))
        try:
            topic, msg = data.split(',')
            with open(topic + ".txt", 'a') as f:
                write_in_file(f, msg)
        except ValueError:
            print('### The received message is in an invalid format!')
        
        return super().set_holding_registers(address, word_list, srv_info)


server = ModbusServer("0.0.0.0", 12345, no_block=True, data_bank=CustomDataBank())
server.start()
print(f"### Server started")
print(f"### The IP of your device is: {get_ip_address('wlan0')}") # wlan0 is the network interface of Raspberry Pi that connects them to the Wi-Fi. Change it according to your own need.

client = None

while True:
    cmd = input('Please choose one of the options below:\n  1. send a message on a topic\n  2. See received messages of a topic\n  0. exit\n')
    if cmd == '1':
        host = input('Please enter the IP address to which you want to send a message:\n')
        topic = input('Please enter the topic you want to send message on:\n')
        msg = input('Please enter the message you want to send:\n')
        data = topic + "," + msg
        data = list(map(ord, data))
        client = ModbusClient(host=host, port=12345, timeout=5)
        try:
            if not client.write_multiple_registers(0, data):
                raise Exception
        except:
            print('### Something went wrong :(')
            print('### Does the IP address exist and is this program running on that machine too?')
    elif cmd == '2':
        topic = input('Please enter the topic you want to see:\n')
        try:
            print('### The received message are as follows:')
            with open(topic + ".txt", 'r') as f:
                print(*f.readlines(), sep='')
        except FileNotFoundError:
            print('### There are no messages on this topic yet :(')
    elif cmd == '0':
        print('### Stopping server, Please wait...')
        server.stop()
        print('### Server stopped. Bye!')
        break
    else:
        print('### Invalid option!')
