from socket import *

from xmlrpc import client
from xmlrpc.server import *

# SOCKET STUFF 
localIP = "192.168.1.67"
localPort = 3001
bufferSize = 1024

# Create a datagram socket
TCPServerSocket = socket(family = AF_INET, type = SOCK_STREAM)

# Bind to address and ip
TCPServerSocket.bind((localIP, localPort))

# Socket listening
TCPServerSocket.listen()

print("TCP server up and listening")

# CONNECTION TO DATABASES
dbUser = client.ServerProxy("http://127.0.0.1:8002/apiUser")

while(True):
    conn, address = TCPServerSocket.accept()

    message = conn.recv(bufferSize)

    if not message:
        break

    print(message)
    print()

    if message == "close":
        TCPServerSocket.close()
        break

    messageToSend = message + " check"

    conn.send(message)


