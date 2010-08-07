#!/usr/bin/env python 

""" 
A simple echo server 
""" 

import socket 
import pygame
from pygame import *

images = {}

def load_images():
    for piece_char in [str(x) for x in range(1,10)] + ['s', 'b', 'f']:
        images['red' + piece_char] = image.load('red' + piece_char + '.png').convert()
        images['blue' + piece_char] = image.load('blue' + piece_char + '.png').convert()

board = """
..........
..........
..........
..........
..XX..XX..
..XX..XX..
..........
..........
..........
..........
"""

if int(raw_input("0 = server, 1 = client\n")) == 0:
    print "server"

    host = '' 
    port = 50000 
    backlog = 5 
    size = 1024 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((host,port)) 
    s.listen(backlog) 
    while 1: 
        client, address = s.accept() 
        data = client.recv(size) 
        if data: 
            print data
            client.send(data) 
        client.close()
    
else:
    print "client"
    host = 'localhost' 
    port = 50000 
    size = 1024 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.connect((host,port)) 
    s.send(board) 
    data = s.recv(size) 
    s.close() 
    print 'Received:\n', data

