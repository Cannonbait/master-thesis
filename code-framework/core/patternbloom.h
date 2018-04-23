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
    void validate_parameters(int num_patterns, int num_items_to_store, int num_blocks, int num_bits);
  public:
    PatternBF();
    PatternBF(int patterns, int items, int num_blocks, int pattern_length);
    PatternBF(vector<boost::dynamic_bitset<>*> patterns, int num_blocks);
    PatternBF(int num_blocks, int num_bits);
    void add(string str); //object
    void add_random(double level_prob, int k);
    void add_indexes(int block_index, int pattern_index);
    void add_many(int x);
    bool test(string str); //object
    bool test(int block_index, int pattern_index); //object
    bool test_rng();
    bool test_random_pattern(double level_prob, int k);
    double test_rng(int num_tests);
    void print();
};
