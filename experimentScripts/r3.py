
# interlink on shortes path from s node to d

import socket
localIP     = ""

localPort   = 20001

bufferSize  = 1024

 

msgFromR3ForD = "[s->r3->d]"
msgFromR3ForS = "[d->r3->s]"
condition = 0

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

 

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("r3 Up and ready to redirect")

# Listen source node incoming datagrams
while(True):

    if condition == 2:
        break
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    clientMsg = repr(message)[2:-1]
    if clientMsg.split("*")[1] == "0":
        condition += 1
    print("s->d: "+clientMsg)


    #redirect message from source to destination
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 

    serverAddressPort = ("10.10.7.1", 20001)
    bytesToSend = (clientMsg+msgFromR3ForD).encode()

    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = repr(str(msgFromServer[0])[2:-1])
    print("d->s: "+msg+msgFromR3ForS)
    # Sending a reply to client

    # redirect response from d to s
    UDPServerSocket.sendto(msg.encode(), address)
