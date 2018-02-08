#ifndef P_BLOOM_H
#define P_BLOOM_H
#endif

#include <random>
#include <vector>
#include <iostream>
#include <string>
#include <boost/dynamic_bitset.hpp>
#include <boost/random/mersenne_twister.hpp>
#include <boost/random/uniform_int_distribution.hpp>

using namespace std;

class PatternBF {
  private:
    static int PATTERN_LENGTH;
    static const int PRIME_MULTIPLIER = 7*23*47*51;
    vector<boost::dynamic_bitset<>*> patterns;
    vector<boost::dynamic_bitset<>*> blocks;
    boost::mt19937 random_source;
    void print_pattern(boost::dynamic_bitset<> * pattern);
    bool test(int block_index, int pattern_index); //object
  public:
    PatternBF(int m, int n, int num_blocks, int pattern_length);
    PatternBF(vector<boost::dynamic_bitset<>*> patterns, int num_blocks);
    void add(string str); //object
    void add_many(int x);
    bool test(string str); //object
    bool test_rng();
    double test_rng(int num_tests);
    void print();
};
