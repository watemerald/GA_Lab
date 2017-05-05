import copy
from poputaion_formation import generate_population
from mutation import mutation
from crossover import crossover
from selection import *
from utils import *
import Deb1

__number_of_runs = 10
__max_finess_evaluations = 20000000
__sigma = 0.01


def main():
    pool = list(generate_population())

    goal_function = Deb1.compute

    starting_average = average_fitness(pool, goal_function)
    for i in range(__number_of_runs):
        pool = copy.copy(pool)
        prev_average = starting_average
        average_close = False
        average_closing = 0
        goal_function.calls = 0
        while True:
            pool = cycle(pool, goal_function)

            if goal_function.calls > __max_finess_evaluations:
                break

            current_average = average_fitness(pool, goal_function)
            if abs(current_average - prev_average) < __sigma:
                average_close = True
                average_closing = average_closing + 1
                if average_closing == 5:
                    break
            else:
                average_close = False
                average_closing = 0

            prev_average = current_average





def cycle(pool, gf):
    child_a, child_b = form_children(pool)

    pool_1 = worst_among_most_similar(pool, child_a, gf)
    pool_2 = worst_among_most_similar(pool, child_b, gf)

    return pool_2


if __name__ == '__main__':
    main()
