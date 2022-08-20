/*aviv shisman 206558157
 * the functions in this cpp file are all to implement the reverse rule
 * the functions dividing to 2 categories:1) check- to check if we put a piece
 * if it will cause a the rule to activate which means its a valid place to put a piece.
 * the functions up down left right and etc are functions that help check.
 *
 * 2)the second category is apply this function job is to apply the changes
 * when a piece is being placed on the board.(sub functions:applyDown and etc)
 *
 * Cell** arr the arr of cells, int x/y the location on the board,char c symbolize which
 * player is playing.
 *
 * int check return 1 if its valid place 0 if it's not.
 */

#include "ReverseRule.h"

/*
 * empty constructor...
 */
ReverseRule::ReverseRule() {

}

/*
 * functions that apply the rule.
 */
void ReverseRule::apply(Cell **arr, int x, int y, char c) const {
    if(right(arr,x,y,c)){applyRight(arr,x,y,c); }
    if(down(arr,x,y,c)){applyDown(arr,x,y,c); }
    if(up(arr,x,y,c)){applyUp(arr,x,y,c); }
    if(left(arr,x,y,c)){applyLeft(arr,x,y,c); }
    if(upRight(arr,x,y,c)){applyUpRight(arr,x,y,c); }
    if(upLeft(arr,x,y,c)){applyUpLeft(arr,x,y,c); }
    if(downLeft(arr,x,y,c)){applyDownLeft(arr,x,y,c); }
    if(downRight(arr,x,y,c)){applyDownRight(arr,x,y,c); }
}
void ReverseRule::applyDown(Cell **arr , int x , int y, char c) const {
    int i=1;
    if(c=='x') {
        if (arr[x][y + 1].symbol == 'o') {
            do {
                arr[x][y+i].symbol=arr[x][y+i].opposite();
                i++;
                if (arr[x][y + i].symbol == 'x') {
                    return;
                }

            }while(arr[x][y + i].symbol == 'o');
        }
    }
    if(c=='o') {
        if (arr[x][y + 1].symbol == 'x') {
            do {
                arr[x][y+i].symbol=arr[x][y+i].opposite();

                i++;
                if (arr[x][y + i].symbol == 'o') {
                    return;
                }
            }while(arr[x][y + i].symbol == 'x');
        }
    }
    return;


}
void ReverseRule::applyUp(Cell **arr , int x , int y, char c) const {
    int i=1;
    if(y<=1){
        return;
    }
    if(c=='x') {
        if (arr[x][y - 1].symbol == 'o') {
            do {
                arr[x][y-i].symbol=arr[x][y-i].opposite();
                i++;
                if (arr[x][y - i].symbol == 'x') {
                    return;
                }

            }while(arr[x][y - i].symbol == 'o');
        }
    }
    if(c=='o') {
        if (arr[x][y - 1].symbol == 'x') {
            do {
                arr[x][y-i].symbol=arr[x][y-i].opposite();

                i++;
                if (arr[x][y - i].symbol == 'o') {
                    return;
                }
            }while(arr[x][y - i].symbol == 'x');
        }
    }
    return;


}
void ReverseRule::applyRight(Cell **arr , int x , int y, char c) const {
    int i=1;
    if(c=='x') {
        if (arr[x+ 1][y].symbol == 'o') {
            do {
                arr[x+i][y].symbol=arr[x+i][y].opposite();
                i++;
                if (arr[x + i][y].symbol == 'x') {
                    return;
                }

            }while(arr[x+ i][y].symbol == 'o');
        }
    }
    if(c=='o') {
        if (arr[x+ 1][y ].symbol == 'x') {
            do {
                arr[x+i][y].symbol=arr[x+i][y].opposite();
                i++;
                if (arr[x+ i][y ].symbol == 'o') {
                    return;
                }
            }while(arr[x+ i][y ].symbol == 'x');
        }
    }
    return;


}
void ReverseRule::applyLeft(Cell** arr,int x,int y,char c) const{
    int i=1;
    if(x<=1){
        return ;
    }
    if(c=='x') {
        if (arr[x-1][y].symbol == 'o') {
            do {
                arr[x-i][y].symbol=arr[x-i][y].opposite();
                i++;
                if (arr[x - i][y].symbol == 'x') {
                    return;
                }
            }while(arr[x- i][y].symbol == 'o');
        }
    }
    if(c=='o') {
        if (arr[x-1][y].symbol == 'x') {
            do {
                arr[x-i][y].symbol=arr[x-i][y].opposite();
                i++;
                if (arr[x-i][y].symbol == 'o') {
                    return ;
                }
            }while(arr[x- i][y].symbol == 'x');
        }
    }
    return ;
}
void ReverseRule::applyDownRight(Cell** arr,int x,int y,char c) const{
    int i=1;
    int j=1;
    if(c=='x') {
        if (arr[x+1][y+1 ].symbol == 'o') {
            do {
                arr[x+i][y+j].symbol=arr[x+i][y+j].opposite();
                i++;
                j++;
                if (arr[x + i][y+j].symbol == 'x') {
                    return;
                }
            }while(arr[x+ i][y+j].symbol == 'o');
        }
    }
    if(c=='o') {
        if (arr[x+1][y+1 ].symbol == 'x') {
            do {
                arr[x+i][y+j].symbol=arr[x+i][y+j].opposite();
                i++;
                j++;
                if (arr[x + i][y+j].symbol == 'o') {
                    return;
                }
            }while(arr[x + i][y+j].symbol == 'x');
        }
    }
    return;
}
void ReverseRule::applyDownLeft(Cell** arr,int x,int y,char c) const{
    int i=1;
    int j=1;
    if(x<=1){
        return ;
    }
    if(c=='x') {
        if (arr[x-1][y+1 ].symbol == 'o') {
            do {
                arr[x-i][y+j].symbol=arr[x-i][y+j].opposite();
                i++;
                j++;
                if (arr[x - i][y+j].symbol == 'x') {
                    return ;
                }
            }while(arr[x- i][y+j].symbol == 'o');
        }
    }
    if(c=='o') {
        if (arr[x-1][y+1 ].symbol == 'x') {
            do {
                arr[x-i][y+j].symbol=arr[x-i][y+j].opposite();
                i++;
                j++;
                if (arr[x - i][y+j].symbol == 'o') {
                    return ;
                }
            }while(arr[x - i][y+j].symbol == 'x');
        }
    }
    return ;
}
void ReverseRule::applyUpRight(Cell** arr,int x,int y,char c) const{
    int i=1;
    int j=1;
    if(y<=1){
        return;
    }
    if(c=='x') {
        if (arr[x+1][y-1 ].symbol == 'o') {
            do {
                arr[x+i][y-j].symbol=arr[x+i][y-j].opposite();
                i++;
                j++;
                if (arr[x + i][y-j].symbol == 'x') {
                    return ;
                }
            }while(arr[x+ i][y-j].symbol == 'o');
        }
    }
    if(c=='o') {
        if (arr[x+1][y-1 ].symbol == 'x') {
            do {
                arr[x+i][y-j].symbol=arr[x+i][y-j].opposite();
                i++;
                j++;
                if (arr[x + i][y-j].symbol == 'o') {
                    return ;
                }
            }while(arr[x + i][y-j].symbol == 'x');
        }
    }
    return ;
}
void ReverseRule::applyUpLeft(Cell** arr,int x,int y,char c) const{
    int i=1;
    int j=1;
    if(y<=1 || x<=1){
        return ;
    }
    if(c=='x') {
        if (arr[x-1][y-1 ].symbol == 'o') {
            do {
                arr[x-i][y-j].symbol=arr[x-i][y-j].opposite();
                i++;
                j++;
                if (arr[x - i][y-j].symbol == 'x') {
                    return ;
                }
            }while(arr[x- i][y-j].symbol == 'o');
        }
    }
    if(c=='o') {
        if (arr[x-1][y-1 ].symbol == 'x') {
            do {
                arr[x-i][y-j].symbol=arr[x-i][y-j].opposite();
                i++;
                j++;
                if (arr[x - i][y-j].symbol == 'o') {
                    return ;
                }
            }while(arr[x - i][y-j].symbol == 'x');
        }
    }
    return ;
}

