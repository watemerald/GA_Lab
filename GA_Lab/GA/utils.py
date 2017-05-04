from parameters import distance_measure
from scipy.spatial.distance import euclidean, hamming

def similarity(a,b, d_m = distance_measure):
    if d_m == 'euclidian':
        return euclidian(a,b)
    if d_m == 'hamming':
        return hamming(a,b)

    raise ValueError("Unknown distance measure {}".
        format(distance_measure))
