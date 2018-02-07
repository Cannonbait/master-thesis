#include "../patternbloom.h"
#include <mutex>

using namespace std;

class Worker {
  public:
    void try_items(int items, mutex &mtx);
    Worker(int patterns, int items, int blocks);
  private:
    PatternBF filter;
};
