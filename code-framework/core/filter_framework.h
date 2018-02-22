#ifndef FILTER_FRAME
#define FILTER_FRAME
#endif

#include <vector>
#include "patternbloom.h"
#include <future>

using namespace std;

class FilterFramework {
  public:
    FilterFramework(int bits, int patterns, int items, int blocks);
    FilterFramework();
    void add_items(int items);
    void add_random(double level_prob, int k);
    void add_items_from_path(int items, string path);
    void replace_patterns(vector< vector<bool> > patterns, int items, int blocks);
    double test_framework(int tests);
    double test_infinite_patterns(int tests, double level_prob);
    double test_framework_from_path(string path);
    void clear_filter();
  private:
    int m; // Number of Bits
    int n; // Number of patterns
    int b; // Number of blocks
    int d; // Number of stored items
    vector<PatternBF> filters;
};
