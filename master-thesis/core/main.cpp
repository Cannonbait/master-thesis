#include "patternbloom.h"
#include <vector>
#include <thread>
#include <iostream>
#include <math.h>

using namespace std;
const int NUM_PATTERNS = 25;
const int NUM_STORED_ITEMS = 100;
const int NUM_BLOCKS = 25;

int main23() {
  PatternBF a = *(new PatternBF(NUM_PATTERNS, NUM_STORED_ITEMS, NUM_BLOCKS));
  a.add_many(NUM_STORED_ITEMS);
  cout << a.test_rng(10000000) << endl;
  return 0;
}
