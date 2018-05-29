import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

_display_colors = ['tab:orange', 'b', 'g', 'c', 'm', 'r', 'k']

def display_data(results, settings):
    dimensions = _generate_dimensions(settings)
    if len(dimensions) > 2:
        raise ValueError("Displaying data over three or more ranges is not supported")

    if len(dimensions) == 1:
        _display_one_dimension(results, settings, dimensions)
    else:
        _display_two_dimensions(results, settings, dimensions)

def _generate_dimensions(settings):
    dimensions = []
    for key in settings.trial_ranges:
        if len(settings.trial_ranges[key]) > 2:
            dimensions.append((key, np.arange(settings.trial_ranges[key][0], settings.trial_ranges[key][1]+1, settings.trial_ranges[key][2])))
    return dimensions

def _display_one_dimension(results, settings, dimensions):
    fig, ax = plt.subplots()
    x = dimensions[0][1]
    for result in results:
        print(result)
        for iy, pattern_design in enumerate(settings.pattern_designs):
            res = [x[iy] for x in result[0]]
            dev = [x[iy] for x in result[1]]
            ax.errorbar(x, res, dev,fmt='-o')

    labels = []
    for source in settings.sources:
        for pattern_design in settings.pattern_designs:
            labels.append(source + " - " + pattern_design.get_name())
    plt.legend(labels)

    if(settings.interpret):
        label = _interpret_parameter(dimensions[0][0])
    else:
        label = dimensions[0][0]
    plt.xlabel(label)
    plt.ylabel("FPR")
    plt.title("False positive rate as a funtion of " + label)
    plt.grid(True)
    plt.show()

def _display_two_dimensions(results, settings, dimensions):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    x, y = np.meshgrid(dimensions[1][1], dimensions[0][1])

    print("a")
    for ix, result in enumerate(results):
        for iy, pattern_design in enumerate(settings.pattern_designs):
            res = [[dim2[iy] for dim2 in dim1] for dim1 in result[0]]
            color = iy + ix*len(settings.pattern_designs)
            ax.plot_surface(x,y,np.asarray(res),color=_display_colors[color])
    print("b")

    # Add legend for planes
    fakeLines = []
    names = []
    for ix, source in enumerate(settings.sources):
        for iy, p_design in enumerate(settings.pattern_designs):
            names.append(source + " - " +p_design.get_name())
            fakeLines.append(mpl.lines.Line2D([iy],[iy], linestyle="none", c=_display_colors[iy + ix*len(settings.pattern_designs)], marker = 'o'))
    ax.legend(fakeLines, names, numpoints = 1)

    if(settings.interpret):
        x_label = _interpret_parameter(dimensions[1][0])
        y_label = _interpret_parameter(dimensions[0][0])
    else:
        x_label = dimensions[1][0]
        y_label = dimensions[0][0]

    plt.title("False positive rate as a funtion of " + x_label + " and " + y_label, y=1.08)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    ax.set_zlabel("FPR")
    plt.show()

def _interpret_parameter(key):
    if key is "m":
        return "bits"
    elif key is "n":
        return "patterns"
    elif key is "b":
        return "blocks"
    elif key is "d":
        return "inserted items"
    else:
        return "Unknown range"
