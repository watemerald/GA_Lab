import copy
from poputaion_formation import generate_population
from mutation import mutation
from crossover import crossover
from selection import *
from utils import *
from TestFunctions import Deb1, Deb2, Deb3, Deb4
import logging
import plotting
import pandas as pd
import numpy as np
import time
from itertools import product
import os.path
from uuid import uuid1
# import parameters
from parameters_new import parameters

from bokeh.plotting import figure, output_file, show

__number_of_runs = 10
__max_finess_evaluations = 20_000_000
__sigma = 0.0001

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(name)s: %(levelname)s - %(message)s')

ch.setFormatter(formatter)

textlog = logging.FileHandler('info.log')
textlog.setFormatter(formatter)

logger.addHandler(textlog)
logger.addHandler(ch)

ndim = parameters.ndim

data_file = 'data.csv'
if os.path.isfile(data_file):
    df = pd.DataFrame.from_csv(data_file)
else:
    with open(data_file, 'w+') as f:
        pass
    df = pd.DataFrame()


def main(optimising_goal=Deb1):
    logger.info('''Starting the main loop with parameters {} \n
    optimising function {}'''.format(parameters, optimising_goal.__name__))
    global df

    starting_pool = list(generate_population())

    # optimising_goal = Deb1
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
        logger.info('Started run number {} at starting time {}'.format(i, starting_time))
        # pool = copy.copy(starting_pool)
        spv = starting_pool_values.copy()
        prev_average = starting_average
        average_close = False
        average_closing = 0
        # logging.warn('Goal function calls {}'.format(goal_function.calls))
        goal_function.calls = 0
        # logging.warn('Goal function calls {}'.format(goal_function.calls))
        while True:
            spv = cycle(spv, goal_function, parameters.method)

            if goal_function.calls > __max_finess_evaluations:
                break

            # current_average = average_fitness(pool, goal_function)
            current_average = spv.fitness.mean()
            current_max = spv.fitness.max()
            # current_max = goal_function(bin_to_double(max_fitness(pool, goal_function)))
            # print("Average fitness: {} \t Max fitness: {}".format(current_average, current_max))
            if abs(current_average - prev_average) <= parameters.sigma:
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
        PR = NP / optimising_goal.get_number_of_global_maxima(ndim)

        peak_values = peak_value_pairs(optimising_goal.get_local_maxima_list(ndim), goal_function)
        PA = peak_accuracy(spv, peak_values)
        DA = distance_accuracy(spv, peak_values)

        ending_time = time.time()

        run_time = ending_time - starting_time

        logger.info('Finished run number {} at ending time {}'.format(i, ending_time))

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
            'run_time': run_time,
            'method': parameters.method
        }
        # df = df.append([optimising_goal.__name__, NFE, NP, PR, PA, DA, run_time])
        df = df.append(datum, ignore_index=True)
        df.to_csv(data_file)


        # logger.debug('Run {} - NFE: {} NP: {} PR: {} PA: {} DA {} Time {}'.format(i, goal_function.calls, len(peaks), PR, PA, DA, (ending_time-starting_time)*1000.0))
        if ndim==1:
            plotting.plot(goal_vector, spv.decoded, spv.fitness, '{} - {}{}.jpg'.format(optimising_goal.__name__, i, uuid1()))

    df.to_csv(data_file)

def cycle(pool, gf, method='worst_among_most_similar'):
    child_a, child_b = form_children(pool)

    dba = decode(child_a)
    if ndim==1:
        child_a = pd.Series([child_a, dba, gf(dba)])
    else:
        import pdb; pdb.set_trace()
        child_a = pd.Series([child_a, dba, gf(*dba)])
    child_a.set_axis(0, ('encoded', 'decoded', 'fitness'))

    dbb = decode(child_b)
    if ndim==1:
        child_b = pd.Series([child_b, dbb, gf(dbb)])
    else:
        child_b = pd.Series([child_b, dbb, gf(*dbb)])
    child_b.set_axis(0, ('encoded', 'decoded', 'fitness'))

    if method == 'worst_among_most_similar':
        pool_1 = worst_among_most_similar(pool, child_a, gf)
        pool_2 = worst_among_most_similar(pool_1, child_b, gf)
    if method == 'most_similar_among_worst':
        pool_1 = most_similar_among_worst(pool, child_a, gf)
        pool_2 = most_similar_among_worst(pool_1, child_b, gf)

    return pool_2

def parameter_generation():
    n = [500]
    ndim = [1,2,3,5]
    pm = [0.1, 0.2]
    pc = [0.1, 0.2]
    coding = ['bin']
    mutation = ['1-point']
    crossover = ['1']
    distance_measure = ['euclidean']
    cs = [0.15]
    cf = [3,4]
    s = [0.01]

    method = ['worst_among_most_similar', 'most_similar_among_worst']

    return list(product(n, ndim, pm, pc, coding, mutation, crossover, distance_measure, cs, cf, s, method))




def population_dict(pool, goal_function):
    return {
    a.to01(): goal_function(decode(a)) for a in pool
    }

if __name__ == '__main__':
    params_to_test = parameter_generation()

    for (n, ndim, pm, pc, coding, mutation, crossover, distance_measure, cs, cf, s, method) in params_to_test:
        parameters.N = n
        parameters.ndim = ndim
        parameters.pm = pm
        parameters.pc = pc
        parameters.coding = coding
        parameters.mutation = mutation
        parameters.distance_measure = distance_measure
        parameters.cs = cs
        parameters.cf = cf
        parameters.s = s
        parameters.method = method

        main(Deb1)
        main(Deb4)



    # main()
