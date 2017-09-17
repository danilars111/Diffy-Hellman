import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


confirm = raw_input("Do you want to connect?[y/n]\n")

if(confirm == 'y'):

	#Connect to the port that the server is listening 
	server_adress = ('localhost', 11111)
	print>>sys.stderr, 'connecting to %s port %s' % server_adress
	sock.connect(server_adress) 
	
	while True:
		try:
			#send data
			message = raw_input("What do you want to send?\n")
			if not message:
				print>>sys.stderr, 'closing socket'
				sock.close()
				break
			print>>sys.stderr, 'sending "%s"' % message
			sock.sendall(message)

			#look for response from server
			amount_received = 0
			amount_expected = len(message)

			while amount_received < amount_expected:
				data  = sock.recv(128)
				amount_received += len(data)
				print>>sys.stderr, 'received "%s"' % data
		finally:
			print>>sys.stderr, "Continuing connection..."	
				
print >> sys.stderr, 'Exiting...'
