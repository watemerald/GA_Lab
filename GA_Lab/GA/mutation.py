import parameters
import random

def mutation(bits,
            p_m = parameters.pm,
            type = parameters.mutation):
    '''Mutation selection
    Selects the appropriate mutation function based on parameters

    Args:
        bits: The bitarray to be mutatted.
        p_m: The mutation probability.
        type: The type of mutation to be performed (1-point or density)

    Returns:
        The mutated bitarray
    '''
    # mutation = '1-point'
    # mutation = 'density'

    if type == '1-point':
        return point_mutation(bits, p_m)
    if type == 'density':
        return density_mutation(bits, p_m)

    raise ValueError("Unknown mutation type {}".format(type))


def point_mutation(bits, p_m = parameters.pm):
    '''Point mutation

    Args:
        bits: The bitarray to be mutatted.
        p_m: The mutation probability.

    Returns:
        The mutated bitarray
    '''
    if random.random() < p_m:
        length = len(bits)
        mutating_bit = random.randrange(length)

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
    length = len(bits)
    for i in range(length):
        if random.random < p_m:
            bits[i] = not bits[i]

    return bits
