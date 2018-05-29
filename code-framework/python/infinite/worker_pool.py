import sys
sys.path.append("../../cython/")
import infinite_framework
import multiprocessing
import time
import numpy as np

class Consumer(multiprocessing.Process):

    def __init__(self, task_queue, result_queue, display):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.display = display
        self.num_consumers = multiprocessing.cpu_count() - 1 # For progress

    def run(self):
        framework = infinite_framework.PyInfiniteFramework()
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                self.task_queue.task_done()
                break
            vals = []
            for trial in range(0, next_task.pattern_trials):
                result = framework.test(next_task.store, next_task.blocks, next_task.tests, next_task.bits, next_task.level)
                vals.append(result)
            self.task_queue.task_done()
            self.result_queue.put((next_task.level, sum(vals)/next_task.pattern_trials, np.std(vals)))


class Task:

    def __init__(self, level, store, blocks, tests, bits, pattern_trials):
        self.store = store
        self.blocks = blocks
        self.tests = tests
        self.bits = bits
        self.level = level
        self.pattern_trials = pattern_trials


class Controller:
    def __init__(self):
        # Establish communication queues
        self.tasks = multiprocessing.JoinableQueue()
        self.results_queue = multiprocessing.Queue()

        # Start consumers
        self.num_consumers = multiprocessing.cpu_count() - 1

        self.consumers = [
            Consumer(self.tasks, self.results_queue, False)
            for i in range(self.num_consumers-1)
        ]
        self.consumers.append(Consumer(self.tasks, self.results_queue, True))
        for w in self.consumers:
            w.start()
        print("Initializing filters...")


    def test(self, trials, settings):
        for trial in trials:
            self.tasks.put(Task(trial, settings.d, settings.b, settings.tests, settings.m, settings.pattern_trials))

        # Add a poison pill for each consumer
        for i in range(self.num_consumers):
            self.tasks.put(None)

        self.tasks.join()
        results = []
        for trial in trials:
            results.append(self.results_queue.get())
        return results
