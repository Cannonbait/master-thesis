from abc import ABCMeta, abstractmethod
import numpy as np

# Interface for the pattern generators
class IPatternGenerator(object):
    __metaclass__ = ABCMeta

    #------------------------------------------------
    # m = bits     (rows)
    # n = patterns (columns)
    # d = items    (defectives)
    # b = blocks   (for item normalization)
    #------------------------------------------------
    @abstractmethod
    def generate_patterns(self,m,n,d,b):
        return np.zeros((n,m), dtype='bool')

    #-------------------------------------------------
    # Should return the name of the pattern
    # generator algorithm. Used for plot label.
    #-------------------------------------------------
    @abstractmethod
    def get_name():
        return "Undefined"
