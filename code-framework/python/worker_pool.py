import sys
sys.path.append("../cython/")
import serial_framework
import multiprocessing
import time
import numpy as np

# Definition for progressbar.
def progbar(curr, total, full_progbar):
    frac = curr/total
    filled_progbar = round(frac*full_progbar)
    print('\r', '#'*filled_progbar + '-'*(full_progbar-filled_progbar), '[{:>7.2%}]'.format(frac), end='')

class Consumer(multiprocessing.Process):

    def __init__(self, task_queue, result_queue, sources, display):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.sources = sources
        self.display = display
        self.num_consumers = multiprocessing.cpu_count() - 1 # For progress

    def run(self):
        for source in self.sources:
            framework = serial_framework.PySerialFramework()
            framework.add_source(source)
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                self.task_queue.task_done()
                break
            vals = [[] for source in self.sources]
            deviations = [[] for source in self.sources]
            for pattern_generator in next_task.pattern_generators:
                temp_val = [[] for source in self.sources]
                for trial in range(0, next_task.pattern_trials):
                    patterns = next_task.get_patterns(pattern_generator)
                    for iSource, source in enumerate(self.sources):
                        result = framework.test(next_task.get_patterns(pattern_generator),
                            next_task.bits, next_task.store, next_task.blocks,
                            next_task.tests, source)
                        temp_val[iSource].append(result)
                averages = [sum(val)/next_task.pattern_trials for val in temp_val]
                deviation = [np.std(val) for val in temp_val]

                conversion = [[] for source in self.sources]
                for ix, val in enumerate(averages):
                    vals[ix].append(val)
                for ix, val in enumerate(deviation):
                    deviations[ix].append(val)
            self.task_queue.task_done()
            self.result_queue.put((next_task.indexes, vals, deviations))


class Task:

    def __init__(self, indexes, pattern_generators, bits, num_patterns, store, blocks, tests, pattern_trials, total):
        self.indexes = indexes
        self.pattern_generators = pattern_generators
        self.bits = bits
        self.num_patterns = num_patterns
        self.store = store
        self.blocks = blocks
        self.tests = tests
        self.pattern_trials = pattern_trials
        self.total = total

    def get_patterns(self, generator):
      return generator.generate_patterns(self.bits, self.num_patterns, self.store, self.blocks)


class Controller:
    def __init__(self, path):
        # Establish communication queues
        self.tasks = multiprocessing.JoinableQueue()
        self.results_queue = multiprocessing.Queue()

        # Start consumers
        self.num_consumers = multiprocessing.cpu_count() - 1

        self.consumers = [
            Consumer(self.tasks, self.results_queue, path, False)
            for i in range(self.num_consumers-1)
        ]
        self.consumers.append(Consumer(self.tasks, self.results_queue, path, True))
        for w in self.consumers:
            w.start()
        print("Initializing filters...")


    def test(self, trials, settings):
        for trial in trials:
            self.tasks.put(Task(trial[0], settings.pattern_designs, trial[1]['m'],
            trial[1]['n'], trial[1]['d'],trial[1]['b'], settings.tests,
            settings.pattern_trials, len(trials)))

        # Add a poison pill for each consumer
        for i in range(self.num_consumers):
            self.tasks.put(None)

        self.tasks.join()
        results = []
        for trial in trials:
            results.append(self.results_queue.get())
        return results
