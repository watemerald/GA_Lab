from parameters import distance_measure
from scipy.spatial.distance import euclidean, hamming
import struct
from bitarray import bitarray


def similarity(a,b, d_m = distance_measure):
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
    return bitarray(strep.rjust(62, '0'))

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
