#include "worker.h"

using namespace std;

int Worker::try_items(int items) {
  int false_positives = 0;
  for(int j = 0; j < items; j++) {
    if(filter.test_rng()) {
      false_positives++;
    }
  }
  mx.lock();
  fp += false_positives;
  mx.unlock();
  return 0;
}

int Worker::fp = 0;
mutex Worker::mx;

Worker::Worker(int patterns, int items, int blocks)
  : filter(PatternBF(patterns, items, blocks, 55)) {
    filter.add_many(items);
}

void Worker::add_item() {
  filter.add_many(1);
}

int Worker::collect_fp() {
  mx.lock();
  int f = fp;
  fp = 0;
  mx.unlock();
  return f;
}
