#ifndef FILTER_FRAME
#define FILTER_FRAME
#endif

#include <vector>
#include "patternbloom.h"
#include <future>

using namespace std;

class SerialFramework{
  private:
    vector<int> source;
    vector<boost::dynamic_bitset<>*> convert_patterns(vector<vector<bool>> patterns);
  public:
    SerialFramework();
    SerialFramework(string path);
    double test(vector< vector<bool> > patterns, int bits, int store, int blocks, int tests);
};