/*
 * functions that check if the rule is occuring.
 */
int ReverseRule :: check(Cell** arr,int x,int y,char c) const{
    if(!arr[x][y].isEmpty()){
        return 0;
    }
    if(x==0 || y==0){
        return 0;
    }
    if(up(arr,x, y,c) ||right(arr,x, y,c) ||down(arr,x, y,c) ||left(arr,x, y,c) ||
       upRight(arr,x, y,c) ||upLeft(arr,x, y,c) ||downLeft(arr,x, y,c)
       ||downRight(arr,x, y,c)){
        return 1;
    }



    return 0;

}
int ReverseRule::down(Cell** arr,int x,int y,char c) const{
    int i=1;
    if(c=='x') {
        if (arr[x][y + 1].symbol == 'o') {
            do {
                i++;
                if (arr[x][y + i].symbol == 'x') {
                    return 1;
                }
            }while(arr[x][y + i].symbol == 'o');
        }
    }
    if(c=='o') {
        if (arr[x][y + 1].symbol == 'x') {
            do {
                i++;
                if (arr[x][y + i].symbol == 'o') {
                    return 1;
                }
            }while(arr[x][y + i].symbol == 'x');
        }
    }
    return 0;
}
int ReverseRule::up(Cell** arr,int x,int y,char c) const{
    int i=1;
    if(y<=1){
        return 0;
    }
    if(c=='x') {
        if (arr[x][y - 1].symbol == 'o') {
            do {
                i++;
                if (arr[x][y - i].symbol == 'x') {
                    return 1;
                }
            }while(arr[x][y - i].symbol == 'o');
        }
    }
    if(c=='o') {
        if (arr[x][y - 1].symbol == 'x') {
            do {
                i++;
                if (arr[x][y - i].symbol == 'o') {
                    return 1;
                }
            }while(arr[x][y - i].symbol == 'x');
        }
    }
    return 0;
}
int ReverseRule::right(Cell** arr,int x,int y,char c) const{
    int i=1;
    if(c=='x') {
        if (arr[x+ 1][y].symbol == 'o') {
            do {
                i++;
                if (arr[x + i][y].symbol == 'x') {
                    return 1;
                }
            }while(arr[x+ i][y].symbol == 'o');
        }
    }
    if(c=='o') {
        if (arr[x+1][y].symbol == 'x') {
            do {
                i++;
                if (arr[x+ i][y].symbol == 'o') {
                    return 1;
                }
            }while(arr[x+ i][y].symbol == 'x');
        }
    }
    return 0;
}
int ReverseRule::left(Cell** arr,int x,int y,char c) const{
    int i=1;
    if(x<=1){
        return 0;
    }
    if(c=='x') {
        if (arr[x-1][y].symbol == 'o') {
            do {
                i++;
                if (arr[x - i][y].symbol == 'x') {
                    return 1;
                }
            }while(arr[x- i][y].symbol == 'o');
        }
    }
    if(c=='o') {
        if (arr[x-1][y].symbol == 'x') {
            do {
                i++;
                if (arr[x-i][y].symbol == 'o') {
                    return 1;
                }
            }while(arr[x- i][y].symbol == 'x');
        }
    }
    return 0;
}
int ReverseRule::downRight(Cell** arr,int x,int y,char c) const{
    int i=1;
    int j=1;
    if(c=='x') {
        if (arr[x+1][y+1 ].symbol == 'o') {
            do {
                i++;
                j++;
                if (arr[x + i][y+j].symbol == 'x') {
                    return 1;
                }
            }while(arr[x+ i][y+j].symbol == 'o');
        }
    }
    if(c=='o') {
        if (arr[x+1][y+1 ].symbol == 'x') {
            do {
                i++;
                j++;
                if (arr[x + i][y+j].symbol == 'o') {
                    return 1;
                }
            }while(arr[x + i][y+j].symbol == 'x');
        }
    }
    return 0;
}
int ReverseRule::downLeft(Cell** arr,int x,int y,char c) const{
    int i=1;
    int j=1;
    if(x<=1){
        return 0;
    }
    if(c=='x') {
        if (arr[x-1][y+1 ].symbol == 'o') {
            do {
                i++;
                j++;
                if (arr[x - i][y+j].symbol == 'x') {
                    return 1;
                }
            }while(arr[x- i][y+j].symbol == 'o');
        }
    }
    if(c=='o') {
        if (arr[x-1][y+1 ].symbol == 'x') {
            do {
                i++;
                j++;
                if (arr[x - i][y+j].symbol == 'o') {
                    return 1;
                }
            }while(arr[x - i][y+j].symbol == 'x');
        }
    }
    return 0;
}
int ReverseRule::upRight(Cell** arr,int x,int y,char c) const{
    int i=1;
    int j=1;
    if(y<=1){
        return 0;
    }
    if(c=='x') {
        if (arr[x+1][y-1 ].symbol == 'o') {
            do {
                i++;
                j++;
                if (arr[x + i][y-j].symbol == 'x') {
                    return 1;
                }
            }while(arr[x+ i][y-j].symbol == 'o');
        }
    }
    if(c=='o') {
        if (arr[x+1][y-1 ].symbol == 'x') {
            do {
                i++;
                j++;
                if (arr[x + i][y-j].symbol == 'o') {
                    return 1;
                }
            }while(arr[x + i][y-j].symbol == 'x');
        }
    }
    return 0;
}
int ReverseRule::upLeft(Cell** arr,int x,int y,char c) const{
    int i=1;
    int j=1;
    if(y<=1 || x<=1){
        return 0;
    }
    if(c=='x') {
        if (arr[x-1][y-1 ].symbol == 'o') {
            do {
                i++;
                j++;
                if (arr[x - i][y-j].symbol == 'x') {
                    return 1;
                }
            }while(arr[x- i][y-j].symbol == 'o');
        }
    }
    if(c=='o') {
        if (arr[x-1][y-1 ].symbol == 'x') {
            do {
                i++;
                j++;
                if (arr[x - i][y-j].symbol == 'o') {
                    return 1;
                }
            }while(arr[x - i][y-j].symbol == 'x');
        }
    }
    return 0;
}

