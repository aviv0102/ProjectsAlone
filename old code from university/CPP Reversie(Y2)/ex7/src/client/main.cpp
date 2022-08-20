/*aviv shisman 206558157 01
rome sharon 209296235 01*/

#include "Board.h"
#include "CellManger.h"
#include "ReverseRule.h"
#include "Player.h"
#include "HumanPlayer.h"
#include "GameFlow.h"
#include "AIPlayer.h"

#include "ClientPlayer.h"
#include <fstream>
#include <sstream>

/*the main function.
creating the board and setting pieces.*/


using namespace std;

int main(int argc, char *argv[]) {
    int shouldDelete = 0;
    int choice;
    do {
        //setting up all the classes related to board
        bool isOnline = false;
        GameFlow *g;
        Player *p1 = NULL;
        Player *p2 = NULL;
        Client *client = NULL;
        Player **players = new Player *[2];
        CellManger *c = new CellManger(8);
        c->setWhite(4, 4);
        c->setWhite(5, 5);
        c->setBlack(4, 5);
        c->setBlack(5, 4);
        Board *b = new Board(8, c->getArr());
        Rule *r = new ReverseRule();
        ifstream settings;
        string line;
        string ip;
        int port = 0;

        //reading the port and ip from file called cSettings
        if (argc <= 1) {
            cout << "Error settings file did'nt entered" << endl;
            return 1;
        }
        settings.open(argv[1]);
        if (!settings.is_open()) {
            cout << "Error opening settings file" << endl;
            return 1;
        }
        getline(settings, line);
        stringstream data(line);
        data >> port;
        getline(settings, ip);


        //chosing the mode
        cout << "Welcome to Reversi!!!!" << endl << "1. 1 vs 1" << endl << "2. 1 vs Computer" << endl
             << "3. play Online" << endl << "4. close reversi" << endl;
        do {
            cout << "Enter your choice here" << endl;
            cin >> choice;
        } while (choice != 1 && choice != 2 && choice != 3 && choice != 4);

        //1v1 offline
        if (choice == 1) {
            p2 = new HumanPlayer('o');

        //1vAi offline
        } else if (choice == 2) {
            p2 = new AIPlayer('o', c);

        //online play...(has a menu for it)
        } else if (choice == 3) {
            //connecting to server
            char symbol;
            isOnline = true;
            client = new Client(ip.c_str(), port);
            try {
                client->connectToServer();
                client->start();
                if (client->recvKey() == 0) {
                    symbol = 'x';
                } else {
                    symbol = 'o';
                }
            } catch (const char *msg) {
                cout << "Faild:" << msg << endl;
            }
            //creating the classes related to online play
            p1 = new ClientPlayer(client, symbol);
            players[0] = p1;
            //player 2 is online so here null
            players[1] = NULL;
            g = new GameFlow(b, c, r, players, client);
            if (symbol == 'x') {
                cout << "Waiting for the other player to connect..." << endl;
                client->recvKey();
            }
        }

        //if not online play
        if (choice != 3 && choice != 4) {
            p1 = new HumanPlayer('x');
            players[0] = p1;
            players[1] = p2;
            g = new GameFlow(b, c, r, players);
        }
        //if choise = 1,2,3 deleting the following
        if (choice < 4 && choice >= 1) {
            g->play();
            b->show();
            delete g;
            delete p1;
            if (!isOnline) {
                delete p2;
            } else {
                delete (client);
            }
        }
        //delete these always
        delete[] players;
        delete b;
        delete r;
        delete c;
    } while (choice != 4);

    return 0;
}


