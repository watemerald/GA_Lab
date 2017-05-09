import copy
from poputaion_formation import generate_population
from mutation import mutation
from crossover import crossover
from selection import *
from utils import *
import Deb1
import logging

__number_of_runs = 10
__max_finess_evaluations = 20_000_000
__sigma = 0.02

logger = logging.getLogger('ga_main')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(name)s: %(levelname)s - %(message)s')

ch. setFormatter(formatter)

logger.addHandler(ch)

def main():
    pool = list(generate_population())

    goal_function = Deb1.compute

    starting_average = average_fitness(pool, goal_function)
    for i in range(__number_of_runs):
        pool = copy.copy(pool)
        prev_average = starting_average
        average_close = False
        average_closing = 0
        # logging.warn('Goal function calls {}'.format(goal_function.calls))
        goal_function.calls = 0
        # logging.warn('Goal function calls {}'.format(goal_function.calls))
        while True:
            pool = cycle(pool, goal_function)

            if goal_function.calls > __max_finess_evaluations:
                break

            current_average = average_fitness(pool, goal_function)
            current_max = goal_function(bin_to_double(max_fitness(pool, goal_function)))
            # print("Average fitness: {} \t Max fitness: {}".format(current_average, current_max))
            if abs(current_average - prev_average) <= __sigma:
                average_close = True
                average_closing = average_closing + 1
                if average_closing >= 5:
                    break
            else:
                average_close = False
                average_closing = 0

            prev_average = current_average

            # logger.debug(population_dict(pool, goal_function))

        peaks = find_peaks(pool, goal_function)
        logger.debug('Run {} - NFE: {} NP: {} '.format(i, goal_function.calls, len(peaks)))

def cycle(pool, gf):
    child_a, child_b = form_children(pool)

    pool_1 = worst_among_most_similar(pool, child_a, gf)
    pool_2 = worst_among_most_similar(pool, child_b, gf)

    return pool_2

def population_dict(pool, goal_function):
    return {
    a.to01(): goal_function(bin_to_double(a)) for a in pool
    }

if __name__ == '__main__':
    main()
