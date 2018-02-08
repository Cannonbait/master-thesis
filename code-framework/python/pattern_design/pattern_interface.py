from abc import ABCMeta, abstractmethod
from numpy import matrix

class IPattern(object):
    __metaclass__ = ABCMeta

    #------------------------------------------------
    # m = bits     (rows)
    # n = patterns (columns)
    # d = items    (defectives)
    #------------------------------------------------
    def __init__(self,m,n,d):
        pass

    #-------------------------------------------------
    # Should return the patterns as a mxn numpy matrix
    #-------------------------------------------------
    @property
    @abstractmethod
    def patterns(self):
        pass
