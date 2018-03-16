import sys
sys.path.append("../cython/")
import serial_framework
import multiprocessing
import time
import comp_pattern

class Consumer(multiprocessing.Process):

    def __init__(self, task_queue, result_queue, path):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.path = path

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
                print('{}: Exiting'.format(proc_name))
                self.task_queue.task_done()
                break
            
            vals = []
            for i, pattern_generator in enumerate(next_task.pattern_generators):
                val = 0
                for trial in range(0, next_task.pattern_trials):
                    val = val + framework.test(next_task.get_patterns(pattern_generator),
                    next_task.bits, next_task.store, next_task.blocks,
                    next_task.tests)
                vals.append(val/next_task.pattern_trials)
            self.task_queue.task_done()
            self.result_queue.put((next_task.indexes, vals))


class Task:

    def __init__(self, indexes, pattern_generators, bits, num_patterns, store, blocks, tests, pattern_trials):
        self.indexes = indexes
        self.pattern_generators = pattern_generators
        self.bits = bits
        self.num_patterns = num_patterns
        self.store = store
        self.blocks = blocks
        self.tests = tests
        self.pattern_trials = pattern_trials

    def get_patterns(self, generator):
      return generator.generate_patterns(self.bits, self.num_patterns, self.store, self.blocks)


class Controller:
    def __init__(self, path):
        # Establish communication queues
        self.tasks = multiprocessing.JoinableQueue()
        self.results_queue = multiprocessing.Queue()

        # Start consumers
        self.num_consumers = multiprocessing.cpu_count() * 1
        print('Creating {} worker threads'.format(self.num_consumers))
        
        self.consumers = [
            Consumer(self.tasks, self.results_queue, path)
            for i in range(self.num_consumers)
        ]
        for w in self.consumers:
            w.start()


    def test(self, trials, settings):
        print("Queueing tasks")
        for trial in trials:
            self.tasks.put(Task(trial[0], settings.pattern_designs, trial[1]['m'],
            trial[1]['n'], trial[1]['d'],trial[1]['b'], settings.tests,
            settings.pattern_trials))

        print("Poison")
        # Add a poison pill for each consumer
        for i in range(self.num_consumers):
            self.tasks.put(None)

        print(self.tasks)

        print("Waiting finish")
        self.tasks.join()

        results = []
        for trial in trials:
            results.append(self.results_queue.get())
        return results
