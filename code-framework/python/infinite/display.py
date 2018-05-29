import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

_display_colors = ['tab:orange', 'b', 'g', 'c', 'm', 'r', 'k']

def display_data(results, settings):
    fig, ax = plt.subplots()
    for result in results:
        ax.errorbar(result[0], result[1], result[2],fmt='-bo')

    plt.xlabel("k value")
    plt.ylabel("FPR")
    plt.title("False positive rate as a funtion of k")
    plt.grid(True)
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
