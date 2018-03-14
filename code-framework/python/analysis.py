import sys
sys.path.append('../cython/')

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import framework
import math
import pattern_designs
from mpl_toolkits.mplot3d import Axes3D
from pattern_interface import IPatternGenerator
import comp_pattern
sys.argv[1:] = ["-m=509", "-n=1000", "-d=100", "-d_end=143", "-b=1", "-che", "-comp"]


######################## PARSE ARGUMENTS
def default_arguments():
    arguments = {"m": 512, "n": 800, "d": 200, "b":1}
    arguments["tests"] = 90000
    arguments["pattern_trials"] = 3
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

        if any([s.startswith("-source=") for s in argv]):
            self.source = [x for x in sys.argv if x.startswith("-source=")][0][len("-source="):]
        else:
            print("Found no \"source\" argument, trials will be run with random input")
            self.source = None

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

def run_trial(trial_parameters, settings):
    """Returns an average value and its standard deviation for every generator"""
    average = [0.0]*(len(settings.pattern_designs)+1)
    std = [0.0]*(len(settings.pattern_designs)+1)
    bits = trial_parameters["m"]
    patterns = trial_parameters["n"]
    stored = trial_parameters["d"]
    blocks = trial_parameters["b"]
    f = framework.PyFilterFramework(bits, patterns, stored, blocks)
    for index, generator in enumerate(settings.pattern_designs):
        av_val = 0.0
        std_val = [0.0]*settings.pattern_trials
        for trial in range(0, settings.pattern_trials):
            f.replace_patterns(generator.generate_patterns(bits, patterns, stored, blocks), blocks)
            f.add_items(stored)
            result = f.test_framework(settings.tests)
            av_val = av_val + result
            std_val[trial] = result
        average[index] = av_val / settings.pattern_trials
        # Calculate the standard deviation
        total = 0.0
        for value in std_val:
            total = total + pow(value-average[index],2)
        if(settings.tests > 1):
            std[index] = math.sqrt(total/(settings.pattern_trials-1))
        else:
            std[index] = math.sqrt(total)

    k_val = math.log(2)*bits/(stored/blocks)
    bloom_val = (1-2.72**(-k_val*(stored/blocks)/bits))**k_val
    average[len(settings.pattern_designs)] = bloom_val
    return (average, std)

def progbar(curr, total, full_progbar):
    frac = curr/total
    filled_progbar = round(frac*full_progbar)
    print('\r', '#'*filled_progbar + '-'*(full_progbar-filled_progbar), '[{:>7.2%}]'.format(frac), end='')

def generate_data(settings):
    """Generates an average value and std for each design over the specified range(s)"""
    # Check that each pattern generator is an instance of the interface
    if not all([issubclass(gen, IPatternGenerator) for gen in settings.pattern_designs]):
        raise ValueError('One or more generators does not implement the IPatternGenerator interface.')

    print("Generating data...")
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
        fpr = np.zeros((dimensions[0][1].size,len(settings.pattern_designs)+1))
        std = np.zeros((dimensions[0][1].size,len(settings.pattern_designs)+1))
        trial_parameters = parameters.copy()
        counter = 0
        progbar(0, dimensions[0][1].size, 40)
        for ix, x in enumerate(dimensions[0][1]):
            trial_parameters[dimensions[0][0]] = x
            (average, standard) = run_trial(trial_parameters, settings)
            fpr[ix,:] = average
            std[ix,:] = standard
            counter = counter + 1
            progbar(counter, dimensions[0][1].size, 40)
        print("\nDone.")
        return (fpr,std)

    else:
        fpr = np.zeros([dimensions[0][1].size, dimensions[1][1].size])
        std = np.zeros((dimensions[0][1].size,len(generator_list)))
        trial_parameters = parameters.copy()
        for ix, x in enumerate(dimensions[0][1]):
            for iy, y in enumerate(dimensions[1][1]):
                trial_parameters[dimensions[0][0]] = x
                trial_parameters[dimensions[1][0]] = y
                fpr[ix][iy] = run_trial(trial_parameters, settings.pattern_trials, settings.tests)
        return (fpr,std)

######################## DISPLAY DATA
def display_data(result, settings):
    (average,std) = result
    dimensions = generate_dimensions(settings)
    if len(dimensions) == 1:
        fig, ax = plt.subplots()
        x = dimensions[0][1]
        for i in range(average[0,:].size):
            ax.errorbar(x,average[:,i],std[:,i], marker="*", mew=3, elinewidth=1)
        plt.xlabel(dimensions[0][0])
        plt.ylabel("FPR")
        legends = [p_design.get_name() for p_design in settings.pattern_designs]
        legends.append('Bloom filter')
        plt.legend(legends)
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

settings = Analysis_Settings(sys.argv)
result = generate_data(settings)
display_data(result, settings)
