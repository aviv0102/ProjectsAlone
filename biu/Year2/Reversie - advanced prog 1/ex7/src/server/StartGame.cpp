// aviv shisman and rom sharon .
#include <map>
#include <unistd.h>
#include "StartGame.h"
StartGame::StartGame(){

}

int StartGame::execute(vector<char *>* args, map<string,GameRoom*>* gameMap,int socket) {
    char buffer[2];
    int ok = 1;
    int wrong = 0;
    string str = getStringFromVector(args);
    //game isn't exist
    if ((*gameMap).find(str) == (*gameMap).end()) {
        write(socket, &ok ,sizeof(ok));
        read(socket, buffer, sizeof(buffer));
        (*gameMap)[str] = new GameRoom(socket);
        return 1;
    }
    else {
        //game exist-> wrong command
        write(socket, &wrong, sizeof(wrong));
        read(socket, buffer, sizeof(buffer));
    }
    return 0;
}