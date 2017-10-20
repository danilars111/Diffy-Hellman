import socket
import sys
import time
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

def bind():
    success = False
    for x in range(0,5):
        try:
            sock.bind(server_adress)
        
        except socket.error:
            print>>sys.stderr,'Adress already in use, retrying in 5 seconds'
            time.sleep(5)
            continue

        success = True
        break

    #Listen for connection
    if success:
        sock.listen(1)

    return success

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
        secretKey= diffieHellman.calc(generator, prime, number)
        
        connection.sendall(str(secretKey))
        
        #Receives the clients part of the shared secret
        secretKey = connection.recv(PRIME_LENGTH)
         
        #Calculates the shared secret with the clients contribution stored in sk                                        
        secretKey = diffieHellman.calc(int(secretKey), prime, number)

        return secretKey

def connect():
    if not bind():
        print>>sys.stderr,'Closing down.. Failed to bind to socket'
        return

    Connect = True
    while Connect: 
	    print >>sys.stderr, 'waiting for connection'
	    connection, client_adress = sock.accept()	
	    print>>sys.stderr, 'connection from', client_adress
	    secretKey = key_exchange(connection, client_adress)
            encryptionKey = encrypt.hash(secretKey)
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

