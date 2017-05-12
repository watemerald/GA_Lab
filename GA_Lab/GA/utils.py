# from parameters import distance_measure, ndim, coding
from parameters_new import parameters
from scipy.spatial.distance import euclidean, hamming
from sympy.combinatorics.graycode import bin_to_gray, gray_to_bin
import struct
from bitarray import bitarray
import pandas as pd
import numpy as np


def similarity(a,b, d_m = None):
    if d_m == None:
        d_m = parameters.distance_measure
    # import pdb; pdb.set_trace()
    if d_m == 'euclidean':
        if isinstance(a, str):
            return euclidean(num(a), num(b))
        return euclidean(a,b)
    if d_m == 'hamming':
        if isinstance(a, str):
            return hamming(num(a), num(b))
        return hamming(a,b)

    raise ValueError("Unknown distance measure {}".
        format(distance_measure))

def num(a):
    return [int(c) for c in a]

def double_to_bin(f):
    '''Converts a double(float) to a binary representation
    '''
    s = struct.pack('d', f)
    strep = str(bin(struct.unpack('q', s)[0]))[2:]
    return strep.rjust(62, '0')

def bin_to_double(b):
    '''Converts a binary number to a double
    '''
    # import pdb; pdb.set_trace()
    try:
        k = int(b.to01(), base=2)
    except AttributeError:
        k = int(b, base=2)
    f2 = struct.pack('q', k)

    return struct.unpack('d', f2)[0]

double_to_bin = np.vectorize(double_to_bin)
bin_to_double = np.vectorize(bin_to_double)
bin_to_gray = np.vectorize(bin_to_gray)
gray_to_bin = np.vectorize(gray_to_bin)

def encode(f, dim=None, coding=None):
    if dim == None:
        dim = parameters.ndim
    if coding == None:
        coding = parameters.coding

    if coding == 'bin':
        return double_to_bin(f)
    elif coding == 'gray':
        return bin_to_gray(double_to_bin(f))
    else:
        raise ValueError("Unknown number coding {}".
            format(coding))

def decode(f, dim=None, coding=None):
    if dim == None:
        dim = parameters.ndim
    if coding == None:
        coding = parameters.coding

    if dim > 1:
        if isinstance(f, str):
            f = [f[i:i+62] for i in range(dim)]
    if coding == 'bin':
        return bin_to_double(f)
    elif coding == 'gray':
        # return bin_to_gray(double_to_bin(f))
        return bin_to_double(gray_to_bin(f))
    else:
        raise ValueError("Unknown number coding {}".
            format(coding))

def average_fitness(pool, goal_function):
    return sum([goal_function(bin_to_double(p)) for p in pool])/ len(pool)

def max_fitness(pool, goal_function):
    return max(pool, key=lambda x: goal_function(bin_to_double(x)))

def find_peaks(pool, goal_function, sigma=0.05):
    seeds = []
    gf = lambda x: goal_function(bin_to_double(x))
    best_to_worst = sorted(pool, key=gf)

    # gf = goal_function

    for chromosome in best_to_worst:
        # import pdb; pdb.set_trace()
        found = False
        for seed in seeds:
            if abs(gf(seed) - gf(chromosome)) <= sigma:
                found = True
                break
        if not found:
            seeds.append(chromosome)

    return seeds

def find_peaks_2(pool_values, sigma=0.01):
    # seeds = pd.DataFrame(columns=('encoded', 'decoded', 'fitness'))

    seeds = []

    best_to_worst = pool_values.sort_values(by='fitness', ascending=False)

    for chromosome in best_to_worst.itertuples():
        found = False
        for seed in seeds:
            if abs(euclidean(chromosome.decoded, seed.decoded) <= sigma):
                found = True
                break
        if not found:

            # import pdb; pdb.set_trace()

            seeds.append(chromosome)


    # import pdb; pdb.set_trace()
    return pd.DataFrame.from_records(seeds).drop(0,1)

def peak_accuracy(pool_values, peaks):
    def diff(peak, value):
        # closest_value = pool_values.ix[
        #     euclidean(pool_values['decoded'], peak).idxmin()
        #     ]
        closest_value = pool_values.ix[
            pool_values['decoded'].apply(lambda x: euclidean(x, peak)).idxmin()
        ]
        return abs(value-closest_value['fitness'])

    ret = sum([diff(peak, value) for (peak, value) in peaks])

    # import pdb; pdb.set_trace()
    return ret

def distance_accuracy(pool_values, peaks):
    def dist(peak, value):
        # closest_value = pool_values.ix[
        #     euclidean(pool_values['decoded'], peak).idxmin()
        #     ]
        closest_value = pool_values.ix[
            pool_values['decoded'].apply(lambda x: euclidean(x, peak)).idxmin()
        ]
        return euclidean(peak, closest_value['decoded'])

    ret = sum([dist(peak, value) for peak, value in peaks])

    return ret

def peak_value_pairs(peak_list, goal_function):
    return [(p, goal_function(*p)) for p in peak_list]
