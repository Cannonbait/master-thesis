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
  k = log(2)*num_blocks*num_bits/items;
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
 * Checks if the supplied item is contained in teh filter.
 * @param item: the item to check for membership
 * @requires: the type T of the item must be hashable.
 */
template <class T> bool LCGFilter::elem(T item) {
  unsigned long value = hash<T>()(item);
  unsigned int block = value % blocks.size();
  boost::dynamic_bitset<> pattern = generate_pattern(value);
  return ((boost::dynamic_bitset<>(*blocks[block]).flip()) & pattern).none();
}

/*
 * Inserts an item into the filter.
 * @param item: the item to be inserted.
 * @requires: the type T of the item must be hashable.
 */
template <class T> void LCGFilter::insert(T item) {
  unsigned long value = hash<T>()(item);
  unsigned int block = value % blocks.size();
  boost::dynamic_bitset<> pattern = generate_pattern(value);
  *blocks[block] = (*blocks[block]) | pattern;
}

/*
 * Tries a randomly generated pattern against the filter.
 */
bool LCGFilter::try_random() {
  srand(std::chrono::system_clock::now().time_since_epoch().count());
  boost::dynamic_bitset<> pattern = generate_pattern(rand());
  unsigned int block = rand() % blocks.size();
  return ((boost::dynamic_bitset<>(*blocks[block]).flip()) & pattern).none();
}

/*
 * Adds a randomly constructed pattern to the filter.
 */
void LCGFilter::add_random() {
  srand(std::chrono::system_clock::now().time_since_epoch().count());
  boost::dynamic_bitset<> pattern = generate_pattern(rand());
  unsigned int block = rand() % blocks.size();
  *blocks[block] = (*blocks[block]) | pattern;
}

/*
 * Returns the size of the filter.
 */
unsigned int LCGFilter::size() {
  return (blocks[0]->size())*blocks.size();
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
