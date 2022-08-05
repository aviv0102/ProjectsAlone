/* name: Aviv Shisman
 * id:	 206558157
 */


//include:
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <dirent.h>
#include <string.h>
#include <wait.h>

//Define:
#define Max 160
#define endLine '\n'
#define answerLength 30
#define MaxArgs 5
#define outputLength 20

//struct for help:
typedef struct stud{
    char name [Max];
    char path[Max];
    char answer[answerLength];
    int  score;
}student;


//declarations:
int initiallize(int ,char*[]);
int numberStudents(char*);
int compile(char*);
int run(char*,char*,char*);
int compareForGrade(char*,char*,char*);
char* find(char*);
char* findOut(char*);
void deleteStudents(student**,int);
void check(student* s,char*,char*,char*);
void getInfoFromConfig(int,char*,char*,char*);
void alarm_hand(int);
void getCompOut(char*,char*);
void writeResults(student**,int);
student** getStudents(char*,int);

//global:
int currentpid=0;//for kill in case of timeout in run

/* getting the config file as param
 * Main using the other functions to run the program...
 */
int main (int argc,char* argv[]) {

    //checking arguments:
    printf("Welcome to my Auto-FeedBack\n");
    printf("checking your arguments...\n\n\n");
    int fd = initiallize(argc, argv);
    if (fd == -1) {
        return -1;
    }

    //reading config:
    printf("Reading config:\n");
    char *libPath = (char *) calloc(Max, sizeof(char));
    char *inputPath = (char *) calloc(Max, sizeof(char));
    char *outputPath = (char *) calloc(Max, sizeof(char));
    if (libPath == NULL || inputPath == NULL || outputPath == NULL) {
        char allocError[] = "Error, allocation failed";
        write(2, allocError, sizeof(allocError) - 1);
        return -1;

    }
    getInfoFromConfig(fd, libPath, inputPath, outputPath);
    printf("Directory to check:%s\nInputFile:%s\nCorrectOutput:%s\n\n\n",libPath,inputPath,outputPath);


    //get number of students:
    int size = numberStudents(libPath);
    if (size == -1) {
        return -1;
    }

    //get students:
    student **students = getStudents(libPath, size);

    //get Comp.out path
    char* compOut=(char*)calloc(Max,sizeof(char));
    char* orignalDir=(char*)calloc(Max,sizeof(char));
    getCompOut(compOut,orignalDir);
    if(compOut==NULL){ return -1; }

    //checking each student and giving him result:
    int i=0;
    printf("\nresults for checking each students are on the way please be patience\n");
    printf("Results:\n");
    for(i=0;i<size;i++){
        check(students[i],inputPath,outputPath,compOut);
        printf("student number:%d grade:%d + reason:%s\n + correct out:%s\n"
                ,i+1,students[i]->score,students[i]->answer,students[i]->path);
    }

    //update results:
    printf("\n\n\nupdate table with results...\n");
    chdir(orignalDir);
    writeResults(students,size);


    free(libPath);
    free(outputPath);
    free(inputPath);
    free(compOut);
    free(orignalDir);
    deleteStudents(students,size);

    close(fd);

    return 0;

}




/* input: the directory we wish to follow
 * output: number of students in it.
 */
int numberStudents(char* libPath){
    DIR *pDir;
    struct dirent *library;
    //first getting number of students
    int size=0;
    if ( (pDir = opendir(libPath)) == NULL)
        return -1;

    while ( (library = readdir(pDir) ) != NULL ){
        //checking if name is directory

        if(strcmp(library->d_name,".")==0 || strcmp(library->d_name,"..")==0){
            //ignore because its not student
            continue;
        }
        char* temp=(char*)calloc(Max,sizeof(char));
        char* help=(char*)calloc(Max,sizeof(char));
        help[0]='/';
        strcpy(temp,libPath);
        strcat(help,library->d_name);
        strcat(temp,help);


        DIR* dir = opendir(temp);
        if (dir)
        {
            size++;
            closedir(dir);
        }
        free(temp);
        free(help);
    }
    closedir( pDir );

    return  size;
}


/* input:argc,argv
 * output: if arguments are legal
 */
int initiallize(int argc,char* argv[]){

    if(argc!=2){
        char NumOfArgsError[]="Error, Number of args is Invalid";
        write(2,NumOfArgsError,sizeof(NumOfArgsError)-1);
        return -1;
    }

    // initialize file descriptors with 'r' mode to the config
    int fd;
    fd = open(argv[1],O_RDONLY);
    if(fd<0){
        char fdError[]="Error, file descriptor is Invalid";
        write(2,fdError,sizeof(fdError)-1);
        return  -1;
    }

    return fd;

}


