/* aviv shisman and rom sharon
 *
 */

#include "Task.h"

Task::Task(void *(*func)(void *), int cs) {
    this->handleClient = func;
    this->clientSocket = cs;


}

void Task::execute() {
    pthread_t temp;
    this->thread=temp;
    pthread_create(&this->thread, NULL,handleClient,(void*)&this->clientSocket);
}

pthread_t Task:: getT(){

    return this->thread;
}
