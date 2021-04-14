import socket

msgFromClient = "Hello UDP Server"
bytesToSend = str.encode(msgFromClient)
serverAddressPort = ("188.82.90.18", 3001)
bufferSize = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)

msgToSend = "close"

UDPClientSocket.sendto(str.encode(msgToSend), serverAddressPort)

    