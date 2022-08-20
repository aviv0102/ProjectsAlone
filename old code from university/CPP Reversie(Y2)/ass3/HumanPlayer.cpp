/*aviv shisman 206558157
 * human player gets the optional moves and choose what to do
 */

#include "HumanPlayer.h"
#include <iostream>
using namespace std;
/*
 * constructor ,symbol is
 */
HumanPlayer::HumanPlayer(char x){
    symbol=x;
}
/* gets arr of points and print them to the user
 * int a the number of points
 */
Point* HumanPlayer::oneMove(Point** pointsArr,int a) const  {
    cout<<symbol<<":"<<"its your Move!\n";
    cout<<"your possible moves are: ";
    for(int i=0;i<a;i++){
            cout<<"("<<pointsArr[i]->getX()<<","<<pointsArr[i]->getY()<<")"<<" ";
    }

    cout<<endl;
    cout<<"choose a move by pressing a number a space and than the other number"<<endl;

    cout<<endl;
    cout<<endl;
    int flag=1;
    int x, y;
    //loops until the user chooses valid option
    do {
        cin >> x >> y;
        for(int i=0;i<a;i++){
            if(x==pointsArr[i]->getX() && y==pointsArr[i]->getY())
                flag=0;
        }
        if(flag==1){
            cout<<"not an option try again"<<endl;
        }
    }while(flag);
    cout<<"you chose "<<x<<","<<y<<endl;

    Point* p=new Point(x,y);

    return p;

}

char HumanPlayer::getSymbol() const {
    return symbol;
};