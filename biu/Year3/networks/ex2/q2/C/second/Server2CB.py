from socket import socket,AF_INET,SOCK_DGRAM

server_socket = socket(AF_INET, SOCK_DGRAM)
server_ip = '127.0.0.1'
server_port = 54321
server_socket.bind((server_ip, server_port))

data, sender_info = server_socket.recvfrom(2048)
print 'Received: ', data
data, sender_info = server_socket.recvfrom(2048)
print 'Received: ', data

for i in range(11):
    data, sender_info = server_socket.recvfrom(2048)
    print 'Received: ', data
    data, sender_info = server_socket.recvfrom(2048)
    print 'Received: ', data

data, sender_info = server_socket.recvfrom(2048)
server_socket.sendto('B', sender_info)
print 'Client disconnected'
server_socket.close()
