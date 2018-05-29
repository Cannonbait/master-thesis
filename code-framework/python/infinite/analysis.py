import sys

from argument_parser import AnalysisSettings
from display import display_data
from data_generator import generate_data

sys.argv[1:] = ["-k=4.0", "-k_end=9.0", "-k_step=0.1", "-tests=1000000", "-pattern_trials=100", "-d=100", "-m=512"]
#sys.argv[1:] = ["-tests=10", "-d=110", "-d_end=150", "-d_step=10", "-n=110", "-che", "-crs", "-source=random", "-source=random"]

if __name__ == '__main__':
    settings = AnalysisSettings(sys.argv)
    result = generate_data(settings)
    display_data(result, settings)
