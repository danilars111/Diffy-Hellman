import socket
import sys
import encrypt
import time
import random
from Crypto import Random
from Crypto.Util import number
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
         
	return sock.recv(2048)


def key_exchange():
	PrimeLength = 128
	KeyLength = 32

	prime = number.getPrime(PrimeLength)
	print >> sys.stderr, 'Prime: %s' % prime
	print >> sys.stderr, 'Len(Prime): %s' % len(str(prime))

	#NOT CSPRNG!!!!!
	generator = random.getrandbits(2*KeyLength)
	print >> sys.stderr, 'Generator: %s' % str(generator)
	print >> sys.stderr, 'Len(Generator): %s' % len(str(generator))
	password = 12222

	temp = send_data(prime)
	temp = send_data(generator)
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
				print >> sys.stderr, "IV2 '%s'" % iv
				message = encrypt.decrypt(sk, ciphertext)

			print >> sys.stderr, "Message recieved '%s'" % message

client()
