from pysnmp.hlapi import *


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

def setsnmp(host, oid, dataType, value):
    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in setCmd(SnmpEngine(),
                              CommunityData('private', mpModel=0),
                              UdpTransportTarget((host, 161)),
                              ContextData(),
                              ObjectType(ObjectIdentity(oid), dataType(value)),
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


agent = ''
while True:
    print('---')
    if not agent:
        agent = input('Please enter the ip address of the device you want to connect to:\n')

    instructions = f'Please select an option below:\n  1. get a MIB from {agent}\n  2. set a MIB of {agent}\n'
    if agent:
        instructions += '  3. change the ip address\n'
    instructions += '  0. exit the program\n'
    cmd = input(instructions)
    if cmd == '1':
        OID = input('Please enter the OID of the object you wish to get:\n')
        getsnmp(agent, OID)
    elif cmd == '2':
        OID = input('Please enter the OID of the object you wish to set:\n')
        dataType = None
        dataTypeId = input('Please select the data type of the chosen object:\n  1. String\n  2. Integer\n') # TODO add more data types
        if dataTypeId == '1':
            dataType = OctetString
        elif dataTypeId == '2':
            dataType = Integer
        else:
            print('Invalid data type! Aborting...')
            continue
        value = input('Please enter the value you wish to set for this object:\n')
        setsnmp(agent, OID, dataType, value)
    elif cmd == '3':
        agent = input('Please enter the ip address of the device you want to connect to:\n')
    elif cmd == '0':
        print('Bye!')
        break
    else:
        print('Invalid option selected!')
