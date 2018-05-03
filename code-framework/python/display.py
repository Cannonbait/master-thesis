import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

_display_colors = ['tab:orange', 'b', 'g', 'c', 'm', 'r', 'k']

def display_data(result, deviation, settings):
    dimensions = _generate_dimensions(settings)
    if len(dimensions) > 2:
        raise ValueError("Displaying data over three or more ranges is not supported")

    if len(dimensions) == 1:
        _display_one_dimension(result, deviation, settings, dimensions)
    else:
        _display_two_dimensions(result, deviation, settings, dimensions)

def _generate_dimensions(settings):
    dimensions = []
    for key in settings.trial_ranges:
        if len(settings.trial_ranges[key]) > 2:
            dimensions.append((key, np.arange(settings.trial_ranges[key][0], settings.trial_ranges[key][1]+1, settings.trial_ranges[key][2])))
    return dimensions

def _display_one_dimension(result, deviation, settings, dimensions):
    fig, ax = plt.subplots()
    x = dimensions[0][1]
    if settings.compare:
        for i in range(0,(result.shape)[1],2):
            ax.errorbar(x,result[:,i],deviation[:,i],fmt='-o',c=_display_colors[i//2])
            ax.errorbar(x,result[:,i+1],deviation[:,i+1],fmt='s--',c=_display_colors[i//2])
        labels = []
        for p_design in settings.pattern_designs:
            labels.append('Empirical '   + p_design.get_name())
            labels.append('Theoretical ' + p_design.get_name())
        plt.legend(labels)
    else:
        for i in range((result.shape)[1]):
            ax.errorbar(x,result[:,i],deviation[:,i],fmt='-o')
        plt.legend([p_design.get_name() for p_design in settings.pattern_designs])

    plt.xlabel(dimensions[0][0])
    plt.ylabel("FPR")
    plt.title("False positive rate as a funtion of " + dimensions[0][0])
    plt.grid(True)
    plt.show()

def _display_two_dimensions(result, deviation, settings, dimensions):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    x, y = np.meshgrid(dimensions[1][1], dimensions[0][1])
    for index, val in enumerate(result[0][0]):
        res = [[dim2[index] for dim2 in dim1] for dim1 in result]
        ax.plot_surface(x,y,np.asarray(res),color=_display_colors[index])
    # Add legend for planes
    fakeLines = []
    names = []
    for index, p_design in enumerate(settings.pattern_designs):
        names.append(p_design.get_name())
        fakeLines.append(mpl.lines.Line2D([index],[index], linestyle="none", c=_display_colors[index], marker = 'o'))
    ax.legend(fakeLines, names, numpoints = 1)
    plt.title("False positive rate as a funtion of " + dimensions[1][0] + " and " + dimensions[0][0], y=1.08)
    plt.xlabel(dimensions[1][0])
    plt.ylabel(dimensions[0][0])
    plt.grid(True)
    ax.set_zlabel("FPR")
    plt.show()
