/*aviv shisman and rom sharon
 * getting the list of games:
 */

#include "ListGames.h"
#include <sys/socket.h>
#include <unistd.h>
#include <string.h>

ListGames::ListGames() {}

int ListGames::execute(vector<char *>* args, map<string,GameRoom*>* gameMap,int socket) {
    char buffer[2];
    string full = "(full)";
    string open = "(1 waiting for you)";
    //iterating over the singelton map
    for(map<string,GameRoom*>::iterator it = gameMap->begin(); it != gameMap->end(); ++it) {
        if(it->second->fullGame()) {
            write(socket, (it->first+full).c_str() , strlen((it->first+full).c_str()) + 1);
        } else {
            write(socket, (it->first+open).c_str() , strlen((it->first+open).c_str()) + 1);
        }
        read(socket, buffer, sizeof(buffer));

    }
    //checking that client recived
    write(socket, "$", sizeof("$"));
    read(socket, buffer, sizeof(buffer));
    return 0;
}