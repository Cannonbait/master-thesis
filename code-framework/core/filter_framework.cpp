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
    workers.push_back(Worker(patterns,items,blocks, bits));
  }
}

double FilterFramework::test_framework(int tests) {
  vector<thread> ts;
  unsigned concurentThreadsSupported = thread::hardware_concurrency()-1;
  int tests_per_thread = tests/concurentThreadsSupported;
  vector< future<int> > futures;
  for(int i = 0; i < workers.size(); i++) {
    promise<int> p;
    futures.push_back(p.get_future());
    ts.push_back(thread(&Worker::try_items, workers[i], tests_per_thread, move(p)));
  }

  join_all(ts);

  int total_false_pos = 0;
   for (future<int>& f : futures) {
     total_false_pos += f.get();
   }
  return ((double)total_false_pos)/((double)(concurentThreadsSupported*tests_per_thread));
}

void FilterFramework::add_item() {
  for(int i = 0; i < workers.size(); i++) {
    workers[i].add_item();
  }
}
