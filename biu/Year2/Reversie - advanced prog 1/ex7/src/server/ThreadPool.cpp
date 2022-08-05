/* aviv shisman and rom sharon
 *
 */

#include <algorithm>
#include "ThreadPool.h"
#include <unistd.h>

/* constructor:
 * creating the threads and giving them a task
 */
ThreadPool::ThreadPool(int threadsNum) :
        stopped(false) {

    //creating threads and sending them
    threads = new pthread_t[threadsNum];
    for (int i = 0; i < threadsNum; i++) {
        pthread_create(threads + i, NULL, execute,
                       this);
    }
    pthread_mutex_init(&lock, NULL);
}

//sending the thread to execute task
void* ThreadPool::execute(void *arg) {
    ThreadPool *pool = (ThreadPool *)arg;
    pool->executeTasks();
}

/*
 * adding task to queue
 */
void ThreadPool::addTask(Task *task) {
    tasksQueue.push(task);
}

/*
 * execute the next task in the pool
 */
void ThreadPool::executeTasks() {
    while (!stopped) {
        pthread_mutex_lock(&lock);
        if (!tasksQueue.empty()) {
            Task* task = tasksQueue.front();
            tasksQueue.pop();
            pthread_mutex_unlock(&lock);
            task->execute();
        }
        else {
            pthread_mutex_unlock(&lock);
            sleep(1);
        }
    }
}

void ThreadPool::terminate() {
    pthread_mutex_destroy(&lock);
    stopped = true;
}
ThreadPool::~ThreadPool() {
    delete[] threads;
}