/* input: c file path
 * output: compiles it...
 */
int compile(char* cPath){
    //creating process for execvp
    pid_t pid;
    pid = fork();

    //if error in fork
    if (pid == -1){
        char compError[] = "Error, compile failed";
        write(2, compError, sizeof(compError) - 1);
        return 1;
    }

        //The child
    else if (pid == 0) {
        char* commands[MaxArgs];
        commands[0]= "gcc";
        commands[1] = cPath;
        commands[2]=NULL;

        //compile errors will go to the txt file and will not show up
        int fderror = open("compileError.txt",O_CREAT|O_TRUNC|O_WRONLY);
        dup2(fderror,2);

        close(fderror);
        unlink("compileError.txt");

        execvp(commands[0], commands);

        char exeError[] = "Error,execvp failed";
        write(2, exeError, sizeof(exeError) - 1);

        return 1;

    }//parent
    else{
        //wait for child
        int returnStatus;
        waitpid(pid,&returnStatus,0);
    }
    return 0;
}


/* input: result(where to store), input(the input from config), aout(compilation output)
 * output: student program output
 */
int run(char* result,char* input,char* aout){

    //setting alarm for timeout(3 seconds is faster)
    signal(SIGALRM,alarm_hand);
    alarm(3);

    //creating process for execvp to run a.out
    pid_t pid;
    pid = fork();


    //if error in fork
    if (pid == -1){
        char forkError[] = "Error, fork failed";
        write(2, forkError, sizeof(forkError) - 1);
        return 1;
    }

        //The child
    else if (pid == 0) {

        // replace standard output with output file and same for input
        int in = open(input,O_RDONLY);
        int out = open(result, O_WRONLY | O_TRUNC | O_CREAT,
                       S_IRUSR | S_IRGRP | S_IWGRP | S_IWUSR);
        dup2(in, 0);
        dup2(out, 1);

        //using execvp
        char* commands[MaxArgs];
        commands[0]= "./a.out";
        commands[1] = NULL;
        commands[2]=NULL;


        //close fd's
        close(in);
        close(out);

        execvp(commands[0], commands);

        char exeError[] = "Error,execvp failed";
        write(2, exeError, sizeof(exeError) - 1);



        return 1;

    }//parent
    else{
        //wait for child
        currentpid=pid;
        int returnStatus;
        waitpid(pid,&returnStatus,0);
        unlink(aout);

        //delete output in case of timeout
        if(currentpid==-1){
            unlink(result);
            return 1;
        }
    }
    return 0;

}


/* compare student output to correct output using comp.out
 * output: comp.out return
 */
int compareForGrade(char* myout,char* correctout,char* compout){

    //creating process for execvp to run comp.out for final grading:
    pid_t pid;
    pid = fork();


    //if error in fork
    if (pid == -1){
        char forkError[] = "Error, fork failed";
        write(2, forkError, sizeof(forkError) - 1);
        return 1;
    }

        //The child
    else if (pid == 0) {

        //using execvp
        char* commands[MaxArgs];
        commands[0]= compout;
        commands[1] =myout;
        commands[2]=correctout;
        commands[3]=NULL;
        execvp(commands[0], commands);
        char exeError[] = "Error,execvp failed";
        write(2, exeError, sizeof(exeError) - 1);

        return 1;

    }//parent
    else{
        //wait for child:
        int returnStatus;
        waitpid(pid,&returnStatus,0);
        unlink(myout);

        //get exit status:
        int exit=WEXITSTATUS(returnStatus);
        return exit;
    }

}


/* get info from config using file descriptor(read)
 * and putting it in pre allocated spaces.(lib,input,output)
 */
void getInfoFromConfig(int fd,char* libPath,char* inputPath,char* outputPath){

    char ch;
    int i=0;
    while(read(fd, &ch, sizeof(char)) >0 &&  ch!=endLine) {
        libPath[i]=ch;
        i++;
    }
    i=0;
    while(read(fd, &ch, sizeof(char)) >0 &&  ch!=endLine) {
        inputPath[i]=ch;
        i++;
    }
    i=0;
    while(read(fd, &ch, sizeof(char)) >0 &&  ch!=endLine) {
        outputPath[i]=ch;
        i++;
    }


}


/*
 * delete all students structs...
 */
