/*aviv shisman and rom sharon
 *startGame header:
 */

#ifndef SERVER_STARTGAME_H
#define SERVER_STARTGAME_H

#include "Command.h"

class StartGame: public Command {
public:
    StartGame();
    int execute(vector<char *>* args,map<string,GameRoom*>*, int);
};

#endif //SERVER_STARTGAME_H

