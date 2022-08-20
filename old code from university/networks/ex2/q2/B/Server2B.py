import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '127.0.0.1'
server_port = 12469
server.bind((server_ip, server_port))
server.listen(5)


client_socket, client_address = server.accept()
print 'Connection from: ', client_address
data = client_socket.recv(1024)
print 'Received: ', data
data = client_socket.recv(1024)
print 'Received: ', data

for i in range(11):
    data = client_socket.recv(1024)
    print 'Received: ', data
    data = client_socket.recv(1024)
    print 'Received: ', data

data = client_socket.recv(1024)
client_socket.send('B')
print 'Client disconnected'
client_socket.close()
