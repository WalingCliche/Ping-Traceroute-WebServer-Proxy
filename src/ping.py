#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
from socket import *
import os
import sys
import struct
import time
import select
import binascii
 
ICMP_ECHO_REQUEST = 8  # ICMP type code for echo request messages
ICMP_ECHO_REPLY = 0  # ICMP type code for echo reply messages
 
 
def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0
 
    while count < countTo:
        thisVal = ord(string[count + 1]) * 256 + ord(string[count])
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2
 
    if countTo < len(string):
        csum = csum + ord(string[len(string) - 1])
        csum = csum & 0xffffffff
 
    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
 
    if sys.platform == 'darwin':
        answer = htons(answer) & 0xffff
    else:
        answer = htons(answer)
 
    return answer
 
 
def receiveOnePing(icmpSocket, destinationAddress, ID, timeout):
    # 1. Wait for the socket to receive a reply
    timeRemaining = timeout
 
    rdy = select.select([icmpSocket], [], [], timeout)
    if len(rdy[0]) == 0:  # Timeout
        return
    timeRecieved = time.time()
    recPckt, adr = icmpSocket.recvfrom(4096)
    icpm_header = recPckt[20:28]
    bytes = struct.calcsize("d")
    type, code, checksum, p_id, sequence = struct.unpack(
        'bbHHh', icpm_header)
    times = recPckt[28:]
    timeSent =struct.unpack("d", recPckt[28:28 + bytes])[0]

    
    
    if ID == p_id:
        print (round((timeRecieved - struct.unpack('d', times)[0])*1000,1), 'recieved from ',destinationAddress)
        ping = (round((timeRecieved - struct.unpack('d', times)[0])*1000,1))
        
        x=timeRecieved - timeSent
    return x
 
 
 
    # 2. Once received, record time of receipt, otherwise, handle a timeout
    # 3. Compare the time of receipt to time of sending, producing the total network delay
    # 4. Unpack the packet header for useful information, including the ID
    # 5. Check that the ID matches between the request and reply
    # 6. Return total network delay
 
 
def sendOnePing(icmpSocket, destinationAddress, ID):
    # 1. Build ICMP header
    header = struct.pack('BBHHH', 8, 0, 0, ID, 1)
    data = struct.pack('d', time.time())
    # 2. Checksum ICMP packet using given function
    chcksm = checksum(header + data)
    # 3. Insert checksum into packet
    header = struct.pack('BBHHH', 8, 0, chcksm, ID, 1)
    packet = header + data
    # 4. Send packet using socket
    icmpSocket.sendto(packet, (destinationAddress, 1))
 
 
 
 
    # 1. Build ICMP header
    # 2. Checksum ICMP packet using given function
    # 3. Insert checksum into packet
    # 4. Send packet using socket
    #  5. Record time of sending
    # pass  # Remove/replace when function is complete
 
 
def doOnePing(destinationAddress, timeout):
    icmp_socket = getprotobyname("icmp")
 
    my_socket = socket(AF_INET, SOCK_RAW, icmp_socket)
    ID = os.getpid() & 0xFFFF  # getting id of the process
 
    sendOnePing(my_socket, destinationAddress, ID)
    delay =receiveOnePing(my_socket, destinationAddress, ID, timeout)
 
    my_socket.close()
    return delay
 
    # 1. Create ICMP socket
    # 2. Call sendOnePing function
    # 3. Call receiveOnePing function
    # 4. Close ICMP socket
    # 5. Return total network delay
    # pass  # Remove/replace when function is complete
 
 
 
 
def ping(host, timeout,iterats):
    ip = gethostbyname(host)
    starttime = time.time()
 
    
    counter =0
    maximum=0
    minimum=0
    packetloss=0
    average=0

    while(counter < iterats):
        delay = doOnePing(ip, timeout)

 	
        time.sleep(1)
        if delay ==0:
            packetloss+=1
        else:
            
            delay = delay *1000
            minimum=delay
            if(delay > maximum):
                maximum=delay
            if(minimum > delay):
                minimum=delay
             
        counter +=1
    print('max ping was',round(maximum,1))
    print('minimum ping was',round(minimum,1))
    
    
    print('Packets lost',packetloss) 
            
        # 1. Look up hostname, resolving it to an IP address
        # 2. Call doOnePing function, approximately every second
        # 3. Print out the returned delay
        # 4. Continue this process until stopped
        # pass  # Remove/replace when function is complete

iterates = input('how many ping you want to send')
timeout = input('what timeout do you fancy my lord')
ping("lancaster.ac.uk",timeout,iterates)
