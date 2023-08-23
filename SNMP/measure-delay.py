from pysnmp.hlapi import *
from datetime import datetime, timezone
import os, time
from dotenv import load_dotenv


load_dotenv()


def getsnmp(host, oid):
    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in getCmd(SnmpEngine(),
                              CommunityData('public', mpModel=1),
                              UdpTransportTarget((host, 161)),
                              ContextData(),
                              ObjectType(ObjectIdentity(oid)),
                              lookupMib=False,
                              lexicographicMode=False):

        if errorIndication:
            print(errorIndication)
            break

        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            break

        else:
            for varBind in varBinds:
                print(' = '.join([x.prettyPrint() for x in varBind]))


FILE_NAME = os.environ['FILE_NAME']
DEVICE_IP = os.environ['DEVICE_IP']
PERIOD = int(os.environ['PERIOD'])

with open(FILE_NAME, 'w') as file:
    print('delay,send_time,acknowledge_time', file=file)

while True:
    send_time = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
    getsnmp(DEVICE_IP, "1.3.6.1.2.1.1.5.0")
    ack_time = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
    with open(FILE_NAME, 'a') as file:
        print(f'{ack_time - send_time:.3f},{send_time:.3f},{ack_time:.3f}',file=file)
    time.sleep(PERIOD)