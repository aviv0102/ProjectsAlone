/*aviv shisman 206558157 and rom sharon
 * the server:
 */

#ifndef Server_H
#define Server_H


#include <sys/types.h>
#include <vector>

using namespace std;

class Server {
public:
    Server(int port);
    void start();
    static void* handleClient(void*);
    void stop(pthread_t);
    static void* acceptClients(void*);
private:
    int port;
    int serverSocket;
};

#endif