from pattern_design.che import CHE
from pattern_design.comp import COMP
from pattern_design.crs import CRS
import sys

def default_arguments():
    arguments = { "m": 512, "n": 4096, "d": 120, "b": 1 }
    arguments["tests"] = 10000
    arguments["pattern_trials"] = 5
    return arguments

def _extract_argument(argv, symbol):
    if any([s.startswith("-{0}=".format(symbol)) for s in argv]):
        return int([x for x in sys.argv if x.startswith("-{0}=".format(symbol))][0][len(symbol)+2:])
    elif symbol in default_arguments():
        return default_arguments()[symbol]
    else:
        return

class AnalysisSettings:
    def __init__(self, argv):
        self.trial_ranges = {}
        range_symbols = ["m", "n", "d", "b"]
        for symbol in range_symbols:
            self.trial_ranges[symbol] = [_extract_argument(argv, symbol)]
            end = _extract_argument(argv, symbol+"_end")
            if end != None:
                self.trial_ranges[symbol].append(end)
                step = _extract_argument(argv, symbol+"_step")
                if step != None:
                    self.trial_ranges[symbol].append(step)
                else:
                    self.trial_ranges[symbol].append(1)

        self.tests = _extract_argument(argv, "tests")
        self.pattern_trials = _extract_argument(argv, "pattern_trials")

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
