from http.server import BaseHTTPRequestHandler, HTTPServer
from http import HTTPStatus
from datetime import datetime
import json
import threading
import requests
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

class Handler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        with open('server.log', 'a') as f:
            f.write("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format%args))

    def write_in_file(self, file, msg):
        print(f"new message received on {datetime.now()}", file=file)
        print(f"payload: {msg}\n", file=file)

    def respond(self, status=200, msg='ok'):
        self.send_response(status)
        self.end_headers()
        self.wfile.write(bytes(msg.encode()))

    def do_POST(self):
        if self.path == '/':
            self.respond(HTTPStatus.BAD_REQUEST, 'path not allowed!')
            return
        
        content_type = self.headers.get('content-type', '')
        if content_type != 'application/json':
            self.respond(HTTPStatus.BAD_REQUEST, 'unsupported content type!')
            return
        
        content_length = int(self.headers.get('content-length', 0))
        if content_length == 0:
            self.respond(HTTPStatus.BAD_REQUEST, 'empty content!')
            return
        
        try:
            msg = json.loads(self.rfile.read(content_length))['data']
        except:
            self.respond(HTTPStatus.BAD_REQUEST, 'error parsing content!')
            return
        
        topic = self.path[1:].replace('/', ' ')
        print(f'### New message on topic {topic}!')
        with open(topic + ".txt", 'a') as f:
            self.write_in_file(f, msg)

        self.respond()

    def do_GET(self):
        self.respond(HTTPStatus.METHOD_NOT_ALLOWED, 'method not allowed!')


if __name__ == "__main__":
    PORT = 8000
    my_server = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"### Server started")
    print(f"### The IP of your device is: {get_ip_address('wlan0')}") # wlan0 is the network interface of Raspberry Pi that connects them to the Wi-Fi. Change it according to your own need.
    threading.Thread(target=my_server.serve_forever).start()

    while True:
        option = input("Please pick one of the options below:\n  1. send a message to another device\n  2. show received messages of a topic\n  0. exit\n")
        if option == "1":
            device_ip = input("Please enter the ip address of the device you want to message:\n")
            title = input("Please enter the topic of your message:\n")
            payload = input("Please enter your message:\n")
            requests.post(f"http://{device_ip}:{PORT}/{title}", f'{{"data": "{payload}"}}', headers={'content-type': 'application/json'})
        elif option == "2":
            topic = input("Please enter the topic you want to see:\n")
            try:
                with open(topic + ".txt", 'r') as f:
                    print(*f.readlines(), sep='')
            except FileNotFoundError:
                print('There are no messages on this topic yet :(')
        elif option == "0":
            my_server.shutdown()
            break
        else:
            print("Invalid option, please try again!")
