#include "worker.h"

using namespace std;

void Worker::try_items(int items, promise<int> && p) {
  int false_positives = 0;
  for(int j = 0; j < items; j++) {
    if(filter.test_rng()) {
      false_positives++;
    }
  }
  p.set_value(false_positives);
}

Worker::Worker(int bits, int patterns, int items, int blocks)
  : filter(PatternBF(patterns, items, blocks, bits)) {
    filter.add_many(items);
}

void Worker::add_item() {
  filter.add_many(1);
}
