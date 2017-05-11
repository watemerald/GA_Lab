import math
import itertools
from .counted import counted

@counted
def compute(*args):
    result = 0
    product = 1

    for (arg, i) in enumerate(args, 1):
        result = result + arg ** 2 / 4000
        product = product * math.cos(arg/ math.sqrt(i))

    result = result - product + 1
    result = 10 - result

    return result

def get_local_maxima_list(dimensionality):
    arguments = [0.1, 0.3, 0.5, 0.7, 0.9]

    a = tuple(itertools.repeat(arguments, dimensionality))

    return list(itertools.product(*a))

def get_global_maxima_list(dimensionality):
    return list(tuple(itertools.repeat([0.1], dimensionality)))

def get_number_of_local_maxima(dimensionality):
    return 10 ** dimensionality + 1

def get_number_of_global_maxima(dimensionality):
    return 1
