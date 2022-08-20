/*aviv shisman 206558157 and rom sharon*/

#include "Client.h"
#include <sstream>
#include <cstdio>
#include <string>
#include <bits/signum.h>
#include <signal.h>

using namespace std;

/*client constructor
 * creating the client
 */
Client::Client(const char *sIP, int sPort){
    serverIP = sIP;
    serverPort = sPort;
    clientSocket = 0;
}

int Client::sendMove(int arg1, int arg2){
    // giving the chosen point to the server
    int n = 1;
    signal(SIGPIPE, SIG_IGN);
    try {
        n = write(clientSocket,&arg1, sizeof(arg1));

    } catch (exception exception1){
        return 0;
    }
    if (n <= 0) {
        signal(SIGPIPE, SIG_IGN);
        return 0;
    }
    try {
        n = write(clientSocket,&arg2, sizeof(arg2));
    } catch (exception exception2){
        return 0;

    }
    if (n <= 0) {
        signal(SIGPIPE, SIG_IGN);
        return 0;
    }
    signal(SIGPIPE, SIG_IGN);

    return 1;
}
void Client::sentString(const char* str){
    int n = write(clientSocket,str, strlen(str)+1);
    if (n == -1) {
        throw "Error writing arg1 to socket";
    }
}
/*
 * recive which player are you 'x' or 'o'
 */
int Client::recvKey(){
    int key;
    int n = read(clientSocket, &key, sizeof(key));
    if (n == -1) {
        throw "Error reading result from socket";
    }
    return key;
}
/*
 * reading a move from Server
 */
Point* Client::readMove(){
    int x, y, end;
    cout << "Waiting for the other player to play..." << endl;
    // Read the new point from the server
    int n = read(clientSocket, &x, sizeof(x));
    if (n == -1) {
        throw "Error reading result from socket";
    }
    n = read(clientSocket, &y, sizeof(y));
    if (n == -1) {
        throw "Error reading result from socket";
    }
    return new Point(x, y);
}
/*
 * connecting to server...
 */
void Client::connectToServer(){
    // Create a socket
    clientSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (clientSocket == -1) {
        throw "Error opening socket";
    }

    // Convert the ip string to a network address
    struct in_addr address;
    if (!inet_aton(serverIP, &address)) {
        throw "Can't parse IP address";
    }

    // Get a hostent structure for the given host address
    struct hostent *server;
    server = gethostbyaddr((const void *) &address, sizeof(address), AF_INET);
    if (server == NULL) {
        throw "Host is unreachable";
    }

    // Create a structure for the server address
    struct sockaddr_in serverAddress;
    bzero((char *) &address, sizeof(address));
    serverAddress.sin_family = AF_INET;
    memcpy((char *) &serverAddress.sin_addr.s_addr, (char *) server->h_addr, server->h_length);

    // htons converts values between host and network byt orders
    serverAddress.sin_port = htons(serverPort);

    // Establish a connection with the TCP server
    if (connect(clientSocket, (struct sockaddr *) &serverAddress, sizeof(serverAddress)) == -1) {
        throw "Error connecting to server";
    }
    cout << "Connected to server" << endl;
}
/*starting the online game with asking for a command
 *printing the menu as well
 */
void Client::start() {
    int result = 0;

    printMenu();
    getchar();
    do {
        //getting a command from user
        string option;
        char buffer[100] = {'\0'};
        cout << "Enter you command here: " << endl;
        getline(std::cin, option);
        sentString(option.c_str());
        if (!strcmp("list_games", option.c_str())) {
            int n = read(clientSocket, buffer, sizeof(buffer));
            write(clientSocket, "y", sizeof("y"));

            while (buffer[0] != '$') {
                cout << buffer << endl;
                int n = read(clientSocket, buffer, sizeof(buffer));
                write(clientSocket, "y", sizeof("y"));

            }
        } else {
            //in case command is invalid(room full or name taken)
            int n = read(clientSocket, &result, sizeof(result));
            if(!result) {
                cout << "Error wrong command" << endl;
            }
            write(clientSocket, "y", sizeof("y"));
        }
    }while (result == 0);
}
/*
 * the menu function!
 */
void Client::printMenu() {
    cout << endl << "Hello player!!!" << endl;
    cout << "Welcome to the online game space" << endl;
    cout << "Here some usefull commands 4 you :)" << endl << endl;
    cout << "start <name> - to start new game called name" << endl;
    cout << "list_games   - get list of the open games you can join" << endl;
    cout << "join <name>  - join a player that currently waiting in the room-> name"<<endl;
    cout << "close <only in game> - in a game you have option of exiting" << endl;
}