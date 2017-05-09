import copy
from poputaion_formation import generate_population
from mutation import mutation
from crossover import crossover
from selection import *
from utils import *
import Deb1
import logging
import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file, show

__number_of_runs = 10
__max_finess_evaluations = 20_000_000
__sigma = 0.0001

logger = logging.getLogger('ga_main')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(name)s: %(levelname)s - %(message)s')

ch. setFormatter(formatter)

logger.addHandler(ch)


def main():
    starting_pool = list(generate_population())

    goal_function = Deb1.compute

    goal_vector = np.vectorize(goal_function)
    convert_vector = np.vectorize(bin_to_double)

    starting_pool_values = {}
    for (k, chromosome) in enumerate(starting_pool):
        db = bin_to_double(chromosome)
        starting_pool_values[k] = (chromosome.to01(), db, goal_function(db))
        # starting_pool_values.append()

    # starting_pool_values = pd.DataFrame(list(starting_pool_values.items()), columns=('encoded', 'decoded', 'fitness'))
    starting_pool_values = pd.DataFrame.from_dict(starting_pool_values, orient='index')
    starting_pool_values.columns = ('encoded', 'decoded', 'fitness')

    starting_pool_values.to_csv('starting_pool.csv', sep='\t')

    starting_average = starting_pool_values.fitness.mean()
    # starting_average = average_fitness(starting_pool, goal_function)

    for i in range(__number_of_runs):
        # pool = copy.copy(starting_pool)
        spv = starting_pool_values.copy()
        prev_average = starting_average
        average_close = False
        average_closing = 0
        # logging.warn('Goal function calls {}'.format(goal_function.calls))
        goal_function.calls = 0
        # logging.warn('Goal function calls {}'.format(goal_function.calls))
        while True:
            spv = cycle(spv, goal_function)

            if goal_function.calls > __max_finess_evaluations:
                break

            # current_average = average_fitness(pool, goal_function)
            current_average = spv.fitness.mean()
            current_max = spv.fitness.max()
            # current_max = goal_function(bin_to_double(max_fitness(pool, goal_function)))
            # print("Average fitness: {} \t Max fitness: {}".format(current_average, current_max))
            if abs(current_average - prev_average) <= __sigma:
                # import pdb; pdb.set_trace()
                average_close = True
                average_closing = average_closing + 1
                if average_closing >= 5:
                    break
            else:
                average_close = False
                average_closing = 0

            prev_average = current_average

        # pool_values = {}
        # for (k, chromosome) in enumerate(pool):
        #     db = bin_to_double(chromosome)
        #     pool_values[k] = (chromosome.to01(), db, goal_function(db))
            # pool_values.append()

        # pool_values = pd.DataFrame(list(pool_values.items()), columns=('encoded', 'decoded', 'fitness'))
        # pool_values = pd.DataFrame.from_dict(pool_values, orient='index')
        # pool_values.columns = ('encoded', 'decoded', 'fitness')

        # import pdb; pdb.set_trace()
        # pool_values

        # pool_values.to_csv('pv.csv', sep='\t')

        peaks = find_peaks_2(spv)

        # import pdb; pdb.set_trace()
        #
        # peaks = find_peaks(pool, goal_function)

        # Evaluation parameters:
        NFE = goal_function.calls
        NP = len(peaks)
        PR = NP / Deb1.get_number_of_global_maxima(1)

        peak_values = peak_value_pairs(Deb1.get_local_maxima_list(1), goal_function)
        PA = peak_accuracy(spv, peak_values)
        DA = distance_accuracy(spv, peak_values)

        logger.debug('Run {} - NFE: {} NP: {} PR: {} PA: {} DA {}'.format(i, goal_function.calls, len(peaks), PR, PA, DA))

def cycle(pool, gf):
    child_a, child_b = form_children(pool)

    dba = bin_to_double(child_a)
    child_a = pd.Series([child_a, dba, gf(dba)])
    child_a.set_axis(0, ('encoded', 'decoded', 'fitness'))

    dbb = bin_to_double(child_b)
    child_b = pd.Series([child_b, dbb, gf(dbb)])
    child_b.set_axis(0, ('encoded', 'decoded', 'fitness'))


    pool_1 = worst_among_most_similar(pool, child_a, gf)
    pool_2 = worst_among_most_similar(pool, child_b, gf)

    return pool_2

def population_dict(pool, goal_function):
    return {
    a.to01(): goal_function(bin_to_double(a)) for a in pool
    }

if __name__ == '__main__':
    main()
