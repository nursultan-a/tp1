<!--1906841 Nursultan ABDRAKYPOV-->
<!--Talgat TYNAEV-->

#Use python 3.6.5

#Each node only execute one script

#Initiation Scenario:

    Node s initiates  r1, r2,r3
    Node r2 initiates d

Thus, follow the following instructions

******************************************************************************
***                              discovery                                 ***
******************************************************************************
script execution to find rtt of each node:
    first  : upload  r3.py  to  r3 node and execute uploaded python code r3.py
    second : upload  r1.py  to  r1 node and execute uploaded python code r1.py
    first  : upload  d.py   to  d  node and execute uploaded python code d.py
    first  : upload  r2.py  to  r2 node and execute uploaded python code r2.py
    first  : upload  s.py   to  s  node and execute uploaded python code s.py

******************************************************************************
***                           experiment                                   ***
******************************************************************************

experiment 1:

    first step: 
    
        go to terminal on node d
        
        execute following command
        
            [sudo tc qdisc add dev eth2 root netem delay 20ms 5ms distribution normal]
            
            upload d.py from experimentFolder and execute it
            
    second step: 
    
        go to terminal on node r3
        
        execute following command
        
            [sudo tc qdisc add dev eth3 root netem delay 20ms 5ms distribution normal]
            
            [sudo tc qdisc add dev eth1 root netem delay 20ms 5ms distribution normal]
            
            upload r3.py from experimentFolder and execute it
            
    third step: 
    
        go to terminal on node r3
        
        execute following command
        
            [sudo tc qdisc add dev eth1 root netem delay 20ms 5ms distribution normal]
            
            upload s.py from experimentFolder and execute it
            
experiment 2:

    first step: 
    
        go to terminal on node d
        
        execute following command
        
            [sudo tc qdisc add dev eth2 root netem delay 40ms 5ms distribution normal]
            
            upload d.py from experimentFolder and execute it
            
    second step: 
    
        go to terminal on node r3
        
        execute following command
        
            [sudo tc qdisc add dev eth3 root netem delay 40ms 5ms distribution normal]
            
            [sudo tc qdisc add dev eth1 root netem delay 40ms 5ms distribution normal]
            
            upload r3.py from experimentFolder and execute it
            
    third step: 
    
        go to terminal on node r3
        
        execute following command
        
            [sudo tc qdisc add dev eth1 root netem delay 40ms 5ms distribution normal]
            
            upload s.py from experimentFolder and execute it
            

experiment 3:

    first step: 
    
        go to terminal on node d
        
        execute following command
        
            [sudo tc qdisc add dev eth2 root netem delay 50ms 5ms distribution normal]
            
            upload d.py from experimentFolder and execute it
            
    second step: 
    
        go to terminal on node r3
        
        execute following command
        
            [sudo tc qdisc add dev eth3 root netem delay 50ms 5ms distribution normal]
            
            [sudo tc qdisc add dev eth1 root netem delay 50ms 5ms distribution normal]
            
            upload r3.py from experimentFolder and execute it
            
    third step: 
    
        go to terminal on node r3
        
        execute following command
        
            [sudo tc qdisc add dev eth1 root netem delay 50ms 5ms distribution normal]
            
            upload s.py from experimentFolder and execute it
            


You can also directly change the delay settings by using following command:

example: [sudo tc qdisc change dev eth3 root netem delay 50ms 5ms distribution normal]



Delete delay configuration from internet:

[sudo tc qdisc change dev <eth> root netem]
    
