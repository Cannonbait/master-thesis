#ifndef FILTER_FRAME
#define FILTER_FRAME
#endif

#include <vector>
#include "patternbloom.h"
#include <future>
#include <string>
#include <boost/random/mersenne_twister.hpp>
#include <boost/random/uniform_int_distribution.hpp>

using namespace std;

class SerialFramework {
  private:
    vector<string> source;
    vector<string> stored; // To check actual FPR and not true positives.
    boost::mt19937 random_source;
    // Internal helpers
    vector<boost::dynamic_bitset<>*> convert_patterns(vector<vector<bool>> patterns);
    void validate_parameters(vector< vector<bool> > patterns, int bits, int store, int blocks, int tests);
    bool is_true_positive(string item);
  public:
    SerialFramework();
    SerialFramework(string path);
    double test_no_path(vector< vector<bool> > patterns, int bits, int store, int blocks, int tests);
    double test(vector< vector<bool> > patterns, int bits, int store, int blocks, int tests);
};
