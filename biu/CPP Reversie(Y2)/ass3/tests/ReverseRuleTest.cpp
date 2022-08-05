/*aviv shisman 206558157 01
rome sharon 209296235 01*/

#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "../ReverseRule.h"
#include "../CellManger.h"

TEST(CellMangerTest, applyLeft){
    ReverseRule reverseRule = ReverseRule();
    CellManger cm(4);
    cm.setBlack(2, 2);
    cm.setBlack(3, 3);
    cm.setWhite(2, 3);
    cm.setWhite(3, 2);
    cm.setBlack(4, 2);
    reverseRule.applyLeft(cm.getArr(), 4, 2, 'x');
    EXPECT_EQ(cm.getCell(3, 2).symbol, 'x');
}

TEST(CellMangerTest, applyRight){
    ReverseRule reverseRule = ReverseRule();
    CellManger cm(4);
    cm.setBlack(2, 2);
    cm.setBlack(3, 3);
    cm.setWhite(2, 3);
    cm.setWhite(3, 2);
    cm.setBlack(4, 2);
    reverseRule.applyRight(cm.getArr(), 2, 2, 'x');
    EXPECT_EQ(cm.getCell(3, 2).symbol, 'x');
}

TEST(CellMangerTest, applyDown){
    ReverseRule reverseRule = ReverseRule();
    CellManger cm(4);
    cm.setBlack(2, 2);
    cm.setBlack(3, 3);
    cm.setWhite(2, 3);
    cm.setWhite(3, 2);
    cm.setWhite(2, 1);
    reverseRule.applyDown(cm.getArr(), 2, 1, 'o');
    EXPECT_EQ(cm.getCell(2, 2).symbol, 'o');
}

TEST(CellMangerTest, applyUp){
    ReverseRule reverseRule = ReverseRule();
    CellManger cm(4);
    cm.setBlack(2, 2);
    cm.setBlack(3, 3);
    cm.setWhite(2, 3);
    cm.setWhite(3, 2);
    cm.setWhite(2, 1);
    reverseRule.applyUp(cm.getArr(), 2, 3, 'o');
    EXPECT_EQ(cm.getCell(2, 2).symbol, 'o');
}

TEST(CellMangerTest, applyDownRight){
    ReverseRule reverseRule = ReverseRule();
    CellManger cm(4);
    cm.setBlack(2, 2);
    cm.setBlack(3, 2);
    cm.setWhite(3, 3);
    cm.setWhite(2, 3);
    cm.setWhite(1, 1);
    reverseRule.applyDownRight(cm.getArr(), 1, 1, 'o');
    EXPECT_EQ(cm.getCell(2, 2).symbol, 'o');
}

TEST(CellMangerTest, applyUpLeft){
    ReverseRule reverseRule = ReverseRule();
    CellManger cm(4);
    cm.setBlack(2, 2);
    cm.setBlack(3, 2);
    cm.setWhite(3, 3);
    cm.setWhite(2, 3);
    cm.setBlack(4, 4);
    reverseRule.applyUpLeft(cm.getArr(),4, 4, 'x');
    EXPECT_EQ(cm.getCell(3, 3).symbol, 'x');
}

TEST(CellMangerTest, applyUpRight){
    ReverseRule reverseRule = ReverseRule();
    CellManger cm(4);
    cm.setBlack(2, 2);
    cm.setBlack(3, 2);
    cm.setWhite(3, 3);
    cm.setWhite(2, 3);
    cm.setBlack(1, 4);
    reverseRule.applyUpRight(cm.getArr(), 1, 4, 'x');
    EXPECT_EQ(cm.getCell(2, 3).symbol, 'x');
}

TEST(CellMangerTest, applyDownLeft){
    ReverseRule reverseRule = ReverseRule();
    CellManger cm(4);
    cm.setBlack(2, 2);
    cm.setBlack(3, 2);
    cm.setWhite(3, 3);
    cm.setWhite(2, 3);
    cm.setBlack(1, 4);
    reverseRule.applyDownLeft(cm.getArr(), 3, 2, 'x');
    EXPECT_EQ(cm.getCell(2, 3).symbol, 'x');
}