#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
from socket import *
import sys
import string
 
 
def handleRequest(tcpSocket):
    data = tcpSocket.recv(1024)
    a = data.split("\r\n")
    # print(data)
    print("\n")
 
    tcpSocket.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
    with open('index.html', 'rb') as f:
        tcpSocket.send(f.read())
        tcpSocket.close()
 
 
def start_proxy(destination, port,whatport):
    print('starting a server')
    server = socket(AF_INET, SOCK_STREAM,getprotobyname('tcp'))
    server.bind(('', whatport))
    #setting timeout
    server.settimeout(1)
    server.listen(1)
 
 
   
    print('create socket server<=>proxy')
   
   
   
    while True:
 
 
        print('waiting for user connection')
 
        try:
            user, adr1 = server.accept()
        except timeout:
            continue
        print('Recieved :', adr1)
        #get request
        addresToConnect = user.recv(1024)
        send = addresToConnect.split()
   
        #obtaining url
        web_domain = send[1]
        web_doimain2= web_domain[7:len(web_domain)-1]
   
 
        print('Connecting to the website')
        #set and connect socket between proxy<=>website
        dbsrv  = socket(AF_INET, SOCK_STREAM,getprotobyname('tcp'))
        dbsrv.connect((web_doimain2 , 80))
        dbsrv.sendall(addresToConnect)
 
 
        print('Connection done .... sending request ')
   
   
        print('sent starting loop')
   
 
   
        #recieve response
        website = dbsrv.recv(1000000)
        print(website)
        #send to user
        user.sendall(website)
         
       
        dbsrv.close()
        user.close()
whatport = input('On what port do you want to bind proxy? ')
start_proxy("lancaster.ac.uk",80,whatport)
