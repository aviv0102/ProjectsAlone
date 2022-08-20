/*aviv shisman 206558157
*rom sharon 209296235*/
#include "Server.h"
#include <fstream>
#include <iostream>
#include <sstream>

using namespace std;

int main(int argc, char *argv[]){
    //reading the port from file called sSettings
    ifstream settings;
    string line;
    int port = 0;
    if (argc <= 1){
        cout << "Error settings file did'nt entered" << endl;
        return 1;
    }
    settings.open(argv[1]);
    if (!settings.is_open()) {
        cout <<"Error opening settings file" << endl;
        return 1;
    }
    getline (settings,line);
    stringstream data(line);
    data >> port;
    //start the server
    Server server(port);
    server.start();
    settings.close();
}
