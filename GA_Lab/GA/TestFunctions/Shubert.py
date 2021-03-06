import math
import itertools
from .counted import counted

@counted
def compute(*args):
    result = 0
    for arg in args:
        result = result + math.sin(5 * math.pi * arg) ** 6

    result = result / len(args)

    return result

def get_local_maxima_list(dimensionality):
    arguments = [0.1, 0.3, 0.5, 0.7, 0.9]

    a = tuple(itertools.repeat(arguments, dimensionality))

    return list(itertools.product(*a))

def get_global_maxima_list(dimensionality):
    return get_local_maxima_list(dimensionality)

def get_number_of_local_maxima(dimensionality):
    return 0

def get_number_of_global_maxima(dimensionality):
    return 5 ** dimensionality
