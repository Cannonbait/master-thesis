#include "blocked_filter.h"
#include <time.h>
#include <iostream>
#include <tr1/functional>

using namespace std;

/*
 * Tests if a random element is part of
 * the set represented by the filter.
 *
 */
bool BlockedFilter::test() {
  seed *= 97;
  srand(seed);
  int v = rand();
  v *= 7;
  v = v % filters.size();
  return filters[v].test();
}

/*
 * Tests if a string is a member of a given set
 * represented by the filter.
 *
 */
bool BlockedFilter::test_item(string s) {
  int v = tr1::hash<string>{}(s);
  v *= 7;
  v = v % filters.size();
  return filters[v].test(s);
}

/*
 * Adds a random object to the filter.
 *
 */
void BlockedFilter::add() {
  seed *= 97;
  srand(seed);
  int v = rand();
  v *= 7;
  v = v % filters.size();
  filters[v].add();
}

/*
 * Adds a string object to the filter.
 *
 */
void BlockedFilter::add_item(string s) {
  int v = tr1::hash<string>{}(s);
  v *= 7;
  v = v % filters.size();
  filters[v].add(s);
}

/*
 * Constructor for a standard blocked filter, with b subfilters.
 * @param m: Number of bits per block.
 * @param b: Number of blocks.
 * @param k: Number of hashes.
 * @param s: Seed value.
 *
 */
BlockedFilter::BlockedFilter(int m, int b, int k, size_t s) {
  seed = s;
  for(int i = 0; i < b; i++) {
    s *= 13;
    BloomFilter bloom = BloomFilter(m,k,s);
    filters.push_back(bloom);
  }
}

/*
 * Constructor for a standard blocked filter, with b subfilters.
 * @param m: Number of bits per block.
 * @param b: Number of blocks.
 * @param k: Number of hashes.
 *
 */
BlockedFilter::BlockedFilter(int m, int b, int k) {
  seed = time(0);
  for(int i = 0; i < b; i++) {
    seed *= 13;
    BloomFilter bloom = BloomFilter(m,k,seed);
    filters.push_back(bloom);
  }
}

/*
 * Empty constructor
 */
BlockedFilter::BlockedFilter() {}

/*
 * Prints the filter to standard output.
 */
void BlockedFilter::display() {
  for(size_t i = 0; i < filters.size(); i++) {
    filters[i].print();
  }
}
