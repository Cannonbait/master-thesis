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

    def __init__(self, task_queue, result_queue, path, display):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.path = path
        self.display = display
        self.num_consumers = multiprocessing.cpu_count() - 1 # For progress

    def run(self):
        proc_name = self.name
        if(self.path != None):
          framework = serial_framework.PySerialFramework(self.path)
        else:
          framework = serial_framework.PySerialFramework()
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill means shutdown
                self.task_queue.task_done()
                break
            if self.display:
                progbar(next_task.total-self.task_queue.qsize() + self.num_consumers, next_task.total,40)
            vals = []
            deviation = []
            for i, pattern_generator in enumerate(next_task.pattern_generators):
                temp_val = []
                for trial in range(0, next_task.pattern_trials):
                    temp_val.append(framework.test(next_task.get_patterns(pattern_generator),
                    next_task.bits, next_task.store, next_task.blocks,
                    next_task.tests))
                average = sum(temp_val)/next_task.pattern_trials
                vals.append(average)
                deviation.append(np.std(temp_val))
            self.task_queue.task_done()
            self.result_queue.put((next_task.indexes, vals, deviation))


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
