#include <string>
#include <vector>
#include "bloom_filter.h"

using namespace std;

class BlockedFilter {
  public:
    bool test_item(string s);
    bool test();
    void add_item(string s);
    void add();
    BlockedFilter(int m, int b, int k, size_t seed);
    BlockedFilter(int m, int b, int k);
    BlockedFilter();
    void display();
  private:
    vector<BloomFilter> filters;
    size_t seed;
};
