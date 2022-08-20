/*aviv shisman 206558157 01
rome sharon 209296235 01*/
#include "Board.h"
#include <iostream>
using namespace std;


//constructor
Board::Board(int size,Cell** arr) : size(size),arr(arr) {}

//simple getter for size
int Board::getSize() const {
    return size;
}
//prints the board in the wanted format.
void Board::show() const {
    for (int i = 0; i <= size; i++) {
        for (int j = 1; j <= size; j++) {
            if (i == 0) {
                cout << " | " << j;
                if (j == size) {
                    cout << " |";
                }
            }
            else {
                if (j == 1) {
                    cout << i << "| ";
                }
                if (arr[i][j].symbol == 'x' || arr[i][j].symbol == 'o') {

                    cout <<arr[i][j].symbol<<" | " ;
                }
                else{
                    cout << "  | ";

                }

            }
        }
        cout << "\n";
        cout << " ";

        for (int j = 0; j < size; j++) {
            cout << "----" ;

        }
        cout << "\n";


    }

    cout<<endl;
}



//
//

