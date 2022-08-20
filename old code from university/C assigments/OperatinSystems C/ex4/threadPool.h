#ifndef __THREAD_POOL__
#define __THREAD_POOL__


//include:
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <stdio.h>
#include "osqueue.h"


/**
 *  @struct threadpool_task
 *  @var function Pointer to the function that will perform the task.
 *  @var argument Argument to be passed to the function.
 */
typedef struct {
    void (*function)(void *);
    void *argument;
} threadpool_task;

/**
 * ThreadPool:
 *
 *  notify       Condition variable to notify worker threads.
 *  threads      Array containing worker threads ID.
 *  thread_count Number of threads
 *  queue        Queue of tasks.
 *  count        Number of pending tasks
 *  shutdown     Flag indicating if the pool is shutting down
 */
typedef struct thread_pool
{
    pthread_mutex_t lock;
    pthread_cond_t notify;
    pthread_t *threads;
    OSQueue* queue;
    int thread_count;
    int count;
    int shutdown;
}ThreadPool;

ThreadPool* tpCreate(int numOfThreads);

void tpDestroy(ThreadPool* threadPool, int shouldWaitForTasks);

int tpInsertTask(ThreadPool* threadPool, void (*computeFunc) (void *), void* param);

#endif
