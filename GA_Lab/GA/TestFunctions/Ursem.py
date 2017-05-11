import math
import itertools
from .counted import counted

@counted
def compute(*args):
    result = 0
    x1, x2 = args

    result = -((4-2.1*x1 ** 2 + x1**4/3) * x1**2 + x1*x2+ 4*(x2**2 -1)*x2**2)

    result = 0


def get_local_maxima_list(dimensionality):
    if dimensionality == 2:
        return [(-0.0898, 0.7126), (0.0898, -0.7126),
                (-1.7036, 0.7961), (1.7036, -0.7961),
                (-1.6071, -0.5687), (1.6071, 0.5687)]

    raise ValueError('Ursem function not defined on dimensionalitys other than 2')

def get_global_maxima_list(dimensionality):
    if dimensionality == 2:
        return [(-0.0898, 0.7126), (0.0898, -0.7126)]


    raise ValueError('Ursem function not defined on dimensionalitys other than 2')

def get_number_of_local_maxima(dimensionality):
    if dimensionality == 2:
        return 4
    return 0

def get_number_of_global_maxima(dimensionality):
    if dimensionality == 2:
        return 2
    return 0
