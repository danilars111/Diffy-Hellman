import socket
import sys

#Create a tcp/ip socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind the socket to port 11111

server_adress = ('localhost', 11111)
print >>sys.stderr, 'starting up on %s port %s' % server_adress
sock.bind(server_adress)


#Listen for connection
sock.listen(1)

while True: 
	print >>sys.stderr, 'waiting for connection'
	connection, client_adress = sock.accept()	
	try:	
		print>>sys.stderr, 'connection from', client_adress
	
		while True:
			data = connection.recv(128)
			print>>sys.stderr, 'received "%s"' % data
			if data:
				#print>>sys.stderr, 'sending data back to client'
				connection.sendall(data)
			else:
				print>>sys.stderr, 'no more data from', client_adress
				break
	finally:
		if(data == ""):
			print>>sys.stderr, 'closing socket'
			sock.close()
