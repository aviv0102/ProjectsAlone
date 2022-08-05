/*aviv shisman 206558157
 * ReverseRule is the first rule we got
 * it means the we can put a piece only in special spots
 * spots that will lead to reverse of other pieces
 * explanation on the functions is in the cpp file
 */

#ifndef ASS1_REVERSERULE_H
#define ASS1_REVERSERULE_H


#include "Rule.h"
#include "GameShower.h"
#include "Cell.h"

class ReverseRule: public Rule {
public:
    ReverseRule();
    void apply(Cell**,int,int,char) const;
    void applyUp(Cell**,int,int,char) const;
    void applyRight(Cell**,int,int,char) const;
    void applyLeft(Cell**,int,int,char) const;
    void applyDown(Cell**,int,int,char) const;
    void applyUpRight(Cell**,int,int,char) const;
    void applyUpLeft(Cell**,int,int,char) const;
    void applyDownLeft(Cell**,int,int,char) const;
    void applyDownRight(Cell**,int,int,char) const;

    int check(Cell**,int,int,char) const;
    int right(Cell**,int,int,char) const;
    int left(Cell**,int,int,char) const;
    int up(Cell**,int,int,char) const;
    int down(Cell**,int,int,char) const;
    int upRight(Cell**,int,int,char) const;
    int upLeft(Cell**,int,int,char) const;
    int downRight(Cell**,int,int,char) const;
    int downLeft(Cell**,int,int,char) const;

};


#endif //ASS1_REVERSERULE_H
