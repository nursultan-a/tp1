import socketserver
import threading
import socket
import time


ServerAddress = ("", 5050)

# IP adress of each neighbour node
ClientAdress = {
        "r2" :"10.10.8.2",
        "d"  :"10.10.4.2",
        "s"  :"10.10.1.1"
        }

# initiation condition
initiate = True
ThreadList = []

#discovery message number
ThreadCount = 1000
bufferSize = 1024

terminate = ThreadCount*6


rtt_s  = 0
rtt_r2 = 0
rtt_d  = 0

total_time_s  = 0
total_time_r2 = 0
total_time_d  = 0

def get_time():
      return int(round(time.time() * 1000))

# send discovery message to any given address, in this case neighbour nodes
def Connect2Server(address, msg_id):
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    serverAddressPort = (address, 5050)

    start_time = get_time()
    msg = "START_R1*"+str(start_time)+"NA*"+str(msg_id)
    bytesToSend = str.encode(msg)

    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msgFromServer = str(repr(msgFromServer[0])[2:-1])

    msg = "["+address+"] : "+msgFromServer

    print(msg)

    end_time = get_time()

    visited_host = msgFromServer.split("*")[0].split("_")[1].lower()

    global total_time_s
    global total_time_r2
    global total_time_d

    global terminate

    if len(msgFromServer.split("*")) >= 4:
        difference = end_time - start_time
        terminate -= 1

        if(visited_host == "s"):
            total_time_s += difference
        elif(visited_host == "r2"):
            total_time_r2 += difference
        elif(visited_host == "d"):
            total_time_d += difference


        if(terminate == 0):
            print("terminating server! last thread is response(ACK)")
            UDPServerObject.shutdown()
            rtt_s = total_time_s/ThreadCount
            rtt_r2 = total_time_r2/ThreadCount
            rtt_d = total_time_d/ThreadCount

            print("rtt(s-r1): "+str(rtt_s)+" rtt(r2-r1): "+str(rtt_r2)+" rtt(d-r2): "+str(rtt_d))
            f = open("link_cost.txt", "w+")
            f.write(str(rtt_s)+", "+str(rtt_r2)+", "+str(rtt_d))
            f.close()


# respond any request for initiation request and start sending and responding simultaneously
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

        global total_time_s
        global total_time_r2
        global total_time_d

        global UDPServerObject
        # initiated from R2 => send discovery message to : S, R2, D
        if(initiate == True and address == ClientAdress["s"]):
            initiate = False
            for key in ClientAdress:
                for index in range(ThreadCount):
                    ThreadInstance = threading.Thread(target=Connect2Server(ClientAdress[key], index))
                    ThreadList.append(ThreadInstance)
                    ThreadInstance.start()
                #main thread to wait till all connection threads are complete
                for index in range(ThreadCount):
                    ThreadList[index].join()
        
        # respond to requested UDP messages
        else:
            terminate -= 1
            ACK = "ACK_R1*"+datagram
            self.wfile.write(ACK.encode())

            if(terminate == 0):
                UDPServerObject.shutdown()
                rtt_s = total_time_s/ThreadCount
                rtt_r2 = total_time_r2/ThreadCount
                rtt_d = total_time_d/ThreadCount
                print("terminating server! last thread is request")
                print("rtt(s-r1): "+str(rtt_s)+" rtt(r2-r1): "+str(rtt_r2)+" rtt(d-r2): "+str(rtt_d))
                f = open("link_cost.txt", "w+")
                f.write(str(rtt_s)+", "+str(rtt_r2)+", "+str(rtt_d))
                f.close()
UDPServerObject = socketserver.ThreadingUDPServer(ServerAddress,UDPRequestHandler)

UDPServerObject.serve_forever()
