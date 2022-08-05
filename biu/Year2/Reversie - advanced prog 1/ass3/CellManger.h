/* aviv shisman 206558157 01
 * rome sharon 209296235 01
 * class we use to represent the board different cells and manage them
 * explanation on the methods in the cpp file
 */

#ifndef ASS1_CELLMANGER_H
#define ASS1_CELLMANGER_H


#include "Cell.h"

class CellManger {
public:
    CellManger(int);
    ~CellManger();
    int getSize() const;
    Cell **getArr() const;
    void setBlack(int,int);
    void setWhite(int,int);
    void setArr(Cell** a);
    void setCell(int, int, char);
    int getCount(char);
    Cell getCell(int,int);
private:
    int size;
    Cell** arr;

};


#endif //ASS1_CELLMANGER_H
