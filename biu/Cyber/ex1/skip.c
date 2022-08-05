// Compile on "u2" with "gcc -g -m32 -o skip skip.c" (ignore warning)
// Run on "u2" the command "./skip 0 0" to print 2048
// Run "./skip ? ?" to print the rightmost digit of you ID
// (discover the arguments ? ?, using gdb and disas)
// Submit the two arguments to moodle
#include <stdio.h>
#define SIZE ?? // replace ?? with the rightmost two digits of your ID

void func(int return_distance, int skip_distance)
{
    char buffer[SIZE];
    int *ret;
    ret = buffer + return_distance;
    (*ret) += skip_distance;
}

void main(int argc, char *argv[])
{
    int return_distance = atoi(argv[1]);
    int skip_distance = atoi(argv[2]);
    int x = 1024;
    int y = 2048;
    func(return_distance, skip_distance);
    switch(x)
    {
        case 0: y = 0; break;
        case 16: y = 1; break;
        case 32: y = 2; break;
        case 48: y = 3; break;
        case 64: y = 4; break;
        case 80: y = 5; break;
        case 96: y = 6; break;
        case 112: y = 7; break;
        case 128: y = 8; break;
        case 144: y = 9; break;
    }
    printf("%d\n",y);
}

