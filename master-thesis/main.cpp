#include <iostream>
#include "patternbloom.h"

using namespace std;

int main()
{
    PatternBF * bf = new PatternBF(10, 2, 5);
    (*bf).add("apa");
    (*bf).add("apap");
    (*bf).add("apad");
    (*bf).add("apaf");
    (*bf).add("apaw");
    (*bf).add("apaq");
    (*bf).add("apae");




    (*bf).print();
    cout << (*bf).test("apa") << endl;
    cout << (*bf).test("bba") << endl;

    return 0;
}
