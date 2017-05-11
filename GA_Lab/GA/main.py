import copy
from poputaion_formation import generate_population
from mutation import mutation
from crossover import crossover
from selection import *
from utils import *
from TestFunctions import Deb1
import logging
import plotting
import pandas as pd
import numpy as np
import time
import parameters

from bokeh.plotting import figure, output_file, show

__number_of_runs = 3
__max_finess_evaluations = 20_000_000
__sigma = 0.0001

logger = logging.getLogger('ga_main')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(name)s: %(levelname)s - %(message)s')

ch. setFormatter(formatter)

logger.addHandler(ch)

df = pd.DataFrame()
data_file = 'data.csv'

def main():
    global df

    starting_pool = list(generate_population())

    optimising_goal = Deb1
    goal_function = optimising_goal.compute

    goal_vector = np.vectorize(goal_function)
    convert_vector = np.vectorize(bin_to_double)

    starting_pool_values = {}
    for (k, chromosome) in enumerate(starting_pool):
        db = decode(chromosome)
        starting_pool_values[k] = (''.join(chromosome), db, goal_function(*db))
        # starting_pool_values.append()

    # starting_pool_values = pd.DataFrame(list(starting_pool_values.items()), columns=('encoded', 'decoded', 'fitness'))
    starting_pool_values = pd.DataFrame.from_dict(starting_pool_values, orient='index')
    starting_pool_values.columns = ('encoded', 'decoded', 'fitness')

    starting_pool_values.to_csv('starting_pool.csv', sep='\t')

    starting_average = starting_pool_values.fitness.mean()
    # starting_average = average_fitness(starting_pool, goal_function)

    for i in range(__number_of_runs):
        starting_time = time.time()
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

        peaks = find_peaks_2(spv)

        # import pdb; pdb.set_trace()
        #
        # peaks = find_peaks(pool, goal_function)

        # Evaluation parameters:
        NFE = goal_function.calls
        NP = len(peaks)
        PR = NP / Deb1.get_number_of_global_maxima(ndim)

        peak_values = peak_value_pairs(Deb1.get_local_maxima_list(ndim), goal_function)
        PA = peak_accuracy(spv, peak_values)
        DA = distance_accuracy(spv, peak_values)

        ending_time = time.time()

        run_time = ending_time - starting_time

        datum = {
            'N': parameters.N,
            'dimensions': parameters.ndim,
            'p_m': parameters.pm,
            'p_c': parameters.pc,
            'coding': parameters.coding,
            'crossover': parameters.crossover,
            'mutation': parameters.mutation,
            'distance_measure': parameters.distance_measure,
            'crowding_selection': parameters.cs,
            'crowding_factor': parameters.cf,
            'subpopulation_size': parameters.s,
            'function_name': optimising_goal.__name__,
            'run_number': i,
            'NFE': NFE,
            'NP': NP,
            'PR': PR,
            'PA': PA,
            'DA': DA,
            'run_time': run_time
        }
        # df = df.append([optimising_goal.__name__, NFE, NP, PR, PA, DA, run_time])
        df = df.append(datum, ignore_index=True)

        # logger.debug('Run {} - NFE: {} NP: {} PR: {} PA: {} DA {} Time {}'.format(i, goal_function.calls, len(peaks), PR, PA, DA, (ending_time-starting_time)*1000.0))

        if ndim==1:
            plotting.plot(goal_vector, spv.decoded, spv.fitness)

    df.to_csv(data_file)

def cycle(pool, gf):
    child_a, child_b = form_children(pool)

    dba = decode(child_a)
    if ndim==1:
        child_a = pd.Series([child_a, dba, gf(dba)])
    else:
        child_a = pd.Series([child_a, dba, gf(*dba)])
    child_a.set_axis(0, ('encoded', 'decoded', 'fitness'))

    dbb = decode(child_b)
    if ndim==1:
        child_b = pd.Series([child_b, dbb, gf(dbb)])
    else:
        child_b = pd.Series([child_b, dbb, gf(*dbb)])
    child_b.set_axis(0, ('encoded', 'decoded', 'fitness'))


    pool_1 = worst_among_most_similar(pool, child_a, gf)
    pool_2 = worst_among_most_similar(pool, child_b, gf)

    return pool_2

def population_dict(pool, goal_function):
    return {
    a.to01(): goal_function(decode(a)) for a in pool
    }

if __name__ == '__main__':
    main()
