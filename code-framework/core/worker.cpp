#include "worker.h"

using namespace std;

void Worker::try_items(int items, mutex &mtx) {
  int false_positives = 0;
  for(int i = 0; i < items; i++) {
    if(filter.test_rng()) {
      false_positives++;
    }
  }
  mtx.lock();
  cout << "False Positives: " << false_positives;
  cout << "alskj";
  cout << "sdfkhödfkl";
  mtx.unlock();
}

Worker::Worker(int patterns, int items, int blocks)
  : filter(PatternBF(patterns, items, blocks, 55)) {
    filter.add_many(items);
}
