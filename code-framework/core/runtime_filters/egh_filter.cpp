#include "egh_filter.h"
#include <chrono>
#include <math.h>
#include <boost/dynamic_bitset.hpp>
#include <random>
#include <iostream>

using namespace std;

EGHFilter::EGHFilter() {}

/*
 * Standard constructor for a EGHFilter.
 * Assumes atleast 1 bit, 1 block, 1 item if less are provided.
 * @param num_bits: the number of bits in each block.
 * @param num_blocks: the number of blocks in the filter.
 * @param items: the expected number of items to be stored in the filter.
 */
EGHFilter::EGHFilter(unsigned int num_bits, unsigned int num_blocks, unsigned int items, unsigned int u) {
  if (num_blocks == 0) num_blocks = 1;
  if (num_bits == 0) num_bits = 1;
  if (items == 0) items = 1;

  for (unsigned int i = 0; i < num_blocks; i++) {
    blocks.push_back(new boost::dynamic_bitset<>(num_bits));
  }
  primes = { 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61 };

  universe = u;
}

// Internal helper for constructing a CRS-pattern.
boost::dynamic_bitset<> EGHFilter::generate_pattern(unsigned long seed_value) {
  size_t pattern_size = blocks[0]->size();
  boost::dynamic_bitset<> pattern = boost::dynamic_bitset<>(pattern_size);
  unsigned int column = seed_value % universe;
  unsigned int row_base = 0;

  for(auto && prime: primes) {
    pattern.set((column % prime) + row_base);
    row_base += prime;
  }
  return pattern;
}
