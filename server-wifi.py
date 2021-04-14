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

print("UDP server up and listening")

# CONNECTION TO DATABASES
dbWiFi = client.ServerProxy("http://127.0.0.1:8001/apiWiFiLog")

while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    message = message.decode(encoding = 'UTF-8', errors = 'strict')

    if message == "close":
        UDPServerSocket.close()
        break

    file = open("text-wifi.txt", "a")
    file.write(message + "\n")
    file.close()

    dbWiFi.newWiFiLog()

    print(message)
    print("")