import parameters
import random

def point_crossover(parent_a, parent_b, p_c = parameters.pc):
    '''Point crossover

    Args:
        parent_a: The first parent.
        parent_b: The second parent.
        p_m: The mutation probability.

    Returns:
        The resulting children
    '''

    if random.random() < p_c:
        len = parent_a.length()
        crossover_point = random.randrange(len)
        child_a = a[:crossover_point] + b[crossover_point:]

        child_b = b[:crossover_point] + a[crossover_point:]

        return child_a, child_b

    return parent_a, parent_b

def two_point_crossover(parent_a, parent_b, p_c = parameters.pc):
    '''2 Point crossover

    Args:
        parent_a: The first parent.
        parent_b: The second parent.
        p_m: The mutation probability.

    Returns:
        The resulting children
    '''
    if random.random() < p_c:
        len = parent_a.length()
        crossover_point_1 = random.randrange(len)
        crossover_point_2 = random.randrange(crossover_point_1, len)

        child_a = a[:crossover_point1] +
                  b[crossover_point_1:crossover_point_2] +
                  a[crossover_point_2:]

        child_b = b[:crossover_point1] +
                  a[crossover_point_1:crossover_point_2] +
                  b[crossover_point_2:]

        return child_a, child_b

    return parent_a, parent_b
