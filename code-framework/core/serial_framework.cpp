#include "serial_framework.h"
#include <iostream>
#include <fstream>
#include <thread>
#include <chrono>
#include <boost/algorithm/string.hpp>
using namespace std;


SerialFramework::SerialFramework() {}
SerialFramework::SerialFramework(string path){
  ifstream data_file(path);
  string line;
  while (getline(data_file, line)){
    source.push_back(stoi(line.substr(0, 8)));
  }
}

double SerialFramework::test(vector<vector<bool>> patterns,
          int bits, int store, int blocks, int tests){
  //Create pattern
  PatternBF bf(convert_patterns(patterns), blocks);

  if (source.size() == 0){
    bf.add_many(store);
    return bf.test_rng(tests);
  }
  else{
    //Store data
    for(int i = 0; i < store; i++){
      // Should possibly be changed to random lines
      int i1 = source[i] % blocks;
      int i2 = source[i] % patterns.size();
      bf.add_indexes((source[i] % blocks), (source[i] % patterns.size()));
    }

    int contained = 0;
    for(int i = store; i < (store+tests); i++){
      if(bf.test(source[i] % blocks, source[i] % patterns.size())){
        contained++;
      }
    }
    return contained/(double)tests;
  }
}

vector<boost::dynamic_bitset<>*> SerialFramework::convert_patterns(vector<vector<bool>> patterns){
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

