#include "patternbloom.h"
#include <iostream>
#include <string>
#include <math.h>
#include <vector>
#include <random>
#include <sstream>
#include <boost/dynamic_bitset.hpp>
#include <chrono>


using namespace std;


PatternBF::PatternBF(){}

/*
 *  Standard constructor for blocked bloom filters. Initializes the patterns
 *  with k random 1's sampled with replacement. Does not populate the filter.
 */
PatternBF::PatternBF(int num_patterns, int num_items_to_store, int num_blocks, int num_bits) {
  for (int i=0; i < num_blocks; i++){
    blocks.push_back(new boost::dynamic_bitset<>(num_bits));
  }
  for (int i=0; i < num_patterns; i++){
    patterns.push_back(new boost::dynamic_bitset<>(num_bits));
  }
  const int k = (num_bits/num_items_to_store)*log(2)+1;
  random_source = boost::mt19937(std::chrono::system_clock::now().time_since_epoch().count());
  boost::random::uniform_int_distribution<> pattern_dist(0,num_bits-1);
  for (int i = 0; i < num_patterns; i++) {
    for (int j = 0; j < k; j++){
      (*patterns[i])[pattern_dist(random_source)] = 1;
    }
  }
}

/*
 * Constructor for bloom filters with fixed patterns. Does not
 * populate the filter.
 */
PatternBF::PatternBF(vector<boost::dynamic_bitset<>*> arg_patterns, int num_blocks){
  random_source = boost::mt19937(std::chrono::system_clock::now().time_since_epoch().count());
  for (int i=0; i < num_blocks; i++){
    blocks.push_back(new boost::dynamic_bitset<>((*arg_patterns[0]).size()));
  }
  for (size_t i=0; i < arg_patterns.size(); i++) {
    patterns.push_back(new boost::dynamic_bitset<>(*arg_patterns[i]));
  }
}

/*
 *  Adds a string item to the filter.
 */
void PatternBF::add(string str) {
  int block_index = std::hash<string>()(str) % blocks.size();
  int pattern_index = std::hash<string>()(str)*PRIME_MULTIPLIER % patterns.size();
  *blocks[block_index] = (*blocks[block_index] | (*patterns[pattern_index]));
}

void PatternBF::add_indexes(int block_index, int pattern_index){
  *blocks[block_index] = (*blocks[block_index] | (*patterns[pattern_index]));
}


/**
  * Add x number of patterns to the bloom filter, with random pattern and random block
**/
void PatternBF::add_many(int x) {
  for(int i = 0; i < x; i++){
    std::uniform_int_distribution<int> dist_patt(0, patterns.size()-1);
    std::uniform_int_distribution<int> dist_blk(0, blocks.size()-1);
    int block_index = dist_blk(random_source);
    *blocks[block_index] = (*blocks[block_index] | (*patterns[dist_patt(random_source)]));
  }
}

/*
 *  Tests a string item for membership in the filter.
 */
bool PatternBF::test(string str) {
  random_source = boost::mt19937(std::chrono::system_clock::now().time_since_epoch().count());
  int block_index = std::hash<string>()(str) % blocks.size();
  int pattern_index = (std::hash<string>()(str)*PRIME_MULTIPLIER) % patterns.size();
  return test(block_index, pattern_index);
}

/*
 * Makes a test of a random pattern in a random block for theoretical wokloads.
 */
bool PatternBF::test_rng(){
  random_source = boost::mt19937(std::chrono::system_clock::now().time_since_epoch().count());
  std::uniform_int_distribution<int> dist_patt(0, patterns.size()-1);
  std::uniform_int_distribution<int> dist_blk(0, blocks.size()-1);
  return test(dist_blk(random_source), dist_patt(random_source));
}

/*
 * Tests a fixed numbre of theoretical items.
 * Returns the FPR from these tests.
 */
double PatternBF::test_rng(int num_tests){
  int contains = 0;
  for (int i = 0; i < num_tests; i++){
    if (test_rng()){
      contains += 1;
    }
  }
  return (double)contains/(double)num_tests;
}

/*
 *  Prints a filters blocks and patterns.
 */
void PatternBF::print(){
  cout << endl << "Patterns" << endl << "---------------------------" << endl;
  for (size_t i = 0; i < patterns.size(); i++){
    print_pattern(patterns[i]);
  }
  cout << endl << "Blocks" << endl << "---------------------------" << endl;
  for (size_t i = 0; i < blocks.size(); i++){
    print_pattern(blocks[i]);
  }
}

// Helper for print()
void PatternBF::print_pattern(boost::dynamic_bitset<> * pattern){
  std::stringstream ss;
  for (size_t i=0; i < (*pattern).size(); i++){
    if (i != 0){
      ss << ",";
    }
    ss << (*pattern)[i];
  }
  cout << ss.str() << endl;
}

/*
 * Performs a test with a fixed block and pattern.
 */
bool PatternBF::test(int block_index, int pattern_index){
  return ((boost::dynamic_bitset<>(*blocks[block_index]).flip()) & (*patterns[pattern_index])).none();
}
