/*aviv shisman 206558157 and rom sharon
 * the server:
 */
#include "Server.h"
#include "CommandManeger.h"
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <string.h>

using namespace std;

#define MAX_CONNECTED_CLIENTS 6
/*
 * constructor
 */
Server::Server(int port) : port(port), serverSocket(0){
    cout << "Server" << endl;
}
/*
 * initializing the server and starting the server thread
 */
void Server::start(){
    string temp;
    int clientSocket1 = 0;
    vector<pthread_t>* threads = new vector<pthread_t>();
    pthread_t serverThread = 0;
    int counter = 0;
    serverSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (serverSocket == -1) {
        throw "Error opening socket";
    }
    // Assign a local address to the socket
    struct sockaddr_in serverAddress;
    bzero((void *) &serverAddress, sizeof(serverAddress));
    serverAddress.sin_family = AF_INET;
    //local host
    serverAddress.sin_addr.s_addr = INADDR_ANY;
    serverAddress.sin_port = htons(port);
    if (bind(serverSocket, (struct sockaddr *) &serverAddress, sizeof(serverAddress)) == -1) {
        throw "Error on binding";
    }
    // Start listening to incoming connections
    listen(serverSocket, MAX_CONNECTED_CLIENTS);

    // Define the client socket's structures
    struct sockaddr_in clientAddress;
    socklen_t clientAddressLen;
    int key = 0;

    pthread_create(&serverThread, NULL, acceptClients, (void *)&serverSocket);

    cout << "Enter 'exit' for close the server" << endl;
    do {
        cin >> temp;
        if (temp != "exit") {
            cout << "wrong command" << endl;
        }
    }while (temp != "exit");

    GameMap::getInstance()->closeGames();
    stop(serverThread);
}
/*
 * waiting for clients to connect.
 * @param serverSocket the main socket of the server
 * @return none
 */
void* Server::acceptClients(void * serverSocket) {
    vector<pthread_t>* threads = new vector<pthread_t>();
    int counter = 0;
    struct sockaddr_in clientAddress;
    socklen_t clientAddressLen;
    int clientSocket1 = 0;
    int server = *((int*)serverSocket);
    while (true) {
        cout << "Waiting for client connectios..." << endl;

        // Accept a new client connection
        clientSocket1 = accept(server, (struct sockaddr *)
                &clientAddress, &clientAddressLen);
        cout << "Client connected" << endl;
        //if accept had an error
        if (clientSocket1 == -1) {
            throw "Error on accept";
        }
        pthread_t temp;
        threads->push_back(temp);
        pthread_create(&threads->at(counter), NULL,handleClient,(void*)&clientSocket1);
        //the game
        counter++;
    }
}
/*
 * stopping the server..
 */
void Server::stop(pthread_t serverThreadId) {
    pthread_cancel(serverThreadId);
    close(serverSocket);
    cout << "Server stopped" << endl;
}
/*this function role is to take a command from the client
 * and take care of it(thread for each client)
 */
void* Server::handleClient(void * client) {
    //closing the server and clients sockets
    CommandsManager commandsManager;
    pthread_mutex_t command_mutex;
    int clientSocket = *((int*)client);
    int inGame = 0;
    vector<char*> *args = NULL;
    while (!inGame) {
        int i = 0;
        args= new vector<char*>;
        char buffer[100] = {'\0'};
        char command[100] = {'\0'};
        //reading the command
        int byte = read(clientSocket, buffer, sizeof(buffer));
        if (byte == -1) {
            cout << "Error reading player move" << endl;
            return NULL;
        }
        if (byte == 0) {
            cout << "Client disconnected" << endl;
            return NULL;
        }
        int flag = 1;
        int j = 0;
        char *param;
        //spliting the string to command and other args
        while (buffer[i] != '\0') {
            if (flag && buffer[i] != ' ') {
                command[i] = buffer[i];
            }
            if (buffer[i] == ' ') {
                if (!flag) {
                    args->push_back(param);
                }
                param = new char[100];
                flag = 0;
                j = 0;
                i++;
                continue;
            } else if (!flag) {
                param[j] = buffer[i];
            }
            i++;
            j++;
        }
        args->push_back(param);
        //each thread have the command maneger on his turn...
        pthread_mutex_lock(&command_mutex);
        inGame = commandsManager.executeCommand(command, args, clientSocket);
        pthread_mutex_unlock(&command_mutex);
    }
}
