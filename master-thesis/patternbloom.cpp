#include "patternbloom.h"
#include <iostream>
#include <tr1/functional>
#include <string>
#include <math.h>
#include <vector>
#include <random>
#include <sstream>
#include <boost/dynamic_bitset.hpp>


using namespace std;

void PatternBF::add(string str) {
  size_t val = tr1::hash<string>()(str);
  val = val % blocks.size();
  boost::dynamic_bitset<> *block = &blocks[val];
  val = tr1::hash<string>()(str);
  val = (val*PRIME_MULTIPLIER) % patterns.size();
  *block = (*block | patterns[val]);
}

/**
  * Add x number of patterns to the bloom filter, with random pattern and random block
**/
void PatternBF::add_many(int x) {
  for(int i = 0; i < x; i++){
    std::uniform_int_distribution<int> dist_patt(0, patterns.size()-1);
    std::uniform_int_distribution<int> dist_blk(0, blocks.size()-1);
    int blk_i = dist_blk(random_source);
    blocks[blk_i] = ((blocks[blk_i]) | (patterns[dist_patt(random_source)]));
  }
}

bool PatternBF::test(string str) {
  size_t val = tr1::hash<string>()(str);
  val = val % blocks.size();
  boost::dynamic_bitset<> *block = &blocks[val];
  val = tr1::hash<string>()(str);
  val = (val*PRIME_MULTIPLIER) % patterns.size();
  boost::dynamic_bitset<> *pattern = &patterns[val];
  return test(block, pattern);
}

bool PatternBF::test(boost::dynamic_bitset<> *block, boost::dynamic_bitset<> *pattern){
  for(int i = 0; i < patterns.size(); i++) {
    if((*pattern)[i] == 1 && (*block)[i] != 1) {
      return false;
    }
  }
  return true;
}

bool PatternBF::test_rng(){
  std::uniform_int_distribution<int> dist_patt(0, patterns.size()-1);
  std::uniform_int_distribution<int> dist_blk(0, blocks.size()-1);
  return test(&blocks[dist_blk(random_source)], &patterns[dist_patt(random_source)]);
}

PatternBF::PatternBF(int n, int d, int num_blocks) {
  patterns.assign(n, boost::dynamic_bitset<>(PATTERN_LENGTH));
  blocks.assign(num_blocks, boost::dynamic_bitset<>(PATTERN_LENGTH));
  const int k = (PATTERN_LENGTH/d)*log(2)+1;

  //Stuff for random patterns
  std::random_device rd;  //Will be used to obtain a seed for the random number engine

  std::mt19937 gen(rd());
  random_source = gen; //Standard mersenne_twister_engine seeded with rd()
  std::uniform_int_distribution<int> distribution(0, PATTERN_LENGTH-1);
  for (int i = 0; i < n; i++){
    for (int j = 0; j < k; j++){
      patterns[i][distribution(random_source)] = 1;
    }
  }
}

PatternBF::PatternBF() {}

/*void PatternBF::print(){
  cout << endl << "Patterns" << endl << "---------------------------" << endl;
  print_patterns(patterns);
  cout << endl << "Blocks" << endl << "---------------------------" << endl;
  print_patterns(blocks);
}*/

void PatternBF::print_patterns(vector<boost::dynamic_bitset<>> patterns){
  for (int i = 0; i < patterns.size(); i++){
    print_pattern(patterns[i]);
  }
}

void PatternBF::print_pattern(boost::dynamic_bitset<> pattern){
  std::stringstream ss;
  for (size_t i=0; i < pattern.size(); i++){
    if (i != 0){
      ss << ",";
    }
    ss << pattern[i];
  }
  cout << ss.str() << endl;
}
