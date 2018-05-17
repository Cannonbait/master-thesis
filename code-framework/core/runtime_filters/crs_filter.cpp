#include "crs_filter.h"
#include <chrono>
#include <math.h>
#include <boost/dynamic_bitset.hpp>
#include <random>
#include <iostream>

using namespace std;

CRSFilter::CRSFilter() {}

/*
 * Standard constructor for a CRSFilter.
 * Assumes atleast 1 bit, 1 block, 1 item if less are provided.
 * @param num_bits: the number of bits in each block.
 * @param num_blocks: the number of blocks in the filter.
 * @param items: the expected number of items to be stored in the filter.
 */
CRSFilter::CRSFilter(unsigned int num_bits, unsigned int num_blocks, unsigned int items) {
  if (num_blocks == 0) num_blocks = 1;
  if (num_bits == 0) num_bits = 1;
  if (items == 0) items = 1;

  for (unsigned int i = 0; i < num_blocks; i++) {
    blocks.push_back(new boost::dynamic_bitset<>(num_bits));
  }
  int k = round(log(2)*num_blocks*num_bits/items);
  k = max(k,1);
  // Hard coded solution. Assumes k <= 7 and m = 512
  switch(k) {
    case 1: primes.push_back(512); break;
    case 2: primes = { 241, 269 }; break;
    case 3: primes = { 151, 179, 181 }; break;
    case 4: primes = { 127, 131, 137, 113 }; break;
    case 5: primes = { 73, 101, 103, 107, 127 }; break;
    case 6: primes = { 61, 79, 83, 89, 97, 101 }; break;
    case 7: primes = { 59, 61, 83, 67, 71, 73, 97 }; break;
    case 8: primes = { 47, 53, 59, 61, 67, 71, 73, 79 }; break;
    case 9: primes = { 43, 47, 53, 59, 61, 67, 71, 73, 37 }; break;
    case 10: primes = { 31, 37, 41, 43, 47, 53, 59, 61, 67, 71 }; break;
    case 11: primes = { 23, 29, 31, 37, 41, 43, 47, 53, 61, 67, 79 }; break;
    case 12: primes = { 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67 }; break;
    case 13: primes = { 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 97 }; break;
    case 14: primes = { 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 67, 79 }; break;
    case 15: primes = { 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 79 }; break;
    case 16: primes = { 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 73 }; break;
    case 17: primes = { 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 73 }; break;
    default:
      primes = { 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61 };
  }

  for(unsigned int i = 0; i < primes.size(); i++) {
    universe *= primes[i];
  }
}

// Internal helper for constructing a CRS-pattern.
boost::dynamic_bitset<> CRSFilter::generate_pattern(unsigned long seed_value) {
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
