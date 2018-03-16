import sys
sys.path.append('../cython/')

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import framework
import serial_framework
import worker_pool
import pattern_designs
from mpl_toolkits.mplot3d import Axes3D
from pattern_interface import IPatternGenerator
import comp_pattern
sys.argv[1:] = ["-m=509", "-n=1000", "-d=100", "-d_end=120", "-b=1", "-che", "-comp"]


######################## PARSE ARGUMENTS
def default_arguments():
    arguments = {"m": 512, "n": 800, "d": 200, "b":30}
    arguments["tests"] = 1000
    arguments["pattern_trials"] = 2
    return arguments

def extract_argument(argv, symbol):
    if any([s.startswith("-{0}=".format(symbol)) for s in argv]):
        return int([x for x in sys.argv if x.startswith("-{0}=".format(symbol))][0][len(symbol)+2:])
    elif symbol in default_arguments():
        return default_arguments()[symbol]
    else:
        return

class Analysis_Settings:
    def __init__(self, argv):
        self.trial_ranges = {}
        range_symbols = ["m", "n", "d", "b"]
        for symbol in range_symbols:
            self.trial_ranges[symbol] = [extract_argument(argv, symbol)]
            end = extract_argument(argv, symbol+"_end")
            if end != None:
                self.trial_ranges[symbol].append(end)

        self.tests = extract_argument(argv, "tests")
        self.pattern_trials = extract_argument(argv, "pattern_trials")

        if any([s.startswith("-path=") for s in argv]):
            self.path = [x for x in sys.argv if x.startswith("-source=")][0][len("-source="):]
        else:
            print("Found no \"source\" argument, trials will be run with random input")
            self.path = None

        self.pattern_designs = []
        if any([s.startswith("-che") for s in argv]):
            self.pattern_designs.append(comp_pattern.CHE)
        if any([s.startswith("-comp") for s in argv]):
            self.pattern_designs.append(comp_pattern.COMP)
        if len(self.pattern_designs) == 0:
            print("No pattern designs flagged")
            sys.exit(0)

######################## GENERATE DATA
def generate_dimensions(settings):
    dimensions = []
    for key in settings.trial_ranges:
        if len(settings.trial_ranges[key]) == 2:
            dimensions.append((key, np.arange(settings.trial_ranges[key][0], settings.trial_ranges[key][1])))
    return dimensions

def convert_to_matrix(results, dimensions, settings):
    matrix = np.zeros([len(dimensions[0][1]), len(settings.pattern_designs)])
    for result in results:
        matrix[result[0]][:] = result[1]
    return matrix

def generate_data(settings):
    # Check that each pattern generator is an instance of the interface
    if not all([issubclass(gen, IPatternGenerator) for gen in settings.pattern_designs]):
        raise ValueError('One or more generators does not implement the IPatternGenerator interface.')

    dimensions = generate_dimensions(settings)
    parameters = {}
    # Set the parameter for all values that are fix (i.e. not a range)
    for key in settings.trial_ranges:
        if len(settings.trial_ranges[key]) == 1:
            parameters[key] = settings.trial_ranges[key][0]
    # If we have no ranges
    if len(dimensions) == 0:
        print("No ranges not implemented")
        sys.exit(0)
    elif len(dimensions) == 1:
        trials = []
        controller = worker_pool.Controller(settings.path)
        for ix, x in enumerate(dimensions[0][1]):
            parameters[dimensions[0][0]] = x
            trials.append((ix, parameters.copy()))
        
        return(convert_to_matrix(controller.test(trials, settings), dimensions, settings))

    else:
        fpr = np.zeros([dimensions[0][1].size, dimensions[1][1].size])
        trial_parameters = parameters.copy()
        
        for ix, x in enumerate(dimensions[0][1]):
            for iy, y in enumerate(dimensions[1][1]):
                trial_parameters[dimensions[0][0]] = x
                trial_parameters[dimensions[1][0]] = y
                fpr[ix][iy] = run_trial(trial_parameters, settings)
        return fpr

######################## DISPLAY DATA

def display_data(result, settings):
    dimensions = generate_dimensions(settings)
    if len(dimensions) == 1:
        fig, ax = plt.subplots()
        x = dimensions[0][1]
        ax.plot(x,result)
        plt.xlabel(dimensions[0][0])
        plt.ylabel("FPR")
        plt.legend([p_design.get_name() for p_design in settings.pattern_designs])
        plt.title("False positive rate as a funtion of " + dimensions[0][0])
        plt.show()
    else:
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        x, y = np.meshgrid(dimensions[1][1], dimensions[0][1])
        ax.plot_surface(x,y,result)
        plt.xlabel(dimensions[1][0])
        plt.ylabel(dimensions[0][0])
        plt.show()

if __name__ == '__main__':
    settings = Analysis_Settings(sys.argv)
    result = generate_data(settings)
    display_data(result, settings)
