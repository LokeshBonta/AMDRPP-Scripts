// tests.cpp
#include "functions.cpp"
#include <gtest/gtest.h>

// All the RPP stuff
// Input buffer will only be one
// GPU output from RPP will be stored in output2 buffer
// CPU output from RPP will be stored in output1 buffer
// Compare Both the Tensors

 
TEST(SquareRootTest, PositiveNos) { 
    ASSERT_EQ(6, squareRoot(36.0));
    ASSERT_EQ(18.0, squareRoot(324.0));
    ASSERT_EQ(25.4, squareRoot(645.16));
    ASSERT_EQ(0, squareRoot(0.0));
}
 
TEST(SquareRootTest, NegativeNos) {
    ASSERT_EQ(-1.0, squareRoot(-15.0));
    ASSERT_EQ(-1.0, squareRoot(-0.2));
}

 TEST(min, IntValues)
 {
     ASSERT_EQ(my_min( 1, 2), min( 1, 2));
     ASSERT_EQ(my_min(7, 5), min(7, 5));
 }

 TEST(min, FloatValues)
 {
     ASSERT_EQ(my_min(1.0, 6.2), min(1.0, 6.2));
     ASSERT_EQ(my_min(7.5, 5.0), min(7.5, 5.0));
 }

int main(int argc, char **argv) {
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
