#ifndef P_BLOOM_H
#define P_BLOOM_H
#endif

#include <bitset>
#include <vector>
#include <iostream>
#include <boost/dynamic_bitset.hpp>

using namespace std;

class PatternBF {
  private:
    static const int PATTERN_LENGTH = 10;
    static const int PRIME_MULTIPLIER = 7*23*47;
    vector<boost::dynamic_bitset<>> patterns;
    vector<boost::dynamic_bitset<>> blocks;
  public:
    PatternBF(int m, int n, int num_blocks);
    void add(string str); //object
    bool test(string str); //object
    void print();
    void print_pattern(boost::dynamic_bitset<> pattern);
    void print_patterns(vector<boost::dynamic_bitset<>> patterns);
    PatternBF(bitset<8> pattern); // TODO
};
