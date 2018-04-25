import sys
sys.path.append("../cython/")
from analysis_settings import AnalysisSettings
from pattern_design.example import ExampleGenerator
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from display import display_data
from data_generator import generate_data

#sys.argv[1:] = ["-d_end=151", "-d_step=10", "-b_step=2", "-b_end=21", "-che", "-crs"]

if __name__ == '__main__':
    settings = AnalysisSettings(sys.argv)
    settings.pattern_designs.append(ExampleGenerator)
    (result, deviation) = generate_data(settings)
    display_data(result, deviation, settings)
