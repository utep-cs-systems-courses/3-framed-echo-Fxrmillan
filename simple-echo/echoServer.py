#! /usr/bin/env python3

# Echo server program

import socket, sys, re
import os
from os import read, write
sys.path.append("../lib")       # for params
import params
def getNamesAndSizes(tempStr):
    if tempStr.find("b'") != -1:
        tempStr = tempStr[tempStr.find("b'") + 2:]
    return tempStr.split(",")

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )



progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets

conn, addr = s.accept()  # wait until incoming connection request (and accept it)
counter =0
namesAndSizes =[]
tarFile = 0
print('Connected by', addr)
while 1:
    data = conn.recv(1024).decode()
    if len(data) == 0:
        print("Zero length read, nothing to send, terminating")
        break
    sendMsg = str("Error").encode()
    if counter == 0:
        namesAndSizes = getNamesAndSizes(data)
        counter += 1
        sendMsg = str("recived").encode()
    elif counter > 0:
        tarFile = data
    print("Received '%s', sending '%s'" % (data, sendMsg.decode()))
    while len(sendMsg):
        bytesSent = conn.send(sendMsg)
        sendMsg = sendMsg[bytesSent:0]
conn.shutdown(socket.SHUT_WR)
conn.close()
print(namesAndSizes)
print(tarFile)


