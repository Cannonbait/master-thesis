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
#include <unordered_map>

using namespace std;

SerialFramework::SerialFramework() {}

void SerialFramework::add_source(string source){
  
  if (source == "random"){
    random_source = boost::mt19937(std::chrono::system_clock::now().time_since_epoch().count());  
  }
  else{
    ifstream data_file(source);
    string line;
    vector<string> read_file;
    while (getline(data_file, line)) {
      read_file.push_back(line);
    }
    sources[source] = read_file;
  }
}


double SerialFramework::test(vector<vector<bool>> patterns,
          int bits, int store, int blocks, int tests, string source) {
  validate_parameters(patterns, bits, store, blocks, tests);

  //Create pattern
  PatternBF bf(convert_patterns(patterns), blocks);


  if (source == "random") {
    bf.add_many(store);
    return bf.test_rng(tests);
  } 

  //Initialize needed values
  mpz_t value, block_i, pattern_i;
  mpz_init(value);
  mpz_init(block_i);
  mpz_init(pattern_i);

  int multiplier = 47;
  int block_index, pattern_index, universe, storage_index;
  string data_point;

  universe = sources[source].size()-1;
  std::uniform_int_distribution<int> dist_blk(0, universe);

  //Store data
  for(unsigned int i = 0; i < store; i++) {
    storage_index = dist_blk(random_source) % universe;
    data_point = sources[source][storage_index];
    stored[source].push_back(data_point);
    // Hash the value and get block/pattern indices
    mpz_set_str(value, data_point.c_str(), 10);
    mpz_mul_ui(value, value, multiplier);
    mpz_mod_ui(block_i, value, blocks);
    mpz_mod_ui(pattern_i, value, patterns.size());
    block_index   = mpz_get_ui(block_i);
    pattern_index = mpz_get_ui(pattern_i);
    bf.add_indexes(block_index, pattern_index);
  }

  //Run tests
  int contained = 0;
  for(unsigned int i = 0; i < tests; i++) {
    storage_index = dist_blk(random_source) % universe;
    data_point = sources[source][storage_index];
    mpz_set_str(value, data_point.c_str(), 10);
    mpz_mul_ui(value, value, multiplier);
    mpz_mod_ui(block_i, value, blocks);
    mpz_mod_ui(pattern_i, value, patterns.size());
    block_index   = mpz_get_ui(block_i);
    pattern_index = mpz_get_ui(pattern_i);

    if((!is_true_positive(data_point, source)) && bf.test(block_index,pattern_index)) {
        contained++;
    }
    
    mpz_clear(value);
    mpz_clear(block_i);
    mpz_clear(pattern_i);
  }
  return (double)contained/(double)tests;
}

void SerialFramework::validate_parameters(vector< vector<bool> > patterns, int bits, int store, int blocks, int tests) {
  if(bits < 1 || store < 1 || blocks < 1 || tests < 1 || patterns.size() < 1) {
    throw invalid_argument("One or more parameters have an invalid value");
  }
}

bool SerialFramework::is_true_positive(string item, string source) {
  return find(stored[source].begin(), stored[source].end(), item) != stored[source].end();
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
