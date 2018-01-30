#ifndef P_BLOOM_H
#define P_BLOOM_H
#endif

#include <bitset>
#include <vector>
#include <iostream>

using namespace std;
const int m = 20; // Cache-line size.

class PatternBF {
  private:
    vector< bitset<m> > blocks_v;
    vector< bitset<m> > patterns_v;
  public:
    PatternBF(int patterns, int items, int blocks);
    void add(string obj);
    bool test(string obj);
    // Function which stores p random patterns in the filter.
    void store_patterns(int p);
};
