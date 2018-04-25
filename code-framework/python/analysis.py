import sys
sys.path.append('../cython/')

import serial_framework
import worker_pool
from analysis_settings import AnalysisSettings
from pattern_design.pattern_interface import IPatternGenerator
from pattern_design.identity import IDENTITY
from pattern_design.example import ExampleGenerator
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
from display import display_data
import matplotlib

#sys.argv[1:] = ["-d_end=151", "-d_step=10", "-b_step=2", "-b_end=21", "-che", "-crs"]

######################## PARSE ARGUMENTS


######################## GENERATE DATA
def _generate_dimensions(settings):
    dimensions = []
    for key in settings.trial_ranges:
        if len(settings.trial_ranges[key]) > 2:
            dimensions.append((key, np.arange(settings.trial_ranges[key][0], settings.trial_ranges[key][1]+1, settings.trial_ranges[key][2])))
    return dimensions

def convert_to_matrix(results, dimensions, settings):
    matrix_arguments = []
    for dimension in dimensions:
        matrix_arguments.append(len(dimension[1]))

    matrix_arguments.append(len(settings.pattern_designs))
    values    = np.zeros(matrix_arguments)
    deviation = np.zeros(matrix_arguments)
    for result in results:
        values[result[0]][:] = result[1]
        deviation[result[0]][:] = result[2]
    return (values, deviation)

def generate_data(settings):
    # Check that each pattern generator is an instance of the interface
    if not all([issubclass(gen, IPatternGenerator) for gen in settings.pattern_designs]):
        raise ValueError('One or more generators does not implement the IPatternGenerator interface.')

    dimensions = _generate_dimensions(settings)
    parameters = _generate_parameters(settings)

    if len(dimensions) == 0:
        raise ValueError('No ranges not supported')
    elif len(dimensions) == 1:
        trials = []
        controller = worker_pool.Controller(settings.path)
        for ix, x in enumerate(dimensions[0][1]):
            parameters[dimensions[0][0]] = x
            trials.append(((ix), parameters.copy()))
        return(convert_to_matrix(controller.test(trials, settings), dimensions, settings))
    else:
        trials = []
        controller = worker_pool.Controller(settings.path)
        for ix, x in enumerate(dimensions[0][1]):
            parameters[dimensions[0][0]] = x
            for iy, y in enumerate(dimensions[1][1]):
                parameters[dimensions[1][0]] = y
                trials.append(((ix, iy), parameters.copy()))
        return(convert_to_matrix(controller.test(trials, settings), dimensions, settings))

def _generate_parameters(settings):
    parameters = {}
    for key in settings.trial_ranges:
        if len(settings.trial_ranges[key]) == 1:
            parameter = settings.trial_ranges[key][0]
            if parameter < 1:
                raise ValueError("Invalid input. One or more arguments are non-positive.")
                sys.exit(0)
            parameters[key] = parameter
    return parameters

if __name__ == '__main__':
    settings = AnalysisSettings(sys.argv)
    settings.pattern_designs.append(ExampleGenerator)
    (result, deviation) = generate_data(settings)
    display_data(result, deviation, settings)
