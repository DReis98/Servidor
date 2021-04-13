import socket

msgFromClient = "Hello UDP Server"
bytesToSend = str.encode(msgFromClient)
serverAddressPort = ("188.82.90.18", 3000)
bufferSize = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)

# Send to server using created UDP socket
number = 1
while(True):
    print("Print your message #" + str(number) + " :")
    number = number + 1

    msgToSend = input()

    UDPClientSocket.sendto(str.encode(msgToSend), serverAddressPort)

    #msgFromServer = UDPClientSocket.recvfrom(bufferSize)

    #msg = "Message from Server: {}".format(msgFromServer[0])
    #serverIP = "Server IP Address: {}".format(serverAddressPort)
    #print(msg)
    #print(serverIP)

    if msgToSend == "close":
        break
    