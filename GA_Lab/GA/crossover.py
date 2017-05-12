# import parameters
from parameters_new import parameters
import random

def crossover(parent_a, parent_b,
             p_c = parameters.pc,
             type = parameters.crossover):
    '''Crossover selection

    Args:
        parent_a: The first parent.
        parent_b: The second parent.
        p_m: The mutation probability.
        type: The type of crossover ('1', '2', 'n')

    Returns:
        The resulting children
    '''

    if type == '1':
        return point_crossover(parent_a, parent_b, p_c)
    if type == '2':
        return two_point_crossover(parent_a, parent_b, p_c)
    if type == 'n':
        return n_point_crossover(paernt_a, parent_b, p_c)

    raise ValueError("Unknown crossover type type {}".format(type))


    #  crossover = '1'
    # crossover = '2'
    # crossover = 'n'

def point_crossover(parent_a, parent_b, p_c = parameters.pc):
    '''Point crossover

    Args:
        parent_a: The first parent.
        parent_b: The second parent.
        p_m: The mutation probability.

    Returns:
        The resulting children
    '''
    coded_a = parent_a.encoded
    coded_b = parent_b.encoded


    if random.random() < p_c:
        length = len(coded_a)
        crossover_point = random.randrange(length)
        child_a = coded_a[:crossover_point] + coded_b[crossover_point:]

        child_b = coded_b[:crossover_point] + coded_a[crossover_point:]

        return child_a, child_b

    return coded_a, coded_b

def two_point_crossover(parent_a, parent_b, p_c = parameters.pc):
    '''2 Point crossover

    Args:
        parent_a: The first parent.
        parent_b: The second parent.
        p_m: The mutation probability.

    Returns:
        The resulting children
    '''
    coded_a = parent_a.encoded
    coded_b = parent_b.encoded

    if random.random() < p_c:
        length = len(coded_a)
        crossover_point_1 = random.randrange(length)
        crossover_point_2 = random.randrange(crossover_point_1, length)

        child_a = coded_a[:crossover_point1] + coded_b[crossover_point_1:crossover_point_2] + coded_a[crossover_point_2:]

        child_b = coded_b[:crossover_point1] + coded_a[crossover_point_1:crossover_point_2] + coded_b[crossover_point_2:]

        return child_a, child_b

    return coded_a, coded_b

def n_point_crossover(parent_a, parent_b, p_c = parameters.pc):
    coded_a = parent_a.encoded
    coded_b = parent_b.encoded

    def mask_digit():
        if random.random() < p_c:
            return 0
        else:
            return 1

    length = len(coded_a)

    mask = [mask_digit() for _ in range(length)]

    child_a = []
    child_b = []

    for (i, m) in enumerate(mask):
        if m == 0:
            child_a[i] = coded_a[i]
            child_b[i] = coded_b[i]
        if m == 1:
            child_a[i] = coded_b[i]
            child_b[i] = coded_a[i]

    return
