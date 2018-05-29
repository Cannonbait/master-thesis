#ifndef FILTER_FRAME
#define FILTER_FRAME
#endif

#include <vector>
#include "infinite_bloom.h"
#include <future>
#include <string>
#include <boost/random/mersenne_twister.hpp>
#include <boost/random/uniform_int_distribution.hpp>
#include <unordered_map>

class InfiniteFramework {
    private:
        boost::mt19937 random_source;
    public:
        InfiniteFramework();
        double test(int store, int blocks, int tests, int bits, double level);
};