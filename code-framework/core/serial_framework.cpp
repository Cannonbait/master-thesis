#include "serial_framework.h"
#include <iostream>
#include <fstream>
#include <thread>
#include <chrono>
#include <boost/algorithm/string.hpp>
#include <gmp.h>
#include <algorithm>
#include <boost/random.hpp>
#include <random>

using namespace std;


SerialFramework::SerialFramework() {}

SerialFramework::SerialFramework(string path) {
  random_source = boost::mt19937(std::chrono::system_clock::now().time_since_epoch().count()*47);
  ifstream data_file(path);
  string line;
  while (getline(data_file, line)) {
    source.push_back(line);
  }
}

double SerialFramework::test_no_path(vector<vector<bool>> patterns,
          int bits, int store, int blocks, int tests) {
    PatternBF bf(convert_patterns(patterns), blocks);
    bf.add_many(store);
    return bf.test_rng(tests);
}

double SerialFramework::test(vector<vector<bool>> patterns,
          int bits, int store, int blocks, int tests){
  //Create pattern
  PatternBF bf(convert_patterns(patterns), blocks);
  if (source.size() == 0) {
    bf.add_many(store);
    return bf.test_rng(tests);
  } else {
    //Store data
    mpz_t value, block_i, pattern_i;
    mpz_init(value);
    mpz_init(block_i);
    mpz_init(pattern_i);
    int multiplier = 47;
    int i1, i2, universe, storage_index;
    universe = source.size()-1;
    std::uniform_int_distribution<int> dist_blk(0, universe);
    
    for(int i = 0; i < store; i++) {
      storage_index = dist_blk(random_source) % universe;
      stored.push_back(source[storage_index]);
      mpz_set_str(value, source[storage_index].c_str(), 10);
      mpz_mul_ui(value, value, multiplier);
      // Should possibly be changed to random lines
      mpz_mod_ui(block_i, value, blocks);
      mpz_mod_ui(pattern_i, value, patterns.size());
      i1 = mpz_get_ui(block_i);
      i2 = mpz_get_ui(pattern_i);
      bf.add_indexes(i1, i2);
    }

    int contained = 0;
    for(int i = store; i < (store+tests); i++) {
      storage_index = dist_blk(random_source) % universe;
      mpz_set_str(value, source[storage_index].c_str(), 10);
      mpz_mul_ui(value, value, multiplier);
      mpz_mod_ui(block_i, value, blocks);
      mpz_mod_ui(pattern_i, value, patterns.size());
      i1 = mpz_get_ui(block_i);
      i2 = mpz_get_ui(pattern_i);

      // The element is a true positive and should not be logged for FPR if it is contained
      if (!(find(stored.begin(), stored.end(), source[i]) != stored.end())) {
        if (bf.test(i1,i2)) {
          contained++;
        }
      }
    }
    mpz_clear(value);
    mpz_clear(block_i);
    mpz_clear(pattern_i);
    return (double)contained/(double)tests;
  }
}

vector<boost::dynamic_bitset<>*> SerialFramework::convert_patterns(vector<vector<bool>> patterns) {
  vector<boost::dynamic_bitset<>*> dyn_patterns(patterns.size());
  for(size_t i = 0; i < patterns.size(); i++) {
    boost::dynamic_bitset<>* bits = new boost::dynamic_bitset<>(patterns[0].size());
    for(size_t j = 0; j < patterns[0].size(); j++){
      (*bits)[j] = patterns[i][j];
    }
    dyn_patterns[i] = bits;
  }
  return dyn_patterns;
  }
