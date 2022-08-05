import socket
import os.path



'''
Main
'''
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = '127.0.0.1'
    server_port = 12345
    server.bind((server_ip, server_port))
    server.listen(5)
    while True:
        client_socket, client_address = server.accept()
        print 'Connection from: ', client_address
        fileName=readMsg(client_socket)
        reactToMsg(client_socket,fileName)

        print 'Client disconnected'
        client_socket.close()

'''
get the content of the msg(the request itself)
'''
def readMsg(socket):
    #getting the file name from the request
    try:
        data = socket.recv(8192)
        lines=data.split('\r\n')
        line=lines[0]
        print 'Client request:'+line
        tokens=line.split(' ')
        token=tokens[1].split('/')
        FileName=token[1]
        for i in range (2,len(token)):
            FileName+='/'+token[i]
        if FileName=='':
            return 'index.html'
        else:
            return FileName
    except:
        print "something wrong in request format"

'''
react to the msg according to requirments
'''
def reactToMsg(socket,fileName):
    path='files/'+fileName

    if(fileName=='redirect'):
        response='HTTP/1.1 301 Moved Permanently\r\nConnection: close\r\nLocation: /result.html'
        response+='\r\n'
        socket.send(response)

    elif(os.path.isfile(path)):
        response='HTTP/1.1 200 OK\r\nConnection: close\r\n'
        response+='\r\n'
        if(not path.endswith('jpg')):
            file=open(path,'r')
            for line in file.readlines():
                response+=line+'\r\n'
            socket.send(response)
        else:
            socket.send(response)
            file = open(path, 'rb')
            data=file.read(1024)
            while data:
                socket.send(data)
                data = file.read(1024)

    else:
        response='HTTP/1.1 404 Not Found\r\nConnection: close\r\n'
        socket.send(response)

    return

if __name__ == '__main__':
    main()