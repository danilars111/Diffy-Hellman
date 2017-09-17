import socket
import sys

#Create a tcp/ip socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind the socket to port 11111

server_adress = ('localhost', 11111)
print >>sys.stderr, 'starting up on %s port %s' % server_adress
sock.bind(server_adress)


#MAAAAAAAAARRIIIIN

