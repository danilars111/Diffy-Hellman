#Module used for encryption
import sys
#from Crypto.Cipher import AES
#import base64

#import hashlib

#def encrypt(password,message):
    #encrypt the message
<<<<<<< HEAD
#    BLOCK_SIZE = 32
#    PADDING = '{'
    
    #Function that the message is a multiple of the block size
#    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
    
    #Produces a ciphertext that consists of (A-Z, a-z, 0-9,+,/
#    EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
    
    #hashes the password with sha256 to get a encryptionkey of 32 bytes
#    key = hashlib.sha256((password).to_bytes(2, byteorder='big')).digest()
    
    #Creates the cipher that the messege is to be encrypted with
#    cipher = AES.new(key)
    
    #Encrypts the message with the cipher and produces a ciphertext
#    ciphertext = EncodeAES(cipher, message)
#    print('Encrypted string:', ciphertext, file=sys.stderr)
=======
    BLOCK_SIZE = 16
    PADDING = '{'

    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

    EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
   

    cipher = AES.new(pad(key))
    
    encoded = EncodeAES(cipher, message)
    print>>sys.stderr, 'Encrypted string:', encoded


def diffyhellman(gen, prime, i):
	#gen and prim are agreed upon values and i is a private secret
	return gen**i % prime


#encrypt(3,'hej')

