/*aviv shisman 206558157 01
rome sharon 209296235 01*/

#include "Cell.h"
/*
 * constructor that gives the cell a symbol x or o
 */
Cell::Cell(char s) : symbol(s) {}
//option for empty constructor
Cell::Cell() {};

/*
 * checking if the cell is empty
 */
int Cell::isEmpty() {
    if(symbol=='x' || symbol=='o'){
        return 0;
    }
    return 1;
}
/*
 * bringing the opposite value of the symbol in cell
 */
char Cell::opposite() {
    if(symbol=='x'){
        return 'o';
    }
    if(symbol=='o'){
        return 'x';
    }
    return 'a';
}
