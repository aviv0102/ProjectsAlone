/*aviv shisman 206558157 01
rome sharon 209296235 01*/
#include "CellManger.h"
/*
 * the constructor using the size to create the cell array
 */
CellManger::CellManger(int s) {
    size=s;
    arr=new Cell*[size+3];
    for(int i = 0; i < size+3; i++) {
        arr[i] = new Cell[size +3]();
        for(int j=0;j<size+3;j++){
            arr[i][j].symbol='a';
        }
    }

}
/*
 * return the size
 */
int CellManger::getSize() const {
    return size;
}
/*
 * setting black piece
 */
void CellManger::setBlack(int x, int y) {
    arr[x][y].symbol='x';
}
/*
 * setting white piece
 */
void CellManger::setWhite(int x, int y) {
    arr[x][y].symbol='o';
}
/*
 * return the array
 */
Cell **CellManger::getArr() const {
    return arr;
}

/*
 * destructor
 */
CellManger::~CellManger() {

    for(int i = 0; i < size+3; i++) {
        delete[]( arr[i]);

    }
    delete [] arr;

}

void CellManger::setArr(Cell** a) {
    for(int i = 0; i < size+3; i++) {
        for(int j=0;j<size+3;j++){
            arr[i][j].symbol= a[i][j].symbol;
        }
    }
}

void CellManger::setCell(int i, int j, char symbol) {
    this->arr[i][j] = symbol;
}

int CellManger::getCount(char symbol) {
    int counter = 0;
    for (int i = 0; i < size+3; ++i) {
        for (int j = 0; j < size+3; ++j) {
            if(arr[i][j].symbol == symbol) {
                counter++;
            }
        }
    }
    return counter;
}
Cell CellManger::getCell(int i,int j){
    return this->arr[i][j];
}