#include <vector>
#include <boost/dynamic_bitset.hpp>

using namespace std;

class AbstractFilter {
  public:
    /* Bloom filter essentials */
    template <class T> bool elem(T item);
    template <class T> void insert(T item);
    unsigned int size();
    /* Experimental neccessities */
    bool try_random();
    void add_random();
  protected:
    virtual boost::dynamic_bitset<> generate_pattern(unsigned long seed_value) = 0;
    vector<boost::dynamic_bitset<>*> blocks;
};
