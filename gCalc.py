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
    print>>sys.stderr, 'pLength: %s' %pLength    
    #Step 3:
    N = int(math.ceil(primeLength/1024))
    
     
    print>>sys.stderr, 'N: %s' % N
    #Step 4:
    c = 0
    while True:
        c += 1
        seed = random.getrandbits(random.randint(1,9) * (2*keyLength))
        
        #Step 5:
        U = 0
        
        #Step 6:
        h1 = SHA.new()
        h2 = SHA.new()

        
        for i in range(0,qLength-1):
            h1.update(bytes(seed + i))
            h2.update(bytes(seed + qLength + i))

            U = U + (int(h1.hexdigest(),16) ^ int(h2.hexdigest(),16)) * (2**(160 * i))

           # print>>sys.stderr, 'U: %s' % U
        #Step 7:
        q = U or 2**((2*keyLength)-1) or 1

        if number.isPrime(q):
            print>>sys.stderr, 'counter: %s' % c
            break

    return generateP(seed, qLength, pLength, primeLength, q, N)


def generateP(seed, qLength, pLength, primeLength,q, N):
    #Step 8:
    counter = 0
    while True:
        print>>sys.stderr, 'Counter: %s' % counter

        #Step 9:
        R = seed + 2*qLength + (pLength * counter)

        #Step 10:
        V = 0
    
        #Step 12:
        h = SHA.new()
        for i in range(0, pLength-1):
            h.update(bytes(R+i))
            V = V + int(h.hexdigest(),16) * 2**(160*i)

        #Step 13:
        W = V % (2*primeLength)
    
        #Step 14:
        X = W or 2**(primeLength-1)

        #step 15:
        p = X - (X % (2*q)) + 1
        

        #Step 16:
        if p > 2**(primeLength -1) and number.isPrime(p):
            return p
        else:
            counter += 1
            print>>sys.stderr, 'Counter: %s' % counter
            if counter >= (4096 * N):
                break

            
    print>>sys.stderr, 'Could not find prime'
    return False
    
    
    #print>>sys.stderr,'qlength: %s\n pLength: %s\n N: %s\n seed: %s\n U: %s\n' % (qLength,pLength,N,seed,U)
    

    

       

print>>sys.stderr, 'is prime: %s' % number.isPrime(1044388881413152506679602719846529545831269060992135009022588756444338172022322690710444046669809783930111585737890362691860127079270495454517218673016928427459146001866885779762982229321192368303346235204368051010309155674155697460347176946394076535157284994895284821633700921811716738972451834979455897010306333468590751358365138782250372269117968985194322444535687415522007151638638141456178420621277822674995027990278673458629544391736919766299005511505446177668154446234882665961680796576903199116089347634947187778906528008004756692571666922964122566174582776707332452371001272163776841229318324903125740713574141005124561965913888899753461735347970011693256316751660678950830027510255804846105583465055446615090444309583050775808509297040039680057435342253926566240898195863631588888936364129920059308455669454034010391478238784189888594672336242763795138176353222845524644040094258962433613354036104643881925238489224010194193088911666165584229424668165441688927790460608264864204237717002054744337988941974661214699689706521543006262604535890998125752275942608772174376107314217749233048217904944409836238235772306749874396760463376480215133461333478395682746608242585133953883882226786118030184028136755970045385534758453247)
