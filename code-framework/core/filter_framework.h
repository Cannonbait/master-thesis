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
    void infinite_framework(int bits, int blocks);
    void infinite_framework_pop(int bits, int blocks, int items, double level_prob, int k);
    FilterFramework();
    void add_items(int items);
    void add_random(double level_prob, int k);
    void add_items_from_path(int items, string path);
    void replace_patterns(vector< vector<bool> > patterns, int blocks);
    double test_framework(int tests);
    double test_infinite_patterns(int tests, double level_prob, int k);
    double test_framework_from_path(string path);
  private:
    int m; // Number of Bits
    int n; // Number of patterns
    int b; // Number of blocks
    int d; // Number of stored items
    vector<PatternBF> filters;
    vector<string> entries;
};
