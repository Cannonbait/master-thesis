#include "patternbloom.h"
#include <mutex>
#include <future>

using namespace std;

class Worker {
  public:
    void try_items(int items, promise<int> && p);
    void add_item();
    Worker(int bits, int patterns, int items, int blocks);
  private:
    PatternBF filter;
};
