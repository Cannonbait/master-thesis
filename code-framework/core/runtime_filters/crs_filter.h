#ifndef CRS_FILTER_H
#define CRS_FILTER_H
#endif

#include <iostream>
#include <random>
#include <vector>
#include "abstract_filter.h"
#include <boost/dynamic_bitset.hpp>

using namespace std;

class CRSFilter: public AbstractFilter {
  public:
    /* Constructors */
    CRSFilter();
    CRSFilter(unsigned int num_bits, unsigned int blocks, unsigned int items);
  private:
    boost::dynamic_bitset<> generate_pattern(unsigned long seed_value) override;
    vector<unsigned int> primes;
    unsigned long universe = 1;
};
