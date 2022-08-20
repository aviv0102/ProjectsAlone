/*aviv shisman 206558157 01
rome sharon 209296235 01*/

#include "AIPlayer.h"
AIPlayer::AIPlayer(char s, CellManger* cells){
    this->symbol = s;
    this->c = cells;
}

char AIPlayer::getSymbol() const {
    return this->symbol;
}

Point* AIPlayer::oneMove(Point ** points, int a) const {
    map<Point*, int> moves;
    Point* p;
    ReverseRule rule;
    int row, col, counter = 0, min = c->getSize() * c->getSize();
    int rowSecond, colSecond, max = -c->getSize() * c->getSize();
    char opposite;
    for(int i = 0; i < a; i++) {
        //copy the board.
        CellManger copyCell(c->getSize());
        row = points[i]->getX();
        col = points[i]->getY();
        copyCell.setArr(c->getArr());

        //applying the move
        copyCell.setCell(row, col, symbol);
        opposite = copyCell.getArr()[row][col].opposite();
        rule.apply(copyCell.getArr(), row, col, symbol);

        //get opposite player moves
        Point** oppositeMoves = new Point*[c->getSize() * c->getSize()];
        for (int k = 1; k <= copyCell.getSize(); k++) {
            for (int l = 1; l <= copyCell.getSize(); l++) {
                if (rule.check(copyCell.getArr(), k, l, opposite) ) {
                    oppositeMoves[counter] = new Point(k, l);
                    counter++;
                }
            }
        }

        //checking the "max" move for opposite player
        for(int j = 0; j < counter; j++) {
            CellManger copyCellSecond(copyCell.getSize());
            copyCellSecond.setArr(copyCell.getArr());
            rowSecond = oppositeMoves[j]->getX();
            colSecond = oppositeMoves[j]->getY();
            copyCellSecond.setCell(rowSecond, colSecond, opposite);
            rule.apply(copyCellSecond.getArr(), rowSecond, colSecond, opposite);
            int sub = copyCell.getCount(opposite) - copyCellSecond.getCount(symbol);
            if(max < sub) {
                max = sub;
            }
        }

        //adding the move we did and the max of the opposite player to map
        moves[points[i]] = max;
        for(int i=0;i<counter;i++){
            delete oppositeMoves[i];
        }
        delete oppositeMoves;
        counter = 0;
    }
    //iterating over the moves and chosing the move that will bring the opposite player the lowest max
    int flag=0;
    for (map<Point*, int>::iterator it=moves.begin(); it!=moves.end(); it++) {
        if(it->second < min) {
            if(flag){
                delete(p);
            }
            min = it->second;
            p = new Point(*it->first);
            flag=1;
        }
    }

    return p;
}

CellManger *AIPlayer::getC() const {
    return c;
}

