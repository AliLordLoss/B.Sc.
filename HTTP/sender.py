import os, time, random
from string import ascii_uppercase
from datetime import datetime, timezone
from sys import getsizeof
from dotenv import load_dotenv
import requests


load_dotenv()


RECEIVER_IP = os.environ['RECEIVER_IP']
DATA_LENGTH = int(os.environ['DATA_LENGTH'])
PERIOD = int(os.environ['PERIOD'])
PREFIX_SIZE = getsizeof(bytes(f"{datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp():.3f}#", 'ascii'))

while True:
    N = DATA_LENGTH - PREFIX_SIZE
    random_string = ''.join(random.choices(ascii_uppercase, k=N))
    send_time = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
    requests.post(f"http://{RECEIVER_IP}:8000", f'{send_time:.3f}#{random_string}', headers={'content-type': 'text/plain'})
    print(f'### sent on: {send_time}')
    time.sleep(PERIOD)
