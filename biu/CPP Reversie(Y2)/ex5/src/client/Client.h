/*aviv shisman and rom sharon
 * the client header:
 */

#ifndef ASS1_CLIENT_H
#define ASS1_CLIENT_H


#include "Point.h"
#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <string.h>
#include <unistd.h>

class Client {
public:
    Client(const char *serverIP, int serverPort);
    void connectToServer();
    int sendMove(int arg1, int arg2);
    void sentString(const char* str);
    Point* readMove();
    int recvKey();
    void start();
private:
    const char *serverIP;
    int serverPort;
    int clientSocket;
    void printMenu();
};


#endif //ASS1_CLIENT_H
