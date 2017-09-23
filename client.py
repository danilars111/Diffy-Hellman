import socket
import sys
import encrypt

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


prime = 11
generator = 5
number = 12

def connect():
	confirm = raw_input("Do you want to connect?[y/n]\n")
	
	if(confirm == 'y'):
		#Connect to the port that the server is listening 
		server_adress = ('localhost', 11111)
		print>>sys.stderr, 'connecting to %s port %s' % server_adress
		sock.connect(server_adress)
		return True
	else:
		return False
			 


def send_data(message):	
	
	#Send message
	print>>sys.stderr, 'sending "%s"' % message
	sock.sendall(str (message))

	#return for response from server
         
	return sock.recv(128)

def key_exchange():
	
	sk = encrypt.diffyhellman(generator, prime, number)
	sk = send_data(sk)

	sk = encrypt.diffyhellman(int(sk), prime, number)
	print >> sys.stderr, "Your super secret key is '%s'" % sk

	return sk

def client():
	if connect():
		#Do a Diffy-Hellman key exchange
		sk = key_exchange()
		#Keep going
		while True:
			message = raw_input("What is your message\n")
			#Until the message is empty
			if (message == ""):
				print>>sys.stderr, 'closing socket'
				sock.close()
				break

			print >> sys.stderr, "Message recieved '%s'" % send_data(message)

client()
