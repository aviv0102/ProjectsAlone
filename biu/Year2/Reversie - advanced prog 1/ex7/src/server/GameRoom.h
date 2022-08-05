/*aviv shisman and rom sharon
 * the gameRoom header:
 *
 */

#ifndef SERVER_GAMEROOM_H
#define SERVER_GAMEROOM_H

using namespace std;

class GameRoom {
public:
    GameRoom(int firstPlayer);
    void setSecondPlayer(int secondPlayer);
    void handleTowClients();
    bool fullGame();
    void closeRoom();
private:
    int firstPlayer ;
    int secondPlayer;
    int closeGame;

};


#endif //SERVER_GAMEROOM_H
