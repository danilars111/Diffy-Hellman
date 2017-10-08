import socket
import diffArgs
import sys
import encrypt
import time
import random
from Crypto.Random.random import getrandbits
from Crypto import Random
from Crypto.Util import number
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect():
	confirm = raw_input("Do you want to connect? [y/n]\n")
	
	if(confirm == 'y'):
		#Connect to the port that the server is listening 
		server_adress = ('localhost', 11111)
		print>>sys.stderr, 'Connecting to %s port %s' % server_adress
		sock.connect(server_adress)
		return True
	else:
	    return False
			 


def send_data(message):	
	
	#Send message
	print>>sys.stderr, 'Sending "%s"...' % message
	sock.sendall(str (message))

	#return for response from server
         
	return sock.recv(len(bytes(message)))


def key_exchange():
	KeyLength = 256
        
        #RFC 3526 4096 bit MODP Group 
        #https://www.ietf.org/rfc/rfc3526.txt

        prime = diffArgs.getPrime()	

	generator = diffArgs.getGen()
	
        password = getrandbits(2*KeyLength)

	send_data(prime)
	send_data(generator)
	sk = encrypt.diffyhellman(generator, prime, password)
	sk = send_data(sk)

	sk = encrypt.diffyhellman(int(sk), prime, password)
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
			message = raw_input("What is your message?\n")

			#Until the message is empty
			if (not message):
				print>>sys.stderr, 'Closing Socket..'
				sock.close()
				break

			if init:
				ciphertext = send_data(encrypt.encrypt(sk, message))
				iv = ciphertext
				message = encrypt.decrypt(sk, ciphertext)
				init = False

			else:
				ciphertext = send_data(encrypt.encrypt(sk, message, iv))
				iv = ciphertext
				message = encrypt.decrypt(sk, ciphertext)

			print >> sys.stderr, "Message recieved '%s'" % message

client()
