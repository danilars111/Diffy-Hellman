#Module used for encryption
import sys
from Crypto.Cipher import AES
import base64
import hashlib

def encrypt(password,message):

    #encrypt the message
    BLOCK_SIZE = 32
    PADDING = '{'
    
    #Function that the message is a multiple of the block size
    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
    
    #Produces a ciphertext that consists of (A-Z, a-z, 0-9,+,/
    EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
    
    #hashes the password with sha256 to get a encryptionkey of 32 bytes
    key = hashlib.sha256(str(password).encode()).digest()
    
    #Creates the cipher that the messege is to be encrypted with
    cipher = AES.new(key)
    
    #Encrypts the message with the cipher and produces a ciphertext

    ciphertext = EncodeAES(cipher, message)
    #print('Encrypted string:', ciphertext, file=sys.stderr)

    return ciphertext

def decrypt (password,ciphertext):
    PADDING = '{'

    DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
  
    key = hashlib.sha256(str(password).encode()).digest()
   
    cipher = AES.new(key)
    
    decoded = DecodeAES(cipher, ciphertext)

   #print('Decrypted string:', decoded, file=sys.stderr)
    return decoded
def diffyhellman(gen, prime, i):
	#gen and prim are agreed upon values and i is a private secret
	return gen**i % prime

