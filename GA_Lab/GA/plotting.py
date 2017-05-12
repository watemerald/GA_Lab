# from bokeh.plotting import figure, output_file, show, save
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def plot(func, dots, values,filename, min=0, max=1):
    # p = plt.figure()
    # output_file('basic_plot.html')
    # x = np.linspace(min, max ,500)
    # p.line(x, func(x))
    # p.scatter(dots, values, fill_color='red')
    #
    # # show(p)
    # save(p)
    x = np.linspace(min, max, 500)
    plt.plot(x, func(x))
    plt.scatter(dots, values, color='r')

    plt.savefig('Images/{}'.format(filename))