void deleteStudents(student** s,int size){
    int i=0;
    for(i=0;i<size;i++){
        free(s[i]);
    }
    free(s);
}


/* input: student,inputPath,outputPath,comp.out path
 * output: non(fills student grade + answer , it uses alot of the other functions)
 */
void check(student* stud,char* inputPath,char* outputPath,char* compout){
    //will be used later
    char* cFilePath;
    char* outFile;

    //changing current WD to student directory
    chdir(stud->path);

    //find the c file:
    if((cFilePath=find(stud->path))==NULL){
        //printf("dont have c file in:%s\n",stud->path);
        strcpy(stud->answer,"NO_C_FILE");
        stud->score=0;
        return;
    }

    //compile the c file:
    if(compile(cFilePath) || (outFile=findOut(stud->path))==NULL){
        //printf("compile error in:%s\n",stud->path);
        strcpy(stud->answer,"COMPILATION_ERROR");
        stud->score=0;
        free(cFilePath);
        return;
    }

    //run the c file with input:
    char* result=(char*)calloc(Max,sizeof(char));
    char* output=(char*)calloc(outputLength,sizeof(char));
    output[0]='/';
    strcat(output,"output.txt");
    strcpy(result,stud->path);
    strcat(result,output);
    free(output);

    if(run(result,inputPath,outFile)){
        //printf("Timeout in:%s\n",stud->path);
        strcpy(stud->answer,"TIMEOUT");
        stud->score=0;
        free(result);
        free(cFilePath);
        free(outFile);
        return;
    }

    //getting final results:
    int final=compareForGrade(result,outputPath,compout);
    if(final==1){
        //they are differ
        strcpy(stud->answer,"BAD_OUTPUT");
        stud->score=60;

    }
    else if(final==2){
        //similar
        strcpy(stud->answer,"SIMILAR_OUTPUT");
        stud->score=80;

    }
    else{
        //identical
        strcpy(stud->answer,"GREAT_JOB");
        stud->score=100;

    }


    //comparing output's:

    free(result);
    free(cFilePath);
    free(outFile);

}


/* get the signal of alarm in case of timeout , change currentPid to notify
 * the parent that TIMEOUT have occured
 */
void alarm_hand(int sig){
    //killing the process in case of timeout
    signal(SIGALRM,alarm_hand);
    kill(currentpid,SIGKILL);
    //giving current pid
    currentpid=-1;
}


/* get comp.out file path (to use it for final grading), var to save WD
 * output:non(fills result with the comp.out path)
 */
void getCompOut(char* result,char* DirToSave){
    char cwd[Max];

    if (getcwd(cwd, sizeof(cwd)) != NULL){
        //save WD
        strcpy(DirToSave,cwd);
        DIR *pDir;
        char* outfile;
        struct dirent *library;
        if ( (pDir = opendir(cwd)) == NULL)
            return ;

        while ( (library = readdir(pDir) ) != NULL ){

            if(strcmp(library->d_name,"comp.out")==0){
                char* help=(char*)calloc(Max,sizeof(char));
                help[0]='/';
                strcpy(result,cwd);
                strcat(help,library->d_name);
                strcat(result,help);

                free(help);
                closedir(pDir);
                return;
            }


        }


        closedir( pDir );

    }

    //in case we couldn't find comp.out
    char Error[] = "Error, comp.out was not found, please try putting it near the .c file";
    write(2, Error, sizeof(Error) - 1);
    free(result);
    result=NULL;
    return;
}


/* input: students, number of students
 * output: non, write results to myResults.csv
 */
void writeResults(student** students,int size) {

    //creating table and file des:
    char cwd[Max];
    char result[Max];
    char mytable[]="myResults.csv";
    if (getcwd(cwd, sizeof(cwd)) != NULL) {
        char *help = (char *) calloc(Max, sizeof(char));
        help[0] = '/';
        strcpy(result, cwd);
        strcat(help, mytable);
        strcat(result, help);

        free(help);


    }

    int out = open(result, O_WRONLY | O_TRUNC | O_CREAT,
                   S_IRUSR | S_IRGRP | S_IWGRP | S_IWUSR);
    if(out<0){
        char fdError[]="Error in update Results.csv, file descriptor is Invalid";
        write(2,fdError,sizeof(fdError)-1);
        return;
    }

    //writing to table:
    int i=0;
    student* curr=NULL;
    char* message=NULL;
    char* end=NULL;

    for(i=0;i<size;i++){
        curr=students[i];
        //writing name
        message=(char*)calloc(Max,sizeof(char));
        strcpy(message,curr->name);
        write(out,message,strlen(message));
        write(out,",",2);
        free(message);

        //writing grade
        message=(char*)calloc(MaxArgs,sizeof(char));
        sprintf(message, "%d", curr->score);
        write(out,message,strlen(message));
        write(out,",",2);

        //writing feedBack
        message=(char*)calloc(Max,sizeof(char));
        strcpy(message,curr->answer);
        write(out,message,strlen(message));
        write(out,"\n",2);
        free(message);

    }


}


