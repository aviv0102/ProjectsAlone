'''
Nadav gross 206844920
Aviv Shisman 206558157
'''

from socket import socket, AF_INET, SOCK_DGRAM
import sys


#getting args:
my_port = int(sys.argv[1])
parent_ip = sys.argv[2]
parent_port = int(sys.argv[3])
ips_file_name = sys.argv[4]


#creating socckets, binding
socket_client = socket(AF_INET, SOCK_DGRAM)
socket_parent = socket(AF_INET,SOCK_DGRAM)
#The server the talks with client   
source_ip = '172.18.6.183'   #The ip changes, we need to update it as well as giving the client

source_port = my_port
socket_client.bind((source_ip, source_port))
print source_ip  +":"+ str(my_port)+":" + parent_ip


#creating dictionary of adresses
ips = open(ips_file_name, 'r+')
lines = ips.readlines()
ips_dict = dict()
for line in lines:
    x = line.split(',')
    name = x[0]
    ip = x[1].rstrip()
    ips_dict[name] = ip

#starting the server
while True:
    data, sender_info = socket_client.recvfrom(2048)
    print "Message: ", data, " from: ", sender_info
    if (ips_dict.__contains__(data)):
        socket_client.sendto(ips_dict[data], sender_info)
    else:
        #asking parent for answer
        socket_parent.sendto(data, (source_ip, parent_port))
        data2, sender_info2 = socket_parent.recvfrom(2048)
        line = data + "," + data2 + "\n"
        ips.write(line)
        ips_dict[data] = data2
        socket_client.sendto(ips_dict[data], sender_info)