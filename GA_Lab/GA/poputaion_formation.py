import random
from parameters import N
from bitarray import bitarray
from utils import bin_to_double, double_to_bin

# def generate_population(N=N):
#      return (bitarray(''.join(random.choices(['0', '1'], k=62)))
#         for i in range(N))

def generate_population(N=N, dim=1, min=0, max=1):
    return [double_to_bin(random.uniform(min, max)) for _ in range(N)]
