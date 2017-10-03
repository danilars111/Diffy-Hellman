import sys
import math
import random
from Crypto.Util import number
from Crypto import Random
from Crypto.Hash import SHA
import hashlib
def generateQ(keyLength, primeLength):
   
    #Step 1: RFC 2631 2.2.1.1
    
    qLength =int(math.ceil((2*keyLength)/160))
    
    #Step 2:
    pLength =int(math.ceil(primeLength/160))
    
    #Step 3:
    N = math.ceil(pLength/1024)
    
    #Step 4:
    c = 0
    while True:
        c += 1
        seed = random.getrandbits(random.randint(1,9) * qLength)
        
        #Step 5:
        U = 0
        
        #Step 6:
        h1 = SHA.new()
        h2 = SHA.new()

        
        for i in range(0,pLength-1):
            h1.update(bytes(seed + i))
            h2.update(bytes(seed + qLength + i))

            U = U + (int(h1.hexdigest(),16) ^ int(h2.hexdigest(),16)) * 2**(160 * i)

            print>>sys.stderr, 'U: %s' % U
        #Step 7:
        q = U or 2**(keyLength-1) or 1

        if number.isPrime(q):
            print>>sys.stderr, 'counter: %s' % c
            break

    return q



    #Step 8:
#    counter = 0

    #Step 9:
#    R = seed + 2*qLength + (pLength * counter)

    #Step 10:
 #   V = 0
    
    #Step 12:
  #  for i in range(0, pLength-1)
   #     V = V + hashlib.SHA1(R + i) * 2**(160*i)

    #Step 13:
   # W = V % (2*primeLength)
    
    #Step 14:
   # X = W or 2**(primeLength-1)

    

    
    
    #print>>sys.stderr,'qlength: %s\n pLength: %s\n N: %s\n seed: %s\n U: %s\n' % (qLength,pLength,N,seed,U)
    

    

       

print>>sys.stderr, 'q: %s' % generateQ(256, 2048)
