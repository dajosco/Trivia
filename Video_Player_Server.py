#!/usr/bin/python

import socket
import os
import sys
from pyomxplayer import OMXPlayer

UDP_IP = "" # "192.168.1.79" direccion de la Rasp Pi     Canada=192.168.2.200   ARGENTINA=192.168.0.107
UDP_PORT = 12121

# Create UDP socket
try:
    sock = socket.socket(socket.AF_INET, #Internet
           socket.SOCK_DGRAM) #UDP
    print "Socket created"
except socket.error, msg:
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

# Bind socket to local host and port
try:
    sock.bind((UDP_IP, UDP_PORT))
except socket.error, msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
print 'Socket bind complete'

#now keep talking with the client
running = 0
while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes

        print "Received mesage:", data,"!"

        if running == 0:
                if "Video" in data:
                        omx = OMXPlayer("//home/pi/Desktop/archivos/testmp4.mp4")   # TODO try except
                        running = 1
                if "Descensor" in data:
                        omx = OMXPlayer("//home/pi/Desktop/archivos/Descensor1.mp4")
                        running = 1
                if "Simpsons" in data:
                        omx = OMXPlayer("//home/pi/Desktop/archivos/Simpsons.mov")
                        running = 1
        else:
                if "Pause" in data:
                        omx.toggle_pause()
                if "Stop" in data:
                        omx.stop()
                        running = 0
        
        if "Exit" in data:
                if running == 1:
                        omx.stop()
                        running = 0
                break
    
sock.close()
