
#module used for encryption
import sys
from Crypto.Cipher import AES
from Crypto import Random
import base64
import hashlib

def encrypt(key, message):

    #encrypt the message
    BLOCK_SIZE = 16
    PADDING = '{'   
    iv = Random.new().read(AES.block_size)
                                                        
    #Function that the message is a multiple of the block size
    pad = lambda s: s + ((BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING)
                                                                    
    #Produces a ciphertext that consists of (A-Z, a-z, 0-9,+,/
    EncodeAES = lambda c, s, iv: base64.b64encode(iv + c.encrypt(pad(s)))
                                                                                 
    #Creates the cipher that the messege is to be encrypted with
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    #Encrypts the message with the cipher and produces a ciphertext
    ciphertext = EncodeAES(cipher, message, iv)

    return ciphertext

def decrypt (key,ciphertext):
    PADDING = '{'

    DecodeAES = lambda c, e: c.decrypt(e).rstrip(PADDING)
                                                                                                                                  
                                                                                                                                              
    ciphertext = base64.b64decode(ciphertext)

    iv = ciphertext[:AES.block_size]

    cipher = AES.new(key, AES.MODE_CBC, iv)
                                                                                                                                                              
    decoded = DecodeAES(cipher, ciphertext[16:])

    #print('Decrypted string:', decoded, file=sys.stderr)
    #print>>sys.stderr, 'Decrypted: %s' % decoded                                                                                                                            
    return decoded

def hash(password):

    #hashes the password with sha256 to get a encryptionkey of 32 bytes
    key = hashlib.sha256(str(password).encode()).digest()
    
    return key
