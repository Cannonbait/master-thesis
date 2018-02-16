#include <string>
#include <vector>
#include "bloom_filter.h"

using namespace std;

class BlockedFilter {
  public:
    bool test(string s);
    bool test();
    void add(string s);
    void add();
    BlockedFilter(int m, int b, int k, size_t seed);
    BlockedFilter(int m, int b, int k);
    void print();
  private:
    vector<BloomFilter> filters;
    size_t seed;
};
