from pbloom import PyPatternBF
from multiprocessing import Process, Queue
import multiprocessing
import time

class PatternFramework:
    def __work(self,q,filter,tests):
        false_positives = 0
        for i in range(tests):
            if filter.test_rng():
                false_positives = false_positives + 1
        q.put(false_positives)

    def test_thoretical_filter(self,tests,patterns,items,blocks):
        cpus = multiprocessing.cpu_count()
        tests_per_process = tests//cpus;
        q = Queue()
        procs = [None]*cpus

        for i in range(cpus):
            filt = PyPatternBF(patterns,items,blocks)
            filt.add_many(items)
            procs[i] = Process(target=self.__work, args=(q,filt,tests_per_process))
            procs[i].start()

        total_errors = 0
        for i in range(cpus):
            total_errors = total_errors + q.get()

        for i in range(cpus):
            procs[i].join()

        return total_errors/tests_per_process

if __name__ == '__main__':
    p = PatternFramework()
    start_time = time.time()
    print(p.test_thoretical_filter(100000000,32,150,32))
    print("--- %s seconds ---" % (time.time() - start_time))
