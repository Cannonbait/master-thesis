#ifndef CRS_FILTER_H
#define CRS_FILTER_H
#endif

#include <iostream>
#include <random>
#include <vector>
#include <boost/dynamic_bitset.hpp>

using namespace std;

class CRSFilter {
  public:
    /* Constructors */
    CRSFilter();
    CRSFilter(unsigned int num_bits, unsigned int blocks, unsigned int items);
    /* Bloom filter essentials */
    template <class T> bool elem(T item);
    template <class T> void insert(T item);
    unsigned int size();
    /* Experimental neccessities */
    bool try_random();
    void add_random();
  private:
    boost::dynamic_bitset<> generate_pattern(unsigned long seed_value);
    vector<boost::dynamic_bitset<>*> blocks;
    vector<unsigned int> primes;
    unsigned long universe;
};
