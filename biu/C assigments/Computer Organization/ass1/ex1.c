//aviv shisman 206558157
#include "ex1.h"


int is_little_endian(){
    unsigned int num=1;
    /*                        00         01     02         03
     *little endian num : 00000001 00000000 00000000 00000000
     *big endian is this: 00000000 00000000 00000000 00000001
     */
    char* pointer=(char*)&num;
    //that way we get only the first byte in num because it will "think"
    // there is only one byte there.

    if(*pointer){
        return 1;//little endian *pointer= 00000001
    }
    return 0;
}

unsigned long merge_bytes(unsigned long x, unsigned long int y){
    if(is_little_endian()){
        //same as last time we take the lsb with the same method
        char* p1=(char*)&y;
        char* p2=(char*)&x;
        //we use pointers to switch
        *p2=*p1;

        return x;
    }
    //‫‪y‬‬ ‫=‬ ‫‪0x76543210ABCDEF19‬‬ ‫‪-‬‬ ‫ו‬ ‫‪x‬‬ ‫=‬ ‫‪0x89ABCDEF12893456 ‬

    //in this part we do the same thing just the way we take the lsb is different
    char* p1=(char*)&y;
    //we go to the end of the word because that's where the lsb is.(in big endian)
    p1=p1+7;
    char* p2=(char*)&x;
    p2=p2+7;
    *p2=*p1;

    return x;

}

unsigned long put_byte(unsigned long x, unsigned char b, int i){

    if(i>7){
        return 0;//error
    }

    if(is_little_endian()){

        char* p=(char*)&x;
        //finding the exact byte we want to replace and replace him manually
        p=p+i;
        *p=b;

        return x;
    }

    char* p=(char*)&x;
    //finding the exact by  te we want to replace and replace him manually
    //we go to the end for the lsb and then we go down because the lsb is the last memory address
    p=p+7-i;
    *p=b;
    return x;

}

