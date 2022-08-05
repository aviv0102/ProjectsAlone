/* name: Aviv Shisman
 * id:	 206558157
 */
 
 
//include:
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>

//Define:
#define ASCII_LITTLE_A 'a'
#define ASCII_LITTLE_Z 'z'
#define ASCII_BIG_A 'A'
#define ASCII_BIG_Z 'Z'
#define NewLine '\n'
#define Space ' '

//Declaration:
int isLetter(int);
int notEnd(char);

int main (int argc,char* argv[])
{
    //variables:
    int flag=0,res=2,len1=0,len2=0;
    char ch1='\0',ch2='\0';


    //checking arguments
    if(argc!=3){
        fprintf(stderr,"Error in number of arguments\n");
        return -1;
    }

    // initialize file descriptors with 'r' mode
    int fd1,fd2;
    fd1 = open(argv[1],O_RDONLY);
    if(fd1<0){
        fprintf(stderr,"Error in number of arguments\n");
        return -1;
    }

    fd2= open(argv[2],O_RDONLY);
    if(fd2<0){
        fprintf(stderr,"Error in number of arguments\n");
        return -1;
    }

    /* I used read  to read characters one by one, but in reality
     * it don't go to the disk every time to read (takes time)
     * it waits for k or all the reads and only then goes to the disk and takes the information.
     */
    while(read(fd1, &ch1, sizeof(char)) >0 &&  read(fd2, &ch2, sizeof(char) ) >0)
    {
        //reset res to not effect if's below
        res=1;

        //in case they equal we proceed:
        if(ch1==ch2){
            len1++;
            len2++;
           continue;
        }
	
        //if they not equal check if similar:(flag=1 ->similar or not equal)
        flag=1;

        //ignore newline or space
        while((ch1==Space || ch1==NewLine) && res>0){
            res=read(fd1, &ch1, sizeof(char));
        }
        while((ch2==Space || ch2==NewLine) && res>0 ){
            res=read(fd2, &ch2, sizeof(char) );
        }

        //in case they equal we after space/newline ignored
        if(ch1==ch2){
            len1++;
            len2++;
            continue;
        }
        else{
          //in case we have different characters->they might have different case
            if(isLetter(ch1) && isLetter(ch2) && abs(ch1-ch2)==Space) {
                len1++;
                len2++;
                continue;
            }
            // in case not equal
            else if(notEnd(ch1) &&notEnd(ch2)) {
                return 1;
            }
            //in case at the end one is space\newline and the other is character
            else if(len1==len2 && notEnd(ch1) && !notEnd(ch2)){
                return 1;
            }
            else if(len1==len2 && notEnd(ch2) && !notEnd(ch1)){
                return 1;
            }
        }

    }
    
    //in case one file is empty
    if(res==2 && (ch1=='\0' || ch2=='\0')){
    	return 1;
    }

    //in case in the end theres another letters
    if(read(fd1, &ch1, sizeof(char)) || read(fd2, &ch2, sizeof(char))){
        if(notEnd(ch1)|| notEnd(ch2)){
            return 1;
        }
    }

    //in case they similar
    if(flag==1){
        return 2;
    }

    close (fd1);
    close (fd2);

    return 0;
}


/*
Function checks whether char is a letter
input: letter (ASCII value)
output: whether it is a letter (ASCII) or not
*/
int isLetter(int ch)
{
    return ((ch >= ASCII_LITTLE_A && ch <= ASCII_LITTLE_Z) ||
            (ch >= ASCII_BIG_A && ch <= ASCII_BIG_Z));
}

int notEnd(char ch){
    if(ch!=Space && ch!=NewLine){
        return 1;
    }
    return 0;
}
