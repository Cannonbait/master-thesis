import sys

from argument_parser import AnalysisSettings
from pattern_design.example import ExampleGenerator
from pattern_design.comp import COMP
from display import display_data
from data_generator import generate_data

sys.argv[1:] = ["-tests=10", "-d=100", "-d_end=120", "-d_step=10", "-n=110", "-n_end=113", "-che", "-source=random", "-source=random"]
#sys.argv[1:] = ["-tests=10", "-d=110", "-d_end=150", "-d_step=10", "-n=110", "-che", "-crs", "-source=random", "-source=random"]

if __name__ == '__main__':
    settings = AnalysisSettings(sys.argv)
    result = generate_data(settings)
    display_data(result, settings)
