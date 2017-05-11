from bokeh.plotting import figure, output_file, show, save
import numpy as np

def plot(func, dots, values, min=0, max=1):
    p = figure()
    output_file('basic_plot.html')
    x = np.linspace(min, max ,500)
    p.line(x, func(x))
    p.scatter(dots, values, fill_color='red')

    # show(p)
    save(p)
