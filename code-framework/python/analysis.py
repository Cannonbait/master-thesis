import sys
sys.path.append('../cython/')

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import serial_framework
import worker_pool
from pattern_design.pattern_interface import IPatternGenerator
from pattern_design.che import CHE
from pattern_design.comp import COMP
from pattern_design.identity import IDENTITY
from pattern_design.crs import CRS
from pattern_design.qary import QARY
from pattern_design.rcrs import RCRS
from mpl_toolkits.mplot3d import Axes3D
#sys.argv[1:] = ["-m=512", "-n=1500", "-d=120", "-d_end=160", "-b=1", "-che", "-comp", "-crs", "-step_size=20", "-pattern_trials=1", "-tests=10000"]
#sys.argv[1:] = ["-source='../data-preparation/out.prep'", "-m=512", "-n=1500", "-d=6000", "-d_end=20000", "-b=100", "-che", "-crs", "-step_size=1000", "-pattern_trials=1", "-tests=10000"]

######################## PARSE ARGUMENTS
def default_arguments():
    arguments = { "m": 512, "n": 4096, "d": 120, "d_end": 180, "b": 1 }
    arguments["tests"] = 10000
    arguments["pattern_trials"] = 5
    arguments["step_size"] = 10
    return arguments

def _extract_argument(argv, symbol):
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
            self.trial_ranges[symbol] = [_extract_argument(argv, symbol)]
            end = _extract_argument(argv, symbol+"_end")
            if end != None:
                self.trial_ranges[symbol].append(end)

        self.tests = _extract_argument(argv, "tests")
        self.pattern_trials = _extract_argument(argv, "pattern_trials")
        self.step_size = _extract_argument(argv, "step_size")

        if any([s.startswith("-compare=") for s in argv]):
            self.compare = [x for x in sys.argv if x.startswith("-compare=")][0][len("-compare="):]
        else:
            self.compare = False
        if any([s.startswith("-source=") for s in argv]):
            self.path = [x for x in sys.argv if x.startswith("-source=")][0][len("-source="):]
            print("Using data from ", self.path)
        else:
            print("Found no \"source\" argument, trials will be run with random input")
            self.compare = False
            self.path = None
        self.pattern_designs = []
        if any([s.startswith("-che") for s in argv]):
            self.pattern_designs.append(CHE)
        if any([s.startswith("-comp") for s in argv]):
            self.pattern_designs.append(COMP)
        if any([s.startswith("-crs") for s in argv]):
            self.pattern_designs.append(CRS)
        if len(self.pattern_designs) == 0:
            print("No pattern designs flagged. Exiting...")
            sys.exit(0)

    @staticmethod
    def create_setting(designs, **arguments):
        return 0

######################## GENERATE DATA
def _generate_dimensions(settings):
    dimensions = []
    for key in settings.trial_ranges:
        if len(settings.trial_ranges[key]) == 2:
            dimensions.append((key, np.arange(settings.trial_ranges[key][0], settings.trial_ranges[key][1], settings.step_size)))
    return dimensions

def _convert_to_matrix(results, dimensions, settings):
    if settings.compare:
        mult = 2
    else:
        mult = 1
    values    = np.zeros([len(dimensions[0][1]), len(settings.pattern_designs)*mult])
    deviation = np.zeros([len(dimensions[0][1]), len(settings.pattern_designs)*mult])
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
    # Set the parameter for all values that are fix (i.e. not a range)


    if len(dimensions) == 0:
        raise ValueError('No ranges not supported')
    elif len(dimensions) == 1:
        trials = []
        controller = worker_pool.Controller(settings.path)
        for ix, x in enumerate(dimensions[0][1]):
            parameters[dimensions[0][0]] = x
            trials.append((ix, parameters.copy()))
        data = _convert_to_matrix(controller.test(trials, settings), dimensions, settings)
        return(data)
    else:
        fpr = np.zeros([dimensions[0][1].size, dimensions[1][1].size])
        trial_parameters = parameters.copy()

        for ix, x in enumerate(dimensions[0][1]):
            for iy, y in enumerate(dimensions[1][1]):
                trial_parameters[dimensions[0][0]] = x
                trial_parameters[dimensions[1][0]] = y
                fpr[ix][iy] = run_trial(trial_parameters, settings)
        return fpr

def _generate_parameters(settings):
    parameters = {}
    for key in settings.trial_ranges:
        if len(settings.trial_ranges[key]) == 1:
            parameter = settings.trial_ranges[key][0]
            if parameter < 1:
                print("Invalid input. One or more arguments are non-positive.")
                print("Exiting...")
                sys.exit(0)
            parameters[key] = parameter
    return parameters

######################## DISPLAY DATA

def display_data(result, deviation, settings):
    dimensions = _generate_dimensions(settings)
    if len(dimensions) == 1:
        fig, ax = plt.subplots()
        x = dimensions[0][1]
        if settings.compare:
            line_colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
            for i in range(0,(result.shape)[1],2):
                ax.errorbar(x,result[:,i],deviation[:,i],fmt='-o',c=line_colors[i//2])
                ax.errorbar(x,result[:,i+1],deviation[:,i+1],fmt='s--',c=line_colors[i//2])
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
    (result, deviation) = generate_data(settings)
    display_data(result, deviation, settings)
