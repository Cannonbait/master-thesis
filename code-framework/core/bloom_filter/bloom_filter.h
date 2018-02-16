#include <boost/dynamic_bitset.hpp>
#include <string>

using namespace std;

class BloomFilter {
  public:
    bool test();
    bool test(string s);
    void add();
    void add(string s);
    BloomFilter(int m, int k, unsigned int seed);
    BloomFilter(int m, int k);
    static int calculate_k(int m, int d);
    void print();
  private:
    boost::dynamic_bitset<> bits;
    int k;
    bool test_help(int val);
    void add_help(int val);
    int primes[7] = { 3, 7, 11, 13, 17, 19, 37 };
    unsigned int seed;
};
