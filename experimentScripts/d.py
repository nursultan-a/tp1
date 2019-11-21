import socket

 

localIP     = ""
localPort   = 20001
bufferSize  = 1024
msgFromServer       = ["Hello Source Destination", "My IP for r3, which you using to send me a message is 10.10.7.1"]
condition = 0

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

while(True):

    if condition == 2:
        break
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    clientMsg =repr(message)[2:-1]    
    print("r3->d: "+clientMsg)

    # Sending a reply to client
    if "Hello" in clientMsg:
        bytesToSend = msgFromServer[0].encode()
    else:
        bytesToSend = msgFromServer[1].encode()
    UDPServerSocket.sendto(bytesToSend, address)


    if clientMsg.split("*")[1] == "0":
        condition += 1
