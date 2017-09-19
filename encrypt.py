#Module used for encryption

def diffyhellman(gen, prime, i):
	#gen and prim are agreed upon values and i is a private secret
	return gen**i % prime
    #fin kod
