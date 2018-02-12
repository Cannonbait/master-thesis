#include "filter_framework.h"
#include <thread>

using namespace std;

// Helper for multithreading
void do_join(thread& t) {
    t.join();
}

// Helper for multithreading
void join_all(vector<thread>& v) {
    for_each(v.begin(),v.end(),do_join);
}

void try_items(int items, promise<int> && p, PatternBF &filter) {
  int false_positives = 0;
  for(int j = 0; j < items; j++) {
    if(filter.test_rng()) {
      false_positives++;
    }
  }
  p.set_value(false_positives);
}

FilterFramework::FilterFramework() {}

/*
 * Default constructor. Constructs a number of patterns equal to the
 * number of avaliable cores for parallelism. Patterns are initialized
 * to a default setting (uniform k over each vector).
 */
FilterFramework::FilterFramework(int bits, int patterns, int items, int blocks) : m(bits), n(patterns), d(items), b(blocks) {
  unsigned concurentThreadsSupported = thread::hardware_concurrency()-1;
  for(size_t i = 0; i < concurentThreadsSupported; i++) {
    filters.push_back(PatternBF(patterns,items,blocks,bits));
    filters[i].add_many(items);
  }
}

/*
 * Tests the current pattern design. Runs the tests in parallel according
 * to the maximum avaliable cores. Returns the FPR.
 *
 */
double FilterFramework::test_framework(int tests) {
  vector<thread> ts;
  unsigned concurentThreadsSupported = thread::hardware_concurrency()-1;
  int tests_per_thread = tests/concurentThreadsSupported;
  vector< future<int> > futures;
  for(size_t i = 0; i < filters.size(); i++) {
    promise<int> p;
    futures.push_back(p.get_future());
    ts.push_back(thread(try_items, tests_per_thread, move(p), ref(filters[i])));
  }

  join_all(ts);

  int total_false_pos = 0;
   for (future<int>& f : futures) {
     total_false_pos += f.get();
   }
  return (double)total_false_pos/(double)(concurentThreadsSupported*tests_per_thread);
}

/*
 * Replaces the patterns in the framework. Resets the blocks and hence
 * a new number of items needs to be added.
 *
 */
void FilterFramework::replace_patterns(vector< vector<bool> > patterns, int items, int blocks) {
  vector<boost::dynamic_bitset<>*> arg_patterns(patterns.size());
  vector<boost::dynamic_bitset<> > patt(patterns.size());
  for(size_t i = 0; i < patterns.size(); i++) {
    boost::dynamic_bitset<> bits;
    bits.clear();
    patt.push_back(bits);
    for(size_t j = 0; j < patterns[0].size(); j++) {
      patt[i].push_back(patterns[i][j]);
    }
    arg_patterns[i] = &patt[i];
  }
  for(size_t i = 0; i < filters.size(); i++) {
    filters[i] = PatternBF(arg_patterns, blocks);
    filters[i].add_many(items);
  }
}

/*
 * Adds a single item to each filter currently active in the framework.
 * This is represented by adding a random pattern into a random block.
 *
 */
void FilterFramework::add_items(int items) {
  for(size_t i = 0; i < filters.size(); i++) {
    filters[i].add_many(items);
  }
}
