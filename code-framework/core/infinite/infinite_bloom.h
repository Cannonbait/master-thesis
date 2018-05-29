#ifndef I_BLOOM_H
#define I_BLOOM_H
#endif

#include <random>
#include <vector>
#include <iostream>
#include <string>
#include <boost/dynamic_bitset.hpp>
#include <boost/random/mersenne_twister.hpp>
#include <boost/random/uniform_int_distribution.hpp>

using namespace std;

class InfiniteBF {
  private:
    vector<boost::dynamic_bitset<>*> blocks;
    boost::mt19937 random_source;
    void shuffle(boost::dynamic_bitset<> &bits, int k);
  public:
    InfiniteBF();
    InfiniteBF(int num_blocks, int num_bits);
    void add(int k);
    bool test(int k);

};
