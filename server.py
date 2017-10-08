import socket
import sys
import encrypt
from Crypto.Random.random import getrandbits

KEY_LENGTH = 256
MESSAGE_SIZE = 128
BLOCK_SIZE = 128
PRIME_LENGTH = 4096


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
		print>>sys.stderr, 'sending data back to client'
		connection.sendall(data)
		return data
	else:
		print>>sys.stderr, 'no more data from', client_adress
		return False

def key_exchange(connection, client_adress):
	prime = long(echo(connection.recv(PRIME_LENGTH), connection, client_adress))
	#print >> sys.stderr, 'Recieved Prime: %s' % str(prime)
	
	generator = long(echo(connection.recv(1), connection, client_adress))
	#print >> sys.stderr, 'Recieved Generator: %s' % str(generator)
       
        number = getrandbits(2*KEY_LENGTH)	

        sk = encrypt.diffyhellman(generator, prime, number)
        connection.sendall(str(sk))
        sk = connection.recv(PRIME_LENGTH)
        #print >> sys.stderr, 'Recieved key from client: %s' % sk                                
                                                
        sk = encrypt.diffyhellman(int(sk), prime, number)
        #print >> sys.stderr, "Your super secret key is '%s'" % sk

        return sk

def connect():
	Connect = True
	while Connect: 
		print >>sys.stderr, 'waiting for connection'
		connection, client_adress = sock.accept()	
		print>>sys.stderr, 'connection from', client_adress
		sk = key_exchange(connection, client_adress)
	
		while True:
                        ciphertext = connection.recv(MESSAGE_SIZE)

			#If data is empty, close the socket
                   	if(not ciphertext):
		       		print>>sys.stderr, 'closing socket'
		       		sock.close()
				Connect = False
				break;


			data = encrypt.decrypt(sk, ciphertext)
			print>>sys.stderr, 'received "%s"' % data
			data = encrypt.encrypt(sk, data, ciphertext)
			print>>sys.stderr, 'sending "%s" back to client' % data
                        connection.sendall(data)
					

connect()
