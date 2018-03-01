#ifndef LCG_FILTER_H
#define LCG_FILTER_H
#endif

#include <iostream>
#include <random>
#include <vector>
#include <boost/dynamic_bitset.hpp>

using namespace std;

class LCGFilter {
  public:
    /* Constructors */
    LCGFilter();
    LCGFilter(unsigned int num_bits, unsigned int blocks, unsigned int items);
    /* Bloom filter essentials */
    template <class T> bool elem(T item);
    template <class T> void insert(T item);
    unsigned int size();
    /* Experimental neccessities */
    bool try_random();
    void add_random();
    void change_lcg(unsigned long new_mod, unsigned long new_mul, unsigned long new_inc);
  private:
    boost::dynamic_bitset<> generate_pattern(unsigned long seed_value);
    vector<boost::dynamic_bitset<>*> blocks;
    unsigned long modulus    = 4294967296;
    unsigned long multiplier = 214013;
    unsigned long increment  = 2531011;
    unsigned int k;
};
