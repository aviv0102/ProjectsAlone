/* name: aviv shisman
 * id: 206558157
 */
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <malloc.h>

#include <wait.h>
#include <stdlib.h>

#define Max 100
#define MaxArgs 20


//the Task -> process that running in background
typedef struct Task {
    int pid;
    char** args;
    int numOfArgs;
    struct Task* next;

}Task_t;

//declerations;
void ChangeDir(char**,int);
void addTask(Task_t*);
void print();
void removeUnused();
int isDead(Task_t*);
void deleteTask(Task_t*);
void killAll();

//the root of the working tasks list
Task_t* root=NULL;



/* the main -> the "shell" we created
 * i used main and other functions to help
 * the loop is infinite to imulate a regult shell
 * and will end only if the command "exit" is entered
 */
int main() {
    int Notexit=1;
    while(Notexit){
        //getting command
        printf("prompt> ");
        char command[Max];
        fgets(command,Max,stdin);
        command[strlen(command)-1]=0;

        //split the command to args
        const char delimeter[2]=" ";
        char* commands[MaxArgs];
        commands[0]=strtok(command,delimeter);
        int i=0;
        while( commands[i] != NULL ) {
            i++;
            commands[i] = strtok(NULL, delimeter);
        }
        int len=i;

        //in case we don't wait for process to end
        int stop=1;
        if(strcmp(commands[i-1],"&")==0){
            stop=0;
            commands[i-1]=NULL;
            len--;
        }

        //in case command is exit
        if(strcmp(commands[0],"exit")==0){
            Notexit=0;
            killAll();
            return 0;
        }

        //in case command is jobs
        if(strcmp(commands[0],"jobs")==0){
            print(len);
            continue;
        }

        //execute command and creating process
        pid_t pid;
        pid = fork();


        //if error in fork
        if (pid == -1)
            fprintf(stderr,"fork error");

        //The child
        else if (pid == 0) {

            //printing pid in case the parent is waiting for child
            //i used the knowledge the process duplicates all the memory
            if(stop){
                printf("%d\n",getpid());
            }

            //cd special method
            if(strcmp(commands[0],"cd")==0){
                //allocatin dynamicly to send to a func
                char** args=(char**)calloc(len,sizeof(char*));
                for(i=0;i<len;i++){
                    args[i]=(char*)calloc(strlen(commands[i])+1,sizeof(char));
                    strcpy(args[i],commands[i]);
                }
                //calling internal method
                ChangeDir(args,len);
            }

            //Not cd -> all the other commands
            else{
                //using execvp to execute shell commands
                //initailly i used execv but man command don't work there so i used execvp
                execvp(commands[0],commands);

                //using execv to run commands without man:
                /*char firstArg[Max]="/bin/";
                char firstArgTail[Max];
                strcpy(firstArgTail,commands[0]);
                strcat(firstArg,firstArgTail);
                execv(firstArg,commands);*/

                //in case of error
                fprintf(stderr,"Error in system call\n");

            }

        }
        //parent
        else{
            //in case we don't got a '&' -> need to wait to child
            if(stop){
                int returnStatus;
                waitpid(pid,&returnStatus,0);
            }
            //if we got a '&' ->  do the task in background-> create a Task and add it to the list
            else{
                //in case we don't wait to the child,the father will print the pid
                printf("%d\n",pid);

                //Creating a Task and adding it using addTask function
                char** args=(char**)calloc(len,sizeof(char*));
                for(i=0;i<len;i++){
                    args[i]=(char*)calloc(strlen(commands[i])+1,sizeof(char));
                    strcpy(args[i],commands[i]);
                }
                Task_t* newTask=(Task_t*)calloc(1,sizeof(Task_t));
                newTask->args=args;
                newTask->pid=pid;
                newTask->numOfArgs=len;
                addTask(newTask);
            }
        }

    }

}

/*
 * my method to do cd command
 */
void ChangeDir(char** args,int len) {
    //if no arguments to cd -> go to Home
    if(args[1]==NULL){
        chdir(getenv("HOME"));
        return;
    }

    //if there is args to cd go to location
    int res=chdir(args[1]);
    if(res==-1){
        fprintf(stderr,"no such dir");
    }
    int i=0;
    for(i=0;i<len;i++){
        free(args[i]);
    }
    free(args);
}

/* adding a task to jobs
 * using linked list
 */
void addTask(Task_t* t){
    if(root==NULL){
        root=t;
        t->next=NULL;
    }
    else{
        Task_t* p=root;
        while(p->next!=NULL){
            p=p->next;
        }
        p->next=t;
        t->next=NULL;
    }

    return;
}

/* going all over the list
 * and printing the tasks
 */
void print(){

    if(root==NULL) {
        return;
    }

    //updating before
    removeUnused();

    //in case root was removed
    if(root==NULL) {
        return;
    }

    int i;
    Task_t* p=root;
    printf("pid:%d ,command:",p->pid);
    for(i=0;i<p->numOfArgs;i++)
        printf(" %s",p->args[i]);
    printf("\n");

    while(p->next!=NULL){
        p=p->next;
        printf("pid:%d ,command:",p->pid);
        for(i=0;i<p->numOfArgs;i++)
            printf(" %s",p->args[i]);
        printf("\n");        }

}

/* remove unActive processes
 * using deleteTask and isDead as subroutines
 */
void removeUnused(){
    Task_t* p;
    if(isDead(root) ){
        if(root->next!=NULL) {
            p = root;
            root = root->next;
            deleteTask(p);
            removeUnused();
            return;
        }else{
            deleteTask(root);
            root=NULL;
        }
    }

    else{
        Task_t* p=root;
        Task_t * temp;
        while(p!=NULL){
            temp=p->next;
            if(temp!=NULL && isDead(temp)){
                if(temp->next!=NULL)
                    p->next=temp->next;
                else{
                    p->next=NULL;
                }
                deleteTask(temp);
            }
            p=p->next;
        }

    }

}

/*
 * checks if process is "Dead"
 */
int isDead(Task_t* t){
    int status;
    if(t==NULL){
        return -1;
    }
    pid_t resultFromCheck=waitpid(t->pid,&status,WNOHANG);
    if(resultFromCheck==-1){
        fprintf(stderr,"Error, can't check process status..");
    }
    else if(resultFromCheck==0){
        //still running
        return 0;
    }
    else if (resultFromCheck==t->pid){
        //stopped
        return 1;
    }
}

/* delete the Task easily
 */
void deleteTask(Task_t* t){
    int i=0;
    for(i=0;i<t->numOfArgs;i++){
        free(t->args[i]);
    }
    free(t->args);
    free(t);
}

//kill all process
void killAll(){

    Task_t* t=root;
    Task_t* p=NULL;

    while(t!=NULL){
        while(!isDead(t)){
            kill(t->pid,SIGKILL);
        }
        p=t;
        t=t->next;
        deleteTask(p);
    }

}
