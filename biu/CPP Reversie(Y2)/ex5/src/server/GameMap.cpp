/* aviv shisman and rom sharon
 * gameMap cpp: (a Singelton)
 */

#include "GameMap.h"

GameMap *GameMap::instance = 0;
//constructor
GameMap *GameMap::getInstance() {
    if (!instance) {
        instance = new GameMap();
        return instance;
    } else {
        return instance;
    }
}

map<string, GameRoom *> *GameMap::getGames() {
    return games;
}
//map of game rooms
GameMap::GameMap() {
    games = new map<string, GameRoom *>();
}
//close games
void GameMap::closeGames() {
    map<string, GameRoom *>::iterator it;
    for (it = games->begin(); it != games->end(); it++) {
        it->second->closeRoom();
    }
}