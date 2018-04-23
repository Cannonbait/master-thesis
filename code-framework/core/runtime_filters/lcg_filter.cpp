#include "lcg_filter.h"
#include <chrono>
#include <math.h>
#include <boost/dynamic_bitset.hpp>

using namespace std;

LCGFilter::LCGFilter() {}

/*
 * Standard constructor for a LCGFilter.
 * Assumes atleast 1 bit, 1 block, 1 item if less are provided.
 * @param num_bits: the number of bits in each block.
 * @param num_blocks: the number of blocks in the filter.
 * @param items: the expected number of items to be stored in the filter.
 */
LCGFilter::LCGFilter(unsigned int num_bits, unsigned int num_blocks, unsigned int items) {
  if (num_blocks == 0) num_blocks = 1;
  if (num_bits == 0) num_bits = 1;
  if (items == 0) items = 1;

  for (unsigned int i = 0; i < num_blocks; i++) {
    blocks.push_back(new boost::dynamic_bitset<>(num_bits));
  }
  k = round(log(2)*num_blocks*num_bits/items);
}

// Internal helper for constructing a LCP-pattern.
boost::dynamic_bitset<> LCGFilter::generate_pattern(unsigned long seed_value) {
  size_t pattern_size = blocks[0]->size();
  boost::dynamic_bitset<> pattern = boost::dynamic_bitset<>(pattern_size);
  unsigned long current_seed = seed_value;

  // Calculate all indexes to set to 1.
  for(unsigned int i = 0; i < k; i++) {
    current_seed = (multiplier*current_seed+increment) % modulus;
    pattern.set(current_seed % pattern_size);
  }

  return pattern;
}

/*
 * Changes the LCG used to generate patterns.
 * @param new_mod: The new modulus value.
 * @param new_mul: The new multiplier value.
 * @param new_inc: The new increment value.
 */
void LCGFilter::change_lcg(
  unsigned long new_mod,
  unsigned long new_mul,
  unsigned long new_inc) {
    modulus    = new_mod;
    multiplier = new_mul;
    increment  = new_inc;
}
