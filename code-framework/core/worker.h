#include "patternbloom.h"
#include <mutex>

using namespace std;

class Worker {
  public:
    int try_items(int items);
    void add_item();
    Worker(int patterns, int items, int blocks);
    int collect_fp();
  private:
    PatternBF filter;
    static mutex mx;
    static int fp;
};
