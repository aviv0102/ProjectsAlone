/*aviv shisman 206558157 01
rome sharon 209296235 01*/

#ifndef ASS1_CELL_H
#define ASS1_CELL_H


class Cell {
public:
    Cell();

    Cell(char);
    char symbol;
    char opposite();
    int isEmpty();
};


#endif //ASS1_CELL_H
