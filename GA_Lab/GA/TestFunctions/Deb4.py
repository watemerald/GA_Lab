import math
import itertools
from .counted import counted

@counted
def compute(*args):
    result = 0
    for arg in args:
        result = result + math.e ** (-2 * math.log(2) * ((arg - 0.08)/0.854)**2)* math.sin(5 * math.pi * (arg** 0.75 - 0.05)) ** 6

    return result

def get_local_maxima_list(dimensionality):
    arguments = [0.080, 0.247, 0.451, 0.681, 0.934]

    a = tuple(itertools.repeat(arguments, dimensionality))

    return list(itertools.product(*a))

def get_global_maxima_list(dimensionality):
    return list(tuple(itertools.repeat([0.080], dimensionality)))

def get_number_of_local_maxima(dimensionality):
    return 5 ** dimensionality

def get_number_of_global_maxima(dimensionality):
    return 1
