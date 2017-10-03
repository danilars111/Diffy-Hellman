import socket
import sys
import encrypt

#prime = 47791
#generator = 48589
#number = 98222




#Create a tcp/ip socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

	prime = long(echo(connection.recv(4096), connection, client_adress))
	print >> sys.stderr, 'Recieved Prime: %s' % str(prime)
	
	generator = long(echo(connection.recv(4096), connection, client_adress))
	print >> sys.stderr, 'Recieved Generator: %s' % str(generator)
	
	number = 5
        
        skClient = long(echo(connection.recv(4096), connection, client_adress))
        print>> sys.stderr, 'Recieved sk: %s' % str(skClient)

        sk = encrypt.diffyhellman(generator, prime, number)
        connection.sendall(str(sk))
        
        
        
        sk = encrypt.diffyhellman(skClient, prime, number)
        print >> sys.stderr, "Your super secret key is '%s'" % sk

        return sk

def connect():
	Connect = True
	while Connect: 
		print >>sys.stderr, 'waiting for connection'
		connection, client_adress = sock.accept()	
		print>>sys.stderr, 'connection from', client_adress
		sk = key_exchange(connection, client_adress)
	
		while True:
                        ciphertext = connection.recv(128)
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
