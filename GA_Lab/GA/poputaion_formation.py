import random
from parameters import N
from bitarray import bitarray

def generate_population(N=N):
     return (bitarray(''.join(random.choices(['0', '1'], k=62)))
        for i in range(N))
