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
#include <stdexcept>

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
    validate_parameters(patterns, bits, store, blocks, tests);
    PatternBF bf(convert_patterns(patterns), blocks);
    bf.add_many(store);
    return bf.test_rng(tests);
}

double SerialFramework::test(vector<vector<bool>> patterns,
          int bits, int store, int blocks, int tests) {

  validate_parameters(patterns, bits, store, blocks, tests);
  //Create pattern
  PatternBF bf(convert_patterns(patterns), blocks);
  if (source.empty()) {
    bf.add_many(store);
    return bf.test_rng(tests);
  } else {
    //Store data
    mpz_t value, block_i, pattern_i;
    mpz_init(value);
    mpz_init(block_i);
    mpz_init(pattern_i);

    int multiplier = 47;
    int block_index, pattern_index, universe, storage_index;
    string data_point;

    universe = source.size()-1;
    std::uniform_int_distribution<int> dist_blk(0, universe);

    for(unsigned int i = 0; i < store; i++) {
      storage_index = dist_blk(random_source) % universe;
      data_point = source[storage_index];
      stored.push_back(data_point);
      // Hash the value and get block/pattern indices
      mpz_set_str(value, data_point.c_str(), 10);
      mpz_mul_ui(value, value, multiplier);
      mpz_mod_ui(block_i, value, blocks);
      mpz_mod_ui(pattern_i, value, patterns.size());
      block_index   = mpz_get_ui(block_i);
      pattern_index = mpz_get_ui(pattern_i);
      bf.add_indexes(block_index, pattern_index);
    }

    int contained = 0;
    for(unsigned int i = 0; i < tests; i++) {
      storage_index = dist_blk(random_source) % universe;
      data_point = source[storage_index];
      mpz_set_str(value, data_point.c_str(), 10);
      mpz_mul_ui(value, value, multiplier);
      mpz_mod_ui(block_i, value, blocks);
      mpz_mod_ui(pattern_i, value, patterns.size());
      block_index   = mpz_get_ui(block_i);
      pattern_index = mpz_get_ui(pattern_i);

      if((!is_true_positive(data_point)) && bf.test(block_index,pattern_index)) {
          contained++;
      }
    }
    mpz_clear(value);
    mpz_clear(block_i);
    mpz_clear(pattern_i);
    return (double)contained/(double)tests;
  }
}

void SerialFramework::validate_parameters(vector< vector<bool> > patterns, int bits, int store, int blocks, int tests) {
  if(bits < 1 || store < 1 || blocks < 1 || tests < 1 || patterns.size() < 1) {
    throw invalid_argument("One or more parameters have an invalid value");
  }
}

bool SerialFramework::is_true_positive(string item) {
  return find(stored.begin(), stored.end(), item) != stored.end();
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
