//aviv shisman 206558157
//explained in  the cpp file

#ifndef ASS1_HUMANPLAYER_H
#define ASS1_HUMANPLAYER_H
#include "Player.h"

class HumanPlayer: public Player {
public:
    Point* oneMove(Point**,int) const;
    HumanPlayer(char);
    char getSymbol() const;
private:
    char symbol;
};


#endif //ASS1_HUMANPLAYER_H
