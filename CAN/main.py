import can
import threading
from datetime import datetime


def write_in_file(file, msg):
        print(f"new message received on {datetime.now()}", file=file)
        print(f"payload: {msg}\n", file=file)


def rcv(bus, stop_event):
    while True:
        if stop_event.is_set():
            break

        data = bus.recv(3)
        if data is None:
            continue
        print('### New message received!')
        data = [item for item in data.data]
        data = ''.join(map(chr, data))
        try:
            topic, msg = data.split(',')
            with open(topic + ".txt", 'a') as f:
                write_in_file(f, msg)
        except ValueError:
            print('### The received message is in an invalid format!')


bustype = 'socketcan'
channel = 'can0'
bus = can.interface.Bus(channel=channel, bustype=bustype, bitrate=125000)

stop_event = threading.Event()

receiver = threading.Thread(target=rcv, args=(bus, stop_event, ))
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
        print('Shutting down socket, please wait...')
        stop_event.set()
        receiver.join()
        bus.shutdown()
        print('Shut down complete, Bye!')
        break
    else:
        print('Invalid option!')
