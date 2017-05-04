import parameters
import random

def point_mutation(bits, p_m = parameters.pm):
    '''Point mutation

    Args:
        bits: The bitarray to be mutatted.
        p_m: The mutation probability.

    Returns:
        The mutated bitarray
    '''
    if random.random < p_m:
        len = bits.length()
        mutating_bit = random.randrange(len)

        bits[mutating_bit] = not bits[mutating_bit]

    return bits

def density_mutation(bits, p_m = parameters.pm):
    '''Density mutation

    Args:
        bits: The bitarray to be mutatted.
        p_m: The mutation probability.

    Returns:
        The mutated bitarray
    '''
    len = bits.length
    for i in range(len):
        if random.random < p_m:
            bits[i] = not bits[i]

    return bits
