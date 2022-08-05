//
// Created by rom on 25/11/17.
//
/*aviv shisman 206558157 01
rome sharon 209296235 01*/
#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "../CellManger.h"


TEST(CellMangerTest, nameOfTest4){
    CellManger cellManger(4);
    int size = cellManger.getSize();
    EXPECT_EQ(4, size);
}

TEST(CellMangerTest, nameOfTest5){
    CellManger cellManger(4);
    cellManger.setCell(1, 2, 'o');
    char symbol = cellManger.getCell(1, 2).symbol;
    EXPECT_EQ('o', symbol);
}

TEST(CellMangerTest, nameOfTest6){
    CellManger cellManger(4);
    cellManger.setBlack(0,0);
    char symbol = cellManger.getCell(0, 0).symbol;
    EXPECT_EQ('x', symbol);
}

TEST(CellMangerTest, nameOfTest7){
    CellManger cellManger(4);
    cellManger.setWhite(0,0);
    char symbol = cellManger.getCell(0, 0).symbol;
    EXPECT_EQ('o', symbol);
}

bool checkIfSimilar(CellManger cellManger, CellManger cm) {
    for(int i = 0; i < cellManger.getSize(); i++) {
        for(int j = 0; j < cellManger.getSize(); j++) {
            if(cellManger.getCell(i, j).symbol != cm.getCell(i, j).symbol) {
                return false;
            }
        }
    }
    return true;
}


TEST(CellMangerTest, nameOfTest8){

    CellManger* cellManger = new CellManger(4);
    cellManger->setWhite(0,0);
    cellManger->setWhite(1,0);
    cellManger->setBlack(2,0);
    cellManger->setBlack(3,0);
    cellManger->setBlack(0,1);
    CellManger* temp = new CellManger(4);
    temp->setArr(cellManger->getArr());
    EXPECT_EQ(checkIfSimilar(*cellManger, *temp), true);
}


