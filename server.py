import socket
import sys
import encrypt
import diffieHellman
from Crypto.Random.random import getrandbits

KEY_LENGTH = 256
MESSAGE_SIZE = 128
BLOCK_SIZE = 128
PRIME_LENGTH = 6144


#Create a tcp/ip socket
sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

#Bind the socket to port 11111
server_adress = ('localhost', 11111)
print >>sys.stderr, 'starting up on %s port %s' % server_adress
sock.bind(server_adress)

#Listen for connection
sock.listen(1)

def echo(data, connection, client_adress):

	if data:
		#print>>sys.stderr, 'sending data back to client'
		connection.sendall(data)
		return data
	else:
		print>>sys.stderr, 'no more data from', client_adress
		return False

def key_exchange(connection, client_adress):
	prime = long(echo(connection.recv(PRIME_LENGTH), connection, client_adress))
	
	generator = long(echo(connection.recv(1), connection, client_adress))
       
        number = getrandbits(2*KEY_LENGTH)	
        
        #Calculates the servers contribution to the shared secretkey
        sk = diffieHellman.calc(generator, prime, number)
        connection.sendall(str(sk))
        
        #Receives the clients part of the shared secret
        sk = connection.recv(PRIME_LENGTH)
        
        #Calculates the shared secret with the clients contribution stored in sk                                        
        sk = diffieHellman.calc(int(sk), prime, number)

        return sk

def connect():
	Connect = True
	while Connect: 
		print >>sys.stderr, 'waiting for connection'
		connection, client_adress = sock.accept()	
		print>>sys.stderr, 'connection from', client_adress
		sk = key_exchange(connection, client_adress)
                encryptionKey = encrypt.hash(sk)
		while True:
                        ciphertext = connection.recv(MESSAGE_SIZE)

			#If data is empty, wait for new connection
                   	if(not ciphertext):
				break;


			data = encrypt.decrypt(encryptionKey, ciphertext)
			print>>sys.stderr, 'received "%s"' % data
			data = encrypt.encrypt(encryptionKey, data, ciphertext)
			print>>sys.stderr, 'sending data back to client'
                        connection.sendall(data)
					

connect()

