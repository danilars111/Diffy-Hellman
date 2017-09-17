import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#confirm = input("Do you want to connect?[y/n]")

#if(confirm == 'y'):

#Connect to the port that the server is listening 
server_adress = ('localhost', 11111)
print>>sys.stderr, 'connecting to %s port %s' % server_adress
sock.connect(server_adress) 

try: 
	#send data
	message = 'This is the message. It will be repeated.'
	print>>sys.stderr, 'sending "%s"' % message
	sock.sendall(message)

	#look for response from server
	amount_received = 0
	amount_expected = len(message)

	while amount_received < amount_expected:
		data  = sock.recv(16)
		amount_received += len(data)
		print>>sys.stderr, 'received "%s"' % data

finally:
	print>>sys.stderr, 'closing socket'
	sock.close()
