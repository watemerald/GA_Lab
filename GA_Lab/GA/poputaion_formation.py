import random
from parameters import N, ndim
from bitarray import bitarray
from utils import bin_to_double, double_to_bin
import numpy as np

# def generate_population(N=N):
#      return (bitarray(''.join(random.choices(['0', '1'], k=62)))
#         for i in range(N))

def generate_population(N=N, dim=ndim, min=0, max=1):
    fc = np.vectorize(lambda _: double_to_bin(random.uniform(min, max)))
    arr = np.zeros((N, dim))
    return fc(arr)
    # return [double_to_bin(random.uniform(min, max)) for _ in range(N)]
