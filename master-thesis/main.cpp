#include "worker.h"
#include <vector>
#include <thread>
#include <iostream>

using namespace std;
const int TESTS_PER_THREAD = 1000;
const int PATTERNS = 25;
const int STORED_ITEMS = 500;
const int BLOCKS = 20;

int main() {
  unsigned concurentThreadsSupported = thread::hardware_concurrency();
  vector<Worker> workers;
  vector<thread> threads;
  vector< future<int> > futures;

  for (int i = 0; i < concurentThreadsSupported-1; i++) {
    workers.push_back(Worker(PATTERNS,STORED_ITEMS,BLOCKS));
    promise<int> p;
    futures.push_back(p.get_future());
    threads.emplace_back(&Worker::try_items, workers[i], TESTS_PER_THREAD, move(p));
  }

  for (auto& t : threads) {
    t.join();
  }

  int total_false_pos = 0;
  for (future<int>& f : futures) {
    total_false_pos += f.get();
  }
  int total_tests = TESTS_PER_THREAD*(concurentThreadsSupported-1);
  cout << "The FPR is: " << total_false_pos << "/" << total_tests;
  cout << " (" << (static_cast<double>(total_false_pos) / (double)(1.0 * total_tests))*100.0 << "%)\n";
  return 0;
}
