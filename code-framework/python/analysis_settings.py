from pattern_design.che import CHE
from pattern_design.comp import COMP
from pattern_design.mcrs import MCRS
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

        self.sources = []
        for source in [s for s in argv if s.startswith("-source=")]:
            if (source[len("-source=")] == "Random"):
                self.sources.append("random")
            else:
                self.sources.append(source[len("-source="):])
            print("Using data from ", source)
        if not self.sources:
            print("Found no \"source\" argument, falling back to RNG as source")
            self.sources.append("random")
        self.pattern_designs = []
        if any([s.startswith("-che") for s in argv]):
            self.pattern_designs.append(CHE)
        if any([s.startswith("-comp") for s in argv]):
            self.pattern_designs.append(COMP)
        if any([s.startswith("-mcrs") for s in argv]):
            self.pattern_designs.append(MCRS)

    @staticmethod
    def create_setting(designs, **arguments):
        return 0

    def add_designs(self,designs):
        self.pattern_designs += designs
