#include "patternbloom.h"
#include <future>

using namespace std;

class Worker {
  public:
    void try_items(int items, promise<int> && p);
    Worker(int patterns, int items, int blocks);
  private:
    PatternBF filter;
};
