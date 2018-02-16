#include "bloom_filter.h"
#include <iostream>
#include <tr1/functional>
#include <time.h>

using namespace std;

/*
 * Computes k random indices and
 * test them.
 */
bool BloomFilter::test() {
  seed *= 97;
  srand(seed);
  int v = rand();
  return test_help(v);
}

/*
 * Tests if a string is stored in the filter.
 */
bool BloomFilter::test(string s) {
  int v = tr1::hash<string>{}(s);
  return test_help(v);
}

// Helper for testing
bool BloomFilter::test_help(int v) {
  int val = v;
  for(int i = 0; i < k; i++) {
    val = v * primes[i];
    val = val % bits.size();
    if(bits[val] != 1) {
      return false;
    }
  }
  return true;
}

/*
 * Adds k uniformly random 1's to the filter
 * with replacement.
 */
void BloomFilter::add() {
  seed *= 97;
  srand(seed);
  int v = rand();
  add_help(v);
}

/*
 * Adds a string to the filter.
 */
void BloomFilter::add(string s) {
  int v = tr1::hash<string>{}(s);
  add_help(v);
}

// Helper for add.
void BloomFilter::add_help(int v) {
  int val = v;
  for(int i = 0; i < k; i++) {
    val = v * primes[i];
    val = val % bits.size();
    bits[val] = 1;
  }
}

/*
 * Constructs a new filter with m bits, k hashes and a seed
 * for random testing.
 */
BloomFilter::BloomFilter(int m, int hashes, unsigned int s) {
  bits = boost::dynamic_bitset<>(m);
  seed = s;
  k = hashes;
}

/*
 * Standard Bloom filter constructor with m bits and k hashes (up to 7).
 */
BloomFilter::BloomFilter(int m, int hashes) {
  seed = time(0);
  bits = boost::dynamic_bitset<>(m);
  k = hashes;
}

void BloomFilter::print() {
  for(size_t i = 0; i < bits.size(); i++) {
    cout << bits[i];
  }
  cout << "\n";
}
