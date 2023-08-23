from http.server import BaseHTTPRequestHandler, HTTPServer
from http import HTTPStatus
from datetime import datetime, timezone
from sys import getsizeof
from dotenv import load_dotenv
import os


load_dotenv()


class Handler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        with open('server.log', 'a') as f:
            f.write("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format%args))

    def respond(self, status=200, msg='ok'):
        self.send_response(status)
        self.end_headers()
        self.wfile.write(bytes(msg.encode()))

    def do_POST(self):
        receive_time = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
        content_length = int(self.headers.get('content-length', 0))

        msg = self.rfile.read(content_length)
        print(msg)

        send_time = (float(msg.decode('ascii').split('#')[0]))

        with open(FILE_NAME, 'a') as file:
            print(f'{receive_time - send_time:.3f},{send_time:.3f},{receive_time:.3f},{getsizeof(msg)}',file=file)

        self.respond()

    def do_GET(self):
        self.respond(HTTPStatus.METHOD_NOT_ALLOWED, 'method not allowed!')

FILE_NAME = os.environ['FILE_NAME']

with open(FILE_NAME, 'w') as file:
    print('delay,send_time,receive_time,data_length',file=file)

try:
    my_server = HTTPServer(("0.0.0.0", 8000), Handler)
    print(f"### Server started")
    my_server.serve_forever()
except KeyboardInterrupt:
    print("### Stopping gracefully...")

my_server.shutdown()
