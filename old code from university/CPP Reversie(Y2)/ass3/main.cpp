/*aviv shisman 206558157 01
rome sharon 209296235 01*/
#include "Board.h"
#include "CellManger.h"
#include "ReverseRule.h"
#include "Player.h"
#include "HumanPlayer.h"
#include "GameFlow.h"
#include "AIPlayer.h"
#include <iostream>
/*the main function.
creating the board and setting pieces.*/

using namespace std;

int main()
{
    int choice;
    CellManger* c=new CellManger(8);
    c->setWhite(4,4);
    c->setWhite(5,5);
    c->setBlack(4,5);
    c->setBlack(5,4);
    Board* b=new Board(8,c->getArr());
    Rule* r=new ReverseRule();
    cout << "Welcome to Reversi!!!!" << endl << "1. 1 vs 1"<< endl << "2. 1 vs Computer" << endl;
    do {
        cout << "Enter your choice here";
        cin >> choice;
    }while (choice != 1 && choice != 2);\
    Player* p2;
    if(choice == 1) {
        p2 =new HumanPlayer('o');
    } else {
        p2 = new AIPlayer('o', c);
    }
    Player* p1=new HumanPlayer('x');

    Player** players=new Player*[2];
    players[0]=p1;
    players[1]=p2;
    GameFlow* g=new GameFlow(b,c,r,players);
    g->play();
    b->show();

    delete c;
    delete b;
    delete r;
    delete p1;
    delete p2;
    delete[] players;
    delete g;


    return 0;
}

