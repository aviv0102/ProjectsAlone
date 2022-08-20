/*aviv shisman 206558157 01
rome sharon 209296235 01*/
#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "../AIPlayer.h"

TEST(AIPlayerT__Test,Init){
    CellManger* man=new CellManger(8);
    AIPlayer player('x',man);
    ASSERT_EQ('x',player.getSymbol());
    ASSERT_EQ(man,player.getC());
    EXPECT_EQ(player.getSymbol(),'x');

    delete(man);

}

TEST(AIPlayerT__Test,OneMoveFunc){
    CellManger* c=new CellManger(8);
    c->setWhite(4,4);
    c->setWhite(5,5);
    c->setBlack(4,5);
    c->setBlack(5,4);
    AIPlayer ai('o',c);
    c->setBlack(3,4);
    Point** points=new Point*[3];
    points[0]=new Point(3,3);
    points[1]=new Point(3,5);
    points[2]=new Point(5,3);
    Point* testPoint=ai.oneMove(points,3);
    EXPECT_TRUE((testPoint->getX()==3 || testPoint->getX()==5) && testPoint->getY()==3);

}