/*aviv shisman and rom sharon
 * the gameRoom cpp:
 * in this class the game will occur
 */

#include <unistd.h>
#include <iostream>
#include "GameRoom.h"
//constructor
GameRoom::GameRoom(int firstPlayer) : firstPlayer(firstPlayer){
    int x=0;
    //send the first player message to wait to the second
    int n = write(firstPlayer, &x, sizeof(x));
    if (n == -1) {
        cout << "Error writing to player2" << endl;
        return;
    }
    secondPlayer=0;
    closeGame=0;
}

//adding the second player socket
void GameRoom::setSecondPlayer(int secondPlayer) {
    this->secondPlayer = secondPlayer;
}

bool GameRoom::fullGame() {
    return secondPlayer && firstPlayer;
}
/*
 * start the game(same function from last ex)
 */
void GameRoom::handleTowClients(){
    int o=1;
    int start=2;

    //telling the second player that he is 'o'
    int n = write(secondPlayer, &o, sizeof(o));
    if (n == -1) {
        cout << "Error writing to player2" << endl;
        return;
    }
    //telling the first player to start
    n = write(firstPlayer, &start, sizeof(start));
    if (n == -1) {
        cout << "Error writing to player1" << endl;
        return;
    }
    while (!closeGame) {
        int x;
        int y;
        // Read new move from 1 problem!!11111
        int byte = read(firstPlayer, &x, sizeof(x));
        if (byte == -1) {
            cout << "Error reading player move" << endl;
            return;
        }
        if (byte == 0) {
            cout << "Client disconnected" << endl;
            return;
        }
        byte = read(firstPlayer, &y, sizeof(y));
        if (byte == -1) {
            cout << "Error reading player move" << endl;
            return;
        }
        if (byte == 0) {
            cout << "Client disconnected" << endl;
            return;
        }
        // Send move to player 2
        byte = write(secondPlayer, &x, sizeof(x));
        if (byte == -1) {
            cout << "Error writing to player2" << endl;
            return;
        }
        byte = write(secondPlayer, &y, sizeof(y));
        if (byte == -1) {
            cout << "Error writing to player2" << endl;
            return;
        }
        //means game over
        if(x == -1 && y == -1) {
            return;
        }
        // Read new move from 2
        byte = read(secondPlayer, &x, sizeof(x));
        if (byte == -1) {
            cout << "Error reading player move" << endl;
            return;
        }
        if (byte == 0) {
            cout << "Client disconnected" << endl;
            return;
        }
        byte = read(secondPlayer, &y, sizeof(y));
        if (byte == -1) {
            cout << "Error reading player move" << endl;
            return;
        }
        if (byte == 0) {
            cout << "Client disconnected" << endl;
            return;
        }

        //writing the move to player 2
        byte = write(firstPlayer, &x, sizeof(x));
        if (byte == -1) {
            cout << "Error writing to player2" << endl;
            return;
        }
        byte = write(firstPlayer, &y, sizeof(y));
        if (byte == -1) {
            cout << "Error writing to player2" << endl;
            return;
        }
        //game over
        if(x == -1 && y == -1) {
            return;
        }
    }
}
/*
 * closing the room and notify both players
 */
void GameRoom::closeRoom() {
    int x=-2,y=-2,byte=0;
    closeGame=1;
    byte = write(firstPlayer, &x, sizeof(x));
    if (byte == -1) {
        cout << "Error writing to player1" << endl;
        return;
    }
    byte = write(firstPlayer, &y, sizeof(y));
    if (byte == -1) {
        cout << "Error writing to player1" << endl;
        return;
    }

    byte = write(secondPlayer, &x, sizeof(x));
    if (byte == -1) {
        cout << "Error writing to player2" << endl;
        return;
    }
    byte = write(secondPlayer, &y, sizeof(y));
    if (byte == -1) {
        cout << "Error writing to player2" << endl;
        return;
    }
    //closing the sockets
    close(firstPlayer);
    close(secondPlayer);
}