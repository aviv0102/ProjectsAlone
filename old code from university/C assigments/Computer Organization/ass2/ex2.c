//aviv shisman 206558157

#include <stdio.h>
//this library is for strcmp
#include <memory.h>


//declerations:
void regularCopy(char* ,char* );
void copyBetweenOS(char*,char*,char*,char*,int);
void byteSwapOSCopy(char*,char*,char*,char*,char*);
short swap(short a);

//main function:
int main(int argc, char **argv) {


    if(argc==3){
        regularCopy(argv[1],argv[2]);
    }
    if(argc==5){
        copyBetweenOS(argv[1],argv[2],argv[3],argv[4],0);
    }
    if(argc==6){
        byteSwapOSCopy(argv[1],argv[2],argv[3],argv[4],argv[5]);
    }

    return 0;
}


/*regular copy without any flags
 * using fopen and fread
 */
void regularCopy(char* src,char* des){
    //opening the file
    FILE* fp1=fopen(src,"rb");
    //creating the new file
    FILE* fp2=fopen(des,"wb");
    //creating a buffer
    short buffer[1];
    //reading the file to the buffer if fread returns 0
    //it means we got to the end of file
    while(fread(buffer, 2*sizeof(char),1,fp1)){
        //writing to the new file
        fwrite(buffer,2*sizeof(char), 1,fp2);
    }
    //closing the stream
    fclose(fp1);
    fclose(fp2);

}
/*special copy between different os's.
 * replacing the new line endings.
 */
void copyBetweenOS(char* src ,char* des ,char* srcOS,char* desOS,int action){
    //checking input
    if(strcmp(srcOS,desOS)){
        regularCopy(src,des);
    }

    //variables that will save the line endings
    short oldLine[2];
    short newLine[2];

    //checking which copy need to preform
    if(strcmp(srcOS,"-win")==0){
        if(strcmp(desOS,"-mac")==0){
            oldLine[0]=0x000d;
            oldLine[1]=0x000a;
            newLine[0]=0x000d;
            newLine[1]=0x0000;
        }
        if(strcmp(desOS,"-unix")==0){
            oldLine[0]=0x000d;
            oldLine[1]=0x000a;
            newLine[0]=0x000a;
            newLine[1]=0x0000;
        }
    }

    if(strcmp(srcOS,"-mac")==0){
        if(strcmp(desOS,"-win")==0){
            oldLine[0]=0x000d;
            oldLine[1]=0x0000;
            newLine[0]=0x000d;
            newLine[1]=0x000a;
        }
        if(strcmp(desOS,"-unix")==0){

            oldLine[0]=0x000d;
            oldLine[1]=0x0000;
            newLine[0]=0x000a;
            newLine[1]=0x0000;
        }
    }

    if(strcmp(srcOS,"-unix")==0){
        if(strcmp(desOS,"-win")==0){
            oldLine[0]=0x000a;
            oldLine[1]=0x0000;
            newLine[0]=0x000d;
            newLine[1]=0x000a;
        }
        if(strcmp(desOS,"-mac")==0){
            oldLine[0]=0x000a;
            oldLine[1]=0x0000;
            newLine[0]=0x000d;
            newLine[1]=0x0000;
        }
    }

    //opening the file
    FILE* fp1=fopen(src,"rb");
    //creating the new file
    FILE* fp2=fopen(des,"wb");
    //creating a buffer
    short buffer[1];
    size_t count=1;
    int flag=0;
    while(fread(buffer, sizeof(short),count,fp1)){

        //changing line endings
        if (*buffer== oldLine[0] || *buffer==swap(oldLine[0])) {
            //if the short is big endian
            if(*buffer==swap(oldLine[0])){
                *buffer=swap(newLine[0]);
                flag++;
            }
            else{
                *buffer = newLine[0];
            }
            //if action is 1 it means byte swap is on
            if(action==1){
                *buffer=swap(*buffer);
            }


            fwrite(buffer,sizeof(short), count,fp2);
            //if desOS is windows
            if(newLine[1]!=0x0000){
                //if short is big endian we write line ending in big endian
                if(flag){
                    *buffer=swap(newLine[1]);
                }else{
                    *buffer = newLine[1];
                }
                if(action==1){
                    *buffer=swap(*buffer);
                }
                fwrite(buffer,sizeof(short),count,fp2);

            }
            continue;
        }

        //if srcOS is windows
        if(*buffer==oldLine[1] || *buffer==swap(oldLine[1])){
            continue;
        }

        //agian if action is 1 it means we activated byte swap
        if(action==1){
            *buffer=swap(*buffer);
        }
        //writing to the new file
        fwrite(buffer,sizeof(short), count,fp2);
    }
    //closing the stream
    fclose(fp1);
    fclose(fp2);

}
/*the byte swap function that uses
 * the copyBetweenOS function it gets the same paramters with the addition of
 * action,action=0 means keep etc...
 */
void byteSwapOSCopy(char* src ,char* des,char* srcOS,char* desOS,char* action){
    if(strcmp(action,"-keep")==0){
        copyBetweenOS(src,des,srcOS,desOS,0);
    }
    else if(strcmp(action,"-swap")==0)
    {
        copyBetweenOS(src,des,srcOS,desOS,1);
    }
}

/*
 * simple swap function that do a swap with a single bytes
 * using the same trick we used in ex1
 */
short swap(short a){
    char* p1=(char*)&a;
    char* p2=(char*)&a;
    p2=p2+1;
    char temp=*p1;
    *p1=*p2;
    *p2=temp;

    return a;
}