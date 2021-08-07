import xmlrpc.server

from socket import socket, AF_INET, SOCK_DGRAM

from xmlrpc import client


# SOCKET STUFF 
localIP = "192.168.1.67"
localPort = 3000
bufferSize = 1024

# Create a datagram socket
UDPServerSocket = socket(family = AF_INET, type = SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# CONNECTION TO DATABASES
dbGPS = client.ServerProxy("http://127.0.0.1:8000/apiGPSLog")
dbWiFi = client.ServerProxy("http://127.0.0.1:8001/apiWiFiLog")
dbUser = client.ServerProxy("http://127.0.0.1:8002/apiUser")

while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    message = message.decode(encoding = 'UTF-8', errors = 'strict')

    if message == "close":
        UDPServerSocket.close()
        break

    message_s = message.split()

    # username em message[1]
    print(message_s)
    
    id_user = dbUser.getIdUser(message_s[1])

    if id_user == 0:
        print("Continued")
        continue

    if message_s[0] == "GPS":
        number = dbGPS.newGPSLog(id_user, message_s[2], message_s[3], float(message_s[4]), float(message_s[5]), float(message_s[6]))
        print("GPS Location" + message_s[4]  + " " + message_s[5] + " "+ message_s[6])
        print(number)
        print("")
    elif message_s[0] == "WiFi":
        msg = message.split(sep = " ", maxsplit = 4)
        number = dbWiFi.newWiFiLog(id_user, message_s[2], message_s[3], msg[4])
        print(number)
        print("")
