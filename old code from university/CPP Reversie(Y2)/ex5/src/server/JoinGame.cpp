/*aviv shisman and rom sharon
 * the join game cpp:
 */

#include <unistd.h>
#include "JoinGame.h"

JoinGame::JoinGame() {}

int JoinGame::execute(vector<char *> *args, map<string, GameRoom *> *gameMap, int socket) {
    char buffer[2];
    int ok = 1;
    int wrong = 0;
    string str = getStringFromVector(args);
    //the game is exist
    if (gameMap->find(str) != gameMap->end() && !(*gameMap)[str]->fullGame()) {
        cout << "joining the game: " << str << endl;
        write(socket, &ok, sizeof(ok));
        read(socket, buffer, sizeof(buffer));
        //adding second player to the gameRoom
        (*gameMap)[str]->setSecondPlayer(socket);
        //starting a game!!
        (*gameMap)[str]->handleTowClients();
        (*gameMap).erase(str);
    } else {
        //if room is full
        write(socket, &wrong, sizeof(wrong));
        read(socket, buffer, sizeof(buffer));
    }
    return 0;
}