import sys

sys.argv[1:] = ["-k=5", "-k_end=7", "-k_step=0.1"]

def default_arguments():
    arguments = { "m": 512, "b": 1, "k": 5, "d": 120}
    arguments["tests"] = 10000
    arguments["pattern_trials"] = 5
    return arguments

def _extract_argument(argv, symbol):
    if any([s.startswith("-{0}=".format(symbol)) for s in argv]):
        return [x for x in sys.argv if x.startswith("-{0}=".format(symbol))][0][len(symbol)+2:]
    elif symbol in default_arguments():
        return default_arguments()[symbol]
    else:
        return 

class AnalysisSettings:
    def __init__(self, argv):
        #Extract k entries
        symbol = "k"
        self.k = [float(_extract_argument(argv, symbol))]
        self.k.append(float(_extract_argument(argv, symbol+"_end")))
        step = _extract_argument(argv, symbol+"_step")
        if step != None:
            self.k.append(float(step))
        else:
            self.k.append(0.1)

        self.m = int(_extract_argument(argv, "m"))
        self.b = int(_extract_argument(argv, "b"))
        self.d = int(_extract_argument(argv, "d"))
        self.tests = int(_extract_argument(argv, "tests"))
        self.pattern_trials = int(_extract_argument(argv, "pattern_trials"))

    @staticmethod
    def create_setting(designs, **arguments):
        return 0
