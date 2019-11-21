import socketserver
import threading
import socket
import time


ServerAddress = ("", 5050)

# IP adress of each neighbour
ClientAdress = {
        "r3"  :"10.10.7.2",
        "r2"  :"10.10.5.1",
        "r1"  :"10.10.4.1"
        }

initiate = True
ThreadList = []
ThreadCount = 1000
bufferSize = 1024

terminate = ThreadCount*6

def get_time():
      return int(round(time.time() * 1000))

# send dicovery message
def Connect2Server(address, msg_id):
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    serverAddressPort = (address, 5050)

    msg = "START_D*"+str(get_time())+"*NA*"+str(msg_id)
    bytesToSend = str.encode(msg)


    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)

    msg = "["+address+"] : "+str(repr(msgFromServer[0])[2:-1])

    print(msg)

    global terminate
    global UDPServerObject
    if terminate == 0:
        print("Terminateing server! Bye")
        UDPServerObject.shutdown()
    terminate -= 1

# handle any incomming request/message & wait for initiation message, after that start to send discovery messages
class UDPRequestHandler(socketserver.DatagramRequestHandler):
    #override
    def handle(self):
        datagram = str(repr(self.rfile.readline().strip())[2:-1])
        address = "{}".format(self.client_address[0])

        print("[" + address + "] : "+datagram)
        global initiate
        global ThreadCount
        global ThreadList

        global terminate

        # initiated from R2 => send discovery message to : S, R2, D
        if(initiate == True and address == ClientAdress["r2"]):
            initiate = False
            for key in ClientAdress:
                for index in range(ThreadCount):
                    # create thread for each request to neigbour nodes
                    ThreadInstance = threading.Thread(target=Connect2Server(ClientAdress[key], index))
                    ThreadList.append(ThreadInstance)
                    ThreadInstance.start()
                #main thread to wait till all connection threads are complete
                for index in range(ThreadCount):
                    ThreadList[index].join()
        # respond to requested UDP messages
        else:
            terminate -= 1
            ACK = "ACK_D*"+datagram
            self.wfile.write(ACK.encode())

            if terminate == 0:
                print("Shutting down server! Bye")
                UDPServerObject.shutdown()


UDPServerObject = socketserver.ThreadingUDPServer(ServerAddress,UDPRequestHandler)

UDPServerObject.serve_forever()