/* input: directory to follow, number of directory's in it(students)
 * output: all the students
 */
student** getStudents(char* libPath,int size){

    //open libPath:
    DIR *pDir;
    if ( (pDir = opendir(libPath)) == NULL)
        return NULL;

    //allocate array of students:
    student** students=(student**)calloc(size,sizeof(student*));
    if(students==NULL){
        char allocError[]="Error, allocation failed";
        write(2,allocError,sizeof(allocError)-1);
        return NULL;
    }

    //vars:
    int i=0;
    struct dirent *library;

    while ( (library = readdir(pDir) ) != NULL ){

        //if library is directory create student and add it
        if(strcmp(library->d_name,".")==0 || strcmp(library->d_name,"..")==0){
            //ignore because its not student
            continue;
        }
        //creating student directory path
        char* temp=(char*)calloc(Max,sizeof(char));
        char* help=(char*)calloc(Max,sizeof(char));
        help[0]='/';
        strcpy(temp,libPath);
        strcat(help,library->d_name);
        strcat(temp,help);


        DIR* dir = opendir(temp);
        //if dir exist creating student profile
        if (dir)
        {
            student* stud=(student*)calloc(1,sizeof(student));
            strcpy(stud->path,temp);
            strcpy(stud->name,library->d_name);
            int size=strlen(stud->name);
            stud->name[size]=0;
            stud->score=0;
            students[i]=stud;
            i++;
            closedir(dir);
        }
        free(temp);
        free(help);
    }
    closedir( pDir );


    return students;
}


/* input:directory of student
 * output: first c file we find( we assume only one exist->instructor approve)
 */
char* find(char* libPath){

    DIR *pDir=NULL;
    DIR *another=NULL;
    struct dirent *library;
    char* cPath=NULL;
    if ( (pDir = opendir(libPath)) == NULL)
        return NULL;

    while ( (library = readdir(pDir) ) != NULL ){
        //checking if name is directory

        if(strcmp(library->d_name,".")==0 || strcmp(library->d_name,"..")==0){
            //ignore because its not student
            continue;
        }

        char* string  = strrchr(library->d_name, '.');

        if( string != NULL &&  strcmp(string, ".c") ==0){
            cPath=(char*)calloc(Max,sizeof(char));
            char* help=(char*)calloc(Max,sizeof(char));
            help[0]='/';
            strcpy(cPath,libPath);
            strcat(help,library->d_name);
            strcat(cPath,help);

            free(help);
            closedir( pDir );


            return cPath;

        }

    }
    closedir( pDir );





    if ( (pDir = opendir(libPath)) == NULL)
        return NULL;

    while ( (library = readdir(pDir) ) != NULL ){
        //checking if name is directory

        if(strcmp(library->d_name,".")==0 || strcmp(library->d_name,"..")==0){
            //ignore because its not student
            continue;
        }

        if((another=opendir(library->d_name))!=NULL){
            char* anotherDir=(char*)calloc(Max,sizeof(char));
            char* help=(char*)calloc(Max,sizeof(char));
            help[0]='/';
            strcpy(anotherDir,libPath);
            strcat(help,library->d_name);
            strcat(anotherDir,help);

            free(help);
            cPath=find(anotherDir);
            closedir(another);
            free(anotherDir);
        }


    }



    return  cPath;

}


/* input:student dir
 * output: a.out from compilation
 */
char* findOut(char* libPath){
    DIR *pDir;
    char* outfile;
    struct dirent *library;
    if ( (pDir = opendir(libPath)) == NULL)
        return NULL;

    while ( (library = readdir(pDir) ) != NULL ){

        if(strcmp(library->d_name,"a.out")==0){
            outfile=(char*)calloc(Max,sizeof(char));
            char* help=(char*)calloc(Max,sizeof(char));
            help[0]='/';
            strcpy(outfile,libPath);
            strcat(help,library->d_name);
            strcat(outfile,help);

            free(help);
            closedir(pDir);

            return outfile;
        }


    }


    closedir( pDir );

    return  NULL;
}
