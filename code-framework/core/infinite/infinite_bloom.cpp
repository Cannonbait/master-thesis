#include "infinite_bloom.h"
#include <iostream>
#include <string>
#include <math.h>
#include <vector>
#include <random>
#include <sstream>
#include <boost/dynamic_bitset.hpp>
#include <chrono>
#include <stdexcept>
#include <boost/random.hpp>

using namespace std;

/*
 * Constructor for blocked filter without patterns. Used for testing
 * "infinite" distributions.
 *
 */
InfiniteBF::InfiniteBF(int num_blocks, int num_bits) {
  random_source = boost::mt19937(std::chrono::system_clock::now().time_since_epoch().count());
  for (int i=0; i < num_blocks; i++){
    blocks.push_back(new boost::dynamic_bitset<>(num_bits));
  }
}

/*
 * Adds a randomly constructed pattern to the filter wth level k or k+1.
 * Used for experiments with "infinit" amounts of patterns.
 * @param level_prob: the probability that the pattern has level k+1
 * @param k: the number of ones in each pattern
 *
 */
void InfiniteBF::add(int k) {
  uniform_int_distribution<int> dist_blk(0, blocks.size()-1);
  int block_index = dist_blk(random_source);
  // Construct the random vector
  boost::dynamic_bitset<> b = boost::dynamic_bitset<>(blocks[0]->size());
  for(int i = 0; i < k; i++) {
    b[i] = 1;
  }
  shuffle(b,k);
  
  *blocks[block_index] = (*blocks[block_index] | b);
}

/*
 * Tests a randomly created pattern for membership in the filter.
 * Used for experiments with "infinit" amount of patterns.
 * @param level_prob: the probability that the pattern has level k+1
 * @param stored_items: the number of stored items in the filter.
 *
 */
bool InfiniteBF::test(int k) {
  uniform_int_distribution<int> dist_blk(0, blocks.size()-1);
  int block_index = dist_blk(random_source);
  // Construct the random vector
  boost::dynamic_bitset<> b = boost::dynamic_bitset<>(blocks[0]->size());
  for(int i = 0; i < k; i++) {
    b[i] = 1;
  }
  shuffle(b,k);
  return ((boost::dynamic_bitset<>(*blocks[block_index]).flip()) & b).none();
}

/*
 * Shuffles the first k items of a bitset with size m into the rest
 * of the bitset. Timecomplexity O(k*log(m)).
 */
void InfiniteBF::shuffle(boost::dynamic_bitset<> &bits, int k) {
  int m = bits.size()-1;
  for(int i = 0; i < k; i++) {
    uniform_int_distribution<int> dist_ind(i, m);
    int index = dist_ind(random_source);
    bool temp = bits[i];
    bits[i] = bits[index];
    bits[index] = temp;
  }
}