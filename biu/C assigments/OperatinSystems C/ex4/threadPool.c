/* author: aviv shisman
 *     id: 206558157
 *
 *     enjoy :)
 */

//include:
#include "threadPool.h"



//declerations:
static void* work(void*);
void freePool(ThreadPool*);



/* Creating a Threadpool with n threads
 *
 * input: n number of threads
 * output: pointer to ThreadPool
 */
ThreadPool* tpCreate(int n){

    if(n <= 0) {
        return NULL;
    }


    //Create Pool and parameters:
    ThreadPool *pool=(ThreadPool *)malloc(sizeof(ThreadPool));
    pool->threads = (pthread_t *)malloc(sizeof(pthread_t) * n);
    pool->queue =osCreateQueue();
    pool->thread_count = 0;
    pool->count = 0;
    pool->shutdown = 0;

    if(pool->queue==NULL || pool==NULL || pool->threads==NULL){
        char allocError[] = "Error, malloc failed";
        write(2, allocError, sizeof(allocError) - 1);
        return NULL;
    }


    //creating mutex and cond:
    if((pthread_mutex_init(&(pool->lock), NULL) != 0) ||
       (pthread_cond_init(&(pool->notify), NULL) != 0)){
        char allocError[] = "Error, mutex creation failed";
        write(2, allocError, sizeof(allocError) - 1);
        return NULL;
    }

    // start the threads:
    int i;
    for(i = 0; i < n; i++) {
        if(pthread_create(&(pool->threads[i]), NULL,
                          work, (void*)pool) != 0) {
            tpDestroy(pool, 0);
            return NULL;
        }
        pool->thread_count++;
    }

    return pool;


}




/* Destroy the threadpool:
 *
 * can not assign anymore tasks to queue
 * param: threadpool the pool we want to destroy
 * param: shouldWaitForTasks ,if number is 0 wait only for running task else wait for all tasks(including queue)
 *
 */
void tpDestroy(ThreadPool* pool, int shouldWaitForTasks){
    printf("start des\n");

    if(pool == NULL) {
        char allocError[] = "Error,pool is Null can not Destroy it";
        write(2, allocError, sizeof(allocError) - 1);
        return;
    }

    //Lock
    if(pthread_mutex_lock(&(pool->lock)) != 0) {
        char allocError[] = "Error,can not lock in destroy";
        write(2, allocError, sizeof(allocError) - 1);
        return;
    }

    //if already in shutdown
    if(pool->shutdown!=0) {
        return;
    }


    if(shouldWaitForTasks!=0){
        pool->shutdown=2;//wait for other tasks
    }else{
        pool->shutdown = 1;// don't wait
    }


    // Wake up all worker threads
    if((pthread_cond_broadcast(&(pool->notify)) != 0) ||
       (pthread_mutex_unlock(&(pool->lock)) != 0)) {
        char allocError[] = "Error,can not unlock in destroy";
        write(2, allocError, sizeof(allocError) - 1);
        return;
    }


    if(shouldWaitForTasks!=0){
        pthread_mutex_lock (&pool->lock);
        if(shouldWaitForTasks!=0){
            printf("start of wait\n");

            pthread_cond_wait(&pool->notify,&pool->lock);
            printf("end of wait\n");

        }
        pthread_mutex_unlock (&pool->lock);
    }

    // Join all worker thread
    int i;
    for(i = 0; i < pool->thread_count; i++) {
        if(pthread_join(pool->threads[i], NULL) != 0) {
            char allocError[] = "Error, join failed";
            write(2, allocError, sizeof(allocError) - 1);
            return;
        }
    }
    freePool(pool);
    printf("end of des\n");


}





/* Add task to queue, Task will be executed when a thread is avialble
 *
 * param: threadpool
 * param: computeFunc -> pointer to computeFunc
 * param: param -> the paremeters
 */
