from socket import *

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

# Socket listening
#TCPServerSocket.listen()

print("UDP user server up and listening")

# CONNECTION TO DATABASES
dbUser = client.ServerProxy("http://127.0.0.1:8002/apiUser")

while(True):
    message, address = UDPServerSocket.recvfrom(bufferSize)

    print(message)
    print()

    message = message.decode(encoding = 'UTF-8', errors = 'strict')

    print(message)
    print()

    if message == "close":
        UDPServerSocket.close()
        break

    messageToSend = message + " check"

    bytesToSend = str.encode(messageToSend)

    UDPServerSocket.sendto(bytesToSend, address)


