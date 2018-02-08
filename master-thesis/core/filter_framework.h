#ifndef FILTER_FRAME
#define FILTER_FRAME
#endif

#include <vector>
#include "worker.h"
using namespace std;

class FilterFramework {
  public:
    FilterFramework(int bits, int patterns, int items, int blocks);
    FilterFramework();
    void add_item();
    double test_framework(int tests);
  private:
    int m;
    int n;
    int b;
    int d;
    vector<Worker> workers;
};
