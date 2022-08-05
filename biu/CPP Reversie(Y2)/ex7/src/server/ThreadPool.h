
#ifndef SERVER_THREADPOOL_H
#define SERVER_THREADPOOL_H

#include <queue>
#include "Task.h"

using namespace std;

class ThreadPool {
public:
    ThreadPool(int size);
    ~ThreadPool();
    void addTask(Task*);
    void terminate();

private:
    queue<Task*> tasksQueue;
    pthread_t* threads;
    void executeTasks();
    bool stopped;
    pthread_mutex_t lock;
    static void *execute(void *arg);
};


#endif //SERVER_THREADPOOL_H
