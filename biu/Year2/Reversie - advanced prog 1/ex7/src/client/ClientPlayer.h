/*aviv shisman and rom sharon
 * Player of online play
 */

#ifndef ASS1_CLIENTPLAYER_H
#define ASS1_CLIENTPLAYER_H
#include "Player.h"
#include "CellManger.h"
#include "Client.h"
/*
 * comments on the functions in the cpp
 */
class ClientPlayer: public Player {
    public:
        Point* oneMove(Point**,int) const;
        char getSymbol() const;
        ClientPlayer(Client* , char);

    private:
        char symbol;
        Client* client;
};


#endif //ASS1_CLIENTPLAYER_H
