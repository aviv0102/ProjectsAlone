'''
Aviv Shisman
Nadav gross
'''
from socket import socket, AF_INET, SOCK_DGRAM
import sys

#args:
server_ip = sys.argv[1]
server_port = sys.argv[2]

#creating socket and getting server port,ip and msg from client
s = socket(AF_INET, SOCK_DGRAM)
dest_ip = server_ip
dest_port = int(server_port)
msg = raw_input("Message to send: ")

#asking server for site ip
while not msg == 'quit':
    s.sendto(msg, (dest_ip,dest_port))
    data, sender_info = s.recvfrom(2048)
    print "Server sent: ", data
    msg = raw_input("Message to send: ")

s.close()
