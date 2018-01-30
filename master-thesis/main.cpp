#include <iostream>
#include "patternbloom.h"

using namespace std;

int main()
{
    PatternBF * bf = new PatternBF(10, 2, 5);
    (*bf).add("apa");
    (*bf).test_rng();




    (*bf).print();

    return 0;
}
