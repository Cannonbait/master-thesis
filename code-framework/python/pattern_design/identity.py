from pattern_design.pattern_interface import IPatternGenerator
import numpy as np
import math
import random
class IDENTITY(IPatternGenerator):

    def generate_patterns(m,n,d,b):
        return np.identity(m)

    def get_name():
        return "Identity matrix"
