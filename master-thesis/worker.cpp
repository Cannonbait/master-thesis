#include "worker.h"

using namespace std;

void Worker::try_items(int items, promise<int> && p) {
  int false_positives = 0;
  for(int i = 0; i < items; i++) {
    if(filter.test_rng(i+1)) {
      false_positives++;
    }
  }
  p.set_value(false_positives);
}

Worker::Worker(int patterns, int items, int blocks)
  : filter(PatternBF(patterns, items, blocks)) {
    filter.store_patterns(items);
}
