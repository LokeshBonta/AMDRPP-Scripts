// whattotest.cpp
#include <math.h>
#include<algorithm>
 
double squareRoot(const double a) {
    double b = sqrt(a);
    if(b != b) { // nan check
        return -1.0;
    }else{
        return sqrt(a);
    }
}

template <typename T>
T min( T in1, T in2)
{
    return std::min(in1, in2);
}

template <typename T>
T my_min( T in1, T in2)
{
    if(in1 < in2) return in1;
    else return in2;
}
