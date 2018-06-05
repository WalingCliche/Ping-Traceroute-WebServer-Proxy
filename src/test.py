#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
from socket import *
import sys
import string
import threading
 
 
def handleRequest(tcpSocket):
    try:
        #reciving request
        data = tcpSocket.recv(1024)
        a = data.split()[1]
        #split to get the file
        web_domain = a[1:]
    
        #print(web_domain)
        #header
        tcpSocket.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
        with open(web_domain, 'rb') as f:
            tcpSocket.send(f.read())
            
    except IOError:
        print('ok')
        with open('error.html', 'rb') as f:
            tcpSocket.send(f.read())
            tcpSocket.close()
    finally:
          tcpSocket.close()
 

 
 
def startServer(serverAddress, serverPort):
    print('How many concurrent connection do you want')
    howmany = input()
    serversocket = socket(
        AF_INET, SOCK_STREAM)
    #setting up server
    serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    print('waiting for user input')
    serverPort = input()
    print('setting up the server')
    serversocket.bind((serverAddress, serverPort))
    serversocket.listen(howmany)
    
    threads=[]
    #threading for connections
    while howmany >0:  
        
        try:
            questSocket = serversocket.accept()[0]
        except socket.timeout:
            continue
        print(howmany)
        #starting new thread
        t = threading.Thread(target=handleRequest, args=(questSocket,))
        t.start()
       
        threads.append(t)
        howmany-=1
        t.join()
        if(howmany==0):
            serversocket.close()
        
        
    

        
        
 
 
 
 

startServer("", 8000)

