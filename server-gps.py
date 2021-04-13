import socket

localIP = "192.168.1.67"
localPort = 3000
bufferSize = 1024

msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)

# Create a datagram socket
UDPServerSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    message = message.decode(encoding = 'UTF-8', errors = 'strict')

    #clientMsg = "Message received: {}".format(message)
    #clientIP = "Client IP Address: {}".format(address)

    if message == "close":
        UDPServerSocket.close()
        break

    file = open("text-gps.txt", "a")
    file.write(message + "\n")
    file.close()

    print(message)
    print("")
    #print(clientIP)

    # Sending a reply to client
    #UDPServerSocket.sendto(str.encode("Received: " + clientMsg), address)