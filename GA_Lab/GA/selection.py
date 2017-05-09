import random
import parameters
from utils import similarity, bin_to_double
from crossover import crossover
from mutation import mutation

def form_children(population,
                  c_s = parameters.cs,
                  c_f = parameters.cf,
                  s = parameters.s):
    '''Select a pair of parents and form children

    Args:
        population: The population selection pool.

    Returns:
        The resulting children
    '''
    # import pdb; pdb.set_trace();
    parent_a = random.choice(population)

    crowding_selection_group = random.sample(population, c_s)

    parent_b = max(crowding_selection_group, key= lambda x: similarity(parent_a, x))

    child_a, child_b = crossover(parent_a, parent_b)

    child_a = mutation(child_a)
    child_b = mutation(child_b)

    return child_a, child_b


def worst_among_most_similar(population,
                            child,
                            goal_function,
                            c_f = parameters.cf,
                            s = parameters.s):
    '''Create new population pool according to the worst among the most similar strategy.

    Args:
        population: The population pool.
        child: New chromosome to be added to the population.
        goal_function: The function we are optimising.

    Returns:
        The resulting population
    '''
    # parent_A = random.choice(population)
    #
    # crowding_selection_group = random.sample(population, s)


    cf_groups = []
    for i in range(c_f):
        cf_groups.append(random.sample(population, s))

    most_similar = []
    for group in cf_groups:
        most_similar.append(max(group, key=lambda x: similarity(child, x)))

    worst = min(most_similar, key=lambda x: goal_function(bin_to_double(x)))

    population.remove(worst)

    population.append(child)

    return population

def most_similar_among_worst(population,
                            child,
                            goal_function,
                            c_f = parameters.cf,
                            s = parameters.s):
    '''Create new population pool according to the most similar among the worst strategy.

    Args:
        population: The population pool.
        child: New chromosome to be added to the population.
        goal_function: The function we are optimising.

    Returns:
        The resulting population
    '''
    # parent_A = random.choice(population)
    #
    # crowding_selection_group = random.sample(population, s)

    cf_groups = []
    for i in range(c_f):
        cf_groups.append(random.sample(population, s))

    worst = []
    for group in cf_groups:
        worst.append(min(group, key=goal_function))

    most_similar = max(worst, key=similarity)

    population.remove(most_similar)

    population.append(child)

    return population
