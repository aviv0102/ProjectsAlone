/* aviv shisman and rom sharon
 * join game header:
 */

#ifndef SERVER_JOINGAME_H
#define SERVER_JOINGAME_H


#include <map>
#include "Command.h"

class JoinGame: public Command {
public:
    JoinGame();
    int execute(vector<char *>* args,map<string,GameRoom*>*, int);
};


#endif //SERVER_JOINGAME_H
