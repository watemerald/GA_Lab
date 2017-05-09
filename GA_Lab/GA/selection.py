import random
import parameters
from utils import similarity, bin_to_double
from crossover import crossover
from mutation import mutation
import pandas as pd

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
    # parent_a = random.choice(population)

    # crowding_selection_group = random.sample(population, c_s)

    parent_a = population.sample(1).iloc[0]

    crowding_selection_group = population.sample(c_s)
    # import pdb; pdb.set_trace()
    # pool_values['decoded'].apply(lambda x: euclidean(x, peak)).idxmin()
    parent_b = crowding_selection_group.ix[
        crowding_selection_group['decoded'].apply(lambda x: similarity(parent_a.decoded, x)).idxmin()
    ]
    # parent_b.orient('index')

    # parent_b = max(crowding_selection_group, key= lambda x: similarity(parent_a, x))

    # import pdb; pdb.set_trace()

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
        # cf_groups.append(random.sample(population, s))
        cf_groups.append(population.sample(s))

    most_similar = []

    for group in cf_groups:
        most_similar.append(group.ix[
            group['decoded'].apply(lambda x: similarity(child.decoded,x)).idxmax()
        ])
        # most_similar.append(max(group, key=lambda x: similarity(child, x)))

    most_similar = pd.DataFrame(most_similar)

    worst = most_similar.fitness.idxmin()
    population = population.drop(worst)

    child.name=worst
    population = population.append(child)

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
        # cf_groups.append(random.sample(population, s))
        cf_groups.append(population.sample(s))

    worst = []
    for group in cf_groups:
        # worst.append(min(group, key=goal_function))
        worst.append(group.ix[
            group.fitness.idxmin()
        ])
    worst = pd.DataFrame(worst)

    # most_similar = max(worst, key=similarity)
    most_similar = worst['decoded'].apply(lambda x: similarity(child.decoded,x)).idxmax()

    population = population.drop(most_similar)
    child.name = most_similar
    population = population.append(child)
    # population.append(child)

    return population
