import socket
import sys
import encrypt
import base64
from Crypto.Util import number
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

length = 4096
prime = number.getPrime(length)
print >> sys.stderr, 'Prime: %s' % prime
print >> sys.stderr, 'Len(Prime): %s' % len(str(prime))
generator = 48589
number = 12222

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
		iv = None
		init = True

		#Do a Diffy-Hellman key exchange
		sk = key_exchange()
		#Keep going
		while True:
			message = raw_input("What is your message\n")
			#Until the message is empty
			if (not message):
				print>>sys.stderr, 'closing socket'
				sock.close()
				break
			if init:
				ciphertext = send_data(encrypt.encrypt(sk, message))
				iv = ciphertext
				print >> sys.stderr, "IV '%s'" % iv
				message = encrypt.decrypt(sk, ciphertext)
				init = False
			else:
				ciphertext = send_data(encrypt.encrypt(sk, message, iv))
				iv = ciphertext
				print >> sys.stderr, "IV22 '%s'" % iv
				message = encrypt.decrypt(sk, ciphertext)

			print >> sys.stderr, "Message recieved '%s'" % message

client()
