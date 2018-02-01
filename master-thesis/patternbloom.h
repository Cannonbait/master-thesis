#ifndef P_BLOOM_H
#define P_BLOOM_H
#endif

#include <random>
#include <vector>
#include <iostream>
#include <string>
#include <boost/dynamic_bitset.hpp>

using namespace std;

class PatternBF {
  private:
    static const int PATTERN_LENGTH = 512;
    static const int PRIME_MULTIPLIER = 7*23*47;
    vector<boost::dynamic_bitset<>> patterns;
    vector<boost::dynamic_bitset<>> blocks;
    std::mt19937 random_source;
    void print_pattern(boost::dynamic_bitset<> pattern);
    void print_patterns(vector<boost::dynamic_bitset<>> patterns);
    bool test(boost::dynamic_bitset<> *block, boost::dynamic_bitset<> *pattern); //object
  public:
    PatternBF();
    PatternBF(int n, int d, int num_blocks);
    void add(string str); //object
    void add_many(int x);
    bool test(string str); //object
    bool test_rng();
  //  void print();
};
