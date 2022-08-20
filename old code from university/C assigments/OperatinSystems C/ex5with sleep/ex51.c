/* Aviv Shisman
 * 206558157
 */

//include:
#include <stdio.h>
#include <unistd.h>
#include <termios.h>
#include <signal.h>

//declerations:
char getch();
void run();


//define
#define Args 4
#define Gui "./draw.out"
#define MaxL 50

int main() {
    run();
}


/*
 * this function runs the all game.
 * it uses the ./draw and signals to give the 'gui' the moves of the player.
 */
void run(){

    //creating pipe
    int fd[2];
    if(pipe(fd)==-1){
        char pipeError[] = "Error, pipe failed";
        write(2, pipeError, sizeof(pipeError) - 1);
        return;
    }

    //creating process for execvp to run a.out
    pid_t pid;
    pid = fork();


    //if error in fork
    if (pid == -1){
        char forkError[] = "Error, fork failed";
        write(2, forkError, sizeof(forkError) - 1);
        return;
    }

    //The child
    else if (pid == 0) {

        //Transfert the fd to char* to send it as argument to execvp
        char fdIn[MaxL];
        char fdOut[MaxL];
        sprintf(fdIn, "%d", fd[0]);
        sprintf(fdOut, "%d", fd[1]);


        //using execvp
        char* commands[Args];
        commands[0]= Gui;
        commands[1] = fdIn;
        commands[2]= fdOut;
        commands[3]=NULL;

        //run the ./draw.out
        execvp(commands[0], commands);

        //error...
        char exeError[] = "Error,execvp failed";
        write(2, exeError, sizeof(exeError) - 1);



        return ;

    }//parent
    else{

        //getting keyboard press from User
        char c;
        while(c!='q'){
            c=getch();

            // Write input string and close writing end of first
            write(fd[1], &c,sizeof(c));
            kill(pid,SIGUSR2);
        }
        close(fd[0]);
        close(fd[1]);

    }
    return;

}



/*
 * get char function from you...
 */
char getch() {
    char buf = 0;
    struct termios old = {0};
    if (tcgetattr(0, &old) < 0)
        perror("tcsetattr()");
    old.c_lflag &= ~ICANON;
    old.c_lflag &= ~ECHO;
    old.c_cc[VMIN] = 1;
    old.c_cc[VTIME] = 0;
    if (tcsetattr(0, TCSANOW, &old) < 0)
        perror("tcsetattr ICANON");
    if (read(0, &buf, 1) < 0)
        perror ("read()");
    old.c_lflag |= ICANON;
    old.c_lflag |= ECHO;
    if (tcsetattr(0, TCSADRAIN, &old) < 0)
        perror ("tcsetattr ~ICANON");
    return (buf);
}