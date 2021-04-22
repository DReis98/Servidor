from socket import socket, AF_INET, SOCK_DGRAM

from xmlrpc import client
from xmlrpc.server import *

# SOCKET STUFF 
localIP = "192.168.1.67"
localPort = 3001
bufferSize = 1024

# Create a datagram socket
UDPServerSocket = socket(family = AF_INET, type = SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# CONNECTION TO DATABASES
dbUser = client.ServerProxy("http://127.0.0.1:8002/apiUser")

while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    message = message.decode(encoding = 'UTF-8', errors = 'strict')

    if message == "close":
        UDPServerSocket.close()
        break

    message = message.split()

    username = message[0]
    password = message[1]
    
    messageToSend = ""

    nbUser = dbUser.checkUserExists(username)
    # nao existe
    if nbUser == 0:
        messageToSend = "created"
        user = dbUser.newUser(username, password)
    elif nbUser == 1:
        nbUserPass = dbUser.checkUserPassword(username, password)
        # wrong password
        if nbUserPass == 0:
            messageToSend = "pass"
        # password correct
        elif nbUserPass == 1:
            messageToSend = "ok"
        else:
            messageToSend = "error"
    else:
        messageToSend = "error"
    

    print(messageToSend)
    
    messageToSend = str.encode(messageToSend)

    UDPServerSocket.sendto(messageToSend, address)

