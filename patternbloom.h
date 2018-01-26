#ifndef P_BLOOM_H
#define P_BLOOM_H
#endif

#include <bitset>
#include <vector>
#include <iostream>

using namespace std;

class PatternBF {
  private:
    bitset<8> m;
  public:
    PatternBF(int m, int n);
    //PatternBF(bitset<8> pattern); // TODO
    void add(bitset<8> pattern); //object
    bool test(bitset<8> pattern); //object
};
