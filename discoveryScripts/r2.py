import socketserver
import threading
import socket
import time


ServerAddress = ("", 5050)

#IP adress of neighbour nodes
ClientAddress = {
        "s"  :"10.10.2.2",
        "r3" :"10.10.6.2",
        "d"  :"10.10.5.2",
        "r1" :"10.10.8.1"

        }
# initiation condition
initiate = True
ThreadList = []

# discovery message number
ThreadCount = 1000
bufferSize = 1024

rtt_s  = 0
rtt_r1 = 0
rtt_r2 = 0
rtt_d  = 0

total_time_s  = 0
total_time_r1 = 0
total_time_r3 = 0
total_time_d  = 0

terminate = ThreadCount*8


def get_time():
      return int(round(time.time() * 1000))

# send discovery request/message to give IP
def Connect2Server(address, msg_id):
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    serverAddressPort = (address, 5050)

    msg = "START_R2*"+str(get_time())+"*NA*"+str(msg_id)
    bytesToSend = str.encode(msg)


    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msgFromServer = str(repr(msgFromServer[0])[2:-1])

    msg = "["+address +"] : "+ msgFromServer

    print(msg)

    end_time = get_time()


    start_time = int(msgFromServer.split("*")[2])
    visited_host = msgFromServer.split("*")[0].split("_")[1].lower()

    global total_time_s
    global total_time_r1
    global total_time_r3
    global total_time_d

    global terminate

    # calculate rtt of each response to requeset
    if len(msgFromServer.split("*")) >= 4:
        difference = end_time - start_time
        terminate -= 1
        
        if visited_host == "s":
            total_time_s += difference
        elif visited_host == "r1":
            total_time_r1 += difference
        elif visited_host == "r3":
            total_time_r3 += difference
        elif visited_host == "d":
            total_time_d += difference
        # if all discovery message handled then terminate server
        if(terminate == 0):
            print("terminating server")
            UDPServerObject.shutdown()
            
            rtt_s = total_time_s/ThreadCount
            rtt_r1 = total_time_r1/ThreadCount
            rtt_r3 = total_time_r3/ThreadCount
            rtt_d = total_time_d/ThreadCount

            print("rtt(s-r2): "+str(rtt_s)+" rtt(r1-r2): "+str(rtt_r1)+" rtt(r3-r2): "+str(rtt_r3)+" rtt(d-r2): "+str(rtt_d))
            f = open("link_costs.txt", "w+")
            f.write(str(rtt_s) +", "+str(rtt_r1)+", "+str(rtt_r3)+", "+str(rtt_d))
            f.close()

# respond any given request and wait for initiation message then initiate and start sending message/request simultaneously
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
        global total_time_r1
        global total_time_r3
        global total_time_d

        global UDPServerObject

        # initiated from S =>initiate D and send discovery message to : R1, R2, R3, S, D
        if(initiate == True and address == ClientAddress["s"]):

            # initiate D
            d_init_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            msg = "initiate message from R2 :)"
            d_init_socket.sendto(str.encode(msg+" start working D"), (ClientAddress["d"], 5050))

            initiate = False

            # send discovery message to near hosts
            for key in ClientAddress:
                for index in range(ThreadCount):
                    ThreadInstance = threading.Thread(target=Connect2Server(ClientAddress[key], index))
                    ThreadList.append(ThreadInstance)
                    ThreadInstance.start()
                #main thread to wait till all connection threads are complete
                for index in range(ThreadCount):
                    ThreadList[index].join()
        
        # respond to requested UDP messages
        else:
            #print("Thread Name: {}".format(threading.current_thread().name))
            terminate -= 1
            ACK = "ACK_R2*"+datagram
            self.wfile.write(ACK.encode())

            #print("condition-ack--------------------"+str(terminate))
            if(terminate == 0):
                print("terminating server")
                UDPServerObject.shutdown()
                
                rtt_s = total_time_s/ThreadCount
                rtt_r1 = total_time_r1/ThreadCount
                rtt_r3 = total_time_r3/ThreadCount
                rtt_d = total_time_d/ThreadCount

                print("rtt(s-r2): "+str(rtt_s)+" rtt(r1-r2): "+str(rtt_r1)+" rtt(r3-r2): "+str(rtt_r3)+" rtt(d-r2): "+str(rtt_d))

                # write to file
                f = open("link_costs.txt", "w+")
                f.write(str(rtt_s) +", "+str(rtt_r1)+", "+str(rtt_r3)+", "+str(rtt_d))
                f.close()



UDPServerObject = socketserver.ThreadingUDPServer(ServerAddress,UDPRequestHandler)

UDPServerObject.serve_forever()
