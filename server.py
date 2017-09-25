import socket
import sys
import encrypt

prime = 47791
generator = 48589
number = 98222




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
		#print>>sys.stderr, 'sending data back to client'
		connection.sendall(data)
		return connection.recv(128)
	else:
		print>>sys.stderr, 'no more data from', client_adress
		return False

def key_exchange(connection, client_adress):

        sk = encrypt.diffyhellman(generator, prime, number)
        sk = echo(str(sk), connection, client_adress)
        
        sk = encrypt.diffyhellman(int(sk), prime, number)
        print >> sys.stderr, "Your super secret key is '%s'" % sk

        return sk

def connect():
	while True: 
		print >>sys.stderr, 'waiting for connection'
		connection, client_adress = sock.accept()	
		try:	
			print>>sys.stderr, 'connection from', client_adress
			sk = key_exchange(connection, client_adress)
	
			while True:
				data = connection.recv(128)
				print>>sys.stderr, 'received "%s"' % data
				print>>sys.stderr, 'received "%s"' % encrypt.decrypt(sk, data)
				if data:
                                    connection.sendall(encrypt.decrypt(sk, data))
                                else:
                                    break
					
		finally:
                    if(data == ""):
		         print>>sys.stderr, 'closing socket'
		         sock.close()

connect()
