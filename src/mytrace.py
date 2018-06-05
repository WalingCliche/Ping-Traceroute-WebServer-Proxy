#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
from socket import *
import os
import sys
import struct
import time
import select
import binascii  
 
from random import randint
 
 
ICMP_ECHO_REQUEST = 8 #ICMP type code for echo request messages
ICMP_ECHO_REPLY = 11 #ICMP type code for echo reply messages
 
def checksum(string): 
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0
 
    while count < countTo:
        thisVal = ord(string[count+1]) * 256 + ord(string[count]) 
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
     
def createPacket(icmpSocket, destinationAddress, ID):
    # 1. Build ICMP header
    # 2. Checksum ICMP packet using given function
    # 3. Insert checksum into packet
    # 4. Send packet using socket
    # 5. Record time of sending
 
    header = struct.pack('BBHHH', ICMP_ECHO_REQUEST, 0, 0, ID, 1)
    checksumResult = checksum(header)
    header = struct.pack('BBHHH', ICMP_ECHO_REQUEST, 0, checksumResult, ID, 1)
 
    return header
     
def trace(destinationAddress, port, numHops):
    #previously covered
    icmp = getprotobyname('icmp')
    address = gethostbyname(destinationAddress)
    ttl = 1
    print("traceroute to " + str(address) + ", " + str(numHops) + " hops max")
     
    while True:
        #measure the time
        currentTime = time.time()
        #setting sockets and create packets
        traceS = socket(AF_INET, SOCK_RAW, icmp)
        packet = createPacket(traceS, destinationAddress, 10)
        traceS.setsockopt(SOL_IP, IP_TTL, ttl)
         
        print(" " + str(ttl) + " "),
        traceS.sendto(packet, (address, port))
        try:
            blank, hopAddr = traceS.recvfrom(1024)
            
            hopAddr = hopAddr[0]
            arrivalTime = time.time()
        except socket.error as (errno,errmsg):
            print('*')
        traceS.close()
         
        print(hopAddr),
        print("----- " + str(round((arrivalTime-currentTime)*1000)) + " ms")
        ttl += 1
        #exceeding hops
        if ttl > numHops or address == hopAddr:
            break
 
trace('lancaster.ac.uk', 80, 10)