int tpInsertTask(ThreadPool* pool, void (*computeFunc) (void *), void* param){

    //can not add task
    if(pool->shutdown!=0) {
        return -1;
    }

    //checking Params
    if(pool == NULL || computeFunc == NULL) {
        char allocError[] = "Error, pool or function ar null";
        write(2, allocError, sizeof(allocError) - 1);
        return -1;
    }

    //Lock:
    if(pthread_mutex_lock(&(pool->lock)) != 0) {
        char allocError[] = "Error, can not lock Queue";
        write(2, allocError, sizeof(allocError) - 1);
        return -1;
    }



    // Add task to queue
    threadpool_task* task=(threadpool_task*)calloc(1,sizeof(task));
    if(task==NULL){
        char allocError[] = "Error, can not allocate Task";
        write(2, allocError, sizeof(allocError) - 1);
        return -1;
    }
    task->function=computeFunc;
    task->argument=param;
    osEnqueue(pool->queue,task);
    pool->count += 1;

    // pthread_cond_broadcast and unlock!
    if(pthread_cond_signal(&(pool->notify)) != 0 ){
        char allocError[] = "Error, problem in Notify";
        write(2, allocError, sizeof(allocError) - 1);
        return -1;
    }

    //unlock
    if(pthread_mutex_unlock(&pool->lock) != 0){
        char allocError[] = "Error, problem in Unlocking Queue";
        write(2, allocError, sizeof(allocError) - 1);
        return -1;
    }

    return 0;

}




/* Threads Wait here for tasks and execute them
 *
 * input: void* Threadpool the pool
 */
static void* work(void *threadpool){

    ThreadPool *pool = (ThreadPool *)threadpool;
    threadpool_task* task=NULL;

    while(1) {

        // Lock must be taken to wait on conditional variable
        pthread_mutex_lock(&(pool->lock));

        //if we waited for all tasks to finish
        if(pool->shutdown==2 && pool->count==0){
            // notify main thread that queue is empty
            if((pthread_cond_broadcast(&(pool->notify)) != 0)){
                char allocError[] = "Error, problem in Notify";
                write(2, allocError, sizeof(allocError) - 1);
                return NULL;
            }
            break;
        }

        //wait for change, if the change is count or shutdown continue
        while(pool->count == 0) {
            pthread_cond_wait(&(pool->notify), &(pool->lock)); //when exit wait we get lock back

            //if it is shutdown go out
            if(pool->shutdown){
                break;
            }
        }

        //same as before (if thread waited we check again)
        if(pool->shutdown==2 && pool->count==0){
            if((pthread_cond_broadcast(&(pool->notify)) != 0)){
                char allocError[] = "Error, problem in Notify";
                write(2, allocError, sizeof(allocError) - 1);
                return NULL;
            }
            break;
        }


        // Do Task
        task=(threadpool_task*)osDequeue(pool->queue);
        pool->count -= 1;

        // Unlock
        pthread_mutex_unlock(&(pool->lock));

        /* Get to work */
        if(task!=NULL){
            (*(task->function))(task->argument);
            free(task);
        }



        //in case we don't run tasks from queue
        if(pool->shutdown ==1 ) {
            break;//don't take another tasks
        }



    }


    //in case of shutdown
    pthread_mutex_unlock(&(pool->lock));
    pthread_exit(NULL);

}


/*
 * free all memory that was allocated.
 */
void freePool(ThreadPool* pool){
    if(pool == NULL ) {
        return;
    }

    /* Did we manage to allocate ? */
    if(pool->threads) {
        free(pool->threads);
        osDestroyQueue(pool->queue);

        /* Because we allocate pool->threads after initializing the
           mutex and condition variable, we're sure they're
           initialized. Let's lock the mutex just in case. */
        pthread_mutex_lock(&(pool->lock));
        pthread_mutex_destroy(&(pool->lock));
        pthread_cond_destroy(&(pool->notify));
    }
    free(pool);
}