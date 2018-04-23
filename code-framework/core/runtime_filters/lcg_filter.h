#ifndef LCG_FILTER_H
#define LCG_FILTER_H
#endif

#include <iostream>
#include <random>
#include <vector>
#include <boost/dynamic_bitset.hpp>
#include "abstract_filter.h"

using namespace std;

class LCGFilter: public AbstractFilter {
  public:
    /* Constructors */
    LCGFilter();
    LCGFilter(unsigned int num_bits, unsigned int blocks, unsigned int items);
    void change_lcg(unsigned long new_mod, unsigned long new_mul, unsigned long new_inc);
  private:
    boost::dynamic_bitset<> generate_pattern(unsigned long seed_value) override;
    unsigned long modulus    = 4294967296;
    unsigned long multiplier = 214013;
    unsigned long increment  = 2531011;
    unsigned int k;
};
