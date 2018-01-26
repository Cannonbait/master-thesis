#include "patternbloom.h"
#include <iostream>
#include <tr1/functional>
#include <string>

using namespace std;

void PatternBF::add(bitset<8> pattern) {
  m |= pattern;
  cout << "Pattern: " << m.to_string() << "\n";
}

bool PatternBF::test(bitset<8> pattern) {
  cout << "Pattern: " << m.to_string() << "\n";
}

PatternBF::PatternBF(bitset<8> pattern) {
  m &= pattern;
}

int main() {
  bitset<8> a;
  PatternBF bf = PatternBF(a);
  a.set();
  bf.add(a);
}
