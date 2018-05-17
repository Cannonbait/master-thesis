#ifndef EGH_FILTER_H
#define EGH_FILTER_H
#endif

#include <iostream>
#include <random>
#include <vector>
#include "abstract_filter.h"
#include <boost/dynamic_bitset.hpp>

using namespace std;

class EGHFilter: public AbstractFilter {
  public:
    /* Constructors */
    EGHFilter();
    EGHFilter(unsigned int num_bits, unsigned int blocks, unsigned int items, unsigned int universe);
  private:
    boost::dynamic_bitset<> generate_pattern(unsigned long seed_value) override;
    vector<unsigned int> primes;
    unsigned long universe = 1;
    unsigned long bonus = 1;
};
