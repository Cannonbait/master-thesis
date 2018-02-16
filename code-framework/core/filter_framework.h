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
    void add_items_from_path(int items, string path);
    void replace_patterns(vector< vector<bool> > patterns, int items, int blocks);
    double test_framework(int tests);
    double test_framework_from_path(string path);
  private:
    int m;
    int n;
    int b;
    int d;
    vector<PatternBF> filters;
};
