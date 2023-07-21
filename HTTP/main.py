from http.server import BaseHTTPRequestHandler, HTTPServer
from http import HTTPStatus
from datetime import datetime
import json
import threading
import requests


class Handler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        message = format % args
        with open('server.log', 'a') as f:
            f.write("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          message.translate(self._control_char_table)))

    def write_in_file(self, file, msg):
        print(f"new message recieved on {datetime.now()}", file=file)
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

        with open(self.path[1:] + ".txt", 'a') as f:
            self.write_in_file(f, msg)

        self.respond()

    def do_GET(self):
        self.respond(HTTPStatus.METHOD_NOT_ALLOWED, 'method not allowed!')


if __name__ == "__main__":
    PORT = 8000
    my_server = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"Server started at {PORT}")
    threading.Thread(target=my_server.serve_forever).start()

    while True:
        option = input("Please pick one of the options below:\n  1. send a message to another device\n  2. exit\n")
        if option == "1":
            device_ip = input("Please enter the ip address of the device you want to message:\n")
            title = input("Please enter the title of your message:\n")
            payload = input("Please enter your message:\n")
            requests.post(f"http://{device_ip}:{PORT}/{title}", f'{{"data": "{payload}"}}', headers={'content-type': 'application/json'})
        elif option == "2":
            my_server.shutdown()
            break
        else:
            print("Invalid option, please try again!")
