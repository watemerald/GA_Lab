from parameters import distance_measure
from scipy.spatial.distance import euclidean, hamming
import struct

def similarity(a,b, d_m = distance_measure):
    if d_m == 'euclidean':
        return euclidean(a,b)
    if d_m == 'hamming':
        return hamming(a,b)

    raise ValueError("Unknown distance measure {}".
        format(distance_measure))

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
    k = int(str(b), base=2)
    f2 = struct.pack('q', k)

    return struct.unpack('d', f2)[0]

def average_fitness(pool, goal_function):
    return sum([goal_function(bin_to_double(p)) for p in pool])/ len(pool)
