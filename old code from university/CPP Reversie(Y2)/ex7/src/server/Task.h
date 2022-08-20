//
// Created by magshimim on 21/01/18.
//

#ifndef SERVER_TASK_H
#define SERVER_TASK_H

#include <vector>
#include <map>
#include "Command.h"

class Task {
public:
    Task(void* (void*), int);
    void execute();
    pthread_t getT();
private:
    void * (*handleClient)(void *arg);
    int clientSocket;
    pthread_t thread;
};


#endif //SERVER_TASK_H
