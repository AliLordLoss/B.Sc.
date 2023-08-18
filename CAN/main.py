import can
import threading
from datetime import datetime


def write_in_file(file, msg):
        print(f"new message received on {datetime.now()}", file=file)
        print(f"payload: {msg}\n", file=file)


def rcv(bus):
    while True:
        data = bus.recv()
        data = ''.join(map(chr, data))
        topic, msg = data.split(',')
        with open(topic + ".txt", 'a') as f:
            write_in_file(f, msg)


bustype = 'socketcan'
channel = 'can0'
bus = can.interface.Bus(channel=channel, bustype=bustype, bitrate=125000)

receiver = threading.Thread(target=rcv, args=(bus, ))
receiver.start()

while True:
    cmd = input('Please select one of the options below:\n  1. Send a message\n  2. See received messages of a topic\n  0. exit\n')
    if cmd == '1':
        topic = input('Please enter the topic you want to send message on:\n')
        msg = input('Please enter the message you want to send:\n')
        data = topic + "," + msg
        data = list(map(ord, data))
        bus.send(can.Message(arbitration_id=0, data=data, is_extended_id=False))
    elif cmd == '2':
        topic = input('Please enter the topic you want to see:\n')
        try:
            with open(topic + ".txt", 'r') as f:
                print(*f.readlines(), sep='')
        except FileNotFoundError:
            print('There are no messages on this topic yet :(')
    elif cmd == '0':
        print('Waiting for receiver to stop...')
        receiver.join()
        print('Receiver stopped!')
        break
    else:
        print('Invalid option!')
