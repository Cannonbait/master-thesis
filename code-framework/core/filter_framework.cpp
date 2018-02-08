#include "filter_framework.h"
#include <thread>

using namespace std;

void do_join(thread& t) {
    t.join();
}

void join_all(vector<thread>& v) {
    for_each(v.begin(),v.end(),do_join);
}

FilterFramework::FilterFramework() {}

FilterFramework::FilterFramework(int bits, int patterns, int items, int blocks) : m(bits), n(patterns), d(items), b(blocks) {
  unsigned concurentThreadsSupported = thread::hardware_concurrency()-1;
  for(int i = 0; i < concurentThreadsSupported; i++) {
    workers.push_back(Worker(patterns,items,blocks));
  }
}

double FilterFramework::test_framework(int tests) {
  vector<thread> ts;
  unsigned concurentThreadsSupported = thread::hardware_concurrency()-1;
  int tests_per_thread = tests/concurentThreadsSupported;
  for(int i = 0; i < workers.size(); i++) {
    ts.push_back(thread(&Worker::try_items, workers[i], tests_per_thread));
  }
  join_all(ts);
  return workers[0].collect_fp();
}

void FilterFramework::add_item() {
  for(int i = 0; i < workers.size(); i++) {
    workers[i].add_item();
  }
}
