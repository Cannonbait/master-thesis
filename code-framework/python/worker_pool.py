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
        framework = serial_framework.PySerialFramework(self.path)
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill means shutdown
                print('{}: Exiting'.format(proc_name))
                self.task_queue.task_done()
                break
            answer = framework.test(next_task.get_patterns(), next_task.bits, next_task.store, next_task.blocks, next_task.tests)
            self.task_queue.task_done()
            self.result_queue.put(answer)


class Task:

    def __init__(self, generator, bits, patterns, store, blocks, tests):
      self.generator = generator
      self.bits = bits
      self.patterns = patterns
      self.store = store
      self.blocks = blocks
      self.tests = tests

    def get_patterns(self):
      return self.generator.generate_patterns(self.bits, self.patterns, self.store, self.blocks)



if __name__ == '__main__':
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    # Start consumers
    num_consumers = multiprocessing.cpu_count() * 1
    print('Creating {} consumers'.format(num_consumers))
    consumers = [
        Consumer(tasks, results, "../data-preparation/babesia-bovis/babesia_bovis_raw1.prep")
        for i in range(num_consumers)
    ]
    for w in consumers:
        w.start()

    # Enqueue jobs
    num_jobs = 10
    for i in range(num_jobs):
        tasks.put(Task(comp_pattern.CHE, 10, 20, 10, 3, 10))

    # Add a poison pill for each consumer
    for i in range(num_consumers):
        tasks.put(None)

    # Wait for all of the tasks to finish
    tasks.join()

    # Start printing results
    while num_jobs:
        result = results.get()
        print('Result:', result)
        num_jobs -= 1
