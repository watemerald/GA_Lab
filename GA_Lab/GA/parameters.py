
# Number of chromosomes in the poputaion
N = 500

# Probability of mutation
pm = 0.1

# Probability of crossover
pc = 0.05

# Which coding to use
coding = 'bin'
# coding = 'gray'

# Which population formation method to use
pop_form = '1'
# pop_form = '2'

# Which crossover type to use
crossover = '1'
# crossover = '2'
# crossover = 'n'

# Which mutation to use
mutation = '1-point'
# mutation = 'density'

# Which distance measure to use
distance_measure = 'euclidian'
# distance_measure = 'hamming'

# Crowding Selection goup size [0.01, 0.15]
cs = int(0.01*N)

# Crowding factor [1,4]
cf = 3

# Crowding subpoputaion size [0.01, 0.15]*N
s = int(0.02 * N)
