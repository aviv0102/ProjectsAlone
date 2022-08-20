/*aviv shisman 206558157 01
rome sharon 209296235 01*/
#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "../Point.h"

TEST(PointTest,Negative){
    Point p(-5,-5);
    EXPECT_EQ(-5,p.getX());
    EXPECT_EQ(p.getY(),-5);

}
TEST(PointTest,Zero){
    Point k(0,0);
    EXPECT_EQ(0,k.getX());
    EXPECT_EQ(k.getY(),0);
}
TEST(PointTest,NoEqual){
    Point k(1,2);
    EXPECT_FALSE(0==k.getX());
    EXPECT_FALSE(k.getY()==0);
}