/*aviv shisman 206558157 01
rome sharon 209296235 01*/
#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "../HumanPlayer.h"


TEST(HumanPlayerTest,testSymbol){
    HumanPlayer p1('x');
    HumanPlayer p2('o');
    ASSERT_EQ('x',p1.getSymbol());
    ASSERT_EQ('o',p2.getSymbol());
    EXPECT_FALSE(p1.getSymbol()=='o');
    EXPECT_FALSE(p1.getSymbol()!='x');

}
TEST(HumanPlayert__Test,testOneMove){
    Point** points=new Point*[1];
    points[0]=new Point(1,1);
    HumanPlayer p1('x');
    Point* p2=p1.oneMove(points,1);
    EXPECT_EQ(p2->getY(),points[0]->getY());
    EXPECT_EQ(p2->getX(),points[0]->getX());
    delete(points[0]);
    delete(points);
}