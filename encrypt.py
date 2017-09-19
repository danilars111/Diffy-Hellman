#Module used for encryption
import sys
from Crypto.Cipher import AES
import base64
import os

def encrypt(key,message):
    #encrypt the message
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

encrypt(3,'hej')
