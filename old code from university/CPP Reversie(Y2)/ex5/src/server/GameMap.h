//
// Created by magshimim on 26/12/17.
//


#ifndef SERVER_GAMEMAP_H
#define SERVER_GAMEMAP_H

#include <map>
#include <string>
#include "GameRoom.h"
using namespace std;


class GameMap {
public:
    static GameMap *getInstance();
    map<string,GameRoom*>* getGames();
    void closeGames();
private:
    GameMap();
    static GameMap *instance;
    map<string,GameRoom*>* games;
};


#endif //SERVER_GAMEMAP_H
