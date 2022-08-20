/*aviv shisman and rom sharon
 * command maneger header:
 */

#ifndef SERVER_COMMANDMANEGER_H
#define SERVER_COMMANDMANEGER_H

#include <map>
#include "Command.h"
#include "GameMap.h"

class CommandsManager {
public:
    CommandsManager();
    ~CommandsManager();
    int executeCommand(char* command, vector <char*>*, int);
private:
    map<string, Command*> commandsMap;
    GameMap* gameMap;
};

#endif //SERVER_COMMANDMANEGER_H
