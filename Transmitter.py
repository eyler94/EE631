#!/usr/bin/env python3
import numpy as np
import socket
from time import sleep

### Define host IP and port
host = '127.0.0.1'
port = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    message = np.float32(np.random.randint(0,2,(30,3))*255)
    #message = np.float32(np.eye(5,3)*255)
    print("sending: \n", message)
    s.sendto(message, (host,port))
    sleep(0.08)

#for color_iter in range(0,250,10):
#	message = np.float32(np.array([color_iter,0,0]))
#	print("sending: \n", message)
#	s.sendto(message, (host,port))
#	sleep(1)

