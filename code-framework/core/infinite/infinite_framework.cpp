#include "infinite_framework.h"
#include <iostream>
#include <fstream>
#include <thread>
#include <chrono>
#include <boost/algorithm/string.hpp>
#include <gmp.h>
#include <algorithm>
#include <boost/random.hpp>
#include <random>
#include <stdexcept>
#include <unordered_map>
#include <math.h>

using namespace std;

InfiniteFramework::InfiniteFramework() {
	random_source = boost::mt19937(std::chrono::system_clock::now().time_since_epoch().count());  
}


double InfiniteFramework::test(int store, int blocks, int tests, int bits, double level) {
  double k;
  double prob = modf(level, &k);
  boost::random::uniform_real_distribution<> prob_dist(0,1);
  //Create pattern
  InfiniteBF bf(blocks, bits);
  for (int i = 0; i < store; i++)
  {
    double rand = prob_dist(random_source);
    if (rand < prob){
      bf.add(k+1);
    } 
    else {
      bf.add(k);
    }
  }
  int positives = 0;
  for (int i = 0; i < tests; i++)
  {
    bool result;
    if (prob_dist(random_source) < prob){
      result = bf.test(k+1);
    } 
    else {
      result = bf.test(k);
    }

    if (result == true){
      positives++;
    }
  }
  
  return (double)positives/(double)tests;
  
}

int main(int argc, char const *argv[])
{
  InfiniteFramework infF = InfiniteFramework();
  infF.test(1, 1, 10, 10, 1);
  return 0;
}