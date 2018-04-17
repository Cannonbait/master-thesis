#include "abstract_filter.h"
#include <chrono>
#include <math.h>

/*
 * Checks if the supplied item is contained in the filter.
 * @param item: the item to check for membership
 * @requires: the type T of the item must be hashable.
 */
template <class T> bool AbstractFilter::elem(T item) {
  unsigned long value = hash<T>()(item);
  unsigned int block = value % blocks.size();
  boost::dynamic_bitset<> pattern = generate_pattern(value);
  return ((boost::dynamic_bitset<>(*blocks[block]).flip()) & pattern).none();
}

/*
 * Inserts an item into the filter.
 * @param item: the item to be inserted.
 * @requires: the type T of the item must be hashable.
 */
template <class T> void AbstractFilter::insert(T item) {
  unsigned long value = hash<T>()(item);
  unsigned int block = value % blocks.size();
  boost::dynamic_bitset<> pattern = generate_pattern(value);
  *blocks[block] = (*blocks[block]) | pattern;
}

/*
 * Tries a randomly generated pattern against the filter.
 */
bool AbstractFilter::try_random() {
  srand(std::chrono::system_clock::now().time_since_epoch().count());
  boost::dynamic_bitset<> pattern = generate_pattern(rand());
  unsigned int block = rand() % blocks.size();
  return ((boost::dynamic_bitset<>(*blocks[block]).flip()) & pattern).none();
}

/*
 * Adds a randomly constructed pattern to the filter.
 */
void AbstractFilter::add_random() {
  srand(std::chrono::system_clock::now().time_since_epoch().count());
  boost::dynamic_bitset<> pattern = generate_pattern(rand());
  unsigned int block = rand() % blocks.size();
  *blocks[block] = (*blocks[block]) | pattern;
}

/*
 * Returns the size of the filter.
 */
unsigned int AbstractFilter::size() {
  return (blocks[0]->size())*blocks.size();
}
