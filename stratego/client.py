import socket
import sys
import cPickle



HOST, PORT = "localhost", 10000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
while 1:
    sock.send("move\n")
    board = cPickle.loads(sock.recv(100000))
    print board


sock.close()
