#include "patternbloom.h"
#include <iostream>
#include <tr1/functional>
#include <string>
#include <math.h>
#include <cstdlib>
#include <bitset>

using namespace std;

/*
  Shuffles the bitset with regard to the number of 1's which
  are assumed to be at the start of the vector.
*/
void shuffle_bits(bitset<m> &bits, int k, int seed) {
  for(int i = 0; i < k; i++) {
      srand(time(0)*1000*(i+10)*(seed+1));
      int j = rand() % (m-i) + i;
      bool temp = bits[i];
      bits[i] = bits[j];
      bits[j] = temp;
  }
}

/*
  For adding strings to the filter. Implemented as
  for cache- and hash optimality. The two hash functions
  are not neccessarily independent.
*/
void PatternBF::add(string obj) {
  size_t val = tr1::hash<string>()(obj);
  val = val % blocks_v.size();
  bitset<m> *block = &blocks_v[val];
  val = tr1::hash<string>()(obj);
  val = (val*13) % patterns_v.size();
  bitset<m> *pattern = &patterns_v[val];
  (*block) |= (*pattern);
}

/*
  Standard test for strings in the filter.
*/
bool PatternBF::test(string obj) {
  size_t val = tr1::hash<string>()(obj);
  val = val % blocks_v.size();
  bitset<m> *block = &blocks_v[val];
  val = tr1::hash<string>()(obj);
  val = (val*13) % patterns_v.size();
  bitset<m> *pattern = &patterns_v[val];

  for(int i = 0; i < m; i++) {
    if((*pattern)[i] == 1 && (*block)[i] != 1) {
      return false;
    }
  }
  return true;
}

PatternBF::PatternBF(int patterns, int items, int blocks) {
  // Initialize blocks
  blocks_v.reserve(blocks);
  for(int i = 0; i < blocks; i++) {
    bitset<m> b;
    blocks_v.push_back(b);
  }

  // Initialize patterns according to CHE.
  patterns_v.reserve(patterns);
  int k = (m/items)*log(2);
  for(int i = 0; i < patterns; i++) {
    bitset<m> pattern;
    for(int j = 0; j < k; j++) {
      pattern[j] = 1;
    }
    shuffle_bits(pattern, k, i);
    patterns_v.push_back(pattern);
  }
}
