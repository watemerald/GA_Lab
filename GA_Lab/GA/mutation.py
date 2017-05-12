from parameters_new import parameters
import random
import copy

def mutation(bits,
            p_m = None,
            type = None):
    '''Mutation selection
    Selects the appropriate mutation function based on parameters

    Args:
        bits: The bitarray to be mutatted.
        p_m: The mutation probability.
        type: The type of mutation to be performed (1-point or density)

    Returns:
        The mutated bitarray
    '''
    if p_m == None:
        p_m = parameters.pm
    if type == None:
        type = parameters.mutation
    # mutation = '1-point'
    # mutation = 'density'

    if type == '1-point':
        return point_mutation(bits, p_m)
    if type == 'density':
        return density_mutation(bits, p_m)

    raise ValueError("Unknown mutation type {}".format(type))


def point_mutation(bits, p_m = None):
    '''Point mutation

    Args:
        bits: The bitarray to be mutatted.
        p_m: The mutation probability.

    Returns:
        The mutated bitarray
    '''
    if p_m == None:
        p_m = parameters.pm

    cat = list(copy.copy(bits))
    if random.random() < p_m:
        length = len(bits)
        mutating_bit = random.randrange(length)

        cat[mutating_bit] = str(1-int(bits[mutating_bit]))
    return ''.join(cat)

def density_mutation(bits, p_m = None):
    '''Density mutation

    Args:
        bits: The bitarray to be mutatted.
        p_m: The mutation probability.

    Returns:
        The mutated bitarray
    '''
    if p_m == None:
        p_m = parameters.pm

    cat = list(copy.copy(bits))
    length = len(bits)
    for i in range(length):
        if random.random < p_m:
            cat[i] = str(1-int(bits[i]))

    return ''.join(cat)
