#include "patternbloom.h"
#include <vector>
#include <thread>
#include <iostream>
#include <math.h>

using namespace std;
const int NUM_PATTERNS = 20;
const int NUM_STORED_ITEMS = 100;
const int NUM_BLOCKS = 20;
const int PATTERN_LENGTH = 50;

int main() {
  // Test for bloom filter to generate own bloom filters
  PatternBF a (NUM_PATTERNS, NUM_STORED_ITEMS, NUM_BLOCKS, PATTERN_LENGTH);
  a.add_many(NUM_STORED_ITEMS);
  cout << a.test_rng(100000) << endl;



  // Test for sending patterns to constructor for bloom filter
  vector<boost::dynamic_bitset<>*> patterns;

  for (int i=0; i < NUM_PATTERNS; i++){
    patterns.push_back(new boost::dynamic_bitset<>(PATTERN_LENGTH));
  }

  const int k = (PATTERN_LENGTH/NUM_STORED_ITEMS)*log(2)+1;
  boost::mt19937 random_source = boost::mt19937(std::chrono::system_clock::now().time_since_epoch().count());
  boost::random::uniform_int_distribution<> pattern_dist(0,PATTERN_LENGTH-1);
  for (int i = 0; i < NUM_PATTERNS; i++){
    for (int j = 0; j < k; j++){
      (*patterns[i])[pattern_dist(random_source)] = 1;
    }
  }

  PatternBF b (patterns, NUM_BLOCKS);
  b.add_many(NUM_STORED_ITEMS);
  cout << b.test_rng(1000000) << endl;



  return 0;
}
