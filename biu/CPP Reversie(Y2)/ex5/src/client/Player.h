/*aviv shisman 206558157
 * interface player
 * every player has the oneMove function the makes one move
 * symbol that represent him
 */

#ifndef ASS1_PLAYER_H
#define ASS1_PLAYER_H


#include "Point.h"

class Player {
public:
    virtual Point* oneMove(Point**,int) const=0;
    virtual char getSymbol() const=0;
    Player(){};

};


#endif //ASS1_PLAYER_H
