#include "filter_framework.h"
#include <iostream>
#include <fstream>
#include <thread>
#include <chrono>
#include <boost/algorithm/string.hpp>
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

void FilterFramework::clear_filter() {
  filters.clear();
  d = 1;
  unsigned concurentThreadsSupported = thread::hardware_concurrency()-1;
  for(size_t i = 0; i < concurentThreadsSupported; i++) {
    filters.push_back(PatternBF(n,d,b,m));
  }
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
    int val = f.get();
    total_false_pos += val;
  }
  return (double)total_false_pos/(double)(concurentThreadsSupported*tests_per_thread);
}

double FilterFramework::test_framework_from_path(string path){
  ifstream data_file("../data_preparation/" + path);
  data_file.ignore(50, '\n'); //Ignore specification data
  string line;
  int positives = 0;
  int totalLines = 0;
  while (getline(data_file, line)){
    vector<string> results;
    boost::split(results, line, [](char c){return c == ',';});
    if (filters[stoi(results[0])].test(stoi(results[1]), stoi(results[2]))){
      positives++;
      cout << positives << endl;
    }
    cout << totalLines << endl;
    totalLines++;
  }
  return (double)positives/(double)totalLines;
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
  d += items;
}

/*
 * Adds a single item to each filter currently active in the framework.
 * This is represented by adding a random pattern into a random block.
 *
 */
void FilterFramework::add_items_from_path(int items, string path) {
  ifstream data_file("../data_preparation/" + path);

  // new lines will be skipped unless we stop it from happening:
  data_file.unsetf(std::ios_base::skipws);

  // count the newlines with an algorithm specialized for counting:
  unsigned line_count = std::count(
    std::istreambuf_iterator<char>(data_file),
    std::istreambuf_iterator<char>(),
    '\n');
  std::cout << "Lines: " << line_count << "\n";
  boost::mt19937 random_source(std::chrono::system_clock::now().time_since_epoch().count());
  boost::random::uniform_int_distribution<> pattern_dist(1, line_count-1);
  vector<int> indexes;


  while (indexes.size() < items*filters.size()){
    int index = pattern_dist(random_source);
    if (find(indexes.begin(), indexes.end(), index) == indexes.end()){
      indexes.push_back(index);
    }
  }
  sort(indexes.begin(), indexes.end());

  data_file.seekg(0, ios::beg);
  data_file.setf(std::ios_base::skipws);
  int line = 0;
  for(int index=0; index < indexes.size(); index++){
    while(indexes[index] != line){
      data_file.ignore(50, '\n');
      line++;
    }
    string buffer;
    getline(data_file, buffer);
    vector<string> results;
    boost::split(results, buffer, [](char c){return c == ',';});
    filters[stoi(results[0])].add_indexes(stoi(results[1]), stoi(results[2]));
  }
  d += items;
  data_file.close();
}

void try_genrated(int items, double level_prob, int k, promise<int> && p, PatternBF &filter) {
  int false_positives = 0;
  for(int j = 0; j < items; j++) {
    if(filter.test_random_pattern(level_prob, k)) {
      false_positives++;
      cout << "A false positive occured" << "\n";
    }
  }
  p.set_value(false_positives);
}

/*
 * Adds a randomly constructed pattern to the filter.
 * @param: level_prob: the probability of a pattern with level k+1
 * @param: expected_items: the expected amount of items to be added.
 *
 */
void FilterFramework::add_random(double level_prob, int k) {
  for(size_t i = 0; i < filters.size(); i++) {
    filters[i].add_random(level_prob, k);
  }
  d++;
}

/*
 * Performs a number of tests in parallel for generated patterns.
 * @param: tests: the number of tests to be performed.
 * @param: level_prob: the probability that a pattern is of level k+1.
 *
 */
double FilterFramework::test_infinite_patterns(int tests, double level_prob) {
  vector<thread> ts;
  unsigned concurentThreadsSupported = thread::hardware_concurrency()-1;
  int tests_per_thread = tests/concurentThreadsSupported;
  vector< future<int> > futures;
  for(size_t i = 0; i < filters.size(); i++) {
    promise<int> p;
    futures.push_back(p.get_future());
    int k = round((b*m/d)*log(2));
    ts.push_back(thread(try_genrated, level_prob, k, tests_per_thread, move(p), ref(filters[i])));
  }

  join_all(ts);

  int total_false_pos = 0;
  for (future<int>& f : futures) {
    int val = f.get();
    total_false_pos += val;
  }
  filters[0].print();
  return (double)total_false_pos/(double)(concurentThreadsSupported*tests_per_thread);
}

int main() {
  int d = 4;
  double p = 0.3;
  FilterFramework f = FilterFramework(20,1,d,1);
  f.clear_filter();
  for(int i = 0; i < d; i++) {
    f.add_random(p,d);
  }
  cout << f.test_infinite_patterns(3, p) << "\n";
  return 0;
}
