/*aviv shisman and rom sharon
 * list games header:
 */

#ifndef SERVER_LISTGAMES_H
#define SERVER_LISTGAMES_H


#include <map>
#include "Command.h"

class ListGames: public Command {
public:
    ListGames();
    int execute(vector<char *>* args,map<string,GameRoom*>*, int);
};


#endif //SERVER_LISTGAMES_H
