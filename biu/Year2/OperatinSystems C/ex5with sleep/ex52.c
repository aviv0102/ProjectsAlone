/* Aviv Shisman
 * 206558157
 */

//include:
#include <stdio.h>
#include <malloc.h>
#include <zconf.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>


//define
#define rows 20
#define cols 20
#define mid 10
#define MaxL 50

//struct:
typedef struct shap{
    int row;
    int col;
    int Reversed;// 0 horizontal 1 for Reversed
    void (*draw)( struct shap*,char**);

}shape;

//declerations:
void play();
void drawBoard(shape**,int);
void fillBoard(char**);
void draw(shape* self,char **);
void FreeShape(shape*);
void FreeBoard(char**);
void TimePassed(shape**,int*);
void getFd(int,char*[]);
void changePos(int);
int applyChange(shape**,int);
char** CreateBoard();
shape* CreateShape();


//global variables(we must have because of the signal):
int *fd;
char change;


/* The main runs the Gui and the shows board
 * if it gets signal from the parent it applys the moves
 */

int main(int argc,char* argv[]) {

    getFd(argc,argv);

    //getting signals
    signal(SIGUSR2,changePos);

    play();


    return 0;
}


/*
 * the main function that has the main loop of game
 */
void play(){

    //for errors
    char allocError[] = "Error, Allocation of Shapes failed";

    //creating Shapes
    shape** myShapes=(shape**)calloc(1,sizeof(shape*));
    int countShape=0;
    if(myShapes==NULL){
        write(2, allocError, sizeof(allocError) - 1);
        return;
    }
    myShapes[countShape]=CreateShape();
    countShape++;

    //Game Loop:
    int flag=1;
    while(flag){
        //in case of change, the default is 'u'
        if(change!='u'){
            flag=applyChange(myShapes,countShape);
            if(flag==0){
                system("clear");
                continue;
            }
        }

        //draw the board and apply time
        drawBoard(myShapes,countShape);
        sleep(1);
        TimePassed(myShapes,&countShape);
        //if time passed and the shape was deleted create a new one
        if(countShape==0){
            countShape++;
            myShapes[countShape-1]=CreateShape();
        }
    }

}


/*
 * draw the board and all the shapes
 */
void drawBoard(shape** myShapes,int count){
    system("clear");
    char ** board=CreateBoard();
    int i=0;
    int j=0;
    int k=0;
    fillBoard(board);

    for(k=0;k<count;k++){
        myShapes[k]->draw(myShapes[k],board);
    }


    for(i=0;i<rows;i++){
        for(j=0;j<cols;j++){
            printf("%c",board[i][j]);
        }
        printf("\n");


    }

    FreeBoard(board);

}


/*
 * apply time pass, delete shapes that got to border
 */
void TimePassed(shape** s,int* n){
    int i=0;
    int update=*n;
    for(i=0;i<*n;i++){
        s[i]->row++;
        if((s[i]->row>=rows-1 && !s[i]->Reversed)||
                s[i]->Reversed && s[i]->row>=rows-2 ){
            FreeShape(s[i]);
            update--;
        }
    }
    *n=update;

}


/*
 * fill the board with the border
 */
void fillBoard(char** board){
    int i=0,j=0;
    for(i=0;i<rows;i++){
        for(j=0;j<cols;j++){

            if(i==rows-1){
                board[i][j]='*';
                continue;
            }

            if(j==0 || j==cols-1){
                board[i][j]='*';
            }
            else{
                board[i][j]=' ';
            }

        }
    }
}

/*
 * draw a shape
 */
void draw(shape* self,char** board){
    int row=self->row;
    int col=self->col;
    if(!self->Reversed){
        board[row][col-1]='-';
        board[row][col]='-';
        board[row][col+1]='-';

    }
    else{
        if(row==0){
            row=1;
            self->row=1;
        }
        board[row-1][col]='-';
        board[row][col]='-';
        board[row+1][col]='-';
    }
}


/*
 * free a shape
 */
void FreeShape(shape* s){
    free(s);
}


/*
 * free Board
 */
void FreeBoard(char** board){
    int i=0;
    for(i=0;i<rows;i++){
        free(board[i]);
    }
    free(board);
}


/*
 * Create a shape
 */
shape* CreateShape(){
    shape* newShape=(shape*)calloc(1,sizeof(shape));
    if(newShape==NULL){
        char allocError[] = "Error, Allocation failed";
        write(2, allocError, sizeof(allocError) - 1);
        return NULL;
    }
    newShape->col=mid;
    newShape->row=0;
    newShape->Reversed=0;
    newShape->draw=draw;

    return newShape;
}


/*
 * create a Board
 */
char** CreateBoard(){
    char allocError[] = "Error, Allocation of Board failed";

    char ** board=(char**)calloc(rows,sizeof(char*));
    if(board==NULL){
        write(2, allocError, sizeof(allocError) - 1);
        return NULL;
    }

    int i=0;
    for(i=0;i<rows;i++){
        board[i]=(char*)calloc(cols,sizeof(char));
        if(board[i]==NULL){
            write(2, allocError, sizeof(allocError) - 1);
            return NULL;
        }
    }
    return board;
}


/*
 * get the file descriptors of the Pipe
 */
void getFd(int argc,char* argv[]){

    if(argc<3){
        char sizeError[] = "Error,number of argc wrong";
        write(2, sizeError, sizeof(sizeError) - 1);
        return ;
    }

    char* fdInStr = argv[1];
    char* fdOutStr= argv[2];
    fd = (int*)calloc(2,sizeof(int));
    if(fd==NULL){
        char allocError[] = "Error, Allocation of fd arr failed";
        write(2, allocError, sizeof(allocError) - 1);
        return;
    }

    int i;
    for(i=0; i<strlen(fdInStr); i++){
        fd[0] = fd[0] * 10 + ( fdInStr[i] - '0' );
    }
    for(i=0; i<strlen(fdOutStr); i++){
        fd[1] = fd[1] * 10 + ( fdOutStr[i] - '0' );
    }
    change='u';

}


/*
 * get a signal and handle it, notify for a move
 */
void changePos(int sig){
    char c;
    read(fd[0], &c, sizeof(c));
    change=c;
}


/*
 * apply the changes on the shape
 */
int applyChange(shape** myShapes,int n ){

    int k;
    for(k=0;k<n;k++){
        int row=myShapes[k]->row;
        int col=myShapes[k]->col;
        int rev=myShapes[k]->Reversed;

        if((change=='a' && col>=3 && !rev)
           || (change=='a' && rev && col>=2)){
            myShapes[k]->col=col-1;
        }
        else if((change =='d' && col<=cols-4 && !rev)
                || (change=='d' && rev && col<=cols-3)){
            myShapes[k]->col=col+1;
        }
        else if(change == 'w'){
            myShapes[k]->Reversed=!rev;
        }
        else if((change == 's' && row<=rows-3 &&!rev)
                || (change=='s' && rev && row<=rows-4) ){
            myShapes[k]->row=row+1;

        }
        else if(change == 'q'){
            return 0;
        }
    }
    change='u';
    return 1;
}
