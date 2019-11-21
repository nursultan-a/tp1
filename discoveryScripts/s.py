import socketserver
import threading
import socket
import time


ServerAddress = ("", 5050)

# all possible ip adress of neighbours
ClientAddress = {
        "r1" :"10.10.1.2",
        "r3" :"10.10.3.2",
        "r2" :"10.10.2.1"
        }
initiate = True
ThreadList = []
ThreadCount = 1000
bufferSize = 1024

terminate = ThreadCount*6 - 1

flag = (ThreadCount*3) 

# initiate hosts: R2, R3, D
r1_init_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
r2_init_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
r3_init_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

msg = "initiate message from S :)"
r1_init_socket.sendto(str.encode(msg+" start working R1"), (ClientAddress["r1"], 5050))
r2_init_socket.sendto(str.encode(msg+" start working R2"), (ClientAddress["r2"], 5050))
r3_init_socket.sendto(str.encode(msg+" start working R3"), (ClientAddress["r3"], 5050))

def get_time():
      return int(round(time.time() * 1000))

#send message to any given ip simultaneously
def Connect2Server(address, msg_id):
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    serverAddressPort = (address, 5050)

    msg = "START_S*"+str(get_time())+"*"+str(msg_id)
    bytesToSend = str.encode(msg)


    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = "[" + address +"] :" +str(repr(msgFromServer[0])[2:-1])

    print(msg)
    global terminate
    global UDPServerObject

    terminate -= 1
    if terminate == 0:
        print("Terminating server! Bye")
        UDPServerObject.shutdown()


# start sending descovery message and replying to request
class UDPRequestHandler(socketserver.DatagramRequestHandler):

    #override
    def handle(self):
        global flag
        flag -= 1
        datagram = str(repr(self.rfile.readline().strip())[2:-1])
        address = "{}".format(self.client_address[0])

        print("[" + address + "] : "+datagram)

        global initiate
        global TreadCount
        global ThreadList
        global terminate
        global UDPServerObject

        #self initiation => send discovery messages to : R3, R2, R1
        if flag > 0:
            ACK = "ACK_S*"+datagram
            self.wfile.write(ACK.encode())
            terminate -= 1
            if terminate == 0:
                print("terminating server!")
                UDPServerObject.shutdown()
        elif(initiate == True):
            ACK = "ACK_S*"+datagram
            self.wfile.write(ACK.encode())
            initiate = False
            for key in ClientAddress:
                for index in range(ThreadCount):
                    ThreadInstance = threading.Thread(target=Connect2Server(ClientAddress[key], index))
                    ThreadList.append(ThreadInstance)
                    ThreadInstance.start()

                for index in range(ThreadCount):
                    ThreadList[index].join()

UDPServerObject = socketserver.ThreadingUDPServer(ServerAddress,UDPRequestHandler)

UDPServerObject.serve_forever()
