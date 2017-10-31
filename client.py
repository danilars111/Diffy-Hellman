import socket
import diffieHellman
import sys
import encrypt
import time
from Crypto.Random.random import getrandbits
from Crypto import Random
from Crypto.Util import number

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
MESSAGE_SIZE = 80

def connect():
    while True:
        confirm = raw_input("Do you want to connect? [y/n]\n")
	
	if(confirm == 'y'):
		#Connect to the port that the server is listening 
		server_adress = ('localhost', 11111)
		print>>sys.stderr, 'Attempting to connect to %s port %s\n' % server_adress
                try:
                    sock.connect(server_adress)
               
                except socket.error:
                    print>>sys.stderr,'Could not connect to socket\n'
                    continue
                
                print>>sys.stderr,'Connection established\n'
                return True
	else:
	    return False
			 


def send_data(message):	
	
	#Send message
        sock.sendall(bytes (message))
	#return for response from server
	return sock.recv(len(bytes(message)))


def key_exchange():
	KEYLENGTH = 256
        PRIME_LENGTH = 6144 
        #RFC 3526 4096 bit MODP Group 
        #https://www.ietf.org/rfc/rfc3526.txt

        prime = diffieHellman.getPrime()	
    
	generator = diffieHellman.getGen()
	
        password = getrandbits(2*KEYLENGTH)

	send_data(prime)
	send_data(generator)

        #Calculates the clients contribution to the shared secretkey
        
        secretKey = diffieHellman.calc(generator, prime, password)
    
	sock.sendall(bytes(secretKey))
        secretKey = sock.recv(PRIME_LENGTH)
        
        #Calculates the shared secret with the servers contribution stored in secretKey
	secretKey = diffieHellman.calc(int(secretKey), prime, password)
	return secretKey

def client():
	if connect():

		#Do a Diffy-Hellman key exchange
		secretKey = key_exchange()
	        encryptionKey = encrypt.hash(secretKey)
                #Keep going
		while True:
			message = raw_input("What is your message?\n")
			if len(message) > MESSAGE_SIZE:
				print>>sys.stderr, 'Message Exceeding the character limit of %s \nTry Again!\n' % MESSAGE_SIZE
				continue

			#Until the message is empty
			if (not message):
				print>>sys.stderr, 'Closing Socket..'
				sock.close()
				break
                        
                        #Send and recieve data to server 
			ciphertext = send_data(encrypt.encrypt(encryptionKey, message))
			message = encrypt.decrypt(encryptionKey, ciphertext)

			print >> sys.stderr, "Message recieved '%s'" % message

client()
